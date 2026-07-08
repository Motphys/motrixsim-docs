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

"""
MuJoCo interactive grasp shake test.

Usage:
    python -m examples.bench.grasp.shake_test_mj --object=cube
    python -m examples.bench.grasp.shake_test_mj --object=cube --noshake --record
"""

import time

import mujoco
import mujoco.viewer
from absl import app, flags
from common import (
    DEFAULT_HOLD_DURATION,
    DROP_Z_THRESHOLD,
    SETTLING_END_TIME,
    SETTLING_START_TIME,
    compute_ctrl_for_time,
)

_Obj = flags.DEFINE_string("object", "cube", "Object to grasp. Choices: [cube, ball, bottle]")
_Shake = flags.DEFINE_boolean("shake", True, "Whether to shake the arm after grasping")
_Record = flags.DEFINE_boolean("record", False, "Whether to record the simulation as video")
_HoldDuration = flags.DEFINE_float("hold_duration", DEFAULT_HOLD_DURATION, "Hold phase duration in seconds")


def main(argv):
    path = f"examples/assets/franka_emika_panda/scene_pick_{_Obj.value}.xml"
    model = mujoco.MjModel.from_xml_path(path)
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, model.key("home").id)

    dt = model.opt.timestep
    init_qpos = model.key("home").qpos[:8].copy()

    act_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, f"actuator{i}") for i in range(1, 9)]
    obj_body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "obj")

    def set_arm_ctrl(target_qpos):
        for i, val in enumerate(target_qpos):
            data.ctrl[act_ids[i]] = val

    def set_gripper_ctrl(val):
        data.ctrl[act_ids[7]] = val

    set_arm_ctrl(init_qpos[:7])
    set_gripper_ctrl(init_qpos[7])
    mujoco.mj_forward(model, data)

    record = _Record.value
    if record:
        frames = []
        renderer = mujoco.Renderer(model)
        renderer.update_scene(data, 0)

    task_name = "shaking-grasp" if _Shake.value else "slip-grasp"
    total_duration = SETTLING_END_TIME + _HoldDuration.value

    with mujoco.viewer.launch_passive(model, data) as viewer:
        step_cnt = 0
        while viewer.is_running():
            step_cnt += 1
            step_start = time.time()
            sim_time = step_cnt * dt

            arm, gripper = compute_ctrl_for_time(sim_time, _Shake.value, shake_step=step_cnt)
            if arm is not None:
                set_arm_ctrl(arm)
            if gripper is not None:
                set_gripper_ctrl(gripper)

            if sim_time >= SETTLING_START_TIME and _Shake.value:
                if data.xpos[obj_body_id][2] < DROP_Z_THRESHOLD:
                    print(f"The {task_name}-{_Obj.value} failed.")
                    break

            mujoco.mj_step(model, data)
            viewer.sync()

            time_until_next = dt - (time.time() - step_start)
            if time_until_next > 0:
                time.sleep(time_until_next)

            if record and len(frames) < data.time * 30:
                renderer.update_scene(data, 0)
                frames.append(renderer.render().copy())

            if sim_time >= total_duration:
                print(f"The {task_name}-{_Obj.value} passed.")
                break

        else:
            print(f"The {task_name}-{_Obj.value} passed.")

    if record:
        import imageio

        imageio.mimwrite(
            f"mujoco_grasp_{_Obj.value}.mp4",
            frames,
            fps=30,
            quality=8,
        )


if __name__ == "__main__":
    app.run(main)
