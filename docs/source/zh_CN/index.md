# MotrixSim

MotrixSim 是一个高性能的物理仿真引擎，专为多体动力学和机器人仿真设计。它提供了一个高效、稳定的物理仿真平台，支持广泛的应用场景，包括机器人控制、强化学习、工业仿真等。

::::{grid} 1 2 3 3

:::{grid-item}

```{video} _static/videos/g1_parlour.mp4
:poster: _static/images/poster/g1_parlour.jpg
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} _static/videos/complex_car.mp4
:poster: _static/images/poster/complex_car.jpg
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} _static/videos/go2-ssgi.mp4
:poster: _static/images/poster/go2-ssgi.jpg
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} _static/videos/arm.mp4
:poster: _static/images/poster/arm.jpg
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} _static/videos/g1_terrian.mp4
:poster: _static/images/poster/g1_terrian.jpg
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} _static/videos/shadow_hand_repose.mp4
:poster: _static/images/poster/shadow_hand_repose.jpg
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

::::

## 主要特性

-   **物理仿真**: 支持刚体动力学、碰撞检测等完整的物理仿真功能
-   **广义坐标建模**: 采用广义坐标系统，支持复杂的多体系统建模
-   **全新求解器**: 采用自研的约束模型和求解器，提供高效、稳定的多体动力学计算
-   **高性能计算**: CPU 版本基于 Rust 开发，提供出色的性能和内存安全性
-   **Python API**: 简洁易用的 Python 接口，便于快速开发和原型制作
-   **机器人支持**: 专门优化的机器人仿真功能，高度兼容 MJCF 模型格式

## 适用场景

-   机器人控制算法开发和测试
-   强化学习环境构建
-   工业实时物理仿真
-   物理现象模拟和分析
-   工程设计验证
-   教育和研究

## MotrixSim 生态与研究

-   **MotrixLab**：基于 MotrixSim 构建的机器人强化学习框架。提供环境注册、训练配置、RL 框架适配、评估和回放工具，覆盖四足、人形、机械臂、灵巧手等机器人任务。仓库：[Motphys/MotrixLab](https://github.com/Motphys/MotrixLab)，文档：[motrixlab.readthedocs.io](https://motrixlab.readthedocs.io/)。
-   **GS-Playground**：由清华 AIR DISCOVER 实验室、Motphys 及合作者共同开发的高保真具身仿真平台。它将 MotrixSim 的并行物理仿真与 3D Gaussian Splatting 渲染相结合，面向视觉导航、操作、运动控制和 Sim2Real 研究。相关工作已被 RSS 2026 接收。仓库：[discoverse-dev/gs_playground](https://github.com/discoverse-dev/gs_playground)，论文：[arXiv:2604.25459](https://arxiv.org/abs/2604.25459)，项目主页：[gsplayground.github.io](https://gsplayground.github.io/)。
-   **UniLab**：一个 CPU 仿真 / GPU 学习的异构机器人强化学习系统。MotrixSim 作为 CPU 批量物理后端集成到统一训练运行时中，支持大规模 rollout 和跨平台训练。仓库：[unilabsim/UniLab](https://github.com/unilabsim/UniLab)，论文：[arXiv:2605.30313](https://arxiv.org/abs/2605.30313)。

```{toctree}
:maxdepth: 1

user_guide/index
```

```{toctree}
:maxdepth: 1

api_reference/index
```
