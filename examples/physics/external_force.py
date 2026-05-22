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
Example demonstrating external force and torque application to links.

This example shows how to use add_external_force and add_external_torque APIs
to apply forces and torques to links in local coordinate frames.

The example uses a box on a plane scene to demonstrate the effects of different
force/torque application patterns. The box is subject to gravity, making the
demonstration more physically realistic.

Phases:
1. Local-space upward force at center of mass (0-3s) - Box moves up without rotation
2. Local-space torque around Z-axis (3-5s) - Box spins in place
3. Local-space force at offset point (5-12s) - Box rotates and moves
"""

import time

from motrixsim import SceneData, load_model, step
from motrixsim.render import RenderApp


def main():
    # Create render window for visualization
    with RenderApp() as render:
        # Load box on plane scene for force/torque demonstration
        model = load_model("examples/assets/box_on_plane.xml")
        render.launch(model)
        data = SceneData(model)

        # Get the box link for applying forces
        box_link = model.get_link("box")

        start_time = time.time()
        phase = 0

        while True:
            elapsed = time.time() - start_time

            # Apply forces based on phase (cycle every 12 seconds)
            cycle_time = elapsed % 12

            if cycle_time < 3.0:
                # Phase 1: local-space upward force at center of mass
                # This causes pure translation without rotation
                # box volume is 0.5x0.5x0.5, density is 1000, gravity is -9.81,
                # so weight is 0.5*0.5*0.5*1000*9.81 = 1226.25, applying 1226.25 force will lift it up
                if phase != 1:
                    phase = 1
                    print("Phase 1: Local-space force [0, 0, 1226.25] at center of mass (upward translation)")
                box_link.add_external_force(data, [0, 0, 1226.25], local=True)

            elif cycle_time < 5.0:
                # Phase 2: local-space torque around Z-axis
                # This causes pure rotation without translation
                if phase != 2:
                    phase = 2
                    print("Phase 2: Local-space torque [0, 0, 500] around Z-axis (rotation)")
                box_link.add_external_torque(data, [0, 0, 500], local=True)

            else:
                # Phase 3: Force at offset point from center of mass
                # This creates both linear acceleration AND torque
                # The force is applied at a point offset from COM, generating a moment
                if phase != 3:
                    phase = 3
                    print("Phase 3: Local-space force [1000, 0, 0] at offset point [0, 0, 0.2] (force + torque)")
                box_link.add_external_force(data, [1000, 0, 0], point=[0, 0, 0.2], local=True)

            step(model, data)
            render.sync(data)


if __name__ == "__main__":
    main()
