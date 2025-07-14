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
    # tag::create_data[]
    # The scene description file
    path = "examples/assets/model.xml"
    # Load the scene model
    model = load_model(path)
    # Create the render instance of the model
    # Try to create 3 model data
    repeat = 3
    render_offset_1 = [0, 0, 0]
    render_offset_2 = [0, 1, 0]
    render_offset_3 = [0, -1, 0]
    render.launch(model, repeat, [render_offset_1, render_offset_2, render_offset_3])
    # Create the physics data of the model
    data_1 = SceneData(model)
    data_2 = SceneData(model)
    data_3 = SceneData(model)
    # end::create_data[]

    # In this case, model has two joints : slide and ball.
    # The num_dof_vel of ball joint is 3. and the num_dof_pos is 4.
    # The num_dof_vel of slide join is 1, and the num_dof_pos is 1.
    # Thus the num_dof_vel of the model is "3 + 1 = 4", and the num_dof_pos is "4 + 1 = 5".
    num_dof_vel = model.num_dof_vel
    num_dof_pos = model.num_dof_pos
    print(f"num_dof_vel is : {num_dof_vel}, num_dof_pos is : {num_dof_pos}")

    # Body
    base_body = model.get_body(model.get_body_index("base"))
    print(f"base body pose is : {base_body.get_pose(data_1)}")

    # Disable gravity in the model
    model.options.disable_gravity = True

    # Set actuator control
    ctrl_value = 1.0
    slide_actuator = model.get_actuator("actuator_slider")
    slide_actuator.set_ctrl(data_1, ctrl_value)
    slide_actuator.set_ctrl(data_2, ctrl_value * 0.5)
    slide_actuator.set_ctrl(data_3, ctrl_value * -0.8)

    # Get slide joint dof vel by data
    slide_joint_index = model.get_joint_index("slider")
    slide_joint_dof_vel_addr = model.joint_dof_vel_indices[slide_joint_index]
    slide_joint_dof_vel = data_1.dof_vel[slide_joint_dof_vel_addr]

    # Wait for creating render world
    start = time.time()

    while True:
        # Control the step interval to prevent too fast simulation
        time.sleep(0.02)
        current_time = time.time()
        if current_time - start > 3.0:
            ctrl_value *= -1
            slide_actuator.set_ctrl(data_1, ctrl_value)
            slide_actuator.set_ctrl(data_2, ctrl_value * 0.5)
            slide_actuator.set_ctrl(data_3, ctrl_value * -0.8)
            start = current_time

        # Physics world step
        step(model, data_1)
        step(model, data_2)
        step(model, data_3)

        link_pose = model.get_link_poses(data_1)
        print(f"link_pose : {link_pose}")

        slide_joint_dof_vel = data_1.dof_vel[slide_joint_dof_vel_addr]
        print(f"slide_joint_dof_vel : {slide_joint_dof_vel}")

        # Sync render objects from physic world
        render.sync([data_1, data_2, data_3])


if __name__ == "__main__":
    main()
