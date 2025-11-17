# 🎨 Renderer (RenderApp)

## Launching and Loading

[`RenderApp`] is responsible for basic scene rendering. Typically, you create a [`RenderApp`] instance in your code, load a model using [`load_model`], and then call [`render.launch(model)`] to load the model into the renderer.

## Synchronization

In the main loop, it is recommended to call [`render.sync(data)`] after each physics simulation step to perform bidirectional synchronization and update rendering.

Users can also adjust the ratio between step and sync according to their needs.

Synchronization includes:

-   Sending physics simulation data, custom UI components, gizmo drawing instructions, etc. to the renderer
-   Receiving IO input events from the renderer

### Render Settings

Currently, global rendering settings are configured via the `RenderSettings` property:

| Parameter Name       |                   Explanation                    | Default Value |
| :------------------- | :----------------------------------------------: | :-----------: |
| simplify_render_mesh |    Whether to automatically simplify the mesh    |     False     |
| enable_shadow        |         Whether to enable light shadows          |     True      |
| enable_ssao          | Whether to enable Screen Space Ambient Occlusion |     True      |
| enable_oit           | Whether to enable Order-Independent Transparency |     True      |

Specifically, the corresponding rendering effects will only take effect if they are enabled in both this global configuration and the scene description file (MJCF/MSD).

_See the complete code at [examples/render_settings.py](../../../../examples/render_settings.py)_

### Custom UI Components

Currently, two types of components are supported: buttons ([`add_button`]) and toggles ([`add_toggle`]). You can set callback functions to respond to user click events.

To display the left panel, call [`render.opt.set_left_panel_vis(True)`]. Components will be displayed in the order they are added.

```{literalinclude} ../../../../examples/custom_ui.py
:language: python
:dedent:
:start-after: "# tag::custom_ui[]"
:end-before:  "# end::custom_ui[]"
```

_See the complete code at [examples/custom_ui.py](../../../../examples/custom_ui.py)_

### Gizmo Drawing

Gizmos are graphical elements used for debugging assistance. The renderer provides a simple API for drawing gizmos.

Gizmos use immediate mode; even if no update is needed, users must add gizmos on every render sync.

```{literalinclude} ../../../../examples/gizmos.py
:language: python
:dedent:
:start-after: "# tag::draw_gizmos[]"
:end-before:  "# end::draw_gizmos[]"
```

_See the complete code at [examples/gizmos.py](../../../../examples/gizmos.py)_

### IO Input Events

You can access the [`Input`] object via [`render.input`]. The Input object provides a series of methods for querying mouse, keyboard, and UI events from the renderer.

For more detailed usage, refer to the following examples:

-   [example/mouse_click.py](../../../../examples/mouse_click.py)
-   [example/read_keyboard.py](../../../../examples/read_keyboard.py)

#### Supported Keyboard Keys Table

The following keyboard key inputs are supported:

| Key Type      | Example Keys                  |
| ------------- | ----------------------------- |
| Letter Keys   | `A`, `B`, ..., `Z`            |
| Function Keys | `F1`, `F2`, ..., `F12`        |
| Special Keys  | `Enter`, `Esc`, `Space`       |
| Arrow Keys    | `Up`, `Down`, `Left`, `Right` |

> Note: All key names are case-insensitive. Keys not listed above are currently unsupported.

## Camera Control

The renderer provides a free camera control system. Users can control the camera's viewpoint and focus (always at the center of the screen) using the mouse:

-   Left mouse button drag: Rotate the camera around the focus point
-   Right mouse button drag: Move the focus point (a red circle indicates the focus)
-   Mouse wheel: Zoom (cannot zoom in beyond the focus point)

## Multi-Instance Rendering of a Single Model

[`render.launch(model)`] also supports two optional parameters: batch:int and render_offset:List[:3]. These are used to set the number of instances and the offset positions when rendering multiple instances of a single model.

```{literalinclude} ../../../../examples/model.py
:language: python
:dedent:
:start-after: "model = load_model(path)"
:end-before:  "# Create the physics data of the model"
```

_See the complete code at [examples/model.py](../../../../examples/model.py)_

### Instance Visibility

The render visibility of each individual instance can be configured as needed.

```
...
# Create multi-instance
render_offsets = []
batch = 10
for i in range(batch):
    render_offsets.append([i * 2.0, 0, 0])
render.launch(model, batch, render_offsets)
data = SceneData(model, batch=(batch,))

target_scene_indices = [1, 3, 5, 7, 9] # Set target instance indices
render.set_scene_vis(target_scene_indices, True) # Show target instances
render.set_scene_vis(target_scene_indices, False) # Hide target instances
```

It can also be enabled and disabled globally.

```
render.set_all_scene_vis(True) # Show all instances
render.set_all_scene_vis(False) # Hide all instances
```

The above operations affect only the rendering visibility and have no effect on the instance's physical simulation.

_See the complete code at [examples/partial_rendering.py](../../../../examples/partial_rendering.py)_

[`RenderApp`]: motrixsim.render.RenderApp
[`load_model`]: motrixsim.load_model
[`render.launch(model)`]: motrixsim.render.RenderApp.launch
[`render.sync(data)`]: motrixsim.render.RenderApp.sync
[`render.input`]: motrixsim.render.RenderApp.input
[`Input`]: motrixsim.render.Input
[`render.opt.set_left_panel_vis(True)`]: motrixsim.render.RenderOpt.set_left_panel_vis
[`add_button`]: motrixsim.render.RenderUI.add_button
[`add_toggle`]: motrixsim.render.RenderUI.add_toggle
