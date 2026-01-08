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
import onnxruntime as ort
from scipy.spatial.transform import Rotation

from motrixsim import SceneData, SceneModel, load_model, run, step
from motrixsim.render import RenderApp

default_joint_pos = np.array(
    [
        -0.312,
        0,
        0,
        0.669,
        -0.363,
        0,  # left leg
        -0.312,
        0,
        0,
        0.669,
        -0.363,
        0,  # right leg
        0,
        0,
        0.073,  # waist
        0.2,
        0.2,
        0,
        0.6,
        0,
        0,
        0,  # left arm
        0.2,
        -0.2,
        0,
        0.6,
        0,
        0,
        0,  # right arm
    ]
)
action_scale = 0.5
lin_vel_scale = 1.0
ang_vel_scale = 1.0


class OnnxController:
    def __init__(
        self,
        model: SceneModel,
        policy_path: str,
        default_angles: np.ndarray,
        ctrl_dt: float,
        action_scale: float = 0.5,
    ):
        self._model = model
        # Create the physics data of the model
        self._data = SceneData(self._model)

        self._policy = ort.InferenceSession(policy_path, providers=["CPUExecutionProvider"])
        self._input_name = self._policy.get_inputs()[0].name
        self._output_name = self._policy.get_outputs()[0].name

        self.command = np.zeros(3, dtype=np.float32)
        self._action_scale = action_scale
        self._default_angles = default_angles.copy()
        self._last_action = np.zeros_like(default_angles, dtype=np.float32)

        self._counter = 0
        self._n_substeps = int(round(ctrl_dt / self._model.options.timestep))

        self._phase = np.array([0.0, np.pi])
        self._gait_freq = 1.5
        self._phase_dt = 2 * np.pi * self._gait_freq * ctrl_dt

    @property
    def data(self):
        return self._data

    # Read data from the world as input parameters for the neural network
    def get_obs(self, model: SceneModel, data: SceneData, command):
        # Get body data
        body_index = model.get_body_index("pelvis")
        body = model.get_body(body_index)

        # linear velocity
        linear_vel = model.get_sensor_value("local_linvel_pelvis", data)
        # gyro vel
        gyro = model.get_sensor_value("gyro_pelvis", data)
        # gravity
        pose = body.get_pose(data)
        inv_rotation = Rotation.from_quat(pose[3:7]).inv()
        gravity = inv_rotation.apply(np.array([0.0, 0.0, -1.0]))

        dof_pos = body.get_joint_dof_pos(data)
        dof_vel = body.get_joint_dof_vel(data)
        phase = np.concatenate([np.cos(self._phase), np.sin(self._phase)])

        obs = np.hstack(
            [linear_vel, gyro, gravity, command, dof_pos - self._default_angles, dof_vel, self._last_action, phase]
        )
        return obs.astype(np.float32)

    # Apply actions to actuators from the neural network
    def apply_actions(self, actions, model: SceneModel, data: SceneData):
        start_actuator_index = model.get_actuator_index("left_hip_pitch_joint")
        for index, act in enumerate(actions):
            actuator_index = start_actuator_index + index
            ctrl = act * self._action_scale + self._default_angles[index]
            actuator = model.get_actuator(actuator_index)
            actuator.set_ctrl(data, ctrl)

    def get_control(self):
        self._counter += 1
        step(self._model, self._data)
        if self.is_fall(self._model, self._data):
            self._data = SceneData(self._model)
            self.command = np.zeros(3, dtype=np.float32)
        if self._counter % self._n_substeps == 0:
            # Get observation
            obs = self.get_obs(self._model, self._data, self.command)
            # Run neural network to get output
            outputs = self._policy.run([self._output_name], {self._input_name: obs.reshape(1, -1)})
            # Read actions from output
            actions = outputs[0][0]
            # Record action as the next step input
            self._last_action = actions.copy()
            # Apply action to model
            self.apply_actions(actions, self._model, self._data)
            # Update gait phase
            phase_tp1 = self._phase + self._phase_dt
            self._phase = np.fmod(phase_tp1 + np.pi, 2 * np.pi) - np.pi

    # Dose the robot fall?
    def is_fall(self, model: SceneModel, data: SceneData):
        pose = model.get_link("pelvis").get_pose(data)
        rotation = Rotation.from_quat(pose[3:7])
        rotated_z_axis = rotation.apply(np.array([0.0, 0.0, 1.0]))
        thr = 0.3
        dot = np.dot(rotated_z_axis, np.array([0.0, 0.0, 1.0]))
        return dot < thr


def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/g1/scene_flat.xml"
        # Load the scene model
        model = load_model(path)

        # config camera to look at g1
        camera = model.cameras[0]
        camera.rotation_track = "look_at_link"
        camera.track_target_link = model.get_link("pelvis")
        render.set_main_camera(camera)

        # Create the render instance of the model
        render.launch(model)

        policy = OnnxController(
            model,
            policy_path="examples/assets/g1/g1_policy.onnx",
            ctrl_dt=0.02,
            default_angles=default_joint_pos,
            action_scale=action_scale,
        )

        input = render.input

        def render_step():
            if input.is_key_pressed("up") or input.is_key_pressed("w"):
                policy.command[0] = 1.0 * lin_vel_scale
            elif input.is_key_pressed("down") or input.is_key_pressed("s"):
                policy.command[0] = -1.0 * lin_vel_scale
            else:
                policy.command[0] = 0.0

            if input.is_key_pressed("left"):
                policy.command[1] = 0.5 * lin_vel_scale
            elif input.is_key_pressed("right"):
                policy.command[1] = -0.5 * lin_vel_scale
            else:
                policy.command[1] = 0.0

            if input.is_key_pressed("a"):
                policy.command[2] = 2.0 * ang_vel_scale
            elif input.is_key_pressed("d"):
                policy.command[2] = -2.0 * ang_vel_scale
            else:
                policy.command[2] = 0.0

            render.sync(policy.data)

        print("Keyboard Controls:")
        print("- Press W / Up Arrow to move forward")
        print("- Press S / Down Arrow to move backward")
        print("- Press Left Arrow to move left")
        print("- Press Right Arrow to move right")
        print("- Press A to rotate left")
        print("- Press D to rotate right")

        run.render_loop(model.options.timestep, 60, policy.get_control, render_step)


# endtag

if __name__ == "__main__":
    main()
