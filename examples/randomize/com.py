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
Eccentric Cylinder on Inclined Plane Experiment

This example demonstrates how center of mass randomization affects the
rolling behavior of cylinders on an inclined plane.

The intuitive visualization:
- Standard COM (no offset): Cylinder rolls smoothly with uniform acceleration
- Slight offset: "Limping" motion with periodic speed fluctuations
- Extreme offset: Cylinder may rock back and forth like a tumbler

This experiment directly transforms abstract CoM offset coordinates into
visibly different motion trajectories.

Key concepts:
- Center of mass randomization in the cylinder's cross-section
- Different rolling behaviors based on COM position
- Batch simulation to compare multiple instances side-by-side

Mouse controls:
- Press and hold left button then drag to rotate the camera/view
- Press and hold right button then drag to pan/translate the view
"""

import numpy as np
from scipy.spatial.transform import Rotation

from motrixsim import SceneData, load_model
from motrixsim.render import Color, RenderApp


def draw_com_gizmos(render, cylinder, data, com_offset, render_offset):
    """
    Draw center of mass visualization using gizmos.

    Args:
        render: RenderApp instance
        cylinder: Link object for the cylinder
        data: SceneData instance
        com_offset: COM offset in local frame, shape (N, 3)
        render_offset: List of render offsets for each instance
    """
    # Get world position and rotation of the cylinder link
    world_pos = cylinder.get_position(data)  # shape: (16, 3)
    world_rot = cylinder.get_rotation(data)  # shape: (16, 4) quaternion (i,j,k,w)

    # Transform local COM offset to world frame
    # COM offset is in link local frame, need to rotate to world frame
    rot_mat = Rotation.from_quat(world_rot)  # shape: (16,) Rotation objects
    world_com_offset = rot_mat.apply(com_offset)  # shape: (16, 3)

    # Calculate world COM position
    world_com_pos = world_pos + world_com_offset  # shape: (16, 3)

    # Draw a sphere at each COM position
    for i in range(len(render_offset)):
        # Get render offset for this instance
        ro = np.array(render_offset[i])
        render.gizmos.draw_sphere(
            0.15,  # radius
            world_com_pos[i] + ro,  # world COM position + render offset
            color=Color.rgb(1, 0, 0),  # red color
        )


def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/cylinder_on_inclined_plane.xml"
        # Load the scene model
        model = load_model(path)

        # Create 16 instances in a 4x4 grid
        # Stagger them horizontally to show all cylinders clearly
        render_offset = []
        for i in range(4):
            for j in range(4):
                render_offset.append([-i * 8, j * 8, 0])

        # Create the render instance of the model
        render.launch(model, batch=16, render_offset=render_offset)

        # Create the physics data of the model
        data = SceneData(model, batch=(16,))

        # Get the cylinder link
        cylinder = model.get_link(0)

        # Randomize center of mass in the cylinder's cross-section
        # The cylinder's rolling axis is along Y, so we randomize in X-Z plane
        # X direction: perpendicular to slope surface (affects stability)
        # Z direction: along the slope surface (affects rolling resistance)
        com_offset = np.zeros((16, 3), dtype=np.float32)

        # Generate different types of COM offsets for demonstration:
        # - First 4: Near zero offset (smooth rolling)
        # - Next 4: Slight offset (periodic fluctuations)
        # - Last 8: Large offset (extreme rocking behavior)
        com_offset[:4, 0] = np.random.uniform(-0.05, 0.05, 4)  # Near center
        com_offset[4:8, 0] = np.random.uniform(-0.15, 0.15, 4)  # Slight offset
        com_offset[8:, 0] = np.random.uniform(-0.25, 0.25, 8)  # Large offset

        # Apply randomization
        cylinder.set_center_of_mass_override(data, com_offset)

        # Verify randomization was applied
        com_get = cylinder.get_center_of_mass_override(data)
        assert np.allclose(com_get, com_offset)

        # Print COM offset summary for reference
        print("\n" + "=" * 60)
        print("Center of Mass Randomization Summary")
        print("=" * 60)
        for i in range(16):
            offset_str = f"({com_get[i, 0]:.3f}, {com_get[i, 1]:.3f}, {com_get[i, 2]:.3f})"
            if abs(com_get[i, 0]) < 0.1:
                behavior = "Smooth rolling"
            elif abs(com_get[i, 0]) < 0.2:
                behavior = "Periodic fluctuation"
            else:
                behavior = "Extreme rocking"
            print(f"Instance {i:2d}: COM offset = {offset_str:>25s} -> {behavior}")
        print("=" * 60 + "\n")

        # Simulation loop
        while True:
            model.step(data)
            # Draw center of mass visualization
            draw_com_gizmos(render, cylinder, data, com_get, render_offset)
            render.sync(data)


if __name__ == "__main__":
    main()
