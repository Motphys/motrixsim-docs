# 📹 CameraViewport

## 概述

CameraViewport 允许您在渲染窗口中创建多个相机视口组件，用于同时显示不同相机的实时渲染画面。这对于多角度观察、传感器数据可视化等场景非常有用。

```{video} /_static/videos/rgbd_camera.mp4
:caption: 右上角展示了使用 Camera Viewport Widget 组件显示的 RGBD 传感器画面
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

### 主要特性

-   **多视口支持**: 在同一窗口中创建多个独立的相机视口
-   **灵活布局**: 支持像素、百分比和自动三种布局格式
-   **动态更新**: 实时更新视口的相机、布局和属性

## 基础创建方法

使用 `render.widgets.create_camera_viewport()` 方法创建相机视口 widget：

```python
viewport = render.widgets.create_camera_viewport(
    camera=cameras[0],
    layout=Layout(left=10, top=10, width=240, height=180),
    sim_world_index=0
)
```

**参数说明**：

-   **camera**: 要显示的相机对象（必需）
-   **layout**: 布局配置（可选，默认为 left=50, top=50, width=200, height=200）
-   **sim_world_index**: 模拟世界索引（可选，默认为 0）

**返回值**：返回一个 `CameraViewport` 对象。

## 创建多个 Viewport

您可以在同一窗口中创建多个 viewport，每个显示不同相机的画面：

```{literalinclude} ../../../../examples/viewer/camera_viewport.py
:language: python
:dedent:
:start-after: "# Viewport 1: Top-left with pixel-based layout"
:end-before: "# Store initial layouts"
```

这段代码创建了三个 viewport：

-   **vp1**: 左上角，使用像素布局，显示 cameras[0]
-   **vp2**: 右上角，使用百分比布局，显示 cameras[1]
-   **vp3**: 左下角，使用混合布局，显示 cameras[0]

![camera viewport](/_static/images/examples/camera_viewport.png)

## Widget 动态更新

创建 widget 后，可以通过 `update()` 方法动态更新其属性。

### 更新 Viewport 属性

`CameraViewport.update()` 方法支持以下参数：

-   **camera**: 新的相机对象
-   **layout**: 新的布局配置
-   **sim_world_index**: 新的模拟世界索引

所有参数都是可选的，只提供需要更新的参数即可。

### 更新相机

切换 viewport 显示的相机：

```python
viewport.update(camera=cameras[1])
```

### 更新布局

修改 viewport 的位置和大小：

```python
viewport.update(layout=Layout(left=100, top=100, width=300, height=200))
```

### 组合更新

可以同时更新多个属性：

```python
viewport.update(
    camera=cameras[2],
    layout=Layout(left=200, top=200),
    sim_world_index=0
)
```

## 交互式控制示例

以下示例展示了如何通过按键交互来更新 widget：

### 切换相机

```{literalinclude} ../../../../examples/viewer/camera_viewport.py
:language: python
:dedent:
:start-after: "# Switch vp1 camera"
:end-before: "# Move vp1 viewport"
```

按 1/2/3 键可以切换 vp1 显示的相机。

### 移动 Viewport 位置

```{literalinclude} ../../../../examples/viewer/camera_viewport.py
:language: python
:dedent:
:start-after: "# Move vp1 viewport"
:end-before: "# Resize vp1 viewport"
```

按 w/a/s/d 键可以移动 vp1 的位置。

### 调整 Viewport 大小

```{literalinclude} ../../../../examples/viewer/camera_viewport.py
:language: python
:dedent:
:start-after: "# Resize vp1 viewport"
:end-before: "# Reset all layouts"
```

按 +/- 键可以调整 vp1 的大小。

## 移除 Viewport

如果不再需要某个 viewport，可以使用 `remove()` 方法将其完全从渲染窗口中移除：

```python
viewport.remove()
```

```{warning}
调用 `remove()` 方法后，该 viewport 将被永久移除。后续对该 viewport 对象调用 `update()` 方法将导致错误。如果需要重新显示，必须重新创建 viewport。
```

以下示例展示了如何通过按键交互来移除 viewport：

```{literalinclude} ../../../../examples/viewer/camera_viewport.py
:language: python
:dedent:
:start-after: "# Remove vp3 from screen"
:end-before: "# Sync render with simulation"
```

按 k 键可以移除 vp3。移除后，vp3 将从屏幕上完全消失，且无法通过 update 方法恢复。

## 完整示例

以下是一个完整的交互式 CameraViewport widget 系统，包含创建、更新、交互控制等功能：

```{literalinclude} ../../../../examples/viewer/camera_viewport.py
:language: python
:dedent:
:start-after: "# Copyright (C)"
:end-before: 'if __name__ == "__main__"'
```

## 相关 API 链接

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
