# 📹 CameraViewport

## Overview

CameraViewport allows you to create multiple camera viewport components within the rendering window for simultaneously displaying real-time rendered views from different cameras. This is very useful for multi-angle observation, sensor data visualization, and other scenarios.

```{video} /_static/videos/rgbd_camera.mp4
:caption: The top-right corner shows the RGBD sensor view displayed using the Camera Viewport Widget component
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

### Key Features

-   **Multi-viewport Support**: Create multiple independent camera viewports in the same window
-   **Flexible Layout**: Supports three layout formats: pixels, percentage, and auto
-   **Dynamic Updates**: Real-time updates of viewport cameras, layouts, and properties

## Basic Creation Method

Use the `render.widgets.create_camera_viewport()` method to create a camera viewport widget:

```python
viewport = render.widgets.create_camera_viewport(
    camera=cameras[0],
    layout=Layout(left=10, top=10, width=240, height=180),
    sim_world_index=0
)
```

**Parameter Description**:

-   **camera**: The camera object to display (required)
-   **layout**: Layout configuration (optional, defaults to left=50, top=50, width=200, height=200)
-   **sim_world_index**: Simulation world index (optional, defaults to 0)

**Return Value**: Returns a `CameraViewport` object.

## Creating Multiple Viewports

You can create multiple viewports in the same window, each displaying a different camera's view:

```{literalinclude} ../../../../examples/render/camera_viewport.py
:language: python
:dedent:
:start-after: "# Viewport 1: Top-left with pixel-based layout"
:end-before: "# Store initial layouts"
```

This code creates three viewports:

-   **vp1**: Top-left corner, using pixel layout, displaying cameras[0]
-   **vp2**: Top-right corner, using percentage layout, displaying cameras[1]
-   **vp3**: Bottom-left corner, using mixed layout, displaying cameras[0]

![camera viewport](/_static/images/examples/camera_viewport.png)

## Widget Dynamic Updates

After creating a widget, you can dynamically update its properties through the `update()` method.

### Updating Viewport Properties

The `CameraViewport.update()` method supports the following parameters:

-   **camera**: New camera object
-   **layout**: New layout configuration
-   **sim_world_index**: New simulation world index

All parameters are optional; only provide the parameters that need to be updated.

### Updating Camera

Switch the camera displayed by the viewport:

```python
viewport.update(camera=cameras[1])
```

### Updating Layout

Modify the position and size of the viewport:

```python
viewport.update(layout=Layout(left=100, top=100, width=300, height=200))
```

### Combined Updates

You can update multiple properties simultaneously:

```python
viewport.update(
    camera=cameras[2],
    layout=Layout(left=200, top=200),
    sim_world_index=0
)
```

## Interactive Control Examples

The following example shows how to update widgets through keyboard interactions:

### Switching Cameras

```{literalinclude} ../../../../examples/render/camera_viewport.py
:language: python
:dedent:
:start-after: "# Switch vp1 camera"
:end-before: "# Move vp1 viewport"
```

Press 1/2/3 keys to switch the camera displayed by vp1.

### Moving Viewport Position

```{literalinclude} ../../../../examples/render/camera_viewport.py
:language: python
:dedent:
:start-after: "# Move vp1 viewport"
:end-before: "# Resize vp1 viewport"
```

Press w/a/s/d keys to move the position of vp1.

### Resizing Viewport

```{literalinclude} ../../../../examples/render/camera_viewport.py
:language: python
:dedent:
:start-after: "# Resize vp1 viewport"
:end-before: "# Reset all layouts"
```

Press +/- keys to adjust the size of vp1.

## Removing Viewports

If you no longer need a viewport, you can use the `remove()` method to completely remove it from the rendering window:

```python
viewport.remove()
```

```{warning}
After calling the `remove()` method, the viewport will be permanently removed. Subsequent calls to the `update()` method on this viewport object will result in an error. If you need to redisplay it, you must recreate the viewport.
```

The following example shows how to remove a viewport through keyboard interaction:

```{literalinclude} ../../../../examples/render/camera_viewport.py
:language: python
:dedent:
:start-after: "# Remove vp3 from screen"
:end-before: "# Sync render with simulation"
```

Press the k key to remove vp3. After removal, vp3 will completely disappear from the screen and cannot be restored through the update method.

## Complete Example

The following is a complete interactive CameraViewport widget system with creation, update, and interaction control features:

```{literalinclude} ../../../../examples/render/camera_viewport.py
:language: python
:dedent:
:start-after: "# Copyright (C)"
:end-before: 'if __name__ == "__main__"'
```

## Related API Links

-   [`Layout`]
-   [`CameraViewport`]
-   [`RenderWidgets.create_camera_viewport()`]
-   [`CameraViewport.update()`]
-   [`CameraViewport.remove()`]

[`Layout`]: motrixsim.render.Layout
[`CameraViewport`]: motrixsim.render.widgets.CameraViewport
[`RenderWidgets.create_camera_viewport()`]: motrixsim.render.RenderWidgets.create_camera_viewport
[`CameraViewport.update()`]: motrixsim.render.widgets.CameraViewport.update
[`CameraViewport.remove()`]: motrixsim.render.widgets.CameraViewport.remove
