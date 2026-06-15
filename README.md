# MotrixSim Docs

English | [简体中文](README.zh-CN.md)

![PyPI - Version](https://img.shields.io/pypi/v/motrixsim)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/motrixsim-core)

![GitHub License](https://img.shields.io/github/license/motphys/motrixsim-docs)

`MotrixSim` is a high-performance physics simulation engine designed for multibody dynamics and robot simulation. It provides an efficient and stable simulation platform for a wide range of applications, including robot control, reinforcement learning, and industrial simulation.

> Documentation: https://motrixsim.readthedocs.io
>
> Online demo: https://motrix.motphys.com

## Key Features

-   **Physics simulation**: Supports rigid-body dynamics, collision detection, and core physics simulation capabilities.
-   **Generalized-coordinate modeling**: Uses generalized coordinates to model complex multibody systems.
-   **New solver architecture**: Provides efficient and stable multibody dynamics computation through in-house constraint models and solvers.
-   **High-performance computing**: The CPU backend is developed in Rust, providing strong performance and memory safety.
-   **Python API**: Offers a concise Python interface for rapid development and prototyping.
-   **Robot support**: Optimized for robot simulation and highly compatible with the MJCF model format.

## Use Cases

-   Robot control algorithm development and testing
-   Reinforcement learning environment construction
-   Industrial real-time physics simulation
-   Physical phenomenon simulation and analysis
-   Engineering design validation
-   Education and research

## MotrixSim Ecosystem and Research

-   **MotrixLab**: A robot reinforcement learning framework built on MotrixSim. It provides environment registration, training configuration, RL framework adapters, evaluation, and replay tools for quadrupeds, humanoids, robotic arms, dexterous hands, and related robot tasks. Repository: [Motphys/MotrixLab](https://github.com/Motphys/MotrixLab), documentation: [motrixlab.readthedocs.io](https://motrixlab.readthedocs.io/).
-   **GS-Playground**: A high-fidelity embodied simulation platform developed by Tsinghua AIR DISCOVER Lab, Motphys, and collaborators. It combines MotrixSim parallel physics simulation with 3D Gaussian Splatting rendering for visual navigation, manipulation, locomotion, and Sim2Real research. The work has been accepted by RSS 2026. Repository: [discoverse-dev/gs_playground](https://github.com/discoverse-dev/gs_playground), paper: [arXiv:2604.25459](https://arxiv.org/abs/2604.25459), project page: [gsplayground.github.io](https://gsplayground.github.io/).
-   **UniLab**: A heterogeneous CPU-simulation / GPU-learning system for robot reinforcement learning. MotrixSim is integrated as a CPU-batched physics backend in the unified training runtime, supporting large-scale rollouts and cross-platform training. Repository: [unilabsim/UniLab](https://github.com/unilabsim/UniLab), paper: [arXiv:2605.30313](https://arxiv.org/abs/2605.30313).

## 🚀 Quick Start

> The following example uses [UV](https://docs.astral.sh/uv/), a Python project management tool.
>
> Please [install UV](https://docs.astral.sh/uv/getting-started/installation/) before getting started.

### 1. Install Git LFS

This repository contains large files managed by [Git LFS](https://git-lfs.com/). Install Git LFS and initialize it first:

```bash
git lfs install
```

### 2. Clone the Repository

```bash
git clone https://github.com/Motphys/motrixsim-docs

cd motrixsim-docs
```

### 3. Install Dependencies

```bash
uv sync
```

### 4. Run Comparisons and Examples

> See the [documentation](https://motrixsim.readthedocs.io) for details.

## 📬 Contact

Questions and suggestions are welcome:

-   GitHub Issues: [Submit an issue](https://github.com/Motphys/motrixsim-docs/issues)

-   Discussions: [Join the discussion](https://github.com/Motphys/motrixsim-docs/discussions)

## Citation

If you use MotrixSim in your research, please cite it as follows:

```bibtex
@software{motrixsim2026,
  title  = {MotrixSim: A Physics Simulation Engine for Robotics and Embodied AI},
  author = {{Motphys Team}},
  year   = {2026},
  url    = {https://motrixsim.readthedocs.io/},
  note   = {Python binary package}
}
```
