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

# from legged_gym.envs.base.legged_robot import Legged_Robot
import numpy as np
import onnxruntime as ort

from legged_gym.addr import LEGGED_GYM_ENVS_DIR
from legged_gym.envs.T1.T1 import T1_env
from legged_gym.envs.T1.T1_config import T1Cfg
from legged_gym.utils import runner

policy_path = "/policy/booster_t1/booster_t1_10000.onnx"
env = T1_env(T1Cfg)
session = ort.InferenceSession(LEGGED_GYM_ENVS_DIR + policy_path, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
actions = np.zeros(12)


def step():
    global actions
    env.step(actions)
    obs = env.get_observation()
    # print(obs)
    input_data = obs.reshape(1, 47).astype(np.float32)
    outputs = session.run([output_name], {input_name: input_data})
    # Read actions from output
    actions = outputs[0][0]


runner.loop(policy_step=step, render=env.render, policy_dt=env.config.sim.dt * env.config.control.decimation)
