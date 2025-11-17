# 🌡️ 传感器（Sensor）

通过配置传感器，用户可以更方便的获取物理对象状态信息，如位置，旋转，速度，加速度等。传感器不会影响到物理仿真的结果，可以添加在不同的对象上，如刚体（Body）、参考点（Site）、关节（Joint）等。

## 📋 传感器概览表

| 传感器类型             | 测量对象        | 坐标系     | 返回维度 | 主要应用                   |
| ---------------------- | --------------- | ---------- | -------- | -------------------------- |
| accelerometer          | site 线性加速度 | site 局部  | 3        | 运动感知、跌倒检测         |
| velocimeter            | site 线性速度   | site 局部  | 3        | 速度监测、运动控制         |
| gyro                   | site 角速度     | site 局部  | 3        | 姿态控制、运动估计         |
| jointpos               | 关节位置/角度   | 关节轴     | 1        | 位置控制、限位监测         |
| jointvel               | 关节速度        | 关节轴     | 1        | 速度控制、运动监控         |
| framepos               | 对象位置        | 指定参考系 | 3        | 相对定位、路径跟踪         |
| framequat              | 对象姿态        | 指定参考系 | 4        | 姿态控制、方向监测         |
| framexaxis/yaxis/zaxis | 对象轴向        | 指定参考系 | 3        | 方向分析、对准控制         |
| framelinvel            | 对象线速度      | 指定参考系 | 3        | 速度跟踪、运动分析         |
| frameangvel            | 对象角速度      | 指定参考系 | 3        | 角速度控制、旋转监测       |
| framelinacc            | 对象线加速度    | 指定参考系 | 3        | 加速度监测、动态分析       |
| subtreecom             | 子树质心        | 全局       | 3        | 稳定性分析、质心跟踪       |
| subtreelinvel          | 子树质心速度    | 全局       | 3        | 动量分析、运动监测         |
| subtreeangmom          | 子树角动量      | 全局       | 3        | 动量守恒、旋转分析         |
| touch                  | site 接触法向力 | site 局部  | 1        | 触觉感知、碰撞检测、力反馈 |

## 🚀 快速开始

### 传感器配置示例

传感器的配置示例可参考 [`examples/assets/site_and_sensor.xml`](../../../../examples/assets/site_and_sensor.xml)：

```xml
<sensor>
    <!-- 局部坐标系传感器 -->
    <accelerometer name="acc_0" site="imu_0"/>
    <velocimeter name="vel_0" site="imu_0"/>
    <gyro name="gyro_0" site="imu_0"/>

    <!-- 关节传感器 -->
    <jointpos name="joint_pos" joint="shoulder"/>
    <jointvel name="joint_vel" joint="shoulder"/>

    <!-- 参考框传感器 -->
    <framepos name="global_pos" objtype="body" objname="robot" reftype="world"/>

    <!-- 子树传感器 -->
    <subtreecom name="robot_com" body="torso"/>

    <!-- 接触传感器 -->
    <touch name="palm_touch" site="palm_site"/>
</sensor>
```

```{note}
**MotrixSim 限制**: 目前不支持 MJCF 标准中的`cutoff`、`noise`和`user`属性
```

### Python API 使用

获取指定传感器的数据：

```{literalinclude} ../../../../examples/site_and_sensor.py
:language: python
:dedent:
:start-after: "# tag::get_sensor_value[]"
:end-before:  "# end::get_sensor_value[]"
```

```{toctree}
:maxdepth: 1
:caption: 传感器详细文档

sensor/accelerometer
sensor/velocimeter
sensor/gyro
sensor/joint
sensor/frame
sensor/subtree
sensor/touch
```
