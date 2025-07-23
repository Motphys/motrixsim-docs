# 🔋 Actuators

Actuators are the core components responsible for controlling the motion of robot joints. MotrixSim supports multiple types of actuators.

Each actuator can be configured with different types and parameters to suit various application scenarios. Actuators can be motors, position controllers, velocity controllers, or general controllers. They enable precise control of the robot by setting target positions, velocities, or other parameters.

The currently supported actuator types are:

| Type             | Description                                                      |
| :--------------- | :-------------------------------------------------------------- |
| Motor            | Drives the robot's joints, providing basic actuation capability. |
| Position         | Precisely controls the joint angle or position.                  |
| Velocity         | Controls the joint's movement speed.                             |
| General          | Provides more flexible control, allowing custom control policies.|

Parameter settings are compatible with [MuJoCo actuator](https://mujoco.readthedocs.io/en/stable/XMLreference.html#actuator) attributes.

> Some attributes of the General actuator are not yet supported. Refer to the [support list](../getting_started/mjcf.md#actuator).

## Actuator Example

First, load the [`model`] and use the [`model.get_actuator`] method to obtain a specific [`Actuator`]. The argument can be the actuator's name or index. Then, set the control target value using the [`actuator.set_ctrl`] method.

The index corresponds to the order defined in the file. You can retrieve all actuator names using the [`model.actuator_names`] method.

Below is a complete code script covering all the above content:

```{literalinclude} ../../../../examples/actuator.py
:language: python
:dedent:
```

[`Actuator`]: motrixsim.Actuator
[`model`]: motrixsim.SceneModel
[`model.get_actuator`]: motrixsim.SceneModel.get_actuator
[`actuator.set_ctrl`]: motrixsim.Actuator.set_ctrl
[`model.actuator_names`]: motrixsim.SceneModel.actuator_names
