import numpy as np

from legged_gym.envs.base.legged_robot import Legged_Robot


class G1_env(Legged_Robot):
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
        self.model.options.timestep = self.config.sim.dt

    def _post_physics_step_callback(self):
        super()._post_physics_step_callback()
        period = 0.8
        self.phase = (self.episode_length_buf * self.dt) % period / period

    def compute_obs(self):
        sin_phase = np.sin(2 * np.pi * self.phase)
        cos_phase = np.cos(2 * np.pi * self.phase)
        diff = self.dof_pos - self.default_angles
        self.obs[:3] = self.gyro * self.config.normalization.obs_scales.ang_vel
        self.obs[3:6] = self.gravity
        self.obs[6:9] = self.commands * self.command_scale
        self.obs[9:21] = diff
        self.obs[21:33] = self.dof_vel * self.config.normalization.obs_scales.dof_vel
        self.obs[33:45] = self.actions
        self.obs[45] = sin_phase
        self.obs[46] = cos_phase
        return self.obs
