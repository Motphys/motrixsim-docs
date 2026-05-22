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

from pathlib import Path
from typing import Sequence

EXPECTED_ACTION_DIM = 29
EXPECTED_OBS_DIM = 160
DEFAULT_ACTION_SCALE = 0.25
DEFAULT_SIM_DT = 0.02 / 3.0
DEFAULT_CTRL_DT = 0.02
DEFAULT_RENDER_FPS = 60.0

LOCAL_LINEAR_VELOCITY_SENSOR = "local_linvel_pelvis"
GYRO_SENSOR = "gyro_torso"
REQUIRED_SENSOR_NAMES = (LOCAL_LINEAR_VELOCITY_SENSOR, GYRO_SENSOR)
REQUIRED_MOTION_FIELDS = (
    "fps",
    "joint_pos",
    "joint_vel",
    "body_pos_w",
    "body_quat_w",
    "body_lin_vel_w",
    "body_ang_vel_w",
)

ANCHOR_BODY_NAME = "torso_link"
BODY_NAMES = (
    "pelvis",
    "left_hip_roll_link",
    "left_knee_link",
    "left_ankle_roll_link",
    "right_hip_roll_link",
    "right_knee_link",
    "right_ankle_roll_link",
    "torso_link",
    "left_shoulder_roll_link",
    "left_elbow_link",
    "left_wrist_yaw_link",
    "right_shoulder_roll_link",
    "right_elbow_link",
    "right_wrist_yaw_link",
)
MOTION_BODY_INDICES = (1, 3, 5, 7, 9, 11, 13, 16, 18, 20, 23, 25, 27, 30)

EXAMPLES_DIR = Path(__file__).resolve().parents[2]
ASSET_DIR = EXAMPLES_DIR / "assets" / "g1_motion_tracking"
SHARED_G1_DIR = EXAMPLES_DIR / "assets" / "g1"
DEFAULT_ONNX_PATH = ASSET_DIR / "model_4999_single.onnx"
DEFAULT_MOTION_PATH = ASSET_DIR / "dance1_subject2_part.npz"
DEFAULT_SCENE_PATH = ASSET_DIR / "scene_flat.xml"
DEFAULT_ROBOT_PATH = SHARED_G1_DIR / "g1.xml"

ACTUATOR_NAMES = (
    "left_hip_pitch_joint",
    "left_hip_roll_joint",
    "left_hip_yaw_joint",
    "left_knee_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_hip_pitch_joint",
    "right_hip_roll_joint",
    "right_hip_yaw_joint",
    "right_knee_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",
    "waist_yaw_joint",
    "waist_roll_joint",
    "waist_pitch_joint",
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "left_wrist_pitch_joint",
    "left_wrist_yaw_joint",
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
    "right_wrist_pitch_joint",
    "right_wrist_yaw_joint",
)
JOINT_NAMES = ACTUATOR_NAMES

ACTUATOR_KP_PROFILE = (
    40.179,
    99.098,
    40.179,
    99.098,
    28.501,
    28.501,
    40.179,
    99.098,
    40.179,
    99.098,
    28.501,
    28.501,
    40.179,
    28.501,
    28.501,
    14.251,
    14.251,
    14.251,
    14.251,
    14.251,
    16.778,
    16.778,
    14.251,
    14.251,
    14.251,
    14.251,
    14.251,
    16.778,
    16.778,
)
ACTUATOR_KD_PROFILE = (0.0,) * EXPECTED_ACTION_DIM
JOINT_ARMATURE_PROFILE = (0.01,) * EXPECTED_ACTION_DIM
JOINT_FRICTIONLOSS_PROFILE = (0.3,) * EXPECTED_ACTION_DIM


def expected_obs_dim(num_actions: int = EXPECTED_ACTION_DIM) -> int:
    return 15 + num_actions * 5


def ensure_file_exists(path: str | Path, description: str) -> Path:
    resolved = Path(path).expanduser().resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"{description} file not found: {resolved}")
    return resolved


def ensure_actuator_count(model, expected_num_actuators: int = EXPECTED_ACTION_DIM) -> None:
    actual = int(model.num_actuators)
    if actual != expected_num_actuators:
        raise ValueError(f"G1 motion tracking expects {expected_num_actuators} actuators, got {actual}")


def ensure_body_names(model, body_names: Sequence[str] = BODY_NAMES) -> None:
    missing = [name for name in body_names if model.get_link(name) is None]
    if missing:
        raise ValueError(f"Model is missing required body links: {', '.join(missing)}")


def ensure_sensor_names(model, data, sensor_names: Sequence[str] = REQUIRED_SENSOR_NAMES) -> None:
    missing: list[str] = []
    for sensor_name in sensor_names:
        try:
            model.get_sensor_value(sensor_name, data)
        except Exception:
            missing.append(sensor_name)

    if missing:
        raise ValueError(f"Model is missing required sensors: {', '.join(missing)}")
