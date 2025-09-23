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

from legged_gym.envs.base.legged_robot import Legged_Robot
from motrixsim import step


class Go1_env(Legged_Robot):
    def compute_obs(self):
        obs = np.zeros(self.config.env.num_observations, dtype=np.float16)
        diff = self.dof_pos - self.default_angles
        obs[:3] = self.linear_vel * self.config.normalization.obs_scales.lin_vel
        obs[3:6] = self.gyro * self.config.normalization.obs_scales.ang_vel
        obs[6:9] = self.gravity
        obs[9:21] = diff
        obs[21:33] = self.dof_vel
        obs[33:45] = self.last_actions
        obs[45:48] = self.commands
        self.last_actions = self.actions
        return obs

    def step(self, actions):
        # Apply actuations, simulate, call self.post_physics_step()

        self.actions = actions
        for _ in range(self.config.control.decimation):
            self.torques = self._compute_torques(self.actions)
            self.e_angle = self.dof_estimate()
            self.data.actuator_ctrls = self.torques
            step(self.model, self.data)

        self.post_physics_step()
        self.obs = self.compute_obs()

    def env_reset(self):
        super().env_reset()

    def dof_estimate(self):  ####分析传递函数
        k = 2
        actions_scaled = self.actions * self.config.control.action_scale
        d_angle = k * (actions_scaled - self.dof_pos) * self.config.sim.dt
        estimate_angle = self.dof_pos + d_angle
        return estimate_angle
