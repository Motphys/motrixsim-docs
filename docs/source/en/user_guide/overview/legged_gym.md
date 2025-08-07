# 🦿 Legged Gym

:::{tip}
For models and code, see the [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) repository.

Before running the examples, please refer to {doc}`../overview/environment_setup` to complete the environment setup.
:::

In the usage examples, we provide a simple framework similar to legged gym, making it convenient for users to test policies trained in legged gym (sim2sim) within MotrixSim.

For more information about the legged gym training framework, click [here](https://github.com/leggedrobotics/legged_gym).

MotrixSim includes two legged gym sim2sim examples: Unitree Go1 and the accelerated evolution T1.

You can run these inference examples with:

```bash
pdm run legged_gym/scripts/go1_play.py
```

and

```bash
pdm run legged_gym/scripts/T1_play.py
```

The results are as follows:

::::{grid} 1 1 2 2

:::{grid-item}

```{video} /_static/videos/go1.mp4
:poster: /_static/images/poster/go1.jpg
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

```{video} /_static/videos/t1.mp4
:poster: /_static/images/poster/t1.jpg
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

The legged gym sim2sim framework we provide is designed to be as consistent as possible with legged gym's Env design, minimizing the learning curve for sim2sim adaptation. The directory structure is as follows:

-   legged_gym
    -   envs: Custom environments
    -   policy: Policy files
    -   resources: MJCF model files
    -   scripts: Play scripts
    -   utils: Utility functions

Taking T1 sim2sim as an example, we create a folder named T1 under envs, which contains two files: `T1.py` and `T1_config.py`, inheriting from `legged_gym.envs.base.legged_robot.Legged_Robot` and `legged_gym.envs.base.legged_robot_config.LeggedRobotCfg`, respectively. You can override the config or env to implement custom observation and action calculations.

The play script for T1 is defined in `legged_gym/scripts/T1_play.py`:

```{literalinclude} ../../../../legged_gym/scripts/T1_play.py
:language: python
:dedent:
```
