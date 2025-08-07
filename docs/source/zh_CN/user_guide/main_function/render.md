# 🎨 渲染器（RenderApp）

## 启动与加载

[`RenderApp`] 负责基本的场景渲染。一般的，在代码中创建一个 [`RenderApp`] 实例，通过 [`load_model`] 加载模型后调用 [`render.launch(model)`] 来为渲染器加载模型。

## 同步

在主循环中，推荐每经过一次物理模拟 step 之后，调用 [`render.sync(data)`] 进行渲染双向同步更新。

用户也可按实际需求自行调整 step 与 sync 之间的倍率。

同步的内容包括：

-   向渲染器发送物理模拟数据、自定义 UI 组件、gizmos 绘制等指令
-   从渲染器获取 IO 输入事件。

### 自定义 UI 组件

目前支持按钮 [`add_button`] 与复选框 [`add_toggle`] 两种组件，通过设置回调函数的方式来响应用户的点击事件。

用户需要通过 [`render.opt.set_left_panel_vis(True)`] 来显示左侧面板，组件会按添加顺序显示在面板上。

```{literalinclude} ../../../../examples/custom_ui.py
:language: python
:dedent:
:start-after: "# tag::custom_ui[]"
:end-before:  "# end::custom_ui[]"
```

_完整代码见 [examples/custom_ui.py](../../../../examples/custom_ui.py)_

### Gizmos 绘制

Gizmos 是一种用于辅助调试的图形元素，渲染器提供了一个简单的 API 来绘制 gizmos。

Gizmos 采用即时模式，即使不需要更新，用户也需要在每次渲染同步时添加 gizmos。

目前支持球体 [`draw_sphere`] 与立方体 [`draw_cuboid`] 两种形状的 gizmos。

```{literalinclude} ../../../../examples/gizmos.py
:language: python
:dedent:
:start-after: "# tag::draw_gizmos[]"
:end-before:  "# end::draw_gizmos[]"
```

_完整代码见 [examples/gizmos.py](../../../../examples/gizmos.py)_

### IO 输入事件

通过 [`render.input`] 可以获取到[`Input`]对象，Input 对象提供了一系列方法，用于查询渲染器的鼠标、键盘以及 UI 事件。

您可以通过以下的例子来了解更详细的用法：

-   [example/mouse_click.py](../../../../examples/mouse_click.py)
-   [example/read_keyboard.py](../../../../examples/read_keyboard.py)

## 摄像头控制

渲染器提供了一个自由的摄像头控制系统，用户可以通过鼠标操作来控制摄像头的视角和焦点（始终位于屏幕中心）。

-   鼠标左键按下并拖动：绕着焦点旋转摄像头
-   鼠标右键按下并拖动：移动焦点（此时显示红圈为焦点）
-   鼠标滚轮：缩放（到焦点位置不可再放大）

## 单模型多实例渲染

[`render.launch(model)`] 还有 repeat:int 与 render_offset:List[:3] 两个可选参数，在需要单个模型多实例渲染时，分别用于设置实例数与偏移位置。

```{literalinclude} ../../../../examples/model.py
:language: python
:dedent:
:start-after: "model = load_model(path)"
:end-before:  "# Create the physics data of the model"
```

_完整代码见 [examples/model.py](../../../../examples/model.py)_

[`RenderApp`]: motrixsim.render.RenderApp
[`load_model`]: motrixsim.load_model
[`render.launch(model)`]: motrixsim.render.RenderApp.launch
[`render.sync(data)`]: motrixsim.render.RenderApp.sync
[`render.input`]: motrixsim.render.RenderApp.input
[`Input`]: motrixsim.render.Input
[`render.opt.set_left_panel_vis(True)`]: motrixsim.render.RenderOpt.set_left_panel_vis
[`add_button`]: motrixsim.render.RenderUI.add_button
[`add_toggle`]: motrixsim.render.RenderUI.add_toggle
[`draw_sphere`]: motrixsim.render.RenderGizmos.draw_sphere
[`draw_cuboid`]: motrixsim.render.RenderGizmos.draw_cuboid
