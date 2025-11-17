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

from absl import app, flags

import motrixsim as mtx

_File = flags.DEFINE_string("file", None, "path to model", required=True)
_BatchSize = flags.DEFINE_integer("batch", 1024, "number of instances to simulate", lower_bound=0)
_NumSteps = flags.DEFINE_integer("steps", 3000, "number of simulation steps to run", lower_bound=1)


def main(argv):
    batch_size = _BatchSize.value
    # Load the scene model
    model = mtx.load_model(_File.value)
    # Create the physics data of the model
    data = mtx.SceneData(model, batch=(batch_size,))

    t0 = time.monotonic()
    for _ in range(_NumSteps.value):
        model.step(data)
    elapsed = time.monotonic() - t0

    print(f"Summary: {_NumSteps.value} steps for {batch_size} instances in {elapsed:.3f} seconds")
    print(f"Average: {(_NumSteps.value * batch_size) / elapsed:.3f} steps/second")


if __name__ == "__main__":
    app.run(main)
