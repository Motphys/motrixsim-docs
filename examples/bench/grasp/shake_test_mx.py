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

"""
MotrixSim interactive grasp shake test.

Usage:
    uv run python -m examples.bench.grasp.shake_test_mx --object=cube
    uv run python -m examples.bench.grasp.shake_test_mx --object=cube --noshake --record
"""

from collections import deque

from absl import app, flags
from common import (
    DEFAULT_HOLD_DURATION,
    DROP_Z_THRESHOLD,
    INIT_QPOS,
    SETTLING_END_TIME,
    SETTLING_START_TIME,
    compute_ctrl_for_time,
)

from motrixsim import SceneData, load_model, run, step
from motrixsim.render import CaptureTask, RenderApp

_Obj = flags.DEFINE_string("object", "cube", "Object to grasp. Choices: [cube, ball, bottle]")
_Shake = flags.DEFINE_boolean("shake", True, "Whether to shake the arm after grasping")
_Record = flags.DEFINE_boolean("record", False, "Whether to record the simulation as video")
_HoldDuration = flags.DEFINE_float("hold_duration", DEFAULT_HOLD_DURATION, "Hold phase duration in seconds")


def main(argv):
    path = f"examples/assets/franka_emika_panda/scene_pick_{_Obj.value}.xml"
    model = load_model(path)
    data = SceneData(model)
    dt = model.options.timestep

    panda = model.get_body(model.get_body_index("link0"))
    panda.set_dof_pos(data, INIT_QPOS)
    obj = model.get_body("obj")

    def set_arm_ctrl(target_qpos):
        start = model.get_actuator_index("actuator1")
        for i, val in enumerate(target_qpos):
            model.get_actuator(start + i).set_ctrl(data, val)

    def set_gripper_ctrl(val):
        model.get_actuator(model.get_actuator_index("actuator8")).set_ctrl(data, val)

    set_arm_ctrl(INIT_QPOS[:7])
    set_gripper_ctrl(INIT_QPOS[7])

    record = _Record.value
    if record:
        frames = []
        capture_tasks = deque()
        capture_index = 0

    task_name = "shaking-grasp" if _Shake.value else "slip-grasp"
    step_cnt = 0
    total_duration = SETTLING_END_TIME + _HoldDuration.value

    with RenderApp() as render:
        render.opt.set_left_panel_vis(True)
        model.cameras[0].set_render_target("image", 320, 240)
        render.launch(model)

        def phys_step():
            nonlocal step_cnt, capture_index
            step_cnt += 1
            sim_time = step_cnt * dt

            arm, gripper = compute_ctrl_for_time(sim_time, _Shake.value, shake_step=step_cnt)
            if arm is not None:
                set_arm_ctrl(arm)
            if gripper is not None:
                set_gripper_ctrl(gripper)

            if sim_time >= SETTLING_START_TIME and _Shake.value:
                if obj.get_pose(data)[2] < DROP_Z_THRESHOLD:
                    print(f"The {task_name}-{_Obj.value}-test failed.")
                    if record:
                        _save_video(frames)
                    exit(0)
            if sim_time >= total_duration:
                print(f"The {task_name}-{_Obj.value}-test passed.")
                if record:
                    _save_video(frames)
                exit(0)

            step(model, data)

        def render_func():
            nonlocal capture_index

            if record and capture_index < step_cnt * dt * 30:
                rcam = render.get_camera(0)
                capture_tasks.append((capture_index, rcam.capture()))
                capture_index += 1

            render.sync(data)

            if record:
                while len(capture_tasks) > 0:
                    task: CaptureTask
                    idx, task = capture_tasks[0]
                    if task.state != "pending":
                        capture_tasks.popleft()
                        img = task.take_image()
                        if img is not None and img.pixels.max() > 0:
                            frames.append(img.pixels)
                    else:
                        break

        run.render_loop(dt, 60, phys_step, render_func)


def _save_video(frames):
    import imageio

    imageio.mimwrite(
        f"motrix_grasp_{_Obj.value}.mp4",
        frames,
        fps=30,
        quality=8,
    )


if __name__ == "__main__":
    app.run(main)
