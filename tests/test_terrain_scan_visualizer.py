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

import sys
from pathlib import Path

import numpy as np

from motrixsim import GeomHField, SceneData, TerrainScanner, msd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))

from utils.terrain_scan_visualizer import TerrainScanVisualizer

MJCF = """
<mujoco>
  <asset>
    <hfield name="terrain1" nrow="3" ncol="3"
            elevation="0 0 0  0 0.5 0  0 0 1"
            size="2 2 1 0"/>
  </asset>
  <worldbody>
    <body name="robot" pos="0 0 2">
      <joint type="free"/>
      <geom type="sphere" size="0.1"/>
    </body>
    <geom name="terrain" type="hfield" hfield="terrain1" pos="0 0 0"/>
  </worldbody>
</mujoco>
"""


def test_terrain_scan_visualizer_updates_mocaps():
    offsets = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    world = msd.from_str(MJCF)
    world.attach(TerrainScanVisualizer.create_msd(offsets, cube_half_size=(0.05, 0.05, 0.02)))
    model = world.build()
    data = SceneData(model)

    terrain = model.get_geom("terrain")
    assert isinstance(terrain, GeomHField)
    frame = model.get_link("robot")
    scanner = TerrainScanner(terrain, frame, offsets)
    visualizer = TerrainScanVisualizer.from_model(
        model=model,
        scanner=scanner,
        frame=frame,
        offsets=offsets,
        cube_half_size=(0.05, 0.05, 0.02),
        z_bias=0.003,
    )

    visualizer.update(data)
    model.forward_kinematic(data)

    heights = scanner.scan(data)
    for index, offset in enumerate(offsets):
        pose = model.get_body(f"terrain_scan_{index:03d}").get_pose(data)
        np.testing.assert_allclose(pose[:2], offset, atol=1e-6)
        np.testing.assert_allclose(pose[2], heights[index] + 0.023, atol=1e-6)
