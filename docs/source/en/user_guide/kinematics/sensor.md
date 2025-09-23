# 🌡️ Sensor

By configuring sensors, users can conveniently obtain the state information of physical objects, such as position, rotation, velocity, acceleration, and more. Sensors do not affect the results of the physical simulation and can be attached to different objects, such as bodies or sites. For configuration examples, see [`examples/assets/site_and_sensor.xml`](../../../../examples/assets/site_and_sensor.xml).

## Currently Supported Sensors

| Type                                     | Function                                                                            | Return Value              |
| :--------------------------------------- | :---------------------------------------------------------------------------------- | :------------------------ |
| Accelerometer                            | 3-axis accelerometer, measures linear acceleration at the mounting point            | `list[float]` <br> len: 3 |
| Velocimeter                              | 3-axis velocimeter, measures linear velocity at the mounting point                  | `list[float]` <br> len: 3 |
| Gyroscope                                | Measures angular velocity at the mounting point                                     | `list[float]` <br> len: 3 |
| Torque                                   | Measures torque at the mounting point                                               | `list[float]` <br> len: 3 |
| Joint Position (jointpos)                | Measures joint position or angle                                                    | `list[float]` <br> len: 1 |
| Joint Velocity (jointvel)                | Measures joint linear or angular velocity                                           | `list[float]` <br> len: 1 |
| Frame Position (framepos)                | Position of the reference frame in the global or specified frame                    | `list[float]` <br> len: 3 |
| Frame Quaternion (framequat)             | Quaternion rotation of the reference frame in the global frame                      | `list[float]` <br> len: 4 |
| Frame X Axis (framexaxis)                | X axis unit vector of the reference frame in the global frame                       | `list[float]` <br> len: 3 |
| Frame Y Axis (frameyaxis)                | Y axis unit vector of the reference frame in the global frame                       | `list[float]` <br> len: 3 |
| Frame Z Axis (framezaxis)                | Z axis unit vector of the reference frame in the global frame                       | `list[float]` <br> len: 3 |
| Frame Linear Velocity (framelinvel)      | Linear velocity of the reference frame in the global frame                          | `list[float]` <br> len: 3 |
| Frame Angular Velocity (frameangvel)     | Angular velocity of the reference frame in the global frame                         | `list[float]` <br> len: 3 |
| Frame Linear Acceleration (framelinacc)  | Linear acceleration of the reference frame in the global frame                      | `list[float]` <br> len: 3 |
| Frame Angular Acceleration (frameangacc) | Angular acceleration of the reference frame in the global frame                     | `list[float]` <br> len: 3 |
| Subtree Center of Mass (subtreecom)      | Center of mass of the kinematic subtree rooted at the specified body (global frame) | `list[float]` <br> len: 3 |
| Subtree Linear Velocity (subtreelinvel)  | Linear velocity of the subtree's center of mass (global frame)                      | `list[float]` <br> len: 3 |
| Subtree Angular Momentum (subtreeangmom) | Angular momentum at the subtree's center of mass (global frame)                     | `list[float]` <br> len: 3 |

## Related API Usage Examples

Get the sensor data for a specified "sensor_name":

```{literalinclude} ../../../../examples/site_and_sensor.py
:language: python
:dedent:
:start-after: "# tag::get_sensor_value[]"
:end-before:  "# end::get_sensor_value[]"
```

For the complete example code, see [`examples/site_and_sensor.py`](../../../../examples/site_and_sensor.py)
