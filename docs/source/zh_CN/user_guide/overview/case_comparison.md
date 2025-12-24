# ⚖️ 用例对比

:::{tip}
模型和代码详见 [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) 仓库

在运行示例之前，请先参考 {doc}`../overview/environment_setup` 完成环境准备。
:::

我们展示一些 MotrixSim 与 MuJoCo 之间仿真效果的对比，以让您直观的感受到 MotrixSim 的仿真优势

## 重力陀螺

重力陀螺的进动与章动仿真可以评估物理引擎对于接触点以及角动量仿真的准确性。

::::{grid} 1 1 2 2

:::{grid-item}

```{video} /_static/videos/gyroscope_motrixsim.mp4
:poster: /_static/images/poster/gyroscope_motrixsim.jpg
:caption: MotrixSim
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} /_static/videos/gyroscope_mujoco.mp4
:poster: /_static/images/poster/gyroscope_mujoco.jpg
:caption: MuJoCo
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

::::

可以发现，MotrixSim 的物理效果更为真实，而 MuJoCo 仿真的陀螺在场景中出现不规则跑动。

MotrixSim 和 MuJoCo 使用同一份 mjcf 模型：[`gyroscope.xml`](../../../../examples/assets/gyroscope.xml).

您可以通过

```bash
uv run examples/gyroscope.py
```

以及

```bash
uv run examples/mujoco/gyroscope.py
```

来运行这两个示例。

## 牛顿摆

牛顿摆是一个经典的物理演示，展示了刚体碰撞中的动量和能量守恒。

::::{grid} 1 1 2 2

:::{grid-item}

```{video} /_static/videos/newton_cradle_motrixsim.mp4
:poster: /_static/images/poster/newton_cradle_motrixsim.jpg
:caption: MotrixSim
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} /_static/videos/newton_cradle_mujoco.mp4
:poster: /_static/images/poster/newton_cradle_mujoco.jpg
:caption: MuJoCo
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

::::

在这个例子中，MotrixSim 和 MuJoCo 使用了两份不同的 MJCF 文件：

-   MotrixSim: [`newton_cradle_mt.xml`](../../../../examples/assets/newton_cradle_mt.xml)
-   MuJoCo: [`newton_cradle_muj.xml`](../../../../examples/assets/newton_cradle_mj.xml)

因为 MuJoCo 只支持 Soft Contact， 而 MotrixSim 同时支持 Soft Contact 和 Hard Contact， 所以我们对 MJCF 作了一些扩展：

```xml
<geom solref="1 0" hard="true" />
```

这里的 `hard=true` 表示这是一个硬接触的几何体， 在此情况下， `solref=(bounciness, ERP)`表示弹性系数和 ERP（误差修正）的值。

您可以通过

```bash
uv run examples/newton_cradle.py
```

以及

```bash
uv run examples/mujoco/newton_cradle.py
```

来运行这两个示例。

## Boston Dynamics Spot

该例子中，我们测试 MotrixSim 和 MuJoCo 在大时间步长下的稳定性。采用的模型为 Boston Dynamics Spot 机器人。

::::{grid} 1 1 2 2

:::{grid-item}

```{video} /_static/videos/spot_motrixsim.mp4
:poster: /_static/images/poster/spot_motrixsim.jpg
:caption: MotrixSim
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} /_static/videos/spot_mujoco.mp4
:poster: /_static/images/poster/spot_mujoco.jpg
:caption: MuJoCo
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

::::

可以看到，MotrixSim 在大时间步长下仍然保持稳定，而 MuJoCo 则出现了明显的抖动和不稳定现象。

该模型取自 mujoco menagerie 仓库，然后我们将 timestep 修改为 0.01s，模型文件：[`spot.xml`](../../../../examples/assets/boston_dynamics_spot/spot.xml)。

您可以通过

```bash
uv run python -m motrixsim.run --file examples/assets/boston_dynamics_spot/scene.xml
```

以及

```bash
uv run python -m mujoco.viewer --mjcf=examples/assets/boston_dynamics_spot/scene.xml
```

来运行这两个示例。

## 货架

该例子是我们内部在测试的一个场景，货架上摆放了大量的商品，可以评估物理引擎在处理复杂场景时的稳定性和准确性。

::::{grid} 1 1 2 2

:::{grid-item}

```{video} /_static/videos/store_motrixsim.mp4
:poster: /_static/images/poster/store_motrixsim.jpg
:caption: MotrixSim
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} /_static/videos/store_mujoco.mp4
:poster: /_static/images/poster/store_mujoco.jpg
:caption: MuJoCo
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

::::

MotrixSim 在处理大量物体接触时表现稳定，而 MuJoCo 在这个场景中产生了物体抖动现象。

您可以通过

```bash
uv run python -m motrixsim.run --file examples/assets/store/scene.xml
```

以及

```bash
uv run python -m mujoco.viewer --mjcf=examples/assets/store/scene.xml
```

来运行这两个示例。

## 机械臂抓取稳定性
该用例比较 MotrixSim 与 MuJoCo 在 Franka 机械臂抓取小球时的接触稳定性。在测试中，给抓取器施加随机晃动扰动以模拟现实环境中的扰动源。结果显示 MotrixSim 在扰动下仍能保持稳固夹持，抑制相对滑移；而 MuJoCo 在相同条件下容易发生滑动，即使在模型中设置了 `<option noslip_iterations="1"/>`，仍无法完全消除滑移现象。

::::{grid} 1 1 3 3

:::{grid-item}

```{video} /_static/videos/grasp_shake_ball_motrix.mp4
:poster: /_static/images/poster/grasp_shake_ball_motrix.jpg
:caption: MotrixSim
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} /_static/videos/grasp_shake_ball_mujoco.mp4
:poster: /_static/images/poster/grasp_shake_ball_mujoco.jpg
:caption: MuJoCo
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} /_static/videos/grasp_shake_ball_mujoco_noslip_iterations=1.mp4
:poster: /_static/images/poster/grasp_shake_ball_mujoco_noslip_iterations=1.jpg
:caption: MuJoCo (`noslip_iterations=1`)
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

::::

要运行该对比示例，请分别执行：

```bash
uv run examples/grasp_shaking_test.py
```

以及

```bash
uv run examples/mujoco/grasp_shaking_test.py
```

该用例直观展示了两套仿真器在接触建模与摩擦处理上的差异，便于开发者评估在抓取与操纵任务中的稳定性表现。
