# MotrixSim Docs

[English](README.md) | 简体中文

![PyPI - Version](https://img.shields.io/pypi/v/motrixsim)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/motrixsim-core)

![GitHub License](https://img.shields.io/github/license/motphys/motrixsim-docs)

`MotrixSim` 是一个高性能的物理仿真引擎，专为多体动力学和机器人仿真设计。它提供了一个高效、稳定的物理仿真平台，支持广泛的应用场景，包括机器人控制、强化学习、工业仿真等。

> 文档地址：https://motrixsim.readthedocs.io
>
> 线上体验地址：https://motrix.motphys.com

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

## MotrixSim 生态与学术成果

-   **MotrixLab**: 基于 MotrixSim 的机器人强化学习框架，提供环境注册、训练配置、RL 框架适配、评测与回放等能力，面向四足、人形、机械臂和灵巧手等机器人任务。仓库：[Motphys/MotrixLab](https://github.com/Motphys/MotrixLab)，文档：[motrixlab.readthedocs.io](https://motrixlab.readthedocs.io/)。
-   **GS-Playground**: 清华大学智能产业研究院（AIR）DISCOVER Lab 联合谋先飞等团队完成的高保真具身仿真平台工作，结合 MotrixSim 并行物理仿真与 3D Gaussian Splatting 高保真渲染，用于视觉导航、操作抓取、运动控制和 Sim2Real 研究。该工作已被 RSS 2026 接收。仓库：[discoverse-dev/gs_playground](https://github.com/discoverse-dev/gs_playground)，论文：[arXiv:2604.25459](https://arxiv.org/abs/2604.25459)，项目主页：[gsplayground.github.io](https://gsplayground.github.io/)。
-   **UniLab**: 异构 CPU-simulation / GPU-learning 机器人强化学习训练系统。MotrixSim 作为 CPU-batched physics backend 接入统一训练 runtime，为大规模 rollout 和跨平台训练提供物理仿真后端。仓库：[unilabsim/UniLab](https://github.com/unilabsim/UniLab)，论文：[arXiv:2605.30313](https://arxiv.org/abs/2605.30313)。

## 🚀 快速开始

> 以下示例使用了 Python 项目管理工具：[UV](https://docs.astral.sh/uv/)
>
> 在开始之前，请先[安装](https://docs.astral.sh/uv/getting-started/installation/)该工具。

### 1. 安装 Git LFS

仓库中包含通过 Git LFS 管理的大文件，请先安装 [Git LFS](https://git-lfs.com/) 并完成初始化：

```bash
git lfs install
```

### 2. 克隆仓库:

```bash
git clone https://github.com/Motphys/motrixsim-docs

cd motrixsim-docs

git lfs pull
```

> 如果您身处中国大陆，建议通过下面方式克隆仓库，并配置国内镜像源以加速依赖下载：
>
> 1. 克隆仓库
>
>     ```bash
>     git clone https://www.modelscope.cn/datasets/motphysdevelopers/motrixsim-docs.git
>     cd motrixsim-docs
>     git lfs pull
>     ```
>
> 2. 修改 `pyproject.toml` 文件，添加国内镜像源
>
>     ```toml
>     [[tool.uv.index]]
>     name = "mirror"
>     # 请填写您选择的国内镜像源，例如：
>     # 清华源: "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
>     url = ""
>     ```

### 3. 安装依赖

```bash
uv sync
```

### 4. 执行对比与示例

> 参考 [文档](https://motrixsim.readthedocs.io) 中的说明

## 📬 联系方式

有问题或建议？欢迎通过以下方式联系我们：

-   GitHub Issues: [提交问题](https://github.com/Motphys/motrixsim-docs/issues)

-   Discussions: [加入讨论](https://github.com/Motphys/motrixsim-docs/discussions)

<p align="center">
  <img src="docs/source/_static/images/weichat-qr.jpg" alt="微信二维码" width="180">
</p>

<p align="center">添加小助手微信进群，请备注：<code>MotrixSim 交流</code></p>

## 引用

如果您在研究中使用 MotrixSim，请按以下方式引用：

```bibtex
@software{motrixsim2026,
  title  = {MotrixSim: A Physics Simulation Engine for Robotics and Embodied AI},
  author = {{Motphys Team}},
  year   = {2026},
  url    = {https://motrixsim.readthedocs.io/},
  note   = {Python binary package}
}
```
