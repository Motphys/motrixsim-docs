# Copyright (C) 2020-2026 Motphys Technology Co., Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.controller import KeyboardCommandAdapter
from utils.policy import G1LocomotionPolicy, G1Policy12Dof, Go1LocomotionPolicy, Go2LocomotionPolicy
from utils.robot import G1Robot, G1Robot12Dof, Go1Robot, Go2Robot
from utils.terrain_scan_visualizer import TerrainScanVisualizer

from motrixsim import GeomHField, SceneData, TerrainScanner, msd
from motrixsim.render import Layout, RenderApp, RenderSettings

DEFAULT_SCENE = "playground"
SCENE_FILES = {
    "plane": "examples/assets/common/flat_scene_with_ssgi.xml",
    "parlour": "examples/assets/parlour/parlour.xml",
    "playground": "examples/assets/ssgi/ssgi_on.xml",
    "stairs": "examples/assets/common/terrain_stairs.xml",
}

ROBOT_CONFIGS = {
    "g1": {
        "robot": G1Robot,
        "policy": G1LocomotionPolicy,
        "camera_position": [-1.5, 0, 1.0],
    },
    "g1_12dof": {
        "robot": G1Robot12Dof,
        "policy": G1Policy12Dof,
        "camera_position": [-1.5, 0, 1.0],
        "timestep": 0.005,
    },
    "go1": {
        "robot": Go1Robot,
        "policy": Go1LocomotionPolicy,
        "camera_position": [-2, 0, 0.5],
    },
    "go2": {
        "robot": Go2Robot,
        "policy": Go2LocomotionPolicy,
        "camera_position": [-2, 0, 0.5],
    },
}


ROBOT_SCENE_OVERRIDES = {
    ("g1", "stairs"): "g1_12dof",
}
SCENE_CAMERA_OVERRIDES = {
    "stairs": {
        "camera_position": [-2.4, 0, 1.15],
        "camera_fovy": 65,
    },
}
DEFAULT_TERRAIN_SCAN_SCENES = {"stairs"}
ROBOT_CHOICES = ("g1", "go1", "go2")
ROBOT_LIDAR_MOUNTS = {
    G1Robot: {
        "name": "g1",
        "link": "torso_link",
        "pos": (0.0, 0.0, 0.52),
    },
    G1Robot12Dof: {
        "name": "g1",
        "link": G1Robot12Dof.base_link_name,
        "pos": (0.0, 0.0, 0.56),
    },
    Go1Robot: {
        "name": "go1",
        "link": Go1Robot.base_link_name,
        "pos": (0.25, 0.0, 0.12),
    },
    Go2Robot: {
        "name": "go2",
        "link": Go2Robot.base_link_name,
        "pos": (0.25, 0.0, 0.12),
    },
}
LIDAR_PROFILE_DIR = Path(__file__).resolve().parent.parent / "assets" / "lidar-profiles"
LIDAR_CATALOG_PATH = LIDAR_PROFILE_DIR / "catalog.xml"
DEFAULT_TERRAIN_SCAN_OFFSETS = np.array(
    [(x, y) for x in np.linspace(-0.8, 0.8, 8) for y in np.linspace(-0.8, 0.8, 8)],
    dtype=np.float32,
)


def load_lidar_profile_rates(catalog_path: Path = LIDAR_CATALOG_PATH) -> dict[str, float]:
    """Return the fixed scan rate of every profile reachable from the catalog."""
    profile_rates: dict[str, float] = {}
    visited: set[Path] = set()

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in visited:
            return
        visited.add(path)
        root = ET.parse(path).getroot()
        for include in root.findall("include"):
            visit(path.parent / include.attrib["file"])
        for lidar in root.findall("./asset/lidar"):
            name = lidar.attrib["name"]
            hzrange = [float(value) for value in lidar.attrib["hzrange"].split()]
            if len(hzrange) != 2 or hzrange[0] != hzrange[1]:
                raise ValueError(f"lidar profile '{name}' must define one fixed hzrange")
            if name in profile_rates:
                raise ValueError(f"duplicate lidar profile '{name}'")
            profile_rates[name] = hzrange[0]

    visit(catalog_path)
    return profile_rates


LIDAR_PROFILE_RATES = load_lidar_profile_rates()
LIDAR_PROFILE_CHOICES = tuple(LIDAR_PROFILE_RATES)


def load_robot_lidar(robot_class: type, profile: str) -> msd.World:
    """Compile a selected catalog profile and the robot-specific mounting site to MSD."""
    try:
        hz = LIDAR_PROFILE_RATES[profile]
    except KeyError as exc:
        raise ValueError(f"unknown lidar profile '{profile}'") from exc
    try:
        mount = ROBOT_LIDAR_MOUNTS[robot_class]
    except KeyError as exc:
        raise ValueError(f"no lidar mount defined for robot class '{robot_class.__name__}'") from exc

    sensor_name = f"{mount['name']}_lidar"
    site_name = f"{mount['name']}_lidar_site"
    site_pos = " ".join(f"{value:g}" for value in mount["pos"])

    lidar_mount_mjcf = f"""<mujoco model="{mount["name"]}_lidar_mount">
  <include file="catalog.xml" />
  <worldbody>
    <site name="{site_name}" pos="{site_pos}"
      quat="0.5 0.5 0.5 0.5" rgba="0 1 0.2 1" size="0.015" />
  </worldbody>
  <sensor>
    <lidar name="{sensor_name}" site="{site_name}"
      asset="{profile}" exclude="parentsubtree" hz="{hz:g}" />
  </sensor>
</mujoco>"""
    source_path = LIDAR_PROFILE_DIR / "robot_locomotion_lidar.xml"
    return msd.from_str(lidar_mount_mjcf, file_path=str(source_path))


def attach_robot_lidar(robot: msd.World, robot_class: type, profile: str) -> None:
    """Attach one selected catalog lidar profile to a supported robot."""
    mount = ROBOT_LIDAR_MOUNTS[robot_class]
    robot.attach(load_robot_lidar(robot_class, profile), mount["link"])


def build_model(
    scene_file: str,
    robot_class: type,
    camera_position: list[float],
    camera_fovy: float,
    lidar_profile: str | None = None,
    extra_worlds=None,
    head_camera: dict | None = None,
):
    """Build a locomotion scene and attach the selected robot and follower camera.

    When ``head_camera`` is provided, a first-person camera is also attached to the given
    robot link and returned as the third tuple element (otherwise ``None``). It renders to
    an offscreen image so it can be shown as an on-screen viewport widget.
    """
    scene = msd.from_file(scene_file)
    robot = msd.from_file(robot_class.mjcf_path)

    camera_mjcf = f"""<mujoco model="camera">
  <worldbody>
    <camera name="follower" pos="{" ".join(str(x) for x in camera_position)}"
      xyaxes="0 -1 0 0 0 1" fovy="{camera_fovy}" trackposspeed="2" trackrotspeed="2" />
  </worldbody>
</mujoco>"""
    camera = msd.from_str(camera_mjcf)
    robot.attach(camera, robot_class.base_link_name)

    if lidar_profile is not None:
        attach_robot_lidar(robot, robot_class, lidar_profile)
        scene.visual.sensor.lidar_point_cloud.point_size_px = 6.0
        scene.visual.sensor.lidar_point_cloud.max_color_distance = 12.0

    if head_camera is not None:
        head_pos = " ".join(str(x) for x in head_camera["pos"])
        head_xyaxes = head_camera.get("xyaxes", "0 -1 0 0 0 1")
        head_fovy = head_camera.get("fovy", 70)
        head_mjcf = f"""<mujoco model="head_camera">
  <worldbody>
    <camera name="head" pos="{head_pos}" xyaxes="{head_xyaxes}" fovy="{head_fovy}" />
  </worldbody>
</mujoco>"""
        robot.attach(msd.from_str(head_mjcf), head_camera["link"])

    scene.attach(robot)
    for extra_world in extra_worlds or ():
        scene.attach(extra_world)

    model = scene.build()
    camera = model.cameras["follower"]
    camera.rotation_track = "look_at_link"
    camera.position_track = "fixed_local"
    camera.track_target_link = model.get_link(robot_class.base_link_name)

    head_cam = None
    if head_camera is not None:
        head_cam = model.cameras["head"]
        width, height = head_camera.get("resolution", (480, 360))
        # Render this camera offscreen so a viewport widget can display its output.
        head_cam.set_render_target("image", width, height)

    return model, camera, head_cam


def run_locomotion(
    robot: str,
    scene: str,
    *,
    scene_file: str | None = None,
    camera_position: list[float] | None = None,
    camera_fovy: float | None = None,
    head_camera: dict | None = None,
    lidar_profile: str | None = None,
):
    # Stairs scene only supports G1 robot
    if scene == "stairs" and robot != "g1":
        raise ValueError(f"stairs scene only supports g1 robot, got '{robot}'")
    if scene_file is None:
        scene_file = SCENE_FILES[scene]

    render_settings = RenderSettings(
        simplify_render_mesh=True,
        enable_shadow=True,
        enable_ssao=False,
        enable_oit=False,
        share_lights_between_envs=False,
        enable_ssgi=True,
    )

    robot_name = ROBOT_SCENE_OVERRIDES.get((robot, scene), robot)
    robot_config = ROBOT_CONFIGS[robot_name]
    RobotClass = robot_config["robot"]
    PolicyClass = robot_config["policy"]
    scene_name = scene
    camera_config = SCENE_CAMERA_OVERRIDES.get(scene_name, {})
    if camera_position is None:
        camera_position = camera_config.get("camera_position", robot_config["camera_position"])
    if camera_fovy is None:
        camera_fovy = camera_config.get("camera_fovy", 45)
    show_terrain_scan = scene_name in DEFAULT_TERRAIN_SCAN_SCENES
    terrain_scan_offsets = DEFAULT_TERRAIN_SCAN_OFFSETS
    extra_worlds = []
    if show_terrain_scan:
        extra_worlds.append(TerrainScanVisualizer.create_msd(terrain_scan_offsets))
    model, camera, head_cam = build_model(
        scene_file,
        RobotClass,
        camera_position,
        camera_fovy,
        lidar_profile=lidar_profile,
        extra_worlds=extra_worlds,
        head_camera=head_camera,
    )
    if "timestep" in robot_config:
        model.options.timestep = robot_config["timestep"]

    # Create robot (state accessor only)
    body = model.get_body(RobotClass.base_link_name)
    robot = RobotClass(body)

    # Create policy (behavior logic with integrated ONNX inference)
    policy = PolicyClass(
        robot=robot,
    )
    terrain_scan_visualizer = None
    if show_terrain_scan:
        terrain = model.get_geom("floor")
        if not isinstance(terrain, GeomHField):
            raise ValueError("--show-terrain-scan requires a scene whose 'floor' geom is a height field")
        scanner = TerrainScanner(
            terrain=terrain,
            frame=model.get_link(RobotClass.base_link_name),
            offsets=terrain_scan_offsets,
            alignment="yaw",
            output="height",
        )
        terrain_scan_visualizer = TerrainScanVisualizer.from_model(
            model=model,
            scanner=scanner,
            frame=model.get_link(RobotClass.base_link_name),
            offsets=terrain_scan_offsets,
        )

    # Create keyboard adapter
    keyboard_adapter = KeyboardCommandAdapter()

    # Initialize simulation data
    data = SceneData(model)
    step = 0
    print(f"Controlling {robot_name.upper()} robot in {scene_name} scene")
    print("Keyboard Controls:")
    print("- Press W / Up Arrow to move forward")
    print("- Press S / Down Arrow to move backward")
    print("- Press Left Arrow to move left")
    print("- Press Right Arrow to move right")
    print("- Press A to rotate left")
    print("- Press D to rotate right")
    print("- Press ESC to exit")

    # Create render window for visualization
    with RenderApp() as render:
        # Configure camera to look at robot
        render.set_main_camera(camera)

        # Launch the render instance of the model
        render.launch(model, render_settings=render_settings)
        if lidar_profile is not None:
            render.opt.set_lidar_point_vis(True)

        # Show the robot's head camera as an on-screen viewport widget. This also puts
        # multiple Gaussian-splat cameras (window + head) on screen at once, which is the
        # scenario the multi-camera 3DGS sort fix targets.
        if head_cam is not None:
            head_layout = (head_camera or {}).get("layout", Layout(right=16, top=16, width=360, height=270))
            render.widgets.create_camera_viewport(head_cam, layout=head_layout)

        # Initialize timing control
        phys_dt = model.options.timestep
        contrl_dt = 0.02
        render_fps = 60.0
        render_dt = 1.0 / render_fps

        n_ctrl = max(1, round(contrl_dt / phys_dt))
        n_render = max(1, round(render_dt / phys_dt))

        # Main loop
        while True:
            # Check if render window is closed
            if render.is_closed:
                break
            # === Physics update phase ===

            if hasattr(policy, "pre_physics_step"):
                policy.pre_physics_step(data)
            model.step(data)
            step += 1

            if step % n_ctrl == 0:
                # control update
                need_reset = policy.step(data, keyboard_adapter.command)
                if need_reset:
                    data = SceneData(model)
                    if hasattr(policy, "reset"):
                        policy.reset()
                    step = 0

            # === Render update phase ===
            # Update keyboard input
            keyboard_adapter.update_from_input(render.input)

            # Check ESC key to exit
            if render.input.is_key_just_pressed("escape"):
                break
            if step % n_render == 0:
                if terrain_scan_visualizer is not None:
                    terrain_scan_visualizer.update(data)
                    model.forward_kinematic(data)
                # Sync rendering (also processes input events)
                render.sync(data)


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Keyboard control for robots")
    parser.add_argument(
        "--robot",
        type=str,
        choices=ROBOT_CHOICES,
        default="go2",
        help="Robot type to control (default: go2)",
    )
    parser.add_argument(
        "--scene",
        type=str,
        choices=sorted(SCENE_FILES),
        default=DEFAULT_SCENE,
        help=f"Scene type to load (default: {DEFAULT_SCENE})",
    )
    parser.add_argument(
        "--lidar",
        choices=LIDAR_PROFILE_CHOICES,
        default=None,
        metavar="PROFILE",
        help="Lidar profile to attach to the selected robot; see --list-lidars (default: no lidar)",
    )
    parser.add_argument(
        "--list-lidars",
        action="store_true",
        help="List available lidar profiles and exit",
    )
    return parser


def main():
    parser = create_argument_parser()
    args = parser.parse_args()
    if args.list_lidars:
        print("\n".join(LIDAR_PROFILE_CHOICES))
        return

    try:
        run_locomotion(args.robot, args.scene, lidar_profile=args.lidar)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
