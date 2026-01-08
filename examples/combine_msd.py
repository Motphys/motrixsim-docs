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

"""
Combine MSD Example

This example demonstrates how to combine multiple models together using
the Scene.attach() method. The new API allows you to:

1. Load multiple model files
2. Attach them together with optional transformations (translation, rotation)
3. Add prefixes/suffixes to avoid name conflicts
4. Extract subtrees from models before attaching
5. Build the final combined model for simulation
"""

# tag::combine_msd_example[]
import time

import motrixsim as mx

# Load the base scene
msd_scene = mx.msd.from_file("examples/assets/store/scene.xml")

# Load a dog model and attach an arm to it
msd_dog = mx.msd.from_file("examples/assets/boston_dynamics_spot/spot.xml")
msd_arm = mx.msd.from_file("examples/assets/stanford_tidybot_adhesion/tidybot.xml")
# Attach arm subtree to the dog's hip link
msd_dog.attach(
    msd_arm,
    self_link_name="hl_hip",
    other_link_name="bracelet_link",  # Extract subtree from arm
    other_rotation=[-0.71, 0, 0, 0.71],  # Rotate 90 degrees around X axis
    other_prefix="arm_",
)

# Attach multiple dogs to the scene at different positions
# Note: other is cloned internally, so msd_dog can be reused
msd_scene.attach(msd_dog, other_translation=[1, 0, 0], other_prefix="dog0_")
msd_scene.attach(msd_dog, other_translation=[2, 0, 0], other_prefix="dog1_")
msd_scene.attach(msd_dog, other_translation=[3, 0, 0], other_prefix="dog2_")

# Build the final model
model = msd_scene.build()

with mx.render.RenderApp("warn") as render:
    render.launch(model)
    data = mx.SceneData(model)

    while True:
        time.sleep(model.options.timestep)
        mx.step(model, data)
        render.sync(data)
# end::combine_msd_example[]
