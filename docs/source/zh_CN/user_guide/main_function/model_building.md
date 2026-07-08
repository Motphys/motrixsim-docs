# 🔨 程序化模型构建

`motphys-scene-descriptor`（下文简称 `MSD`）是 MotrixSim 的场景描述与组合能力。在 Python 侧，它通过 [`motrixsim.msd`](../../api_reference/msd/msd.md) 暴露给用户。

如果把仿真流程拆成两个阶段：

1. 场景描述与组装阶段（可变）
2. 物理仿真运行阶段（高性能、稳定）

那么 `MSD` 就是第 1 阶段的核心工具，负责把 MJCF、URDF 和 USD 资产组织、变换、组合后，构建成可仿真的 [`SceneModel`](scene_model.md)。

## 它解决了什么问题

在机器人或多体系统开发中，常见需求是：

-   同一机器人挂载不同末端执行器
-   同一个模型在场景里实例化多份
-   从大模型中提取子树拼接到另一个模型
-   在仿真前统一做平移、旋转和命名空间管理

如果直接在原始模型文件里反复手改，维护成本高且容易出错。`MSD` 的关键价值是把不同来源的资产先统一到同一个 `World` 空间，再做程序化操作：

-   MJCF、URDF 或 USD 可通过 `msd.from_file` 读入 `World`
-   动态生成的 MJCF/URDF 字符串可通过 `msd.from_str` 读入 `World`
-   统一后就能用同一套 `attach/transform/prefix/build` 流程完成组装与编译

```{figure} /_static/images/msd/msd-unified-space.svg
:alt: MSD unified asset space
:width: 100%
:align: center

MSD 将 MJCF/URDF/USD 等不同资产格式统一到同一可编排空间。
```

## 5 分钟快速上手

### 第一步：加载场景与模型

```python
import motrixsim as mx

scene = mx.msd.from_file("examples/assets/store/scene.xml")
robot = mx.msd.from_file("examples/assets/boston_dynamics_spot/spot.xml")
```

### 第二步：把模型附加到场景

```python
scene.attach(
    robot,
    other_translation=[1.0, 0.0, 0.0],
    other_prefix="spot_",
)
```

### 第三步：构建为可仿真的 SceneModel

```python
model = scene.build()
data = mx.SceneData(model)
mx.step(model, data)
```

上面这三步就是最常见的 `MSD` 工作流：`加载 -> 组合 -> build -> 仿真`。

### 完整示例代码

```python
import motrixsim as mx

robot = mx.msd.from_file("robot.xml")
full_arm = mx.msd.from_file("arm_with_base.xml")

# 只附加 "forearm" 子树，而不是整个手臂模型
robot.attach(
    full_arm,
    self_link_name="shoulder",
    other_link_name="forearm",  # 从此连杆提取
    other_prefix="arm_"
)

model = robot.build()
```

## 完整示例

以下是一个创建包含多个机器人场景的完整示例。完整代码请参阅 [`examples/physics/combine_msd.py`](../../../../examples/physics/combine_msd.py)。

```{literalinclude} ../../../../examples/physics/combine_msd.py
:language: python
:start-after: "# tag::combine_msd_example[]"
:end-before: "# end::combine_msd_example[]"
```

## 核心概念

| 概念        | 说明                                                          |
| ----------- | ------------------------------------------------------------- |
| `World`     | `MSD` 的可变场景对象。可以持续 `attach`、增删元素、设置变换。 |
| `attach`    | 把另一个 `World` 合并到当前场景，可设置挂接点、位姿、前后缀。 |
| `build`     | 把 `World` 编译成不可变的 `SceneModel`，用于实际仿真。        |
| `base_path` | 解析纹理、网格等相对路径的基准目录，文件引用场景必须明确。    |

## 常用接口速览

| 接口                                                                | 用途                                     |
| ------------------------------------------------------------------- | ---------------------------------------- |
| [`msd.from_file(path)`](motrixsim.msd.from_file)                    | 从 MJCF、URDF 或 USD 文件加载 `World`    |
| [`msd.from_str(string, format, base_path)`](motrixsim.msd.from_str) | 从字符串加载，适合动态生成模型           |
| [`World.attach(...)`](motrixsim.msd.World.attach)                   | 组合模型，支持平移旋转、前后缀、子树提取 |
| [`World.build(base_path)`](motrixsim.msd.build)                     | 构建最终 `SceneModel`                    |

完整 API 参见：[`motrixsim.msd`](../../api_reference/msd/msd.md)。

## FAQ

1. Q：我已经有 MJCF/URDF，还需要手写 MSD 吗？  
   A：通常不需要。可以直接 `msd.from_file(...).build()`，只有在“程序化组合/编辑”场景下才需要深入使用 MSD 对象。

2. Q：我可以复用同一个被附加模型多次吗？  
   A：可以。`attach` 时会内部克隆 `other`，适合批量实例化同一个子模型。

3. Q：USD 场景如何接入？  
   A：如果只需要直接仿真，使用 `motrixsim.load_model(...)` 加载为 `SceneModel`；如果需要先和其他 `MSD` world 组合，使用 `motrixsim.msd.from_file(...)` 转换。二者都需要安装 `usd` extra。
