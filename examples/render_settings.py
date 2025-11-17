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
from motrixsim.render import RenderApp, RenderSettings

# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view


def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/render_settings.xml"
        # Load the scene model
        model = load_model(path)
        # Performance render settings, no shadows, no screen space effect.
        # performance_settings = RenderSettings.performance()
        # Quality render settings, enable shadows and screen space effect.
        quality_settings = RenderSettings.quality()
        quality_settings.simplify_render_mesh = True
        quality_settings.enable_oit = False
        quality_settings.enable_shadow = True
        quality_settings.enable_ssao = True
        # Create the render instance of the model
        render.launch(model, render_settings=quality_settings)
        # Create the physics data of the model
        data = SceneData(model)

        while True:
            # Control the step interval to prevent too fast simulation
            time.sleep(0.02)
            # Physics world step
            step(model, data)
            # Sync render objects from physic world
            render.sync(data)


if __name__ == "__main__":
    main()
