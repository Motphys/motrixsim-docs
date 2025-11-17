# Accelerometer

The accelerometer sensor is used to measure the three-axis linear acceleration at the mounting point in the **local coordinate system**. In robot simulation, accelerometers are commonly used to perceive the robot's motion state and provide important feedback information for control algorithms.

## 🎯 Functional Description

The accelerometer measures the linear acceleration at the sensor mounting point in the **site local coordinate system**, including the influence of gravitational acceleration. This sensor returns an array of 3 floating-point numbers, representing the acceleration components in the X, Y, and Z axis directions respectively.

## 📋 Return Value Format

```python
acceleration = model.get_sensor_value("accelerometer_name", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 3)
# Unit: m/s²
```

-   **acceleration[..., 0]**: X-axis acceleration component (local coordinate system)
-   **acceleration[..., 1]**: Y-axis acceleration component (local coordinate system)
-   **acceleration[..., 2]**: Z-axis acceleration component (local coordinate system)

## ⚙️ MJCF Configuration Parameters

In MotrixSim, accelerometer sensors support the following MJCF configuration fields:

### Basic Configuration

```xml
<sensor>
    <accelerometer name="sensor_name"
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

### Basic Accelerometer Configuration

```xml
<!-- Define mounting point in body -->
<site name="car_imu" type="sphere" size="0.03" rgba="0 1 0 1" pos="0 0 0"/>

<!-- Define accelerometer sensor -->
<sensor>
    <accelerometer name="car_accelerometer" site="car_imu"/>
</sensor>
```

### Multiple Accelerometer Configuration

```xml
<!-- Install multiple accelerometers at different positions -->
<site name="imu_base" pos="0 0 0" size="0.02"/>
<site name="imu_end" pos="0 0 1" size="0.02"/>

<sensor>
    <accelerometer name="acc_base" site="imu_base"/>
    <accelerometer name="acc_end" site="imu_end"/>
</sensor>
```

## 🚀 Usage Examples

### Python API Usage

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# Load scene
model = load_model("scene_with_accelerometer.xml")
data = SceneData(model)

# Run simulation and get accelerometer data
for step_count in range(1000):
    step(model, data)

    # Get accelerometer data
    acc_data = model.get_sensor_value("car_accelerometer", data)

    # If single environment simulation, data shape is (3,)
    if acc_data.ndim == 1:
        print(f"Acceleration: [{acc_data[0]:.3f}, {acc_data[1]:.3f}, {acc_data[2]:.3f}] m/s²")

        # Calculate acceleration magnitude
        acc_magnitude = np.linalg.norm(acc_data)
        print(f"Acceleration magnitude: {acc_magnitude:.3f} m/s²")
    else:
        # Vectorized environment case
        print(f"Acceleration data shape: {acc_data.shape}")
```

### Practical Application Scenarios

```python
# Robot fall detection
def detect_fall(acceleration, threshold=15.0):
    """Detect fall based on accelerometer data"""
    acc_magnitude = np.linalg.norm(acceleration)
    return acc_magnitude > threshold

# Stationary detection (considering gravity)
def is_stationary(acceleration, gravity_threshold=9.5):
    """Detect if device is stationary (considering gravity influence)"""
    acc_magnitude = np.linalg.norm(acceleration)
    # When stationary, acceleration magnitude should be close to gravitational acceleration
    return abs(acc_magnitude - gravity_threshold) < 0.5

# Calculate tilt angle
def calculate_tilt_angle(acceleration):
    """Calculate device tilt angle based on accelerometer"""
    # Assume device is mainly affected by gravity
    gravity = np.array([0, 0, -9.81])

    # Normalize vectors
    acc_norm = acceleration / np.linalg.norm(acceleration)
    gravity_norm = gravity / np.linalg.norm(gravity)

    # Calculate angle
    cos_angle = np.dot(acc_norm, gravity_norm)
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))

    return np.degrees(angle)
```

## 📊 Physical Principles

The accelerometer measurement is based on Newton's second law. In the simulation environment:

1. **Local coordinate system measurement**: The returned acceleration values are represented in the site's local coordinate system
2. **Gravity influence**: When the sensor is stationary relative to the ground, it will measure the projection of gravitational acceleration in the local coordinate system
3. **Linear acceleration**: Measures the pure linear acceleration at the mounting point, excluding rotational components

For example, when a robot is tilted, even when stationary, the accelerometer will produce non-zero readings due to the projection of gravity in the local coordinate system.

## ⚠️ Important Notes

1. **Local coordinate system**: The returned acceleration values are represented in the site's local coordinate system, not the global coordinate system
2. **Gravity influence**: When stationary, the accelerometer will measure the projection of gravitational acceleration in the local coordinate system
3. **Mounting position**: The sensor measures the acceleration at the site mounting point position
4. **No advanced attribute support**: MotrixSim currently does not support `cutoff`, `noise`, and `user` attributes
5. **Data type**: The return value is `numpy.ndarray` type, with shapes supporting vectorized environments
