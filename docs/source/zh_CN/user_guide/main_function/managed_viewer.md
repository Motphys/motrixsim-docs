# 🎮 交互式查看器（Interactive Viewer）

## 概述

交互式查看器提供了一个简化的接口，用于快速可视化和交互物理仿真。[`viewer.launch()`] 函数以阻塞模式运行，这意味着在查看器窗口关闭之前，它不会将控制权返回给你的 Python 代码。这种阻塞行为能够实现精确的物理循环时序和自动化的仿真处理。

与需要手动同步和循环管理的底层 [`RenderApp`] API 不同，交互式查看器会自动处理仿真循环、渲染同步和常用的 UI 控制。

![Interactive Viewer 界面概览](/_static/images/interactive_viewer_overview.png)

## 使用场景

交互式查看器专为以下场景设计：

-   **快速可视化模型**：用最少的代码测试和检查物理仿真
-   **交互式调试**：使用内置播放控件检查仿真行为
-   **教学演示**：专注于物理概念而无需处理渲染复杂性
-   **原型开发**：快速迭代模型设计和行为
-   **简单应用**：当不需要自定义渲染逻辑或非阻塞执行时

对于需要对仿真循环进行细粒度控制的生产应用，请考虑使用 [`RenderApp`]。

### 主要特性

-   **阻塞执行**：运行直到窗口关闭，支持精确的物理循环时序
-   **自动仿真循环**：物理步进和渲染自动处理
-   **内置控件**：开箱即用的播放/暂停、重置、单步执行和速度控制
-   **多种调用模式**：支持空会话、仅模型、模型和数据三种模式
-   **文件加载**：直接将 XML 模型文件拖入查看器窗口即可即时加载
-   **零配置**：使用合理的默认值即可工作，但在需要时可自定义

## 命令行接口

交互式查看器也可以直接从命令行启动：

```bash
# 使用指定模型文件启动
uv run python -m motrixsim.interactive_viewer --file=path/to/your/model.xml

# 启动空查看器（拖放模型文件即可加载）
uv run python -m motrixsim.interactive_viewer
```

### CLI 参数

| 参数     | 必需 | 描述                                                                 |
| -------- | ---- | -------------------------------------------------------------------- |
| `--file` | 否   | 模型文件路径。如果不提供，将启动空查看器，可以通过拖放模型文件加载。 |

### 示例

```bash
# 使用指定模型启动查看器
uv run python -m motrixsim.interactive_viewer --file=examples/assets/boston_dynamics_spot/scene_arm.xml

# 启动空查看器进行拖放交互
uv run python -m motrixsim.interactive_viewer
```

CLI 提供了一种无需编写 Python 代码即可快速可视化模型的方式。当提供文件参数时，它会自动：

-   加载指定的模型
-   创建具有初始状态的场景数据
-   运行几个物理步骤以稳定仿真
-   启动交互式查看器

不带参数启动时，你可以直接将 XML 模型文件拖入查看器窗口即可即时加载。

```{note}
如需对初始条件或自定义回调进行更多控制，请直接使用 Python API 的 [`viewer.launch()`]。
```

## 使用模式

[`viewer.launch()`] 函数支持三种不同的调用模式以适应不同的使用场景：

### 1. 空会话（默认模型）

```python
import motrixsim as mx

# 使用默认演示模型启动
mx.viewer.launch()
```

使用默认演示模型启动交互式可视化会话。这是探索查看器功能最快捷的方式。

**提示：** 你还可以直接将 XML 模型文件拖入查看器窗口来即时加载，这样可以轻松快速预览不同的模型，无需编写代码。

### 2. 仅模型

```python
import motrixsim as mx

# 加载你的模型
model = mx.load_model("path/to/your/model.xml")

# 启动查看器 - 将自动创建内部 SceneData
mx.viewer.launch(model)
```

为给定模型启动可视化会话。查看器会在内部自动创建自己的 [`SceneData`] 实例用于仿真。

### 3. 模型和数据

```python
import motrixsim as mx
from motrixsim import SceneData

# 加载模型并创建数据
model = mx.load_model("path/to/your/model.xml")
data = SceneData(model)

# 配置初始状态
data.qpos[:] = initial_positions
data.qvel[:] = initial_velocities

# 使用初始数据启动查看器
mx.viewer.launch(model, data)
```

使用提供的 [`SceneData`] 实例作为仿真的初始状态。查看器会为其仿真循环创建数据的内部副本。此模式在以下情况下很有用：

-   设置特定的初始条件（位置、速度、控制输入）
-   在可视化之前运行稳定步骤
-   从特定的仿真状态启动查看器

### 预仿真示例

在启动查看器之前运行一些物理步骤以稳定初始状态：

```{literalinclude} ../../../../examples/interactive_viewer.py
:language: python
:dedent:
:start-after: "# Use custom model with physics data"
:end-before: "viewer.launch(model, data)"
```

这种预仿真方法特别适用于：

-   允许初始接触力稳定
-   达到稳定的平衡配置
-   在可视化之前预计算派生量

## 完整示例

以下是一个使用波士顿动力 Spot 机器人演示交互式查看器的完整示例：

```{literalinclude} ../../../../examples/interactive_viewer.py
:language: python
:dedent:
:start-after: "# Copyright (C)"
```

此示例：

1. 加载带有机械臂的 Spot 机器人模型（包含执行器）
2. 创建场景数据
3. 运行 20 个物理步骤以稳定仿真
4. 启动交互式查看器

## 内置控件

交互式查看器提供了几个通过 UI 访问的内置控件：

| 控件          | 功能                         |
| ------------- | ---------------------------- |
| **播放/暂停** | 启动或暂停仿真               |
| **重置**      | 将仿真重置为初始状态         |
| **单步执行**  | 将仿真推进一步（暂停时）     |
| **速度控制**  | 调整仿真速度（慢动作到快进） |

额外的鼠标控制：

-   **左键拖拽**：围绕焦点旋转相机
-   **右键拖拽**：移动焦点
-   **鼠标滚轮**：放大/缩小

```{tip}
按空格键可以快速切换播放和暂停状态。
```

## 与 RenderApp 的对比

交互式查看器和 [`RenderApp`] 服务于不同的使用场景：

| 特性         | 交互式查看器         | RenderApp                    |
| ------------ | -------------------- | ---------------------------- |
| **执行模式** | 阻塞（运行直到关闭） | 非阻塞（手动控制）           |
| **仿真循环** | 自动                 | 手动（`step()` 调用）        |
| **同步**     | 自动                 | 手动（`render.sync()` 调用） |
| **使用场景** | 快速可视化、原型开发 | 生产应用、自定义逻辑         |
| **控制流**   | 查看器控制流程       | 你控制流程                   |
| **自定义**   | 有限                 | 完全控制                     |

### 何时使用

**使用交互式查看器：**

-   快速测试或调试模型
-   创建教学演示
-   构建简单的交互式工具
-   你需要最少的代码

**使用 RenderApp：**

-   与现有应用程序逻辑集成
-   需要对渲染时机进行细粒度控制
-   构建生产应用程序
-   实现自定义 UI 或可视化
-   运行带有可选渲染的无头仿真

## 最佳实践

### 模型加载

```python
# 好：绝对或相对路径
model = mx.load_model("examples/assets/boston_dynamics_spot/scene_arm.xml")

# 好：使用 pathlib 实现跨平台兼容性
from pathlib import Path
model_path = Path(__file__).parent / "assets" / "model.xml"
model = mx.load_model(str(model_path))
```

### 数据初始化

```python
# 初始化数据
data = SceneData(model)

# 设置初始配置
data.qpos[:] = initial_positions
data.qvel[:] = initial_velocities

# 运行几个步骤以稳定
for _ in range(10):
    mx.step(model, data)

# 启动查看器
mx.viewer.launch(model, data)
```

## 限制和注意事项

```{warning}
交互式查看器是阻塞的 - 你的 Python 代码不会继续执行，直到查看器窗口关闭。如果你需要并发执行，请使用 [`RenderApp`]。
```

**其他注意事项：**

-   **单窗口**：一次只能有一个交互式查看器处于活动状态
-   **无多实例渲染**：对于批量渲染，请使用 [`RenderApp`]
-   **有限的自定义**：对于自定义 UI 或高级渲染功能，请使用 [`RenderApp`]

## 相关文档

-   [渲染器（RenderApp）](render.md) - 具有完全控制的底层渲染 API
-   [相机](../render/camera.md) - 相机控制和配置
-   [组件部件](../render/widgets.md) - 多视口渲染

### API 参考

-   [`viewer.launch()`]
-   [`SceneModel`]
-   [`SceneData`]
-   [`step()`]

[`RenderApp`]: motrixsim.render.RenderApp
[`viewer.launch()`]: motrixsim.viewer.launch
[`SceneModel`]: motrixsim.SceneModel
[`SceneData`]: motrixsim.SceneData
[`step()`]: motrixsim.step
