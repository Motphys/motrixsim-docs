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
from collections import deque

from motrixsim import SceneData, load_model, step
from motrixsim.render import CaptureTask, RenderApp


def main():
    with RenderApp(headless=True) as renderer:
        # The scene description file
        path = "examples/assets/go1/scene.xml"
        # Load the scene model
        model = load_model(path)
        cameras = model.cameras
        cameras[0].set_render_target("image", 256, 256)
        data = SceneData(model)
        renderer.launch(model)
        tasks = deque()
        image_index = 0
        sync_count = 0
        t = time.monotonic()
        while True:
            # Control the step interval to prevent too fast simulation
            for _ in range(10):
                # Physics world step
                step(model, data)

            cap = renderer.get_camera(0).capture()
            tasks.append(cap)
            renderer.sync(data)
            sync_count += 1

            while len(tasks) > 0:
                task: CaptureTask = tasks[0]
                if task.state != "pending":
                    tasks.popleft()
                    img = task.take_image()
                    if img is not None:
                        print(image_index, img.pixels[0:2, 0:2])
                        image_index += 1
                else:
                    break
            if image_index > 1000:
                break
        cost = time.monotonic() - t
        print(f"total cost = {cost}")
        images_per_second = image_index / cost
        print("fps = ", images_per_second)


if __name__ == "__main__":
    main()
