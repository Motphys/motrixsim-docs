# 🖼️ Widget 组件

## 概述

Widget 系统允许您在渲染窗口中创建多个可视化的组件，包括相机视口（CameraViewport）和自定义图像（ImageWidget）。这对于多视角观察、传感器数据可视化、自定义 UI 显示等场景非常有用。

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

-   **多种 Widget 类型**: 支持相机视口（CameraViewport）和自定义图像（ImageWidget）
-   **多组件支持**: 在同一窗口中创建多个独立的 widget 组件
-   **灵活布局**: 支持像素、百分比和自动三种布局格式
-   **动态更新**: 实时更新 widget 的内容、布局和属性

## Widget 类型

MotrixSim 提供以下两种 Widget 类型：

```{toctree}
:maxdepth: 1

camera_viewport
image_widget
```

### 核心概念

在开始使用 widget 之前，需要了解以下几个核心概念：

-   **Layout（布局）**: 配置 widget 的位置和大小
-   **CameraViewport（相机视口）**: 显示相机画面的 widget 组件
-   **ImageWidget（图像组件）**: 显示自定义图像的 widget 组件
-   **RenderWidgets（Widget 接口）**: 创建和管理 widget 的主要接口

## Layout 配置系统

Layout 类用于配置 widget 在屏幕上的位置和大小。它提供了 6 个布局参数：

-   **left**: 左侧位置
-   **right**: 右侧位置
-   **top**: 顶部位置
-   **bottom**: 底部位置
-   **width**: 宽度
-   **height**: 高度

### 布局格式

Layout 参数支持三种格式：

#### 像素格式

直接使用数值表示像素：

```python
layout = Layout(left=50, top=50, width=200, height=150)
```

这表示 widget 距离左侧 50 像素，距离顶部 50 像素，宽度 200 像素，高度 150 像素。

#### 百分比格式

使用字符串表示百分比：

```python
layout = Layout(left="10%", top="10%", width="30%", height="30%")
```

这表示 widget 距离左侧 10%，距离顶部 10%，宽度占 30%，高度占 30%。

#### 自动格式

使用"auto"字符串表示自动布局：

```python
layout = Layout(width="auto", height="auto")
```

宽度和高度会根据内容自动调整。

#### 混合格式

可以混合使用不同的格式：

```python
layout = Layout(left=10, top="60%", width=320, height=240)
```

这表示左侧距离 10 像素，顶部距离 60%，宽度 320 像素，高度 240 像素。

### 布局示例

以下示例展示了三种不同的布局格式：

```{literalinclude} ../../../../examples/viewer/camera_viewport.py
:language: python
:dedent:
:start-after: "# Viewport 1: Top-left with pixel-based layout"
:end-before: "# Store initial layouts"
```

```{note}
您可以根据实际需求选择合适的布局格式。像素布局适合固定UI，百分比布局适合响应式设计。
```

## 最佳实践与注意事项

### 性能优化建议

```{warning}
避免频繁创建和销毁widget，这会影响性能。建议在初始化时创建所有需要的widget，然后使用update()方法动态更新它们的属性。
```

### 布局建议

1. **像素布局**: 适用于固定 UI 元素，如按钮、面板等
2. **百分比布局**: 适用于需要响应式设计的场景
3. **避免重叠**: 确保多个 widget 不会重叠，以免相互遮挡
4. **预加载布局**: 在初始化时设置好所有 widget 的布局，减少运行时调整

## 相关 API 链接

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
