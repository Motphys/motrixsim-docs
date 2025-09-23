# 🔷 Geometry

Geometry determines the appearance and collision properties of objects in the scene. Geometries can be added under `<body>` or `<worldbody>`, or used to configure default-related properties. [MJCF Geometry Configurable Attributes](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-geom)

## Geometry Types

Currently supported geometry types are as follows:
| Type | Description |
| :-----------------| :-------------------------------------------------------------------------- |
| Plane (`plane`) | Infinite plane dividing the entire scene, can only be configured under `worldbody` or a static `body`. In the plane’s local coordinate system, the Z-axis is the normal direction. The region below the plane (−Z direction) is the collision area. The first two values of the `size` parameter are only for visualization and do not affect collision volume. |
| Height field (`hfield`) | Requires referencing an asset under the corresponding `hfield` tag. No need to configure the `size` attribute. For an example, see [`examples/assets/hfield.xml`](../../../../examples/assets/hfield.xml). |
| Sphere (`sphere`) | The `size` attribute has only 1 value, defining the radius of the sphere. |
| Capsule (`capsule`)| Can be regarded as composed of two hemispheres and a cylinder. The `size` consists of the radius of the hemispheres and the half-height of the cylinder. |
| Cylinder (`cylinder`)| The `size` consists of the radius of the circle and the half-height of the cylinder. |
| Box (`box`) | The `size` consists of the half-lengths along the X, Y, and Z directions. |
| Mesh (`mesh`) | Requires referencing an asset under the corresponding `mesh` tag. No need to configure the `size` attribute. For an example, see [`examples/assets/boston_dynamics_spot/spot.xml`](../../../../examples/assets/boston_dynamics_spot/spot.xml). |

## Main Interfaces

In MotrixSim, you can access Geom objects in the following ways:

-   [`model.num_geoms`]: Get the number of Geoms in the current world.
-   [`model.geoms`]: Get all Geom objects in the current world.
-   [`model.get_geom(key)`]: Get a specific Geom object by name or index.

Once you obtain a Geom object, you can read information such as its position, orientation, velocity, etc. For details, please refer to the [`Geom API`].

## Example

You can run a simple example of Geom API usage with:

```bash
pdm run examples/geom.py
```

See the source code at [`examples/geom.py`](../../../../examples/geom.py)。

[`model.num_geoms`]: motrixsim.SceneModel.num_geoms
[`model.geoms`]: motrixsim.SceneModel.geoms
[`model.get_geom(key)`]: motrixsim.SceneModel.get_geom
[`Geom API`]: motrixsim.Geom
