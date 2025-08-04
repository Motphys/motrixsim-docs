# 🛸 Floating Base

In [Body](body.md), we introduced three types of connections between a Body and the World:

-   Fixed connection (Fixed)
-   Joint connection (Joint)
-   Free movement (FloatingBase)

For a freely moving Body, its base is considered floating, and it possesses a FloatingBase object. A FloatingBase has 3 translational and 3 rotational degrees of freedom. Through the floatingbase object, MotrixSim provides additional features and properties, allowing users to conveniently control and query the state of the floating base.

When simulating quadruped or humanoid robots, they typically have a floating base.

## MJCF Mapping

In MJCF, if a `<body>` element contains a `<freejoint>` element, MotrixSim will automatically parse it as a FloatingBase object. For more information about `<freejoint>` in MJCF, refer to the official documentation:
[freejoint](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-freejoint)

## Accessing FloatingBase

Generally, you can access the FloatingBase object as follows:

```python
# Get the Body object
cube = model.get_body('free_cube')
fb = cube.floatingbase
if fb is not None:
    # This body has a floating base
    # call some methods or properties on fb
    print(fb.get_translation(data))  # get position in global frame
    print(fb.set_translation(data, [1.0, 2.0, 3.0]))  # set position in global frame
```

```{note}
The FloatingBase object provides methods not available to ordinary Joints. For example, it allows direct setting of position, rotation, and velocity in Cartesian coordinates. MotrixSim will automatically convert these parameters from Cartesian to generalized coordinates and update [`data.dof_pos`] and [`data.dof_vel`].
Note that when you set position, rotation, or velocity using methods like [`floatingbase.set_translation`], MotrixSim only updates the dof data in Data. The kinematic state of the entire link tree will only be updated after you call `motrixsim.step` or `motrixsim.forward`.
```

## API Reference

For more APIs related to FloatingBase, see [`FloatingBase API`]

[`FloatingBase API`]: motrixsim.FloatingBase
[`data.dof_pos`]: motrixsim.SceneData.dof_pos
[`data.dof_vel`]: motrixsim.SceneData.dof_vel
[`floatingbase.set_translation`]: motrixsim.FloatingBase.set_translation
[`motrixsim.step`]: motrixsim.step
[`motrixsim.forward`]: motrixsim.forward
