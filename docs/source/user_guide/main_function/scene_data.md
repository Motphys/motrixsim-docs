# 💾 数据（SceneData）

在上一章节中，我们了解了 [`SceneModel`](scene_model.md) 用于描述静态的物理模型。本章节将重点介绍 `SceneData`的创建和使用方法。

## 基本概念

`SceneData` 是 MotrixSim 仿真系统中的**动态数据容器**，存储了系统在运行过程中的所有变化量。这些数据不限于关节的位置和速度，还包括物体在空间中的位置和姿态、传感器的数值等。

`SceneData` 中的状态更新需要通过调用运动学函数来更新系统状态。

## 创建数据

### 基本创建

```{literalinclude} ../../../../examples/empty.py
:language: python
:dedent:
:start-after: "# tag::create_data[]"
:end-before:  "# end::create_data[]"
```

完整的示例代码请参见 [`examples/empty.py`](../../../../examples/empty.py)。

### 多数据实例

MotrixSim 支持基于同一个 `SceneModel` 创建多个独立的 `SceneData` 实例，适用于并行实验、状态备份、参数对比等场景。

```{literalinclude} ../../../../examples/model.py
:language: python
:dedent:
:start-after: "# tag::create_data[]"
:end-before:  "# end::create_data[]"
```

各数据实例之间互不影响，可以独立进行状态更新。

完整的示例代码请参见 [`examples/model.py`](../../../../examples/model.py)。

## 状态访问

### 直接数组访问

`SceneData` 提供了直接访问系统状态数组的方式：

```python
pos = data.dof_pos_array
vel = data.dof_vel_array
```

详细的 `SceneData` 属性，请参阅：[**API 快速参考 - SceneData**](../../api_reference/api_quick_reference.md#-scenedata---状态数据)

### 通过组件访问

结合 `SceneModel` 的 Named Access，可以通过组件对象来访问或设置特定的状态：

```{literalinclude} ../../../../examples/body.py
:language: python
:dedent:
:start-after: "# tag::access_body[]"
:end-before:  "# end::access_body[]"
```

完整的示例代码请参见 [`examples/body.py`](../../../../examples/body.py)。

## API Reference

更多与 SceneData 相关的 API，请参考 [`SceneData API`]

[`SceneData API`]: motrixsim.SceneData
