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


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def main():
    # Create render window for visualization
    render = RenderApp()
    # The scene description file
    path = "examples/assets/keyboard_car.xml"
    # Load the scene model
    model = load_model(path)
    # Create the render instance of the model
    render.launch(model)
    # Create the physics data of the model
    data = SceneData(model)
    # Get actuator for car controlling
    forward = model.get_actuator("forward")
    turn = model.get_actuator("turn")
    forward_value = 0.0
    turn_value = 0.0
    print("==========================")
    print("Press 'W' to move forward, 'S' to move backward, 'A' to turn left, 'D' to turn right.")

    while True:
        forward.set_ctrl(data, forward_value)
        turn.set_ctrl(data, turn_value)
        # Control the step interval to prevent too fast simulation
        time.sleep(0.002)
        # Step the physics world
        step(model, data)
        # Sync render objects from physic world
        render.sync(data)
        input = render.input
        # Read keyboard from render app
        forward_value = 0.0
        turn_value = 0.0
        if input.is_key_pressed("a"):
            turn_value = 1
        if input.is_key_pressed("d"):
            turn_value = -1
        if input.is_key_pressed("s"):
            forward_value = -1
        if input.is_key_pressed("w"):
            forward_value = 1


if __name__ == "__main__":
    main()
