# MotrixSim

MotrixSim 是一个高性能的物理仿真引擎，专为多体动力学和机器人仿真设计。它提供了一个高效、稳定的物理仿真平台，支持广泛的应用场景，包括机器人控制、强化学习、工业仿真等。

::::{grid} 1 2 3 3

:::{grid-item}

```{video} _static/videos/g1_keyboard_control.mp4
:poster: _static/images/poster/g1_keyboard_control.jpg
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} _static/videos/gyroscope_motrixsim.mp4
:poster: _static/images/poster/gyroscope_motrixsim.jpg
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} _static/videos/go2_keyboard_control.mp4
:poster: _static/images/poster/go2_keyboard_control.jpg
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

```{video} _static/videos/store_motrixsim.mp4
:poster: _static/images/poster/store_motrixsim.jpg
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

```{toctree}
:maxdepth: 1

user_guide/index
```

```{toctree}
:maxdepth: 1

api_reference/index
```
