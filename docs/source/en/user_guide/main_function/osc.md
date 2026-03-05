# 🎯 Operational Space Controller (OSC)

MotrixSim provides an Operational Space Controller (OSC) in the `motrixsim.osc` module. It exposes a single stateless solver class [`OscSolver`] that computes joint torques for task-space end-effector control.

## Basic Concepts

Operational Space Control (OSC) is a torque control method for robot manipulators. Unlike Inverse Kinematics, which computes joint _positions_ to achieve a desired end-effector pose, OSC computes joint _torques_ that account for the robot's full dynamics (inertia, Coriolis forces, gravity). The computation process can be expressed as: `joint_torques = compute_osc(osc_solver, ik_chain, end_effector_goal)`.

## IK Model

OSC reuses the same [`IkChain`] from `motrixsim.ik` to define the kinematic chain. An IK chain model consists of a series of connected joints and an end-effector, as shown below:

![ikchain](/_static/images/ikchain.png)

In MotrixSim, you can create an IK chain model as follows:

```{literalinclude} ../../../../examples/osc.py
:language: python
:dedent:
:start-after: "# tag::create_osc_solver"
:end-before:  "# end::create_osc_solver"
```

The code above creates an IK chain model by specifying the end link and an optional starting link. You can also define the offset of the end-effector relative to the end link using the `end_effector_offset` parameter.

Refer to the API documentation for more details about [`IkChain`].

## OSC Solver

After defining the IK chain, create an [`OscSolver`] to perform the actual torque computation. The solver is **stateless** — it holds no simulation state. You own the `IkChain` and the goal variables, updating them as needed each control step.

**Constructor parameters:**

| Parameter          | Type                 | Default | Description                                             |
| ------------------ | -------------------- | ------- | ------------------------------------------------------- |
| `control_ori`      | `bool`               | `True`  | Enable orientation control in addition to position      |
| `uncouple_pos_ori` | `bool`               | `True`  | Decouple position and orientation control               |
| `kp`               | `float` or `ndarray` | `150.0` | Stiffness gain for tracking the target                  |
| `damping_ratio`    | `float`              | `1.0`   | Damping ratio; `1.0` = critically damped (no overshoot) |
| `nullspace_kp`     | `float`              | `10.0`  | Stiffness gain for nullspace joint position control     |

Then, compute joint torques by calling the `solve` method:

```{literalinclude} ../../../../examples/osc.py
:language: python
:dedent:
:start-after: "# tag::solve_osc"
:end-before:  "# end::solve_osc"
```

The `solve` method returns a `numpy.ndarray` of shape `(*data.shape, num_dof)` containing the computed joint torques. You are responsible for applying these torques to the correct actuator indices in `data.actuator_ctrls`.

**`solve` parameters:**

| Parameter             | Shape                    | Description                                                                                               |
| --------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------- |
| `chain`               | —                        | `IkChain` defining the kinematic chain                                                                    |
| `ee_target_pos`       | `(*data.shape, 3)`       | Target end-effector position `[x, y, z]` in world frame                                                   |
| `ee_target_ori`       | `(*data.shape, 3)`       | Target orientation as axis-angle `[ax, ay, az]` (direction = rotation axis, magnitude = angle in radians) |
| `nullspace_joint_pos` | `(*data.shape, num_dof)` | Reference joint positions for nullspace control                                                           |
| `data`                | —                        | Current `SceneData` (supports batched multi-world simulation)                                             |

**Parameter tuning:**

**`kp` — stiffness gain**

Controls how aggressively the controller tracks the target. Higher values produce faster response but may cause oscillation or torque saturation.

-   **Small values (50–100)**: Soft, compliant behavior
-   **Medium values (150–200)**: Good balance for most applications, recommended starting point
-   **Large values (200–400)**: Stiff, fast tracking; watch for torque saturation

**`damping_ratio`**

Controls the velocity damping relative to `kp`.

-   **`1.0`**: Critically damped — recommended starting point, no overshoot
-   **`< 1.0`**: Underdamped — faster but may oscillate
-   **`> 1.0`**: Overdamped — slower but very stable

**`nullspace_kp`**

Drives joints toward `nullspace_joint_pos` without disturbing the end-effector task. Useful for keeping redundant joints away from limits. Set to `0.0` to disable. Typical range: `5–20`.

```{note}
When using the OSC Solver, you may encounter instability or poor tracking. Possible reasons include:

- The target position is outside the robot arm's reachable workspace.
- Torques saturate at actuator limits — reduce `kp` or increase `damping_ratio`.
- The robot is near a singular configuration — reduce `kp` or move the robot away from the singularity.

**Tips for better performance:**
- Start with `kp = 150.0` and `damping_ratio = 1.0`, then tune from there.
- Initialize `nullspace_joint_pos` to the robot's home configuration to keep joints away from limits.
- For batched (multi-world) simulation, all inputs must have a leading batch dimension matching `data.shape`.
- The solver computes torques for the chain's DOF only — map them to the correct indices in `data.actuator_ctrls` (see the example).
```

_See the complete code in [examples/osc.py](../../../../examples/osc.py)_

[`OscSolver`]: motrixsim.osc.OscSolver
[`IkChain`]: motrixsim.ik.IkChain
