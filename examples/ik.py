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
from scipy.spatial.transform import Rotation

from motrixsim import SceneData, ik, load_model, step
from motrixsim.render import RenderApp


# - Press -> to move target +x
# - Press <- to move target -x
# - Press ^ to move target +y
# - Press v to move target -y
# - Press w to move target +z
# - Press s to move target -z
# - Press q to rotate target +yaw
# - Press e to rotate target -yaw
def main():
    # Create render window for visualization
    with RenderApp() as render:
        path = "examples/assets/stanford_tidybot/scene.xml"
        model = load_model(path)
        data = SceneData(model)
        # tag::create_ik_chain
        chain = ik.IkChain(
            model, end_link="base", start_link="gen3/base_link", end_effector_offset=[0.0, 0.0, 0.15, 0, 0, 0, 1]
        )
        # end::create_ik_chain

        # tag::create_ik_solver

        # Damped Least Squares (DLS) solver with robust numerical stability
        solver = ik.DlsSolver(
            max_iter=100,
            step_size=0.5,
            tolerance=1e-3,
            damping=1e-3,  # Key parameter for DLS - start with 1e-3 for most applications
        )

        # Alternative: use Gauss-Newton solver (faster but less stable near singularities)
        # solver = ik.GaussNewtonSolver(
        #     max_iter=100,
        #     step_size=0.5,
        #     tolerance=1e-3,
        # )

        # DLS Damping parameter tuning guide:
        # - damping=1e-5: Near Gauss-Newton behavior, fast convergence when well-conditioned
        # - damping=1e-3: Good balance for most applications (default)
        # - damping=1e-1: Very stable but slower, useful near singular configurations
        # end::create_ik_solver

        step(model, data)
        target_pose = model.get_link("base").get_pose(data)
        target_pose[0:3] += np.array([0.2, 0.0, -0.2])

        gizmos = render.gizmos
        input = render.input

        print("Press -> to move target +x")
        print("Press <- to move target -x")
        print("Press ^ to move target +y")
        print("Press v to move target -y")
        print("Press w to move target +z")
        print("Press s to move target -z")
        print("Press q to rotate target +yaw")
        print("Press e to rotate target -yaw")

        render.launch(model)
        while True:
            time.sleep(model.options.timestep)
            step(model, data)
            render.sync(data)
            if input.is_key_pressed("left"):
                target_pose[0] -= 0.002
            if input.is_key_pressed("right"):
                target_pose[0] += 0.002
            if input.is_key_pressed("up"):
                target_pose[1] += 0.002
            if input.is_key_pressed("down"):
                target_pose[1] -= 0.002
            if input.is_key_pressed("w"):
                target_pose[2] += 0.002
            if input.is_key_pressed("s"):
                target_pose[2] -= 0.002
            if input.is_key_pressed("q"):
                r = Rotation.from_quat(target_pose[3:7])
                r2 = Rotation.from_euler("y", 0.5, degrees=True)
                r_new = r2 * r
                target_pose[3:7] = r_new.as_quat()
            if input.is_key_pressed("e"):
                r = Rotation.from_quat(target_pose[3:7])
                r2 = Rotation.from_euler("y", -0.5, degrees=True)
                r_new = r2 * r
                target_pose[3:7] = r_new.as_quat()

            gizmos.draw_cuboid(np.array([0.07, 0.07, 0.07]), target_pose[0:3], rot=target_pose[3:7])
            gizmos.draw_axes(target_pose[0:3], target_pose[3:7], length=0.1)

            # tag::solve_ik
            result = solver.solve(chain, data, target_pose)
            # the first element is actual iteration number used, which may be less than max_iter
            num_iter = result[0]  # noqa: F841
            # the second element is the final residual after iteration end.
            residual = result[1]
            # the remaining elements are the desired dof_pos
            desired_dof_pos = result[2:]

            # Check convergence: residual < tolerance means successful convergence
            if residual < 1e-3:
                # in stanford_tidybot model, the first 3 actuators are for the mobile base,
                # we only need to control the arm dof_pos.
                ctrls = data.actuator_ctrls
                ctrls[3:10] = desired_dof_pos
                data.actuator_ctrls = ctrls
            else:
                # DLS typically provides better convergence than Gauss-Newton,
                # but if you still see convergence issues, try:
                # 1. Increasing damping parameter (e.g., 1e-2)
                # 2. Breaking down large movements into smaller steps
                # 3. Checking if target is within robot workspace
                print(f"IK not converged: iterations={num_iter:.0f}, residual={residual:.2e}")
                print("Tips: increase damping, use smaller steps, or check workspace limits")

            # end::solve_ik


if __name__ == "__main__":
    main()
