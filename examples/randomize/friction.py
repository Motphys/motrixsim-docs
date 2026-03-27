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
Geom Friction Randomization on a Ramp

This example demonstrates how per-geom friction overrides affect sliding
behavior of a box on a 30-degree ramp.

Physical intuition:
- A box is placed near the top of a 30-degree ramp. Gravity pulls it down.
- tan(30 deg) ~ 0.577, so slide friction below ~0.577 lets the box slide,
  and above ~0.577 the box grips and stays put.
- The 16 batch instances sweep slide friction from 0.01 to 2.0, clearly
  showing the transition from sliding to static.

Key concepts:
- Per-geom friction override using `set_friction_override`
- Batch simulation to compare multiple friction values simultaneously

Mouse controls:
- Press and hold left button then drag to rotate the camera/view
- Press and hold right button then drag to pan/translate the view
"""

import numpy as np

from motrixsim import SceneData, load_model
from motrixsim.render import RenderApp


def main():
    with RenderApp() as render:
        path = "examples/assets/box_on_ramp.xml"
        model = load_model(path)

        # 16 instances in a 4x4 grid
        render_offset = []
        for i in range(4):
            for j in range(4):
                render_offset.append([-i * 8.0, j * 8.0, 0])

        render.launch(model, batch=16, render_offset=render_offset)
        data = SceneData(model, batch=(16,))

        # Override box geom friction per batch
        box_geom = model.get_geom("box_geom")
        slide_frictions = np.linspace(0.01, 2.0, 16).astype(np.float32)
        frictions = np.zeros((16, 3), dtype=np.float32)
        frictions[:, 0] = slide_frictions
        box_geom.set_friction_override(data, frictions)

        # Print summary
        critical = np.tan(np.radians(30))
        print("\n" + "=" * 60)
        print(f"Box on 30-deg Ramp (critical friction ~ {critical:.3f})")
        print("=" * 60)
        for i in range(16):
            f = slide_frictions[i]
            status = "SLIDE" if f < critical else "GRIP"
            print(f"  Instance {i:2d}: friction = {f:.3f}  -> {status}")
        print("=" * 60 + "\n")

        while True:
            model.step(data)
            render.sync(data)


if __name__ == "__main__":
    main()
