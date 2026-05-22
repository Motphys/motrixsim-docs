# 🔨 Programmatic Model Building

`motphys-scene-descriptor` (`MSD`) provides scene description and composition capabilities in MotrixSim. In Python, it is exposed through [`motrixsim.msd`](../../api_reference/msd/msd.md).

If we split the simulation workflow into two stages:

1. Scene description and assembly (mutable)
2. Physics simulation runtime (high-performance, stable)

Then `MSD` is the core tool for stage 1. It organizes, transforms, and combines MJCF/URDF/MSD assets, then builds them into a simulatable [`SceneModel`](scene_model.md).

## What Problems It Solves

In robotics and multibody workflows, common needs include:

-   Mounting different end-effectors on the same robot
-   Instancing the same model multiple times in one scene
-   Extracting a subtree from a large model and attaching it elsewhere
-   Applying translation/rotation and naming conventions before simulation

Editing raw model files repeatedly is costly and error-prone. The key value of `MSD` is to unify assets from different formats into one `World` space, then apply one programmatic pipeline:

-   Load MJCF/URDF through `msd.from_file` or `msd.from_str`
-   Convert USD to `World` through `load_usd2msd` (requires `usd2msd`)
-   Use the same `attach/transform/prefix/build` flow after unification

```{figure} /_static/images/msd/msd-unified-space.svg
:alt: MSD unified asset workflow
:width: 100%
:align: center

MSD unifies MJCF/URDF/USD assets into one programmable space.
```

## 5-Minute Quick Start

### Step 1: Load scene and model

```python
import motrixsim as mx

scene = mx.msd.from_file("examples/assets/store/scene.xml")
robot = mx.msd.from_file("examples/assets/boston_dynamics_spot/spot.xml")
```

### Step 2: Attach model into scene

```python
scene.attach(
    robot,
    other_translation=[1.0, 0.0, 0.0],
    other_prefix="spot_",
)
```

### Step 3: Build into a simulatable SceneModel

```python
model = scene.build()
data = mx.SceneData(model)
mx.step(model, data)
```

This is the most common `MSD` workflow: `load -> compose -> build -> simulate`.

### Full Example Code

```python
import motrixsim as mx

robot = mx.msd.from_file("robot.xml")
full_arm = mx.msd.from_file("arm_with_base.xml")

# Only attach the "forearm" subtree, not the entire arm model
robot.attach(
    full_arm,
    self_link_name="shoulder",
    other_link_name="forearm",  # Extract from this link
    other_prefix="arm_"
)

model = robot.build()
```

## Complete Example

Here's a complete example that creates a scene with multiple robots. For the full example, see [`examples/physics/combine_msd.py`](../../../../examples/physics/combine_msd.py).

```{literalinclude} ../../../../examples/physics/combine_msd.py
:language: python
:start-after: "# tag::combine_msd_example[]"
:end-before: "# end::combine_msd_example[]"
```

## Core Concepts

| Concept     | Description                                                                       |
| ----------- | --------------------------------------------------------------------------------- |
| `World`     | Mutable scene object in `MSD`; supports repeated `attach` and edits.              |
| `attach`    | Merge another `World` into current one with target link, pose, prefixes/suffixes. |
| `build`     | Compile `World` into an immutable `SceneModel` for simulation.                    |
| `base_path` | Base directory for resolving relative texture/mesh asset paths.                   |

## API Quick Reference

| API                                                                 | Usage                                                                 |
| ------------------------------------------------------------------- | --------------------------------------------------------------------- |
| [`msd.from_file(path)`](motrixsim.msd.from_file)                    | Load `World` from MJCF/URDF/MSD file                                  |
| [`msd.from_str(string, format, base_path)`](motrixsim.msd.from_str) | Load from model string (dynamic generation)                           |
| `motrixsim.load_usd2msd(usd_path)`                                  | Convert USD to `World` for the same composition pipeline              |
| [`World.attach(...)`](motrixsim.msd.World.attach)                   | Compose models with transforms, prefixes/suffixes, subtree extraction |
| [`World.build(base_path)`](motrixsim.msd.build)                     | Build final `SceneModel`                                              |

Full API details: [`motrixsim.msd`](../../api_reference/msd/msd.md).

## FAQ

1. Q: I already have MJCF/URDF. Do I still need to write MSD manually?  
   A: Usually no. You can directly use `msd.from_file(...).build()`. Deep MSD editing is only needed for programmatic composition/editing cases.

2. Q: Can I reuse the same attached model multiple times?  
   A: Yes. `attach` clones `other` internally, which is suitable for batch instancing.

3. Q: How do I use USD scenes?  
   A: Use the USD loading flow provided by `motrixsim` to convert into `MSD`, then build `SceneModel` (requires `usd2msd` dependency).
