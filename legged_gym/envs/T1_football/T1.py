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

import numpy as np
from scipy.spatial.transform import Rotation

from legged_gym.envs.base.legged_robot import Legged_Robot
from motrixsim import step
from motrixsim.render import Color


class T1_Football_env(Legged_Robot):
    turn_value: float = 0.0
    forward_value: float = 0.0
    right_value: float = 0.0
    state: str = "walk"
    start: int = 120

    def __init__(self, Cfg):
        self.T = 0
        super().__init__(Cfg)
        self.command_scale = np.array(
            (
                self.config.normalization.obs_scales.lin_vel,
                self.config.normalization.obs_scales.lin_vel,
                self.config.normalization.obs_scales.ang_vel,
            ),
            dtype=np.float16,
        )

        data = np.load(self.config.reference.ref)
        self.frame_id = self.start
        self.num_frames = data["num_frames"]  # 178#178
        self.ref_root_vel = data["root_vel"]
        self.ref_dof_vel = data["dof_vel"]
        self.ref_link_pos = data["link_pos"]
        self.ref_joint_dof = data["joint_dof"]
        self.ref_root_rot_quat = data["root_rot_quat"]
        self.ref_angular_v = data["angular_v"]

        # set gizmos by api
        self._render.gizmos.joint_size = 1.5
        self._render.gizmos.line_width = 5
        self._render.gizmos.collider_color = Color.rgb(0.5, 1, 0.5)
        self._render.gizmos.joint_color = Color.rgb(1, 1, 0.5)

    def buffer_init(self):
        super().buffer_init()
        self.fb = self.body.floatingbase
        self.gait_frequency = 0
        self.gait_process = 0

    def step(self, actions):
        self.actions = actions
        is_kick = self.state == "kick"
        decimation = self.config.control.decimation if not is_kick else self.config.control.decimation1
        for _ in range(decimation):
            self.gait_process = np.fmod(self.gait_process + self.config.sim.dt * self.gait_frequency, 1.0)
            self.torques = self._compute_torques(self.actions)
            self.data.actuator_ctrls = self.torques
            step(self.model, self.data)
        self.post_physics_step()
        self.obs = self.compute_obs()

        if self.state == "kick":
            # change state back to walk after kick motion is done
            if self.frame_id == self.num_frames - 35:
                self.state = "walk"
                self.frame_id = self.start
                self.T = 60
                self.actions = np.zeros(12)
                self.obs = self.compute_obs()

    def kick(self):
        """
        Change state to kick
        Returns:
            bool: whether state changed successfully
        """
        if self.state == "walk" and self.T == 0:
            self.state = "kick"
            self.start_p = self.fb.get_dof_pos(self.data)
            return True
        return False

    def UpdateAction(self, x, y, rot):
        self.turn_value = rot
        self.forward_value = x
        self.right_value = y

    def draw_predict_goal(self):
        start = self.fb.get_dof_pos(self.data)
        R = Rotation.from_quat(start[3:7])
        goal = R.apply(np.array([0.4666305, -0.10587938, 0.0409625]))
        goal = start[:3] + goal
        goal[2] = 0
        self._render.gizmos.draw_sphere(0.1, goal, color=Color.rgb(1, 0, 0))

    def compute_obs(self):
        if self.T > 0:
            self.T = self.T - 1
        is_kick = self.state == "kick"

        if is_kick:
            return self._compute_kick_obs()
        else:
            return self._compute_walk_obs()

    def _compute_walk_obs(self):
        obs = np.zeros(self.config.env.num_observations, dtype=np.float16)
        diff = self.dof_pos - self.default_angles
        obs[:3] = self.gravity * self.config.normalization.gravity
        obs[3:6] = self.gyro * self.config.normalization.obs_scales.lin_vel
        obs[6:9] = self.commands * self.command_scale
        obs[9] = np.cos(2 * np.pi * self.gait_process) * (self.gait_frequency > 1.0e-8)
        obs[10] = np.sin(2 * np.pi * self.gait_process) * (self.gait_frequency > 1.0e-8)
        obs[11:23] = diff[11:] * self.config.normalization.obs_scales.dof_pos
        obs[23:35] = self.dof_vel[11:] * self.config.normalization.obs_scales.dof_vel
        obs[35:47] = self.actions
        return obs

    def _compute_kick_obs(self):
        self.phase = np.float32(self.frame_id / self.num_frames)
        obs = np.zeros(134, dtype=np.float16)
        diff = self.dof_pos - self.default_angles
        ref_diff = self.ref_joint_dof[self.frame_id] - self.default_angles
        obs[:3] = self.linear_vel * 2
        obs[3:6] = self.gyro * 0.25
        obs[6:9] = self.gravity
        obs[9] = self.phase
        obs[10:13] = self.ref_root_vel[self.frame_id] * 2
        obs[13:36] = self.ref_dof_vel[self.frame_id] * 0.05
        obs[36:39] = self.ref_link_pos[self.frame_id, 17, :]
        obs[39:42] = self.ref_link_pos[self.frame_id, 23, :]
        obs[42:65] = ref_diff * 1
        obs[65:88] = diff * 1
        obs[88:111] = self.dof_vel * 0.05
        obs[111:134] = self.actions
        if self.frame_id < self.num_frames - 1:
            self.frame_id = self.frame_id + 1

        return obs

    def _compute_torques(self, actions):
        # Compute torques from actions.
        # pd controller
        is_kick = self.state == "kick"
        if is_kick:
            action_scale = self.config.control.action_scale1
            action = actions * action_scale
        else:
            action_scale = self.config.control.action_scale
            action = np.zeros(self.config.env.num_actions, dtype=np.float16)
            action[11:] = actions * action_scale

        control_type = self.config.control.control_type
        self._sync_dof_data()
        if control_type == "P":
            torques = self.kps * (action + self.default_angles - self.dof_pos) - self.kds * self.dof_vel
        else:
            raise NameError(f"Unknown controller type: {control_type}")
        return np.clip(torques, -self.torque_limits, self.torque_limits)

    def reset_dofs(self):
        for i in range(self.config.env.num_actions):
            self.joints[i].set_dof_pos(self.data, [self.default_angles[i]])

    def env_reset(self):
        self.frame_id = self.start
        self.data.reset(self.model)
        self.reset_dofs()
        self.state = "walk"
        self.actions = np.zeros(12, dtype=np.float16)
        self.model.forward_kinematic(self.data)
        self.compute_obs()

    def _post_physics_step_callback(self):
        x = self.forward_value
        y = self.right_value
        rot = self.turn_value

        v = np.array([x, y])
        norm = v
        target_action = [
            norm[0] * self.config.normalization.obs_scales.lin_vel,
            norm[1] * self.config.normalization.obs_scales.lin_vel,
            rot * self.config.normalization.obs_scales.ang_vel,
        ]
        target_action = np.array(target_action)
        if abs(target_action[0]) < 0.1 and abs(target_action[2]) <= 0.1 and abs(target_action[1]) < 0.1 and self.T == 0:
            self.gait_frequency = 0
        else:
            self.gait_frequency = 1.5
        self.commands = target_action
