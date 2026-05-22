# 🎲 Parameter Randomization

MotrixSim provides Domain Randomization capabilities, allowing you to set different physical parameters for each instance in multi-environment parallel simulations. This is essential for Sim-to-Real transfer and reinforcement learning training.

## Supported Randomization Parameters Overview

| Property       | Object       | Setter                        | Getter                        | Data Shape   |
| :------------- | :----------- | :---------------------------- | :---------------------------- | :----------- |
| Mass           | `Link`       | `set_mass_override`           | `get_mass_override`           | `(batch,)`   |
| Center of Mass | `Link`       | `set_center_of_mass_override` | `get_center_of_mass_override` | `(batch, 3)` |
| Friction       | `Geom`       | `set_friction_override`       | `get_friction_override`       | `(batch, 3)` |
| Geom Size      | `Geom*`      | `set_size_override`           | `get_size_override`           | `(batch, N)` |
| Armature       | `Joint`      | `set_armature_override`       | `get_armature_override`       | `(batch,)`   |
| Frictionloss   | `Joint`      | `set_frictionloss_override`   | `get_frictionloss_override`   | `(batch,)`   |
| Kp Gain        | `Actuator`   | `set_kp_override`             | `get_kp_override`             | `(batch,)`   |
| Damping (Kd)   | `Actuator`   | `set_damping_override`        | `get_kd_override`             | `(batch,)`   |
| Gravity        | `SceneModel` | `set_gravity_override`        | `get_gravity_override`        | `(batch, 3)` |

```{note}
All override methods act on `SceneData` and do not modify the `SceneModel` itself. This allows the same model to use different parameters across different instances.
```

## Core Concept

Parameter randomization is implemented through the **Override API**. Overrides act on `SceneData` rather than `SceneModel`, meaning different simulation instances of the same model can have different physical parameters without reloading the model.

Basic usage pattern:

```python
# Create batch simulation data
data = mtx.SceneData(model, batch=(16,))

# Get model object
link = model.get_link("body_name")

# Set override (shape includes batch dimension)
mass = np.random.uniform(0.1, 10.0, size=(16,))
link.set_mass_override(data, mass)

# Read override
mass_get = link.get_mass_override(data)
```

## Supported Randomization Parameters

### Link Parameters

#### Mass Randomization

Use `Link.set_mass_override` to modify link mass, affecting inertia and gravitational behavior.

```{figure} /_static/images/examples/randomize_mass.jpg
:width: 100%
:align: center
```

```{literalinclude} ../../../../examples/randomize/mass.py
:language: python
:dedent:
:lines: 27-47
```

Full example: [`examples/randomize/mass.py`](../../../../examples/randomize/mass.py)

#### Center of Mass Randomization

Use `Link.set_center_of_mass_override` to modify link center of mass position, affecting rotational behavior and stability.

```{figure} /_static/images/examples/randomize_com.jpg
:width: 100%
:align: center
```

```python
com_offset = np.zeros((16, 3), dtype=np.float32)
com_offset[:, 0] = np.random.uniform(-0.25, 0.25, 16)
link.set_center_of_mass_override(data, com_offset)
```

Full example: [`examples/randomize/com.py`](../../../../examples/randomize/com.py)

### Geometry Parameters

#### Friction Randomization

Use `Geom.set_friction_override` to modify geometry friction coefficients. The friction is a 3D vector `(slide, spin, roll)`.

```{figure} /_static/images/examples/randomize_friction.jpg
:width: 100%
:align: center
```

```python
geom = model.get_geom("box_geom")
frictions = np.zeros((16, 3), dtype=np.float32)
frictions[:, 0] = np.linspace(0.01, 2.0, 16)  # slide friction
geom.set_friction_override(data, frictions)
```

Full example: [`examples/randomize/friction.py`](../../../../examples/randomize/friction.py)

#### Geometry Size Randomization

Use the `set_size_override` method on geometry subclasses to modify collision shape sizes. Different geometry types have different size dimensions:

```{figure} /_static/images/examples/randomize_geom_size.jpg
:width: 100%
:align: center
```

| Geometry Type   | Size Dims | Meaning             |
| :-------------- | :-------- | :------------------ |
| `GeomSphere`    | 1         | Radius              |
| `GeomCapsule`   | 2         | Radius, half-height |
| `GeomCuboid`    | 3         | X/Y/Z half-extents  |
| `GeomCylinder`  | 2         | Radius, half-height |
| `GeomEllipsoid` | 3         | X/Y/Z semi-axes     |

```python
from motrixsim import GeomSphere

sphere = model.get_geom("sphere")
assert isinstance(sphere, GeomSphere)
radii = np.random.uniform(0.1, 0.8, size=(16, 1)).astype(np.float32)
sphere.set_size_override(data, radii)
```

Full example: [`examples/randomize/geom_size.py`](../../../../examples/randomize/geom_size.py)

### Joint Parameters

#### Armature Randomization

Use `Joint.set_armature_override` to modify joint armature (virtual rotor inertia), affecting joint dynamic response speed.

```{figure} /_static/images/examples/randomize_armature.jpg
:width: 100%
:align: center
```

```python
joint = model.get_joint("rotor_joint")
armature = np.linspace(0.1, 5.0, 16).astype(np.float32)
joint.set_armature_override(data, armature)
```

Full example: [`examples/randomize/armature.py`](../../../../examples/randomize/armature.py)

#### Joint Frictionloss Randomization

Use `Joint.set_frictionloss_override` to modify Coulomb dry friction at the joint, affecting joint resistance characteristics.

```{figure} /_static/images/examples/randomize_frictionloss.jpg
:width: 100%
:align: center
```

```python
joint = model.get_joint("pendulum_hinge")
frictionloss = np.linspace(0.0, 200.0, 16).astype(np.float32)
joint.set_frictionloss_override(data, frictionloss)
```

Full example: [`examples/randomize/frictionloss.py`](../../../../examples/randomize/frictionloss.py)

### Actuator Parameters

#### Kp/Kd Randomization

Use `Actuator.set_kp_override` and `Actuator.set_damping_override` to modify the proportional and derivative gains of position actuators.

```{figure} /_static/images/examples/randomize_actuator_kp_kd.jpg
:width: 100%
:align: center
```

```python
actuator = model.get_actuator("servo")
kp = np.array([10.0, 30.0, 60.0, 120.0], dtype=np.float32)
kd = np.array([1.0, 3.0, 8.0, 20.0], dtype=np.float32)
actuator.set_kp_override(data, kp)
actuator.set_damping_override(data, kd)
```

Full example: [`examples/randomize/actuator_kp_kd.py`](../../../../examples/randomize/actuator_kp_kd.py)

### Scene Parameters

#### Gravity Direction Randomization

Use `SceneModel.set_gravity_override` to modify the gravity vector for each instance.

```{figure} /_static/images/examples/randomize_gravity_direction.jpg
:width: 100%
:align: center
```

```python
gravity = np.random.randn(16, 3).astype(np.float32)
gravity /= np.linalg.norm(gravity, axis=1, keepdims=True)
gravity *= 9.81
model.set_gravity_override(data, gravity)
```

Full example: [`examples/randomize/gravity_direction.py`](../../../../examples/randomize/gravity_direction.py)
