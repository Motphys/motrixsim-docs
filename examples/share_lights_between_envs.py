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

from absl import app, flags

from motrixsim import SceneData, load_model, run
from motrixsim.render import RenderApp, RenderSettings

# uv run python examples/share_lights_between_envs.py --share_lights=False to disable light sharing between
# multiple simulation worlds
_ShareLights = flags.DEFINE_bool("share_lights", True, "Whether to share lights between multiple simulation worlds")


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def main(argv):
    # Create render window for visualization
    with RenderApp() as render:
        # tag::init batch data
        size = 10
        batch_size = size * size
        path = "examples/assets/multi_world_camera.xml"
        # Load the scene model
        model = load_model(path)
        data = SceneData(model, batch=(batch_size,))
        render_offset = []
        for i in range(size):
            for j in range(size):
                render_offset.append([-i * 2, j * 2, 0])

        print("Sharing lights between envs:", _ShareLights.value)

        render_settings = RenderSettings.performance()
        render_settings.enable_shadow = True
        render_settings.share_lights_between_envs = _ShareLights.value
        render.launch(model, batch=batch_size, render_offset=render_offset, render_settings=render_settings)

        run.render_loop(
            model.options.timestep,
            60.0,
            lambda: model.step(data),
            lambda: render.sync(data),
        )


if __name__ == "__main__":
    app.run(main)
