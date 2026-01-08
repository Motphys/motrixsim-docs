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

import motrixsim as mx
from motrixsim import SceneData, step, viewer

# Use default model and data
# viewer.launch()

# use custom model
# model = mx.load_model("examples/assets/body.xml")
# viewer.launch(model)

# Use custom model with empty data
# model = mx.load_model("examples/assets/body.xml")
# data = SceneData(model)
# viewer.launch(model, data)

# Use custom model with physics data
# This example uses the Boston Dynamics Spot robot with arm to demonstrate
# the interactive viewer with a model that includes actuators
model = mx.load_model("examples/assets/boston_dynamics_spot/scene_arm.xml")
data = SceneData(model)
for _ in range(20):
    # Physics world step
    step(model, data)

viewer.launch(model, data)
