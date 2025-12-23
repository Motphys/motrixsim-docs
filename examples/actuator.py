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

# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view


def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/actuator.xml"
        # Load the scene model
        model = load_model(path)
        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)

        # ----------Try to access actuators----------
        # How many actuators are in the model?
        num_actuators = model.num_actuators
        print(f"num_actuators is : {num_actuators}")
        # The name list of actuators
        actuator_names = model.actuator_names
        print(f"actuator_names is : {actuator_names}")
        # The control range of actuators
        actuator_ctrl_limits = model.actuator_ctrl_limits
        print(f"actuator_ctrl_limits is : {actuator_ctrl_limits}")

        # Get actuator_A index in model
        actuator_A_index = model.get_actuator_index("actuator_A")
        # Get actuator_A by the way with index
        actuator_A = model.get_actuator(actuator_A_index)
        print(f"actuator_A by index name is : {actuator_A.name}")
        # Get actuator_A by the way with name
        actuator_A = model.get_actuator("actuator_A")
        # Get other actuators
        actuator_B = model.get_actuator("actuator_B")
        actuator_C = model.get_actuator("actuator_C")

        # Look at the actuators' index
        print(
            f"actuator_A index is :{actuator_A.index}, actuator_B index is :{actuator_B.index}, "
            f"actuator_C index is : {actuator_C.index}"
        )

        # Look at the actuators' control range
        actuator_A_ctrl_range = actuator_A.ctrl_range
        actuator_B_ctrl_range = actuator_B.ctrl_range
        actuator_C_ctrl_range = actuator_C.ctrl_range
        print(f"actuator_A_ctrl_range is : {actuator_A_ctrl_range}")
        print(f"actuator_B_ctrl_range is : {actuator_B_ctrl_range}")
        print(f"actuator_C_ctrl_range is : {actuator_C_ctrl_range}")

        start = time.time()
        flip = False
        print_count = 0

        def control_and_step():
            nonlocal start, flip, print_count

            if time.time() - start > 1.5:
                actuator_A.set_ctrl(data, 1.0 if flip else -1.0)
                actuator_C.set_ctrl(data, 0.5 if flip else -0.5)
                flip = not flip
                start = time.time()

            if print_count < 200:
                ctrls = model.get_actuator_ctrls(data)
                print(f"actuator_ctrls is :{ctrls}")
                print_count += 1

            # Physics world step
            step(model, data)

        run.render_loop(model.options.timestep, 60, control_and_step, lambda: render.sync(data))


if __name__ == "__main__":
    main()
