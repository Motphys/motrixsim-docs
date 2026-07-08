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

from __future__ import annotations

import importlib
from typing import Sequence

import numpy as np

from .contract import (
    ANCHOR_BODY_NAME,
    BODY_NAMES,
    DEFAULT_ACTION_SCALE,
    EXPECTED_ACTION_DIM,
    EXPECTED_OBS_DIM,
)
from .reference import MotionData


def resolve_onnx_providers(device: str, available_providers: Sequence[str]) -> list[str]:
    providers: list[str] = []
    if device.startswith("cuda") and "CUDAExecutionProvider" in available_providers:
        providers.append("CUDAExecutionProvider")
    if "CPUExecutionProvider" in available_providers:
        providers.append("CPUExecutionProvider")
    return providers or list(available_providers)


def _import_onnxruntime():
    try:
        return importlib.import_module("onnxruntime")
    except ImportError as exc:
        raise ImportError(
            "onnxruntime is required to run G1 motion tracking playback. "
            "Install it from `motrixsim-python` with "
            "`uv sync --all-packages --all-extras --reinstall-package motrixsim-core`."
        ) from exc


def _last_dim(shape) -> int | None:
    if not shape:
        return None
    last = shape[-1]
    return int(last) if isinstance(last, int) else None


def _xyzw_to_wxyz(quat_xyzw: np.ndarray) -> np.ndarray:
    quat_xyzw = np.asarray(quat_xyzw, dtype=np.float32)
    return np.array([quat_xyzw[3], quat_xyzw[0], quat_xyzw[1], quat_xyzw[2]], dtype=np.float32)


def _quat_conjugate(quat: np.ndarray) -> np.ndarray:
    quat = np.asarray(quat, dtype=np.float32)
    return np.array([quat[0], -quat[1], -quat[2], -quat[3]], dtype=np.float32)


def _quat_inv(quat: np.ndarray) -> np.ndarray:
    return _quat_conjugate(quat)


def _quat_mul(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    w1, x1, y1, z1 = np.asarray(q1, dtype=np.float32)
    w2, x2, y2, z2 = np.asarray(q2, dtype=np.float32)
    return np.array(
        [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        ],
        dtype=np.float32,
    )


def _quat_apply(quat: np.ndarray, vector: np.ndarray) -> np.ndarray:
    quat = np.asarray(quat, dtype=np.float32)
    vector = np.asarray(vector, dtype=np.float32)

    w, x, y, z = quat
    vx, vy, vz = vector

    t = 2.0 * np.array(
        [
            y * vz - z * vy,
            z * vx - x * vz,
            x * vy - y * vx,
        ],
        dtype=np.float32,
    )
    t += 2.0 * w * vector

    return vector + np.array(
        [
            y * t[2] - z * t[1],
            z * t[0] - x * t[2],
            x * t[1] - y * t[0],
        ],
        dtype=np.float32,
    )


def _subtract_frame_transforms(
    frame_pos_w: np.ndarray,
    frame_quat_w: np.ndarray,
    target_pos_w: np.ndarray,
    target_quat_w: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    frame_pos_w = np.asarray(frame_pos_w, dtype=np.float32)
    frame_quat_w = np.asarray(frame_quat_w, dtype=np.float32)
    target_pos_w = np.asarray(target_pos_w, dtype=np.float32)
    target_quat_w = np.asarray(target_quat_w, dtype=np.float32)

    rel_pos = _quat_apply(_quat_inv(frame_quat_w), target_pos_w - frame_pos_w)
    rel_quat = _quat_mul(_quat_inv(frame_quat_w), target_quat_w)
    return rel_pos.astype(np.float32), rel_quat.astype(np.float32)


def _matrix_from_quat(quat: np.ndarray) -> np.ndarray:
    w, x, y, z = np.asarray(quat, dtype=np.float32)
    xx = x * x
    yy = y * y
    zz = z * z
    xy = x * y
    xz = x * z
    yz = y * z
    wx = w * x
    wy = w * y
    wz = w * z

    return np.array(
        [
            [1.0 - 2.0 * (yy + zz), 2.0 * (xy - wz), 2.0 * (xz + wy)],
            [2.0 * (xy + wz), 1.0 - 2.0 * (xx + zz), 2.0 * (yz - wx)],
            [2.0 * (xz - wy), 2.0 * (yz + wx), 1.0 - 2.0 * (xx + yy)],
        ],
        dtype=np.float32,
    )


class G1MotionTrackingPolicy:
    """Standalone ONNX playback policy for G1 motion tracking."""

    def __init__(
        self,
        robot,
        onnx_path: str,
        action_scale: float = DEFAULT_ACTION_SCALE,
        device: str = "cpu",
        body_names: Sequence[str] = BODY_NAMES,
        anchor_body_name: str = ANCHOR_BODY_NAME,
    ):
        self._robot = robot
        self._body_names = tuple(body_names)
        self._anchor_body_name = anchor_body_name
        self._anchor_body_index = self._body_names.index(anchor_body_name)

        self.default_angles = np.asarray(robot._DEFAULT_ANGLES, dtype=np.float32).copy()
        if self.default_angles.shape != (EXPECTED_ACTION_DIM,):
            raise ValueError(
                f"G1 motion tracking expects {EXPECTED_ACTION_DIM} default angles, "
                f"got shape {self.default_angles.shape}"
            )

        self.action_scale = float(action_scale)
        self.last_actions = np.zeros(EXPECTED_ACTION_DIM, dtype=np.float32)

        ort = _import_onnxruntime()
        providers = resolve_onnx_providers(device, ort.get_available_providers())
        self._policy_session = ort.InferenceSession(onnx_path, providers=providers)

        inputs = self._policy_session.get_inputs()
        outputs = self._policy_session.get_outputs()
        if len(inputs) != 1 or len(outputs) != 1:
            raise ValueError(
                "Expected ONNX policy with exactly one input and one output, "
                f"got inputs={[value.name for value in inputs]}, "
                f"outputs={[value.name for value in outputs]}"
            )

        self._input_name = inputs[0].name
        self._output_name = outputs[0].name
        input_dim = _last_dim(inputs[0].shape)
        output_dim = _last_dim(outputs[0].shape)
        if input_dim != EXPECTED_OBS_DIM:
            raise ValueError(f"Expected ONNX input dim {EXPECTED_OBS_DIM}, got {inputs[0].shape}")
        if output_dim != EXPECTED_ACTION_DIM:
            raise ValueError(f"Expected ONNX output dim {EXPECTED_ACTION_DIM}, got {outputs[0].shape}")

    def build_actor_observation(self, data, motion_data: MotionData) -> np.ndarray:
        anchor_link = self._robot.model.get_link(self._anchor_body_name)
        if anchor_link is None:
            raise ValueError(f"Anchor link '{self._anchor_body_name}' not found in model")

        robot_anchor_pose = np.asarray(anchor_link.get_pose(data), dtype=np.float32)
        robot_anchor_pos_w = robot_anchor_pose[:3]
        robot_anchor_quat_w = _xyzw_to_wxyz(robot_anchor_pose[3:7])

        motion_anchor_pos_w = np.asarray(motion_data.body_pos_w[self._anchor_body_index], dtype=np.float32)
        motion_anchor_quat_w = np.asarray(motion_data.body_quat_w[self._anchor_body_index], dtype=np.float32)

        motion_anchor_pos_b, motion_anchor_ori_rel = _subtract_frame_transforms(
            robot_anchor_pos_w,
            robot_anchor_quat_w,
            motion_anchor_pos_w,
            motion_anchor_quat_w,
        )
        motion_anchor_ori_b = _matrix_from_quat(motion_anchor_ori_rel)[:, :2].reshape(6)

        linvel = np.asarray(self._robot.local_linear_vel(data), dtype=np.float32)
        gyro = np.asarray(self._robot.gyro(data), dtype=np.float32)
        dof_pos = np.asarray(self._robot.dof_pos(data), dtype=np.float32)
        dof_vel = np.asarray(self._robot.dof_vel(data), dtype=np.float32)
        joint_pos_rel = dof_pos - self.default_angles

        observation = np.concatenate(
            [
                np.asarray(motion_data.joint_pos, dtype=np.float32),
                np.asarray(motion_data.joint_vel, dtype=np.float32),
                motion_anchor_pos_b,
                motion_anchor_ori_b,
                linvel,
                gyro,
                joint_pos_rel,
                dof_vel,
                self.last_actions,
            ]
        ).astype(np.float32, copy=False)

        if observation.shape != (EXPECTED_OBS_DIM,):
            raise ValueError(f"Expected actor observation shape {(EXPECTED_OBS_DIM,)}, got {observation.shape}")
        return observation

    def compute_action(self, observation: np.ndarray) -> np.ndarray:
        observation = np.asarray(observation, dtype=np.float32)
        if observation.shape != (EXPECTED_OBS_DIM,):
            raise ValueError(f"Expected actor observation shape {(EXPECTED_OBS_DIM,)}, got {observation.shape}")

        outputs = self._policy_session.run(
            [self._output_name],
            {self._input_name: observation.reshape(1, -1)},
        )
        action = np.asarray(outputs[0][0], dtype=np.float32)
        if action.shape != (EXPECTED_ACTION_DIM,):
            raise ValueError(f"Expected action shape {(EXPECTED_ACTION_DIM,)}, got {action.shape}")
        return action

    def apply_action(self, data, action: np.ndarray) -> None:
        action = np.asarray(action, dtype=np.float32)
        if action.shape != (EXPECTED_ACTION_DIM,):
            raise ValueError(f"Expected action shape {(EXPECTED_ACTION_DIM,)}, got {action.shape}")

        ctrl = action * self.action_scale + self.default_angles
        self._robot.set_actuator_ctrls(data, ctrl)
        self.last_actions = action.copy()

    def step(self, data, motion_data: MotionData) -> np.ndarray:
        observation = self.build_actor_observation(data, motion_data)
        action = self.compute_action(observation)
        self.apply_action(data, action)
        return action
