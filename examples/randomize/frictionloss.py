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
Pendulum Frictionloss Randomization Experiment

This example demonstrates how frictionloss (Coulomb dry friction) affects the
motion of a pendulum released from an 80° angle.

Physical intuition:
- Frictionloss is Coulomb (dry) friction: a constant resistive force that
  opposes joint motion regardless of speed.
- Unlike viscous damping (proportional to speed), Coulomb friction can
  **freeze a joint at a non-equilibrium position**: when gravity torque
  drops below the friction threshold, the pendulum stops dead at that angle.
- Zero frictionloss: Pendulum swings freely and oscillates for a long time.
- Low frictionloss: Many oscillations, gradually settles near the bottom.
- Medium frictionloss: A few oscillations, stops partway down.
- High frictionloss: Barely moves, freezes at a large angle far from vertical.

The frozen-at-angle behavior is uniquely attributable to Coulomb friction
and is clearly visible across the 4x4 grid of instances.

Key concepts:
- Frictionloss randomization across a hinge joint
- Effect on resting angle of a pendulum released from 80 degrees
- Batch simulation to compare multiple instances side-by-side

Mouse controls:
- Press and hold left button then drag to rotate the camera/view
- Press and hold right button then drag to pan/translate the view
"""

import numpy as np

from motrixsim import SceneData, load_model
from motrixsim.render import RenderApp


def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/randomize/pendulum.xml"
        # Load the scene model
        model = load_model(path)

        # Create 16 instances in a 4x4 grid
        render_offset = []
        for i in range(4):
            for j in range(4):
                render_offset.append([-i * 2.5, j * 2.5, 0])

        # Create the render instance of the model
        render.launch(model, batch=16, render_offset=render_offset)

        # Create the physics data of the model
        data = SceneData(model, batch=(16,))

        # Get the pendulum hinge joint by name
        joint = model.get_joint("pendulum_hinge")

        # Generate frictionloss values ranging from no friction to high friction.
        #
        # Physics basis: gravity torque on this pendulum is τ(θ) = 193.7 × sin(θ) N·m.
        # At the 80° initial angle, τ ≈ 190.7 N·m. The upper bound of 200 N·m is chosen
        # to slightly exceed this critical torque so the last instance is completely frozen.
        frictionloss = np.linspace(0.0, 200.0, 16).astype(np.float32)
        joint.set_frictionloss_override(data, frictionloss)

        # Verify the override was applied correctly
        frictionloss_get = joint.get_frictionloss_override(data)
        assert np.allclose(frictionloss_get, frictionloss)

        # Print summary table
        print("\n" + "=" * 60)
        print("Frictionloss Randomization Summary")
        print("=" * 60)
        for i in range(16):
            val = frictionloss_get[i]
            if val < 30.0:
                behavior = "Free swinging"
            elif val < 160.0:
                behavior = "Dampened swinging"
            else:
                behavior = "Frozen at angle"
            print(f"Instance {i:2d}: frictionloss = {val:.1f} N·m -> {behavior}")
        print("=" * 60 + "\n")

        while True:
            model.step(data)
            render.sync(data)


if __name__ == "__main__":
    main()
