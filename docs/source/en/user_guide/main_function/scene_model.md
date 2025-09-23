# 🏗️ Model (SceneModel)

In MotrixSim, the model `SceneModel` and the data `SceneData` are essential components for building a simulation environment and are used throughout the entire physics simulation process. This chapter mainly introduces the creation and usage of `SceneModel`, while [`SceneData`](scene_data.md) will be described in detail in the next chapter.

## Basic Concepts

`SceneModel` describes the model, i.e., all **time-invariant quantities**. This includes geometric shapes, mass properties, joint connections, actuator configurations, and other static information. During the entire simulation, `SceneModel` remains unchanged, while all time-varying dynamic states (positions, velocities, forces, etc.) are stored in `SceneData`.

`SceneModel` mainly contains the following:

| Category              | Description                                                                                                                                                                                                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Components            | Joints [`Joint`](../kinematics/joint.md), Bodies [`Body`](../kinematics/body.md), Links [`Link`](../kinematics/link.md), Geomtries [`Geometry`](../kinematics/geometry.md), Sensors [`Sensor`](../kinematics/sensor.md), Actuators [`Actuator`](../kinematics/actuator.md), Sites [`Site`](../kinematics/site.md), etc. |
| Simulation Parameters | [`Options`](options.md) (including `timestep`, `gravity`, etc.)                                                                                                                                                                                                                                                         |

## Creating a Model

### Loading from File

The most common way is to create a model from an MJCF or URDF file:

```{literalinclude} ../../../../examples/empty.py
:language: python
:dedent:
:start-after: "# tag::load_model_from_file[]"
:end-before:  "# end::load_model_from_file[]"
```

For the complete example, see [`examples/empty.py`](../../../../examples/empty.py).

### Loading from String

You can also create a model directly from an MJCF string:

```{literalinclude} ../../../../examples/load_from_str.py
:language: python
:dedent:
:start-after: "# tag::model_load_from_string[]"
:end-before:  "# end::model_load_from_string[]"
```

For the complete example, see [`examples/load_from_str.py`](../../../../examples/load_from_str.py).

## Component Access (Named Access)

After creating a model, you often need to access its components to set parameters, retrieve information, or perform control. MotrixSim provides convenient named access interfaces for model components, supporting direct access to various components by **name** or **index**.

Below is an example of accessing a `joint` by name and index. For the complete example, see [`examples/joint.py`](../../../../examples/joint.py).

### Basic Access Methods

-   Access by **name**

```python
 hinge = model.get_joint("hinge")
```

-   Access by **index** (an interface for name-to-index conversion is also provided)

```{literalinclude} ../../../../examples/joint.py
:language: python
:dedent:
:start-after: "# tag::joint_index[]"
:end-before:  "# end::joint_index[]"
```

### Batch Access

In addition to accessing individual components, you can also retrieve lists of component objects or names in batch:

```{literalinclude} ../../../../examples/joint.py
:language: python
:dedent:
:start-after: "# tag::access_all[]"
:end-before:  "# end::access_all[]"
```

The access methods support the model components mentioned in [`Basic Concepts`]. For detailed access methods, see: [**API Quick Reference - Named Access**](../../api_reference/api_quick_reference.md#named-access-model-component-access).

## API Reference

For more APIs related to SceneModel, see [`SceneModel API`]

[`SceneModel API`]: motrixsim.SceneModel
[`Basic Concepts`]: #basic-concepts
