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

from motrixsim import SceneData, load_model, run, step
from motrixsim.render import RenderApp


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/geom.xml"
        # Load the scene model
        model = load_model(path)
        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)

        # How many geoms are in the model?
        num_geoms = model.num_geoms
        # The geom list
        geoms = model.geoms
        # The geom name list
        geom_names = model.geom_names
        print(f"num_geoms : {num_geoms}, geoms : {geoms}, geoms_names : {geom_names}")

        # Get the geom index
        cube_A_index = model.get_geom_index("cube_A")
        print(f"cube_A_index is: {cube_A_index}")

        # get the geom by name
        cube_A = model.get_geom("cube_A")

        # Get some geom data
        cube_A_name = cube_A.name
        cube_A_pose = cube_A.get_pose(data)
        cube_A_linear_vel = cube_A.get_linear_velocity(data)
        cube_A_angular_vel = cube_A.get_angular_velocity(data)
        print(f"cube_A_name: {cube_A_name}, cube_A_pose : {cube_A_pose}")
        print(f"cube_A_linear_vel: {cube_A_linear_vel}, cube_A_angular_vel : {cube_A_angular_vel}")

        run.render_loop(model.options.timestep, 60, lambda: step(model, data), lambda: render.sync(data))


if __name__ == "__main__":
    main()
