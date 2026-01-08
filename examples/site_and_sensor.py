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

import numpy as np

from motrixsim import SceneData, load_model, run, step
from motrixsim.render import Color, RenderApp


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/site_and_sensor.xml"
        # Load the scene model
        model = load_model(path)
        # Create the render instance of the model
        render.launch(model)
        # Create the physics data of the model
        data = SceneData(model)

        # tag::site_access[]
        # ----------Try to access site----------
        # How many sites are in the model?
        num_sites = model.num_sites
        # Site objects
        sites = model.sites
        # Site names
        site_names = model.site_names
        print(f"num_sites : {num_sites}, sites : {sites}, site_names : {site_names}")

        # Get site by name
        car_imu = model.get_site("car_imu")
        print(f"car_imu's site index : {car_imu.index}")
        print(f"The car_imu site is on : [{car_imu.parent_link.name}] link")
        print(f"site_name of car_imu : {car_imu.name}")
        print(f"car_imu's local position : {car_imu.local_pos}")
        print(f"car_imu's local rotation : {car_imu.local_quat}")
        print(f"car_imu's world pose : {car_imu.get_pose(data)}")
        # ----------End----------
        # end::site_access[]
        # How many sensors are in the model?
        num_sensors = model.num_sensors
        print(f"num_sensors : {num_sensors}")

        # Set slide actuator control
        act = model.get_actuator("actuator_slider")
        act.set_ctrl(data, 1.0)

        # Set hinge joint velocity
        hinge = model.get_joint("hinge")
        hinge.set_dof_vel(data, np.array([3]))

        def render_step():
            # tag::get_sensor_value[]
            # Get sensor value directly
            v0 = (model.get_sensor_value("vel_0", data),)
            v1 = (model.get_sensor_value("vel_1", data),)
            v2 = (model.get_sensor_value("vel_2", data),)
            v3 = (model.get_sensor_value("vel_3", data),)
            (print(f"velocimeter values are : {v0}, {v1}, {v2}, {v3}"),)

            acc_0 = (model.get_sensor_value("acc_0", data),)
            acc_1 = (model.get_sensor_value("acc_1", data),)
            acc_2 = (model.get_sensor_value("acc_2", data),)
            acc_3 = (model.get_sensor_value("acc_3", data),)
            (print(f"accelerometer values are : {acc_0}, {acc_1}, {acc_2}, {acc_3}"),)

            gyro_0 = (model.get_sensor_value("gyro_0", data),)
            gyro_1 = (model.get_sensor_value("gyro_1", data),)
            gyro_2 = (model.get_sensor_value("gyro_2", data),)
            gyro_3 = (model.get_sensor_value("gyro_3", data),)
            (print(f"gyro values are : {gyro_0}, {gyro_1}, {gyro_2}, {gyro_3}"),)
            # end::get_sensor_value[]

            # tag::contact_sensor_gizmos[]
            # Get contact sensor data: [found, then 12 values per contact point]
            contact_data = model.get_sensor_value("box_floor_contact", data)
            num_contacts = int(contact_data[0])

            # Process each contact point
            for i in range(num_contacts):
                # Each contact has 12 values
                offset = 1 + i * 12

                # Extract force components (scalars, not vectors!)
                force_normal_mag = contact_data[offset + 0]  # Normal force magnitude
                force_tangent0_mag = contact_data[offset + 1]  # Tangent 0 force magnitude
                force_tangent1_mag = contact_data[offset + 2]  # Tangent 1 force magnitude

                # Extract contact position
                contact_pos = contact_data[offset + 3 : offset + 6]

                # Extract normal vector
                normal = contact_data[offset + 6 : offset + 9]

                # Extract first tangent vector
                tangent0 = contact_data[offset + 9 : offset + 12]

                # Compute second tangent vector: tangent1 = tangent0 × normal
                tangent1 = np.cross(tangent0, normal)

                # Scale force magnitudes for visualization
                force_scale = 0.01

                # Compute force vectors for visualization
                # Normal force vector (green arrow)
                normal_force_end = contact_pos + normal * force_normal_mag * force_scale

                # Tangent 0 force vector (red arrow)
                tangent0_force_end = contact_pos + tangent0 * force_tangent0_mag * force_scale

                # Tangent 1 force vector (blue arrow)
                tangent1_force_end = contact_pos + tangent1 * force_tangent1_mag * force_scale

                # Draw contact point (small white sphere)
                render.gizmos.draw_sphere(0.02, contact_pos, color=Color.rgb(1, 1, 1))

                # Draw normal force arrow (green - perpendicular to surface)
                render.gizmos.draw_arrow(contact_pos, normal_force_end, color=Color.rgb(0, 1, 0))

                # Draw tangent 0 force arrow (red - friction direction 0)
                render.gizmos.draw_arrow(contact_pos + normal * 0.01, tangent0_force_end, color=Color.rgb(1, 0, 0))

                # Draw tangent 1 force arrow (blue - friction direction 1)
                render.gizmos.draw_arrow(contact_pos + normal * 0.01, tangent1_force_end, color=Color.rgb(0, 0, 1))
            # end::contact_sensor_gizmos[]

            (print("-----------------------------------------"),)
            render.sync(data)

        run.render_loop(model.options.timestep, 30, lambda: step(model, data), render_step)


if __name__ == "__main__":
    main()
