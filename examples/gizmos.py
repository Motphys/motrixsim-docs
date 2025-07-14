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

import numpy as np
from scipy.spatial.transform import Rotation

from motrixsim import SceneData, load_model, step
from motrixsim.render import Color, RenderApp


def main():
    render = RenderApp()
    path = "examples/assets/model.xml"
    model = load_model(path)
    data = SceneData(model)

    render.launch(model)

    x = 0
    dir = 1

    rot = Rotation.identity()
    dr = Rotation.from_rotvec(0.01 * np.array([0, 0, 1]))
    while True:
        time.sleep(0.02)
        step(model, data)

        # tag::draw_gizmos[]
        # gizmos is drawning in immediate mode. so you must call it every frame
        render.gizmos.draw_sphere(0.1, np.array([x, 0, 1]), color=Color.rgb(1, 0, 0))

        render.gizmos.draw_cuboid(
            size=np.array([0.2, 0.3, 0.4]), pos=np.array([1, 0, 1]), rot=rot.as_quat(), color=Color.rgb(0, 1, 0)
        )
        # end::draw_gizmos[]

        x += dir * 0.01
        if x > 1:
            dir = -1
        elif x < -1:
            dir = 1

        rot = dr * rot

        render.sync([data])


if __name__ == "__main__":
    main()
