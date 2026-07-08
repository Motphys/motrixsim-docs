# Copyright (C) 2020-2026 Motphys Technology Co., Ltd. All Rights Reserved.
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

import argparse
from pathlib import Path

import motrixsim as mx
from motrixsim.render import RenderApp

SCENE_MJCF = """
<mujoco>
  <option timestep="0.02"/>
  <visual>
    <global azimuth="90" elevation="-45" fovy="75"/>
  </visual>
  <asset>
    <texture type="skybox" builtin="gradient" rgb1=".45 .55 .68" rgb2="0 0 0"
      width="100" height="100"/>
  </asset>
  <worldbody>
    <light name="key" pos="0 -3 5" directional="true"/>
    <geom name="floor" type="plane" size="3.5 3.5 0.1" rgba="0.55 0.58 0.62 1"/>
    <body name="box" pos="0 0 0.24">
      <geom name="box" type="box" size="0.12 0.12 0.24" rgba="0.9 0.35 0.15 1"/>
    </body>
  </worldbody>
</mujoco>
"""


def make_grid_offsets(size: int, spacing: float) -> list[list[float]]:
    half_extent = (size - 1) * spacing * 0.5
    return [
        [col * spacing - half_extent, row * spacing - half_extent, 0.0] for row in range(size) for col in range(size)
    ]


def main():
    parser = argparse.ArgumentParser(description="Headless system camera batch capture example")
    parser.add_argument("--output", default="shot/system_camera_batch_capture.png", help="Output PNG path")
    parser.add_argument("--width", type=int, default=1024, help="Capture width")
    parser.add_argument("--height", type=int, default=768, help="Capture height")
    parser.add_argument("--warmup-frames", type=int, default=120, help="Physics/render frames before capture")
    args = parser.parse_args()

    grid_size = 4
    batch_size = grid_size * grid_size
    model = mx.msd.from_str(SCENE_MJCF).build()
    model.cameras.set_system_render_target("image", args.width, args.height)

    data = mx.SceneData(model, batch=(batch_size,))
    render_offset = make_grid_offsets(grid_size, spacing=0.42)

    with RenderApp(headless=True) as renderer:
        renderer.launch(model, batch=batch_size, render_offset=render_offset)
        renderer.system_camera.set_view(
            lookat=[0.0, 0.0, 0.35],
            distance=3.0,
            elevation=-30.0,
            azimuth=90.0,
        )

        for _ in range(args.warmup_frames):
            mx.step(model, data)
            renderer.sync(data, wait=True)

        task = renderer.system_camera.capture()
        renderer.sync(data, wait=True)

        image = task.take_image()
        if image is None:
            raise RuntimeError("System camera capture did not return an image")

        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save_to_disk(str(output))
        print(f"Captured {batch_size} objects to {output}")


if __name__ == "__main__":
    main()
