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
OSC (Operational Space Control) Interactive Example

Demonstrates end-effector position and orientation control using OSC.

Controls:
- Arrow keys: Move target in XY plane
- W/S: Move target in Z
- Q/E: Rotate target yaw
- R: Reset goal to current pose
- ESC: Exit

This example shows how to use the OscSolver with IkChain to control a robot arm's
end-effector pose using computed torques.
"""

import numpy as np
from scipy.spatial.transform import Rotation

from motrixsim import SceneData, load_model, run, step
from motrixsim.ik import IkChain
from motrixsim.osc import OscSolver
from motrixsim.render import RenderApp


# - Press -> to move target +x
# - Press <- to move target -x
# - Press ^ to move target +y
# - Press v to move target -y
# - Press w to move target +z
# - Press s to move target -z
# - Press q to rotate target +yaw
# - Press e to rotate target -yaw
# - Press r to reset goal to current pose
def main():
    # Create render window for visualization
    with RenderApp() as render:
        # Load Stanford TidyBot model with torque control actuators
        path = "examples/assets/stanford_tidybot/scene_torque.xml"
        model = load_model(path)
        data = SceneData(model)

        # tag::create_osc_solver
        # Create IK chain for the 7-DOF arm
        chain = IkChain(
            model,
            end_link="base",
            start_link="gen3/base_link",
            end_effector_offset=np.array([0.0, 0.0, 0.15, 0, 0, 0, 1], dtype=np.float32),
        )

        # Create OSC solver (stateless)
        solver = OscSolver(
            control_ori=True,
            uncouple_pos_ori=True,
            kp=200.0,
            damping_ratio=1.0,
            nullspace_kp=10.0,
        )
        # end::create_osc_solver

        num_dof = chain.num_dof_vel
        print(f"OSC Chain: {num_dof} DOF")

        # Initialize and run FK
        step(model, data)

        # Initialize goal state (user manages this)
        # Get current end-effector pose
        ee_pose = chain.get_end_effector_pose(data)
        goal_pos = ee_pose[:3].copy()  # [x, y, z]
        goal_ori = np.array([0.0, 0.0, 0.0], dtype=np.float32)  # axis-angle (identity rotation)

        # Initialize nullspace target to current joint positions
        nullspace_target = chain.get_dof_pos(data).copy()

        # Set initial target pose (offset from current)
        target_pose = model.get_link("base").get_pose(data).copy()
        target_pose[0:3] += np.array([0.2, 0.0, -0.2])

        # Update goal to target
        goal_pos = target_pose[0:3].copy()
        goal_ori = Rotation.from_quat(target_pose[3:7]).as_rotvec().astype(np.float32)

        # Track time since last goal change
        steps_since_goal_change = 0
        torques_saturated = False

        # Local offset for end-effector (same as end_effector_offset in chain)
        local_ee_offset = np.array([0.0, 0.0, 0.15])

        # Helper function to apply local offset to base pose
        def get_ee_world_pos(base_pose):
            """Get end-effector world position from base link pose.

            Applies local_ee_offset in the base link's local frame.
            """
            base_pos = base_pose[0:3]
            base_quat = base_pose[3:7]
            # Transform local offset to world frame using base orientation
            world_offset = Rotation.from_quat(base_quat).apply(local_ee_offset)
            return base_pos + world_offset

        # UI elements
        input_mgr = render.input
        gizmos = render.gizmos

        print_controls()
        render.launch(model)

        def osc_control_and_step():
            nonlocal steps_since_goal_change, torques_saturated

            # OSC control loop:
            # 1. Compute torques using current goal
            # 2. Apply torques to actuators
            # 3. Step simulation

            # tag::solve_osc
            # Compute torques using OscSolver (stateless)
            torques = solver.solve(chain, goal_pos, goal_ori, nullspace_target, data)

            # Check for torque saturation (before clipping)
            torque_max_large = np.max(np.abs(torques[:4]))
            torque_max_small = np.max(np.abs(torques[4:]))
            torque_max = max(torque_max_large, torque_max_small)
            torques_saturated = torque_max_large > 105.0 or torque_max_small > 52.0

            # Apply torques to arm actuators
            # In stanford_tidybot model, the first 3 actuators are for the mobile base (position control),
            # actuators 3-9 are for the 7-DOF arm (torque control)
            ctrls = data.actuator_ctrls
            # Use Kinova Gen3 torque limits: large joints ±105 Nm, small joints ±52 Nm
            torques_clipped = np.clip(torques[:4], -105.0, 105.0).tolist() + np.clip(torques[4:], -52.0, 52.0).tolist()
            ctrls[3:10] = torques_clipped
            data.actuator_ctrls = ctrls

            # Step simulation AFTER applying controls
            step(model, data)
            # end::solve_osc

            # Calculate position error and other diagnostics
            current_pose = model.get_link("base").get_pose(data)
            # Get end-effector position in world frame (correctly applying local offset)
            current_pos = get_ee_world_pos(current_pose)
            target_pos = target_pose[0:3]
            pos_error = np.linalg.norm(current_pos - target_pos)

            # Get joint positions to check for limits
            dof_pos = data.dof_pos
            # In stanford_tidybot: first 3 DOF for mobile base, next 7 for arm
            arm_dof_start = 3
            _arm_qpos = dof_pos[arm_dof_start : arm_dof_start + 7]

            steps_since_goal_change += 1

            # Improved diagnostics with better thresholds
            # True singularity: very low torque (<5Nm) with large error (>20mm)
            is_singularity = pos_error > 0.02 and torque_max < 5.0
            # Slow convergence: moderate error persisting after many steps
            is_slow_convergence = pos_error > 0.01 and steps_since_goal_change > 1000
            # Good convergence: error < 10mm
            is_converged = pos_error < 0.01

            # Enhanced output with better diagnostics
            sat_indicator = " [SAT]" if torques_saturated else ""
            sing_indicator = " [SINGULARITY!]" if is_singularity else ""
            slow_indicator = " [SLOW]" if is_slow_convergence and not is_converged else ""
            converged_indicator = " [OK]" if is_converged else ""

            print(
                f"\rErr: {pos_error:.6f}m | Steps: {steps_since_goal_change:4d} | "
                f"Torque: {torque_max:6.1f}Nm | "
                f"Cur:[{current_pos[0]:.3f},{current_pos[1]:.3f},{current_pos[2]:.3f}] "
                f"Tgt:[{target_pos[0]:.3f},{target_pos[1]:.3f},{target_pos[2]:.3f}]"
                f"{sat_indicator}{sing_indicator}{slow_indicator}{converged_indicator}\033[K",
                end="",
                flush=True,
            )

        def render_step():
            nonlocal target_pose, goal_pos, goal_ori, steps_since_goal_change

            # Delta values for updating target_pose
            delta_pos = 0.002
            delta_ori = 0.5  # degrees

            # Flag to track if goal changed this frame
            goal_changed = False

            # Position control - update target_pose and goal
            if input_mgr.is_key_pressed("left"):
                target_pose[0] -= delta_pos
                goal_pos = target_pose[0:3].copy()
                goal_changed = True
            if input_mgr.is_key_pressed("right"):
                target_pose[0] += delta_pos
                goal_pos = target_pose[0:3].copy()
                goal_changed = True
            if input_mgr.is_key_pressed("up"):
                target_pose[1] += delta_pos
                goal_pos = target_pose[0:3].copy()
                goal_changed = True
            if input_mgr.is_key_pressed("down"):
                target_pose[1] -= delta_pos
                goal_pos = target_pose[0:3].copy()
                goal_changed = True
            if input_mgr.is_key_pressed("w"):
                target_pose[2] += delta_pos
                goal_pos = target_pose[0:3].copy()
                goal_changed = True
            if input_mgr.is_key_pressed("s"):
                target_pose[2] -= delta_pos
                goal_pos = target_pose[0:3].copy()
                goal_changed = True

            # Orientation control
            if input_mgr.is_key_pressed("q"):
                r = Rotation.from_quat(target_pose[3:7])
                r_delta = Rotation.from_euler("y", delta_ori, degrees=True)
                target_pose[3:7] = (r_delta * r).as_quat()
                goal_ori = Rotation.from_quat(target_pose[3:7]).as_rotvec().astype(np.float32)
                goal_changed = True
            if input_mgr.is_key_pressed("e"):
                r = Rotation.from_quat(target_pose[3:7])
                r_delta = Rotation.from_euler("y", -delta_ori, degrees=True)
                target_pose[3:7] = (r_delta * r).as_quat()
                goal_ori = Rotation.from_quat(target_pose[3:7]).as_rotvec().astype(np.float32)
                goal_changed = True

            # Reset to current pose
            if input_mgr.is_key_pressed("r"):
                base_pose = model.get_link("base").get_pose(data)
                # Set target to current end-effector position (correctly applying local offset)
                target_pose[0:3] = get_ee_world_pos(base_pose)
                target_pose[3:7] = base_pose[3:7]  # Keep orientation
                goal_pos = target_pose[0:3].copy()
                goal_ori = Rotation.from_quat(target_pose[3:7]).as_rotvec().astype(np.float32)
                goal_changed = True

            # Reset step counter when goal changes
            if goal_changed:
                steps_since_goal_change = 0

            # Draw target pose visualization (white cuboid + axes)
            gizmos.draw_cuboid(np.array([0.07, 0.07, 0.07]), target_pose[0:3], rot=target_pose[3:7])
            gizmos.draw_axes(target_pose[0:3], target_pose[3:7], length=0.1)

            render.sync(data)

        run.render_loop(model.options.timestep, 60, osc_control_and_step, render_step)


def print_controls():
    print("\n=== OSC Control Example (using OscSolver) ===")
    print("Controls:")
    print("  -> / <-  : Move target +x / -x")
    print("  ^ / v    : Move target +y / -y")
    print("  w / s    : Move target +z / -z")
    print("  q / e    : Rotate target +yaw / -yaw")
    print("  r        : Reset goal to current pose")
    print("\nDiagnostics:")
    print("  Err          : Position error from target")
    print("  Steps        : Steps since last goal change")
    print("  Torque       : Maximum torque magnitude")
    print("  [OK]         : Converged (error < 10mm)")
    print("  [SLOW]       : Slow convergence (>1000 steps, error >10mm)")
    print("  [SAT]        : Torque saturation (>105Nm or >52Nm)")
    print("  [SINGULARITY!]: True singularity (torque <5Nm, error >20mm)")
    print("")


if __name__ == "__main__":
    main()
