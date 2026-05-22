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

from dataclasses import dataclass

import numpy as np

from .contract import REQUIRED_MOTION_FIELDS


@dataclass(frozen=True)
class MotionData:
    joint_pos: np.ndarray
    joint_vel: np.ndarray
    body_pos_w: np.ndarray
    body_quat_w: np.ndarray
    body_lin_vel_w: np.ndarray
    body_ang_vel_w: np.ndarray


class MotionReference:
    """Load and advance G1 motion-tracking reference data from a `.npz` file."""

    def __init__(self, motion_file: str, body_indices: np.ndarray | None = None):
        data = np.load(motion_file)
        missing = [field_name for field_name in REQUIRED_MOTION_FIELDS if field_name not in data]
        if missing:
            raise ValueError("Motion reference is missing required fields: " + ", ".join(sorted(missing)))

        self.fps = int(np.asarray(data["fps"]).reshape(-1)[0])
        if self.fps <= 0:
            raise ValueError(f"Motion reference fps must be positive, got {self.fps}")

        self.joint_pos = np.asarray(data["joint_pos"], dtype=np.float32)
        self.joint_vel = np.asarray(data["joint_vel"], dtype=np.float32)
        body_pos_w = np.asarray(data["body_pos_w"], dtype=np.float32)
        body_quat_w = np.asarray(data["body_quat_w"], dtype=np.float32)
        body_lin_vel_w = np.asarray(data["body_lin_vel_w"], dtype=np.float32)
        body_ang_vel_w = np.asarray(data["body_ang_vel_w"], dtype=np.float32)
        if body_indices is not None:
            body_indices = np.asarray(body_indices, dtype=np.int32)
            body_pos_w = body_pos_w[:, body_indices]
            body_quat_w = body_quat_w[:, body_indices]
            body_lin_vel_w = body_lin_vel_w[:, body_indices]
            body_ang_vel_w = body_ang_vel_w[:, body_indices]

        self.body_pos_w = body_pos_w
        self.body_quat_w = body_quat_w
        self.body_lin_vel_w = body_lin_vel_w
        self.body_ang_vel_w = body_ang_vel_w

        self.num_frames = int(self.joint_pos.shape[0])
        if self.num_frames == 0:
            raise ValueError("Motion reference must contain at least one frame")

        self.current_frame = 0
        self._frame_accumulator = 0.0

    def frame(self, frame_index: int | None = None) -> MotionData:
        index = self.current_frame if frame_index is None else int(frame_index) % self.num_frames
        return MotionData(
            joint_pos=self.joint_pos[index].copy(),
            joint_vel=self.joint_vel[index].copy(),
            body_pos_w=self.body_pos_w[index].copy(),
            body_quat_w=self.body_quat_w[index].copy(),
            body_lin_vel_w=self.body_lin_vel_w[index].copy(),
            body_ang_vel_w=self.body_ang_vel_w[index].copy(),
        )

    def current(self) -> MotionData:
        return self.frame(self.current_frame)

    def advance(self, frames: int = 1) -> int:
        self.current_frame = (self.current_frame + int(frames)) % self.num_frames
        return self.current_frame

    def advance_by_dt(self, dt: float) -> int:
        self._frame_accumulator += float(dt) * self.fps
        whole_frames = int(self._frame_accumulator)
        if whole_frames <= 0:
            return self.current_frame

        self._frame_accumulator -= whole_frames
        return self.advance(whole_frames)
