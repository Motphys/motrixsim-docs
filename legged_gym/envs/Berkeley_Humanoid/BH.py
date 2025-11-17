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
from scipy.spatial.transform import Rotation

from legged_gym.envs.base.legged_robot import Legged_Robot


class BH_env(Legged_Robot):
    def compute_obs(self):
        obs = np.zeros(self.config.env.num_observations, dtype=np.float16)
        diff = self.dof_pos - self.default_angles
        obs[:3] = self.commands
        # obs[3:6] = self.linear_vel * self.config.normalization.obs_scales.lin_vel
        obs[3:6] = self.gyro * self.config.normalization.obs_scales.ang_vel
        obs[6:9] = self.gravity
        obs[9:21] = diff
        obs[21:33] = self.dof_vel
        obs[33:45] = self.actions

        # self.last_actions = self.actions
        return obs

    def post_physics_step(self):
        """check terminations, compute observations and rewards
        calls self._post_physics_step_callback() for common computations
        calls self._draw_heightmap_vis() if needed
        """
        self.episode_length_buf += 1
        self.common_step_counter += 1

        # prepare quantities
        # self.linear_vel = self.get_sensor_value(self.config.sensor.local_linvel)
        self.gyro = self.get_sensor_value(self.config.sensor.gyro)
        self.pose = self.body.get_pose(self.data)
        inv_rotation = Rotation.from_quat(self.pose[3:7]).inv()  ###xyzw
        self.gravity = inv_rotation.apply(np.array([0.0, 0.0, -1.0]))
        self._sync_dof_data()
        self._post_physics_step_callback()
        self.check_termination()
        self.reset()
