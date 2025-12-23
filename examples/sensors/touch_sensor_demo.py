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

r"""
Touch Sensor Demo Example

This example demonstrates how to use touch sensors to detect contact between a \
robot end-effector and environmental objects.
Includes the following features:
1. Robot arm motion control
2. Touch sensor data reading
3. Contact detection and force feedback
4. Visualization rendering

"""

import numpy as np

from motrixsim import SceneData, load_model, run, step
from motrixsim.render import Color, RenderApp


def main():
    """Main function: Touch sensor demo"""
    # Create render window
    with RenderApp() as render:
        # Scene file path
        path = "examples/assets/touch_sensor_demo.xml"

        # Load scene model
        model = load_model(path)

        # Launch renderer
        render.launch(model)

        # Create physics data
        data = SceneData(model)

        # Get actuator
        arm_act = model.get_actuator("arm_act")

        # Get touch sensor site position
        end_site = model.get_site("end")

        print("=== Touch Sensor Demo ===")
        print("Control Instructions:")
        print("- Automatic control of rigid body and wall collision, touch sensor detects contact force")
        print("- Red sphere represents touch sensor position")

        print("=" * 50)

        # Run simulation and get touch sensor data
        step_count = 0

        def control_and_step():
            nonlocal step_count

            # Physics world step
            step(model, data)
            step_count += 1

            # Linear motion control
            # Create linear reciprocating motion: from -2 to 2, then return
            cycle_time = 200.0  # Steps to complete one round trip
            cycle_position = (step_count % cycle_time) / cycle_time
            if cycle_position < 0.5:
                # Forward phase: from -2 to 2
                arm_control = -2.0 + cycle_position * 8.0
            else:
                # Return phase: from 2 to -2
                arm_control = 2.0 - (cycle_position - 0.5) * 8.0

            arm_act.set_ctrl(data, arm_control)

        def render_and_display():
            # Get all touch sensor data
            force_data = model.get_sensor_value("touch sensor", data)
            # Handle single environment simulation data (shape is (1,))
            force_value = force_data[0]
            if force_value > 0.0:
                # Output touch sensor data
                print("Touch force = ", force_value)

            # Get touch sensor position
            sensor_pose = end_site.get_pose(data)
            sensor_pos = sensor_pose[:3]  # Extract position part

            # Draw touch sensor position (red sphere)
            render.gizmos.draw_sphere(0.03, sensor_pos, color=Color.rgb(1, 0, 0))

            # When pressure is detected, draw arrow based on pressure value
            if force_value > 0.0:
                arrow_length = force_value * 0.002
                arrow_end = sensor_pos + np.array([arrow_length, 0, 0])  # Along positive x-axis
                render.gizmos.draw_arrow(
                    start=sensor_pos,
                    end=arrow_end,
                    color=Color.rgb(1, 1, 0),  # Yellow arrow
                )

            # Sync render objects
            render.sync(data)

        run.render_loop(model.options.timestep, 60, control_and_step, render_and_display)


if __name__ == "__main__":
    main()
