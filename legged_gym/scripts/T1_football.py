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
import onnxruntime as ort

from legged_gym.addr import LEGGED_GYM_ENVS_DIR
from legged_gym.envs.T1_football.T1 import T1_Football_env
from legged_gym.envs.T1_football.T1_config import T1FootballCfg
from legged_gym.utils import runner

policy_path = "/policy/booster_t1/loco.onnx"
policy_kick = "/policy/booster_t1/n_kick.onnx"
env = T1_Football_env(T1FootballCfg)
forward_value = 0.0
right_value = 0.0
turn_value = 0.0
actions = np.zeros(12)
camera = env.model.cameras[0]
env.get_render().set_main_camera(camera)


class PolicyRunner:
    session: ort.InferenceSession
    input_name: str
    output_name: str

    def __init__(self, path: str):
        self.session = ort.InferenceSession(LEGGED_GYM_ENVS_DIR + path, providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def infer(self, observation: np.ndarray) -> np.ndarray:
        input_data = observation.reshape(1, -1).astype(np.float32)
        outputs = self.session.run([self.output_name], {self.input_name: input_data})
        return outputs[0][0]


walk_policy = PolicyRunner(policy_path)
kick_policy = PolicyRunner(policy_kick)

policies = {
    "walk": walk_policy,
    "kick": kick_policy,
}


def step():
    global forward_value
    global turn_value
    global right_value
    global actions

    last_state = env.state
    env.step(actions)
    policy = policies[env.state]
    obs = env.get_observation()
    actions = policy.infer(obs)

    forward_value = 0.0
    right_value = 0.0
    turn_value = 0.0

    input = env.get_render().input
    if input.is_key_pressed("q"):
        turn_value = 0.6
    if input.is_key_pressed("e"):
        turn_value = -0.6
    if input.is_key_pressed("w"):
        forward_value = 0.6
    if input.is_key_pressed("s"):
        forward_value = -0.4
    if input.is_key_pressed("a"):
        right_value = 0.4
    if input.is_key_pressed("d"):
        right_value = -0.4
    if input.is_key_pressed("f"):
        if env.kick():
            actions = np.zeros(23)
    if input.is_key_pressed("g"):
        env.T = 60
        if env.state == "kick":
            env.state = "walk"
            actions = np.zeros(12)
        env.frame_id = env.start
    env.UpdateAction(forward_value, right_value, turn_value)

    if input.is_key_pressed("r"):
        env.env_reset()

    if last_state == "kick" and env.state == "walk":
        # finished kick motion, back to walk
        actions = np.zeros(12)

    env.draw_predict_goal()


runner.loop(
    policy_step=step,
    render=env.render,
    policy_dt=env.config.sim.dt * env.config.control.decimation,
)
