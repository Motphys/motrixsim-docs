# 📍 参考点（Site）

## 概述

`Site`（参考点）是 MotrixSim 中一个重要的概念，它代表模型中用户感兴趣的位置点。`Site` 本质上是虚拟的位置标记，用于标记模型框架内特定的位置和方向。

### 主要特点

-   **虚拟参考点**：`Site` 是虚拟的位置标记，不参与碰撞检测或惯性属性计算
-   **参考位置**：用于指定传感器、端点等对象的空间属性
-   **轻量级**：相比物理几何体，`Site` 不参与物理计算，开销更小

## 使用方法和示例

### 使用方法

通过 [`SceneModel`](../main_function/scene_model.md) 对象获取所有 `Site` 信息、通过名称获取特定 `Site` 等：

```{literalinclude} ../../../../../examples/site_and_sensor.py
:language: python
:dedent:
:start-after: "# tag::site_access[]"
:end-before:  "# end::site_access[]"
```

完整示例代码参见 [`examples/site_and_sensor.py`](../../../../../examples/site_and_sensor.py)。

### 应用场景

`Site` 有多种应用场景：

-   **传感器位置**：IMU、相机、激光雷达等传感器的安装位置
-   **参考点标记**：关键位置的标记，如关节中心、质心等
-   **调试辅助**：可视化重要位置点，帮助验证模型正确性
-   **路径规划**：作为路径规划中的关键点或目标点

## 在 MJCF 中定义 Site

在 MJCF 文件中，`Site` 通过 `<site>` 标签定义。详细的标签属性和用法请参考 [MJCF 格式说明](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-site)。

**注意**：MotrixSim 目前已支持 Site 的核心功能和常用属性，部分`<site>`属性尚在开发中，请参照 [支持列表](../getting_started/mjcf.md) 使用。

以下是 `site_and_sensor.xml` 中的 `Site` 定义示例：

```{literalinclude} ../../../../../examples/assets/site_and_sensor.xml
:language: xml
:dedent:
:lines: 9-19
```

完整的 XML 文件参见：[`examples/assets/site_and_sensor.xml`](../../../../../examples/assets/site_and_sensor.xml)

## 注意事项

1. **坐标系**：`Site` 的位置和方向是相对于其父链接的坐标系
2. **命名唯一性**：每个 `Site` 在模型中应该有唯一的名称
3. **可视化**：`Site` 可以在渲染中显示，有助于调试和验证位置
4. **虚拟特性**：`Site` 是虚拟的，如需物理交互请使用 `<geom>` 标签

## API Reference

更多与 Site 相关的 API，请参考 [`Site API`]

[`Site API`]: motrixsim.Site
