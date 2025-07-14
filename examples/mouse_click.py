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

# This example demonstrates how to determine a target intersection point via mouse events,
# and controls the movement of a ball by setting its velocity.
# It involves functionalities related to `WorldBody` and `FloatingBase`.

import time

import numpy as np

from motrixsim import SceneData, load_model, step
from motrixsim.render import RenderApp


# Calculate the intersection of a ray with a ground plane.
def ray_plane_intersection(ray, normal):
    origin = np.array([ray[0], ray[1], ray[2]])
    direction = np.array([ray[3], ray[4], ray[5]])
    denom = np.dot(normal, direction)
    if abs(denom) > 1e-6:
        t = -np.dot(origin, normal) / denom
        if t >= 0.0:
            return origin + t * direction

    return np.array([0, 0, 0])


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
# - Double-click the left mouse button to calculate the target point
def main():
    # Create render window for visualization
    render = RenderApp()
    # The scene description file
    path = "examples/assets/mouse_click.xml"
    # Load the scene model
    model = load_model(path)
    # Create the render instance of the model
    render.launch(model)
    # Create the physics data of the model
    data = SceneData(model)

    # The plane normal
    normal = np.array([0.0, 0.0, 1.0])
    # The world body floating base.
    body_fb = model.get_body(model.get_body_index("sphere")).floatingbase
    # Move speed
    move_speed = 1.2
    # Target position
    target_position = np.array([0, 0])
    while True:
        # Control the step interval to prevent too fast simulation
        time.sleep(0.002)
        # Step the physics world
        step(model, data)
        # Sync render objects from physic world
        render.sync(data)
        # Get input from render
        input = render.input
        if input.is_mouse_just_pressed("left"):
            # Get mouse ray from render input
            ray = input.mouse_ray()
            # Calculate the intersection point, which is target
            target_position = ray_plane_intersection(ray, normal)

        # Get current position of the body
        current_pos = body_fb.get_translation(data)
        # Calculate the direction
        move_direction = target_position[:2] - current_pos[:2]
        # Check if the body reaches the target
        if np.linalg.norm(move_direction) < 0.1:
            move_direction = np.array([0, 0])

        # Get and set velocity
        linear_vel = body_fb.get_global_linear_velocity(data)
        body_fb.set_global_linear_velocity(
            data, np.array([move_direction[0] * move_speed, move_direction[1] * move_speed, linear_vel[2]])
        )


if __name__ == "__main__":
    main()
