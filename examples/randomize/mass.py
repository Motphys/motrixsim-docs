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


import numpy as np

from motrixsim import SceneData, load_model
from motrixsim.render import RenderApp

# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view


def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/randomization.xml"
        # Load the scene model
        model = load_model(path)
        # Create the render instance of the model
        render_offset = []
        for i in range(4):
            for j in range(4):
                render_offset.append([-i * 2, j * 2, 0])
        render.launch(model, batch=16, render_offset=render_offset)
        # Create the physics data of the model
        data = SceneData(model, batch=(16,))
        ball = model.get_link(0)
        mass = np.random.uniform(0.1, 500.0, size=(16,))
        ball.set_mass_override(data, mass)
        mass_get = ball.get_mass_override(data)
        assert np.allclose(mass_get, mass)

        while True:
            model.step(data)
            render.sync(data)


if __name__ == "__main__":
    main()
