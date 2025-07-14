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

from motrixsim import SceneData, load_model, step
from motrixsim.render import RenderApp


def main():
    render = RenderApp()

    # The scene description file
    path = "examples/assets/model.xml"
    # Load the scene model
    model = load_model(path)
    data = SceneData(model)

    render.launch(model)

    # tag::custom_ui[]
    force = 10

    # button
    def on_click():
        nonlocal force
        print("Button clicked!")
        model.get_actuator("actuator_slider").set_ctrl(data, force)
        force = -force

    def on_toggle_changed(value: bool):
        print("toggle value:", value)

    render.opt.set_left_panel_vis(True)
    render.ui.add_button("Click Me", on_click)
    render.ui.add_toggle("Some Toggle", False, on_toggle_changed)
    # end::custom_ui[]

    while True:
        time.sleep(0.02)
        step(model, data)
        render.sync([data])


if __name__ == "__main__":
    main()
