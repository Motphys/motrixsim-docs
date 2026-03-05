# 📚 Example Programs

:::{tip}
For models and code, see the [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) repository.

Before running the examples, please refer to {doc}`../overview/environment_setup` to complete the environment setup.
:::

We provide a series of example programs to help you master the use of MotrixSim from scratch.

**On all platforms** (Linux, Windows, MacOS), you can run any example of interest with:

```bash
uv run examples/{example_name}.py
```

````{note}
**Special note for MacOS (aarch64-apple-darwin) platform**:

- If the example uses {doc}`../main_function/render`, use:
  ```bash
  uv run mxpython examples/{example_name}.py
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
  - [`empty.py`](../../../../examples/empty.py)
  - Create an empty scene, equivalent to a Hello World example.
* - ![falling_ball](/_static/images/examples/falling_ball.png)
  - [`falling_ball.py`](../../../../examples/falling_ball.py)
  - A ball falls under gravity, demonstrating how to create a `model` and `data`.
```

## API Demonstrations

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![actuator](/_static/images/examples/actuator.png)
  - [`actuator.py`](../../../../examples/actuator.py)
  - Retrieve and configure `actuator` parameters.
* - ![body](/_static/images/examples/body.png)
  - [`body.py`](../../../../examples/body.py)
  - Usage of `body`-related APIs; here, `body` specifically refers to the root world body.
* - ![joint](/_static/images/examples/joint.png)
  - [`joint.py`](../../../../examples/joint.py)
  - Usage of `joint`-related APIs, including reading and writing `dof_position` and `dof_velocity`.
* - ![link](/_static/images/examples/link.png)
  - [`link.py`](../../../../examples/link.py)
  - Usage of `link`-related APIs.
* - ![model](/_static/images/examples/model.png)
  - [`model.py`](../../../../examples/model.py)
  - Usage of `model`-related APIs, including multi-instance scenarios for a single model.
* - ![options](/_static/images/examples/options.png)
  - [`options.py`](../../../../examples/options.py)
  - Configure simulator parameters using `options`.
* - ![site_and_sensor](/_static/images/examples/site_and_sensor.png)
  - [`site_and_sensor.py`](../../../../examples/site_and_sensor.py)
  - Usage of `site` and `sensor`-related APIs.
* - ![friction](/_static/images/examples/friction.png)
  - [`friction.py`](../../../../examples/friction.py)
  - Scene demonstrating friction configuration.
* - ![parallelsim](/_static/images/examples/parallelsim.png)
  - [`parallelsim.py`](../../../../examples/parallelsim.py)
  - Multi-environment parallel simulation.
* - ![inverse kinematics](/_static/images/examples/ik.png)
  - [`ik.py`](../../../../examples/ik.py)
  - Demonstrates how to use the built-in IK module in MotrixSim for inverse kinematics solving.
* - ![load_from_str](/_static/images/examples/load_from_str.jpg)
  - [`load_from_str.py`](../../../../examples/load_from_str.py)
  - Load an MJCF model from a string, demonstrating how to create a scene directly from an XML string.
* - ![combine_msd](/_static/images/examples/combine_msd.jpg)
  - [`combine_msd.py`](../../../../examples/combine_msd.py)
  - Combine multiple MSD models, demonstrating how to use the `Scene.attach()` method to attach multiple models together, supporting transforms and namespace prefixes.
* - ![geom](/_static/images/examples/geom.jpg)
  - [`geom.py`](../../../../examples/geom.py)
  - Usage of geometry-related APIs, showing how to access and query geometry position, velocity, and other information.
* - ![hfield](/_static/images/examples/hfield.jpg)
  - [`hfield.py`](../../../../examples/hfield.py)
  - Usage of height field APIs, demonstrating how to access terrain height data and perform statistical analysis.
* - ![camera_control](/_static/images/examples/change_camera_state.jpg)
  - [`camera_control.py`](../../../../examples/camera_control.py)
  - Camera control API usage, showing how to enable/disable system and scene cameras, and get camera poses.
* - ![custom_ui](/_static/images/examples/custom_ui.jpg)
  - [`custom_ui.py`](../../../../examples/custom_ui.py)
  - Usage of custom UI elements, demonstrating how to add buttons and switches for interaction.
```

## Interactive Control

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![keyboard_car](/_static/images/examples/keyboard_car.png)
  - [`keyboard_car.py`](../../../../examples/keyboard_car.py)
  - Control a cart using the keyboard; demonstrates keyboard event handling. Use W to move forward, S to move backward. Turning: A to turn left, D to turn right.
* - ![mouse_click](/_static/images/examples/mouse_click.png)
  - [`mouse_click.py`](../../../../examples/mouse_click.py)
  - Move a ball by clicking on the ground with the mouse; demonstrates mouse event handling.
* - ![gizmos](/_static/images/examples/gizmos.jpg)
  - [`gizmos.py`](../../../../examples/gizmos.py)
  - Usage of the 3D gizmo drawing system, demonstrating how to draw spheres, cubes, capsules, arrows, grids, and other visualization helpers.
```

## Physics Simulation

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![gyroscope](/_static/images/examples/gyroscope.png)
  - [`gyroscope.py`](../../../../examples/gyroscope.py)
  - Physical simulation of a gyroscope.
* - ![gyroscope_zero_gravity](/_static/images/examples/gyroscope_zero_gravity.png)
  - [`gyroscope_zero_gravity.py`](../../../../examples/gyroscope_zero_gravity.py)
  - Gyroscope in a zero-gravity environment, demonstrating conservation of angular momentum.
* - ![newton_cradle](/_static/images/examples/newton_cradle.png)
  - [`newton_cradle.py`](../../../../examples/newton_cradle.py)
  - Physical simulation of Newton's cradle.
* - ![slope](/_static/images/examples/slope.png)
  - [`slope.py`](../../../../examples/slope.py)
  - Simulation of a block rolling down a slope.
* - ![local_arm](/_static/images/examples/local_arm.png)
  - [`local_arm.py`](../../../../examples/local_arm.py)
  - A robotic arm composed of simple geometries and `joints`.
* - ![adhesion](/_static/images/examples/adhesion.png)
  - [`adhesion.py`](../../../../examples/adhesion.py)
  - A robotic arm with adhesion actuator.
```

## Robotics Applications

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![go1](/_static/images/poster/go1.jpg)
  - [`go1.py`](../../../../examples/go1.py)
  - Random motion of the Go1 quadruped robot, demonstrating how to integrate a neural network and use `.onnx` files.
* - ![go2](/_static/images/poster/go2_keyboard_control.jpg)
  - [`robot_locomotion.py`](../../../../examples/robot_locomotion.py)
  - Go2 quadruped keyboard control example: arrow keys and WASD control walking and turning. Use `uv run examples/robot_locomotion.py --robot go2` to run.
* - ![g1](/_static/images/poster/g1_keyboard_control.jpg)
  - [`robot_locomotion.py`](../../../../examples/robot_locomotion.py)
  - G1 humanoid keyboard control example: arrow keys and WASD control walking and turning. Use `uv run examples/robot_locomotion.py --robot g1` to run.
* - ![g1_parlour](/_static/images/poster/g1_parlour.jpg)
  - [`robot_locomotion.py`](../../../../examples/robot_locomotion.py)
  - G1 humanoid keyboard control example in an indoor parlour scene: arrow keys and WASD control walking and turning. Use `uv run examples/robot_locomotion.py --robot g1 --scene parlour` to run.
* - ![robotic_arm](/_static/images/examples/robotic_arm.png)
  - [`robotic_arm.py`](../../../../examples/robotic_arm.py)
  - The Stanford robotic arm uses a sequence of movement commands to pick and place a ball.
* - ![grasp_shaking_test](/_static/images/examples/grasp_shaking_test.jpg)
  - [`grasp_shaking_test.py`](../../../../examples/grasp_shaking_test.py)
  - Grasping and shaking test for the Franka Panda robotic arm, demonstrating how the arm grasps objects and maintains stability. Supports `--object` parameter to select object type (cube/ball/bottle), `--shake` parameter to control shaking, and `--record` parameter to record video.
```

## Rendering & Visualization

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![render_settings](/_static/images/examples/render_settings.jpg)
  - [`render_settings.py`](../../../../examples/render_settings.py)
  - Rendering settings configuration example, demonstrating how to use `RenderSettings` to configure shadows, screen-space ambient occlusion (SSAO), and other rendering effects.
* - ![partial_rendering](/_static/images/examples/partial_rendering.jpg)
  - [`partial_rendering.py`](../../../../examples/partial_rendering.py)
  - Selective rendering control in batch rendering, showing how to dynamically control visibility of specific scenes in multi-environment parallel simulation. Press A/D keys to toggle partial scene visibility, Q/E keys for all scenes.
* - ![share_lights_between_envs](/_static/images/examples/share_lights_between_envs.jpg)
  - [`share_lights_between_envs.py`](../../../../examples/share_lights_between_envs.py)
  - Light sharing optimization between environments, demonstrating how to share lights in parallel simulation to improve performance. Use `--share_lights=False` parameter to disable light sharing.
```
