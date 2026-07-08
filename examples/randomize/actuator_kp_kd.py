# Copyright (C) 2020-2026 Motphys Technology Co., Ltd. All Rights Reserved.
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
Position Actuator kp/kd Randomization Experiment

This example demonstrates how position actuator gains (kp and kd) affect the
servo behavior of a pendulum driven to a target angle.

Physical intuition:
- A position actuator applies torque: tau = kp * (target - pos) - kd * vel
- kp (proportional gain) controls the stiffness of the servo response.
  Higher kp -> faster convergence but more overshoot.
- kd (derivative gain) controls the damping.
  Higher kd -> less overshoot but slower response.

Layout (4x4 grid, 16 instances):
- Rows (top to bottom): increasing kp (10, 30, 60, 120 N*m/rad)
- Columns (left to right): increasing kd (1, 3, 8, 20 N*m*s/rad)

Expected behavior:
- Top-left (low kp, low kd): slow and oscillatory
- Top-right (low kp, high kd): slow, critically/over-damped
- Bottom-left (high kp, low kd): fast but very oscillatory
- Bottom-right (high kp, high kd): fast and well-damped

Key concepts:
- Actuator parameter override with set_kp_override / set_kd_override
- Per-instance randomization via batch data
- Visualizing the effect of PD gains on servo dynamics

Mouse controls:
- Press and hold left button then drag to rotate the camera/view
- Press and hold right button then drag to pan/translate the view
"""

import numpy as np

from motrixsim import PositionActuator, SceneData, load_model
from motrixsim.render import RenderApp

# Target angle for the servo (radians, ~45 degrees)
TARGET_ANGLE = 0.8


def main():
    with RenderApp() as render:
        path = "examples/assets/randomize/servo_pendulum.xml"
        model = load_model(path)

        # 4x4 grid layout
        n_rows, n_cols = 4, 4
        n_instances = n_rows * n_cols
        render_offset = []
        for row in range(n_rows):
            for col in range(n_cols):
                render_offset.append([-row * 3, col * 3, 0])

        render.launch(model, batch=n_instances, render_offset=render_offset)
        render.system_camera.set_view(lookat=[-4.5, 4.5, 0.5], distance=13.0, elevation=-25, azimuth=90)
        data = SceneData(model, batch=(n_instances,))

        actuator = model.get_actuator("servo")
        assert isinstance(actuator, PositionActuator), "Expected 'servo' actuator to be a PositionActuator"

        # Define kp and kd values for each axis
        kp_values = np.array([10.0, 30.0, 60.0, 120.0], dtype=np.float32)
        kd_values = np.array([1.0, 3.0, 8.0, 20.0], dtype=np.float32)

        # Build per-instance arrays: rows vary kp, columns vary kd
        kp_per_instance = np.repeat(kp_values, n_cols).astype(np.float32)
        kd_per_instance = np.tile(kd_values, n_rows).astype(np.float32)

        # Apply overrides
        actuator.set_kp_override(data, kp_per_instance)
        actuator.set_damping_override(data, kd_per_instance)

        # Verify
        assert np.allclose(actuator.get_kp_override(data), kp_per_instance)
        assert np.allclose(actuator.get_kd_override(data), kd_per_instance)

        # Set target angle for all instances (scalar is broadcast to all batches)
        actuator.set_ctrl(data, TARGET_ANGLE)

        # Print summary
        print("\n" + "=" * 70)
        print("Actuator kp/kd Randomization Summary")
        print("=" * 70)
        print(f"Target angle: {TARGET_ANGLE:.2f} rad ({np.degrees(TARGET_ANGLE):.1f} deg)")
        print(f"\n{'Instance':>10} {'kp':>8} {'kd':>8}  Expected behavior")
        print("-" * 60)
        for i in range(n_instances):
            kp = kp_per_instance[i]
            kd = kd_per_instance[i]
            row, col = divmod(i, n_cols)
            if kd < 5:
                damping = "oscillatory"
            elif kd < 12:
                damping = "moderate"
            else:
                damping = "well-damped"
            if kp < 20:
                speed = "slow"
            elif kp < 80:
                speed = "medium"
            else:
                speed = "fast"
            print(f"  [{row},{col}] {i:2d}  {kp:7.1f}  {kd:7.1f}  {speed}, {damping}")
        print("=" * 70 + "\n")

        while True:
            model.step(data)
            render.sync(data)


if __name__ == "__main__":
    main()
