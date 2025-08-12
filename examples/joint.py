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

# tag::init[]
import time

import numpy as np

from motrixsim import SceneData, load_model, step
from motrixsim.render import RenderApp

# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view


def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/joint.xml"
        # Load the scene model
        model = load_model(path)

        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)
        # end::init[]

        # tag::access_all[]
        # ----------Try to access joint data----------
        # How many joints in the model?
        num_joints = model.num_joints
        # Get the all joints in the model
        joints = model.joints
        # The name list of joints in the model
        joint_names = model.joint_names
        print(f"num_joints :{num_joints}, joint_names : {joint_names}, joints : {joints}")
        # end::access_all[]

        # tag::joint_index[]
        # Try to visit "joint_A"
        joint_A_index = model.get_joint_index("joint_A")
        joint_A = model.get_joint(joint_A_index)
        assert joint_A is not None, "Expect joint_A in the model"
        print(f"joint_addr is {joint_A_index}, joint_A is : {joint_A}, name is : {joint_A.name}")
        # end::joint_index[]

        # The num_dof_vel of joint_A
        joint_A_num_dof_vel = joint_A.num_dof_vel
        # The num_dof_pos of joint_A
        joint_A_num_dof_pos = joint_A.num_dof_pos
        # For a hinge joint, the DOFs for position and velocity are both 1.
        print(f"joint_A_num_dof_vel is : {joint_A_num_dof_vel}, joint_A_num_dof_pos is : {joint_A_num_dof_pos}")

        # The same data of joint_B
        joint_B_index = model.get_joint_index("joint_B")
        joint_B = model.get_joint(joint_B_index)
        assert joint_B is not None, "Expect joint_B in the model"
        joint_B_num_dof_vel = joint_B.num_dof_vel  # Since joint_B is ball joint ,the num_dof_vel is 3
        joint_B_num_dof_pos = joint_B.num_dof_pos  # Since joint_B is ball joint ,the num_dof_pos is 4
        print(f"joint_B_num_dof_vel is : {joint_B_num_dof_vel}, joint_B_num_dof_pos is : {joint_B_num_dof_pos}")

        # We can use model to get num_dof_pos/num_dof_vel of all the joints directly
        vel_num = model.joint_dof_vel_nums
        pos_num = model.joint_dof_pos_nums
        print(f"vel_num is : {vel_num}, pos_num is : {pos_num}")

        # tag::joint_dof_pos_vel[]
        # Indicate the first pos data index of each joint in SceneData.dof_pos
        pos_indices = model.joint_dof_pos_indices
        # Indicate the first vel data index of each joint in SceneData.dof_vel
        vel_indices = model.joint_dof_vel_indices

        # The pos of joint_A (hinge joint ,num_dof_pos is 1, num_dof_vel is 1)
        joint_A_pos_0 = data.dof_pos[pos_indices[joint_A_index]]
        joint_A_vel_0 = data.dof_vel[vel_indices[joint_A_index]]
        print(f"joint_A_pos_0 is :{joint_A_pos_0}, joint_A_vel_0 is : {joint_A_vel_0} ")
        # end::joint_dof_pos_vel[]

        print("--------------------")
        # The pos of joint_B (ball joint, num_dof_pos is 4, num_dof_vel is 3)
        joint_B_pos = data.dof_pos[pos_indices[joint_B_index] : pos_indices[joint_B_index] + joint_B_num_dof_pos]
        print(f"joint_B_pos is :{joint_B_pos}")
        print("--------------------")

        joint_B_vel = data.dof_vel[vel_indices[joint_B_index] : vel_indices[joint_B_index] + joint_B_num_dof_vel]
        print(f"joint_B_vel = :{joint_B_vel}")

        # tag::joint_limits[]
        joint_limits = model.joint_limits
        assert joint_limits.shape == (2, num_joints), (
            f"joint_limits shape is {joint_limits.shape}, but should be (2, {num_joints})"
        )
        # Limits of joint_A
        limits = joint_limits[:, joint_A_index]
        print(f"limit of joint_A in radian, min: {limits[0]}, max: {limits[1]}")

        # Limits of joint_B
        limits = joint_limits[:, joint_B_index]
        print(f"limit of joint_B is radian, min: {limits[0]}, max: {limits[1]}")
        # end::joint_limits[]
        # -----------End----------

        # tag::set_pos_vel[]
        print("-------Set vel and get-------")
        # Try to set vel directly
        joint_A.set_dof_vel(data, np.array([0.1]))
        # Use joint dof_vel_index to get dof_vel
        dof_vel_index = joint_A.dof_pos_index
        dof_vel = data.dof_vel[dof_vel_index]
        print(f"dof_vel of joint_A is : {dof_vel}")
        # Or use get_dof_vel() directly. It's the same with dof_pos
        dof_vel = joint_A.get_dof_vel(data)
        print(f"dof_vel of joint_A is : {dof_vel}")
        print("-----------------------------")
        # Set positions
        # joint_A, num_dof_pos is 1
        joint_A.set_dof_pos(data, [0.1])
        # joint_B, num_dof_pos is 4
        joint_B.set_dof_pos(data, [0.0, 0.0, 0.0, 1.0])
        # end::set_pos_vel[]

        start = time.time()
        forward_vel = 1.0
        backward_vel = -1.0
        flip = False
        print_count = 0
        set_vel = False

        while True:
            # Control the step interval to prevent too fast simulation
            time.sleep(0.02)
            # Physics world step
            step(model, data)

            if time.time() - start > 2.0:
                vel = forward_vel if flip else backward_vel
                # joint_A, num_dof_vel is 1
                joint_A_vel = [vel]
                # joint_B, num_dof_vel is 3
                joint_B_vel = [0, -vel * 2.5, 0]
                joint_A.set_dof_vel(data, joint_A_vel)
                joint_B.set_dof_vel(data, joint_B_vel)

                start = time.time()
                flip = not flip
                set_vel = True

            if set_vel and print_count < 25:
                joint_A_pos = joint_A.get_dof_pos(data)
                joint_A_vel = joint_A.get_dof_vel(data)
                print(f"joint_A_pos : {joint_A_pos}, joint_A_vel : {joint_A_vel}")
                print("-----------")
                joint_B_pos = joint_B.get_dof_pos(data)
                joint_B_vel = joint_B.get_dof_vel(data)
                print(f"joint_B_pos : {joint_B_pos}, joint_B_vel : {joint_B_vel}")
                print("-----------")
                print_count += 1

            # Sync render objects from physic world
            render.sync(data)


if __name__ == "__main__":
    main()
