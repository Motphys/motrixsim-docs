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
    # tag::num_bodies
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/body.xml"
        # Load the scene model
        model = load_model(path)
        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)
        # How many bodies in the model?
        num_bodies = model.num_bodies
        # we have 3 bodies in the model
        assert num_bodies == 3, f"Expect 3 bodies, but got {num_bodies}"

        # end::num_bodies

        # The all bodies's name
        body_names = model.body_names
        print(f"body_names : {body_names}")

        # The body list in model
        bodies = model.bodies
        # Iter bodies by list
        for body in bodies:
            print(f"each body name : {body.name}")

        # Iter bodies by index
        for i in range(num_bodies):
            body = model.get_body(i)
            print(f"addr : {i},  body name : {body.name}")

        # tag::articulated_body
        capsule = model.get_body("capsule")
        assert capsule is not None, "Expect capsule to be a body in model"
        assert capsule.num_links == 2, "Expect capsule to have two links"
        assert capsule.num_joints == 2, "Expect capsule to have two joints"
        # end::articulated_body

        # ----------Try to access some body----------
        # cube is free move, try to control it
        cube = model.get_body("free_cube")

        assert cube is not None, "Expect cube to be a body in model"
        assert cube.num_links == 1, "Expect cube to have one link"
        assert cube.num_joints == 0, "Single body should have no joint"

        # tag::floatingbase
        # we can get floatingbase if the body is free move
        cube_fb = cube.floatingbase
        assert cube_fb is not None, "Expect cube to be a floating base body"
        # end::floatingbase

        # Indicate the first pos data index in SceneData.dof_pos
        dof_pos_start = cube_fb.dof_pos_start
        dof_pos_indices = cube_fb.dof_pos_indices  # for free joint, length is 7, position + rotation
        print(f"dof_pos_start : {dof_pos_start},  dof_pos_indices : {dof_pos_indices}")

        # Get capsule position from data
        pos = data.dof_pos[dof_pos_indices]

        print("position is : ", pos[:3])
        print("rotation is : ", pos[3:])

        # Indicate the first vel data index in SceneData.dof_vel
        dof_vel_start = cube_fb.dof_vel_start
        dof_vel_indices = cube_fb.dof_vel_indices  # for free joint, lenth is 6
        print(f"dof_vel_start : {dof_vel_start},  dof_vel_indices : {dof_vel_indices}")

        # Get capsule velocity from data
        vel = data.dof_vel[dof_vel_indices]

        print("position velocity is : ", vel[:3])
        print("rotation velocity is : ", vel[3:])

        # tag::access_body[]
        # Get position from body directly
        dof_pos = cube_fb.get_dof_pos(data)
        # Get velocity from body directly
        dof_vel = cube_fb.get_dof_vel(data)
        # Get position and rotation directly
        # Note: This data will be delayed by one frame
        pose = cube.get_pose(data)

        print(f"dof_pos is : {dof_pos}")
        print(f"dof_vel is : {dof_vel}")
        print(f"pose is {pose}")
        # end::access_body[]
        # ----------End----------

        set_pos = False
        start = time.time()
        print_count = 0

        while True:
            # Control the step interval to prevent too fast simulation
            time.sleep(0.02)

            if not set_pos and time.time() - start > 3:
                # Set the position and rotation of the capsule body
                cube_fb.set_translation(data, np.array([0.0, 0.0, 3.0]))
                cube_fb.set_rotation(data, np.array([0.259, 0.0, 0.0, 0.966]))
                set_pos = True

            if set_pos and print_count < 100:
                dof_pos = cube_fb.get_dof_pos(data)
                pose = cube.get_pose(data)
                print(f"dof_pos is : {dof_pos}")
                print(f"pose is {pose}")
                print(f"----------{print_count}----------")
                print_count += 1

            # Physics world step
            step(model, data)
            # Sync render objects from physic world
            render.sync(data)


if __name__ == "__main__":
    main()
