# Touch Sensor

Touch sensors are used to detect contact and measure normal forces at specified site locations. In robot simulation, touch sensors are commonly used to implement tactile perception, collision detection, and force feedback control.

## 🎯 Functionality Description

Touch sensors measure the contact normal force experienced at the mounted site location. When other objects contact the sensor's detection area (defined by the site's shape and size), the sensor returns the magnitude of the normal force generated at the contact points.

### Core Features

1. **Location-Specific**: Detects contact at specific site locations
2. **Force Measurement**: Returns scalar values of contact normal force
3. **Shape-Aware**: Detection based on site's geometric shape
4. **Real-Time Response**: Provides contact force information at each simulation step

## 📋 Return Value Format

```python
touch_force = model.get_sensor_value("touch_sensor_name", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 1)
# Unit: N (Newtons)
```

-   **touch_force[..., 0]**: Contact normal force magnitude
-   **Value = 0**: No contact state
-   **Value > 0**: Contact present, value represents normal force magnitude

## ⚙️ MJCF Configuration Parameters

In MotrixSim, touch sensors support the following MJCF configuration fields:

### Basic Configuration

```xml
<sensor>
    <touch name="sensor_name"
          site="site_name"/>
</sensor>
```

### Supported Attributes

| Attribute Name | Type   | Required | Default | Description                               |
| -------------- | ------ | -------- | ------- | ----------------------------------------- |
| **name**       | string | ✅       | -       | Unique identifier name for the sensor     |
| **site**       | string | ✅       | -       | Name of the reference site for the sensor |

**Note**: MotrixSim currently does not support `cutoff`, `noise`, and `user` attributes from the MJCF standard.

## 📝 Configuration Examples

### Basic Touch Sensor Configuration

```xml
<!-- Define tactile detection point -->
<site name="palm_touch" type="sphere" size="0.05" rgba="1 0 1 1" pos="0 0 0"/>

<!-- Define touch sensor -->
<sensor>
    <touch name="palm_sensor" site="palm_touch"/>
</sensor>
```

### Cylinder Collision Detection Configuration (from touch_sensor_demo.xml)

```{literalinclude} ../../../../../examples/assets/touch_sensor_demo.xml
:language: xml
```

### Multiple Touch Sensor Configuration

```xml
<!-- Multiple tactile points on robot fingers -->
<site name="thumb_tip" pos="0.1 0 0.15" type="sphere" size="0.02" rgba="1 0 0 1"/>
<site name="index_tip" pos="0.05 0 0.18" type="sphere" size="0.02" rgba="0 1 0 1"/>
<site name="middle_tip" pos="0 0 0.18" type="sphere" size="0.02" rgba="0 0 1 1"/>

<!-- Corresponding touch sensors -->
<sensor>
    <touch name="thumb_touch" site="thumb_tip"/>
    <touch name="index_touch" site="index_tip"/>
    <touch name="middle_touch" site="middle_tip"/>
</sensor>
```

### Touch Sensors with Different Shapes

```xml
<!-- Spherical tactile sensor -->
<site name="sphere_touch" type="sphere" size="0.03" rgba="1 1 0 1" pos="0 0 0"/>

<!-- Capsule-shaped tactile sensor -->
<site name="capsule_touch" type="capsule" size="0.02 0.1" rgba="1 0 1 1" pos="0 0 0"/>

<!-- Cylindrical tactile sensor -->
<site name="cylinder_touch" type="cylinder" size="0.03 0.08" rgba="0 1 1 1" pos="0 0 0"/>

<sensor>
    <touch name="sphere_sensor" site="sphere_touch"/>
    <touch name="capsule_sensor" site="capsule_touch"/>
    <touch name="cylinder_sensor" site="cylinder_touch"/>
</sensor>
```

## 🚀 Usage Examples

### Python API Usage

For complete visualization examples, see [`examples/sensors/touch_sensor_demo.py`](../../../../../examples/sensors/touch_sensor_demo.py).

#### Basic Configuration and Sensor Data Retrieval

```{literalinclude} ../../../../../examples/sensors/touch_sensor_demo.py
:language: python
:dedent:
:start-after: "        # Scene file path"
:end-before: "        print(\"=== Touch Sensor Demo ===\")"
```

#### Sensor Data Reading and Visualization

```{literalinclude} ../../../../../examples/sensors/touch_sensor_demo.py
:language: python
:dedent:
:start-after: "            # Get all touch sensor data"
:end-before: "            # Sync render objects"
```

### Practical Application Scenarios

This example demonstrates a cylinder performing linear reciprocating motion along the x-axis, hitting a wall to test the feedback from the end touch sensor:

1. **Linear Motion Control**: Cylinder moves from -2 to 2, then returns, achieving reciprocating motion
2. **Real-Time Contact Detection**: When the cylinder end contacts the wall, the sensor detects pressure
3. **Visual Feedback**:
    - Red sphere shows sensor position
    - Yellow arrow length is proportional to contact force, intuitively displaying force magnitude
4. **Force Monitoring**: Console outputs contact force values in real-time

### Detection Process

1. **Contact Point Identification**: If a contact point is located within the touch sensor's site range, or if the normal direction of the contact point passes through the site, it is considered as valid contact
2. **Force Calculation**: Calculate normal force at each contact point
3. **Force Accumulation**: Sum normal forces from all contact points
4. **Return Result**: Return total normal force magnitude

## ⚠️ Important Notes

1. **Site Shape Importance**: The sensor's detection range is determined by the site's geometric shape and size
2. **Normal Force Measurement**: Only measures normal force, excluding tangential force components
3. **Force Accumulation**: Forces from multiple contact points are accumulated into a single scalar value
4. **No Advanced Attributes**: MotrixSim currently does not support `cutoff`, `noise`, and `user` attributes
5. **Data Type**: Return value is `numpy.ndarray` type, shape supports vectorized environments
6. **Zero Value Meaning**: Return value of 0 indicates no contact or negligible contact force
