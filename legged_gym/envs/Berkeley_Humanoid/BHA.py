import numpy as np
from scipy.spatial.transform import Rotation

from legged_gym.envs.base.legged_robot import Legged_Robot


class BHA_env(Legged_Robot):
    def compute_obs(self):
        # print(self.default_angles)
        obs = np.zeros(self.config.env.num_observations, dtype=np.float16)
        diff = self.dof_pos - self.default_angles
        obs[:3] = self.commands
        # obs[3:6] = self.linear_vel * self.config.normalization.obs_scales.lin_vel
        obs[3:6] = self.gyro * self.config.normalization.obs_scales.ang_vel
        obs[6:9] = self.gravity
        obs[9:31] = diff
        obs[31:53] = self.dof_vel
        obs[53:75] = self.actions

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

    def buffer_init(self):
        # init buffers
        k = False
        self.commands = np.zeros(3, dtype=np.float32)
        self.obs = np.zeros(self.config.env.num_observations, dtype=np.float32)
        self.kps = np.ones(self.config.env.num_actions, dtype=np.float32)
        self.kds = np.ones(self.config.env.num_actions, dtype=np.float32)
        if type(self.config.control.stiffness) is int:
            self.kps = self.kps * self.config.control.stiffness
            self.kds = self.kds * self.config.control.damping
            k = True
        self.max_episode_length = self.config.sim.max_episode_length
        self.reset_buf = False
        self.default_angles = np.zeros(self.config.env.num_actions, dtype=np.float16)
        found = False
        for i in range(self.model.num_actuators):
            for name in (
                self.config.init_state.default_joint_angles.keys()
            ):  # cfg["init_state"]["default_joint_angles"].keys():
                if name in self.model.actuator_names[i]:
                    self.default_angles[i] = self.config.init_state.default_joint_angles[
                        name
                    ]  # .cfg["init_state"]["default_joint_angles"][name]
                    found = True
            if not found:
                self.default_angles[i] = self.config.init_state.default_joint_angles[
                    "default"
                ]  # cfg["init_state"]["default_joint_angles"]["default"]
            if k is False:
                found = False
                for name in self.config.control.stiffness.keys():  # cfg["control"]["stiffness"].keys():
                    # print("##################")
                    # print(i)
                    # print(name)

                    # print(self.model.actuator_names[i])
                    if name in self.model.actuator_names[i]:
                        # print("found")
                        self.kps[i] = self.config.control.stiffness[name]  # cfg["control"]["stiffness"][name]
                        self.kds[i] = self.config.control.damping[name]
                        # dof_damping[i] = cfg["control"]["damping"][name]
                        found = True
                    if found:
                        break
                if not found:
                    print("no found")
                    raise ValueError("PD gain of joint  were not defined")
        # print(self.default_angles)
        self.episode_length_buf = 0
        self.common_step_counter = 0
        self.last_actions = np.zeros(self.config.env.num_actions, dtype=np.float16)
        self.commands = self.resample_commands()
        self.torque_limits = self.config.control.torque_limits

        self._sync_dof_data()
