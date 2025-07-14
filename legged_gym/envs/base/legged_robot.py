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

import random

import numpy as np
from scipy.spatial.transform import Rotation

from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg
from motrixsim import SceneData, load_model, step
from motrixsim.render import RenderApp


class Legged_Robot:
    def __init__(self, Cfg: LeggedRobotCfg):
        self.config = Cfg
        self.env_init()
        self.render_init()
        self.buffer_init()

    def buffer_init(self):
        # init buffers
        unified_stiffness = False
        unified_damping = False
        self.commands = np.zeros(3, dtype=np.float32)
        self.obs = np.zeros(self.config.env.num_observations, dtype=np.float32)
        self.kps = np.ones(self.config.env.num_actions, dtype=np.float32)
        self.kds = np.ones(self.config.env.num_actions, dtype=np.float32)
        if type(self.config.control.stiffness) is int:
            self.kps = self.kps * self.config.control.stiffness
            unified_stiffness = True
        else:
            assert isinstance(self.config.control.stiffness, dict), "config.control.stiffess must be a dict or an int"

        if type(self.config.control.damping) is int:
            self.kds = self.kds * self.config.control.damping
            unified_damping = True
        else:
            assert isinstance(self.config.control.damping, dict), "config.control.damping must be a dict or an int"

        self.max_episode_length = self.config.sim.max_episode_length
        self.reset_buf = False
        self.default_angles = np.zeros(self.config.env.num_actions, dtype=np.float16)

        for actuator_index, actuator in enumerate(self.model.actuators):
            assert actuator.target_type == "joint", "The actuator must target a joint"
            assert actuator.typ == "motor", "The actuator type must be 'motor' for this implementation"
            actuator_name = actuator.name
            joint_name = actuator.target_name
            default_joint_angle = self.config.init_state.default_joint_angles.get(joint_name, None)

            if default_joint_angle is not None:
                self.default_angles[actuator_index] = default_joint_angle
            else:
                # If no specific default angle is set for the joint, use the default value
                self.default_angles[actuator_index] = self.config.init_state.default_joint_angles.get("default", 0.0)
                print(
                    f"""Warning: No default angle set for joint '{joint_name}',
                      using default value {self.default_angles[actuator_index]}"""
                )

            if not unified_stiffness:
                self.kps[actuator_index] = self.config.control.stiffness[actuator_name]

            if not unified_damping:
                self.kds[actuator_index] = self.config.control.damping[actuator_name]

        # print("default_angles = ",self.default_angles)
        self.episode_length_buf = 0
        self.common_step_counter = 0
        self.last_actions = np.zeros(self.config.env.num_actions, dtype=np.float16)
        self.commands = self.resample_commands()
        self.torque_limits = self.config.control.torque_limits
        self._sync_dof_data()

    def render_init(self):
        # Create render window for visualization
        self._render = RenderApp()
        # Launch the render with the model
        self._render.launch(self.model)

    def env_init(self):
        # The scene description file
        path = self.config.asset.file
        # Load the scene model
        self.model = load_model(path)
        self.model.options.timestep = self.config.sim.dt
        # Create the physics data of the model
        self.data = SceneData(self.model)
        self.model.forward_kinematic(self.data)
        self.body = self.model.get_body(self.config.asset.body_name)

    def step(self, actions):
        # Apply actuations, simulate, call self.post_physics_step()

        self.actions = actions
        for _ in range(self.config.control.decimation):
            self.torques = self._compute_torques(self.actions)
            self.data.actuator_ctrls = self.torques
            step(self.model, self.data)
        self.post_physics_step()
        self.obs = self.compute_obs()

    def render(self):
        """Render the scene"""
        self._render.sync(self.data)

    def post_physics_step(self):
        """check terminations, compute observations and rewards
        calls self._post_physics_step_callback() for common computations
        calls self._draw_heightmap_vis() if needed
        """
        self.episode_length_buf += 1
        self.common_step_counter += 1

        # prepare quantities
        self.linear_vel = self.get_sensor_value(self.config.sensor.local_linvel)
        self.gyro = self.get_sensor_value(self.config.sensor.gyro)
        self.pose = self.body.get_pose(self.data)
        inv_rotation = Rotation.from_quat(self.pose[3:7]).inv()  ###xyzw
        self.gravity = inv_rotation.apply(np.array([0.0, 0.0, -1.0]))
        self._sync_dof_data()
        self._post_physics_step_callback()
        self.check_termination()
        self.reset()

    def get_sensor_value(self, sensor_name):
        sensor_value = self.model.get_sensor_value(sensor_name, self.data)
        return sensor_value

    def _post_physics_step_callback(self):
        """Callback called before computing terminations, rewards, and observations
        Default behaviour: Compute ang vel command based on target and heading,
        compute measured terrain heights and randomly push robots
        """
        if self.episode_length_buf % 100 == 0:
            self.commands = self.resample_commands()

    def check_termination(self):
        """Check if environments need to be reset"""
        self.terminated = self.is_fall()
        self.timed_out = self.episode_length_buf > self.max_episode_length
        self.reset_buf = self.terminated | self.timed_out

    def is_fall(self):
        rotation = Rotation.from_quat(self.pose[3:7])  # xyzw
        rotated_z_axis = rotation.apply(np.array([0.0, 0.0, 1.0]))
        thr = 0.3
        dot = np.dot(rotated_z_axis, np.array([0.0, 0.0, 1.0]))
        return dot < thr

    def reset(self):
        if self.reset_buf:
            self.env_reset()
            self.buffer_init()

    def env_reset(self):
        self.data.reset(self.model)
        self.model.forward_kinematic(self.data)

    def get_observation(self):
        return self.obs

    def compute_obs(self):
        raise NotImplementedError("compute_obs() must be implemented for env")

    def resample_commands(self):
        x = (
            random.random() * (self.config.commands.ranges.lin_vel_x[1] - self.config.commands.ranges.lin_vel_x[0])
            - self.config.commands.ranges.lin_vel_x[1]
        )
        y = (
            random.random() * (self.config.commands.ranges.lin_vel_y[1] - self.config.commands.ranges.lin_vel_y[0])
            - self.config.commands.ranges.lin_vel_y[1]
        )
        rot = (
            random.random() * (self.config.commands.ranges.ang_vel_yaw[1] - self.config.commands.ranges.ang_vel_yaw[0])
            + self.config.commands.ranges.ang_vel_yaw[0]
        )
        v = np.array([x, y])
        norm = v
        target_action = [
            norm[0] * self.config.normalization.obs_scales.lin_vel,
            norm[1] * self.config.normalization.obs_scales.lin_vel,
            rot * self.config.normalization.obs_scales.ang_vel,
        ]
        target_action = np.array(target_action)
        target_action = target_action * 0.2 + self.commands * 0.8
        return target_action

    def _compute_torques(self, actions):
        # Compute torques from actions.
        # pd controller
        actions_scaled = actions * self.config.control.action_scale
        control_type = self.config.control.control_type
        self._sync_dof_data()
        if control_type == "P":
            torques = self.kps * (actions_scaled + self.default_angles - self.dof_pos) - self.kds * self.dof_vel
        else:
            raise NameError(f"Unknown controller type: {control_type}")
        return np.clip(torques, -self.torque_limits, self.torque_limits)

    def _sync_dof_data(self):
        self.dof_pos = self.body.get_joint_dof_pos(self.data)
        self.dof_vel = self.body.get_joint_dof_vel(self.data)
