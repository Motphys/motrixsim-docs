# 🔋 驱动器

驱动器 (Actuator) 是控制机器人关节运动的核心组件，MotrixSim 支持多种类型的驱动器。

每个驱动器都可以配置不同的类型和参数，以适应不同的应用场景。
驱动器可以是马达、位置控制器、速度控制器或通用控制器等。它们通过设置目标位置、速度或其他参数来实现对机器人的精确控制。

现支持的驱动器类型有：

| 类型             | 解释                                               |
| :--------------- | :------------------------------------------------- |
| 马达（Motor）    | 用于驱动机器人的关节，提供基本的运动能力。         |
| 位置（Position） | 精确控制关节的角度或位置。                         |
| 速度（Velocity） | 控制关节的运动速度。                               |
| 通用（General）  | 提供更灵活的控制方式，可以根据需要自定义控制策略。 |

设置可兼容 [MuJoCo actuator](https://mujoco.readthedocs.io/en/stable/XMLreference.html#actuator) 的参数。

> General 部分属性未支持，参照 [支持列表](../getting_started/mjcf_reference.md)。

## 驱动器示例

首先加载模型 [`model`] 并通过 [`model.get_actuator`] 方法获取指定的 [`Actuator`]，参数可以是驱动器的名称或索引。
然后通过 [`actuator.set_ctrl`] 方法设置控制目标值。

索引与文件中定义顺序一致，可通过 [`model.actuator_names`] 方法获取所有驱动器的名称列表。

以下是涵盖上述所有内容的完整代码脚本：

```{literalinclude} ../../../../examples/physics/actuator.py
:language: python
:dedent:
```

[`Actuator`]: motrixsim.Actuator
[`model`]: motrixsim.SceneModel
[`model.get_actuator`]: motrixsim.SceneModel.get_actuator
[`actuator.set_ctrl`]: motrixsim.Actuator.set_ctrl
[`model.actuator_names`]: motrixsim.SceneModel.actuator_names
