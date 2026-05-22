# 🔩 关节

关节用来定义它所在的刚体 ([Body](body.md)) 与父刚体之间的运动自由度。每个刚体可以定义多个关节，组合多种自由度。如果一个刚体没有定义关节，该刚体与父刚体刚性连接。世界刚体 (world body) 中不能定义关节。关节的状态数据（位置、速度）保存在 [SceneData](../main_function/scene_data.md) 中，由于关节定义的自由度不同，状态数据的长度也有所不同。

## 关节类型

```{list-table}
   :header-rows: 1
   :widths: 15 15 15 10 45

   * - 类型
     - 自由度
     - 旋转表示
     - 限制
     - 说明
   * - 滑动关节（Slide）
     - 1 位移
     - 无
     - 可配置
     - 由关节位置和滑动方向定义。
   * - 铰链关节（Hinge）
     - 1 旋转
     - 角度
     - 可配置
     - 绕指定旋转轴旋转，旋转通过指定位置，是默认的关节类型。
   * - 球形关节（Ball）
     - 3 旋转
     - 四元数
     - 可配置
     - 绕指定点旋转，可与滑动关节组合，不可与球形关节或铰链关节同时定义。
```

与 Mujoco 不同，mjcf 文件中的`<freejoint>`元素在 MotrixSim 中会解析为[FloatingBase](floating_base.md)。

## 配置示例

关节通过 MJCF 文件进行配置，可参考 [`examples/assets/joint.xml`](../../../../examples/assets/joint.xml)

[MJCF 关节相关标签说明](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-joint)

## API 使用示例

在 MotrixSim 中加载 MJCF 文件创建场景和数据

```{literalinclude} ../../../../examples/physics/joint.py
:language: python
:dedent:
:start-after: "# tag::init[]"
:end-before:  "# end::init[]"
```

获取场景中的所有关节

```{literalinclude} ../../../../examples/physics/joint.py
:language: python
:dedent:
:start-after: "# tag::access_all[]"
:end-before:  "# end::access_all[]"
```

通过关节名称获取关节索引和访问

```{literalinclude} ../../../../examples/physics/joint.py
:language: python
:dedent:
:start-after: "# tag::joint_index[]"
:end-before:  "# end::joint_index[]"
```

获取关节对应自由度的值和速度

```{literalinclude} ../../../../examples/physics/joint.py
:language: python
:dedent:
:start-after: "# tag::joint_dof_pos_vel[]"
:end-before:  "# end::joint_dof_pos_vel[]"
```

获取关节的限制

```{literalinclude} ../../../../examples/physics/joint.py
:language: python
:dedent:
:start-after: "# tag::joint_limits[]"
:end-before:  "# end::joint_limits[]"
```

配置关节的位置和速度

```{literalinclude} ../../../../examples/physics/joint.py
:language: python
:dedent:
:start-after: "# tag::set_pos_vel[]"
:end-before:  "# end::set_pos_vel[]"
```

完整代码见 [joint.py](../../../../examples/physics/joint.py)

## API Reference

更多与 Joint 相关的 API，请参考 [`Joint API`]

[`Joint API`]: motrixsim.Joint
