# 🔨 Model Building

MotrixSim provides a programmatic model building API that allows you to load, transform, and combine multiple models before simulation. This is useful for:

-   Combining robot models with different end-effectors
-   Creating multi-robot scenes
-   Dynamically assembling models at runtime

## Basic Concepts

The model building API is available through the [`motrixsim.msd`](../../api_reference/msd/msd.md) module:

| Class/Function                                           | Description                                                                          |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [`msd.from_file(path)`](motrixsim.msd.from_file)         | Load a model file (MJCF/URDF/MSD) and return a [`Scene`](motrixsim.msd.Scene) object |
| [`msd.from_str(string, format)`](motrixsim.msd.from_str) | Load a model from string                                                             |
| [`Scene.attach(other, ...)`](motrixsim.msd.Scene.attach) | Attach another model to this one                                                     |
| [`Scene.build()`](motrixsim.msd.Scene.build)             | Build the final [`SceneModel`](motrixsim.SceneModel) for simulation                  |

The [`Scene`](motrixsim.msd.Scene) object is a mutable representation of a model that can be transformed and combined before being compiled into an immutable [`SceneModel`](motrixsim.SceneModel).

## Basic Usage

### Loading and Building a Model

The simplest usage is to load a model file and build it:

```python
import motrixsim as mx

# Load and build in one chain
model = mx.msd.from_file("robot.xml").build()

# Or step by step
scene = mx.msd.from_file("robot.xml")
model = scene.build()
```

### Loading from String

You can also create a model from an MJCF/URDF string:

```python
import motrixsim as mx

mjcf_string = """
<mujoco>
  <worldbody>
    <body name="box">
      <geom type="box" size="0.1 0.1 0.1"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mx.msd.from_str(mjcf_string, format="mjcf").build()
```

## Combining Models

The `attach` method allows you to combine multiple models together:

```python
import motrixsim as mx

# Load two models
robot = mx.msd.from_file("robot.xml")
gripper = mx.msd.from_file("gripper.xml")

# Attach gripper to robot's hand link
robot.attach(
    gripper,
    self_link_name="hand",      # Link in robot to attach to
    other_prefix="gripper_",    # Prefix for gripper's names
    other_translation=[0.1, 0, 0]  # Offset
)

model = robot.build()
```

### Attach Parameters

| Parameter           | Type           | Description                                                     |
| ------------------- | -------------- | --------------------------------------------------------------- |
| `other`             | `Scene`        | The model to attach (cloned internally, can be reused)          |
| `self_link_name`    | `str`          | Link in this model to attach to. If `None`, merge at root level |
| `other_link_name`   | `str`          | Extract only this subtree from the other model                  |
| `other_translation` | `[x, y, z]`    | Translation offset for the attached model                       |
| `other_rotation`    | `[x, y, z, w]` | Rotation quaternion for the attached model                      |
| `other_prefix`      | `str`          | Prefix to add to all names in the attached model                |
| `other_suffix`      | `str`          | Suffix to add to all names in the attached model                |

### Creating Multiple Instances

Since `attach` clones the other model internally, you can attach the same model multiple times:

```python
import motrixsim as mx

scene = mx.msd.from_file("scene.xml")
robot = mx.msd.from_file("robot.xml")

# Create multiple robot instances at different positions
scene.attach(robot, other_prefix="robot1_", other_translation=[0, 0, 0])
scene.attach(robot, other_prefix="robot2_", other_translation=[2, 0, 0])
scene.attach(robot, other_prefix="robot3_", other_translation=[4, 0, 0])

model = scene.build()
```

### Extracting Subtrees

You can extract a specific subtree from a model before attaching:

```python
import motrixsim as mx

robot = mx.msd.from_file("robot.xml")
full_arm = mx.msd.from_file("arm_with_base.xml")

# Only attach the "forearm" subtree, not the entire arm model
robot.attach(
    full_arm,
    self_link_name="shoulder",
    other_link_name="forearm",  # Extract from this link
    other_prefix="arm_"
)

model = robot.build()
```

## Complete Example

Here's a complete example that creates a scene with multiple robots. For the full example, see [`examples/combine_msd.py`](../../../../examples/combine_msd.py).

```{literalinclude} ../../../../examples/combine_msd.py
:language: python
:start-after: "# tag::combine_msd_example[]"
:end-before: "# end::combine_msd_example[]"
```

## MJCF Attach Element

MotrixSim also supports the MJCF `<attach>` element for combining models in XML:

```xml
<mujoco>
  <asset>
    <model name="gripper" file="gripper.xml"/>
  </asset>
  <worldbody>
    <body name="robot">
      <!-- robot definition -->
      <body name="hand">
        <attach model="gripper" prefix="gripper_"/>
      </body>
    </body>
  </worldbody>
</mujoco>
```

For MJCF support details, see [MJCF Files](../getting_started/mjcf.md).

## API Reference

For detailed API documentation, see [`motrixsim.msd`](../../api_reference/msd/msd.md).
