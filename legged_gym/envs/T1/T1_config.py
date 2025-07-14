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


class T1Cfg(LeggedRobotCfg):
    class sim(LeggedRobotCfg.sim):
        dt = 0.002

    class env(LeggedRobotCfg.env):
        num_observations = 47

    class init_state(LeggedRobotCfg.init_state):
        default_joint_angles = {
            "Left_Hip_Pitch": -0.2,
            "Right_Hip_Pitch": -0.2,
            "Left_Knee_Pitch": 0.4,
            "Right_Knee_Pitch": 0.4,
            "Left_Ankle_Pitch": -0.25,
            "Right_Ankle_Pitch": -0.25,
            "default": 0.0,
        }

    class control(LeggedRobotCfg.control):
        stiffness = {
            "Left_Hip_Pitch": 200.0,
            "Right_Hip_Pitch": 200.0,
            "Left_Hip_Roll": 200.0,
            "Right_Hip_Roll": 200.0,
            "Left_Hip_Yaw": 200.0,
            "Right_Hip_Yaw": 200.0,
            "Left_Knee_Pitch": 200.0,
            "Right_Knee_Pitch": 200.0,
            "Left_Ankle_Pitch": 50.0,
            "Right_Ankle_Pitch": 50.0,
            "Left_Ankle_Roll": 50.0,
            "Right_Ankle_Roll": 50.0,
        }  # [N*m/rad]
        damping = {
            "Left_Hip_Pitch": 5.0,
            "Right_Hip_Pitch": 5.0,
            "Left_Hip_Roll": 5.0,
            "Right_Hip_Roll": 5.0,
            "Left_Hip_Yaw": 5.0,
            "Right_Hip_Yaw": 5.0,
            "Left_Knee_Pitch": 5.0,
            "Right_Knee_Pitch": 5.0,
            "Left_Ankle_Pitch": 1.0,
            "Right_Ankle_Pitch": 1.0,
            "Left_Ankle_Roll": 1.0,
            "Right_Ankle_Roll": 1.0,
        }  # [N*m*s/rad]
        action_scale = 1.0
        decimation = 10

    class normalization(LeggedRobotCfg.normalization):
        gravity = 1

        class obs_scales(LeggedRobotCfg.normalization.obs_scales):
            dof_vel = 0.1

    class asset(LeggedRobotCfg.asset):
        file = LEGGED_GYM_ENVS_DIR + "/resources/robots/T1/T1_locomotion.xml"
        body_name = "Trunk"

    class commands(LeggedRobotCfg.commands):
        class ranges(LeggedRobotCfg.commands.ranges):
            lin_vel_x = [-0.5, 0.5]  # min max [m/s]
            lin_vel_y = [-0.5, 0.5]  # min max [m/s]
            ang_vel_yaw = [-0.2, 0.2]  # min max [rad/s]
            heading = [-3.14, 3.14]
