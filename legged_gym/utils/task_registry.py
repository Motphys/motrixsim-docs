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

from legged_gym.envs.base.legged_robot import Legged_Robot
from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg


class TaskRegistry:
    def __init__(self):
        self.task_classes = {}
        self.env_cfgs = {}

    def register(self, name: str, task_class: Legged_Robot, env_cfg: LeggedRobotCfg):
        self.task_classes[name] = task_class
        self.env_cfgs[name] = env_cfg

    def get_task_class(self, name: str) -> Legged_Robot:
        return self.task_classes[name]

    def get_cfgs(self, name) -> LeggedRobotCfg:
        env_cfg = self.env_cfgs[name]
        return env_cfg

    def make_env(self, name) -> Legged_Robot:
        if name in self.task_classes:
            task_class = self.get_task_class(name)
        else:
            raise ValueError(f"Task with name: {name} was not registered")

        env_cfg = self.get_cfgs(name)
        print(env_cfg)
        print(task_class)
        env = task_class(Cfg=env_cfg)
        return env


# make global task registry
task_registry = TaskRegistry()
