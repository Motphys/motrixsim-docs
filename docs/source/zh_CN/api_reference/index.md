# API 参考

MotrixSim 是一个高性能的物理仿真引擎，提供了丰富的 Python API 用于机器人仿真、物理建模和实时渲染。

## 🚀 快速开始

**[API 快速参考](api_quick_reference.md)** - 汇总常用 API 并按功能分组，帮助你快速定位所需接口

## 📋 API 层级架构

MotrixSim 的 API 设计采用分层架构，满足不同用户的使用需求：

| 层级         | 模块                                     | 特点               | 适用场景             |
| ------------ | ---------------------------------------- | ------------------ | -------------------- |
| **核心模块** | [`motrixsim`](core/index.md)             | 简单易用、接口友好 | 机器人控制、强化学习 |
| **渲染模块** | [`motrixsim.render`](rendering/index.md) | 实时渲染、交互界面 | 仿真可视化、调试分析 |

## 📚 详细模块文档

```{toctree}
:titlesonly:

api_quick_reference
core/index
rendering/index
```
