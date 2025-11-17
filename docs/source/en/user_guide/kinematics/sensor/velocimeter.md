# Velocimeter

The velocimeter sensor is used to measure the three-axis linear velocity at the mounting point in the **local coordinate system**. In robot simulation, velocimeters are commonly used to monitor the robot's motion speed and provide important data for velocity control and motion estimation.

## 🎯 Functional Description

The velocimeter measures the linear velocity at the sensor mounting point in the **site local coordinate system**. This sensor returns an array of 3 floating-point numbers, representing the velocity components in the X, Y, and Z axis directions respectively.

## 📋 Return Value Format

```python
velocity = model.get_sensor_value("velocimeter_name", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 3)
# Unit: m/s
```

-   **velocity[..., 0]**: X-axis velocity component (local coordinate system)
-   **velocity[..., 1]**: Y-axis velocity component (local coordinate system)
-   **velocity[..., 2]**: Z-axis velocity component (local coordinate system)

## ⚙️ MJCF Configuration Parameters

In MotrixSim, velocimeter sensors support the following MJCF configuration fields:

### Basic Configuration

```xml
<sensor>
    <velocimeter name="sensor_name"
                 site="site_name"/>
</sensor>
```

### Supported Attributes

| Attribute Name | Type   | Required | Default | Description                                     |
| -------------- | ------ | -------- | ------- | ----------------------------------------------- |
| **name**       | string | ✅       | -       | Unique identifier name of sensor                |
| **site**       | string | ✅       | -       | Name of reference point where sensor is mounted |

**Note**: MotrixSim currently does not support the `cutoff`, `noise`, and `user` attributes from the MJCF standard.

## 📝 Configuration Examples

### Basic Velocimeter Configuration

```xml
<!-- Define mounting point in body -->
<site name="car_vel_sensor" type="sphere" size="0.03" rgba="1 0 1 1" pos="0 0 0"/>

<!-- Define velocimeter sensor -->
<sensor>
    <velocimeter name="car_velocimeter" site="car_vel_sensor"/>
</sensor>
```

### Multiple Velocimeter Configuration

```xml
<!-- Install multiple velocimeters at different positions -->
<site name="vel_base" pos="0 0 0" size="0.02"/>
<site name="vel_end_effector" pos="1 0 0" size="0.02"/>

<sensor>
    <velocimeter name="vel_base" site="vel_base"/>
    <velocimeter name="vel_end" site="vel_end_effector"/>
</sensor>
```

## 🚀 Usage Examples

### Python API Usage

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# Load scene
model = load_model("scene_with_velocimeter.xml")
data = SceneData(model)

# Run simulation and get velocimeter data
for step_count in range(1000):
    step(model, data)

    # Get velocimeter data
    vel_data = model.get_sensor_value("car_velocimeter", data)

    # If single environment simulation, data shape is (3,)
    if vel_data.ndim == 1:
        print(f"Velocity: [{vel_data[0]:.3f}, {vel_data[1]:.3f}, {vel_data[2]:.3f}] m/s")

        # Calculate velocity magnitude
        vel_magnitude = np.linalg.norm(vel_data)
        print(f"Velocity magnitude: {vel_magnitude:.3f} m/s")
    else:
        # Vectorized environment case
        print(f"Velocity data shape: {vel_data.shape}")
```

### Practical Application Scenarios

```python
# Velocity monitoring and limiting
def monitor_velocity(velocity, max_speed=5.0):
    """Monitor and check if velocity exceeds limits"""
    vel_magnitude = np.linalg.norm(velocity)
    if vel_magnitude > max_speed:
        print(f"Warning: Velocity {vel_magnitude:.2f} m/s exceeds maximum limit {max_speed} m/s")
    return vel_magnitude

# Displacement estimation (based on velocity integration)
def estimate_displacement(velocity_history, dt=0.01):
    """Estimate displacement based on velocity history"""
    if len(velocity_history) < 2:
        return np.zeros(3)

    displacement = np.zeros(3)
    for i in range(1, len(velocity_history)):
        # Simple trapezoidal integration
        avg_vel = (velocity_history[i] + velocity_history[i-1]) / 2
        displacement += avg_vel * dt

    return displacement

# Motion direction analysis
def analyze_motion_direction(velocity):
    """Analyze main motion direction"""
    vel_magnitude = np.linalg.norm(velocity)
    if vel_magnitude < 0.01:  # Stationary threshold
        return "Stationary"

    # Normalize velocity vector
    vel_norm = velocity / vel_magnitude

    # Determine main direction
    max_axis = np.argmax(np.abs(vel_norm))
    directions = ["X-axis", "Y-axis", "Z-axis"]
    return f"Main motion along {directions[max_axis]}"
```

## 📊 Physical Principles

The velocimeter measurement is based on rigid body kinematics principles:

1. **Local coordinate system measurement**: The returned velocity values are represented in the site's local coordinate system
2. **Linear velocity**: Only measures translational motion velocity, excluding rotational motion
3. **Instantaneous velocity**: Provides instantaneous velocity information at the current moment

For the velocity of a point on a rotating body, it can be calculated using rigid body kinematics formula:

```
v_point = v_center + ω × r_point_center
```

Where ω is the angular velocity, and r is the position vector relative to the center of mass.

## ⚠️ Important Notes

1. **Local coordinate system**: The returned velocity values are represented in the site's local coordinate system, not the global coordinate system
2. **Linear velocity only**: Measures linear velocity, excluding tangential velocity components caused by rotation
3. **Mounting position**: The sensor measures the linear velocity at the site mounting point position
4. **No advanced attribute support**: MotrixSim currently does not support `cutoff`, `noise`, and `user` attributes
5. **Data type**: The return value is `numpy.ndarray` type, with shapes supporting vectorized environments
6. **Velocity integration**: If displacement information is needed, integration of velocity is required, which may produce cumulative errors
