# 速度计（Velocimeter）

速度计传感器用于测量安装点在**局部坐标系**下的三轴线性速度。在机器人仿真中，速度计常用于监测机器人的运动速度，为速度控制和运动估计提供重要数据。

## 🎯 功能描述

速度计测量的是传感器安装点在**site 局部坐标系**下的线性速度。该传感器返回的是一个包含 3 个浮点数的数组，分别表示 X、Y、Z 轴方向上的速度分量。

## 📋 返回值格式

```python
velocity = model.get_sensor_value("velocimeter_name", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 3)
# 单位：m/s
```

-   **velocity[..., 0]**: X 轴方向的速度分量（局部坐标系）
-   **velocity[..., 1]**: Y 轴方向的速度分量（局部坐标系）
-   **velocity[..., 2]**: Z 轴方向的速度分量（局部坐标系）

## ⚙️ MJCF 配置参数

在 MotrixSim 中，速度计传感器支持以下 MJCF 配置字段：

### 基本配置

```xml
<sensor>
    <velocimeter name="sensor_name"
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

### 基本速度计配置

```xml
<!-- 在body中定义安装点 -->
<site name="car_vel_sensor" type="sphere" size="0.03" rgba="1 0 1 1" pos="0 0 0"/>

<!-- 定义速度计传感器 -->
<sensor>
    <velocimeter name="car_velocimeter" site="car_vel_sensor"/>
</sensor>
```

### 多个速度计配置

```xml
<!-- 为不同位置安装多个速度计 -->
<site name="vel_base" pos="0 0 0" size="0.02"/>
<site name="vel_end_effector" pos="1 0 0" size="0.02"/>

<sensor>
    <velocimeter name="vel_base" site="vel_base"/>
    <velocimeter name="vel_end" site="vel_end_effector"/>
</sensor>
```

## 🚀 使用示例

### Python API 使用

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# 加载场景
model = load_model("scene_with_velocimeter.xml")
data = SceneData(model)

# 运行仿真并获取速度计数据
for step_count in range(1000):
    step(model, data)

    # 获取速度计数据
    vel_data = model.get_sensor_value("car_velocimeter", data)

    # 如果是单环境仿真，数据形状为 (3,)
    if vel_data.ndim == 1:
        print(f"速度: [{vel_data[0]:.3f}, {vel_data[1]:.3f}, {vel_data[2]:.3f}] m/s")

        # 计算速度大小
        vel_magnitude = np.linalg.norm(vel_data)
        print(f"速度大小: {vel_magnitude:.3f} m/s")
    else:
        # 向量化环境的情况
        print(f"速度数据形状: {vel_data.shape}")
```

### 实际应用场景

```python
# 速度监控和限制
def monitor_velocity(velocity, max_speed=5.0):
    """监控并检查速度是否超出限制"""
    vel_magnitude = np.linalg.norm(velocity)
    if vel_magnitude > max_speed:
        print(f"警告: 速度 {vel_magnitude:.2f} m/s 超出最大限制 {max_speed} m/s")
    return vel_magnitude

# 位移估计（基于速度积分）
def estimate_displacement(velocity_history, dt=0.01):
    """基于速度历史估计位移"""
    if len(velocity_history) < 2:
        return np.zeros(3)

    displacement = np.zeros(3)
    for i in range(1, len(velocity_history)):
        # 简单的梯形积分
        avg_vel = (velocity_history[i] + velocity_history[i-1]) / 2
        displacement += avg_vel * dt

    return displacement

# 运动方向分析
def analyze_motion_direction(velocity):
    """分析主要运动方向"""
    vel_magnitude = np.linalg.norm(velocity)
    if vel_magnitude < 0.01:  # 静止阈值
        return "静止"

    # 归一化速度向量
    vel_norm = velocity / vel_magnitude

    # 判断主要方向
    max_axis = np.argmax(np.abs(vel_norm))
    directions = ["X轴", "Y轴", "Z轴"]
    return f"主要沿{directions[max_axis]}方向运动"
```

## 📊 物理原理

速度计的测量基于刚体运动学原理：

1. **局部坐标系测量**: 返回的速度值是在 site 的局部坐标系中表示的
2. **线性速度**: 仅测量平移运动的速度，不包括旋转运动
3. **瞬时速度**: 提供当前时刻的瞬时速度信息

对于旋转体上某一点的速度，可以通过刚体运动学公式计算：

```
v_point = v_center + ω × r_point_center
```

其中 ω 是角速度，r 是相对于质心的位置向量。

## ⚠️ 注意事项

1. **局部坐标系**: 返回的速度值是在 site 的局部坐标系中表示的，不是全局坐标系
2. **仅线性速度**: 测量的是线性速度，不包括因旋转产生的切向速度分量
3. **安装位置**: 传感器测量的是 site 安装点位置的线速度
4. **不支持高级属性**: MotrixSim 目前不支持`cutoff`、`noise`和`user`属性
5. **数据类型**: 返回值是`numpy.ndarray`类型，形状支持向量化环境
6. **速度累积**: 如需位移信息，需要对速度进行积分，可能产生累积误差
