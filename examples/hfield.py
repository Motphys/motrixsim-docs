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

from motrixsim import SceneData, load_model, step
from motrixsim.render import RenderApp


def demonstrate_hfield_api(model):
    """Demonstrate height field API usage"""
    print("=== Height Field API Demo ===")

    # tag::basic_access
    # Get number of height fields
    num_hfields = model.num_hfields
    print(f"Scene contains {num_hfields} height fields")

    # Get height field by name
    hfield1 = model.get_hfield("terrain1")
    print(f"Height field name: {hfield1.name}")
    print(f"Grid size: {hfield1.nrow} × {hfield1.ncol}")
    print(f"Bounding box: {hfield1.bound}")

    # Get height field by index
    hfield2 = model.get_hfield(1)
    print(f"Second height field name: {hfield2.name}")

    # Get complete height matrix
    height_matrix = hfield1.height_matrix
    print(f"Height matrix shape: {height_matrix.shape}")

    # Query specific height value
    sample_height = hfield1.get(row=7, col=7)
    print(f"Center point height: {sample_height:.3f}")
    # end::basic_access

    # tag::height_analysis
    # Height data analysis
    heights = hfield1.height_matrix

    # Calculate statistics
    min_height = np.min(heights)
    max_height = np.max(heights)
    mean_height = np.mean(heights)
    std_height = np.std(heights)

    print("\nHeight statistics:")
    print(f"  Min height: {min_height:.3f}")
    print(f"  Max height: {max_height:.3f}")
    print(f"  Mean height: {mean_height:.3f}")
    print(f"  Std deviation: {std_height:.3f}")

    # Find specific elevation ranges
    high_points = np.where(heights > 0.5)
    print(f"\nPoints with height > 0.5: {len(high_points[0])}")

    # Calculate terrain slope (simple approximation)
    if heights.shape[0] > 1 and heights.shape[1] > 1:
        # Calculate elevation differences between adjacent points
        grad_y = np.gradient(heights, axis=0)
        grad_x = np.gradient(heights, axis=1)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)

        max_gradient = np.max(gradient_magnitude)
        print(f"Max slope gradient: {max_gradient:.3f}")
    # end::height_analysis

    print("\n" + "=" * 50 + "\n")


def main():
    # Create render window for visualization
    render = RenderApp()
    # The scene description file
    path = "examples/assets/hfield.xml"
    # Load the scene model
    model = load_model(path)

    # Demonstrate height field API
    demonstrate_hfield_api(model)

    # Create the render instance of the model
    render.launch(model)
    # Create the physics data of the model
    data = SceneData(model)

    # Add object to demonstrate collision with height field
    # Add a test object below existing sphere
    print("Starting simulation demo...")
    print("Spheres will collide with height field and roll along terrain")
    print("Use mouse to control view:")
    print("  - Left click drag: Rotate view")
    print("  - Right click drag: Pan view")

    while True:
        # Control the step interval to prevent too fast simulation
        time.sleep(0.02)
        # Physics world step
        step(model, data)
        # Sync render objects from physic world
        render.sync(data)


if __name__ == "__main__":
    main()
