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


import numpy as np

import motrixsim as mx
from motrixsim import Body, SceneData


class RobotBase:
    def __init__(self, body: Body):
        """Init the robot

        Args:
            body: The motrixsim.Body of the robot
        """
        self._body = body
        self._model = body.model
        self._base_link = body.base_link

    @property
    def body(self) -> Body:
        """The body object of the robot."""
        return self._body

    @property
    def model(self) -> mx.SceneModel:
        """The scene model of the robot."""
        return self._model

    @property
    def base_link(self) -> mx.Link:
        """The base link of the robot."""
        return self._base_link

    @property
    def num_actuators(self) -> int:
        """The number of actuators of the robot."""
        return self._body.num_actuators

    def dof_pos(self, data: SceneData) -> np.ndarray:
        """Get the joint positions.

        Args:
            data: The SceneData of the simulation

        Returns:
            The joint positions as a numpy array
        """
        return self._body.get_joint_dof_pos(data)

    def dof_vel(self, data: SceneData) -> np.ndarray:
        """Get the joint velocities.

        Args:
            data: The SceneData of the simulation

        Returns:
            The joint velocities as a numpy array
        """
        return self._body.get_joint_dof_vel(data)

    def base_pose(self, data: SceneData) -> np.ndarray:
        """Get the global pose of the base link.

        Args:
            data: The SceneData of the simulation

        Returns:
            A 7D pose vector [x, y, z, qx, qy, qz, qw]
        """
        return self._base_link.get_pose(data)

    def set_actuator_ctrls(self, data: SceneData, ctrls: np.ndarray) -> None:
        """Set all actuator control signals at once.

        Args:
            data: Scene simulation data
            ctrls: Numpy array of control signal values for all actuators.
        """
        self._body.set_actuator_ctrls(data, ctrls)

    def gravity(self, data: SceneData) -> np.ndarray:
        """Get the gravity vector in the body coordinate system.

        Args:
            data: Scene simulation data

        Returns:
            3D gravity vector [gx, gy, gz]
        """
        rot = self._body.get_rotation_mat(data)
        return rot.T @ np.array([0.0, 0.0, -1.0])


class Go2Robot(RobotBase):
    """Go2 robot state accessor.

    Note:
        Provides a unified interface for accessing robot state, including sensor data,
        joint state, and base state. Also provides actuator control interface.

        This class does not contain any control policy logic. All policy-related
        behavior should be implemented by Go2LocomotionPolicy or other Policy classes.
    """

    mjcf_path = "examples/assets/go2/go2_mjx.xml"
    base_link_name = "base"

    def __init__(self, body: Body):
        """Initialize Go2 robot state accessor.

        Args:
            body: The Body object of the robot (typically obtained from model.get_body("base"))
        """
        super().__init__(body)

    # === Sensor Data ===

    def local_linear_vel(self, data: SceneData) -> np.ndarray:
        """Get the linear velocity in the local coordinate system.

        Args:
            data: Scene simulation data

        Returns:
            3D linear velocity vector [vx, vy, vz]
        """
        return self._model.get_sensor_value("local_linvel", data)

    def gyro(self, data: SceneData) -> np.ndarray:
        """Get the gyroscope angular velocity.

        Args:
            data: Scene simulation data

        Returns:
            3D angular velocity vector [wx, wy, wz]
        """
        return self._model.get_sensor_value("gyro", data)


class Go1Robot(RobotBase):
    """Go1 robot state accessor.

    Note:
        Provides a unified interface for accessing robot state, including sensor data,
        joint state, and base state. Also provides actuator control interface.

        This class does not contain any control policy logic. All policy-related
        behavior should be implemented by Go1LocomotionPolicy or other Policy classes.

    """

    mjcf_path = "examples/assets/go1/go1_mjx_fullcollisions.xml"
    base_link_name = "trunk"

    def __init__(self, body: Body):
        """Initialize Go1 robot state accessor.

        Args:
            body: The Body object of the robot (typically obtained from model.get_body("trunk"))
        """
        super().__init__(body)

    # === Sensor Data ===

    def local_linear_vel(self, data: SceneData) -> np.ndarray:
        """Get the linear velocity in the local coordinate system.

        Args:
            data: Scene simulation data

        Returns:
            3D linear velocity vector [vx, vy, vz]
        """
        return self._model.get_sensor_value("local_linvel", data)

    def gyro(self, data: SceneData) -> np.ndarray:
        """Get the gyroscope angular velocity.

        Args:
            data: Scene simulation data

        Returns:
            3D angular velocity vector [wx, wy, wz]
        """
        return self._model.get_sensor_value("gyro", data)


class G1Robot(RobotBase):
    """G1 robot state accessor.

    Note:
        G1 is a humanoid robot with 29 degrees of freedom including:
        - 12 DoF for legs (6 per leg)
        - 3 DoF for waist (yaw, pitch, roll)
        - 14 DoF for arms (7 per arm)
        - Plus articulated fingers (additional DoF not in default positions)

        Provides a unified interface for accessing robot state, including sensor data,
        joint state, and base state. Also provides actuator control interface.

        This class does not contain any control policy logic. All policy-related
        behavior should be implemented by G1LocomotionPolicy or other Policy classes.

        Key differences from Go1/Go2:
        - Robot type: Humanoid (vs quadruped)
        - Base link name: "pelvis" (vs "trunk"/"base")
        - DoF: 27 (vs 12)
        - Has upper body with waist and arms
    """

    mjcf_path = "examples/assets/g1/g1.xml"
    base_link_name = "pelvis"

    # Default joint positions (29D: legs(12) + waist(3) + arms(14))
    _DEFAULT_ANGLES = np.array(
        [
            # Left leg (6)
            -0.312,
            0,
            0,
            0.669,
            -0.363,
            0,
            # Right leg (6)
            -0.312,
            0,
            0,
            0.669,
            -0.363,
            0,
            # Waist (3)
            0,
            0,
            0.073,
            # Left arm (7) - shoulder(3) + elbow(1) + wrist(3)
            0.2,
            0.2,
            0,
            0.6,
            0,
            0,
            0,
            # Right arm (7) - shoulder(3) + elbow(1) + wrist(3)
            0.2,
            -0.2,
            0,
            0.6,
            0,
            0,
            0,
        ]
    )

    def __init__(self, body: Body):
        """Initialize G1 robot state accessor.

        Args:
            body: The Body object of the robot (typically obtained from model.get_body("pelvis"))
        """
        super().__init__(body)

    # === Sensor Data ===

    def local_linear_vel(self, data: SceneData) -> np.ndarray:
        """Get the linear velocity in the local coordinate system.

        Args:
            data: Scene simulation data

        Returns:
            3D linear velocity vector [vx, vy, vz]
        """
        return self._model.get_sensor_value("local_linvel_pelvis", data)

    def gyro(self, data: SceneData) -> np.ndarray:
        """Get the gyroscope angular velocity.

        Args:
            data: Scene simulation data

        Returns:
            3D angular velocity vector [wx, wy, wz]
        """
        return self._model.get_sensor_value("gyro_pelvis", data)
