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

from legged_gym.envs.go1.go1 import Go1_env
from legged_gym.envs.go1.go1_config import Go1Cfg
from legged_gym.envs.T1.T1 import T1_env
from legged_gym.envs.T1.T1_config import T1Cfg
from legged_gym.utils.task_registry import task_registry

task_registry.register("go1", Go1_env, Go1Cfg)
task_registry.register("T1", T1_env, T1Cfg)
