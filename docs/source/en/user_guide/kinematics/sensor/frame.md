# Frame Sensor

Frame sensors are used to measure the position, rotation, velocity, and acceleration information of objects in specified reference coordinate systems. These sensors provide more flexible measurement methods than local coordinate system sensors, allowing measurements relative to arbitrary reference points.

```{warning}
**Important: MotrixSim vs MuJoCo Quaternion Format Differences**

- **MotrixSim**: Uses **XYZW** format to store quaternions `[x, y, z, w]`
- **MuJoCo**: Uses **WXYZ** format to store quaternions `[w, x, y, z]`

This difference is critical! When using quaternions for attitude calculation or integration with other systems, format conversion must be performed, otherwise it will lead to calculation errors.
```

## 🎯 Functional Description

Frame sensors measure the state information of specified objects (body or site) relative to the reference coordinate system. The reference coordinate system can be the global coordinate system, or the local coordinate system of other bodies or sites.

### Sensor Types

1. **Position Sensors**:

    - `framepos`: Measures the position of the object in the reference coordinate system
    - `framequat`: Measures the rotation quaternion of the object in the reference coordinate system

2. **Axis Sensors**:

    - `framexaxis`: Measures the unit vector of the object's X-axis in the reference coordinate system
    - `frameyaxis`: Measures the unit vector of the object's Y-axis in the reference coordinate system
    - `framezaxis`: Measures the unit vector of the object's Z-axis in the reference coordinate system

3. **Velocity Sensors**:

    - `framelinvel`: Measures the linear velocity of the object in the reference coordinate system
    - `frameangvel`: Measures the angular velocity of the object in the reference coordinate system

4. **Acceleration Sensors**:
    - `framelinacc`: Measures the linear acceleration of the object in the reference coordinate system

## 📋 Return Value Format

```python
# Position sensor
frame_position = model.get_sensor_value("framepos_sensor", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 3)
# Unit: m

# Quaternion sensor
frame_quaternion = model.get_sensor_value("framequat_sensor", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 4)
# Format: [x, y, z, w] (MotrixSim format, note the difference from MuJoCo's [w, x, y, z] format)

# Axis sensor
frame_axis = model.get_sensor_value("framexaxis_sensor", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 3)

# Velocity sensor
linear_velocity = model.get_sensor_value("framelinvel_sensor", data)
angular_velocity = model.get_sensor_value("frameangvel_sensor", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 3)
# Unit: m/s (linear velocity), rad/s (angular velocity)

# Acceleration sensor
linear_acceleration = model.get_sensor_value("framelinacc_sensor", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 3)
# Unit: m/s²
```

## ⚙️ MJCF Configuration Parameters

In MotrixSim, frame sensors support the following MJCF configuration fields:

### Basic Configuration

```xml
<sensor>
    <framepos name="sensor_name"
              objtype="body"
              objname="object_name"
              reftype="body"
              refname="reference_name"/>
</sensor>
```

### Supported Attributes

| Attribute Name | Type   | Required | Default | Description                                                   |
| -------------- | ------ | -------- | ------- | ------------------------------------------------------------- |
| **name**       | string | ✅       | -       | Unique identifier name of sensor                              |
| **objtype**    | string | ✅       | -       | Measured object type ("body" or "site")                       |
| **objname**    | string | ✅       | -       | Measured object name                                          |
| **reftype**    | string | ✅       | -       | Reference coordinate system type ("body", "site", or "world") |
| **refname**    | string | ❓       | -       | Reference object name (required when reftype is not "world")  |

**Note**: MotrixSim currently does not support the `cutoff`, `noise`, and `user` attributes from the MJCF standard.

## 📝 Configuration Examples

### Measurement Relative to Global Coordinate System

```xml
<!-- Define objects to be measured -->
<body name="robot_arm" pos="1 0 0">
    <site name="end_effector" pos="2 0 0"/>
</body>

<!-- Sensors relative to global coordinate system -->
<sensor>
    <framepos name="arm_global_pos" objtype="body" objname="robot_arm"
               reftype="world"/>
    <framequat name="arm_global_quat" objtype="body" objname="robot_arm"
                reftype="world"/>
    <framelinvel name="arm_global_vel" objtype="body" objname="robot_arm"
                  reftype="world"/>
</sensor>
```

### Measurement Relative to Other Objects

```xml
<!-- Reference object -->
<body name="base_station" pos="0 0 0"/>
<!-- Moving object -->
<body name="mobile_robot" pos="2 1 0"/>

<!-- Sensors relative to reference station -->
<sensor>
    <framepos name="robot_relative_pos"
               objtype="body" objname="mobile_robot"
               reftype="body" refname="base_station"/>
    <framequat name="robot_relative_quat"
                objtype="body" objname="mobile_robot"
                reftype="body" refname="base_station"/>
</sensor>
```

### Measurement Relative to Site

```xml
<body name="robot_body">
    <site name="reference_site" pos="0 0 1"/>
    <site name="target_site" pos="1 0 0"/>
</body>

<!-- Target site state relative to reference_site -->
<sensor>
    <framepos name="target_relative_pos"
               objtype="site" objname="target_site"
               reftype="site" refname="reference_site"/>
    <framexaxis name="target_x_axis"
                 objtype="site" objname="target_site"
                 reftype="site" refname="reference_site"/>
</sensor>
```

## 🚀 Usage Examples

### Python API Usage

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# Load scene
model = load_model("scene_with_frame_sensors.xml")
data = SceneData(model)

# Run simulation and get frame sensor data
for step_count in range(1000):
    step(model, data)

    # Get global position
    global_pos = model.get_sensor_value("arm_global_pos", data)
    if global_pos.ndim == 1:
        print(f"Robot global position: [{global_pos[0]:.3f}, {global_pos[1]:.3f}, {global_pos[2]:.3f}] m")

    # Get global attitude (quaternion)
    global_quat = model.get_sensor_value("arm_global_quat", data)
    if global_quat.ndim == 1:
        # MotrixSim quaternion format: [x, y, z, w]
        print(f"Robot attitude quaternion (xyzw): [{global_quat[0]:.3f}, {global_quat[1]:.3f}, {global_quat[2]:.3f}, {global_quat[3]:.3f}]")

        # If conversion to MuJoCo format [w, x, y, z] is needed:
        mujoco_quat = np.array([global_quat[3], global_quat[0], global_quat[1], global_quat[2]])
        print(f"MuJoCo format quaternion (wxyz): [{mujoco_quat[0]:.3f}, {mujoco_quat[1]:.3f}, {mujoco_quat[2]:.3f}, {mujoco_quat[3]:.3f}]")

    # Get relative position
    relative_pos = model.get_sensor_value("robot_relative_pos", data)
    if relative_pos.ndim == 1:
        distance = np.linalg.norm(relative_pos)
        print(f"Relative distance: {distance:.3f} m")

    # Get axis information
    x_axis = model.get_sensor_value("target_x_axis", data)
    if x_axis.ndim == 1:
        print(f"Target X-axis direction: [{x_axis[0]:.3f}, {x_axis[1]:.3f}, {x_axis[2]:.3f}]")
```

### Practical Application Scenarios

```python
# Quaternion format conversion functions
def motrix_to_mujoco_quat(motrix_quat):
    """MotrixSim XYZW format to MuJoCo WXYZ format"""
    # MotrixSim: [x, y, z, w] -> MuJoCo: [w, x, y, z]
    return np.array([motrix_quat[3], motrix_quat[0], motrix_quat[1], motrix_quat[2]])

def mujoco_to_motrix_quat(mujoco_quat):
    """MuJoCo WXYZ format to MotrixSim XYZW format"""
    # MuJoCo: [w, x, y, z] -> MotrixSim: [x, y, z, w]
    return np.array([mujoco_quat[1], mujoco_quat[2], mujoco_quat[3], mujoco_quat[0]])

# Quaternion processing functions (adapted to MotrixSim's XYZW format)
def quaternion_to_euler(quat):
    """MotrixSim quaternion to Euler angles (XYZW format)"""
    x, y, z, w = quat  # Note: MotrixSim is XYZW format
    # Roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    # Pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = np.copysign(np.pi / 2, sinp)  # use 90 degrees if out of range
    else:
        pitch = np.arcsin(sinp)

    # Yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw

# Distance and direction analysis
def analyze_relative_position(relative_pos, threshold=2.0):
    """Analyze relative position relationship"""
    distance = np.linalg.norm(relative_pos)

    if distance < threshold:
        return "Close", distance

    # Calculate direction vector
    direction = relative_pos / distance

    # Determine main direction
    max_component = np.argmax(np.abs(direction))
    directions = ['+X', '+Y', '+Z', '-X', '-Y', '-Z']
    actual_direction = directions[max_component] if direction[max_component] > 0 else directions[max_component + 3]

    return f"Far (in {actual_direction} direction)", distance

# Attitude similarity calculation
def calculate_orientation_similarity(quat1, quat2):
    """Calculate similarity between two quaternions"""
    # Normalize quaternions
    quat1_norm = quat1 / np.linalg.norm(quat1)
    quat2_norm = quat2 / np.linalg.norm(quat2)

    # Calculate dot product
    dot_product = np.dot(quat1_norm, quat2_norm)

    # Ensure within valid range
    dot_product = np.clip(dot_product, -1.0, 1.0)

    # Calculate angle difference
    angle_diff = np.arccos(abs(dot_product))

    return np.degrees(angle_diff)

# Axis analysis
def analyze_axis_orientation(axis_vector):
    """Analyze the direction of axis orientation"""
    # Normalize vector
    axis = axis_vector / np.linalg.norm(axis_vector)

    # Angle with each coordinate axis
    x_angle = np.degrees(np.arccos(np.clip(axis[0], -1, 1)))
    y_angle = np.degrees(np.arccos(np.clip(axis[1], -1, 1)))
    z_angle = np.degrees(np.arccos(np.clip(axis[2], -1, 1)))

    return {
        'x_angle': x_angle,
        'y_angle': y_angle,
        'z_angle': z_angle,
        'dominant_axis': np.argmax(np.abs(axis))
    }
```

## 📊 Physical Principles

Frame sensors are based on coordinate transformation principles:

1. **Coordinate transformation**: Transform object attitude from its own coordinate system to the specified reference coordinate system
2. **Relative measurement**: Provide relative pose information between two objects
3. **Quaternion representation**: Use quaternions to avoid gimbal lock problems and provide stable attitude representation

Transformation formula:

```
T_ref = T_ref_to_world⁻¹ * T_obj_to_world
```

Where T represents homogeneous transformation matrices.

## ⚠️ Important Notes

1. **Reference coordinate system**: Must clearly specify the reference coordinate system type and name
2. **Object existence**: Measured objects and reference objects must exist in the scene
3. **Quaternion format difference**: MotrixSim uses **XYZW** format `[x, y, z, w]`, different from MuJoCo's WXYZ format `[w, x, y, z]`!
4. **Format conversion**: If MuJoCo compatibility is needed, quaternion format conversion is required: `mujoco_quat = [motrix_quat[3], motrix_quat[0], motrix_quat[1], motrix_quat[2]]`
5. **No advanced attribute support**: MotrixSim currently does not support `cutoff`, `noise`, and `user` attributes
6. **Data type**: The return value is `numpy.ndarray` type, with shapes supporting vectorized environments
7. **Reference system consistency**: Ensure consistency between reference coordinate system and object coordinate system
