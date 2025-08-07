# ⚖️ Case Comparison

:::{tip}
For models and code, see the [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) repository.

Before running the examples, please refer to {doc}`../overview/environment_setup` to complete the environment setup.
:::

We present several comparisons between MotrixSim and MuJoCo simulation results to give you an intuitive sense of MotrixSim's simulation advantages.

## Gravity Gyroscope

The precession and nutation simulation of a gravity gyroscope can evaluate the accuracy of a physics engine in simulating contact points and angular momentum.

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

It can be observed that MotrixSim produces more realistic physical effects, while the gyroscope simulated by MuJoCo exhibits irregular movement in the scene.

MotrixSim and MuJoCo use the same MJCF model: [`gyroscope.xml`](../../../../examples/assets/gyroscope.xml).

You can run these examples with:

```bash
pdm run examples/gyroscope.py
```

and

```bash
pdm run examples/mujoco/gyroscope.py
```

## Newton's Cradle

Newton's cradle is a classic physics demonstration that shows the conservation of momentum and energy in rigid body collisions.

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

In this example, MotrixSim and MuJoCo use two different MJCF files:

-   MotrixSim: [`newton_cradle_mt.xml`](../../../../examples/assets/newton_cradle_mt.xml)
-   MuJoCo: [`newton_cradle_muj.xml`](../../../../examples/assets/newton_cradle_mj.xml)

Since MuJoCo only supports soft contact, while MotrixSim supports both soft and hard contact, we made some extensions to the MJCF:

```xml
<geom solref="1 0" hard="true" />
```

Here, `hard=true` indicates a hard contact geometry. In this case, `solref=(bounciness, ERP)` specifies the restitution coefficient and ERP (error reduction parameter).

You can run these examples with:

```bash
pdm run examples/newton_cradle.py
```

and

```bash
pdm run examples/mujoco/newton_cradle.py
```

## Boston Dynamics Spot

In this example, we test the stability of MotrixSim and MuJoCo under large time steps using the Boston Dynamics Spot robot model.

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

It can be seen that MotrixSim remains stable under large time steps, while MuJoCo exhibits significant jitter and instability.

The model is taken from the mujoco menagerie repository, with the timestep modified to 0.01s. Model file: [`spot.xml`](../../../../examples/assets/boston_dynamics_spot/spot.xml).

You can run these examples with:

```bash
pdm run python -m motrixsim.run --file examples/assets/boston_dynamics_spot/scene.xml
```

and

```bash
pdm run python -m mujoco.viewer --mjcf=examples/assets/boston_dynamics_spot/scene.xml
```

## Store Shelf

This example is an internal test scenario where a large number of items are placed on shelves, evaluating the stability and accuracy of the physics engine in handling complex scenes.

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

MotrixSim remains stable when handling a large number of object contacts, while MuJoCo produces object jitter in this scenario.

You can run these examples with:

```bash
pdm run python -m motrixsim.run --file examples/assets/store/scene.xml
```

and

```bash
pdm run python -m mujoco.viewer --mjcf=examples/assets/store/scene.xml
```
