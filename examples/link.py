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

import numpy as np

from motrixsim import SceneData, load_model, step
from motrixsim.render import RenderApp


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def main():
    # Create render window for visualization
    render = RenderApp()
    # The scene description file
    path = "examples/assets/link.xml"
    # Load the scene model
    model = load_model(path)
    # Create the render instance of the model
    render.launch(model)
    # Create the physics data of the model
    data = SceneData(model)

    # How many links are in the model?
    num_links = model.num_links
    # The link list
    links = model.links
    # The link name list
    link_names = model.link_names
    print(f"num_links : {num_links}, links : {links}, link_names : {link_names}")
    # Get all the links' pose
    link_pose = model.get_link_poses(data)
    print(f"link_pose : {link_pose}")

    # Get the link
    base_link_index = model.get_link_index("base")
    # base_link = model.get_link(base_link_index)
    # Or get the link by name
    arm_A_link = model.get_link("arm_A")
    print(f"base_link_index is: {base_link_index}")

    # Get some link data
    arm_A_link_name = arm_A_link.name
    arm_A_link_pose = arm_A_link.get_pose(data)
    arm_A_link_linear_vel = arm_A_link.get_linear_velocity(data)
    arm_A_link_angular_vel = arm_A_link.get_angular_velocity(data)
    print(f"arm_A_link_name: {arm_A_link_name}, arm_A_link_pose : {arm_A_link_pose}")
    print(f"arm_A_link_linear_vel: {arm_A_link_linear_vel}, arm_A_link_angular_vel : {arm_A_link_angular_vel}")

    arm_B_index = model.get_link_index("arm_B")
    arm_B_link = model.get_link(arm_B_index)

    # Set joint vel
    # The directions of the velocity are opposite, so the final angular velocity of link "arm_B" is -0.5
    joint_A = model.get_joint("joint_A")
    joint_A.set_dof_vel(data, np.array([3.0]))
    joint_B = model.get_joint("joint_B")
    joint_B.set_dof_vel(data, np.array([-3.5]))

    print_count = 0

    while True:
        # Control the step interval to prevent too fast simulation
        time.sleep(0.02)
        # Physics world step
        step(model, data)
        # Sync render objects from physic world
        render.sync(data)

        if print_count < 100:
            arm_A_link_pose = arm_A_link.get_pose(data)
            arm_A_link_angular_vel = arm_A_link.get_angular_velocity(data)
            print(f" arm_A_link_pose : {arm_A_link_pose}, arm_A_link_angular_vel : {arm_A_link_angular_vel}")

            arm_B_link_pose = arm_B_link.get_pose(data)
            arm_B_link_angular_vel = arm_B_link.get_angular_velocity(data)
            print(f" arm_B_link_pose : {arm_B_link_pose}, arm_B_link_angular_vel : {arm_B_link_angular_vel}")

            print_count += 1


if __name__ == "__main__":
    main()
