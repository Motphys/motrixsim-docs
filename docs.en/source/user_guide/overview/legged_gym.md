# 🦿 Legged Gym

:::{tip}
模型和代码详见 [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) 仓库

在运行示例之前，请先参考 {doc}`../overview/environment_setup` 完成环境准备。
:::

我们在使用范例里，提供了一个简易的、类似 legged gym 的框架，方便用户将 legged gym 里训练的策略 sim2sim 到 MotrixSim 中进行测试。

关于 legged gym 训练框架，您可以点击 [这里](https://github.com/leggedrobotics/legged_gym) 了解更多信息。

在 MotrixSim 中附带了两个 legged gym sim2sim 的示例，分别是 Unitree Go1 和加速进化的 T1.

您可以通过

```bash
pdm run legged_gym/scripts/go1_play.py
```

以及

```bash
pdm run legged_gym/scripts/T1_play.py
```

来分别运行这两个 Inference 示例，效果如下：

::::{grid} 1 1 2 2

:::{grid-item}

```{video} ../../_static/videos/go1.mp4
:poster: ../../_static/images/poster/go1.jpg
:caption: Go1
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

:::{grid-item}

```{video} ../../_static/videos/t1.mp4
:poster: ../../_static/images/poster/t1.jpg
:caption: T1
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

:::

::::

## Custom Env

我们提供的 legged gym sim2sim 框架，尽量在 Env 的设计上与 legged gym 保持一致，以减少您进行 sim2sim 时的理解成本。其目录结构如下：

-   legged_gym
    -   envs: 自定的 Envs
    -   policy: 策略文件
    -   resources: mjcf 模型文件
    -   scripts: play 脚本
    -   utils: 工具函数

以 T1 的 sim2sim 为例，我们在 envs 下创建了一个名为 T1 的文件夹，里面包含了两个文件：`T1.py` 和 `T1_config.py`，分别继承自 `legged_gym.envs.base.legged_robot.Legged_Robot` 和 `legged_gym.envs.base.legged_robot_config.LeggedRobotCfg` 。 您可以重载 config 或者 env 来实现自定义的 observations 以及 actions 计算。

`legged_gym/scripts/T1_play.py` 中定义了 T1 的 play 脚本：

```{literalinclude} ../../../../legged_gym/scripts/T1_play.py
:language: python
:dedent:
```
