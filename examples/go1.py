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
import time

import numpy as np
import onnxruntime as ort
from scipy.spatial.transform import Rotation

from motrixsim import SceneData, SceneModel, load_model, step
from motrixsim.render import RenderApp

default_joint_pos = np.array([0.1, 0.9, -1.8, -0.1, 0.9, -1.8, 0.1, 0.9, -1.8, -0.1, 0.9, -1.8])
action_scale = 0.5
lin_vel_scale = 0.7
ang_vel_scale = 1.5


# Read data from the world as input parameters for the neural network
def compute_observations(last_actions, target_action, model: SceneModel, data: SceneData):
    obs = []
    # Get body data
    body_index = model.get_body_index("trunk")
    body = model.get_body(body_index)

    # linear velocity
    linear_vel = model.get_sensor_value("local_linvel", data)
    obs.extend(linear_vel.tolist())
    # gyro vel
    gyro = model.get_sensor_value("gyro", data)
    obs.extend(gyro.tolist())
    # gravity
    pose = body.get_pose(data)
    inv_rotation = Rotation.from_quat(pose[3:7]).inv()
    gravity = inv_rotation.apply(np.array([0.0, 0.0, -1.0]))
    obs.extend(gravity)

    dof_pos = body.get_joint_dof_pos(data)
    dof_vel = body.get_joint_dof_vel(data)
    diff = dof_pos - default_joint_pos
    obs.extend(diff.tolist())
    obs.extend(dof_vel.tolist())
    obs.extend(last_actions)
    obs.extend(target_action)
    return obs


# Set a target posiion randomly and go back
def update_target(goback, body_position: np.ndarray):
    target_action = [0, 0]
    if goback:
        v = -body_position[:2]
        norm = v / np.linalg.norm(v)
        target_action = [norm[0] * lin_vel_scale, norm[1] * lin_vel_scale, 0]
    else:
        x = random.random() * 4.0 - 2.0
        y = random.random() * 4.0 - 2.0
        rot = random.random() * 4.0 - 2.0
        v = np.array([x, y])
        norm = v / np.linalg.norm(v)
        target_action = [norm[0] * lin_vel_scale, norm[1] * lin_vel_scale, rot * ang_vel_scale]
    return target_action


# Apply actions to actuators from the neural network
def apply_actions(actions, model: SceneModel, data: SceneData):
    start_actuator_index = model.get_actuator_index("FR_hip")
    for index, act in enumerate(actions):
        actuator_index = start_actuator_index + index
        ctrl = act * action_scale + default_joint_pos[index]
        actuator = model.get_actuator(actuator_index)
        actuator.set_ctrl(data, ctrl)


# Dose the robot fall?
def is_fall(model: SceneModel, data: SceneData):
    pose = model.get_link("trunk").get_pose(data)
    rotation = Rotation.from_quat(pose[3:7])
    rotated_z_axis = rotation.apply(np.array([0.0, 0.0, 1.0]))
    thr = 0.3
    dot = np.dot(rotated_z_axis, np.array([0.0, 0.0, 1.0]))
    return dot < thr


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def main():
    # Create render window for visualization
    render = RenderApp()
    render.opt.set_left_panel_vis(True)
    # The scene description file
    path = "examples/assets/go1/scene.xml"
    # Load the scene model
    model = load_model(path)
    # Create the render instance of the model
    render.launch(model)
    # Create the physics data of the model
    data = SceneData(model)

    session = ort.InferenceSession("examples/assets/go1/go1_policy.onnx", providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    last_actions = [0] * 12
    n_infer_interval = 10
    n_set_tartget_interval = 750
    go_back = False
    nsteps = 0
    target_action = [0.5, 0, 0]

    while True:
        # Control the step interval to prevent too fast simulation
        time.sleep(0.002)
        # Physics world step
        step(model, data)

        # If go1 falls, reset the scene
        if is_fall(model, data):
            data = SceneData(model)

        # Add step count
        nsteps += 1
        if nsteps % n_infer_interval == 0:
            # Set random target
            if nsteps % n_set_tartget_interval == 0:
                body_pose = model.get_body(model.get_body_index("trunk")).get_pose(data)
                target_action = update_target(go_back, body_pose[:3])
                go_back = not go_back
            # Get observation
            obs = compute_observations(last_actions, target_action, model, data)
            # Setup input data
            input_data = np.array(obs).reshape(1, 48).astype(np.float32)
            # Run neural network to get output
            outputs = session.run([output_name], {input_name: input_data})
            # Read actions from output
            actions = outputs[0][0]
            # Apply action to model
            apply_actions(actions, model, data)
            # Record action as the next step input
            last_actions = actions

        # Sync render objects from physic world
        render.sync([data])


if __name__ == "__main__":
    main()
