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

from motrixsim import SceneData, load_model, step
from motrixsim.render import RenderApp


def lerp(a, b, t):
    return a + t * (b - a)


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def main():
    # Create render window for visualization
    render = RenderApp()
    # The scene description file
    path = "examples/assets/stanford_tidybot_adhesion/scene.xml"
    # Load the scene model
    model = load_model(path)
    # Create the render instance of the model
    render.launch(model)
    # Create the physics data of the model
    data = SceneData(model)

    # Get actuator to control robot action
    joint_x = model.get_actuator("joint_x")
    joint_y = model.get_actuator("joint_y")
    joint_th = model.get_actuator("joint_th")
    joint_2 = model.get_actuator("joint_2")
    joint_4 = model.get_actuator("joint_4")
    joint_6 = model.get_actuator("joint_6")
    adhere = model.get_actuator("adhere")
    start = time.time()
    action_index = 0
    action_time = 2

    while True:
        # Control the step interval to prevent too fast simulation
        time.sleep(0.002)

        diff = time.time() - start

        # Action by sequence
        if diff < action_time:
            r = diff / action_time
            if action_index == 0:
                lerp_value = lerp(0, -1.6, r)
                joint_th.set_ctrl(data, lerp_value)
                lerp_value = lerp(0, -1.18, r)
                joint_2.set_ctrl(data, lerp_value)
                lerp_value = lerp(0, -1.54, r)
                joint_4.set_ctrl(data, lerp_value)
                lerp_value = lerp(0, -0.357, r)
                joint_6.set_ctrl(data, lerp_value)
            elif action_index == 1:
                action_time = 0.2
            elif action_index == 2:
                action_time = 1
                adhere.set_ctrl(data, 50)
                lerp_value = lerp(-1.1, -0.5, r)
                joint_2.set_ctrl(data, lerp_value)
                lerp_value = lerp(-1.5, -1.37, r)
                joint_4.set_ctrl(data, lerp_value)
                lerp_value = lerp(-0.35, -1.2, r)
                joint_6.set_ctrl(data, lerp_value)
            elif action_index == 3:
                action_time = 3
                lerp_value = lerp(0, 1, r)
                joint_x.set_ctrl(data, lerp_value)
                lerp_value = lerp(0, 0.36, r)
                joint_y.set_ctrl(data, lerp_value)
            elif action_index == 4:
                adhere.set_ctrl(data, 0)
        else:
            start = time.time()
            action_index += 1

        # Physics world step
        step(model, data)
        # Sync render objects from physic world
        render.sync(data)


if __name__ == "__main__":
    main()
