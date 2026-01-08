# 🖼️ ImageWidget

## Overview

ImageWidget allows you to display custom images within the rendering window, which is very useful for visualizing sensor data, displaying debug information, creating custom UIs, and other scenarios.

### Key Features

-   **Custom Image Display**: Supports image data in numpy array format
-   **Flexible Layout**: Supports three layout formats: pixels, percentage, and auto
-   **Dynamic Updates**: Real-time updates of image content and layout properties

## Creating Images

Before using ImageWidget, you need to create an Image object. Use the `render.create_image()` method to create an image from a numpy array:

```python
import numpy as np

# Create a random RGB image
pixels = np.random.randint(0, 256, (240, 320, 3), dtype=np.uint8)
image = render.create_image(pixels)
```

**Parameter Description**:

-   **pixels**: numpy array with shape `(height, width, 3)` and dtype `uint8`
-   **Return Value**: Returns an `Image` object

**Image Format Requirements**:

-   **Color Space**: RGB format, each channel value range is 0-255
-   **Data Type**: Must be `np.uint8`
-   **Shape**: `(height, width, 3)`, where 3 represents the RGB three channels

```{note}
The image shape is (height, width, 3), not (width, height, 3). The first dimension is height (number of rows), and the second dimension is width (number of columns).
```

## Creating ImageWidget

Use the `render.widgets.create_image_widget()` method to create an image widget:

```python
widget = render.widgets.create_image_widget(
    image=image,
    layout=Layout(left=10, top=10, width=320, height=240)
)
```

**Parameter Description**:

-   **image**: Image object (required)
-   **layout**: Layout configuration (optional, defaults to left=50, top=50, width=200, height=200)

**Return Value**: Returns an `ImageWidget` object.

## Creating Multiple ImageWidgets

You can create multiple ImageWidgets in the same window, each displaying different images:

```{literalinclude} ../../../../examples/render/image_widget.py
:language: python
:dedent:
:start-after: "# Widget 1: Top-left"
:end-before: "# Store initial layouts"
```

This code creates three ImageWidgets:

-   **widget1**: Top-left corner, using pixel layout, displaying random noise image
-   **widget2**: Top-right corner, using percentage layout, displaying gradient image
-   **widget3**: Bottom-left corner, using mixed layout, displaying checkerboard image

![image widget](/_static/images/examples/image_widget.jpg)

## ImageWidget Dynamic Updates

After creating an ImageWidget, you can dynamically update its displayed content and layout in various ways.

### Updating Image Content

ImageWidget provides two methods to update image content:

#### Method 1: Directly Update Image's pixels Property (Recommended)

This is the most efficient method as it reuses the existing Image object:

```python
# Create new pixel data
new_pixels = np.random.randint(0, 256, (240, 320, 3), dtype=np.uint8)

# Directly update image content
image.pixels = new_pixels
```

#### Method 2: Create New Image and Update Widget

If you need to completely replace the image object:

```python
# Create new image
new_image = render.create_image(new_pixels)

# Update widget to use new image
widget.update(image=new_image)
```

```{note}
Method 1 (directly updating pixels) is more efficient as it avoids creating new Image objects. For scenarios that require frequent image content updates (such as real-time sensor data display), it is recommended to use Method 1.
```

### Updating Layout

Like CameraViewport, you can update ImageWidget's layout using the `update()` method:

```python
widget.update(layout=Layout(left=20, top=20, width=400, height=300))
```

### Combined Updates

You can update both image and layout simultaneously:

```python
widget.update(
    image=new_image,
    layout=Layout(left=50, top=50, width=320, height=240)
)
```

## Interactive Control Examples

The following example shows how to control ImageWidget through keyboard interactions:

### Switching Image Content

```{literalinclude} ../../../../examples/render/image_widget.py
:language: python
:dedent:
:start-after: "# Change widget1 pattern type"
:end-before: "# Move widget1 (10 pixels per keypress)"
```

Press 1/2/3 keys to switch the image type displayed by widget1 (random noise/gradient/checkerboard).

### Moving ImageWidget Position

```{literalinclude} ../../../../examples/render/image_widget.py
:language: python
:dedent:
:start-after: "# Move widget1 (10 pixels per keypress)"
:end-before: "# Resize widget1 (20 pixels per keypress)"
```

Press w/a/s/d keys to move the position of widget1.

### Resizing ImageWidget

```{literalinclude} ../../../../examples/render/image_widget.py
:language: python
:dedent:
:start-after: "# Resize widget1 (20 pixels per keypress)"
:end-before: "# Reset all layouts"
```

Press +/- keys to adjust the size of widget1.

## Removing ImageWidget

If you no longer need an ImageWidget, you can use the `remove()` method to completely remove it from the rendering window:

```python
widget.remove()
```

```{warning}
After calling the `remove()` method, the widget will be permanently removed. Subsequent calls to the `update()` method on this widget object will result in an error. If you need to redisplay it, you must recreate the widget.
```

## Complete Example

The following is a complete ImageWidget interaction example showing how to dynamically generate and update images:

```{literalinclude} ../../../../examples/render/image_widget.py
:language: python
:dedent:
:start-after: "# Copyright (C)"
:end-before: 'if __name__ == "__main__"'
```

**ImageWidget Control Instructions**:

-   **SPACE**: Regenerate all images
-   **1/2/3**: Switch widget1 image type (random noise/gradient/checkerboard)
-   **w/a/s/d**: Move widget1 position (up/left/down/right)
-   **+/-**: Adjust widget1 size
-   **r**: Reset all layouts

## Performance Optimization Recommendations

1. **Image Update Frequency**:

    - For real-time sensor data, recommend using `image.pixels = new_pixels` method
    - Avoid creating new Image objects in high-frequency loops
    - Set reasonable update frequency to avoid exceeding rendering frame rate

2. **Image Size Optimization**:

    - Use appropriate image resolution, avoid unnecessarily large images
    - For small-sized widgets, using smaller images can improve performance
    - Consider using image pyramids or multi-resolution display

3. **Memory Management**:
    - Reuse Image objects instead of frequently creating new ones
    - Promptly remove widgets that are no longer needed
    - Pay attention to numpy array memory management to avoid memory leaks

## Related API Links

-   [`Layout`]
-   [`ImageWidget`]
-   [`Image`]
-   [`RenderWidgets.create_image_widget()`]
-   [`RenderApp.create_image()`]
-   [`ImageWidget.update()`]
-   [`ImageWidget.remove()`]

[`Layout`]: motrixsim.render.Layout
[`ImageWidget`]: motrixsim.render.widgets.ImageWidget
[`Image`]: motrixsim.render.Image
[`RenderWidgets.create_image_widget()`]: motrixsim.render.RenderWidgets.create_image_widget
[`RenderApp.create_image()`]: motrixsim.render.RenderApp.create_image
[`ImageWidget.update()`]: motrixsim.render.widgets.ImageWidget.update
[`ImageWidget.remove()`]: motrixsim.render.widgets.ImageWidget.remove
