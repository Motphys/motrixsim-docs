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

import logging
from time import sleep

import motrixsim as mx

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

input_path = "examples/assets/usd/anymal_c.usda"

model = mx.load_usd(input_path)

with mx.render.RenderApp("info") as render:
    render.launch(model)
    data = mx.SceneData(model)
    gizmos = render.gizmos
    while True:
        sleep(0.1)
        gizmos.draw_axes()

        model.step(data)
        render.sync(data)
