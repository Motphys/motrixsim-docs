# 🏗️ 模型

MotrixSim 中的模型 `SceneModel` 和数据 `SceneData` 是构建仿真环境的必要组成对象，贯穿整个物理仿真过程。本章节主要介绍 `SceneModel` 的创建和使用方法，而 [`SceneData`](scene_data.md) 将在下一章节详细描述。

## 基本概念

`SceneModel` 是对模型的描述，即所有**不随时间变化的量**。这包括几何形状、质量属性、关节连接关系、执行器配置等静态信息。在整个仿真过程中，`SceneModel` 保持不变，而所有随时间变化的动态状态（位置、速度、力等）都存储在 `SceneData` 中。

`SceneModel` 主要包含以下内容：

| 分类     | 说明                                                                                                                                                                                                                                                                                                     |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 模型组件 | 关节 [`Joint`](../kinematics/joint.md)、刚体 [`Body`](../kinematics/body.md)、连杆 [`Link`](../kinematics/link.md)、几何体[`Geometry`](../kinematics/geometry.md)、传感器 [`Sensor`](../kinematics/sensor.md)、执行器 [`Actuator`](../kinematics/actuator.md)、参考点 [`Site`](../kinematics/site.md) 等 |
| 仿真参数 | [`Options`](options.md)（包括 `timestep`、`gravity` 等）                                                                                                                                                                                                                                                 |

## 创建模型

### 从文件加载

使用 `motrixsim.load_model(path)` 可以将 MJCF、URDF 或 USD 文件加载为 `SceneModel`。

USD 场景也使用同一个加载入口，但需要安装可选的 `usd` extra：

```bash
pip install "motrixsim[usd]"
```

使用 `uv` 时：

```bash
uv add "motrixsim[usd]"
```

请在运行 MotrixSim 的同一个 Python 环境中安装这个 extra。如果已经安装过不带 USD 支持的 MotrixSim，可以在同一个环境中重新运行上面的命令，以补齐可选 USD 依赖。当前 USD 转换支持范围见 [USD 支持参考](../getting_started/usd_reference.md)。

下面的示例使用 `load_model` 加载 MJCF 场景：

```{literalinclude} ../../../../examples/getting_started/empty.py
:language: python
:dedent:
:start-after: "# tag::load_model_from_file[]"
:end-before:  "# end::load_model_from_file[]"
```

完整示例代码参见 [`examples/getting_started/empty.py`](../../../../examples/getting_started/empty.py)。

对于 USD 场景，使用同一个入口即可直接加载为 `SceneModel`：

```python
import motrixsim as mx

model = mx.load_model("scene.usda")
data = mx.SceneData(model)
```

### 从字符串加载

也可以直接从 MJCF 字符串创建模型：

```{literalinclude} ../../../../examples/getting_started/load_from_str.py
:language: python
:dedent:
:start-after: "# tag::model_load_from_string[]"
:end-before:  "# end::model_load_from_string[]"
```

完整示例代码参见 [`examples/getting_started/load_from_str.py`](../../../../examples/getting_started/load_from_str.py)。

## 组件访问 (Named Access)

创建模型后，我们通常需要访问模型中的组件来设置参数、获取信息或进行控制。MotrixSim 为模型组件提供了便捷的命名访问接口，支持通过**名称**或**索引**直接访问各种组件。

下面通过 `joint` 的访问示例，展示如何通过名称和索引来进行访问。完整示例代码参见 [`examples/physics/joint.py`](../../../../examples/physics/joint.py)。

### 基本访问方式

-   通过**名称**访问

```python
 hinge = model.get_joint("hinge")
```

-   通过**索引**访问 （也提供了从名称到索引的接口）

```{literalinclude} ../../../../examples/physics/joint.py
:language: python
:dedent:
:start-after: "# tag::joint_index[]"
:end-before:  "# end::joint_index[]"
```

### 批量访问

除了单个组件访问，还可以批量获取组件对象或名称列表：

```{literalinclude} ../../../../examples/physics/joint.py
:language: python
:dedent:
:start-after: "# tag::access_all[]"
:end-before:  "# end::access_all[]"
```

访问方式支持 [`基本概念`]中提到的模型组件。详细的访问方法，请参阅：[**API 快速参考 - Named Access**](../../api_reference/api_quick_reference.md#-named-access---模型组件访问)。

## API Reference

更多与 SceneModel 相关的 API，请参考 [`SceneModel API`]

[`SceneModel API`]: motrixsim.SceneModel
[`基本概念`]: #基本概念

```{toctree}
:caption: 模型组件
:maxdepth: 1

../kinematics/body
../kinematics/floating_base
../kinematics/joint
../kinematics/link
../kinematics/geometry
../kinematics/actuator
../kinematics/sensor
../kinematics/site
```
