# 加速度计（Accelerometer）

加速度计传感器用于测量安装点在**局部坐标系**下的三轴线性加速度。在机器人仿真中，加速度计常用于感知机器人的运动状态，为控制算法提供重要的反馈信息。

## 🎯 功能描述

加速度计测量的是传感器安装点在**site 局部坐标系**下的线性加速度，包括重力加速度的影响。该传感器返回的是一个包含 3 个浮点数的数组，分别表示 X、Y、Z 轴方向上的加速度分量。

## 📋 返回值格式

```python
acceleration = model.get_sensor_value("accelerometer_name", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 3)
# 单位：m/s²
```

-   **acceleration[..., 0]**: X 轴方向的加速度分量（局部坐标系）
-   **acceleration[..., 1]**: Y 轴方向的加速度分量（局部坐标系）
-   **acceleration[..., 2]**: Z 轴方向的加速度分量（局部坐标系）

## ⚙️ MJCF 配置参数

在 MotrixSim 中，加速度计传感器支持以下 MJCF 配置字段：

### 基本配置

```xml
<sensor>
    <accelerometer name="sensor_name"
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

### 基本加速度计配置

```xml
<!-- 在body中定义安装点 -->
<site name="car_imu" type="sphere" size="0.03" rgba="0 1 0 1" pos="0 0 0"/>

<!-- 定义加速度计传感器 -->
<sensor>
    <accelerometer name="car_accelerometer" site="car_imu"/>
</sensor>
```

### 多个加速度计配置

```xml
<!-- 为不同位置安装多个加速度计 -->
<site name="imu_base" pos="0 0 0" size="0.02"/>
<site name="imu_end" pos="0 0 1" size="0.02"/>

<sensor>
    <accelerometer name="acc_base" site="imu_base"/>
    <accelerometer name="acc_end" site="imu_end"/>
</sensor>
```

## 🚀 使用示例

### Python API 使用

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# 加载场景
model = load_model("scene_with_accelerometer.xml")
data = SceneData(model)

# 运行仿真并获取加速度计数据
for step_count in range(1000):
    step(model, data)

    # 获取加速度计数据
    acc_data = model.get_sensor_value("car_accelerometer", data)

    # 如果是单环境仿真，数据形状为 (3,)
    if acc_data.ndim == 1:
        print(f"加速度: [{acc_data[0]:.3f}, {acc_data[1]:.3f}, {acc_data[2]:.3f}] m/s²")

        # 计算加速度大小
        acc_magnitude = np.linalg.norm(acc_data)
        print(f"加速度大小: {acc_magnitude:.3f} m/s²")
    else:
        # 向量化环境的情况
        print(f"加速度数据形状: {acc_data.shape}")
```

### 实际应用场景

```python
# 机器人跌倒检测
def detect_fall(acceleration, threshold=15.0):
    """基于加速度计数据检测跌倒"""
    acc_magnitude = np.linalg.norm(acceleration)
    return acc_magnitude > threshold

# 静止检测（考虑重力）
def is_stationary(acceleration, gravity_threshold=9.5):
    """检测设备是否静止（考虑重力影响）"""
    acc_magnitude = np.linalg.norm(acceleration)
    # 静止时加速度大小应接近重力加速度
    return abs(acc_magnitude - gravity_threshold) < 0.5

# 计算倾斜角度
def calculate_tilt_angle(acceleration):
    """基于加速度计计算设备的倾斜角度"""
    # 假设设备主要受重力影响
    gravity = np.array([0, 0, -9.81])

    # 归一化向量
    acc_norm = acceleration / np.linalg.norm(acceleration)
    gravity_norm = gravity / np.linalg.norm(gravity)

    # 计算夹角
    cos_angle = np.dot(acc_norm, gravity_norm)
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))

    return np.degrees(angle)
```

## 📊 物理原理

加速度计的测量基于牛顿第二定律。在仿真环境中：

1. **局部坐标系测量**: 返回的加速度值是在 site 的局部坐标系中表示的
2. **重力影响**: 当传感器相对于地面静止时，会测量到重力加速度在局部坐标系中的投影
3. **线性加速度**: 测量的是安装点的纯线性加速度，不包括旋转分量

例如，当机器人倾斜时，即使静止，加速度计也会因为重力在局部坐标系中的分量而产生非零读数。

## ⚠️ 注意事项

1. **局部坐标系**: 返回的加速度值是在 site 的局部坐标系中表示的，不是全局坐标系
2. **重力影响**: 静止时加速度计会测量到重力加速度在局部坐标系中的投影
3. **安装位置**: 传感器测量的是 site 安装点位置的加速度
4. **不支持高级属性**: MotrixSim 目前不支持`cutoff`、`noise`和`user`属性
5. **数据类型**: 返回值是`numpy.ndarray`类型，形状支持向量化环境
