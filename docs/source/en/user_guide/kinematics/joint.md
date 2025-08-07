# 🔩 Joint

A joint defines the degrees of freedom (DoF) between its associated rigid body ([Body](body.md)) and its parent body. Each rigid body can define multiple joints to combine various degrees of freedom. If a body does not define any joints, it is rigidly connected to its parent. Joints cannot be defined in the world body. The state data (position, velocity) of joints is stored in [SceneData](../main_function/scene_data.md). Since joints can define different numbers of DoF, the length of the state data varies accordingly.

## Joint Types

```{list-table}
   :header-rows: 1
   :widths: 15 15 15 10 45
   * - Type
     - DoF
     - Rotation Representation
     - Limits
     - Description
   * - Slide Joint
     - 1 translation
     - None
     - Configurable
     - Defined by joint position and sliding direction.
   * - Hinge Joint
     - 1 rotation
     - Angle
     - Configurable
     - Rotates about a specified axis and position; this is the default joint type.
   * - Ball Joint
     - 3 rotations
     - Quaternion
     - Configurable
     - Rotates about a specified point; can be combined with slide joints, but not with other ball or hinge joints simultaneously.
```

Unlike Mujoco, the `<freejoint>` element in an mjcf file is parsed as a [FloatingBase](floating_base.md) in MotrixSim.

## Configuration Example

Joints are configured via MJCF files. See [`examples/assets/joint.xml`](../../../../examples/assets/joint.xml) for reference.

[Explanation of MJCF joint-related tags](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-joint)

## API Usage Example

Load an MJCF file in MotrixSim to create a scene and data:

```{literalinclude} ../../../../examples/joint.py
:language: python
:dedent:
:start-after: "# tag::init[]"
:end-before:  "# end::init[]"
```

Access all joints in the scene:

```{literalinclude} ../../../../examples/joint.py
:language: python
:dedent:
:start-after: "# tag::access_all[]"
:end-before:  "# end::access_all[]"
```

Get joint index and access by joint name:

```{literalinclude} ../../../../examples/joint.py
:language: python
:dedent:
:start-after: "# tag::joint_index[]"
:end-before:  "# end::joint_index[]"
```

Get the value and velocity of the DoF associated with a joint:

```{literalinclude} ../../../../examples/joint.py
:language: python
:dedent:
:start-after: "# tag::joint_dof_pos_vel[]"
:end-before:  "# end::joint_dof_pos_vel[]"
```

Get joint limits:

```{literalinclude} ../../../../examples/joint.py
:language: python
:dedent:
:start-after: "# tag::joint_limits[]"
:end-before:  "# end::joint_limits[]"
```

Set joint position and velocity:

```{literalinclude} ../../../../examples/joint.py
:language: python
:dedent:
:start-after: "# tag::set_pos_vel[]"
:end-before:  "# end::set_pos_vel[]"
```

For the complete code, see [joint.py](../../../../examples/joint.py)

## API Reference

For more APIs related to Joint, see [`Joint API`]

[`Joint API`]: motrixsim.Joint
