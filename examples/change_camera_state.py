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
    with RenderApp() as render:
        render.opt.set_left_panel_vis(True)

        # The scene description file
        path = "examples/assets/control_cameras.xml"
        # Load the scene model
        model = load_model(path)

        cameras = model.cameras
        cameras[0].set_render_target("image", 320, 240)

        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)

        while True:
            # Control the step interval to prevent too fast simulation
            time.sleep(0.001)
            # Physics world step
            step(model, data)
            # Sync render objects from physic world
            render.sync(data)

            system_camera = render.system_camera
            # Disable the system camera.
            if render.input.is_key_just_pressed("a"):
                system_camera.active = False
            # Enable the masystemin camera.
            if render.input.is_key_just_pressed("d"):
                system_camera.active = True

            scene_camera = render.get_camera(0)
            # Disable the main camera.
            if render.input.is_key_just_pressed("q"):
                scene_camera.active = False
            # Enable the main camera.
            if render.input.is_key_just_pressed("e"):
                scene_camera.active = True


if __name__ == "__main__":
    main()
