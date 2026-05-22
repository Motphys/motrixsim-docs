# 🌐 WebViewer

This page explains how to use the MotrixSim web viewer, including how to load files, how to understand the file tree, what the top bar buttons do, and how to operate the viewer with mouse and keyboard.

## Open the Viewer

Open the MotrixSim web viewer page in a modern browser with WebAssembly support.

Simulation page URL: <https://motrix.motphys.com/>

After the page finishes loading, you will typically see:

-   A left-side file panel with `Online` and `Customize`
-   A central 3D viewport
-   A top bar with playback and scene control buttons

```{figure} /_static/images/web_viewer/viewer-overview.jpg
:alt: MotrixSim Web Viewer overview
:width: 90%

Overview of the MotrixSim web viewer, including the left file tree, central 3D viewport, and top toolbar.
```

## Load Models by Dragging a Folder

On the web platform, the viewer cannot directly access your local file system like the native desktop app. The recommended workflow is to drag a whole model folder into the browser window.

### Recommended Folder Structure

The dragged folder should contain the scene file and all resources it depends on, for example:

```text
boston_dynamics_spot/
├── scene.xml
├── meshes/
├── textures/
└── ...
```

### How to Load

1. Open the viewer page.
2. Drag the entire model folder into the browser window.
3. Wait for the files to appear in the left-side `Customize` section.
4. In the file tree, click a scene file such as `.xml`, `.urdf`, or `.json` to load it.

```{figure} /_static/images/web_viewer/drag_folder_here.jpg
:alt: Drag a model folder into the web viewer
:width: 90%

Drag the complete model folder, including the scene file and all dependent assets, into the viewer page.
```

```{note}
Dragging the whole folder is preferred over dragging only the scene file, because referenced meshes, textures, and other dependent assets usually need to stay in the same relative paths.
```

## `Online` vs `Customize`

The left file tree has two data sources.

### `Online`

-   Provided by the deployed website
-   Read-only
-   Suitable for built-in demos and shared example assets
-   Files appear automatically after the viewer loads the online manifest

### `Customize`

-   Built from folders or files you drag into the page
-   Exists only in the current browser session
-   Best for testing your own MJCF, URDF, MSD, meshes, and textures

In short:

-   Use `Online` for bundled web examples
-   Use `Customize` for your own local assets

## Load a Scene from the File Tree

Once files appear in the left panel:

1. Expand `Online` or `Customize`
2. Browse to the scene file
3. Click the scene file entry

Scene files are shown as selectable items in the file tree. Clicking one starts the asset loading pipeline and spawns the scene in the viewer.

## Top Bar Buttons

The top bar contains playback controls and scene utility buttons.

```{figure} /_static/images/web_viewer/buttons.jpg
:alt: MotrixSim Web Viewer top bar buttons
:width: 90%

Common buttons in the top toolbar, including playback controls, scene controls, and the help entry.
```

### Playback Controls

-   `Play`: start or resume simulation
-   `Pause`: pause simulation
-   `Next`: step forward by one frame

### Scene Controls

These are the shared scene control buttons implemented in the viewer top bar:

-   `Reset`: reset scene state to the initial simulation state
-   `Reload`: reload the currently loaded model file and its assets

### Viewer-Specific Buttons

The MotrixSim viewer may also show additional buttons on the right side of the top bar, such as:

-   `Help`: open this web viewer guide page

## Input Guide

This section summarizes the most common mouse and keyboard operations when using MotrixSim.

### Mouse

-   Left mouse drag: orbit the camera around the scene
-   Mouse wheel: zoom in or out
-   Middle mouse drag or the corresponding trackpad gesture: pan the camera

### Keyboard

-   `Space`: pause or resume simulation
-   `F10`: advance one simulation step
-   `Ctrl+E`: reset the scene
-   `Ctrl+R`: reload the current model
-   `F11`: toggle fullscreen when supported

### Physics Drag Interaction

If physics drag is enabled in the current app configuration:

-   Hold `Ctrl`
-   Press the left mouse button on a draggable object
-   Move the mouse to drag the object

```{video} /_static/videos/physics_drag.mp4
:poster: /_static/images/poster/physics_drag.jpg
:caption: Example of physics drag interaction: hold Ctrl and drag an object
:playsinline:
:width: 100%
```

## Typical Workflow

1. Open the web viewer
2. Drag a complete model folder into the page
3. Click the scene file from `Customize`
4. Use the mouse to inspect the scene
5. Use the top bar buttons to play, pause, reset, or reload

## See Also

-   [Installation](installation.md)
-   [Hello MotrixSim](hello_motrixsim.md)
-   [Render](../main_function/render.md)
