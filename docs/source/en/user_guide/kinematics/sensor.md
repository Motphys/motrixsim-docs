# 🌡️ Sensor

By configuring sensors, users can more conveniently obtain the state information of physical objects, such as position, rotation, velocity, acceleration, etc. Sensors do not affect the results of the physical simulation and can be attached to different objects, such as bodies, sites, joints, etc.

## 📋 Sensor Overview Table

| Sensor Type            | Measured Object            | Coordinate System   | Return Dimensions | Main Applications                                                     |
| ---------------------- | -------------------------- | ------------------- | ----------------- | --------------------------------------------------------------------- |
| accelerometer          | site linear acceleration   | site local          | 3                 | motion perception, fall detection                                     |
| velocimeter            | site linear velocity       | site local          | 3                 | velocity monitoring, motion control                                   |
| gyro                   | site angular velocity      | site local          | 3                 | attitude control, motion estimation                                   |
| jointpos               | joint position/angle       | joint axis          | 1                 | position control, limit monitoring                                    |
| jointvel               | joint velocity             | joint axis          | 1                 | velocity control, motion monitoring                                   |
| framepos               | object position            | specified reference | 3                 | relative positioning, path tracking                                   |
| framequat              | object orientation         | specified reference | 4                 | attitude control, orientation monitoring                              |
| framexaxis/yaxis/zaxis | object axis                | specified reference | 3                 | direction analysis, alignment control                                 |
| framelinvel            | object linear velocity     | specified reference | 3                 | velocity tracking, motion analysis                                    |
| frameangvel            | object angular velocity    | specified reference | 3                 | angular velocity control, rotation monitoring                         |
| framelinacc            | object linear acceleration | specified reference | 3                 | acceleration monitoring, dynamic analysis                             |
| subtreecom             | subtree center of mass     | global              | 3                 | stability analysis, COM tracking                                      |
| subtreelinvel          | subtree COM velocity       | global              | 3                 | momentum analysis, motion monitoring                                  |
| subtreeangmom          | subtree angular momentum   | global              | 3                 | momentum conservation, rotation analysis                              |
| touch                  | site contact normal force  | site local          | 1                 | tactile perception, collision detection, force feedback               |
| contact                | geometric contact info     | local contact frame | variable          | ground contact detection, grasping force feedback, collision analysis |

## 🚀 Quick Start

### Sensor Configuration Example

Sensor configuration examples can be found in [`examples/assets/site_and_sensor.xml`](../../../../examples/assets/site_and_sensor.xml):

```xml
<sensor>
    <!-- Local coordinate system sensors -->
    <accelerometer name="acc_0" site="imu_0"/>
    <velocimeter name="vel_0" site="imu_0"/>
    <gyro name="gyro_0" site="imu_0"/>

    <!-- Joint sensors -->
    <jointpos name="joint_pos" joint="shoulder"/>
    <jointvel name="joint_vel" joint="shoulder"/>

    <!-- Reference frame sensors -->
    <framepos name="global_pos" objtype="body" objname="robot" reftype="world"/>

    <!-- Subtree sensors -->
    <subtreecom name="robot_com" body="torso"/>

    <!-- Contact sensors -->
    <touch name="palm_touch" site="palm_site"/>

    <!-- Contact sensor (detailed) -->
    <contact name="box_floor_contact" geom1="bar" geom2="freebox"
             data="found force pos normal tangent" num="4" reduce="none"/>
</sensor>
```

```{note}
**MotrixSim Limitation**: Currently does not support `cutoff`, `noise`, and `user` attributes from the MJCF standard
```

### Python API Usage

Get data from specified sensors:

```{literalinclude} ../../../../examples/site_and_sensor.py
:language: python
:dedent:
:start-after: "# tag::get_sensor_value[]"
:end-before:  "# end::get_sensor_value[]"
```

```{toctree}
:maxdepth: 1
:caption: Detailed Sensor Documentation

sensor/accelerometer
sensor/velocimeter
sensor/gyro
sensor/joint
sensor/frame
sensor/subtree
sensor/touch
sensor/contact
```
