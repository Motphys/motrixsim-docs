# 🦾 Inverse Kinematics (IK)

MotrixSim provides an efficient and easy-to-use Inverse Kinematics (IK) solver located in the `motrixsim.ik` module. It supports two IK solvers: a Gauss-Newton-based solver ([`GaussNewtonSolver`]) and a Damped Least Squares (DLS) solver ([`DlsSolver`]), along with a simple IK chain model ([`IkChain`]).

```{video} /_static/videos/ik.mp4
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

## Basic Concepts

Inverse Kinematics (IK) is the process of calculating the joint parameters required to achieve a specific position and orientation of a robot's end-effector (e.g., a robotic arm's gripper). In contrast, Forward Kinematics calculates the position and orientation of the end-effector based on known joint parameters. The IK computation process can be expressed as: `joint_dof_pos = compute_inverse_kinematic(ik_model, end_effector_pose)`.

## IK Model

The IK model defines the structure and constraints of the IK problem. Currently, MotrixSim only supports chain structures (IKChain) composed of single-degree-of-freedom joints (Hinge, Slide).

### IK Chain

An IK chain model consists of a series of connected joints and an end-effector, as shown below:

![ikchain](/_static/images/ikchain.png)

In MotrixSim, you can create an IK chain model as follows:

```{literalinclude} ../../../../examples/ik.py
:language: python
:dedent:
:start-after: "# tag::create_ik_chain"
:end-before:  "# end::create_ik_chain"
```

The code above creates an IK chain model by specifying the end link and an optional starting link. You can also define the offset of the end-effector relative to the end link using the `end_effector_offset` parameter.

Refer to the API documentation for more details about [`IkChain`].

## IK Solver

After defining the IKModel, you can use an IK Solver to perform the actual IK solving. MotrixSim supports two IK solvers: the traditional Gauss-Newton solver [`GaussNewtonSolver`] and the more robust Damped Least Squares (DLS) solver [`DlsSolver`].

### Damped Least Squares (DLS) IK Solver

The Damped Least Squares (DLS) method is a robust optimization algorithm that adds regularization to handle singular configurations and improve numerical stability. It's particularly effective when dealing with near-singular Jacobian matrices or when the robot arm approaches singular configurations. DLS is also known as the Levenberg-Marquardt method when applied to IK problems.

**Key advantages:**

-   Better numerical stability near singular configurations
-   More consistent convergence behavior
-   Adjustable damping parameter for different scenarios

In MotrixSim, you can create a DLS IK solver as follows:

```{literalinclude} ../../../../examples/ik.py
:language: python
:dedent:
:start-after: "# tag::create_ik_solver"
:end-before:  "# end::create_ik_solver"
```

**Damping Parameter Tuning:**
The damping parameter is crucial for DLS performance:

-   **Small values (1e-6 to 1e-4)**: Near Gauss-Newton behavior, fast convergence when well-conditioned
-   **Medium values (1e-4 to 1e-2)**: Good balance for most applications, recommended starting point
-   **Large values (1e-2 to 1.0)**: More stable but slower convergence, useful near singularities

### Gauss-Newton IK Solver

The Gauss-Newton method is an iterative optimization algorithm for nonlinear least squares problems. It linearizes the nonlinear function and uses the least squares method to update parameter estimates, gradually approaching the target value. In IK solving, the Gauss-Newton method iteratively adjusts joint parameters to make the end-effector's position and orientation as close as possible to the target position and orientation.

The Gauss-Newton solver is simpler and may converge faster when the system is well-conditioned, but can struggle near singular configurations.

**When to use DLS vs Gauss-Newton:**

-   **Use DLS** when working near singular configurations, when numerical stability is important, or when you encounter convergence issues with Gauss-Newton
-   **Use Gauss-Newton** when you need maximum speed and the system is well-conditioned, away from singularities

Then, execute the IK solving process by calling the `solve` method:

```{literalinclude} ../../../../examples/ik.py
:language: python
:dedent:
:start-after: "# tag::solve_ik"
:end-before:  "# end::solve_ik"
```

The `solve` method returns a `numpy.ndarray` object with the shape `(*data.shape, chain.num_dof_pos + 2)`, where `chain.num_dof_pos` is the number of degrees of freedom in the IK chain. The additional two elements represent the solver's convergence status and the number of iterations.

```{note}
When using the IK Solver, it may sometimes fail to converge. Possible reasons include:

- The target position is outside the robot arm's workspace.
- The IK process does not consider constraints such as collisions.
- The initial pose of the robot arm is too far from the target, making it impossible to converge within the set number of iterations.
- For Gauss-Newton: The system is near a singular configuration where the Jacobian matrix becomes ill-conditioned.
- For DLS: The damping parameter might need adjustment for your specific use case.

**Tips for better convergence:**
- Use DLS solver when working near singular configurations
- Adjust the damping parameter based on your scenario (start with 1e-3)
- Ensure the target pose is reachable within the robot's workspace
- Consider breaking down large movements into smaller incremental steps
```

_See the complete code in [examples/ik.py](../../../../examples/ik.py)_

[`IkChain`]: motrixsim.ik.IkChain
[`GaussNewtonSolver`]: motrixsim.ik.GaussNewtonSolver
[`DlsSolver`]: motrixsim.ik.DlsSolver
