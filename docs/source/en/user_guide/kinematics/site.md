# 📍 Site

## Overview

A `Site` is an important concept in MotrixSim, representing a point of interest in the model. A `Site` is essentially a virtual marker used to indicate specific positions and orientations within the model framework.

### Key Features

-   **Virtual Reference Point**: A `Site` is a virtual marker and does not participate in collision detection or inertia calculations
-   **Reference Location**: Used to specify spatial properties for sensors, endpoints, and other objects
-   **Lightweight**: Compared to physical geometries, a `Site` does not participate in physics calculations and has minimal overhead

## Usage and Examples

### Usage

You can access all `Site` information or retrieve a specific `Site` by name via the [`SceneModel`](../main_function/scene_model.md) object:

```{literalinclude} ../../../../examples/site_and_sensor.py
:language: python
:dedent:
:start-after: "# tag::site_access[]"
:end-before:  "# end::site_access[]"
```

For a complete example, see [`examples/site_and_sensor.py`](../../../../examples/site_and_sensor.py).

### Application Scenarios

`Site` can be used in various scenarios:

-   **Sensor Mounting**: Installation points for IMUs, cameras, LiDARs, etc.
-   **Reference Markers**: Marking key locations such as joint centers, centers of mass, etc.
-   **Debugging Aid**: Visualizing important points to help verify model correctness
-   **Path Planning**: Used as waypoints or target points in path planning

## Defining Site in MJCF

In MJCF files, a `Site` is defined using the `<site>` tag. For detailed tag attributes and usage, refer to the [MJCF Format Documentation](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-site).

**Note**: MotrixSim currently supports the core features and common attributes of Site. Some `<site>` attributes are still under development. Please refer to the [support list](../getting_started/mjcf.md) for details.

Below is an example of a `Site` definition from `site_and_sensor.xml`:

```{literalinclude} ../../../../examples/assets/site_and_sensor.xml
:language: xml
:dedent:
:lines: 9-19
```

For the complete XML file, see: [`examples/assets/site_and_sensor.xml`](../../../../examples/assets/site_and_sensor.xml)

## Notes

1. **Coordinate System**: The position and orientation of a `Site` are relative to its parent link's coordinate frame
2. **Unique Naming**: Each `Site` should have a unique name within the model
3. **Visualization**: `Site` can be displayed in the renderer, which is helpful for debugging and verifying positions
4. **Virtual Nature**: `Site` is virtual; use the `<geom>` tag if physical interaction is required

## API Reference

For more APIs related to Site, see [`Site API`]

[`Site API`]: motrixsim.Site
