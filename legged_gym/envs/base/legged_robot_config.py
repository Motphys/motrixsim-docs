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


class LeggedRobotCfg:
    class sim:
        max_episode_length = 1000
        dt = 0.004

    class env:
        num_observations = 48
        num_actions = 12

    class init_state:
        # the initial position of the robot in the world frame
        pos = [0.0, 0.0, 0.42]

        # the default angles for all joints. key = joint name, value = target angle [rad]
        default_joint_angles = {
            "FL_hip": 0.1,
            "RL_hip": 0.1,
            "FR_hip": -0.1,
            "RR_hip": -0.1,
            "FL_thigh": 0.8,
            "RL_thigh": 1.0,
            "FR_thigh": 0.8,
            "RR_thigh": 1.0,
            "FL_calf": -1.5,
            "RL_calf": -1.5,
            "FR_calf": -1.5,
            "RR_calf": -1.5,
        }

    class commands:
        resampling_interval = 200  # dt

        class ranges:
            lin_vel_x = [-1.0, 1.0]  # min max [m/s]
            lin_vel_y = [-1.0, 1.0]  # min max [m/s]
            ang_vel_yaw = [-1, 1]  # min max [rad/s]
            heading = [-3.14, 3.14]

    class control:
        # PD Drive parameters:
        control_type = "P"
        stiffness = 35  # [N*m/rad]
        damping = 0  # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.25
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4
        torque_limits = 23.7

    class asset:
        file = LEGGED_GYM_ENVS_DIR + "/resources/robots/go1/scene.xml"
        body_name = "trunk"

    class normalization:
        class obs_scales:
            lin_vel = 1.0
            ang_vel = 1.0
            dof_pos = 1.0
            dof_vel = 1.0

    class sensor:
        local_linvel = "local_linvel"
        gyro = "gyro"
