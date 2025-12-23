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

from motrixsim import SceneData, load_model, run, step
from motrixsim.render import RenderApp


def lerp(a, b, t):
    return a + t * (b - a)


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/stanford_tidybot/scene.xml"
        # Load the scene model
        model = load_model(path)
        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)

        # Get actuator to control robot action
        joint_x = model.get_actuator("joint_x")
        joint_y = model.get_actuator("joint_y")
        joint_2 = model.get_actuator("joint_2")
        joint_4 = model.get_actuator("joint_4")
        fingers_actuator = model.get_actuator("fingers_actuator")
        joint_7 = model.get_actuator("joint_7")
        move_x = 0.5
        move_y = -0.3
        move_2 = 1.5
        move_4 = 1.5
        move_7 = 1.0
        fingers = 255
        start = time.time()
        action_index = 0

        def phys_step():
            nonlocal start, action_index
            diff = time.time() - start
            # Action by sequence
            if diff < 1:
                if action_index == 0:
                    lerp_value = lerp(0, move_x, diff)
                    joint_x.set_ctrl(data, lerp_value)
                elif action_index == 1:
                    lerp_value = lerp(0, move_y, diff)
                    joint_y.set_ctrl(data, lerp_value)
                elif action_index == 2:
                    lerp_value = lerp(0, move_2, diff)
                    joint_2.set_ctrl(data, lerp_value)
                elif action_index == 3:
                    lerp_value = lerp(0, move_4, diff)
                    joint_4.set_ctrl(data, lerp_value)
                elif action_index == 4:
                    lerp_value = lerp(move_y, 0.03, diff)
                    joint_y.set_ctrl(data, lerp_value)
                elif action_index == 5:
                    lerp_value = lerp(0, fingers, diff)
                    fingers_actuator.set_ctrl(data, lerp_value)
                elif action_index == 6:
                    lerp_value = lerp(move_2, 0, diff)
                    joint_2.set_ctrl(data, lerp_value)
                elif action_index == 7:
                    lerp_value = lerp(0.03, 1.0, diff)
                    joint_y.set_ctrl(data, lerp_value)
                elif action_index == 8:
                    lerp_value = lerp(0, move_7, diff)
                    joint_7.set_ctrl(data, lerp_value)
                elif action_index == 9:
                    lerp_value = lerp(fingers, 0, diff)
                    fingers_actuator.set_ctrl(data, lerp_value)
                elif action_index == 10:
                    lerp_value = lerp(move_4, 0, diff)
                    joint_4.set_ctrl(data, lerp_value)
            else:
                start = time.time()
                action_index += 1

            # Physics world step
            step(model, data)

        run.render_loop(model.options.timestep, 60, phys_step, lambda: render.sync(data))


if __name__ == "__main__":
    main()
