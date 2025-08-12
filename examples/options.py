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

from motrixsim import SceneData, SceneModel, load_model, step
from motrixsim.render import RenderApp


def simulate(render: RenderApp, model: SceneModel, data: SceneData):
    time.sleep(0.02)
    # Step the physics world
    step(model, data)
    # Sync render objects from physic world
    render.sync(data)


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/options.xml"
        # Load the scene model
        model = load_model(path)
        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)
        # tag::options_code[]

        # ---------Try to access options----------
        options = model.options
        print(f"model.options: {options}")
        # Get gravity
        gravity = options.gravity  # noqa: F841
        # Get timestep
        timestep = options.timestep  # noqa: F841
        # Get max iterations
        max_iterations = options.max_iterations  # noqa: F841
        # Get solver tolerance
        solver_tolerance = options.solver_tolerance  # noqa: F841
        # Get simulation flags
        disable_gravity = options.disable_gravity  # noqa: F841
        disable_contacts = options.disable_contacts  # noqa: F841
        disable_impedance = options.disable_impedance  # noqa: F841
        # ----------End----------

        # Set gravity
        options.gravity = [0, 0, 9.8]

        for i in range(50):
            simulate(render, model, data)

        # Set gravity
        options.gravity = [0, 0, -9.8]

        for i in range(200):
            simulate(render, model, data)

        # Set simulation flags
        options.disable_contacts = True
        options.disable_impedance = True
        # end::options_code[]
        while True:
            simulate(render, model, data)


if __name__ == "__main__":
    main()
