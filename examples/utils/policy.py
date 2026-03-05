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

from typing import TYPE_CHECKING

import numpy as np
import onnxruntime as ort
from scipy.spatial.transform import Rotation

from motrixsim import SceneData

if TYPE_CHECKING:
    from utils.robot import G1Robot, Go1Robot, Go2Robot


class Go2LocomotionPolicy:
    """Go2 robot locomotion control policy (with integrated ONNX inference).

    Note:
        Integrates observation computation, ONNX model inference, action application,
        and fall detection. Initialized directly via ONNX model file path.

        Policy-specific configuration:
        - default_angles: Default joint positions
        - action_scale: Action scaling factor
        - last_action: Last applied action
    """

    # Default joint positions (12D: FL, FR, RL, RR legs, 3 joints per leg)
    _DEFAULT_ANGLES = np.array([0.1, 0.9, -1.8, -0.1, 0.9, -1.8, 0.1, 0.9, -1.8, -0.1, 0.9, -1.8])
    onnx_path = "examples/assets/go2/go2_policy.onnx"

    def __init__(
        self,
        robot: "Go2Robot",
        action_scale: float = 0.5,
        lin_vel_scale: float = 1.0,
        ang_vel_scale: float = 1.5,
    ):
        """Initialize locomotion control policy (with ONNX inference).

        Args:
            robot: Go2 robot state accessor
            default_angles: Default joint positions (12D), uses built-in defaults if None
            action_scale: Action scaling factor, default 0.5
            lin_vel_scale: Linear velocity scaling factor, default 2.0
            ang_vel_scale: Angular velocity scaling factor, default 3.0
        """
        self._robot = robot

        # Use provided default_angles or built-in defaults
        self.default_angles = self._DEFAULT_ANGLES.copy()
        self.action_scale = action_scale
        self.lin_vel_scale = lin_vel_scale
        self.ang_vel_scale = ang_vel_scale
        self.last_action = np.zeros_like(self.default_angles, dtype=np.float32)

        # Initialize ONNX inference session
        self._policy_session = ort.InferenceSession(Go2LocomotionPolicy.onnx_path, providers=["CPUExecutionProvider"])
        self._input_name = self._policy_session.get_inputs()[0].name
        self._output_name = self._policy_session.get_outputs()[0].name

    def scale_command(self, raw_command: np.ndarray) -> np.ndarray:
        """Apply velocity scaling to raw keyboard commands.

        Args:
            raw_command: Raw command vector [x, y, yaw], value range [-1, 1]

        Returns:
            Scaled command vector [x_vel, y_vel, yaw_vel]
        """
        scales = np.array([self.lin_vel_scale, self.lin_vel_scale, self.ang_vel_scale])
        return raw_command * scales

    def get_observation(self, data: SceneData, command: np.ndarray) -> np.ndarray:
        """Compute the observation vector.

        Note:
            Observation vector composition (48D):
            - [0:3] local_linear_vel
            - [3:6] gyro
            - [6:9] gravity
            - [9:21] dof_pos - default_angles
            - [21:33] dof_vel
            - [33:45] last_action
            - [45:48] command

        Args:
            data: Scene simulation data
            command: Command vector [x_vel, y_vel, yaw_vel]

        Returns:
            48D observation vector
        """
        # Get state from robot
        lin_vel = self._robot.local_linear_vel(data)
        gyro = self._robot.gyro(data)
        gravity = self._robot.gravity(data)
        dof_pos = self._robot.dof_pos(data)
        dof_vel = self._robot.dof_vel(data)

        # Combine observation vector
        obs = np.hstack(
            [
                lin_vel,
                gyro,
                gravity,
                dof_pos - self.default_angles,
                dof_vel,
                self.last_action,
                command,
            ]
        )
        return obs.astype(np.float32)

    def compute_action(self, observation: np.ndarray) -> np.ndarray:
        """Compute action from observation vector (ONNX inference).

        Args:
            observation: Observation vector (48D)

        Returns:
            12D action vector
        """
        outputs = self._policy_session.run([self._output_name], {self._input_name: observation.reshape(1, -1)})
        return outputs[0][0]

    def step(self, data: SceneData, command: np.ndarray) -> bool:
        """Execute one control step: observe -> infer -> apply.

        Note:
            Convenience method that encapsulates the complete control flow:
            1. Compute observation vector
            2. ONNX model inference to get action
            3. Apply action to actuators

        Args:
            data: Scene simulation data
            command: Command vector [x_vel, y_vel, yaw_vel]

        Returns:
            True if robot has fallen, False otherwise
        """
        command = self.scale_command(command)
        obs = self.get_observation(data, command)
        action = self.compute_action(obs)
        self.apply_action(data, action)
        return self.is_fallen(data)

    def apply_action(self, data: SceneData, action: np.ndarray) -> None:
        """Apply action to actuators.

        Note:
            Control signal calculation: action * action_scale + default_angle

        Args:
            data: Scene simulation data
            action: 12D action vector
        """

        ctrl = action * self.action_scale + self.default_angles
        self._robot.set_actuator_ctrls(data, ctrl)
        self.last_action = action.copy()

    def is_fallen(self, data: SceneData) -> bool:
        """Detect whether the robot has fallen.

        Note:
            Determined by base pose: when the dot product of the base z-axis
            and world z-axis is less than threshold (0.3), the robot is
            considered fallen.

        Args:
            data: Scene simulation data

        Returns:
            True if fallen, False otherwise
        """
        pose = self._robot.base_pose(data)
        rotation = Rotation.from_quat(pose[3:7])
        rotated_z_axis = rotation.apply(np.array([0.0, 0.0, 1.0]))

        thr = 0.3
        dot = np.dot(rotated_z_axis, np.array([0.0, 0.0, 1.0]))
        return dot < thr


class Go1LocomotionPolicy:
    """Go1 robot locomotion control policy (with integrated ONNX inference).

    Note:
        Integrates observation computation, ONNX model inference, action application,
        and fall detection. Initialized directly via ONNX model file path.

        Policy-specific configuration:
        - default_angles: Default joint positions (same as Go2)
        - action_scale: Action scaling factor (0.5)
        - onnx_model_path: ONNX model file path
        - last_action: Last applied action

        Key differences from Go2:
        - lin_vel_scale: 0.7 (vs 2.0 for Go2)
        - ang_vel_scale: 1.5 (vs 3.0 for Go2)
    """

    # Default joint positions (12D: FL, FR, RL, RR legs, 3 joints per leg)
    _DEFAULT_ANGLES = np.array([0.1, 0.9, -1.8, -0.1, 0.9, -1.8, 0.1, 0.9, -1.8, -0.1, 0.9, -1.8])
    onnx_path = "examples/assets/go1/go1_policy.onnx"

    def __init__(
        self,
        robot: "Go1Robot",
        action_scale: float = 0.5,
        lin_vel_scale: float = 0.7,
        ang_vel_scale: float = 1.5,
    ):
        """Initialize locomotion control policy (with ONNX inference).

        Args:
            robot: Go1 robot state accessor
            onnx_model_path: ONNX model file path
            default_angles: Default joint positions (12D), uses built-in defaults if None
            action_scale: Action scaling factor, default 0.5
            lin_vel_scale: Linear velocity scaling factor, default 0.7
            ang_vel_scale: Angular velocity scaling factor, default 1.5
        """
        self._robot = robot

        self.default_angles = self._DEFAULT_ANGLES.copy()

        self.action_scale = action_scale
        self.lin_vel_scale = lin_vel_scale
        self.ang_vel_scale = ang_vel_scale
        self.last_action = np.zeros_like(self.default_angles, dtype=np.float32)

        # Initialize ONNX inference session
        self._policy_session = ort.InferenceSession(Go1LocomotionPolicy.onnx_path, providers=["CPUExecutionProvider"])
        self._input_name = self._policy_session.get_inputs()[0].name
        self._output_name = self._policy_session.get_outputs()[0].name

    def scale_command(self, raw_command: np.ndarray) -> np.ndarray:
        """Apply velocity scaling to raw commands.

        Args:
            raw_command: Raw command vector [x, y, yaw], value range [-1, 1]

        Returns:
            Scaled command vector [x_vel, y_vel, yaw_vel]
        """
        scales = np.array([self.lin_vel_scale, self.lin_vel_scale, self.ang_vel_scale])
        return raw_command * scales

    def get_observation(self, data: SceneData, command: np.ndarray) -> np.ndarray:
        """Compute the observation vector.

        Note:
            Observation vector composition (48D):
            - [0:3] local_linear_vel
            - [3:6] gyro
            - [6:9] gravity
            - [9:21] dof_pos - default_angles
            - [21:33] dof_vel
            - [33:45] last_action
            - [45:48] command

        Args:
            data: Scene simulation data
            command: Command vector [x_vel, y_vel, yaw_vel]

        Returns:
            48D observation vector
        """
        # Get state from robot
        lin_vel = self._robot.local_linear_vel(data)
        gyro = self._robot.gyro(data)
        gravity = self._robot.gravity(data)
        dof_pos = self._robot.dof_pos(data)
        dof_vel = self._robot.dof_vel(data)

        # Combine observation vector
        obs = np.hstack(
            [
                lin_vel,
                gyro,
                gravity,
                dof_pos - self.default_angles,
                dof_vel,
                self.last_action,
                command,
            ]
        )
        return obs.astype(np.float32)

    def compute_action(self, observation: np.ndarray) -> np.ndarray:
        """Compute action from observation vector (ONNX inference).

        Args:
            observation: Observation vector (48D)

        Returns:
            12D action vector
        """
        outputs = self._policy_session.run([self._output_name], {self._input_name: observation.reshape(1, -1)})
        return outputs[0][0]

    def step(self, data: SceneData, command: np.ndarray) -> bool:
        """Execute one control step: observe -> infer -> apply.

        Note:
            Convenience method that encapsulates the complete control flow:
            1. Compute observation vector
            2. ONNX model inference to get action
            3. Apply action to actuators

        Args:
            data: Scene simulation data
            command: Command vector [x_vel, y_vel, yaw_vel]

        Returns:
            True if robot has fallen, False otherwise
        """
        command = self.scale_command(command)
        obs = self.get_observation(data, command)
        action = self.compute_action(obs)
        self.apply_action(data, action)
        return self.is_fallen(data)

    def apply_action(self, data: SceneData, action: np.ndarray) -> None:
        """Apply action to actuators.

        Note:
            Control signal calculation: action * action_scale + default_angle

        Args:
            data: Scene simulation data
            action: 12D action vector
        """

        ctrl = action * self.action_scale + self.default_angles
        self._robot.set_actuator_ctrls(data, ctrl)
        self.last_action = action.copy()

    def is_fallen(self, data: SceneData) -> bool:
        """Detect whether the robot has fallen.

        Note:
            Determined by base pose: when the dot product of the base z-axis
            and world z-axis is less than threshold (0.3), the robot is
            considered fallen.

        Args:
            data: Scene simulation data

        Returns:
            True if fallen, False otherwise
        """
        pose = self._robot.base_pose(data)
        rotation = Rotation.from_quat(pose[3:7])
        rotated_z_axis = rotation.apply(np.array([0.0, 0.0, 1.0]))

        thr = 0.3
        dot = np.dot(rotated_z_axis, np.array([0.0, 0.0, 1.0]))
        return dot < thr


class G1LocomotionPolicy:
    """G1 robot locomotion control policy (with integrated ONNX inference).

    Note:
        Integrates observation computation, ONNX model inference, action application,
        and fall detection. Initialized directly via ONNX model file path.

        Policy-specific configuration:
        - default_angles: Default joint positions (27D for G1)
        - action_scale: Action scaling factor (0.5)
        - onnx_model_path: ONNX model file path
        - last_action: Last applied action

        Key differences from Go1/Go2:
        - DoF: 27 (vs 12)
        - lin_vel_scale: 1.0 (vs 0.7 for Go1, 2.0 for Go2)
        - ang_vel_scale: 1.0 (vs 1.5 for Go1, 3.0 for Go2)
    """

    _DEFAULT_ANGLES = np.array(
        [
            -0.312,
            0,
            0,
            0.669,
            -0.363,
            0,  # left leg
            -0.312,
            0,
            0,
            0.669,
            -0.363,
            0,  # right leg
            0,
            0,
            0.073,  # waist
            0.2,
            0.2,
            0,
            0.6,
            0,
            0,
            0,  # left arm
            0.2,
            -0.2,
            0,
            0.6,
            0,
            0,
            0,  # right arm
        ]
    )
    onnx_path = "examples/assets/g1/g1_policy.onnx"

    def __init__(
        self,
        robot: "G1Robot",
        action_scale: float = 0.5,
        lin_vel_scale: float = 1.0,
        ang_vel_scale: float = 1.0,
        ctrl_dt: float = 0.02,
    ):
        """Initialize locomotion control policy (with ONNX inference).

        Args:
            robot: G1 robot state accessor
            onnx_model_path: ONNX model file path
            default_angles: Default joint positions (27D), uses built-in defaults if None
            action_scale: Action scaling factor, default 0.5
            lin_vel_scale: Linear velocity scaling factor, default 1.0
            ang_vel_scale: Angular velocity scaling factor, default 1.0
            ctrl_dt: Control timestep for phase updates, default 0.02
        """
        self._robot = robot
        self.default_angles = robot._DEFAULT_ANGLES.copy()
        self.action_scale = action_scale
        self.lin_vel_scale = lin_vel_scale
        self.ang_vel_scale = ang_vel_scale
        self.last_action = np.zeros_like(self.default_angles, dtype=np.float32)
        self.ctrl_dt = ctrl_dt

        # Initialize gait phase
        self._phase = np.array([0.0, np.pi])
        self._gait_freq = 1.5

        # Initialize ONNX inference session
        self._policy_session = ort.InferenceSession(G1LocomotionPolicy.onnx_path, providers=["CPUExecutionProvider"])
        self._input_name = self._policy_session.get_inputs()[0].name
        self._output_name = self._policy_session.get_outputs()[0].name

    def scale_command(self, raw_command: np.ndarray) -> np.ndarray:
        """Apply velocity scaling to raw commands.

        Args:
            raw_command: Raw command vector [x, y, yaw], value range [-1, 1]

        Returns:
            Scaled command vector [x_vel, y_vel, yaw_vel]
        """
        scales = np.array([self.lin_vel_scale, self.lin_vel_scale, self.ang_vel_scale])
        return raw_command * scales

    def get_observation(self, data: SceneData, command: np.ndarray) -> np.ndarray:
        """Compute the observation vector.

        Note:
            Observation vector composition (G1-specific):
            - [0:3] local_linear_vel
            - [3:6] gyro
            - [6:9] gravity
            - [9:12] command
            - [12:39] dof_pos - default_angles (27D)
            - [39:66] dof_vel (27D)
            - [66:93] last_action (27D)
            - [93:95] phase (2D: cos, sin)

        Args:
            data: Scene simulation data
            command: Command vector [x_vel, y_vel, yaw_vel]

        Returns:
            Observation vector for policy input
        """
        # Get state from robot
        lin_vel = self._robot.local_linear_vel(data)
        gyro = self._robot.gyro(data)
        gravity = self._robot.gravity(data)
        dof_pos = self._robot.dof_pos(data)
        dof_vel = self._robot.dof_vel(data)
        phase = self.get_phase()

        # Combine observation vector (structure matches G1 policy)
        obs = np.hstack(
            [
                lin_vel,
                gyro,
                gravity,
                command,
                dof_pos - self.default_angles,
                dof_vel,
                self.last_action,
                phase,
            ]
        )
        return obs.astype(np.float32)

    def compute_action(self, observation: np.ndarray) -> np.ndarray:
        """Compute action from observation vector (ONNX inference).

        Args:
            observation: Observation vector

        Returns:
            Action vector (27D for G1)
        """
        outputs = self._policy_session.run([self._output_name], {self._input_name: observation.reshape(1, -1)})
        return outputs[0][0]

    def step(self, data: SceneData, command: np.ndarray) -> bool:
        """Execute one control step: observe -> infer -> apply.

        Note:
            Convenience method that encapsulates the complete control flow:
            1. Compute observation vector
            2. ONNX model inference to get action
            3. Apply action to actuators
            4. Update gait phase

        Args:
            data: Scene simulation data
            command: Command vector [x_vel, y_vel, yaw_vel]

        Returns:
            True if robot has fallen, False otherwise
        """
        # Scale command
        scaled_command = self.scale_command(command)

        # Get observation and compute action
        obs = self.get_observation(data, scaled_command)
        action = self.compute_action(obs)

        # Apply action
        self.apply_action(data, action)

        # Update phase
        self.update_phase(self.ctrl_dt)

        # Check if fallen
        return self.is_fallen(data)

    def apply_action(self, data: SceneData, action: np.ndarray) -> None:
        """Apply action to actuators.

        Note:
            Control signal calculation: action * action_scale + default_angle

        Args:
            data: Scene simulation data
            action: Action vector (27D for G1)
        """

        ctrl = action * self.action_scale + self.default_angles
        self._robot.set_actuator_ctrls(data, ctrl)
        self.last_action = action.copy()

    def get_phase(self) -> np.ndarray:
        """Get the current gait phase.

        Returns:
            2D phase vector [cos(phase), sin(phase)]
        """
        return np.concatenate([np.cos(self._phase), np.sin(self._phase)])

    def update_phase(self, dt: float) -> None:
        """Update the gait phase.

        Args:
            dt: Time step for phase update
        """
        phase_dt = 2 * np.pi * self._gait_freq * dt
        phase_tp1 = self._phase + phase_dt
        self._phase = np.fmod(phase_tp1 + np.pi, 2 * np.pi) - np.pi

    def is_fallen(self, data: SceneData) -> bool:
        """Detect whether the robot has fallen.

        Note:
            Determined by base pose: when the dot product of the base z-axis
            and world z-axis is less than threshold (0.3), the robot is
            considered fallen.

        Args:
            data: Scene simulation data

        Returns:
            True if fallen, False otherwise
        """
        pose = self._robot.base_pose(data)
        rotation = Rotation.from_quat(pose[3:7])
        rotated_z_axis = rotation.apply(np.array([0.0, 0.0, 1.0]))

        thr = 0.3
        dot = np.dot(rotated_z_axis, np.array([0.0, 0.0, 1.0]))
        return dot < thr
