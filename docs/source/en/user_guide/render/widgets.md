# 🖼️ Widget Components

## Overview

The Widget system allows you to create multiple visualization components within the rendering window, including camera viewports (CameraViewport) and custom images (ImageWidget). This is very useful for multi-angle observation, sensor data visualization, custom UI display, and other scenarios.

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

-   **Multiple Widget Types**: Supports camera viewports (CameraViewport) and custom images (ImageWidget)
-   **Multi-component Support**: Create multiple independent widget components in the same window
-   **Flexible Layout**: Supports three layout formats: pixels, percentage, and auto
-   **Dynamic Updates**: Real-time updates of widget content, layout, and properties

## Widget Types

MotrixSim provides the following two Widget types:

```{toctree}
:maxdepth: 1

camera_viewport
image_widget
```

### Core Concepts

Before starting to use widgets, you need to understand the following core concepts:

-   **Layout**: Configure the position and size of widgets
-   **CameraViewport**: Widget component that displays camera views
-   **ImageWidget**: Widget component that displays custom images
-   **RenderWidgets**: Main interface for creating and managing widgets

## Layout Configuration System

The Layout class is used to configure the position and size of widgets on the screen. It provides 6 layout parameters:

-   **left**: Left position
-   **right**: Right position
-   **top**: Top position
-   **bottom**: Bottom position
-   **width**: Width
-   **height**: Height

### Layout Formats

Layout parameters support three formats:

#### Pixel Format

Directly use numeric values to represent pixels:

```python
layout = Layout(left=50, top=50, width=200, height=150)
```

This means the widget is 50 pixels from the left, 50 pixels from the top, with a width of 200 pixels and a height of 150 pixels.

#### Percentage Format

Use strings to represent percentages:

```python
layout = Layout(left="10%", top="10%", width="30%", height="30%")
```

This means the widget is 10% from the left, 10% from the top, with a width of 30% and a height of 30%.

#### Auto Format

Use the "auto" string to indicate automatic layout:

```python
layout = Layout(width="auto", height="auto")
```

Width and height will automatically adjust based on content.

#### Mixed Format

You can mix different formats:

```python
layout = Layout(left=10, top="60%", width=320, height=240)
```

This means the left distance is 10 pixels, the top distance is 60%, with a width of 320 pixels and a height of 240 pixels.

### Layout Examples

The following example shows three different layout formats:

```{literalinclude} ../../../../examples/render/camera_viewport.py
:language: python
:dedent:
:start-after: "# Viewport 1: Top-left with pixel-based layout"
:end-before: "# Store initial layouts"
```

```{note}
You can choose the appropriate layout format according to your actual needs. Pixel layout is suitable for fixed UI, while percentage layout is suitable for responsive design.
```

## Best Practices and Notes

### Performance Optimization Recommendations

```{warning}
Avoid frequently creating and destroying widgets, as this will affect performance. It is recommended to create all required widgets during initialization, then use the update() method to dynamically update their properties.
```

### Layout Recommendations

1. **Pixel Layout**: Suitable for fixed UI elements such as buttons, panels, etc.
2. **Percentage Layout**: Suitable for scenarios requiring responsive design
3. **Avoid Overlap**: Ensure that multiple widgets do not overlap to avoid blocking each other
4. **Preload Layouts**: Set up layouts for all widgets during initialization to reduce runtime adjustments

## Related API Links

-   [`Layout`]
-   [`CameraViewport`]
-   [`ImageWidget`]
-   [`Image`]
-   [`RenderWidgets`]

[`Layout`]: motrixsim.render.Layout
[`CameraViewport`]: motrixsim.render.widgets.CameraViewport
[`ImageWidget`]: motrixsim.render.widgets.ImageWidget
[`Image`]: motrixsim.render.Image
[`RenderWidgets`]: motrixsim.render.RenderWidgets
