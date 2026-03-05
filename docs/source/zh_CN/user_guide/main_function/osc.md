# 🎯 操作空间控制器（OSC）

MotrixSim 在 `motrixsim.osc` 模块中提供了操作空间控制器（OSC）。该模块暴露了一个无状态的求解器类 [`OscSolver`]，用于计算机器人末端执行器任务空间控制所需的关节力矩。

## 基本概念

操作空间控制（OSC）是一种针对机器人机械臂的力矩控制方法。与反向运动学（IK）不同——IK 计算关节*位置*以达到期望的末端执行器位姿——OSC 直接计算考虑了机器人完整动力学（惯性、科里奥利力、重力）的关节*力矩*。用一个公式来表示 OSC 计算过程就是：`joint_torques = compute_osc(osc_solver, ik_chain, end_effector_goal)`。

## IK Model

OSC 复用 `motrixsim.ik` 中的 [`IkChain`] 来定义运动链。IK 链由一系列连接的关节和一个末端执行器组成，如下图所示：

![ikchain](/_static/images/ikchain.png)

在 MotrixSim 中，您可以通过以下方式创建一个 IK 链模型：

```{literalinclude} ../../../../examples/osc.py
:language: python
:dedent:
:start-after: "# tag::create_osc_solver"
:end-before:  "# end::create_osc_solver"
```

以上代码通过指定末端连杆和可选的起始连杆来创建一个 IK 链模型。您还可以通过 `end_effector_offset` 参数来定义末端执行器相对于末端连杆的偏移。

您可以查看 API 文档了解更多关于 [`IkChain`] 的信息。

## OSC Solver

在定义了 IK 链之后，创建 [`OscSolver`] 来执行实际的力矩计算。求解器是**无状态**的——它不持有任何仿真状态。用户自行管理 `IkChain` 和目标变量，在每个控制步骤中按需更新它们。

**构造参数：**

| 参数               | 类型                 | 默认值  | 说明                               |
| ------------------ | -------------------- | ------- | ---------------------------------- |
| `control_ori`      | `bool`               | `True`  | 在位置控制之外启用姿态控制         |
| `uncouple_pos_ori` | `bool`               | `True`  | 解耦位置和姿态控制                 |
| `kp`               | `float` 或 `ndarray` | `150.0` | 跟踪目标的刚度增益                 |
| `damping_ratio`    | `float`              | `1.0`   | 阻尼比；`1.0` = 临界阻尼（无过冲） |
| `nullspace_kp`     | `float`              | `10.0`  | 零空间关节位置控制的刚度增益       |

然后通过调用 `solve` 方法来计算关节力矩：

```{literalinclude} ../../../../examples/osc.py
:language: python
:dedent:
:start-after: "# tag::solve_osc"
:end-before:  "# end::solve_osc"
```

`solve` 方法返回形状为 `(*data.shape, num_dof)` 的 `numpy.ndarray`，包含计算得到的关节力矩。用户负责将这些力矩应用到 `data.actuator_ctrls` 中正确的执行器索引上。

**`solve` 参数：**

| 参数                  | 形状                     | 说明                                                                |
| --------------------- | ------------------------ | ------------------------------------------------------------------- |
| `chain`               | —                        | 定义运动链的 `IkChain`                                              |
| `ee_target_pos`       | `(*data.shape, 3)`       | 世界坐标系中的目标末端执行器位置 `[x, y, z]`                        |
| `ee_target_ori`       | `(*data.shape, 3)`       | 以轴角表示的目标姿态 `[ax, ay, az]`（方向 = 旋转轴，大小 = 弧度角） |
| `nullspace_joint_pos` | `(*data.shape, num_dof)` | 零空间控制的参考关节位置                                            |
| `data`                | —                        | 当前 `SceneData`（支持批量多世界仿真）                              |

**参数调优：**

**`kp` — 刚度增益**

控制控制器跟踪目标的积极程度。较高的值产生更快的响应，但可能导致振荡或力矩饱和。

-   **小值（50–100）**：柔顺行为
-   **中值（150–200）**：大多数应用的良好平衡点，推荐起始值
-   **大值（200–400）**：刚硬、快速跟踪；注意力矩饱和

**`damping_ratio`**

控制相对于 `kp` 的速度阻尼。

-   **`1.0`**：临界阻尼——推荐起始值，无过冲
-   **`< 1.0`**：欠阻尼——更快但可能振荡
-   **`> 1.0`**：过阻尼——更慢但非常稳定

**`nullspace_kp`**

在不干扰末端执行器任务的情况下，将关节驱向 `nullspace_joint_pos`。适用于避免冗余关节超限。设置为 `0.0` 可禁用。典型范围：`5–20`。

```{note}
OSC Solver 在进行求解时，可能会遇到不稳定或跟踪效果差的情况，原因是多样的，例如：

- 目标位置超出了机械臂的工作空间
- 力矩饱和（达到执行器限制）——减小 `kp` 或增大 `damping_ratio`
- 机器人接近奇异配置——减小 `kp` 或将机器人从奇异点移开

**提高性能的技巧：**
- 从 `kp = 150.0`、`damping_ratio = 1.0` 开始，再逐步调整
- 将 `nullspace_joint_pos` 初始化为机器人的初始配置，以避免关节超限
- 对于批量（多世界）仿真，所有输入必须具有与 `data.shape` 匹配的前导批次维度
- 求解器仅计算运动链 DOF 对应的力矩——需手动将其映射到 `data.actuator_ctrls` 中正确的索引（参见示例）
```

_查看完整代码请见 [examples/osc.py](../../../../examples/osc.py)_

[`OscSolver`]: motrixsim.osc.OscSolver
[`IkChain`]: motrixsim.ik.IkChain
