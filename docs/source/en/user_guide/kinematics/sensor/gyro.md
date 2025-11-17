# Gyroscope

The gyroscope sensor (gyro) is used to measure the three-axis angular velocity at the mounting point in the **local coordinate system**. In robot simulation, the gyroscope is a core sensor for attitude control and motion estimation, widely used in drones, robotic arms, mobile robots, and other fields.

## 🎯 Functional Description

The gyroscope measures the angular velocity at the sensor mounting point in the **site local coordinate system**. This sensor returns an array of 3 floating-point numbers, representing the angular velocity components rotating around the X, Y, and Z axes respectively.

## 📋 Return Value Format

```python
angular_velocity = model.get_sensor_value("gyro_name", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 3)
# Unit: rad/s
```

-   **angular_velocity[..., 0]**: Angular velocity rotating around X-axis (local coordinate system)
-   **angular_velocity[..., 1]**: Angular velocity rotating around Y-axis (local coordinate system)
-   **angular_velocity[..., 2]**: Angular velocity rotating around Z-axis (local coordinate system)

## ⚙️ MJCF Configuration Parameters

In MotrixSim, gyroscope sensors support the following MJCF configuration fields:

### Basic Configuration

```xml
<sensor>
    <gyro name="sensor_name"
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

### Basic Gyroscope Configuration

```xml
<!-- Define mounting point in body -->
<site name="robot_gyro" type="sphere" size="0.03" rgba="1 1 0 1" pos="0 0 0.1"/>

<!-- Define gyroscope sensor -->
<sensor>
    <gyro name="robot_gyro_sensor" site="robot_gyro"/>
</sensor>
```

### Multi-axis Gyroscope Configuration

```xml
<!-- Install gyroscopes for different components -->
<site name="base_gyro" pos="0 0 0" size="0.02"/>
<site name="arm_gyro" pos="1 0 0.5" size="0.02"/>

<sensor>
    <gyro name="base_angular_vel" site="base_gyro"/>
    <gyro name="arm_angular_vel" site="arm_gyro"/>
</sensor>
```

## 🚀 Usage Examples

### Python API Usage

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# Load scene
model = load_model("scene_with_gyro.xml")
data = SceneData(model)

# Run simulation and get gyroscope data
for step_count in range(1000):
    step(model, data)

    # Get gyroscope data
    gyro_data = model.get_sensor_value("robot_gyro_sensor", data)

    # If single environment simulation, data shape is (3,)
    if gyro_data.ndim == 1:
        print(f"Angular velocity: [{gyro_data[0]:.3f}, {gyro_data[1]:.3f}, {gyro_data[2]:.3f}] rad/s")

        # Calculate angular velocity magnitude
        angular_speed = np.linalg.norm(gyro_data)
        print(f"Angular velocity magnitude: {angular_speed:.3f} rad/s")

        # Convert to degrees/second
        angular_speed_deg = np.degrees(angular_speed)
        print(f"Angular velocity magnitude: {angular_speed_deg:.1f} °/s")
    else:
        # Vectorized environment case
        print(f"Angular velocity data shape: {gyro_data.shape}")
```

### Practical Application Scenarios

```python
# Attitude integration (simple Euler integration)
def integrate_attitude(angular_velocity, current_quat, dt=0.01):
    """Update attitude quaternion based on angular velocity integration"""
    # Convert angular velocity to quaternion rate of change
    omega = angular_velocity
    omega_magnitude = np.linalg.norm(omega)

    if omega_magnitude < 1e-6:
        return current_quat

    # Rotation axis
    axis = omega / omega_magnitude
    # Rotation angle
    angle = omega_magnitude * dt

    # Create incremental quaternion [w, x, y, z]
    half_angle = angle / 2
    dq = np.array([
        np.cos(half_angle),
        axis[0] * np.sin(half_angle),
        axis[1] * np.sin(half_angle),
        axis[2] * np.sin(half_angle)
    ])

    # Quaternion multiplication to update attitude
    return quaternion_multiply(dq, current_quat)

# Angular velocity threshold detection
def detect_rotation(angular_velocity, threshold=0.1):
    """Detect significant rotation"""
    angular_speed = np.linalg.norm(angular_velocity)
    return angular_speed > threshold

# Rotational motion analysis
def analyze_rotation_pattern(angular_velocity):
    """Analyze rotation pattern and main axis"""
    angular_speed = np.linalg.norm(angular_velocity)
    if angular_speed < 0.01:
        return "Stationary", None

    # Normalize angular velocity vector to get rotation axis
    rotation_axis = angular_velocity / angular_speed

    # Find main rotation axis
    max_component = np.argmax(np.abs(rotation_axis))
    axes = ['X-axis', 'Y-axis', 'Z-axis']
    main_axis = axes[max_component]

    return f"Rotating around {main_axis}", rotation_axis

def quaternion_multiply(q1, q2):
    """Quaternion multiplication"""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2

    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])
```

## 📊 Physical Principles

The gyroscope is based on rigid body rotational kinematics principles:

1. **Local coordinate system measurement**: The returned angular velocity values are represented in the site's local coordinate system
2. **Instantaneous angular velocity**: Provides instantaneous angular velocity information at the current moment

The angular velocity vector `ω = [ωx, ωy, ωz]` represents the rotation rate around each coordinate axis, and its magnitude `||ω||` is the overall rotation rate.

## ⚠️ Important Notes

1. **Local coordinate system**: The returned angular velocity values are represented in the site's local coordinate system, not the global coordinate system
2. **Attitude integration**: If attitude information is needed, integration of angular velocity is required, which can easily produce cumulative errors
3. **No advanced attribute support**: MotrixSim currently does not support `cutoff`, `noise`, and `user` attributes
4. **Data type**: The return value is `numpy.ndarray` type, with shapes supporting vectorized environments
5. **Singularity issues**: Numerical instability may occur in certain attitudes (such as gimbal lock)
