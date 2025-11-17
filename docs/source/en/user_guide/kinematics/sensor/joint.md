# Joint Sensor

Joint sensors are used to measure the position and velocity information of robot joints, and are core sensor types for robot control and status monitoring. They include joint position sensors (jointpos) and joint velocity sensors (jointvel).

## 🎯 Functional Description

Joint sensors directly measure the motion state of specified joints, including position and velocity information. Unlike sensors installed at spatial points, joint sensors are directly associated with joints, providing precise joint motion parameters.

### Sensor Types

1. **Joint Position Sensor (jointpos)**: Measures the current position or angle of the joint
2. **Joint Velocity Sensor (jointvel)**: Measures the current velocity or angular velocity of the joint

## 📋 Return Value Format

```python
# Joint position sensor
joint_position = model.get_sensor_value("jointpos_sensor", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 1)
# Unit: rad (rotary joint) or m (prismatic joint)

# Joint velocity sensor
joint_velocity = model.get_sensor_value("jointvel_sensor", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 1)
# Unit: rad/s (rotary joint) or m/s (prismatic joint)
```

## ⚙️ MJCF Configuration Parameters

In MotrixSim, joint sensors support the following MJCF configuration fields:

### Joint Position Sensor Configuration

```xml
<sensor>
    <jointpos name="sensor_name"
              joint="joint_name"/>
</sensor>
```

### Joint Velocity Sensor Configuration

```xml
<sensor>
    <jointvel name="sensor_name"
              joint="joint_name"/>
</sensor>
```

### Supported Attributes

| Attribute Name | Type   | Required | Default | Description                      |
| -------------- | ------ | -------- | ------- | -------------------------------- |
| **name**       | string | ✅       | -       | Unique identifier name of sensor |
| **joint**      | string | ✅       | -       | Name of joint to be measured     |

**Note**: MotrixSim currently does not support the `cutoff`, `noise`, and `user` attributes from the MJCF standard.

## 📝 Configuration Examples

### Basic Joint Sensor Configuration

```xml
<!-- Define joints -->
<joint name="shoulder_pitch" type="hinge" axis="0 1 0" range="-3.14 3.14"/>
<joint name="elbow" type="hinge" axis="0 1 0" range="0 3.14"/>
<joint name="wrist_slide" type="slide" axis="1 0 0" range="-0.5 0.5"/>

<!-- Joint position sensors -->
<sensor>
    <jointpos name="shoulder_pos" joint="shoulder_pitch"/>
    <jointpos name="elbow_pos" joint="elbow"/>
    <jointpos name="wrist_pos" joint="wrist_slide"/>
</sensor>

<!-- Joint velocity sensors -->
<sensor>
    <jointvel name="shoulder_vel" joint="shoulder_pitch"/>
    <jointvel name="elbow_vel" joint="elbow"/>
    <jointvel name="wrist_vel" joint="wrist_slide"/>
</sensor>
```

### Composite Joint Sensor Configuration

```xml
<!-- Configure position and velocity sensors for the same joint -->
<joint name="base_rotation" type="hinge" axis="0 0 1" limited="false"/>

<sensor>
    <jointpos name="base_rot_pos" joint="base_rotation"/>
    <jointvel name="base_rot_vel" joint="base_rotation"/>
</sensor>
```

## 🚀 Usage Examples

### Python API Usage

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# Load scene
model = load_model("robot_with_joint_sensors.xml")
data = SceneData(model)

# Run simulation and get joint sensor data
for step_count in range(1000):
    step(model, data)

    # Get joint positions
    shoulder_pos = model.get_sensor_value("shoulder_pos", data)
    elbow_pos = model.get_sensor_value("elbow_pos", data)

    # Get joint velocities
    shoulder_vel = model.get_sensor_value("shoulder_vel", data)
    elbow_vel = model.get_sensor_value("elbow_vel", data)

    # Handle single environment simulation data (shape is (1,))
    if shoulder_pos.ndim == 1:
        print(f"Shoulder joint angle: {np.degrees(shoulder_pos[0]):.1f}°")
        print(f"Elbow joint angle: {np.degrees(elbow_pos[0]):.1f}°")
        print(f"Shoulder joint velocity: {np.degrees(shoulder_vel[0]):.1f}°/s")
        print(f"Elbow joint velocity: {np.degrees(elbow_vel[0]):.1f}°/s")

    # Joint limit check
    if np.abs(shoulder_pos[0]) > np.radians(150):
        print("Warning: Shoulder joint approaching limit!")
```

### Practical Application Scenarios

```python
# Joint control (PD controller)
def joint_control_pd(current_pos, target_pos, current_vel, kp=10.0, kd=1.0):
    """Simple PD joint controller"""
    # Position error
    pos_error = target_pos - current_pos
    # Damping term
    damping = -kd * current_vel

    # Control torque
    control_signal = kp * pos_error + damping
    return control_signal

# Motion range monitoring
def monitor_joint_limits(joint_pos, joint_name, min_limit, max_limit):
    """Monitor if joint exceeds motion range"""
    pos = joint_pos[0] if joint_pos.ndim == 1 else joint_pos[0, 0]

    if pos < min_limit:
        print(f"Warning: {joint_name} below lower limit {np.degrees(min_limit):.1f}°")
        return False
    elif pos > max_limit:
        print(f"Warning: {joint_name} above upper limit {np.degrees(max_limit):.1f}°")
        return False
    return True

# Joint motion analysis
def analyze_joint_motion(position_history, velocity_history, window_size=10):
    """Analyze joint motion patterns"""
    if len(position_history) < window_size:
        return "Insufficient data", {}

    recent_positions = position_history[-window_size:]
    recent_velocities = velocity_history[-window_size:]

    # Average velocity
    avg_velocity = np.mean(recent_velocities)
    # Velocity variance
    velocity_variance = np.var(recent_velocities)
    # Motion range
    motion_range = np.max(recent_positions) - np.min(recent_positions)

    # Motion state determination
    if abs(avg_velocity) < 0.01 and velocity_variance < 0.01:
        motion_state = "Stationary"
    elif velocity_variance > 1.0:
        motion_state = "Variable speed motion"
    else:
        motion_state = "Uniform motion"

    analysis = {
        "state": motion_state,
        "avg_velocity": avg_velocity,
        "velocity_variance": velocity_variance,
        "motion_range": motion_range
    }

    return motion_state, analysis

# Trajectory tracking
def trajectory_tracking(current_pos, desired_trajectory, time_step, kp=50.0):
    """Trajectory tracking controller"""
    if time_step >= len(desired_trajectory):
        target_pos = desired_trajectory[-1]
    else:
        target_pos = desired_trajectory[time_step]

    # Simple P control
    error = target_pos - current_pos
    control_signal = kp * error

    return control_signal, target_pos
```

## 📊 Physical Principles

Joint sensors are based on rigid body kinematics principles:

1. **Direct measurement**: Directly measure the internal state of joints, no need to infer through spatial points
2. **Joint type adaptation**:
    - Rotary joint (hinge): Returns angle (rad) and angular velocity (rad/s)
    - Prismatic joint (slide): Returns displacement (m) and linear velocity (m/s)
3. **Single degree of freedom**: Each sensor measures one degree of freedom motion

## ⚠️ Important Notes

1. **Joint association**: Sensors must be associated with valid joints
2. **Unit attention**: Rotary joints use radians, prismatic joints use meters
3. **Data shape**: Return values are single-element arrays with shape `(*data.shape, 1)`
4. **No advanced attribute support**: MotrixSim currently does not support `cutoff`, `noise`, and `user` attributes
