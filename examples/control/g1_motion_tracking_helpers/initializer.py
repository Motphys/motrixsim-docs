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

import numpy as np

from motrixsim import PositionActuator

from . import contract
from .reference import MotionData


def _wxyz_to_xyzw(quat_wxyz: np.ndarray) -> np.ndarray:
    quat_wxyz = np.asarray(quat_wxyz, dtype=np.float32)
    return np.array([quat_wxyz[1], quat_wxyz[2], quat_wxyz[3], quat_wxyz[0]], dtype=np.float32)


def initialize_motion_tracking_state(robot, model, data, motion_data: MotionData, root_body_index: int = 0) -> None:
    """Initialize the robot to the first motion frame before playback starts."""

    body = robot.body
    floatingbase = body.floatingbase
    if floatingbase is None:
        raise ValueError("G1 motion tracking playback requires a floating-base robot body")

    root_pos = np.asarray(motion_data.body_pos_w[root_body_index], dtype=np.float32)
    root_quat_xyzw = _wxyz_to_xyzw(motion_data.body_quat_w[root_body_index])
    root_lin_vel = np.asarray(motion_data.body_lin_vel_w[root_body_index], dtype=np.float32)
    root_ang_vel = np.asarray(motion_data.body_ang_vel_w[root_body_index], dtype=np.float32)
    joint_pos = np.asarray(motion_data.joint_pos, dtype=np.float32)
    joint_vel = np.asarray(motion_data.joint_vel, dtype=np.float32)
    dof_pos = np.concatenate([root_pos, root_quat_xyzw, joint_pos]).astype(np.float32, copy=False)
    dof_vel = np.concatenate([root_lin_vel, root_ang_vel, joint_vel]).astype(np.float32, copy=False)

    body.set_dof_pos(data, dof_pos)
    body.set_dof_vel(data, dof_vel)
    floatingbase.set_translation(data, root_pos)
    floatingbase.set_rotation(data, root_quat_xyzw)
    floatingbase.set_global_linear_velocity(data, root_lin_vel)
    floatingbase.set_global_angular_velocity(data, root_ang_vel)
    body.set_actuator_ctrls(data, joint_pos)
    model.forward_kinematic(data)


def _profile_value(value: float) -> np.ndarray:
    return np.asarray(value, dtype=np.float32)


def _ensure_profile_length(name: str, values: tuple[float, ...], expected: int = contract.EXPECTED_ACTION_DIM) -> None:
    if len(values) != expected:
        raise ValueError(f"{name} must contain {expected} values, got {len(values)}")


def apply_motion_tracking_profile(model, data) -> None:
    """Apply task-specific runtime parameters on top of the shared G1 model."""

    _ensure_profile_length("ACTUATOR_NAMES", contract.ACTUATOR_NAMES)
    _ensure_profile_length("ACTUATOR_KP_PROFILE", contract.ACTUATOR_KP_PROFILE)
    _ensure_profile_length("ACTUATOR_KD_PROFILE", contract.ACTUATOR_KD_PROFILE)
    _ensure_profile_length("JOINT_NAMES", contract.JOINT_NAMES)
    _ensure_profile_length("JOINT_ARMATURE_PROFILE", contract.JOINT_ARMATURE_PROFILE)
    _ensure_profile_length("JOINT_FRICTIONLOSS_PROFILE", contract.JOINT_FRICTIONLOSS_PROFILE)

    for actuator_name, kp, kd in zip(
        contract.ACTUATOR_NAMES,
        contract.ACTUATOR_KP_PROFILE,
        contract.ACTUATOR_KD_PROFILE,
        strict=True,
    ):
        actuator = model.get_actuator(actuator_name)
        if not isinstance(actuator, PositionActuator):
            raise TypeError(f"Actuator '{actuator_name}' must be a position actuator")
        actuator.set_kp_override(data, _profile_value(kp))
        actuator.set_damping_override(data, _profile_value(kd))

    for joint_name, armature, frictionloss in zip(
        contract.JOINT_NAMES,
        contract.JOINT_ARMATURE_PROFILE,
        contract.JOINT_FRICTIONLOSS_PROFILE,
        strict=True,
    ):
        joint = model.get_joint(joint_name)
        if joint is None:
            raise ValueError(f"Joint '{joint_name}' not found in model")
        joint.set_armature_override(data, _profile_value(armature))
        joint.set_frictionloss_override(data, _profile_value(frictionloss))
