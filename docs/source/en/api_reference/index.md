# API Reference

MotrixSim is a high-performance physics simulation engine that provides a comprehensive Python API for robotics simulation, physical modeling, and real-time rendering.

## 🚀 Quick Start

**[API Quick Reference](api_quick_reference.md)** - Summarizes commonly used APIs grouped by functionality to help you quickly locate the required interfaces

## 📋 API Architecture

The MotrixSim API is designed with a layered architecture to meet the needs of different users:

| Layer              | Module                                   | Features                            | Application Scenarios                            |
| ------------------ | ---------------------------------------- | ----------------------------------- | ------------------------------------------------ |
| **Core**           | [`motrixsim`](core/index.md)             | Simple, user-friendly API           | Robot control, reinforcement learning            |
| **Model Building** | [`motrixsim.msd`](msd/index.md)          | Programmatic model combining        | Multi-robot scenes, dynamic model assembly       |
| **Rendering**      | [`motrixsim.render`](rendering/index.md) | Real-time rendering, interactive UI | Simulation visualization, debugging and analysis |
| **IK Module**      | [`motrixsim.ik`](ik/index.md)            | Efficient solving, easy to use      | Inverse kinematics solving                       |

## 📚 Detailed Module Documentation

```{toctree}
:titlesonly:

api_quick_reference
core/index
msd/index
rendering/index
rendering/widgets
ik/index
```
