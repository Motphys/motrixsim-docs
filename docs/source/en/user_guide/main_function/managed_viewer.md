# 🎮 Interactive Viewer

## Overview

The Interactive Viewer provides a simplified interface for quickly visualizing and interacting with physics simulations. The [`viewer.launch()`] function operates in a blocking mode, meaning it will not return control to your Python code until the viewer window is closed. This blocking behavior enables precise timing of the physics loop and automatic handling of the simulation.

Unlike the lower-level [`RenderApp`] API which requires manual synchronization and loop management, the interactive viewer automatically handles the simulation loop, rendering synchronization, and common UI controls.

![Interactive Viewer Overview](/_static/images/interactive_viewer_overview.png)

## When to Use

The interactive viewer is designed for scenarios where you want to:

-   **Quickly visualize models**: Test and inspect physics simulations with minimal code
-   **Interactive debugging**: Examine simulation behavior using built-in playback controls
-   **Educational demonstrations**: Focus on physics concepts without rendering complexity
-   **Prototype development**: Rapidly iterate on model designs and behaviors
-   **Simple applications**: When custom rendering logic or non-blocking execution is not required

For production applications requiring fine-grained control over the simulation loop, consider using [`RenderApp`] instead.

### Key Features

-   **Blocking execution**: Runs until the window is closed, supporting precise physics loop timing
-   **Automatic simulation loop**: Physics steps and rendering are handled automatically
-   **Built-in controls**: Play/pause, reset, step-through, and speed control out of the box
-   **Multiple invocation modes**: Supports empty session, model-only, and model with data
-   **File loading**: Drag XML model files directly into the viewer window to load them instantly
-   **Zero configuration**: Works with sensible defaults, but customizable when needed

## Command-Line Interface

The interactive viewer can also be launched directly from the command line:

```bash
# Launch with a specific model file
uv run python -m motrixsim.interactive_viewer --file=path/to/your/model.xml

# Launch empty viewer (drag and drop model files to load)
uv run python -m motrixsim.interactive_viewer
```

### CLI Arguments

| Argument | Required | Description                                                                                                |
| -------- | -------- | ---------------------------------------------------------------------------------------------------------- |
| `--file` | No       | Path to the model file. If not provided, launches an empty viewer where you can drag and drop model files. |

### Examples

```bash
# Launch viewer with a specific model
uv run python -m motrixsim.interactive_viewer --file=examples/assets/boston_dynamics_spot/scene_arm.xml

# Launch empty viewer for drag-and-drop interaction
uv run python -m motrixsim.interactive_viewer
```

The CLI provides a quick way to visualize models without writing Python code. When a file is provided, it automatically:

-   Loads the specified model
-   Creates scene data with initial state
-   Runs a few physics steps for stabilization
-   Launches the interactive viewer

When launched without arguments, you can simply drag XML model files into the viewer window to load them instantly.

```{note}
For more control over initial conditions or custom callbacks, use the Python API directly with [`viewer.launch()`].
```

## Usage Modes

The [`viewer.launch()`] function supports three distinct invocation patterns to accommodate different use cases:

### 1. Empty Session (Default Model)

```python
import motrixsim as mx

# Launch with default demonstration model
mx.viewer.launch()
```

Launches an interactive visualization session with a default demonstration model. This is the quickest way to explore the viewer functionality.

**Tip:** You can also drag XML model files directly into the viewer window to load them instantly, making it easy to quickly preview different models without writing code.

### 2. Model Only

```python
import motrixsim as mx

# Load your model
model = mx.load_model("path/to/your/model.xml")

# Launch viewer - will create internal SceneData automatically
mx.viewer.launch(model)
```

Launches a visualization session for the given model. The viewer internally creates its own instance of [`SceneData`] for the simulation.

### 3. Model and Data

```python
import motrixsim as mx
from motrixsim import SceneData

# Load model and create data
model = mx.load_model("path/to/your/model.xml")
data = SceneData(model)

# Configure initial state
data.qpos[:] = initial_positions
data.qvel[:] = initial_velocities

# Launch viewer with initial data
mx.viewer.launch(model, data)
```

Uses the provided [`SceneData`] instance as the initial state for the simulation. The viewer creates an internal copy of the data for its simulation loop. This mode is useful when you need to:

-   Set specific initial conditions (positions, velocities, control inputs)
-   Run stabilization steps before visualization
-   Start the viewer from a particular simulation state

### Pre-Simulation Example

Run some physics steps before launching the viewer to stabilize the initial state:

```{literalinclude} ../../../../examples/interactive_viewer.py
:language: python
:dedent:
:start-after: "# Use custom model with physics data"
:end-before: "viewer.launch(model, data)"
```

This pre-simulation approach is particularly useful for:

-   Allowing initial contact forces to settle
-   Reaching a stable equilibrium configuration
-   Pre-computing derived quantities before visualization

## Complete Example

Here's a complete example demonstrating the interactive viewer with the Boston Dynamics Spot robot:

```{literalinclude} ../../../../examples/interactive_viewer.py
:language: python
:dedent:
:start-after: "# Copyright (C)"
```

This example:

1. Loads the Spot robot model with robotic arm (includes actuators)
2. Creates scene data
3. Runs 20 physics steps to stabilize the simulation
4. Launches the interactive viewer

## Built-in Controls

The managed viewer provides several built-in controls accessible through the UI:

| Control           | Function                                              |
| ----------------- | ----------------------------------------------------- |
| **Play/Pause**    | Start or pause the simulation                         |
| **Reset**         | Reset the simulation to initial state                 |
| **Single Step**   | Advance simulation by one step (when paused)          |
| **Speed Control** | Adjust simulation speed (slow motion to fast forward) |

Additional mouse controls:

-   **Left mouse drag**: Rotate camera around focus point
-   **Right mouse drag**: Move focus point
-   **Mouse wheel**: Zoom in/out

```{tip}
Press the spacebar to quickly toggle between play and pause states.
```

## Comparison with RenderApp

The interactive viewer and [`RenderApp`] serve different use cases:

| Feature             | Interactive Viewer               | RenderApp                      |
| ------------------- | -------------------------------- | ------------------------------ |
| **Execution mode**  | Blocking (runs until closed)     | Non-blocking (manual control)  |
| **Simulation loop** | Automatic                        | Manual (`step()` calls)        |
| **Synchronization** | Automatic                        | Manual (`render.sync()` calls) |
| **Use case**        | Quick visualization, prototyping | Production apps, custom logic  |
| **Control flow**    | Viewer controls flow             | You control flow               |
| **Customization**   | Limited                          | Full control                   |

### When to Use Each

**Use Interactive Viewer when:**

-   Quickly testing or debugging a model
-   Creating educational demonstrations
-   Building simple interactive tools
-   You want minimal code

**Use RenderApp when:**

-   Integrating with existing application logic
-   Need fine-grained control over rendering timing
-   Building production applications
-   Implementing custom UI or visualization
-   Running headless simulations with optional rendering

## Best Practices

### Model Loading

```python
# Good: Absolute or relative paths
model = mx.load_model("examples/assets/boston_dynamics_spot/scene_arm.xml")

# Good: Use pathlib for cross-platform compatibility
from pathlib import Path
model_path = Path(__file__).parent / "assets" / "model.xml"
model = mx.load_model(str(model_path))
```

### Data Initialization

```python
# Initialize data
data = SceneData(model)

# Set initial configuration
data.qpos[:] = initial_positions
data.qvel[:] = initial_velocities

# Run a few steps to stabilize
for _ in range(10):
    mx.step(model, data)

# Launch viewer
mx.viewer.launch(model, data)
```

## Limitations and Notes

```{warning}
The interactive viewer is blocking - your Python code will not continue until the viewer window is closed. If you need concurrent execution, use [`RenderApp`] instead.
```

**Other considerations:**

-   **Single window**: Only one interactive viewer can be active at a time
-   **No multi-instance rendering**: For batch rendering, use [`RenderApp`]
-   **Limited customization**: For custom UI or advanced rendering features, use [`RenderApp`]

## Related Documentation

-   [Renderer (RenderApp)](render.md) - Lower-level rendering API with full control
-   [Camera](../render/camera.md) - Camera control and configuration
-   [Widget Components](../render/widgets.md) - Multi-viewport rendering

### API Reference

-   [`viewer.launch()`]
-   [`SceneModel`]
-   [`SceneData`]
-   [`step()`]

[`RenderApp`]: motrixsim.render.RenderApp
[`viewer.launch()`]: motrixsim.viewer.launch
[`SceneModel`]: motrixsim.SceneModel
[`SceneData`]: motrixsim.SceneData
[`step()`]: motrixsim.step
