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


class T1_env(Legged_Robot):
    def __init__(self, Cfg):
        super().__init__(Cfg)
        self.command_scale = np.array(
            (
                self.config.normalization.obs_scales.lin_vel,
                self.config.normalization.obs_scales.lin_vel,
                self.config.normalization.obs_scales.ang_vel,
            ),
            dtype=np.float16,
        )

    def buffer_init(self):
        super().buffer_init()
        self.gait_frequency = 1.5
        self.gait_process = 0

    def step(self, actions):
        # Apply actuations, simulate, call self.post_physics_step()
        # Sync render objects from physic world
        # print(self.dof_pos)
        self.actions = actions
        # print(self.actions)
        for _ in range(self.config.control.decimation):
            self.gait_process = np.fmod(self.gait_process + self.config.sim.dt * self.gait_frequency, 1.0)
            self.torques = self._compute_torques(self.actions)
            self.data.actuator_ctrls = self.torques
            step(self.model, self.data)
        self.post_physics_step()
        self.obs = self.compute_obs()

    def compute_obs(self):
        obs = np.zeros(self.config.env.num_observations, dtype=np.float16)
        diff = self.dof_pos - self.default_angles
        obs[:3] = self.gravity * self.config.normalization.gravity
        obs[3:6] = self.gyro * self.config.normalization.obs_scales.lin_vel
        obs[6:9] = self.commands * self.command_scale
        obs[9] = np.cos(2 * np.pi * self.gait_process) * (self.gait_frequency > 1.0e-8)
        obs[10] = np.sin(2 * np.pi * self.gait_process) * (self.gait_frequency > 1.0e-8)
        obs[11:23] = diff * self.config.normalization.obs_scales.dof_pos
        obs[23:35] = self.dof_vel * self.config.normalization.obs_scales.dof_vel
        obs[35:47] = self.actions
        return obs
