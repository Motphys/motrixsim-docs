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
        render.opt.set_left_panel_vis(True)
        # The scene description file
        path = "examples/assets/partial_rendering.xml"
        # Load the scene model
        model = load_model(path)

        render_offsets = []
        batch = 10
        for i in range(batch):
            render_offsets.append([i * 2.0, 0, 0])

        # Create the render instance of the model
        render.launch(model, batch, render_offsets)
        # Create the physics data of the model
        data = SceneData(model, batch=(batch,))

        target_scene_indices = [1, 3, 5, 7, 9]

        def render_step():
            if render.input.is_key_just_pressed("a"):
                render.set_scene_vis(target_scene_indices, False)

            if render.input.is_key_just_pressed("d"):
                render.set_scene_vis(target_scene_indices, True)

            if render.input.is_key_just_pressed("q"):
                render.set_all_scene_vis(False)

            if render.input.is_key_just_pressed("e"):
                render.set_all_scene_vis(True)

            render.sync(data)

        run.render_loop(model.options.timestep, 60, lambda: step(model, data), render_step)


# endtag

if __name__ == "__main__":
    main()
