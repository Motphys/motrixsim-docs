# 参考框传感器（Frame）

参考框传感器用于测量物体在指定参考坐标系下的位置、旋转、速度和加速度信息。这类传感器提供了比局部坐标系传感器更灵活的测量方式，可以相对于任意参考点进行测量。

```{warning}
**重要：MotrixSim vs MuJoCo 四元数格式差异**

- **MotrixSim**: 使用 **XYZW** 格式存储四元数 `[x, y, z, w]`
- **MuJoCo**: 使用 **WXYZ** 格式存储四元数 `[w, x, y, z]`

这个差异至关重要！在使用四元数进行姿态计算或与其他系统集成时，必须进行格式转换，否则会导致计算错误。
```

## 🎯 功能描述

参考框传感器测量指定对象（body 或 site）相对于参考坐标系的状态信息。参考坐标系可以是全局坐标系，也可以是其他 body 或 site 的局部坐标系。

### 传感器类型

1. **位置传感器**:

    - `framepos`: 测量对象在参考坐标系下的位置
    - `framequat`: 测量对象在参考坐标系下的旋转四元数

2. **轴向传感器**:

    - `framexaxis`: 测量对象 X 轴在参考坐标系中的单位向量
    - `frameyaxis`: 测量对象 Y 轴在参考坐标系中的单位向量
    - `framezaxis`: 测量对象 Z 轴在参考坐标系中的单位向量

3. **速度传感器**:

    - `framelinvel`: 测量对象在参考坐标系下的线速度
    - `frameangvel`: 测量对象在参考坐标系下的角速度

4. **加速度传感器**:
    - `framelinacc`: 测量对象在参考坐标系下的线加速度

## 📋 返回值格式

```python
# 位置传感器
frame_position = model.get_sensor_value("framepos_sensor", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 3)
# 单位：m

# 四元数传感器
frame_quaternion = model.get_sensor_value("framequat_sensor", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 4)
# 格式：[x, y, z, w]  (MotrixSim格式，注意与MuJoCo的[w, x, y, z]格式不同)

# 轴向传感器
frame_axis = model.get_sensor_value("framexaxis_sensor", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 3)

# 速度传感器
linear_velocity = model.get_sensor_value("framelinvel_sensor", data)
angular_velocity = model.get_sensor_value("frameangvel_sensor", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 3)
# 单位：m/s (线速度), rad/s (角速度)

# 加速度传感器
linear_acceleration = model.get_sensor_value("framelinacc_sensor", data)
# 类型：numpy.ndarray[float32]
# 形状：shape = (*data.shape, 3)
# 单位：m/s²
```

## ⚙️ MJCF 配置参数

在 MotrixSim 中，参考框传感器支持以下 MJCF 配置字段：

### 基本配置

```xml
<sensor>
    <framepos name="sensor_name"
              objtype="body"
              objname="object_name"
              reftype="body"
              refname="reference_name"/>
</sensor>
```

### 支持的属性

| 属性名      | 类型   | 必需 | 默认值 | 描述                                         |
| ----------- | ------ | ---- | ------ | -------------------------------------------- |
| **name**    | string | ✅   | -      | 传感器的唯一标识名称                         |
| **objtype** | string | ✅   | -      | 被测量对象类型（"body"或"site"）             |
| **objname** | string | ✅   | -      | 被测量对象名称                               |
| **reftype** | string | ✅   | -      | 参考坐标系类型（"body"、"site"或"world"）    |
| **refname** | string | ❓   | -      | 参考对象名称（当 reftype 不为"world"时必需） |

**注意**: MotrixSim 目前暂不支持 MJCF 标准中的`cutoff`、`noise`和`user`属性。

## 📝 配置示例

### 相对于全局坐标系的测量

```xml
<!-- 定义要测量的对象 -->
<body name="robot_arm" pos="1 0 0">
    <site name="end_effector" pos="2 0 0"/>
</body>

<!-- 相对于全局坐标系的传感器 -->
<sensor>
    <framepos name="arm_global_pos" objtype="body" objname="robot_arm"
               reftype="world"/>
    <framequat name="arm_global_quat" objtype="body" objname="robot_arm"
                reftype="world"/>
    <framelinvel name="arm_global_vel" objtype="body" objname="robot_arm"
                  reftype="world"/>
</sensor>
```

### 相对于其他物体的测量

```xml
<!-- 基准物体 -->
<body name="base_station" pos="0 0 0"/>
<!-- 移动物体 -->
<body name="mobile_robot" pos="2 1 0"/>

<!-- 相对于基准站的传感器 -->
<sensor>
    <framepos name="robot_relative_pos"
               objtype="body" objname="mobile_robot"
               reftype="body" refname="base_station"/>
    <framequat name="robot_relative_quat"
                objtype="body" objname="mobile_robot"
                reftype="body" refname="base_station"/>
</sensor>
```

### 相对于 site 的测量

```xml
<body name="robot_body">
    <site name="reference_site" pos="0 0 1"/>
    <site name="target_site" pos="1 0 0"/>
</body>

<!-- 相对于reference_site的target_site状态 -->
<sensor>
    <framepos name="target_relative_pos"
               objtype="site" objname="target_site"
               reftype="site" refname="reference_site"/>
    <framexaxis name="target_x_axis"
                 objtype="site" objname="target_site"
                 reftype="site" refname="reference_site"/>
</sensor>
```

## 🚀 使用示例

### Python API 使用

```python
import numpy as np
from motrixsim import load_model, SceneData, step

# 加载场景
model = load_model("scene_with_frame_sensors.xml")
data = SceneData(model)

# 运行仿真并获取参考框传感器数据
for step_count in range(1000):
    step(model, data)

    # 获取全局位置
    global_pos = model.get_sensor_value("arm_global_pos", data)
    if global_pos.ndim == 1:
        print(f"机器人全局位置: [{global_pos[0]:.3f}, {global_pos[1]:.3f}, {global_pos[2]:.3f}] m")

    # 获取全局姿态（四元数）
    global_quat = model.get_sensor_value("arm_global_quat", data)
    if global_quat.ndim == 1:
        # MotrixSim四元数格式: [x, y, z, w]
        print(f"机器人姿态四元数(xyzw): [{global_quat[0]:.3f}, {global_quat[1]:.3f}, {global_quat[2]:.3f}, {global_quat[3]:.3f}]")

        # 如果需要转换为MuJoCo格式 [w, x, y, z]:
        mujoco_quat = np.array([global_quat[3], global_quat[0], global_quat[1], global_quat[2]])
        print(f"MuJoCo格式四元数(wxyz): [{mujoco_quat[0]:.3f}, {mujoco_quat[1]:.3f}, {mujoco_quat[2]:.3f}, {mujoco_quat[3]:.3f}]")

    # 获取相对位置
    relative_pos = model.get_sensor_value("robot_relative_pos", data)
    if relative_pos.ndim == 1:
        distance = np.linalg.norm(relative_pos)
        print(f"相对距离: {distance:.3f} m")

    # 获取轴向信息
    x_axis = model.get_sensor_value("target_x_axis", data)
    if x_axis.ndim == 1:
        print(f"目标X轴方向: [{x_axis[0]:.3f}, {x_axis[1]:.3f}, {x_axis[2]:.3f}]")
```

### 实际应用场景

```python
# 四元数格式转换函数
def motrix_to_mujoco_quat(motrix_quat):
    """MotrixSim XYZW格式转MuJoCo WXYZ格式"""
    # MotrixSim: [x, y, z, w] -> MuJoCo: [w, x, y, z]
    return np.array([motrix_quat[3], motrix_quat[0], motrix_quat[1], motrix_quat[2]])

def mujoco_to_motrix_quat(mujoco_quat):
    """MuJoCo WXYZ格式转MotrixSim XYZW格式"""
    # MuJoCo: [w, x, y, z] -> MotrixSim: [x, y, z, w]
    return np.array([mujoco_quat[1], mujoco_quat[2], mujoco_quat[3], mujoco_quat[0]])

# 四元数处理函数（适配MotrixSim的XYZW格式）
def quaternion_to_euler(quat):
    """MotrixSim四元数转欧拉角（XYZW格式）"""
    x, y, z, w = quat  # 注意：MotrixSim是XYZW格式
    # Roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    # Pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    if abs(sinp) >= 1:
        pitch = np.copysign(np.pi / 2, sinp)  # use 90 degrees if out of range
    else:
        pitch = np.arcsin(sinp)

    # Yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw

# 距离和方向分析
def analyze_relative_position(relative_pos, threshold=2.0):
    """分析相对位置关系"""
    distance = np.linalg.norm(relative_pos)

    if distance < threshold:
        return "接近", distance

    # 计算方向向量
    direction = relative_pos / distance

    # 判断主要方向
    max_component = np.argmax(np.abs(direction))
    directions = ['+X', '+Y', '+Z', '-X', '-Y', '-Z']
    actual_direction = directions[max_component] if direction[max_component] > 0 else directions[max_component + 3]

    return f"远离({actual_direction}方向)", distance

# 姿态相似度计算
def calculate_orientation_similarity(quat1, quat2):
    """计算两个四元数的相似度"""
    # 归一化四元数
    quat1_norm = quat1 / np.linalg.norm(quat1)
    quat2_norm = quat2 / np.linalg.norm(quat2)

    # 计算点积
    dot_product = np.dot(quat1_norm, quat2_norm)

    # 确保在有效范围内
    dot_product = np.clip(dot_product, -1.0, 1.0)

    # 计算角度差
    angle_diff = np.arccos(abs(dot_product))

    return np.degrees(angle_diff)

# 轴向分析
def analyze_axis_orientation(axis_vector):
    """分析轴向的方向"""
    # 归一化向量
    axis = axis_vector / np.linalg.norm(axis_vector)

    # 与各坐标轴的夹角
    x_angle = np.degrees(np.arccos(np.clip(axis[0], -1, 1)))
    y_angle = np.degrees(np.arccos(np.clip(axis[1], -1, 1)))
    z_angle = np.degrees(np.arccos(np.clip(axis[2], -1, 1)))

    return {
        'x_angle': x_angle,
        'y_angle': y_angle,
        'z_angle': z_angle,
        'dominant_axis': np.argmax(np.abs(axis))
    }
```

## 📊 物理原理

参考框传感器基于坐标变换原理：

1. **坐标变换**: 将对象的姿态从自身坐标系变换到指定的参考坐标系
2. **相对测量**: 提供两个物体之间的相对位姿信息
3. **四元数表示**: 使用四元数避免万向节锁问题，提供稳定的姿态表示

变换公式：

```
T_ref = T_ref_to_world⁻¹ * T_obj_to_world
```

其中 T 表示齐次变换矩阵。

## ⚠️ 注意事项

1. **参考坐标系**: 必须明确指定参考坐标系类型和名称
2. **对象存在性**: 被测量对象和参考对象必须存在于场景中
3. **四元数格式差异**: MotrixSim 使用 **XYZW** 格式 `[x, y, z, w]`，与 MuJoCo 的 WXYZ 格式 `[w, x, y, z]` 不同！
4. **格式转换**: 如需与 MuJoCo 兼容，需要进行四元数格式转换：`mujoco_quat = [motrix_quat[3], motrix_quat[0], motrix_quat[1], motrix_quat[2]]`
5. **不支持高级属性**: MotrixSim 目前不支持`cutoff`、`noise`和`user`属性
6. **数据类型**: 返回值是`numpy.ndarray`类型，形状支持向量化环境
7. **参考系一致**: 确保参考坐标系和对象坐标系的一致性
