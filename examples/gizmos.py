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


import numpy as np
from scipy.spatial.transform import Rotation

from motrixsim import SceneData, load_model, run, step
from motrixsim.render import Color, RenderApp


def main():
    with RenderApp() as render:
        path = "examples/assets/model.xml"
        model = load_model(path)
        data = SceneData(model)

        render.launch(model)

        x = 0
        dir = 1

        rot = Rotation.identity()
        dr = Rotation.from_rotvec(0.01 * np.array([0, 0, 1]))

        # set gizmos by api
        render.gizmos.draw_collider = True
        render.gizmos.draw_site = True
        render.gizmos.draw_joint = True
        render.gizmos.joint_size = 1.5
        render.gizmos.line_width = 5
        render.gizmos.collider_color = Color.rgb(0.5, 1, 0.5)
        render.gizmos.joint_color = Color.rgb(1, 1, 0.5)
        # end

        # enable gizmos editor
        render.opt.set_left_panel_vis(True)
        # end

        def phys_step():
            step(model, data)

        def render_step():
            # tag::draw_gizmos[]
            nonlocal rot, dir, x
            # gizmos is drawning in immediate mode. so you must call it every frame
            gizmos = render.gizmos
            gizmos.draw_sphere(0.1, np.array([x, 0, 1]), color=Color.rgb(1, 0, 0))

            gizmos.draw_cuboid(
                size=np.array([0.2, 0.3, 0.4]), pos=np.array([1, 0, 1]), rot=rot.as_quat(), color=Color.rgb(0, 1, 0)
            )

            gizmos.draw_cuboid(
                size=np.array([0.1, 0.1, 1]), pos=np.array([3, 0, 1]), rot=rot.as_quat(), color=Color.rgb(0, 1, 0)
            )

            gizmos.draw_capsule(0.5, 0.5, pos=np.array([1, 1, 1]), rot=Rotation.identity().as_quat())
            gizmos.draw_cylinder(0.5, 0.5, pos=np.array([2, 1, 1]), rot=Rotation.identity().as_quat())
            gizmos.draw_arrow(start=np.array([3, 1, 1]), end=np.array([4, 2, 1]), color=Color.rgb(1, 1, 0))
            gizmos.draw_line(start=np.array([3, 2, 1]), end=np.array([4, 3, 1]), color=Color.rgb(1, 1, 0))
            gizmos.draw_ray(start=np.array([4, 1, 1]), vector=np.array([3, 0.2, 0]), color=Color.rgb(1, 1, 0.2))
            gizmos.draw_grid(
                pos=np.array([0, -2, 1]),
                rot=rot.as_quat(),
                color=Color.rgb(1, 0.5, 0.2),
            )
            gizmos.draw_rect(
                pos=np.array([3, -2, 1]),
                rot=Rotation.identity().as_quat(),
                width=1.5,
                height=3.5,
                color=Color.rgb(0.5, 1, 0.2),
            )
            # end::draw_gizmos[]

            x += dir * 0.01
            if x > 1:
                dir = -1
            elif x < -1:
                dir = 1

            rot = dr * rot
            render.sync(data)

        run.render_loop(model.options.timestep, 60, phys_step, render_step)


if __name__ == "__main__":
    main()
