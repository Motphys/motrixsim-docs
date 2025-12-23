# 🎨 Renderer (RenderApp)

## Launching and Loading

[`RenderApp`] is responsible for basic scene rendering. Typically, you create a [`RenderApp`] instance in your code, load a model using [`load_model`], and then call [`render.launch(model)`] to load the model into the renderer.

## Synchronization

In motrixsim, the renderer runs in an independent thread, so we need to call [`render.sync(data)`] in the Python main thread to achieve bidirectional synchronization between physics simulation data and the renderer. The render.sync method actually executes the following logic:

-   Sends pose data of all physics objects, user drawing instructions, etc. to the renderer
-   Retrieves window, UI, and other input events as well as camera rendering data from the renderer

The underlying thread model is as follows:

![thread model](/_static/images/render_thread_model.jpg)

-   **Main thread**, i.e., the thread where Python code executes. We typically execute `render.sync(data)` once after several physics steps to synchronize data. sync does two things:
    1. Accepts input events and camera data from the render thread via the Event pipeline
    2. Sends frame data to the Frame pipeline (blocks and waits if the Frame pipeline is full)
-   **Render thread**, responsible for window creation and rendering loop execution. In each loop, it does two things:
    1. Accepts frame data from the main thread via the Frame pipeline and submits it to GPU for rendering (skips if the pipeline is empty)
    2. Processes window, UI, and camera data requests, and sends them to the Event pipeline

## Render Settings

Currently, there is a configuration item `RenderSettings` for global rendering configuration:

| Parameter Name       |                   Explanation                    | Default Value |
| :------------------- | :----------------------------------------------: | :-----------: |
| simplify_render_mesh |      Whether to automatically simplify mesh      |     False     |
| enable_shadow        |         Whether to enable light shadows          |     True      |
| enable_ssao          | Whether to enable Screen Space Ambient Occlusion |     True      |
| enable_oit           | Whether to enable Order-Independent Transparency |     True      |

Specifically, the corresponding rendering effects will only take effect when both global configuration is enabled AND certain rendering items are also enabled in the scene description file (mjcf/msd).

_Example code see [examples/render_settings.py](../../../../examples/render_settings.py)_

## Custom UI Components

Currently supports two types of components: buttons ([`add_button`]) and toggles ([`add_toggle`]), which respond to user click events by setting callback functions.

Users need to display the left panel through [`render.opt.set_left_panel_vis(True)`], and components will be displayed on the panel in the order they are added.

```{literalinclude} ../../../../examples/custom_ui.py
:language: python
:dedent:
:start-after: "# tag::custom_ui[]"
:end-before:  "# end::custom_ui[]"
```

_Full code see [examples/custom_ui.py](../../../../examples/custom_ui.py)_

## Gizmos Drawing

Gizmos are graphical elements used for debugging assistance. The renderer provides a simple API to draw gizmos.

| Method Name        |               Meaning               |
| :----------------- | :---------------------------------: |
| draw_sphere        |        Draw wireframe sphere        |
| draw_cuboid        |        Draw wireframe cuboid        |
| draw_cylinder      |       Draw wireframe cylinder       |
| draw_capsule       |       Draw wireframe capsule        |
| draw_ray           |              Draw ray               |
| draw_line          |          Draw line segment          |
| draw_arrow         |             Draw arrow              |
| draw_rect          |          Draw 2D rectangle          |
| draw_grid          |            Draw 3D grid             |
| draw_axes          |        Draw coordinate axes         |
| set_draw_collider  |    Turn on/off collider drawing     |
| set_draw_joint     |      Turn on/off joint drawing      |
| set_draw_site      | Turn on/off reference point drawing |
| set_collider_color |     Set collider drawing color      |
| set_joint_color    |       Set joint drawing color       |
| set_line_width     |       Set drawing line width        |
| set_joint_size     |       Set joint drawing size        |

Gizmos use immediate mode, so even if no update is needed, users need to add gizmos during each render synchronization.

```{literalinclude} ../../../../examples/gizmos.py
:language: python
:dedent:
:start-after: "# tag::draw_gizmos[]"
:end-before:  "# end::draw_gizmos[]"
```

_Full code see [examples/gizmos.py](../../../../examples/gizmos.py)_

## IO Input Events

You can get the [`Input`] object through [`render.input`]. The Input object provides a series of methods for querying the renderer's mouse, keyboard, and UI events.

You can understand more detailed usage through the following examples:

-   [example/mouse_click.py](../../../../examples/mouse_click.py)
-   [example/read_keyboard.py](../../../../examples/read_keyboard.py)

#### Valid Keyboard Input List

The following is the list of supported keyboard key inputs:

| Key Type      |         Example Keys          |
| :------------ | :---------------------------: |
| Letter Keys   |      `A`, `B`, ..., `Z`       |
| Function Keys |    `F1`, `F2`, ..., `F12`     |
| Special Keys  |    `Enter`, `Esc`, `Space`    |
| Arrow Keys    | `Up`, `Down`, `Left`, `Right` |

> Note: The above are all case-insensitive, and keys not mentioned in the table are not currently supported.

## System Camera Control

The renderer provides a free system camera control system. Users can control the viewing angle and focus point of the system camera through mouse operations (the focus point is always located at the screen center).

-   Left mouse button press and drag: Rotate the system camera around the focus point
-   Right mouse button press and drag: Move the focus point (shows red circle as focus point)
-   Mouse scroll wheel: Zoom (cannot zoom in further when at focus point position)

For more camera control methods, please refer to [Camera](../render/camera.md).

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

When we perform single model multi-instance rendering, we can configure the rendering visibility of each instance as needed.

```
...
# Create multiple instances
render_offsets = []
batch = 10
for i in range(batch):
    render_offsets.append([i * 2.0, 0, 0])
render.launch(model, batch, render_offsets)
data = SceneData(model, batch=(batch,))

target_scene_indices = [1, 3, 5, 7, 9] # Specify instance indices
render.set_scene_vis(target_scene_indices, False) # Hide target instances
render.set_scene_vis(target_scene_indices, True) # Show target instances
```

It can also be enabled/disabled globally:

```
render.set_all_scene_vis(False) # Hide all instances
render.set_all_scene_vis(True) # Show all instances
```

The above operations only affect rendering visibility and do not affect the object's physics simulation.

_Full code see [examples/partial_rendering.py](../../../../examples/partial_rendering.py)_

[`RenderApp`]: motrixsim.render.RenderApp
[`load_model`]: motrixsim.load_model
[`render.launch(model)`]: motrixsim.render.RenderApp.launch
[`render.sync(data)`]: motrixsim.render.RenderApp.sync
[`render.input`]: motrixsim.render.RenderApp.input
[`Input`]: motrixsim.render.Input
[`render.opt.set_left_panel_vis(True)`]: motrixsim.render.RenderOpt.set_left_panel_vis
[`add_button`]: motrixsim.render.RenderUI.add_button
[`add_toggle`]: motrixsim.render.RenderUI.add_toggle
