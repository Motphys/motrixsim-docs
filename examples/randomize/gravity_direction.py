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


"""
Gravity Direction Randomization in a Transparent Box

This example demonstrates per-instance gravity override by placing a small ball
at the center of a transparent six-sided box and assigning each batch instance a
different gravity direction.

Physical intuition:
- The six translucent walls form a closed box.
- A small sphere starts near the center of each box.
- Every batch instance uses the same model, but a different Data-only gravity
  vector.
- The ball accelerates toward a different wall in each instance, showing that
  gravity direction is randomized per SceneData instance rather than by changing
  the shared Model options.

Key concepts:
- Scene-level gravity override with ``model.set_gravity_override(data, gravity)``
- Batch simulation to compare multiple gravity directions simultaneously

Mouse controls:
- Press and hold left button then drag to rotate the camera/view
- Press and hold right button then drag to pan/translate the view
"""

import numpy as np

from motrixsim import SceneData, load_mjcf_str
from motrixsim.render import RenderApp, RenderSettings

MJCF = """
<mujoco>
  <option timestep="0.01" iterations="16"/>
  <worldbody>
    <light pos="0 -3 4" dir="0 1 -1" directional="true"/>

    <geom name="reference_ground" type="plane" pos="0 0 -1.15"
          size="0 0 0" rgba="0.55 0.58 0.62 0.38"
          contype="0" conaffinity="0"/>

    <!--
      Six fixed planes form a closed half-space box for collision.
      For plane geoms, size only affects the finite visual rectangle; collision remains infinite.
      Using planes avoids transparent box slab overlap and makes the container visually stable.
    -->
    <geom name="wall_x_pos" type="plane" pos="1 0 0" zaxis="-1 0 0"
          size="1 1 0.01" rgba="0.2 0.7 1.0 0.10"
          friction="0.6 0.005 0.0001" condim="3"/>
    <geom name="wall_x_neg" type="plane" pos="-1 0 0" zaxis="1 0 0"
          size="1 1 0.01" rgba="0.2 0.7 1.0 0.10"
          friction="0.6 0.005 0.0001" condim="3"/>
    <geom name="wall_y_pos" type="plane" pos="0 1 0" zaxis="0 -1 0"
          size="1 1 0.01" rgba="0.2 0.7 1.0 0.10"
          friction="0.6 0.005 0.0001" condim="3"/>
    <geom name="wall_y_neg" type="plane" pos="0 -1 0" zaxis="0 1 0"
          size="1 1 0.01" rgba="0.2 0.7 1.0 0.10"
          friction="0.6 0.005 0.0001" condim="3"/>
    <geom name="wall_z_pos" type="plane" pos="0 0 1" zaxis="0 0 -1"
          size="1 1 0.01" rgba="0.2 0.7 1.0 0.10"
          friction="0.6 0.005 0.0001" condim="3"/>
    <geom name="wall_z_neg" type="plane" pos="0 0 -1" zaxis="0 0 1"
          size="1 1 0.01" rgba="0.2 0.7 1.0 0.10"
          friction="0.6 0.005 0.0001" condim="3"/>

    <body name="ball" pos="0 0 0">
      <freejoint/>
      <geom name="ball_geom" type="sphere" size="0.14"
            rgba="1.0 0.35 0.15 1.0" friction="0.8 0.005 0.0001"
            density="1200" condim="3"/>
    </body>
  </worldbody>
</mujoco>
"""

BATCH = 16
GRAVITY_MAGNITUDE = 6.0


def random_unit_vectors(rng: np.random.Generator, count: int) -> np.ndarray:
    vectors = rng.normal(size=(count, 3)).astype(np.float32)
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors


def main():
    with RenderApp() as render:
        model = load_mjcf_str(MJCF)

        render_offset = []
        for i in range(4):
            for j in range(4):
                render_offset.append([-i * 3.0, j * 3.0, 0])

        render_settings = RenderSettings(False, True, True, True, True)
        render.launch(
            model,
            batch=BATCH,
            render_offset=render_offset,
            render_settings=render_settings,
        )
        render.system_camera.set_view(
            lookat=[-4.5, 4.5, 0.0],
            distance=18.0,
            elevation=-35.0,
            azimuth=45.0,
        )
        data = SceneData(model, batch=(BATCH,))

        rng = np.random.default_rng(7)
        directions = random_unit_vectors(rng, BATCH)
        gravity = (directions * GRAVITY_MAGNITUDE).astype(np.float32)
        model.set_gravity_override(data, gravity)

        print("\n" + "=" * 72)
        print("Gravity Direction Randomization")
        print("=" * 72)
        for i, g in enumerate(gravity):
            print(f"  Instance {i:2d}: gravity = [{g[0]: .2f}, {g[1]: .2f}, {g[2]: .2f}]")
        print("=" * 72 + "\n")

        while not render.is_closed:
            model.step(data)
            render.sync(data)


if __name__ == "__main__":
    main()
