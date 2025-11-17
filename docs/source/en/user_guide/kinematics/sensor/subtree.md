# Subtree Sensor

Subtree sensors are used to measure the overall physical characteristics of the kinematic subtree rooted at a specified rigid body, including center of mass position, center of mass linear velocity, and center of mass angular momentum. These sensors are very useful for analyzing the overall dynamic characteristics of complex mechanical systems.

## 🎯 Functional Description

Subtree sensors calculate the physical properties of the complete kinematic subtree with the specified body as the root node, with all results represented in the global coordinate system.

### Sensor Types

1. **Center of Mass Sensor (subtreecom)**: Measures the center of mass position of the subtree
2. **Center of Mass Linear Velocity Sensor (subtreelinvel)**: Measures the linear velocity of the subtree's center of mass
3. **Angular Momentum Sensor (subtreeangmom)**: Measures the angular momentum at the subtree's center of mass

## 📋 Return Value Format

```python
# Center of mass position sensor
subtree_com = model.get_sensor_value("subtreecom_sensor", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 3)
# Unit: m

# Center of mass linear velocity sensor
subtree_linvel = model.get_sensor_value("subtreelinvel_sensor", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 3)
# Unit: m/s

# Angular momentum sensor
subtree_angmom = model.get_sensor_value("subtreeangmom_sensor", data)
# Type: numpy.ndarray[float32]
# Shape: shape = (*data.shape, 3)
# Unit: kg·m²/s
```

## ⚙️ MJCF Configuration Parameters

In MotrixSim, subtree sensors support the following MJCF configuration fields:

### Basic Configuration

```xml
<sensor>
    <subtreecom name="sensor_name"
                body="root_body_name"/>
</sensor>
```

### Supported Attributes

| Attribute Name | Type   | Required | Default | Description                       |
| -------------- | ------ | -------- | ------- | --------------------------------- |
| **name**       | string | ✅       | -       | Unique identifier name of sensor  |
| **body**       | string | ✅       | -       | Name of body serving as root node |

**Note**: MotrixSim currently does not support the `cutoff`, `noise`, and `user` attributes from the MJCF standard.

## 📝 Configuration Examples

### Basic Subtree Sensor Configuration

```xml
<!-- Robot structure -->
<body name="torso" pos="0 0 1">
    <site name="torso_com" pos="0 0 0"/>

    <!-- Left arm -->
    <body name="left_shoulder" pos="0.2 0 0.5">
        <body name="left_elbow" pos="0.3 0 0">
            <body name="left_wrist" pos="0.25 0 0"/>
        </body>
    </body>

    <!-- Right arm -->
    <body name="right_shoulder" pos="-0.2 0 0.5">
        <body name="right_elbow" pos="-0.3 0 0">
            <body name="right_wrist" pos="-0.25 0 0"/>
        </body>
    </body>
</body>

<!-- Subtree sensors -->
<sensor>
    <!-- Entire robot (complete subtree with torso as root) -->
    <subtreecom name="robot_com" body="torso"/>
    <subtreelinvel name="robot_linvel" body="torso"/>
    <subtreeangmom name="robot_angmom" body="torso"/>

    <!-- Left arm subtree only -->
    <subtreecom name="left_arm_com" body="left_shoulder"/>
    <subtreelinvel name="left_arm_linvel" body="left_shoulder"/>

    <!-- Right arm subtree only -->
    <subtreecom name="right_arm_com" body="right_shoulder"/>
    <subtreeangmom name="right_arm_angmom" body="right_shoulder"/>
</sensor>
```

### Multi-level Subtree Monitoring

```xml
<!-- Complex mechanical structure -->
<body name="base" pos="0 0 0">
    <body name="main_arm" pos="1 0 1">
        <body name="forearm" pos="1 0 0">
            <body name="end_effector" pos="0.8 0 0">
                <!-- End effectors such as grippers -->
                <body name="finger1" pos="0.1 0.05 0"/>
                <body name="finger2" pos="0.1 -0.05 0"/>
            </body>
        </body>
    </body>
</body>

<!-- Multi-level subtree sensors -->
<sensor>
    <!-- Complete mechanical arm -->
    <subtreecom name="full_arm_com" body="main_arm"/>
    <subtreelinvel name="full_arm_vel" body="main_arm"/>

    <!-- Forearm subtree -->
    <subtreecom name="forearm_com" body="forearm"/>

    <!-- End effector subtree -->
    <subtreecom name="end_effector_com" body="end_effector"/>
    <subtreeangmom name="end_effector_angmom" body="end_effector"/>
</sensor>
```

## 🚀 Usage Examples

### Python API Usage

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# Load scene
model = load_model("robot_with_subtree_sensors.xml")
data = SceneData(model)

# Run simulation and get subtree sensor data
for step_count in range(1000):
    step(model, data)

    # Get overall robot center of mass
    robot_com = model.get_sensor_value("robot_com", data)
    if robot_com.ndim == 1:
        print(f"Robot center of mass position: [{robot_com[0]:.3f}, {robot_com[1]:.3f}, {robot_com[2]:.3f}] m")

    # Get overall robot center of mass velocity
    robot_vel = model.get_sensor_value("robot_linvel", data)
    if robot_vel.ndim == 1:
        speed = np.linalg.norm(robot_vel)
        print(f"Robot center of mass velocity: {speed:.3f} m/s")

    # Get angular momentum
    robot_angmom = model.get_sensor_value("robot_angmom", data)
    if robot_angmom.ndim == 1:
        angular_momentum = np.linalg.norm(robot_angmom)
        print(f"Robot angular momentum magnitude: {angular_momentum:.3f} kg·m²/s")

    # Get left and right arm center of mass positions
    left_arm_com = model.get_sensor_value("left_arm_com", data)
    right_arm_com = model.get_sensor_value("right_arm_com", data)
    if left_arm_com.ndim == 1 and right_arm_com.ndim == 1:
        arm_distance = np.linalg.norm(left_arm_com - right_arm_com)
        print(f"Left and right arm center of mass distance: {arm_distance:.3f} m")
```

### Practical Application Scenarios

```python
# Stability analysis
def stability_analysis(com_position, support_polygon):
    """Perform stability analysis based on center of mass position"""
    # Simplified here, actual implementation needs to determine if COM projection is within support polygon
    com_x, com_y = com_position[0], com_position[1]

    # Assume support area is rectangle [-0.2, 0.2] x [-0.2, 0.2]
    support_min, support_max = -0.2, 0.2

    if support_min <= com_x <= support_max and support_min <= com_y <= support_max:
        return "Stable"
    else:
        return "Unstable"

# Momentum conservation verification
def momentum_conservation_check(angmom_history, dt=0.01):
    """Check if angular momentum is conserved (without external forces)"""
    if len(angmom_history) < 2:
        return True, 0.0

    # Calculate angular momentum rate of change
    recent_angmom = np.array(angmom_history[-5:]) if len(angmom_history) >= 5 else np.array(angmom_history)

    # Calculate rate of change
    if len(recent_angmom) > 1:
        changes = np.diff(recent_angmom, axis=0) / dt
        max_change_rate = np.max(np.abs(changes))
        return max_change_rate < 0.1, max_change_rate  # Threshold adjustable

    return True, 0.0

# Subtree mass estimation
def estimate_subtree_mass(com_position, assumed_density=1000.0):
    """Estimate subtree mass based on center of mass position (simplified method)"""
    # This is just an example, actual implementation needs to calculate based on geometric shape and material density
    # Assume we know the subtree bounding box, can roughly estimate volume
    bounding_box_volume = 0.1  # Example value
    estimated_mass = bounding_box_volume * assumed_density
    return estimated_mass

# Collision detection and analysis
def collision_detection_subtree(com1, vel1, mass1, com2, vel2, mass2, threshold=0.5):
    """Simple collision detection based on subtree centers of mass"""
    # Calculate relative position and velocity
    relative_pos = com2 - com1
    relative_vel = vel2 - vel1
    distance = np.linalg.norm(relative_pos)

    if distance < threshold:
        # Calculate collision parameters
        normal = relative_pos / distance if distance > 0 else np.array([1, 0, 0])
        relative_speed = np.dot(relative_vel, normal)

        if relative_speed < 0:  # Approaching
            # Momentum analysis
            total_momentum = mass1 * vel1 + mass2 * vel2
            impulse_magnitude = 2 * relative_speed / (1/mass1 + 1/mass2)

            return {
                'collision': True,
                'distance': distance,
                'relative_speed': relative_speed,
                'impulse': impulse_magnitude,
                'normal': normal
            }

    return {'collision': False, 'distance': distance}

# Energy analysis
def energy_analysis_subtree(linvel, angmom, mass, inertia_tensor):
    """Subtree energy analysis"""
    # Kinetic energy calculation
    kinetic_energy_linear = 0.5 * mass * np.dot(linvel, linvel)
    kinetic_energy_angular = 0.5 * np.dot(angmom, np.linalg.solve(inertia_tensor, angmom))
    total_kinetic_energy = kinetic_energy_linear + kinetic_energy_angular

    return {
        'linear_ke': kinetic_energy_linear,
        'angular_ke': kinetic_energy_angular,
        'total_ke': total_kinetic_energy
    }
```

## 📊 Physical Principles

Subtree sensors are based on classical mechanics principles:

1. **Center of mass calculation**: Weighted average of mass and position of all objects in the subtree
2. **Linear velocity**: The velocity of the center of mass equals the total momentum of the subtree divided by total mass
3. **Angular momentum**: Angular momentum relative to the center of mass, considering rotation and translation of all objects

Center of mass calculation formula:

```
COM = (Σ(m_i * r_i)) / (Σ(m_i))
```

Angular momentum calculation formula:

```
L = Σ(r_i × p_i + I_i * ω_i)
```

Where r_i is the position relative to the center of mass, p_i is momentum, I_i is moment of inertia, and ω_i is angular velocity.

## ⚠️ Important Notes

1. **Subtree definition**: Subtree includes the specified body and its complete kinematic subtree of all descendants
2. **Global coordinate system**: All measurement results are represented in the global coordinate system
3. **Mass distribution**: Sensor accuracy depends on correct mass attribute definitions
4. **Dynamics constraints**: Subtree sensors are not directly affected by joint constraints
5. **No advanced attribute support**: MotrixSim currently does not support `cutoff`, `noise`, and `user` attributes
6. **Data type**: The return value is `numpy.ndarray` type, with shapes supporting vectorized environments
7. **Computational complexity**: Subtree sensors may involve complex calculations and have some impact on performance
