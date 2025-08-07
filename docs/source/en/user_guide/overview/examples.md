# 📚 Example Programs

:::{tip}
For models and code, see the [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) repository.

Before running the examples, please refer to {doc}`../overview/environment_setup` to complete the environment setup.
:::

We provide a series of example programs to help you master the use of MotrixSim from scratch. You can run any example of interest with:

```bash
pdm run examples/{example_name}.py
```

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
* - ![option](/_static/images/examples/option.png)
  - [`options.py`](../../../../examples/options.py)
  - Configure simulator parameters using `options`.
* - ![site_and_sensor](/_static/images/examples/site_and_sensor.png)
  - [`site_and_sensor.py`](../../../../examples/site_and_sensor.py)
  - Usage of `site` and `sensor`-related APIs.
* - ![friction](/_static/images/examples/friction.png)
  - [`friction.py`](../../../../examples/friction.py)
  - Scene demonstrating friction configuration.
```

## Interactive Control

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![read_keyboard](/_static/images/examples/read_keyboard.png)
  - [`read_keyboard.py`](../../../../examples/read_keyboard.py)
  - Control a cart using the keyboard; demonstrates keyboard event handling. Use W to move forward, S to move backward. Turning: A to turn left, D to turn right.
* - ![mouse_click](/_static/images/examples/mouse_click.png)
  - [`mouse_click.py`](../../../../examples/mouse_click.py)
  - Move a ball by clicking on the ground with the mouse; demonstrates mouse event handling.
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
```

## Robotics Applications

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40
* - **Preview**
  - **File**
  - **Description**
* - ![go1](/_static/images/examples/go1.png)
  - [`go1.py`](../../../../examples/go1.py)
  - Random motion of the Go1 quadruped robot, demonstrating how to integrate a neural network and use `.onnx` files.
* - ![robotic_arm](/_static/images/examples/robotic_arm.png)
  - [`robotic_arm.py`](../../../../examples/robotic_arm.py)
  - The Stanford robotic arm uses a sequence of movement commands to pick and place a ball.
```
