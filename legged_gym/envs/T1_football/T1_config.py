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

from legged_gym.addr import LEGGED_GYM_ENVS_DIR
from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg


class T1FootballCfg(LeggedRobotCfg):
    class sim(LeggedRobotCfg.sim):
        max_episode_length = 50000
        dt = 0.005
        # dt = 0.005

    class env(LeggedRobotCfg.env):
        num_observations = 47
        num_actions = 23

    class init_state(LeggedRobotCfg.init_state):
        default_joint_angles = {
            "AAHead_yaw": 0,
            "Head_pitch": 0,
            "Left_Shoulder_Pitch": 0,
            "Left_Shoulder_Roll": -1.2,
            "Left_Elbow_Pitch": 0,
            "Left_Elbow_Yaw": -0.6,
            "Right_Shoulder_Pitch": 0,
            "Right_Shoulder_Roll": 1.2,
            "Right_Elbow_Pitch": 0,
            "Right_Elbow_Yaw": 0.6,
            "Waist": 0.0,
            "Left_Hip_Pitch": -0.2,
            "Right_Hip_Pitch": -0.2,
            "Left_Knee_Pitch": 0.4,
            "Right_Knee_Pitch": 0.4,
            "Left_Ankle_Pitch": -0.25,
            "Right_Ankle_Pitch": -0.25,
            # "Left_Ankle_Roll": -0.25,
            # "Right_Ankle_Roll": -0.25,
            "default": 0.0,
        }

    class control(LeggedRobotCfg.control):
        stiffness = {
            # 'Shoulder': 50,
            # 'Elbow': 50,
            # 'Waist': 200,
            # 'Head': 50,
            "AAHead_yaw": 50,
            "Head_pitch": 50,
            "Left_Shoulder_Pitch": 50,
            "Left_Shoulder_Roll": 50,
            "Left_Elbow_Pitch": 50,
            "Left_Elbow_Yaw": 50,
            "Right_Shoulder_Pitch": 50,
            "Right_Shoulder_Roll": 50,
            "Right_Elbow_Pitch": 50,
            "Right_Elbow_Yaw": 50,
            "Waist": 200,
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
            # 'Shoulder': 1.0,
            # 'Elbow': 1.0,
            # 'Waist': 5.0,
            # 'Head': 1.0,
            "AAHead_yaw": 1.0,
            "Head_pitch": 1.0,
            "Left_Shoulder_Pitch": 1.0,
            "Left_Shoulder_Roll": 1.0,
            "Left_Elbow_Pitch": 1.0,
            "Left_Elbow_Yaw": 1.0,
            "Right_Shoulder_Pitch": 1.0,
            "Right_Shoulder_Roll": 1.0,
            "Right_Elbow_Pitch": 1.0,
            "Right_Elbow_Yaw": 1.0,
            "Waist": 5.0,
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
        decimation = 4
        action_scale1 = 0.25
        decimation1 = 7
        torque_limits = 100

    class reference:
        ref = LEGGED_GYM_ENVS_DIR + "/ref/tensor_dict1.npz"

    class normalization(LeggedRobotCfg.normalization):
        gravity = 1

        class obs_scales(LeggedRobotCfg.normalization.obs_scales):
            dof_vel = 0.1

    class asset(LeggedRobotCfg.asset):
        file = LEGGED_GYM_ENVS_DIR + "/resources/robots/T1_football/T1_football.xml"
        body_name = "Trunk"

    class commands(LeggedRobotCfg.commands):
        class ranges(LeggedRobotCfg.commands.ranges):
            lin_vel_x = [-0.5, 0.5]  # min max [m/s]
            lin_vel_y = [-0.5, 0.5]  # min max [m/s]
            ang_vel_yaw = [-0.2, 0.2]  # min max [rad/s]
            heading = [-3.14, 3.14]
