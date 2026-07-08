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

from pathlib import Path

import numpy as np
import onnxruntime as ort

from motrixsim import SceneData, SceneModel, load_model
from motrixsim.render import RenderApp

ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "rm65_open_cabinet"
MODEL_FILE = ASSET_DIR / "scene.xml"
ONNX_FILE = ASSET_DIR / "rm65_open_cabinet.onnx"

CTRL_DT = 0.025
BASE_OBS_DIM = 21
ACTION_DIM = 7
ARM_ACTION_DIM = 6
ACTION_HISTORY_LEN = 9
ACTION_DELAY_STEPS = 6
VEL_SCALE = 0.5

ARM_JOINTS = [
    "joint_1",
    "joint_2",
    "joint_3",
    "joint_4",
    "joint_5",
    "joint_6",
    "gripper_Left_1_Joint",
]
GRIPPER_SITE = "gripper"
DRAWER_HANDLE_SITE = "drawer_bottom_handle"
DRAWER_JOINT = "drawer_bottom_joint"
CABINET_RESET_JOINTS = [
    "door_right_joint",
    "door_left_joint",
    "drawer_top_joint",
    DRAWER_JOINT,
]

INIT_CTRL = np.zeros(ACTION_DIM, dtype=np.float32)
CTRL_MIN = np.array([-3.106, -2.2689, -2.356, -3.106, -2.234, -6.28, -0.91], dtype=np.float32)
CTRL_MAX = np.array([3.106, 2.2689, 2.356, 3.106, 2.234, 6.28, 0.0], dtype=np.float32)

MAX_ARM_STEP = 1.15 * CTRL_DT
MAX_ARM_ACC_STEP = 10.47 * CTRL_DT * CTRL_DT
ARM_LAG_ALPHA = 0.062
GRIPPER_OPEN = 0.0
GRIPPER_CLOSED = -0.91
GRIPPER_MAX_STEP = 4.0 * CTRL_DT
GRIPPER_LAG_ALPHA = 0.062
GRIPPER_HOLD_ACTION = -10.0
GRIPPER_CLOSE_ON_THRESHOLD = 0.78
GRIPPER_OPEN_OFF_THRESHOLD = 0.62
GRIPPER_MIN_SWITCH_STEPS = 10
DRAWER_OPEN_THRESHOLD = 0.38
DRAWER_SUCCESS_HOLD_SECONDS = 1.0
DRAWER_TIMEOUT_SECONDS = 60.0
DRAWER_SUCCESS_HOLD_STEPS = max(1, round(DRAWER_SUCCESS_HOLD_SECONDS / CTRL_DT))
DRAWER_TIMEOUT_STEPS = max(DRAWER_SUCCESS_HOLD_STEPS + 1, round(DRAWER_TIMEOUT_SECONDS / CTRL_DT))


def drawer_is_open(drawer_pos: float) -> bool:
    return drawer_pos >= DRAWER_OPEN_THRESHOLD


def quat_conjugate(q: np.ndarray) -> np.ndarray:
    return np.array([-q[0], -q[1], -q[2], q[3]], dtype=np.float32)


def quat_mul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    q = np.array(
        [
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz,
        ],
        dtype=np.float32,
    )
    norm = np.linalg.norm(q)
    return q / norm if norm > 1e-6 else np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)


def scale_to_minus_one_one(value: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
    return 2.0 * (value - lower) / (upper - lower) - 1.0


def scale_from_minus_one_one(value: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
    return lower + (value + 1.0) * 0.5 * (upper - lower)


def sigmoid(value: float) -> float:
    return float(1.0 / (1.0 + np.exp(-value)))


class Rm65OpenCabinetPolicy:
    def __init__(self, model: SceneModel):
        self.model = model
        self.joints = [self._require(model.get_joint(name), f"joint {name}") for name in ARM_JOINTS]
        self.cabinet_joints = [self._require(model.get_joint(name), f"joint {name}") for name in CABINET_RESET_JOINTS]
        self.drawer_joint = self._require(model.get_joint(DRAWER_JOINT), f"joint {DRAWER_JOINT}")
        self.actuators = [self._require(model.get_actuator(index), f"actuator {index}") for index in range(ACTION_DIM)]
        self.gripper_site = self._require(model.get_site(GRIPPER_SITE), f"site {GRIPPER_SITE}")
        self.handle_site = self._require(model.get_site(DRAWER_HANDLE_SITE), f"site {DRAWER_HANDLE_SITE}")

        self.session = ort.InferenceSession(str(ONNX_FILE), providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        self.reset_cache()

    @staticmethod
    def _require(value, description: str):
        if value is None:
            raise RuntimeError(f"missing {description}")
        return value

    def hold_action(self) -> np.ndarray:
        action = np.zeros(ACTION_DIM, dtype=np.float32)
        action[:ARM_ACTION_DIM] = scale_to_minus_one_one(
            INIT_CTRL[:ARM_ACTION_DIM], CTRL_MIN[:ARM_ACTION_DIM], CTRL_MAX[:ARM_ACTION_DIM]
        )
        action[ARM_ACTION_DIM] = GRIPPER_HOLD_ACTION
        return action

    def reset_cache(self) -> None:
        hold_action = self.hold_action()
        self.prev_dof_pos: np.ndarray | None = None
        self.action_history = np.tile(hold_action, ACTION_HISTORY_LEN).astype(np.float32)
        self.action_delay_buffer = np.tile(hold_action, (ACTION_DELAY_STEPS + 1, 1)).astype(np.float32)
        self.arm_prev_delta = np.zeros(ARM_ACTION_DIM, dtype=np.float32)
        self.arm_actuator_target = np.zeros(ARM_ACTION_DIM, dtype=np.float32)
        self.gripper_target_smooth = float(GRIPPER_OPEN)
        self.gripper_binary_closed = False
        self.gripper_steps_since_switch = GRIPPER_MIN_SWITCH_STEPS
        self.episode_control_steps = 0
        self.success_hold_steps = 0
        self.success_latched = False

    def reset_data(self, data: SceneData) -> None:
        for joint in self.cabinet_joints:
            joint.set_dof_pos(data, [0.0])
        for joint, value in zip(self.joints, INIT_CTRL):
            joint.set_dof_pos(data, [float(value)])
        data.set_dof_vel(np.zeros_like(data.dof_vel))
        for actuator, value in zip(self.actuators, INIT_CTRL):
            actuator.set_ctrl(data, float(value))
        self.model.forward_kinematic(data)
        self.reset_cache()

    def robot_joint_pos(self, data: SceneData) -> np.ndarray:
        return np.array([joint.get_dof_pos(data)[0] for joint in self.joints], dtype=np.float32)

    def drawer_position(self, data: SceneData) -> float:
        return float(self.drawer_joint.get_dof_pos(data)[0])

    def target_relative_pose(self, data: SceneData) -> np.ndarray:
        gripper_pose = np.asarray(self.gripper_site.get_pose(data), dtype=np.float32)
        handle_pose = np.asarray(self.handle_site.get_pose(data), dtype=np.float32)

        pos_delta = handle_pose[:3] - gripper_pose[:3]
        quat_delta = quat_mul(handle_pose[3:7], quat_conjugate(gripper_pose[3:7]))
        if quat_delta[3] < 0.0:
            quat_delta = -quat_delta
        return np.concatenate([pos_delta, quat_delta]).astype(np.float32)

    def compute_observation(self, data: SceneData) -> np.ndarray:
        dof_pos = self.robot_joint_pos(data)
        dof_pos_scaled = scale_to_minus_one_one(dof_pos, CTRL_MIN, CTRL_MAX)
        if self.prev_dof_pos is None:
            dof_vel_rel = np.zeros(ACTION_DIM, dtype=np.float32)
        else:
            dof_vel_rel = (dof_pos - self.prev_dof_pos) / CTRL_DT * VEL_SCALE
        self.prev_dof_pos = dof_pos.copy()

        obs = np.concatenate(
            [
                dof_pos_scaled,
                dof_vel_rel,
                self.target_relative_pose(data),
                self.action_history,
            ]
        ).astype(np.float32)
        assert obs.shape == (BASE_OBS_DIM + ACTION_DIM * ACTION_HISTORY_LEN,)
        return np.clip(obs, -5.0, 5.0)

    def apply_action(self, data: SceneData, raw_action: np.ndarray) -> None:
        raw_action = np.asarray(raw_action, dtype=np.float32).reshape(ACTION_DIM)
        self.action_delay_buffer = np.vstack([raw_action, self.action_delay_buffer[:-1]])
        delayed_action = self.action_delay_buffer[ACTION_DELAY_STEPS]

        self.action_history = np.concatenate([raw_action, self.action_history[:-ACTION_DIM]]).astype(np.float32)

        dof_pos = self.robot_joint_pos(data)
        target_ctrl = np.zeros(ACTION_DIM, dtype=np.float32)
        target = scale_from_minus_one_one(
            np.clip(delayed_action[:ARM_ACTION_DIM], -1.0, 1.0),
            CTRL_MIN[:ARM_ACTION_DIM],
            CTRL_MAX[:ARM_ACTION_DIM],
        )
        limited_delta = np.clip(target - dof_pos[:ARM_ACTION_DIM], -MAX_ARM_STEP, MAX_ARM_STEP)
        acc_limited_delta = np.clip(
            limited_delta,
            self.arm_prev_delta - MAX_ARM_ACC_STEP,
            self.arm_prev_delta + MAX_ARM_ACC_STEP,
        )
        self.arm_prev_delta = acc_limited_delta
        target_joint_pos = dof_pos[:ARM_ACTION_DIM] + acc_limited_delta
        self.arm_actuator_target = (1.0 - ARM_LAG_ALPHA) * self.arm_actuator_target + ARM_LAG_ALPHA * target_joint_pos
        target_ctrl[:ARM_ACTION_DIM] = np.clip(
            self.arm_actuator_target,
            CTRL_MIN[:ARM_ACTION_DIM],
            CTRL_MAX[:ARM_ACTION_DIM],
        )

        close_ratio = sigmoid(float(delayed_action[ARM_ACTION_DIM]))
        if self.gripper_steps_since_switch >= GRIPPER_MIN_SWITCH_STEPS:
            should_close = not self.gripper_binary_closed and close_ratio >= GRIPPER_CLOSE_ON_THRESHOLD
            should_open = self.gripper_binary_closed and close_ratio <= GRIPPER_OPEN_OFF_THRESHOLD
            if should_close or should_open:
                self.gripper_binary_closed = should_close
                self.gripper_steps_since_switch = 0
        self.gripper_steps_since_switch += 1

        gripper_target = GRIPPER_CLOSED if self.gripper_binary_closed else GRIPPER_OPEN
        gripper_limited = self.gripper_target_smooth + np.clip(
            gripper_target - self.gripper_target_smooth,
            -GRIPPER_MAX_STEP,
            GRIPPER_MAX_STEP,
        )
        self.gripper_target_smooth = (
            1.0 - GRIPPER_LAG_ALPHA
        ) * self.gripper_target_smooth + GRIPPER_LAG_ALPHA * gripper_limited
        target_ctrl[ARM_ACTION_DIM] = np.clip(
            self.gripper_target_smooth,
            CTRL_MIN[ARM_ACTION_DIM],
            CTRL_MAX[ARM_ACTION_DIM],
        )

        for actuator, ctrl in zip(self.actuators, target_ctrl):
            actuator.set_ctrl(data, float(ctrl))

    def maybe_reset_episode(self, data: SceneData) -> bool:
        self.episode_control_steps += 1
        if not self.success_latched and drawer_is_open(self.drawer_position(data)):
            self.success_latched = True

        if self.success_latched:
            self.success_hold_steps += 1
            if self.success_hold_steps >= DRAWER_SUCCESS_HOLD_STEPS:
                self.reset_data(data)
                return True
            return False

        if self.episode_control_steps >= DRAWER_TIMEOUT_STEPS:
            self.reset_data(data)
            return True
        return False

    def step(self, data: SceneData) -> bool:
        if not self.success_latched and drawer_is_open(self.drawer_position(data)):
            self.success_latched = True
        if self.success_latched:
            return self.maybe_reset_episode(data)

        obs = self.compute_observation(data).reshape(1, -1).astype(np.float32)
        actions = self.session.run([self.output_name], {self.input_name: obs})[0][0]
        self.apply_action(data, actions)
        return self.maybe_reset_episode(data)


def main() -> None:
    model = load_model(str(MODEL_FILE))
    data = SceneData(model)
    policy = Rm65OpenCabinetPolicy(model)
    policy.reset_data(data)

    phys_dt = float(model.options.timestep)
    ctrl_interval = max(1, round(CTRL_DT / phys_dt))
    render_interval = max(1, round((1.0 / 60.0) / phys_dt))

    print("Running rm65_open_cabinet. Press R to reset, ESC to exit.")
    with RenderApp() as render:
        render.launch(model)
        step_index = 0
        while not render.is_closed:
            model.step(data)
            step_index += 1

            if step_index % ctrl_interval == 0:
                if policy.step(data):
                    step_index = 0

            if render.input.is_key_just_pressed("r"):
                data = SceneData(model)
                policy.reset_data(data)
                step_index = 0
            if render.input.is_key_just_pressed("esc"):
                break

            if step_index % render_interval == 0:
                render.sync(data)


if __name__ == "__main__":
    main()
