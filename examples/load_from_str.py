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

from motrixsim import SceneData, load_mjcf_str, step
from motrixsim.render import RenderApp

# tag::model_load_from_string[]
mjcf = """<mujoco>
    <option timestep="0.001"/>
    <worldbody>
        <light name="light" pos="0 0 3"/>
        <geom name="floor" size="0 0 0.05" type="plane"/>
        <body pos="0 0 0.1">
            <freejoint/>
            <geom type="sphere" size=".1" />
        </body>
        <body pos="0.01 0 0.3">
            <freejoint/>
            <geom type="sphere" size=".1" />
        </body>
    </worldbody>
</mujoco>"""


def main():
    # Create render window for visualization
    render = RenderApp()
    # Load the scene model
    model = load_mjcf_str(mjcf)
    # end::model_load_from_string[]
    # Create the render instance of the model
    render.launch(model)
    # Create the physics data of the model
    data = SceneData(model)

    while True:
        # Control the step interval to prevent too fast simulation
        time.sleep(0.001)
        # Step the physics world
        step(model, data)
        render.sync(data)


if __name__ == "__main__":
    main()
