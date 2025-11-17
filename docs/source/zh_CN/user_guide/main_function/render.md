# 🎨 渲染器（RenderApp）

## 启动与加载

[`RenderApp`] 负责基本的场景渲染。一般的，在代码中创建一个 [`RenderApp`] 实例，通过 [`load_model`] 加载模型后调用 [`render.launch(model)`] 来为渲染器加载模型。

## 同步

在主循环中，推荐每经过一次物理模拟 step 之后，调用 [`render.sync(data)`] 进行渲染双向同步更新。

用户也可按实际需求自行调整 step 与 sync 之间的倍率。

同步的内容包括：

-   向渲染器发送物理模拟数据、自定义 UI 组件、gizmos 绘制等指令
-   从渲染器获取 IO 输入事件。

### 渲染配置

当前，有配置项`RenderSettings`来进行全局渲染配置：
| 参数名 | 解释 | 默认值 |
| :------- | :---------------------------: | :-------:|
| simplify_render_mesh | 是否自动进行网格的简化 | False |
| enable_shadow | 是否启用灯光阴影 | True |
| enable_ssao | 是否启用屏幕空间环境光遮蔽 | True |
| enable_oit | 是否启用顺序无关透明渲染 | True |

特别的，当且仅当全局配置开启，且场景描述文件（mjcf/msd）中也启用某些渲染项时，才会有最终的效果。

_示例代码见 [examples/render_settings.py](../../../../examples/render_settings.py)_

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

| 方法名             |        释义         |
| :----------------- | :-----------------: |
| draw_sphere        |    绘制线框球形     |
| draw_cuboid        |    绘制线框矩体     |
| draw_cylinder      |   绘制线框圆柱体    |
| draw_capsule       |   绘制线框胶囊体    |
| draw_ray           |      绘制射线       |
| draw_line          |      绘制线段       |
| draw_arrow         |      绘制箭头       |
| draw_rect          |    绘制 2D 矩形     |
| draw_grid          |    绘制 3D 栅格     |
| draw_axes          |     绘制坐标轴      |
| set_draw_collider  | 开启/关闭碰撞体绘制 |
| set_draw_joint     |  开启/关闭关节绘制  |
| set_draw_site      | 开启/关闭参考点绘制 |
| set_collider_color | 设置碰撞体绘制颜色  |
| set_joint_color    |  设置关节绘制颜色   |
| set_line_width     |  设置绘制线段宽度   |
| set_joint_size     |  设置关节绘制大小   |

Gizmos 采用即时模式，即使不需要更新，用户也需要在每次渲染同步时添加 gizmos。

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

#### 合法键盘输入列表

以下是支持的键盘按键输入列表：

| 按键类型 |           示例按键            |
| :------- | :---------------------------: |
| 字母键   |      `A`, `B`, ..., `Z`       |
| 功能键   |    `F1`, `F2`, ..., `F12`     |
| 特殊键   |    `Enter`, `Esc`, `Space`    |
| 方向键   | `Up`, `Down`, `Left`, `Right` |

> 注意：以上均不区分大小写，表格内未提及的键位暂不支持。

## 摄像头控制

渲染器提供了一个自由的摄像头控制系统，用户可以通过鼠标操作来控制摄像头的视角和焦点（始终位于屏幕中心）。

-   鼠标左键按下并拖动：绕着焦点旋转摄像头
-   鼠标右键按下并拖动：移动焦点（此时显示红圈为焦点）
-   鼠标滚轮：缩放（到焦点位置不可再放大）

## 单模型多实例渲染

[`render.launch(model)`] 还有 batch:int 与 render_offset:List[:3] 两个可选参数，在需要单个模型多实例渲染时，分别用于设置实例数与偏移位置。

```{literalinclude} ../../../../examples/model.py
:language: python
:dedent:
:start-after: "model = load_model(path)"
:end-before:  "# Create the physics data of the model"
```

_完整代码见 [examples/model.py](../../../../examples/model.py)_

### 实例可见性

当我们进行单模型多实例渲染时，可以按需配置每一个实例的渲染可见性。

```
...
# 创建多个实例
render_offsets = []
batch = 10
for i in range(batch):
    render_offsets.append([i * 2.0, 0, 0])
render.launch(model, batch, render_offsets)
data = SceneData(model, batch=(batch,))

target_scene_indices = [1, 3, 5, 7, 9] # 指定实例索引
render.set_scene_vis(target_scene_indices, False) # 隐藏目标实例
render.set_scene_vis(target_scene_indices, True) # 显示目标实例
```

也可以全局开启/关闭：

```
render.set_all_scene_vis(False) # 隐藏所有实例
render.set_all_scene_vis(True) # 显示所有实例
```

上述操作仅影响渲染可见性，不影响对象的物理仿真。

_完整代码见 [examples/partial_rendering.py](../../../../examples/partial_rendering.py)_

[`RenderApp`]: motrixsim.render.RenderApp
[`load_model`]: motrixsim.load_model
[`render.launch(model)`]: motrixsim.render.RenderApp.launch
[`render.sync(data)`]: motrixsim.render.RenderApp.sync
[`render.input`]: motrixsim.render.RenderApp.input
[`Input`]: motrixsim.render.Input
[`render.opt.set_left_panel_vis(True)`]: motrixsim.render.RenderOpt.set_left_panel_vis
[`add_button`]: motrixsim.render.RenderUI.add_button
[`add_toggle`]: motrixsim.render.RenderUI.add_toggle
