# 🔨 模型构建

MotrixSim 提供了程序化模型构建 API，允许您在仿真前加载、变换和组合多个模型。这对以下场景非常有用：

-   将机器人模型与不同的末端执行器组合
-   创建多机器人场景
-   在运行时动态组装模型

## 基本概念

模型构建 API 通过 [`motrixsim.msd`](../../api_reference/msd/msd.md) 模块提供：

| 类/函数                                                  | 描述                                                                    |
| -------------------------------------------------------- | ----------------------------------------------------------------------- |
| [`msd.from_file(path)`](motrixsim.msd.from_file)         | 加载模型文件（MJCF/URDF/MSD）并返回 [`Scene`](motrixsim.msd.Scene) 对象 |
| [`msd.from_str(string, format)`](motrixsim.msd.from_str) | 从字符串加载模型                                                        |
| [`Scene.attach(other, ...)`](motrixsim.msd.Scene.attach) | 将另一个模型附加到当前模型                                              |
| [`Scene.build()`](motrixsim.msd.Scene.build)             | 构建用于仿真的最终 [`SceneModel`](motrixsim.SceneModel)                 |

[`Scene`](motrixsim.msd.Scene) 对象是模型的可变表示，可以在编译为不可变的 [`SceneModel`](motrixsim.SceneModel) 之前进行变换和组合。

## 基本用法

### 加载和构建模型

最简单的用法是加载模型文件并构建：

```python
import motrixsim as mx

# 链式调用加载并构建
model = mx.msd.from_file("robot.xml").build()

# 或分步骤进行
scene = mx.msd.from_file("robot.xml")
model = scene.build()
```

### 从字符串加载

您也可以从 MJCF/URDF 字符串创建模型：

```python
import motrixsim as mx

mjcf_string = """
<mujoco>
  <worldbody>
    <body name="box">
      <geom type="box" size="0.1 0.1 0.1"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mx.msd.from_str(mjcf_string, format="mjcf").build()
```

## 组合模型

`attach` 方法允许您将多个模型组合在一起：

```python
import motrixsim as mx

# 加载两个模型
robot = mx.msd.from_file("robot.xml")
gripper = mx.msd.from_file("gripper.xml")

# 将夹爪附加到机器人的手部连杆
robot.attach(
    gripper,
    self_link_name="hand",      # 机器人中要附加到的连杆
    other_prefix="gripper_",    # 夹爪名称的前缀
    other_translation=[0.1, 0, 0]  # 偏移量
)

model = robot.build()
```

### Attach 参数

| 参数                | 类型           | 描述                                                    |
| ------------------- | -------------- | ------------------------------------------------------- |
| `other`             | `Scene`        | 要附加的模型（内部会克隆，可重复使用）                  |
| `self_link_name`    | `str`          | 当前模型中要附加到的连杆。如果为 `None`，则在根级别合并 |
| `other_link_name`   | `str`          | 仅从另一个模型中提取此子树                              |
| `other_translation` | `[x, y, z]`    | 附加模型的平移偏移                                      |
| `other_rotation`    | `[x, y, z, w]` | 附加模型的旋转四元数                                    |
| `other_prefix`      | `str`          | 添加到附加模型中所有名称的前缀                          |
| `other_suffix`      | `str`          | 添加到附加模型中所有名称的后缀                          |

### 创建多个实例

由于 `attach` 会在内部克隆另一个模型，您可以多次附加同一个模型：

```python
import motrixsim as mx

scene = mx.msd.from_file("scene.xml")
robot = mx.msd.from_file("robot.xml")

# 在不同位置创建多个机器人实例
scene.attach(robot, other_prefix="robot1_", other_translation=[0, 0, 0])
scene.attach(robot, other_prefix="robot2_", other_translation=[2, 0, 0])
scene.attach(robot, other_prefix="robot3_", other_translation=[4, 0, 0])

model = scene.build()
```

### 提取子树

您可以在附加之前从模型中提取特定的子树：

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

以下是一个创建包含多个机器人场景的完整示例。完整代码请参阅 [`examples/combine_msd.py`](../../../../examples/combine_msd.py)。

```{literalinclude} ../../../../examples/combine_msd.py
:language: python
:start-after: "# tag::combine_msd_example[]"
:end-before: "# end::combine_msd_example[]"
```

## MJCF Attach 元素

MotrixSim 还支持 MJCF 的 `<attach>` 元素，用于在 XML 中组合模型：

```xml
<mujoco>
  <asset>
    <model name="gripper" file="gripper.xml"/>
  </asset>
  <worldbody>
    <body name="robot">
      <!-- 机器人定义 -->
      <body name="hand">
        <attach model="gripper" prefix="gripper_"/>
      </body>
    </body>
  </worldbody>
</mujoco>
```

有关 MJCF 支持的详细信息，请参阅 [MJCF 文件](../getting_started/mjcf_reference.md)。

## API 参考

有关详细的 API 文档，请参阅 [`motrixsim.msd`](../../api_reference/msd/msd.md)。
