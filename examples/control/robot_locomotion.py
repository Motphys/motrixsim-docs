# Copyright (C) 2020-2025 Motphys Technology Co., Ltd. All Rights Reserved.
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
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.controller import KeyboardCommandAdapter
from utils.policy import G1LocomotionPolicy, G1Policy12Dof, Go1LocomotionPolicy, Go2LocomotionPolicy
from utils.robot import G1Robot, G1Robot12Dof, Go1Robot, Go2Robot
from utils.terrain_scan_visualizer import TerrainScanVisualizer

from motrixsim import GeomHField, SceneData, TerrainScanner, msd
from motrixsim.render import RenderApp, RenderSettings

DEFAULT_SCENE = "plane"
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
DEFAULT_TERRAIN_SCAN_OFFSETS = np.array(
    [(x, y) for x in np.linspace(-0.8, 0.8, 8) for y in np.linspace(-0.8, 0.8, 8)],
    dtype=np.float32,
)


def build_model(
    scene_name: str,
    robot_class: type,
    camera_position: list[float],
    camera_fovy: float,
    extra_worlds=None,
):
    """Build a locomotion scene and attach the selected robot and follower camera."""
    scene = msd.from_file(SCENE_FILES[scene_name])
    robot = msd.from_file(robot_class.mjcf_path)

    camera_mjcf = f"""<mujoco model="camera">
  <worldbody>
    <camera name="follower" pos="{" ".join(str(x) for x in camera_position)}"
      xyaxes="0 -1 0 0 0 1" fovy="{camera_fovy}" trackposspeed="2" trackrotspeed="2" />
  </worldbody>
</mujoco>"""
    camera = msd.from_str(camera_mjcf)
    robot.attach(camera, robot_class.base_link_name)
    scene.attach(robot)
    for extra_world in extra_worlds or ():
        scene.attach(extra_world)

    model = scene.build()
    camera = model.cameras["follower"]
    camera.rotation_track = "look_at_link"
    camera.position_track = "fixed_local"
    camera.track_target_link = model.get_link(robot_class.base_link_name)
    return model, camera


def main():
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
    args = parser.parse_args()

    # Stairs scene only supports G1 robot
    if args.scene == "stairs" and args.robot != "g1":
        parser.error(f"stairs scene only supports g1 robot, got '{args.robot}'")

    render_settings = RenderSettings(
        simplify_render_mesh=True,
        enable_shadow=True,
        enable_ssao=False,
        enable_oit=False,
        share_lights_between_envs=False,
        enable_ssgi=True,
    )

    robot_name = ROBOT_SCENE_OVERRIDES.get((args.robot, args.scene), args.robot)
    robot_config = ROBOT_CONFIGS[robot_name]
    RobotClass = robot_config["robot"]
    PolicyClass = robot_config["policy"]
    scene_name = args.scene
    camera_config = SCENE_CAMERA_OVERRIDES.get(scene_name, {})
    camera_position = camera_config.get("camera_position", robot_config["camera_position"])
    camera_fovy = camera_config.get("camera_fovy", 45)
    show_terrain_scan = scene_name in DEFAULT_TERRAIN_SCAN_SCENES
    terrain_scan_offsets = DEFAULT_TERRAIN_SCAN_OFFSETS
    extra_worlds = []
    if show_terrain_scan:
        extra_worlds.append(TerrainScanVisualizer.create_msd(terrain_scan_offsets))
    model, camera = build_model(
        scene_name,
        RobotClass,
        camera_position,
        camera_fovy,
        extra_worlds=extra_worlds,
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


if __name__ == "__main__":
    main()
