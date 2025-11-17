# 子树传感器（Subtree）

子树传感器用于测量以指定刚体为根节点的运动学子树的整体物理特性，包括质心位置、质心线速度和质心角动量。这类传感器对于分析复杂机械系统的整体动态特性非常有用。

## 🎯 功能描述

子树传感器计算以指定 body 为根节点的完整运动学子树的物理属性，所有结果都在全局坐标系中表示。

### 传感器类型

1. **质心传感器（subtreecom）**: 测量子树的质心位置
2. **质心线速度传感器（subtreelinvel）**: 测量子树质心的线速度
3. **角动量传感器（subtreeangmom）**: 测量子树质心处的角动量

## 📋 返回值格式

```python
# 质心位置传感器
subtree_com = model.get_sensor_value("subtreecom_sensor", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 3)
# 单位：m

# 质心线速度传感器
subtree_linvel = model.get_sensor_value("subtreelinvel_sensor", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 3)
# 单位：m/s

# 角动量传感器
subtree_angmom = model.get_sensor_value("subtreeangmom_sensor", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 3)
# 单位：kg·m²/s
```

## ⚙️ MJCF 配置参数

在 MotrixSim 中，子树传感器支持以下 MJCF 配置字段：

### 基本配置

```xml
<sensor>
    <subtreecom name="sensor_name"
                body="root_body_name"/>
</sensor>
```

### 支持的属性

| 属性名   | 类型   | 必需 | 默认值 | 描述                   |
| -------- | ------ | ---- | ------ | ---------------------- |
| **name** | string | ✅   | -      | 传感器的唯一标识名称   |
| **body** | string | ✅   | -      | 作为根节点的 body 名称 |

**注意**: MotrixSim 目前暂不支持 MJCF 标准中的`cutoff`、`noise`和`user`属性。

## 📝 配置示例

### 基本子树传感器配置

```xml
<!-- 机器人结构 -->
<body name="torso" pos="0 0 1">
    <site name="torso_com" pos="0 0 0"/>

    <!-- 左臂 -->
    <body name="left_shoulder" pos="0.2 0 0.5">
        <body name="left_elbow" pos="0.3 0 0">
            <body name="left_wrist" pos="0.25 0 0"/>
        </body>
    </body>

    <!-- 右臂 -->
    <body name="right_shoulder" pos="-0.2 0 0.5">
        <body name="right_elbow" pos="-0.3 0 0">
            <body name="right_wrist" pos="-0.25 0 0"/>
        </body>
    </body>
</body>

<!-- 子树传感器 -->
<sensor>
    <!-- 整个机器人（以torso为根的完整子树） -->
    <subtreecom name="robot_com" body="torso"/>
    <subtreelinvel name="robot_linvel" body="torso"/>
    <subtreeangmom name="robot_angmom" body="torso"/>

    <!-- 仅左臂子树 -->
    <subtreecom name="left_arm_com" body="left_shoulder"/>
    <subtreelinvel name="left_arm_linvel" body="left_shoulder"/>

    <!-- 仅右臂子树 -->
    <subtreecom name="right_arm_com" body="right_shoulder"/>
    <subtreeangmom name="right_arm_angmom" body="right_shoulder"/>
</sensor>
```

### 多级子树监控

```xml
<!-- 复杂机械结构 -->
<body name="base" pos="0 0 0">
    <body name="main_arm" pos="1 0 1">
        <body name="forearm" pos="1 0 0">
            <body name="end_effector" pos="0.8 0 0">
                <!-- 夹爪等末端执行器 -->
                <body name="finger1" pos="0.1 0.05 0"/>
                <body name="finger2" pos="0.1 -0.05 0"/>
            </body>
        </body>
    </body>
</body>

<!-- 多级子树传感器 -->
<sensor>
    <!-- 完整机械臂 -->
    <subtreecom name="full_arm_com" body="main_arm"/>
    <subtreelinvel name="full_arm_vel" body="main_arm"/>

    <!-- 前臂子树 -->
    <subtreecom name="forearm_com" body="forearm"/>

    <!-- 末端执行器子树 -->
    <subtreecom name="end_effector_com" body="end_effector"/>
    <subtreeangmom name="end_effector_angmom" body="end_effector"/>
</sensor>
```

## 🚀 使用示例

### Python API 使用

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# 加载场景
model = load_model("robot_with_subtree_sensors.xml")
data = SceneData(model)

# 运行仿真并获取子树传感器数据
for step_count in range(1000):
    step(model, data)

    # 获取整体机器人质心
    robot_com = model.get_sensor_value("robot_com", data)
    if robot_com.ndim == 1:
        print(f"机器人质心位置: [{robot_com[0]:.3f}, {robot_com[1]:.3f}, {robot_com[2]:.3f}] m")

    # 获取整体机器人质心速度
    robot_vel = model.get_sensor_value("robot_linvel", data)
    if robot_vel.ndim == 1:
        speed = np.linalg.norm(robot_vel)
        print(f"机器人质心速度: {speed:.3f} m/s")

    # 获取角动量
    robot_angmom = model.get_sensor_value("robot_angmom", data)
    if robot_angmom.ndim == 1:
        angular_momentum = np.linalg.norm(robot_angmom)
        print(f"机器人角动量大小: {angular_momentum:.3f} kg·m²/s")

    # 获取左右臂质心位置
    left_arm_com = model.get_sensor_value("left_arm_com", data)
    right_arm_com = model.get_sensor_value("right_arm_com", data)
    if left_arm_com.ndim == 1 and right_arm_com.ndim == 1:
        arm_distance = np.linalg.norm(left_arm_com - right_arm_com)
        print(f"左右臂质心距离: {arm_distance:.3f} m")
```

### 实际应用场景

```python
# 稳定性分析
def stability_analysis(com_position, support_polygon):
    """基于质心位置进行稳定性分析"""
    # 这里简化处理，实际需要判断质心投影是否在支撑多边形内
    com_x, com_y = com_position[0], com_position[1]

    # 假设支撑区域是矩形 [-0.2, 0.2] x [-0.2, 0.2]
    support_min, support_max = -0.2, 0.2

    if support_min <= com_x <= support_max and support_min <= com_y <= support_max:
        return "稳定"
    else:
        return "不稳定"

# 动量守恒验证
def momentum_conservation_check(angmom_history, dt=0.01):
    """检查角动量是否守恒（无外力时）"""
    if len(angmom_history) < 2:
        return True, 0.0

    # 计算角动量变化率
    recent_angmom = np.array(angmom_history[-5:]) if len(angmom_history) >= 5 else np.array(angmom_history)

    # 计算变化率
    if len(recent_angmom) > 1:
        changes = np.diff(recent_angmom, axis=0) / dt
        max_change_rate = np.max(np.abs(changes))
        return max_change_rate < 0.1, max_change_rate  # 阈值可调整

    return True, 0.0

# 子树质量估算
def estimate_subtree_mass(com_position, assumed_density=1000.0):
    """基于质心位置估算子树质量（简化方法）"""
    # 这里只是示例，实际需要根据几何形状和材料密度计算
    # 假设我们知道子树的边界框，可以粗略估算体积
    bounding_box_volume = 0.1  # 示例值
    estimated_mass = bounding_box_volume * assumed_density
    return estimated_mass

# 碰撞检测与分析
def collision_detection_subtree(com1, vel1, mass1, com2, vel2, mass2, threshold=0.5):
    """基于子树质心的简单碰撞检测"""
    # 计算相对位置和速度
    relative_pos = com2 - com1
    relative_vel = vel2 - vel1
    distance = np.linalg.norm(relative_pos)

    if distance < threshold:
        # 计算碰撞参数
        normal = relative_pos / distance if distance > 0 else np.array([1, 0, 0])
        relative_speed = np.dot(relative_vel, normal)

        if relative_speed < 0:  # 正在接近
            # 动量分析
            total_momentum = mass1 * vel1 + mass2 * vel2
            impulse_magnitude = 2 * relative_speed / (1/mass1 + 1/mass2)

            return {
                'collision': True,
                'distance': distance,
                'relative_speed': relative_speed,
                'impulse': impulse_magnitude,
                'normal': normal
            }

    return {'collision': False, 'distance': distance}

# 能量分析
def energy_analysis_subtree(linvel, angmom, mass, inertia_tensor):
    """子树能量分析"""
    # 动能计算
    kinetic_energy_linear = 0.5 * mass * np.dot(linvel, linvel)
    kinetic_energy_angular = 0.5 * np.dot(angmom, np.linalg.solve(inertia_tensor, angmom))
    total_kinetic_energy = kinetic_energy_linear + kinetic_energy_angular

    return {
        'linear_ke': kinetic_energy_linear,
        'angular_ke': kinetic_energy_angular,
        'total_ke': total_kinetic_energy
    }
```

## 📊 物理原理

子树传感器基于经典力学原理：

1. **质心计算**: 对子树内所有物体的质量和位置进行加权平均
2. **线速度**: 质心的速度等于子树总动量除以总质量
3. **角动量**: 相对于质心的角动量，考虑所有物体的转动和平动

质心计算公式：

```
COM = (Σ(m_i * r_i)) / (Σ(m_i))
```

角动量计算公式：

```
L = Σ(r_i × p_i + I_i * ω_i)
```

其中 r_i 是相对于质心的位置，p_i 是动量，I_i 是转动惯量，ω_i 是角速度。

## ⚠️ 注意事项

1. **子树定义**: 子树包括指定 body 及其所有子代的完整运动学子树
2. **全局坐标系**: 所有测量结果都在全局坐标系中表示
3. **质量分布**: 传感器的准确性依赖于正确的质量属性定义
4. **动力学约束**: 子树传感器不受关节约束的直接影响
5. **不支持高级属性**: MotrixSim 目前不支持`cutoff`、`noise`和`user`属性
6. **数据类型**: 返回值是`numpy.ndarray`类型，形状支持向量化环境
7. **计算复杂度**: 子树传感器可能涉及较复杂的计算，对性能有一定影响
