# 🖼️ ImageWidget

## 概述

ImageWidget 允许您在渲染窗口中显示自定义图像，这对于可视化传感器数据、显示调试信息、创建自定义 UI 等场景非常有用。

### 主要特性

-   **自定义图像显示**: 支持 numpy 数组格式的图像数据
-   **灵活布局**: 支持像素、百分比和自动三种布局格式
-   **动态更新**: 实时更新图像内容和布局属性

## 创建图像

在使用 ImageWidget 之前，需要先创建一个 Image 对象。使用 `render.create_image()` 方法从 numpy 数组创建图像：

```python
import numpy as np

# 创建一个随机RGB图像
pixels = np.random.randint(0, 256, (240, 320, 3), dtype=np.uint8)
image = render.create_image(pixels)
```

**参数说明**：

-   **pixels**: numpy 数组，shape 必须为 `(height, width, 3)`，dtype 为 `uint8`
-   **返回值**: 返回一个 `Image` 对象

**图像格式要求**：

-   **颜色空间**: RGB 格式，每个通道值范围为 0-255
-   **数据类型**: 必须是 `np.uint8`
-   **形状**: `(height, width, 3)`，其中 3 表示 RGB 三个通道

```{note}
图像的形状是 (height, width, 3)，而不是 (width, height, 3)。第一个维度是高度（行数），第二个维度是宽度（列数）。
```

## 创建 ImageWidget

使用 `render.widgets.create_image_widget()` 方法创建图像 widget：

```python
widget = render.widgets.create_image_widget(
    image=image,
    layout=Layout(left=10, top=10, width=320, height=240)
)
```

**参数说明**：

-   **image**: Image 对象（必需）
-   **layout**: 布局配置（可选，默认为 left=50, top=50, width=200, height=200）

**返回值**：返回一个 `ImageWidget` 对象。

## 创建多个 ImageWidget

您可以在同一窗口中创建多个 ImageWidget，每个显示不同的图像：

```{literalinclude} ../../../../examples/viewer/image_widget.py
:language: python
:dedent:
:start-after: "# Widget 1: Top-left"
:end-before: "# Store initial layouts"
```

这段代码创建了三个 ImageWidget：

-   **widget1**: 左上角，使用像素布局，显示随机噪声图像
-   **widget2**: 右上角，使用百分比布局，显示渐变图像
-   **widget3**: 左下角，使用混合布局，显示棋盘格图像

![image widget](/_static/images/examples/image_widget.jpg)

## ImageWidget 动态更新

创建 ImageWidget 后，可以通过多种方式动态更新其显示的内容和布局。

### 更新图像内容

ImageWidget 提供了两种更新图像内容的方法：

#### 方法 1：直接更新 Image 的 pixels 属性（推荐）

这是最高效的方法，因为它复用了已有的 Image 对象：

```python
# 创建新的像素数据
new_pixels = np.random.randint(0, 256, (240, 320, 3), dtype=np.uint8)

# 直接更新图像内容
image.pixels = new_pixels
```

#### 方法 2：创建新 Image 并更新 Widget

如果需要完全替换图像对象：

```python
# 创建新图像
new_image = render.create_image(new_pixels)

# 更新widget以使用新图像
widget.update(image=new_image)
```

```{note}
方法1（直接更新 pixels）更高效，因为它避免了创建新的 Image 对象。在需要频繁更新图像内容的场景（如实时传感器数据显示）中，建议使用方法1。
```

### 更新布局

与 CameraViewport 一样，可以使用 `update()` 方法更新 ImageWidget 的布局：

```python
widget.update(layout=Layout(left=20, top=20, width=400, height=300))
```

### 组合更新

可以同时更新图像和布局：

```python
widget.update(
    image=new_image,
    layout=Layout(left=50, top=50, width=320, height=240)
)
```

## 交互式控制示例

以下示例展示了如何通过键盘交互来控制 ImageWidget：

### 切换图像内容

```{literalinclude} ../../../../examples/viewer/image_widget.py
:language: python
:dedent:
:start-after: "# Change widget1 pattern type"
:end-before: "# Move widget1 (10 pixels per keypress)"
```

按 1/2/3 键可以切换 widget1 显示的图像类型（随机噪声/渐变/棋盘格）。

### 移动 ImageWidget 位置

```{literalinclude} ../../../../examples/viewer/image_widget.py
:language: python
:dedent:
:start-after: "# Move widget1 (10 pixels per keypress)"
:end-before: "# Resize widget1 (20 pixels per keypress)"
```

按 w/a/s/d 键可以移动 widget1 的位置。

### 调整 ImageWidget 大小

```{literalinclude} ../../../../examples/viewer/image_widget.py
:language: python
:dedent:
:start-after: "# Resize widget1 (20 pixels per keypress)"
:end-before: "# Reset all layouts"
```

按 +/- 键可以调整 widget1 的大小。

## 移除 ImageWidget

如果不再需要某个 ImageWidget，可以使用 `remove()` 方法将其完全从渲染窗口中移除：

```python
widget.remove()
```

```{warning}
调用 `remove()` 方法后，该 widget 将被永久移除。后续对该 widget 对象调用 `update()` 方法将导致错误。如果需要重新显示，必须重新创建 widget。
```

## 完整示例

以下是一个完整的 ImageWidget 交互示例，展示如何动态生成和更新图像：

```{literalinclude} ../../../../examples/viewer/image_widget.py
:language: python
:dedent:
:start-after: "# Copyright (C)"
:end-before: 'if __name__ == "__main__"'
```

**ImageWidget 控制说明**：

-   **SPACE**: 重新生成所有图像
-   **1/2/3**: 切换 widget1 的图像类型（随机噪声/渐变/棋盘格）
-   **w/a/s/d**: 移动 widget1 位置（上/左/下/右）
-   **+/-**: 调整 widget1 大小
-   **r**: 重置所有布局

## 性能优化建议

1. **图像更新频率**:

    - 对于实时传感器数据，建议使用 `image.pixels = new_pixels` 方法
    - 避免在高频循环中创建新的 Image 对象
    - 合理设置更新频率，避免超过渲染帧率

2. **图像尺寸优化**:

    - 使用合适的图像分辨率，避免不必要的过大的图像
    - 对于小尺寸 widget，使用较小的图像可以提高性能
    - 考虑使用图像金字塔或多分辨率显示

3. **内存管理**:
    - 复用 Image 对象，而不是频繁创建新的
    - 及时移除不再需要的 widget
    - 注意 numpy 数组的内存管理，避免内存泄漏

## 相关 API 链接

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
