# MotrixSim

MotrixSim 是一个高性能的物理仿真引擎，专为多体动力学和机器人仿真设计。它提供了一个高效、稳定的物理仿真平台，支持广泛的应用场景，包括机器人控制、强化学习、工业仿真等。

<style>
.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin: 30px 0;
}
.video-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.video-item video {
  width: 100%;
  border-radius: 4px;
}
</style>

<div class="video-grid">
  <div class="video-item">
    <video controls loop autoplay style="width: 100%;">
        <source src="_static/videos/t1.webm" type="video/webm">
    </video>
  </div>
  <div class="video-item">
    <video controls loop autoplay style="width: 100%;">
        <source src="_static/videos/gyroscope_motrixsim.webm" type="video/webm">
    </video>
  </div>
  <div class="video-item">
    <video controls loop autoplay style="width: 100%;">
        <source src="_static/videos/go1.webm" type="video/webm">
    </video>
  </div>
  <div class="video-item">
    <video controls loop autoplay style="width: 100%;">
        <source src="_static/videos/arm.webm" type="video/webm">
    </video>
  </div>
  <div class="video-item">
    <video controls loop autoplay style="width: 100%;">
        <source src="_static/videos/gyro_no_gravity.webm" type="video/webm">
    </video>
  </div>
  <div class="video-item">
    <video controls loop autoplay style="width: 100%;">
        <source src="_static/videos/store_motrixsim.webm" type="video/webm">
    </video>
  </div>

</div>

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
