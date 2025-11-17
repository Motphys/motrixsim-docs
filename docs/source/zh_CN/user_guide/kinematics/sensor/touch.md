# 触摸传感器（Touch）

触摸传感器用于在指定的 site 位置检测接触并测量法向力。在机器人仿真中，触摸传感器常用于实现触觉感知、碰撞检测和力反馈控制。

## 🎯 功能描述

触摸传感器测量的是安装 site 位置感受到的接触法向力。当其他物体与传感器的检测区域（由 site 的形状和大小定义）发生接触时，传感器会返回接触点产生的法向力大小。

### 核心特性

1. **位置特定**: 检测特定 site 位置的接触
2. **力测量**: 返回接触法向力的标量值
3. **形状感知**: 基于 site 的几何形状进行检测
4. **实时响应**: 每个仿真步提供接触力信息

## 📋 返回值格式

```python
touch_force = model.get_sensor_value("touch_sensor_name", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 1)
# 单位：N (牛顿)
```

-   **touch_force[..., 0]**: 接触法向力大小
-   **值 = 0**: 无接触状态
-   **值 > 0**: 有接触，数值表示法向力大小

## ⚙️ MJCF 配置参数

在 MotrixSim 中，触摸传感器支持以下 MJCF 配置字段：

### 基本配置

```xml
<sensor>
    <touch name="sensor_name"
          site="site_name"/>
</sensor>
```

### 支持的属性

| 属性名   | 类型   | 必需 | 默认值 | 描述                   |
| -------- | ------ | ---- | ------ | ---------------------- |
| **name** | string | ✅   | -      | 传感器的唯一标识名称   |
| **site** | string | ✅   | -      | 安装传感器的参考点名称 |

**注意**: MotrixSim 目前暂不支持 MJCF 标准中的`cutoff`、`noise`和`user`属性。

## 📝 配置示例

### 基本触摸传感器配置

```xml
<!-- 定义触觉检测点 -->
<site name="palm_touch" type="sphere" size="0.05" rgba="1 0 1 1" pos="0 0 0"/>

<!-- 定义触摸传感器 -->
<sensor>
    <touch name="palm_sensor" site="palm_touch"/>
</sensor>
```

### 圆柱体碰撞检测配置（来自 touch_sensor_demo.xml）

```{literalinclude} ../../../../../examples/assets/touch_sensor_demo.xml
:language: xml
```

### 多个触摸传感器配置

```xml
<!-- 机器人手指上的多个触觉点 -->
<site name="thumb_tip" pos="0.1 0 0.15" type="sphere" size="0.02" rgba="1 0 0 1"/>
<site name="index_tip" pos="0.05 0 0.18" type="sphere" size="0.02" rgba="0 1 0 1"/>
<site name="middle_tip" pos="0 0 0.18" type="sphere" size="0.02" rgba="0 0 1 1"/>

<!-- 对应的触摸传感器 -->
<sensor>
    <touch name="thumb_touch" site="thumb_tip"/>
    <touch name="index_touch" site="index_tip"/>
    <touch name="middle_touch" site="middle_tip"/>
</sensor>
```

### 不同形状的触摸传感器

```xml
<!-- 球形触觉传感器 -->
<site name="sphere_touch" type="sphere" size="0.03" rgba="1 1 0 1" pos="0 0 0"/>

<!-- 胶囊形触觉传感器 -->
<site name="capsule_touch" type="capsule" size="0.02 0.1" rgba="1 0 1 1" pos="0 0 0"/>

<!-- 圆柱形触觉传感器 -->
<site name="cylinder_touch" type="cylinder" size="0.03 0.08" rgba="0 1 1 1" pos="0 0 0"/>

<sensor>
    <touch name="sphere_sensor" site="sphere_touch"/>
    <touch name="capsule_sensor" site="capsule_touch"/>
    <touch name="cylinder_sensor" site="cylinder_touch"/>
</sensor>
```

## 🚀 使用示例

### Python API 使用

完整的可视化示例请参考 [`examples/sensors/touch_sensor_demo.py`](../../../../../examples/sensors/touch_sensor_demo.py)。

#### 基本配置和传感器获取

```{literalinclude} ../../../../../examples/sensors/touch_sensor_demo.py
:language: python
:dedent:
:start-after: "        # Scene file path"
:end-before: "        print(\"=== Touch Sensor Demo ===\")"
```

#### 传感器数据读取与可视化

```{literalinclude} ../../../../../examples/sensors/touch_sensor_demo.py
:language: python
:dedent:
:start-after: "            # Get all touch sensor data"
:end-before: "            # Sync render objects"
```

### 实际应用场景

该示例演示了一个圆柱体沿 x 轴做线性往复运动，撞击墙壁来测试末端 touch 传感器的反馈：

1. **线性运动控制**: 圆柱体从-2 移动到 2，然后返回，实现往复运动
2. **实时接触检测**: 当圆柱体末端接触墙壁时，传感器检测到压力
3. **可视化反馈**:
    - 红色球体显示传感器位置
    - 黄色箭头长度与接触力成正比，直观显示力的大小
4. **力监控**: 控制台实时输出接触力数值

### 检测流程

1. **接触点识别**: 如果接触点位于 Touch 传感器的 site 范围内，或者接触点的法线方向穿过 site，则视为有效接触
2. **力计算**: 计算每个接触点的法向力
3. **力累积**: 将所有接触点的法向力求和
4. **返回结果**: 返回总的法向力大小

## ⚠️ 注意事项

1. **Site 形状重要性**: 传感器的检测范围由 site 的几何形状和大小决定
2. **法向力测量**: 仅测量法向力，不包括切向力分量
3. **力累积**: 多个接触点的力会累积为单个标量值
4. **不支持高级属性**: MotrixSim 目前不支持`cutoff`、`noise`和`user`属性
5. **数据类型**: 返回值是`numpy.ndarray`类型，形状支持向量化环境
6. **零值含义**: 返回值为 0 表示无接触或接触力可忽略
