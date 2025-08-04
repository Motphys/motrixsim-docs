# ⚙️ Global Settings (Options)

`Options` is the global configuration object in MotrixSim, used to set various parameters for physical simulation. These parameters affect the accuracy, stability, and performance of the simulation.

## Basic Concepts

Common configuration parameters include:

| Parameter        | Description                          | Default Value |
| ---------------- | ------------------------------------ | ------------- |
| `timestep`       | Simulation time step (seconds)       | 0.002         |
| `gravity`        | Gravity acceleration [x, y, z]       | [0, 0, -9.81] |
| `max_iterations` | Max iterations for constraint solver | 100           |

## Configuration Methods

### XML Configuration

In MJCF files, you can use the `<option>` tag to configure parameters:

```xml
<mujoco>
    <option timestep="0.002" gravity="0 0 -9.81" iterations="100"/>
</mujoco>
```

### Code Configuration

You can access and modify the configuration via the `options` attribute of `SceneModel`.

```{literalinclude} ../../../../../examples/options.py
:language: python
:dedent:
:start-after: "# tag::options_code[]"
:end-before:  "# end::options_code[]"
```

For a complete example, see [`examples/options.py`](../../../../../examples/options.py).

## API Reference

For more APIs related to Options, see [`Options API`]

[`Options API`]: motrixsim.Options
