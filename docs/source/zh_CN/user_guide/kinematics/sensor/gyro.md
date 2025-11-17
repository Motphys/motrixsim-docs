# 角速度计（Gyro）

角速度计传感器（陀螺仪）用于测量安装点在**局部坐标系**下的三轴角速度。在机器人仿真中，角速度计是姿态控制和运动估计的核心传感器，广泛应用于无人机、机器人手臂、移动机器人等领域。

## 🎯 功能描述

角速度计测量的是传感器安装点在**site 局部坐标系**下的角速度。该传感器返回的是一个包含 3 个浮点数的数组，分别表示绕 X、Y、Z 轴旋转的角速度分量。

## 📋 返回值格式

```python
angular_velocity = model.get_sensor_value("gyro_name", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 3)
# 单位：rad/s
```

-   **angular_velocity[..., 0]**: 绕 X 轴旋转的角速度（局部坐标系）
-   **angular_velocity[..., 1]**: 绕 Y 轴旋转的角速度（局部坐标系）
-   **angular_velocity[..., 2]**: 绕 Z 轴旋转的角速度（局部坐标系）

## ⚙️ MJCF 配置参数

在 MotrixSim 中，角速度计传感器支持以下 MJCF 配置字段：

### 基本配置

```xml
<sensor>
    <gyro name="sensor_name"
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

### 基本角速度计配置

```xml
<!-- 在body中定义安装点 -->
<site name="robot_gyro" type="sphere" size="0.03" rgba="1 1 0 1" pos="0 0 0.1"/>

<!-- 定义角速度计传感器 -->
<sensor>
    <gyro name="robot_gyro_sensor" site="robot_gyro"/>
</sensor>
```

### 多轴角速度计配置

```xml
<!-- 为不同部件安装角速度计 -->
<site name="base_gyro" pos="0 0 0" size="0.02"/>
<site name="arm_gyro" pos="1 0 0.5" size="0.02"/>

<sensor>
    <gyro name="base_angular_vel" site="base_gyro"/>
    <gyro name="arm_angular_vel" site="arm_gyro"/>
</sensor>
```

## 🚀 使用示例

### Python API 使用

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# 加载场景
model = load_model("scene_with_gyro.xml")
data = SceneData(model)

# 运行仿真并获取角速度计数据
for step_count in range(1000):
    step(model, data)

    # 获取角速度计数据
    gyro_data = model.get_sensor_value("robot_gyro_sensor", data)

    # 如果是单环境仿真，数据形状为 (3,)
    if gyro_data.ndim == 1:
        print(f"角速度: [{gyro_data[0]:.3f}, {gyro_data[1]:.3f}, {gyro_data[2]:.3f}] rad/s")

        # 计算角速度大小
        angular_speed = np.linalg.norm(gyro_data)
        print(f"角速度大小: {angular_speed:.3f} rad/s")

        # 转换为度/秒
        angular_speed_deg = np.degrees(angular_speed)
        print(f"角速度大小: {angular_speed_deg:.1f} °/s")
    else:
        # 向量化环境的情况
        print(f"角速度数据形状: {gyro_data.shape}")
```

### 实际应用场景

```python
# 姿态积分（简单欧拉积分）
def integrate_attitude(angular_velocity, current_quat, dt=0.01):
    """基于角速度积分更新姿态四元数"""
    # 将角速度转换为四元数变化率
    omega = angular_velocity
    omega_magnitude = np.linalg.norm(omega)

    if omega_magnitude < 1e-6:
        return current_quat

    # 旋转轴
    axis = omega / omega_magnitude
    # 旋转角度
    angle = omega_magnitude * dt

    # 创建增量四元数 [w, x, y, z]
    half_angle = angle / 2
    dq = np.array([
        np.cos(half_angle),
        axis[0] * np.sin(half_angle),
        axis[1] * np.sin(half_angle),
        axis[2] * np.sin(half_angle)
    ])

    # 四元数乘法更新姿态
    return quaternion_multiply(dq, current_quat)

# 角速度阈值检测
def detect_rotation(angular_velocity, threshold=0.1):
    """检测是否有显著旋转"""
    angular_speed = np.linalg.norm(angular_velocity)
    return angular_speed > threshold

# 旋转运动分析
def analyze_rotation_pattern(angular_velocity):
    """分析旋转模式和主轴"""
    angular_speed = np.linalg.norm(angular_velocity)
    if angular_speed < 0.01:
        return "静止", None

    # 归一化角速度向量得到旋转轴
    rotation_axis = angular_velocity / angular_speed

    # 找到主要旋转轴
    max_component = np.argmax(np.abs(rotation_axis))
    axes = ['X轴', 'Y轴', 'Z轴']
    main_axis = axes[max_component]

    return f"绕{main_axis}旋转", rotation_axis

def quaternion_multiply(q1, q2):
    """四元数乘法"""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2

    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])
```

## 📊 物理原理

角速度计基于刚体旋转运动学原理：

1. **局部坐标系测量**: 返回的角速度值是在 site 的局部坐标系中表示的
2. **瞬时角速度**: 提供当前时刻的瞬时角速度信息

角速度向量`ω = [ωx, ωy, ωz]`表示绕各坐标轴的旋转速率，其大小`||ω||`为整体的旋转速率。

## ⚠️ 注意事项

1. **局部坐标系**: 返回的角速度值是在 site 的局部坐标系中表示的，不是全局坐标系
2. **姿态积分**: 如需姿态信息，需要对角速度进行积分，容易产生累积误差
3. **不支持高级属性**: MotrixSim 目前不支持`cutoff`、`noise`和`user`属性
4. **数据类型**: 返回值是`numpy.ndarray`类型，形状支持向量化环境
5. **奇异值问题**: 在某些姿态下（如万向节锁）可能出现数值不稳定
