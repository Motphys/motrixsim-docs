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

from motrixsim import SceneData, load_model, run
from motrixsim.render import RenderApp


def main():
    # Create render window for visualization
    with RenderApp() as render:
        # tag::init batch data
        size = 10
        batch_size = size * size
        path = "examples/assets/stanford_tidybot/scene.xml"

        model = load_model(path)
        data = SceneData(model, batch=(batch_size,))

        # When create scene data in batch mode, we also need to launch the render in batch mode.
        # The render offset can be assigned for each instance to avoid overlapping.
        # Note: The offset only affects the render objects, the physics instance is still at the origin.
        render_offset = []
        for i in range(size):
            for j in range(size):
                render_offset.append([-i * 2, j * 2, 0])
        render.launch(model, batch=batch_size, render_offset=render_offset)
        # a batch dimension is added to all data fields
        assert data.dof_pos.shape == (batch_size, model.num_dof_pos)

        # end::init batch data

        print("Press 'r' to reset all instances")
        print("Press 'a' to apply a random actuator ctrls to all instances")
        print("Press 's' to apply a random actuator ctrls to the first instance")
        print("Press 'd' to apply a random actuator ctrls to instances with odd index")

        def physics_step():
            model.step(data)

        def render_step():
            render.sync(data)
            input = render.input
            if input.is_key_just_pressed("r"):
                data.reset(model)
            if input.is_key_just_pressed("a"):
                # tag:: set actuator ctrl in batch
                data.actuator_ctrls = np.random.rand(batch_size, model.num_actuators)
                # end:: set actuator ctrl in batch
            if input.is_key_just_pressed("s"):
                # tag:: set actuator ctrl in single
                single_data = data[0]
                assert single_data.shape == ()
                single_data.actuator_ctrls = np.random.rand(model.num_actuators)
                # end:: set actuator ctrl in single
            if input.is_key_just_pressed("d"):
                # tag:: set actuator ctrl in mask
                mask = np.arange(batch_size) % 2 == 1
                masked_data = data[mask]
                masked_data.actuator_ctrls = np.random.rand(int(batch_size / 2), model.num_actuators)
                # end:: set actuator ctrl in mask

        run.render_loop(
            model.options.timestep,
            60.0,
            physics_step,
            render_step,
        )


if __name__ == "__main__":
    main()
