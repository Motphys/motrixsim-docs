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


class G1Cfg(LeggedRobotCfg):
    class sim(LeggedRobotCfg.sim):
        dt = 0.005

    class env(LeggedRobotCfg.env):
        num_envs = 1
        num_observations = 47
        space = 0

    class control(LeggedRobotCfg.control):
        action_scale = 0.25
        torque_limits = 139
        decimation = 4
        stiffness = {
            "left_hip_yaw_joint": 100,
            "left_hip_roll_joint": 100,
            "left_hip_pitch_joint": 100,
            "left_knee_joint": 150,
            "left_ankle_pitch_joint": 40,
            "left_ankle_roll_joint": 40,
            "right_hip_yaw_joint": 100,
            "right_hip_roll_joint": 100,
            "right_hip_pitch_joint": 100,
            "right_knee_joint": 150,
            "right_ankle_pitch_joint": 40,
            "right_ankle_roll_joint": 40,
        }  # [N*m/rad]
        damping = {
            "left_hip_yaw_joint": 2,
            "left_hip_roll_joint": 2,
            "left_hip_pitch_joint": 2,
            "left_knee_joint": 4,
            "left_ankle_pitch_joint": 2,
            "left_ankle_roll_joint": 2,
            "right_hip_yaw_joint": 2,
            "right_hip_roll_joint": 2,
            "right_hip_pitch_joint": 2,
            "right_knee_joint": 4,
            "right_ankle_pitch_joint": 2,
            "right_ankle_roll_joint": 2,
        }  # [N*m/rad]  # [N*m*s/rad]

    class init_state(LeggedRobotCfg.init_state):
        default_joint_angles = {  # = target angles [rad] when action = 0.0
            "left_hip_yaw_joint": 0.0,
            "left_hip_roll_joint": 0,
            "left_hip_pitch_joint": -0.1,
            "left_knee_joint": 0.3,
            "left_ankle_pitch_joint": -0.2,
            "left_ankle_roll_joint": 0,
            "right_hip_yaw_joint": 0.0,
            "right_hip_roll_joint": 0,
            "right_hip_pitch_joint": -0.1,
            "right_knee_joint": 0.3,
            "right_ankle_pitch_joint": -0.2,
            "right_ankle_roll_joint": 0,
            "torso_joint": 0.0,
        }

    class commands(LeggedRobotCfg.commands):
        class ranges(LeggedRobotCfg.commands.ranges):
            lin_vel_x = [-0, 1]
            lin_vel_y = [-0.5, 0.5]
            ang_vel_yaw = [-1, 1]

    class normalization(LeggedRobotCfg.normalization):
        class obs_scales(LeggedRobotCfg.normalization.obs_scales):
            lin_vel = 2.0
            ang_vel = 0.25
            dof_pos = 1.0
            dof_vel = 0.05
            height_measurements = 5.0

    class sensor(LeggedRobotCfg.sensor):
        local_linvel = "local_linvel"
        gyro = "gyro"

    class asset(LeggedRobotCfg.asset):
        file = LEGGED_GYM_ENVS_DIR + "/resources/robots/G1/G1_scene.xml"
        foot_name = "foot"
        penalize_contacts_on = []
        terminate_after_contacts_on = [
            "pelvis",
        ]
        ground = "floor"
        body_name = "pelvis"
