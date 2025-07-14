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

from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg


class Go1Cfg(LeggedRobotCfg):
    class sim(LeggedRobotCfg.sim):
        dt = 0.004

    class control(LeggedRobotCfg.control):
        action_scale = 0.5
        decimation = 10

    class init_state(LeggedRobotCfg.init_state):
        default_joint_angles = {  # = target angles [rad] when action = 0.0
            "FL_hip_joint": 0.1,  # [rad]
            "RL_hip_joint": 0.1,  # [rad]
            "FR_hip_joint": -0.1,  # [rad]
            "RR_hip_joint": -0.1,  # [rad]
            "FL_thigh_joint": 0.9,  # [rad]
            "RL_thigh_joint": 0.9,  # [rad]
            "FR_thigh_joint": 0.9,  # [rad]
            "RR_thigh_joint": 0.9,  # [rad]
            "FL_calf_joint": -1.8,  # [rad]
            "RL_calf_joint": -1.8,  # [rad]
            "FR_calf_joint": -1.8,  # [rad]
            "RR_calf_joint": -1.8,  # [rad]
        }

    class commands(LeggedRobotCfg.commands):
        class ranges(LeggedRobotCfg.commands.ranges):
            lin_vel_x = [-2, 2]
            lin_vel_y = [-2, 2]
            ang_vel_yaw = [-1, 1]
