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

from collections import deque

import numpy as np
from absl import app, flags

from motrixsim import SceneData, load_model, run, step
from motrixsim.render import CaptureTask, RenderApp

_Obj = flags.DEFINE_string("object", "cube", "object to grasp, Choices: [cube, ball, bottle]")
_Shake = flags.DEFINE_boolean("shake", True, "whether to shake the arm after grasping, Choices: [True, False]")
_Record = flags.DEFINE_boolean("record", False, "whether to record the simulation, Choices: [True, False]")


def lerp(a, b, t):
    return a + t * (b - a)


init_qpos = np.array([0.0, 0.0, 0.0, -1.5708, 0.0, 1.5708, -0.7853, 0.04, 0.04])
grasp_qpos = np.array([-1.0104, 1.5623, 1.3601, -1.6840, -1.5863, 1.7810, 1.4598, 0.04, 0.04])
lift_qpos = np.array([-1.0426, 1.4028, 1.5634, -1.7114, -1.4055, 1.6015, 1.4510, 0.0, 0.0])


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def main(argv):
    # Create render window for visualization
    with RenderApp() as render:
        render.opt.set_left_panel_vis(True)

        # The scene description file
        path = f"examples/assets/franka_emika_panda/scene_pick_{_Obj.value}.xml"
        # Load the scene model
        model = load_model(path)
        cameras = model.cameras
        cameras[0].set_render_target("image", 320, 240)

        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)

        if _Record.value:
            frames = []
            capture_tasks = deque()
            capture_index = 0

        panda_index = model.get_body_index("link0")
        panda = model.get_body(panda_index)
        panda.set_dof_pos(data, init_qpos)

        object_index = model.get_body_index(_Obj.value)
        obj = model.get_body(object_index)

        def set_arm_ctrl(target_qpos):
            start_actuator_index = model.get_actuator_index("actuator1")
            for index, ctrl in enumerate(target_qpos):
                actuator_index = start_actuator_index + index
                actuator = model.get_actuator(actuator_index)
                actuator.set_ctrl(data, ctrl)

        def set_gripper_ctrl(target_gripper):
            actuator_index = model.get_actuator_index("actuator8")
            actuator = model.get_actuator(actuator_index)
            actuator.set_ctrl(data, target_gripper)

        set_arm_ctrl(init_qpos[:7])
        set_gripper_ctrl(init_qpos[7])

        task = "shaking-grasp" if _Shake.value else "slip-grasp"
        step_cnt = 0

        def phys_step():
            nonlocal step_cnt, capture_index
            step_cnt += 1

            if 0 <= step_cnt < 500:
                ctrl_arm = lerp(init_qpos[:7], lift_qpos[:7], step_cnt / 500)
                set_arm_ctrl(ctrl_arm)
            elif 500 <= step_cnt < 1000:
                ctrl_arm = lerp(lift_qpos[:7], grasp_qpos[:7], (step_cnt - 500) / 500)
                set_arm_ctrl(ctrl_arm)
            elif 1000 <= step_cnt < 1500:
                set_gripper_ctrl(lerp(0.04, 0, (step_cnt - 1000) / 500))
            elif 1500 <= step_cnt < 2000:
                ctrl_arm = lerp(grasp_qpos[:7], lift_qpos[:7], (step_cnt - 1500) / 500)
                set_arm_ctrl(ctrl_arm)
            elif 2000 <= step_cnt < 10000 and step_cnt % 2 == 0 and _Shake.value:
                ctrl_arm = lift_qpos[:7] + np.random.normal(0, 0.025, size=7)
                set_arm_ctrl(ctrl_arm)
                obj_pos = obj.get_pose(data)
                if obj_pos[2] < 0.03:
                    print(f"❌ The {task}-{_Obj.value}-test failed.")
                    if _Record.value:
                        import imageio

                        imageio.mimwrite(
                            f"motrix_grasp_{'shake' if _Shake.value else 'slip'}_{_Obj.value}.mp4",
                            frames,
                            fps=30,
                            quality=8,
                        )
                    exit(0)
            elif step_cnt > 10000:
                print(f"✅ The {task}-{_Obj.value}-test passed.")
                if _Record.value:
                    import imageio

                    imageio.mimwrite(
                        f"motrix_grasp_{'shake' if _Shake.value else 'slip'}_{_Obj.value}.mp4",
                        frames,
                        fps=30,
                        quality=8,
                    )
                exit(0)

            # Physics world step
            step(model, data)

        def render_func():
            nonlocal capture_index
            if _Record.value and capture_index < step_cnt * model.options.timestep * 30:
                rcam = render.get_camera(0)
                capture_tasks.append((capture_index, rcam.capture()))
                capture_index += 1

            render.sync(data)
            if _Record.value:
                while len(capture_tasks) > 0:
                    task: CaptureTask
                    idx, task = capture_tasks[0]
                    if task.state != "pending":
                        capture_tasks.popleft()
                        img = task.take_image()
                        # assert img is not None
                        if img is not None and img.pixels.max() > 0:
                            frames.append(img.pixels)
                    else:
                        break

        run.render_loop(model.options.timestep, 60, phys_step, render_func)


if __name__ == "__main__":
    app.run(main)
