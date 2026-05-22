# 📚 Example Programs

:::{tip}
For models and code, see the [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) repository.

Before running the examples, please refer to {doc}`../overview/environment_setup` to complete the environment setup.
:::

We provide a series of example programs to help you master the use of MotrixSim from scratch.

**On all platforms** (Linux, Windows, MacOS), you can run any example of interest with:

```bash
uv run examples/{category}/{example_name}.py
```

````{note}
**Special note for MacOS (aarch64-apple-darwin) platform**:

- If the example uses {doc}`../main_function/render`, use:
  ```bash
  uv run mxpython examples/{category}/{example_name}.py
  ```

-   If the example **does not use** `RenderApp` (physics simulation only), use `uv run` which is consistent with other platforms

Most examples requiring visual rendering (such as robotic arm control, robot locomotion, etc.) use RenderApp and need `uv run mxpython`.

````

## Getting Started

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![empty](/_static/images/examples/empty.png)
  - [`empty.py`](../../../../examples/getting_started/empty.py)
  - Create an empty scene, equivalent to a Hello World example.
* - ![falling_ball](/_static/images/examples/falling_ball.png)
  - [`falling_ball.py`](../../../../examples/getting_started/falling_ball.py)
  - A ball falls under gravity, demonstrating how to create a `model` and `data`.
* - ![load_from_str](/_static/images/examples/load_from_str.jpg)
  - [`load_from_str.py`](../../../../examples/getting_started/load_from_str.py)
  - Load an MJCF model from a string, demonstrating how to create a scene directly from an XML string.
* - ![slope](/_static/images/examples/slope.png)
  - [`slope.py`](../../../../examples/getting_started/slope.py)
  - Simulation of a block rolling down a slope.
```

## Physics

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![actuator](/_static/images/examples/actuator.png)
  - [`actuator.py`](../../../../examples/physics/actuator.py)
  - Retrieve and configure `actuator` parameters.
* - ![body](/_static/images/examples/body.png)
  - [`body.py`](../../../../examples/physics/body.py)
  - Usage of `body`-related APIs; here, `body` specifically refers to the root world body.
* - ![joint](/_static/images/examples/joint.png)
  - [`joint.py`](../../../../examples/physics/joint.py)
  - Usage of `joint`-related APIs, including reading and writing `dof_position` and `dof_velocity`.
* - ![link](/_static/images/examples/link.png)
  - [`link.py`](../../../../examples/physics/link.py)
  - Usage of `link`-related APIs.
* - ![model](/_static/images/examples/model.png)
  - [`model.py`](../../../../examples/physics/model.py)
  - Usage of `model`-related APIs, including multi-instance scenarios for a single model.
* - ![options](/_static/images/examples/options.png)
  - [`options.py`](../../../../examples/physics/options.py)
  - Configure simulator parameters using `options`.
* - ![site_and_sensor](/_static/images/examples/site_and_sensor.png)
  - [`site_and_sensor.py`](../../../../examples/physics/site_and_sensor.py)
  - Usage of `site` and `sensor`-related APIs.
* - ![friction](/_static/images/examples/friction.png)
  - [`friction.py`](../../../../examples/physics/friction.py)
  - Scene demonstrating friction configuration.
* - ![geom](/_static/images/examples/geom.jpg)
  - [`geom.py`](../../../../examples/physics/geom.py)
  - Usage of geometry-related APIs, showing how to access and query geometry position, velocity, and other information.
* - ![hfield](/_static/images/examples/hfield.jpg)
  - [`hfield.py`](../../../../examples/physics/hfield.py)
  - Usage of height field APIs, demonstrating how to access terrain height data and perform statistical analysis.
* - ![combine_msd](/_static/images/examples/combine_msd.jpg)
  - [`combine_msd.py`](../../../../examples/physics/combine_msd.py)
  - Combine multiple MSD models, demonstrating how to use the `Scene.attach()` method to attach multiple models together, supporting transforms and namespace prefixes.
* - ![adhesion](/_static/images/examples/adhesion.png)
  - [`adhesion.py`](../../../../examples/physics/adhesion.py)
  - A robotic arm with adhesion actuator.
* - ![external_force](/_static/images/examples/external_force.jpg)
  - [`external_force.py`](../../../../examples/physics/external_force.py)
  - External force and torque application example, demonstrating how to use `add_external_force` and `add_external_torque` APIs to apply forces and torques to links in local coordinate frames. Includes three phases: center-of-mass thrust, Z-axis torque, and offset-point force.
```

## Control

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![keyboard_car](/_static/images/examples/keyboard_car.png)
  - [`keyboard_car.py`](../../../../examples/control/keyboard_car.py)
  - Control a cart using the keyboard; demonstrates keyboard event handling. Use W to move forward, S to move backward. Turning: A to turn left, D to turn right.
* - ![mouse_click](/_static/images/examples/mouse_click.png)
  - [`mouse_click.py`](../../../../examples/control/mouse_click.py)
  - Move a ball by clicking on the ground with the mouse; demonstrates mouse event handling.
* - ![inverse kinematics](/_static/images/examples/ik.png)
  - [`ik.py`](../../../../examples/control/ik.py)
  - Demonstrates how to use the built-in IK module in MotrixSim for inverse kinematics solving.
* - ![local_arm](/_static/images/examples/local_arm.png)
  - [`local_arm.py`](../../../../examples/control/local_arm.py)
  - A robotic arm composed of simple geometries and `joints`.
* - ![robotic_arm](/_static/images/examples/robotic_arm.png)
  - [`robotic_arm.py`](../../../../examples/control/robotic_arm.py)
  - The Stanford robotic arm uses a sequence of movement commands to pick and place a ball.
* - ![go1](/_static/images/poster/go1.jpg)
  - [`go1.py`](../../../../examples/control/go1.py)
  - Random motion of the Go1 quadruped robot, demonstrating how to integrate a neural network and use `.onnx` files.
* - ![go2](/_static/images/poster/go2_keyboard_control.jpg)
  - [`robot_locomotion.py`](../../../../examples/control/robot_locomotion.py)
  - Go2 quadruped keyboard control example: arrow keys and WASD control walking and turning. Use `uv run examples/control/robot_locomotion.py --robot go2` to run.
* - ![g1](/_static/images/poster/g1_keyboard_control.jpg)
  - [`robot_locomotion.py`](../../../../examples/control/robot_locomotion.py)
  - G1 humanoid keyboard control example: arrow keys and WASD control walking and turning. Use `uv run examples/control/robot_locomotion.py --robot g1` to run.
* - ![g1_motion_tracking](/_static/images/poster/g1_motion_tracking.png)
  - [`g1_motion_tracking.py`](../../../../examples/control/g1_motion_tracking.py)
  - G1 humanoid motion-tracking playback example. It loads the bundled reference motion and ONNX actor for single-environment playback. Use `uv run examples/control/g1_motion_tracking.py` to run.
* - ![g1_parlour](/_static/images/poster/g1_parlour.jpg)
  - [`robot_locomotion.py`](../../../../examples/control/robot_locomotion.py)
  - G1 humanoid keyboard control example in an indoor parlour scene: arrow keys and WASD control walking and turning. Use `uv run examples/control/robot_locomotion.py --robot g1 --scene parlour` to run.
* - ![rm65_open_cabinet](/_static/images/examples/rm65_open_cabinet.png)
  - [`rm65_open_cabinet.py`](../../../../examples/control/rm65_open_cabinet.py)
  - RM65 cabinet-opening policy example using an ONNX policy. [Demo video](/_static/videos/rm65_open_cabinet.mp4). Press `R` to reset and `ESC` to exit.
* - ![shadow_hand_repose](/_static/images/examples/shadow_hand_repose.jpg)
  - [`shadow_hand_repose.py`](../../../../examples/control/shadow_hand_repose.py)
  - Shadow Hand cube reorientation policy example using an ONNX policy. [Demo video](/_static/videos/shadow_hand_repose.mp4). Press `R` to reset and `ESC` to exit.
* - ![osc](/_static/images/examples/osc.jpg)
  - [`osc.py`](../../../../examples/control/osc.py)
  - Operational Space Control (OSC) interactive example, demonstrating how to use `OscSolver` with `IkChain` to control end-effector position and orientation via computed torques. Arrow keys and WASD to move target, Q/E to rotate, R to reset.
* - ![go1_multi_task](/_static/images/examples/go1_multi_task.jpg)
  - [`go1_multi_task.py`](../../../../examples/go1_multi_task.py)
  - Go1 quadruped multi-task policy example, supporting walking, handstand, footstand, and getup recovery mode switching. WASD to move, U for handstand, I for footstand, O for recovery, P to reset.
```

## Parallel Simulation

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![parallelsim](/_static/images/examples/parallelsim.png)
  - [`parallelsim.py`](../../../../examples/parallel/parallelsim.py)
  - Multi-environment parallel simulation.
```

## Randomization

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![randomize_mass](/_static/images/examples/randomize_mass.jpg)
  - [`mass.py`](../../../../examples/randomize/mass.py)
  - Randomize rigid body mass from 0.1 kg to 500 kg across 16 parallel instances, demonstrating how mass affects falling dynamics.
* - ![randomize_friction](/_static/images/examples/randomize_friction.jpg)
  - [`friction.py`](../../../../examples/randomize/friction.py)
  - Randomize per-geom friction coefficients from 0.01 to 2.0, demonstrating the transition from sliding to static grip on a 30° ramp.
* - ![randomize_armature](/_static/images/examples/randomize_armature.jpg)
  - [`armature.py`](../../../../examples/randomize/armature.py)
  - Randomize joint armature (virtual rotor inertia), showing how armature affects the natural frequency of a torsion-spring-driven arm.
* - ![randomize_frictionloss](/_static/images/examples/randomize_frictionloss.jpg)
  - [`frictionloss.py`](../../../../examples/randomize/frictionloss.py)
  - Randomize joint frictionloss (Coulomb dry friction) from 0 to 200 N·m, demonstrating how friction can freeze a pendulum at different angles.
* - ![randomize_com](/_static/images/examples/randomize_com.jpg)
  - [`com.py`](../../../../examples/randomize/com.py)
  - Randomize center of mass position within the cylinder cross-section, showing how COM offset affects rolling behavior.
* - ![randomize_actuator_kp_kd](/_static/images/examples/randomize_actuator_kp_kd.jpg)
  - [`actuator_kp_kd.py`](../../../../examples/randomize/actuator_kp_kd.py)
  - Randomize position actuator PD gains in a 4×4 grid with kp (10–120 N·m/rad) varying by row and kd (1–20 N·m·s/rad) by column, visualizing PD servo dynamics.
* - ![randomize_geom_size](/_static/images/examples/randomize_geom_size.jpg)
  - [`geom_size.py`](../../../../examples/randomize/geom_size.py)
  - Randomize collision and visual sizes of five geometry types (sphere, capsule, box, cylinder, ellipsoid), showing how size affects settling height and contact behavior.
* - ![randomize_gravity_direction](/_static/images/examples/randomize_gravity_direction.jpg)
  - [`gravity_direction.py`](../../../../examples/randomize/gravity_direction.py)
  - Randomize gravity direction by assigning each of 16 parallel instances a different gravity vector inside a transparent box, demonstrating per-instance gravity override with `set_gravity_override`.
```

## Viewer

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![camera_control](/_static/images/examples/change_camera_state.jpg)
  - [`camera_control.py`](../../../../examples/viewer/camera_control.py)
  - Camera control API usage, showing how to enable/disable system and scene cameras, and get camera poses.
* - ![camera_viewport](/_static/images/examples/camera_viewport.png)
  - [`camera_viewport.py`](../../../../examples/viewer/camera_viewport.py)
  - Camera viewport widgets displaying different camera feeds with interactive controls for switching cameras, resizing, and repositioning viewports.
* - ![custom_ui](/_static/images/examples/custom_ui.jpg)
  - [`custom_ui.py`](../../../../examples/viewer/custom_ui.py)
  - Usage of custom UI elements, demonstrating how to add buttons and switches for interaction.
* - ![gizmos](/_static/images/examples/gizmos.jpg)
  - [`gizmos.py`](../../../../examples/viewer/gizmos.py)
  - Usage of the 3D gizmo drawing system, demonstrating how to draw spheres, cubes, capsules, arrows, grids, and other visualization helpers.
* - ![image_widget](/_static/images/examples/image_widget.jpg)
  - [`image_widget.py`](../../../../examples/viewer/image_widget.py)
  - Image widget system usage, demonstrating how to display and interactively manipulate multiple image panels.
* - ![render_settings](/_static/images/examples/render_settings.jpg)
  - [`render_settings.py`](../../../../examples/viewer/render_settings.py)
  - Rendering settings configuration example, demonstrating how to use `RenderSettings` to configure shadows, screen-space ambient occlusion (SSAO), and other rendering effects.
* - ![partial_rendering](/_static/images/examples/partial_rendering.jpg)
  - [`partial_rendering.py`](../../../../examples/viewer/partial_rendering.py)
  - Selective rendering control in batch rendering, showing how to dynamically control visibility of specific scenes in multi-environment parallel simulation. Press A/D keys to toggle partial scene visibility, Q/E keys for all scenes.
* - ![share_lights_between_envs](/_static/images/examples/share_lights_between_envs.jpg)
  - [`share_lights_between_envs.py`](../../../../examples/viewer/share_lights_between_envs.py)
  - Light sharing optimization between environments, demonstrating how to share lights in parallel simulation to improve performance. Use `--share_lights=False` parameter to disable light sharing.
* - ![ssgi](/_static/images/poster/go2-ssgi.jpg)
  - [`ssgi.py`](../../../../examples/viewer/ssgi.py)
  - Screen Space Global Illumination (SSGI) rendering example, demonstrating how to use `RenderSettings` to enable high-quality SSGI rendering effects.
* - ![headless](/_static/images/examples/empty.png)
  - [`headless.py`](../../../../examples/viewer/headless.py)
  - Headless rendering example, demonstrating how to use `RenderApp(headless=True)` to run simulation without a window and batch-capture images via the system camera. Use `--no-wait` to switch between sync and async capture modes.
```

## Benchmark

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![gyroscope](/_static/images/examples/gyroscope.png)
  - [`gyroscope_mx.py`](../../../../examples/bench/gyroscope/gyroscope_mx.py)
  - Physical simulation of a gyroscope.
* - ![gyroscope_zero_gravity](/_static/images/examples/gyroscope_zero_gravity.png)
  - [`gyroscope_zero_gravity_mx.py`](../../../../examples/bench/gyroscope_zero_gravity/gyroscope_zero_gravity_mx.py)
  - Gyroscope in a zero-gravity environment, demonstrating conservation of angular momentum.
* - ![newton_cradle](/_static/images/examples/newton_cradle.png)
  - [`newton_cradle_mx.py`](../../../../examples/bench/newton_cradle/newton_cradle_mx.py)
  - Physical simulation of Newton's cradle.
* - ![grasp_shaking_test](/_static/images/examples/grasp_shaking_test.jpg)
  - [`shake_test_mx.py`](../../../../examples/bench/grasp/shake_test_mx.py)
  - Grasping and shaking test for the Franka Panda robotic arm, demonstrating how the arm grasps objects and maintains stability. Supports `--object` parameter to select object type (cube/ball/bottle), `--shake` parameter to control shaking, and `--record` parameter to record video.
```
