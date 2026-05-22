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

from __future__ import annotations

import html

import numpy as np

from motrixsim import SceneData, msd


class TerrainScanVisualizer:
    """Mocap-box overlay for visualizing terrain scan samples."""

    def __init__(
        self,
        *,
        scanner,
        frame,
        offsets: np.ndarray,
        mocaps: list,
        cube_half_size: tuple[float, float, float],
        z_bias: float,
    ):
        self.scanner = scanner
        self.frame = frame
        self.offsets = np.asarray(offsets, dtype=np.float32)
        self.mocaps = mocaps
        self.cube_half_size = cube_half_size
        self.z_bias = z_bias
        self._heights = np.empty((self.offsets.shape[0],), dtype=np.float32)
        self._pose = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], dtype=np.float32)

    @staticmethod
    def create_msd(
        offsets,
        *,
        name: str = "terrain_scan",
        cube_half_size: tuple[float, float, float] = (0.035, 0.035, 0.01),
        rgba: tuple[float, float, float, float] = (0.1, 0.7, 1.0, 0.8),
    ):
        """Create a root-level MSD world containing one mocap box per scan offset."""
        offsets = _normalize_offsets(offsets)
        size = " ".join(str(v) for v in cube_half_size)
        color = " ".join(str(v) for v in rgba)
        safe_name = html.escape(name, quote=True)
        bodies = []
        for index in range(offsets.shape[0]):
            body_name = f"{safe_name}_{index:03d}"
            geom_name = f"{body_name}_geom"
            bodies.append(
                f"""    <body name="{body_name}" mocap="true">
      <geom name="{geom_name}" type="box" size="{size}" rgba="{color}" contype="0" conaffinity="0"/>
    </body>"""
            )
        return msd.from_str(
            f"""<mujoco model="{safe_name}">
  <worldbody>
{chr(10).join(bodies)}
  </worldbody>
</mujoco>"""
        )

    @classmethod
    def from_model(
        cls,
        *,
        model,
        scanner,
        frame,
        offsets,
        name: str = "terrain_scan",
        cube_half_size: tuple[float, float, float] = (0.035, 0.035, 0.01),
        z_bias: float = 0.005,
    ) -> "TerrainScanVisualizer":
        """Bind a generated visualizer MSD to a built SceneModel."""
        offsets = _normalize_offsets(offsets)
        mocaps = []
        for index in range(offsets.shape[0]):
            body = model.get_body(f"{name}_{index:03d}")
            if body is None or body.mocap is None:
                raise RuntimeError(f"missing terrain scan mocap body: {name}_{index:03d}")
            mocaps.append(body.mocap)
        return cls(
            scanner=scanner,
            frame=frame,
            offsets=offsets,
            mocaps=mocaps,
            cube_half_size=cube_half_size,
            z_bias=z_bias,
        )

    def update(self, data: SceneData) -> None:
        """Update all mocap boxes to the latest scan world positions."""
        heights = self.scanner.scan(data, out=self._heights)
        pose = self.frame.get_pose(data)
        if np.asarray(pose).ndim != 1:
            raise ValueError("TerrainScanVisualizer only supports non-batched SceneData")

        frame_x, frame_y = pose[0], pose[1]
        qx, qy, qz, qw = pose[3], pose[4], pose[5], pose[6]
        yaw = np.arctan2(2.0 * (qw * qz + qx * qy), 1.0 - 2.0 * (qy**2 + qz**2))
        cos_yaw = np.cos(yaw)
        sin_yaw = np.sin(yaw)

        self._pose[3:] = [0.0, 0.0, 0.0, 1.0]
        for index, (offset_x, offset_y) in enumerate(self.offsets):
            self._pose[0] = frame_x + cos_yaw * offset_x - sin_yaw * offset_y
            self._pose[1] = frame_y + sin_yaw * offset_x + cos_yaw * offset_y
            self._pose[2] = heights[index] + self.cube_half_size[2] + self.z_bias
            self.mocaps[index].set_pose(data, self._pose)


def _normalize_offsets(offsets) -> np.ndarray:
    result = np.asarray(offsets, dtype=np.float32)
    if result.ndim != 2 or result.shape[1] != 2:
        raise ValueError("terrain scan offsets must have shape (N, 2)")
    return result
