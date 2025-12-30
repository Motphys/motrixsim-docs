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

import time

import mujoco
import mujoco.viewer
import numpy as np
from absl import app, flags

_Obj = flags.DEFINE_string("object", "cube", "object to grasp, Choices: [cube, ball, bottle]")
_Shake = flags.DEFINE_boolean("shake", True, "whether to shake the arm after grasping, Choices: [True, False]")
_Record = flags.DEFINE_boolean("record", True, "whether to record the simulation, Choices: [True, False]")


def lerp(a, b, t):
    return a + t * (b - a)


def main(argv):
    path = f"examples/assets/franka_emika_panda/scene_pick_{_Obj.value}.xml"

    model = mujoco.MjModel.from_xml_path(path)
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, model.key("home").id)

    if _Record.value:
        frames = []
        renderer = mujoco.Renderer(model)
        renderer.update_scene(data, 0)

    nj = 8
    init_qpos = model.key("home").qpos[:nj].copy()
    grasp_qpos = model.key("grasp").qpos[:nj].copy()
    lift_qpos = model.key("lift").qpos[:nj].copy()

    task = "shaking-grasp" if _Shake.value else "slip-grasp"
    with mujoco.viewer.launch_passive(model, data) as viewer:
        step_cnt = 0
        while viewer.is_running():
            step_cnt += 1
            step_start = time.time()

            if 0 <= step_cnt < 500:
                ctrl_arm = lerp(init_qpos[:7], lift_qpos[:7], step_cnt / 500)
                data.ctrl[:7] = ctrl_arm
            elif 500 <= step_cnt < 1000:
                ctrl_arm = lerp(lift_qpos[:7], grasp_qpos[:7], (step_cnt - 500) / 500)
                data.ctrl[:7] = ctrl_arm
            elif 1000 <= step_cnt < 1500:
                data.ctrl[7] = lerp(0.04, 0, (step_cnt - 1000) / 500)
            elif 1500 <= step_cnt < 2000:
                ctrl_arm = lerp(grasp_qpos[:7], lift_qpos[:7], (step_cnt - 1500) / 500)
                data.ctrl[:7] = ctrl_arm
            elif 2000 <= step_cnt < 10000:
                if _Shake.value and step_cnt % 2 == 0:
                    ctrl_arm = lift_qpos[:7] + np.random.normal(0, 0.025, size=7)
                    data.ctrl[:7] = ctrl_arm
                obj_pos = data.xpos[model.body(_Obj.value).id]
                if obj_pos[2] < 0.04:
                    print(f"❌ The {task}-{_Obj.value} failed.")
                    break
            elif step_cnt > 10000:
                print(f"✅ The {task}-{_Obj.value} passed.")
                break

            # mj_step can be replaced with code that also evaluates
            # a policy and applies a control signal before stepping the physics.
            mujoco.mj_step(model, data)

            # Pick up changes to the physics state, apply perturbations, update options from GUI.
            viewer.sync()

            # Rudimentary time keeping, will drift relative to wall clock.
            time_until_next_step = model.opt.timestep - (time.time() - step_start)
            if time_until_next_step > 0:
                time.sleep(time_until_next_step)

            if _Record.value and len(frames) < data.time * 30:
                renderer.update_scene(data, 0)
                frames.append(renderer.render().copy())

    if _Record.value:
        import imageio

        imageio.mimwrite(
            f"mujoco_grasp_{'shake' if _Shake.value else 'slip'}_{_Obj.value}_noslip_iterations=1.mp4",
            frames,
            fps=30,
            quality=8,
        )


if __name__ == "__main__":
    app.run(main)
