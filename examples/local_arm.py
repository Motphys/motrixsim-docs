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
        path = "examples/assets/local_arm.xml"
        # Load the scene model
        model = load_model(path)
        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)

        # Get actuator to control robot action
        rotate = model.get_actuator("rotate")
        up_down = model.get_actuator("up_down")
        fingers_actuator = model.get_actuator("fingers_actuator")
        move_rotate = -1.0
        move_up_down = 0.2
        move_fingers_actuator = 10
        fingers_actuator.set_ctrl(data, -10)

        start = time.time()
        action_index = 0

        def control_and_step():
            nonlocal start, action_index

            diff = time.time() - start

            # Action by sequence
            if diff < 1:
                if action_index == 0:
                    lerp_value = lerp(0, move_up_down, diff)
                    up_down.set_ctrl(data, lerp_value)
                elif action_index == 1:
                    lerp_value = lerp(0, move_rotate, diff)
                    rotate.set_ctrl(data, lerp_value)
                elif action_index == 2:
                    lerp_value = lerp(move_up_down, -0.02, diff)
                    up_down.set_ctrl(data, lerp_value)
                elif action_index == 3:
                    lerp_value = lerp(0, move_fingers_actuator, diff)
                    fingers_actuator.set_ctrl(data, lerp_value)
                elif action_index == 4:
                    lerp_value = lerp(0, move_up_down, diff)
                    up_down.set_ctrl(data, lerp_value)
                elif action_index == 5:
                    lerp_value = lerp(move_rotate, -move_rotate, diff)
                    rotate.set_ctrl(data, lerp_value)
                elif action_index == 6:
                    lerp_value = lerp(move_fingers_actuator, -move_fingers_actuator, diff)
                    fingers_actuator.set_ctrl(data, lerp_value)
            else:
                start = time.time()
                action_index += 1

            # Physics world step
            step(model, data)

        run.render_loop(model.options.timestep, 60, control_and_step, lambda: render.sync(data))


if __name__ == "__main__":
    main()
