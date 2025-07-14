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

import time
from typing import Callable


def loop(policy_step: Callable, render: Callable, policy_dt: float, render_dt: float = 0.016):
    """
    A simple runner that run the policy step and render in different intervals.

    Args:
        policy_step (Callable): A function that performs a single policy step.
        render (Callable): A function that renders the environment.
        policy_dt (float): The time interval for policy steps in seconds.
        render_dt (float): The time interval for rendering in seconds. Default is 0.016 seconds (60 FPS).
    """
    render_dt = max(render_dt, policy_dt)
    policy_step_accumulated_times = 0.0
    while True:
        t0 = time.time()
        while policy_step_accumulated_times > policy_dt:
            policy_step_accumulated_times -= policy_dt
            policy_step()

        render()
        passed = time.time() - t0
        if passed < render_dt:
            time.sleep(render_dt - passed)

        policy_step_accumulated_times += time.time() - t0
