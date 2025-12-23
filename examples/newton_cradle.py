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
    # The scene description file
    path = "examples/assets/newton_cradle_mt.xml"
    # Load the scene model
    model = load_model(path)
    # Create render window for visualization
    with RenderApp() as render:
        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)
        run.render_loop(model.options.timestep, 60, lambda: step(model, data), lambda: render.sync(data))


if __name__ == "__main__":
    main()
