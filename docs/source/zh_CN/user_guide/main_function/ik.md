# 🦾 反向运动学（IK）

MotrixSim 提供了一个高效且易于使用的反向运动学（IK）求解器，位于`motrixsim.ik`模块中。
目前支持基于高斯-牛顿法的 IK 求解器（[`GaussNewtonSolver`]）和简单的 IK 链模型（[`IkChain`]）。

```{video} /_static/videos/ik.mp4
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

## 基本概念

Inverse Kinematics (IK) 是计算机器人末端执行器（如机械臂手爪）位置和姿态所需的关节参数的过程。与之相对的是正向运动学（Forward Kinematics），它是通过已知的关节参数来计算末端执行器的位置和姿态。
用一个公式来表示 IK 计算过程就是: `joint_dof_pos = compute_inverse_kinematic(ik_model, end_effector_pose)`。

## IK Model

IK 模型用于定义 IK 问题的结构和约束。当前 MotrixSim 仅支持由单自由度关节(Hinge,Slide)组成的链式结构(IKChain)。

### IK Chain

IK 链模型由一系列连接的关节和一个末端执行器组成, 如下图所示：

![ikchain](/_static/images/ikchain.png)

在 MotrixSim 中，您可以通过以下方式创建一个 IK 链模型：

```{literalinclude} ../../../../examples/ik.py
:language: python
:dedent:
:start-after: "# tag::create_ik_chain"
:end-before:  "# end::create_ik_chain"
```

以上代码通过指定末端连杆和可选的起始连杆来创建一个 IK 链模型。您还可以通过 `end_effector_offset` 参数来定义末端执行器相对于末端连杆的偏移。

您可以查看 API 文档了解更多关于 [`IkChain`] 的信息。

## IK Solver

在定义了 IKModel 之后，您可以使用 IK Solver 来做具体的 IK 求解工作。MotrixSim 目前支持基于高斯-牛顿法的 IK 求解器[`GaussNewtonSolver`]。

### Gauss-Newton IK Solver

高斯-牛顿法是一种用于非线性最小二乘问题的迭代优化算法。它通过线性化非线性函数并使用最小二乘法来更新参数估计，从而逐步逼近目标值。在 IK 求解中，高斯-牛顿法通过迭代调整关节参数，使得末端执行器的位置和姿态尽可能接近目标位置和姿态。

在 MotrixSim 中，您可以通过以下方式创建一个高斯-牛顿 IK 求解器：

```{literalinclude} ../../../../examples/ik.py
:language: python
:dedent:
:start-after: "# tag::create_ik_solver"
:end-before:  "# end::create_ik_solver"
```

然后通过调用 `solve` 方法来执行 IK 求解：

```{literalinclude} ../../../../examples/ik.py
:language: python
:dedent:
:start-after: "# tag::solve_ik"
:end-before:  "# end::solve_ik"
```

solve 方法返回 numpy.ndarray 对象，其形状为`(*data.shape, chain.num_dof_pos + 2)`. 其中 `chain.num_dof_pos` 是 IK 链的自由度数量，额外的两个元素分别表示求解器的收敛状态和迭代次数。

```{note}
IK Solver在进行求解时，可能会遇到无法收敛的情况，原因是多样的，例如:

- 目标位置超出了机械臂的工作空间
- IK过程并没有考虑碰撞等限制
- 机械臂的初始姿态距离目标位置过远，无法在设定的迭代次数内收敛
- ....

```

_查看完整代码请见 [examples/ik.py](../../../../examples/ik.py)_

[`IkChain`]: motrixsim.ik.IkChain
[`GaussNewtonSolver`]: motrixsim.ik.GaussNewtonSolver
