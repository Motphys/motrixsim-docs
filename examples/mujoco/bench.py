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

import mujoco
from absl import app, flags

_File = flags.DEFINE_string("file", None, "path to MJCF model file", required=True)
_NumSteps = flags.DEFINE_integer("steps", 3000, "number of simulation steps to run", lower_bound=1)


def main(argv):
    model_path = _File.value
    num_steps = _NumSteps.value

    print("Benchmark configuration:")
    print(f"  Model: {model_path}")
    print(f"  Steps: {num_steps}")
    print()

    # Load model and create data
    model = mujoco.MjModel.from_xml_path(model_path)
    data = mujoco.MjData(model)

    # Warmup
    for _ in range(100):
        mujoco.mj_step(model, data)

    # Reset data
    data = mujoco.MjData(model)

    # Benchmark
    t0 = time.monotonic()
    for _ in range(num_steps):
        mujoco.mj_step(model, data)
    elapsed = time.monotonic() - t0

    print("Results:")
    print(f"  Elapsed time: {elapsed:.3f} seconds")
    print(f"  Throughput: {num_steps / elapsed:.3f} steps/second")
    print(f"  Average time per step: {elapsed / num_steps * 1000:.3f} ms")


if __name__ == "__main__":
    app.run(main)
