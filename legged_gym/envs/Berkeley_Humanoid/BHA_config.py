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

from legged_gym.addr import LEGGED_GYM_ENVS_DIR
from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg


class BHACfg(LeggedRobotCfg):  # policy_biped_50hz
    # control_dt: 0.004
    # policy_dt: 0.02
    class sim(LeggedRobotCfg.sim):
        dt = 0.004

    class env(LeggedRobotCfg.env):
        num_observations = 75
        num_actions = 22

    class control(LeggedRobotCfg.control):
        action_scale = 0.25
        decimation = 5
        stiffness = {"arm": 10, "leg": 20}
        damping = {"arm": 2, "leg": 2}
        torque_limits = 5

    class init_state(LeggedRobotCfg.init_state):
        default_joint_angles = {  # = target angles [rad] when action = 0.0
            "leg_left_hip_roll_joint": 0.0,
            "leg_left_hip_yaw_joint": 0.0,
            "leg_left_hip_pitch_joint": -0.2,
            "leg_left_knee_pitch_joint": 0.4,
            "leg_left_ankle_pitch_joint": -0.3,
            "leg_left_ankle_roll_joint": 0.0,
            "leg_right_hip_roll_joint": 0.0,
            "leg_right_hip_yaw_joint": 0.0,
            "leg_right_hip_pitch_joint": -0.2,
            "leg_right_knee_pitch_joint": 0.4,
            "leg_right_ankle_pitch_joint": -0.3,
            "leg_right_ankle_roll_joint": 0.0,
            "default": 0,
        }

    class asset(LeggedRobotCfg.asset):
        file = LEGGED_GYM_ENVS_DIR + "/resources/robots/BHL/bhl_scene.xml"
        body_name = "base"

    class sensor(LeggedRobotCfg.sensor):
        gyro = "imu_gyro"

    class commands(LeggedRobotCfg.commands):
        class ranges(LeggedRobotCfg.commands.ranges):
            lin_vel_x = [-2.0, 2.0]  # min max [m/s]
            lin_vel_y = [-1.0, 1.0]  # min max [m/s]
            ang_vel_yaw = [-0.5, 0.5]  # min max [rad/s]
            heading = [-3.14, 3.14]
