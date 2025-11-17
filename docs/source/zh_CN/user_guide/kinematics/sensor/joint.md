# 关节传感器（Joint）

关节传感器用于测量机器人关节的位置和速度信息，是机器人控制和状态监测的核心传感器类型。包括关节位置传感器（jointpos）和关节速度传感器（jointvel）两种。

## 🎯 功能描述

关节传感器直接测量指定关节的运动状态，包括位置和速度信息。与安装在空间点的传感器不同，关节传感器直接与关节关联，提供精确的关节运动参数。

### 传感器类型

1. **关节位置传感器（jointpos）**: 测量关节的当前位置或角度
2. **关节速度传感器（jointvel）**: 测量关节的当前速度或角速度

## 📋 返回值格式

```python
# 关节位置传感器
joint_position = model.get_sensor_value("jointpos_sensor", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 1)
# 单位：rad（旋转关节）或 m（滑动关节）

# 关节速度传感器
joint_velocity = model.get_sensor_value("jointvel_sensor", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 1)
# 单位：rad/s（旋转关节）或 m/s（滑动关节）
```

## ⚙️ MJCF 配置参数

在 MotrixSim 中，关节传感器支持以下 MJCF 配置字段：

### 关节位置传感器配置

```xml
<sensor>
    <jointpos name="sensor_name"
              joint="joint_name"/>
</sensor>
```

### 关节速度传感器配置

```xml
<sensor>
    <jointvel name="sensor_name"
              joint="joint_name"/>
</sensor>
```

### 支持的属性

| 属性名    | 类型   | 必需 | 默认值 | 描述                 |
| --------- | ------ | ---- | ------ | -------------------- |
| **name**  | string | ✅   | -      | 传感器的唯一标识名称 |
| **joint** | string | ✅   | -      | 要测量的关节名称     |

**注意**: MotrixSim 目前暂不支持 MJCF 标准中的`cutoff`、`noise`和`user`属性。

## 📝 配置示例

### 基本关节传感器配置

```xml
<!-- 定义关节 -->
<joint name="shoulder_pitch" type="hinge" axis="0 1 0" range="-3.14 3.14"/>
<joint name="elbow" type="hinge" axis="0 1 0" range="0 3.14"/>
<joint name="wrist_slide" type="slide" axis="1 0 0" range="-0.5 0.5"/>

<!-- 关节位置传感器 -->
<sensor>
    <jointpos name="shoulder_pos" joint="shoulder_pitch"/>
    <jointpos name="elbow_pos" joint="elbow"/>
    <jointpos name="wrist_pos" joint="wrist_slide"/>
</sensor>

<!-- 关节速度传感器 -->
<sensor>
    <jointvel name="shoulder_vel" joint="shoulder_pitch"/>
    <jointvel name="elbow_vel" joint="elbow"/>
    <jointvel name="wrist_vel" joint="wrist_slide"/>
</sensor>
```

### 复合关节传感器配置

```xml
<!-- 为同一关节同时配置位置和速度传感器 -->
<joint name="base_rotation" type="hinge" axis="0 0 1" limited="false"/>

<sensor>
    <jointpos name="base_rot_pos" joint="base_rotation"/>
    <jointvel name="base_rot_vel" joint="base_rotation"/>
</sensor>
```

## 🚀 使用示例

### Python API 使用

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# 加载场景
model = load_model("robot_with_joint_sensors.xml")
data = SceneData(model)

# 运行仿真并获取关节传感器数据
for step_count in range(1000):
    step(model, data)

    # 获取关节位置
    shoulder_pos = model.get_sensor_value("shoulder_pos", data)
    elbow_pos = model.get_sensor_value("elbow_pos", data)

    # 获取关节速度
    shoulder_vel = model.get_sensor_value("shoulder_vel", data)
    elbow_vel = model.get_sensor_value("elbow_vel", data)

    # 处理单环境仿真数据（形状为 (1,)）
    if shoulder_pos.ndim == 1:
        print(f"肩关节角度: {np.degrees(shoulder_pos[0]):.1f}°")
        print(f"肘关节角度: {np.degrees(elbow_pos[0]):.1f}°")
        print(f"肩关节速度: {np.degrees(shoulder_vel[0]):.1f}°/s")
        print(f"肘关节速度: {np.degrees(elbow_vel[0]):.1f}°/s")

    # 关节限位检查
    if np.abs(shoulder_pos[0]) > np.radians(150):
        print("警告: 肩关节接近限位!")
```

### 实际应用场景

```python
# 关节控制（PD控制器）
def joint_control_pd(current_pos, target_pos, current_vel, kp=10.0, kd=1.0):
    """简单的PD关节控制器"""
    # 位置误差
    pos_error = target_pos - current_pos
    # 阻尼项
    damping = -kd * current_vel

    # 控制力矩
    control_signal = kp * pos_error + damping
    return control_signal

# 运动范围监控
def monitor_joint_limits(joint_pos, joint_name, min_limit, max_limit):
    """监控关节是否超出运动范围"""
    pos = joint_pos[0] if joint_pos.ndim == 1 else joint_pos[0, 0]

    if pos < min_limit:
        print(f"警告: {joint_name} 超出下限 {np.degrees(min_limit):.1f}°")
        return False
    elif pos > max_limit:
        print(f"警告: {joint_name} 超出上限 {np.degrees(max_limit):.1f}°")
        return False
    return True

# 关节运动分析
def analyze_joint_motion(position_history, velocity_history, window_size=10):
    """分析关节运动模式"""
    if len(position_history) < window_size:
        return "数据不足", {}

    recent_positions = position_history[-window_size:]
    recent_velocities = velocity_history[-window_size:]

    # 平均速度
    avg_velocity = np.mean(recent_velocities)
    # 速度方差
    velocity_variance = np.var(recent_velocities)
    # 运动范围
    motion_range = np.max(recent_positions) - np.min(recent_positions)

    # 运动状态判断
    if abs(avg_velocity) < 0.01 and velocity_variance < 0.01:
        motion_state = "静止"
    elif velocity_variance > 1.0:
        motion_state = "变速运动"
    else:
        motion_state = "匀速运动"

    analysis = {
        "state": motion_state,
        "avg_velocity": avg_velocity,
        "velocity_variance": velocity_variance,
        "motion_range": motion_range
    }

    return motion_state, analysis

# 轨迹跟踪
def trajectory_tracking(current_pos, desired_trajectory, time_step, kp=50.0):
    """轨迹跟踪控制器"""
    if time_step >= len(desired_trajectory):
        target_pos = desired_trajectory[-1]
    else:
        target_pos = desired_trajectory[time_step]

    # 简单P控制
    error = target_pos - current_pos
    control_signal = kp * error

    return control_signal, target_pos
```

## 📊 物理原理

关节传感器基于刚体运动学原理：

1. **直接测量**: 直接测量关节的内部状态，无需通过空间点推算
2. **关节类型适配**:
    - 旋转关节（hinge）: 返回角度（rad）和角速度（rad/s）
    - 滑动关节（slide）: 返回位移（m）和线速度（m/s）
3. **单自由度**: 每个传感器测量一个自由度的运动

## ⚠️ 注意事项

1. **关节关联**: 传感器必须与有效关节关联
2. **单位注意**: 旋转关节使用弧度，滑动关节使用米
3. **数据形状**: 返回值为单元素数组，形状为 `(*data.shape, 1)`
4. **不支持高级属性**: MotrixSim 目前不支持`cutoff`、`noise`和`user`属性
