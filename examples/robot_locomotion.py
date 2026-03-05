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

from utils.controller import KeyboardCommandAdapter
from utils.policy import G1LocomotionPolicy, Go1LocomotionPolicy, Go2LocomotionPolicy
from utils.robot import G1Robot, Go1Robot, Go2Robot

from motrixsim import SceneData, msd
from motrixsim.render import RenderApp

# Camera positions for different robot types
camera_positions = {
    "g1": [-1.5, 0, 1.0],
    "go1": [-2, 0, 0.5],
    "go2": [-2, 0, 0.5],
}


def main():
    parser = argparse.ArgumentParser(description="Keyboard control for robots")
    parser.add_argument(
        "--robot",
        type=str,
        choices=["g1", "go1", "go2"],
        default="go2",
        help="Robot type to control (default: go2)",
    )
    parser.add_argument(
        "--scene",
        type=str,
        choices=["plane", "parlour"],
        default="plane",
        help="Scene type to load (default: plane)",
    )

    args = parser.parse_args()

    # Select scene file based on argument
    if args.scene == "plane":
        scene_file = "examples/assets/common/flat_scene.xml"
    else:  # parlour
        scene_file = "examples/assets/parlour/parlour.xml"

    # Select robot configuration based on argument
    if args.robot == "g1":
        RobotClass = G1Robot
        PolicyClass = G1LocomotionPolicy
    elif args.robot == "go1":
        RobotClass = Go1Robot
        PolicyClass = Go1LocomotionPolicy
    else:  # go2
        RobotClass = Go2Robot
        PolicyClass = Go2LocomotionPolicy

    # Load the scene model
    scene = msd.from_file(scene_file)
    robot = msd.from_file(RobotClass.mjcf_path)
    # Build camera MJCF with robot-specific position
    pos = camera_positions[args.robot]
    camera_mjcf = f"""<mujoco model="camera">
  <worldbody>
    <camera name="follower" pos="{" ".join(str(x) for x in pos)}"
      xyaxes="0 -1 0 0 0 1" trackposspeed="2" trackrotspeed="2" />
  </worldbody>
</mujoco>"""
    camera = msd.from_str(camera_mjcf)
    robot.attach(camera, RobotClass.base_link_name)

    scene.attach(robot)

    model = scene.build()

    camera = model.cameras["follower"]
    camera.rotation_track = "look_at_link"
    camera.position_track = "fixed_local"
    camera.track_target_link = model.get_link(RobotClass.base_link_name)

    # Create robot (state accessor only)
    body = model.get_body(RobotClass.base_link_name)
    robot = RobotClass(body)

    # Create policy (behavior logic with integrated ONNX inference)
    policy = PolicyClass(
        robot=robot,
    )

    # Create keyboard adapter
    keyboard_adapter = KeyboardCommandAdapter()

    # Initialize simulation data
    data = SceneData(model)
    step = 0
    print(f"Controlling {args.robot.upper()} robot")
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
        render.launch(model)

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

            model.step(data)
            step += 1

            if step % n_ctrl == 0:
                # control update
                need_reset = policy.step(data, keyboard_adapter.command)
                if need_reset:
                    data = SceneData(model)
                    step = 0

            # === Render update phase ===
            # Update keyboard input
            keyboard_adapter.update_from_input(render.input)

            # Check ESC key to exit
            if render.input.is_key_just_pressed("escape"):
                break
            if step % n_render == 0:
                # Sync rendering (also processes input events)
                render.sync(data)


if __name__ == "__main__":
    main()
