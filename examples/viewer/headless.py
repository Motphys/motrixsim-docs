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

import argparse
import time
from collections import deque

from motrixsim import SceneData, load_model, step
from motrixsim.render import RenderApp


def main():
    parser = argparse.ArgumentParser(description="Headless rendering example")
    parser.add_argument("--no-wait", action="store_true", help="Use sync(wait=False) instead of sync(wait=True)")
    args = parser.parse_args()

    with RenderApp(headless=True) as renderer:
        # The scene description file
        path = "examples/assets/go1/scene.xml"
        # Load the scene model
        model = load_model(path)
        model.cameras.set_system_render_target("image", 256, 256)
        data = SceneData(model)
        renderer.launch(model)
        image_index = 0
        sync_count = 0
        t = time.monotonic()
        # Cache for pending captures when wait=False
        pending_captures = deque()
        while True:
            for _ in range(10):
                # Physics world step
                step(model, data)

            cap = renderer.system_camera.capture()
            renderer.sync(data, wait=not args.no_wait)
            sync_count += 1

            if args.no_wait:
                # When wait=False, cache the capture and check pending ones
                pending_captures.append(cap)
                # Check if any pending capture has image ready
                while pending_captures:
                    pending_cap = pending_captures[0]
                    img = pending_cap.take_image()
                    if img is not None:
                        pending_captures.popleft()
                        print(image_index, img.pixels[0:2, 0:2])
                        image_index += 1
                    else:
                        # First pending capture not ready, stop checking
                        break
            else:
                # When wait=True, image should be ready immediately
                img = cap.take_image()
                if img is not None:
                    print(image_index, img.pixels[0:2, 0:2])
                    image_index += 1
            if image_index > 1000:
                break
        cost = time.monotonic() - t
        print(f"total cost = {cost}")
        images_per_second = image_index / cost
        print("fps = ", images_per_second)


if __name__ == "__main__":
    main()
