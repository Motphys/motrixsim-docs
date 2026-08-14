# Lidar Sensor

MotrixSim Lidar is a multi-beam ranging sensor that performs batched raycasts against physics
collision geometry. A site defines its mounting pose, and the sensor publishes a world-frame point
cloud for obstacle avoidance, terrain perception, localization and mapping, and reinforcement
learning observations.

```{video} /_static/videos/lidar_sensor.mp4
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

The colored lines and points show real-time Lidar hits on the floor, walls, spheres, capsules, and
obstacles around the robot. Point-cloud visualization is display-only and does not participate in
sensor computation.

## Quick Start

A Lidar consists of three parts:

1. `body/site` defines the mounting frame;
2. `asset/lidar` defines a reusable model and scan geometry;
3. `sensor/lidar` attaches a sensor instance to the site and references the profile.

The following configuration creates a 1024×64, 360-degree Grid Lidar. Omitting `hz` produces one
complete static snapshot per physics step.

```xml
<mujoco model="lidar_example">
  <asset>
    <lidar name="grid_64"
      cutoff="25"
      pattern="grid"
      hscan="1024" vscan="64"
      hrange="-180 180" vrange="-15 15"/>
  </asset>

  <worldbody>
    <body name="robot">
      <site name="lidar_site"
        pos="0.25 0 0.20"
        quat="0.5 0.5 0.5 0.5"
        size="0.01"/>
    </body>
  </worldbody>

  <sensor>
    <lidar name="roof_lidar"
      site="lidar_site"
      asset="grid_64"
      exclude="parentsubtree"/>
  </sensor>
</mujoco>
```

Each `step()` advances the Lidar. `get_sensor_value()` returns a flattened point buffer; the stable
Grid layout is `(hscan, vscan, 3)`.

```python
import numpy as np

from motrixsim import SceneData, load_model

HSCAN = 1024
VSCAN = 64

model = load_model("lidar_scene.xml")
data = SceneData(model)

model.step(data)
values = model.get_sensor_value("roof_lidar", data)
points = values.reshape(HSCAN, VSCAN, 3)

# A point that missed is (0, 0, 0).
hit_mask = np.any(points != 0.0, axis=-1)
hit_points = points[hit_mask]
print(f"hits: {hit_points.shape[0]}")
```

## MJCF Parameter Overview

Model and scan parameters belong to `asset/lidar`; instance identity, mounting, and runtime scan
frequency belong to `sensor/lidar`. Do not put profile parameters on a sensor instance.

### `asset/lidar`

| Attribute    | Applies to  | Default / constraint                                                | Description                                           |
| ------------ | ----------- | ------------------------------------------------------------------- | ----------------------------------------------------- |
| `name`       | All         | Required and globally unique                                        | Profile name referenced by `sensor/lidar.asset`       |
| `cutoff`     | All         | Default `100`; positive and finite                                  | Maximum range in meters                               |
| `pattern`    | All         | Default `grid`; `grid` / `rings`                                    | Scan geometry type                                    |
| `hscan`      | Grid, Rings | Default `1`; positive integer; mutually exclusive with `reportrate` | Horizontal columns in one complete scan               |
| `vscan`      | Grid        | Default `1`; positive integer                                       | Vertical beams in each column                         |
| `hrange`     | Grid, Rings | Default `0 0`; two finite values                                    | Horizontal start and end angles in degrees            |
| `vrange`     | Grid        | Default `0 0`; two finite values                                    | Vertical start and end angles in degrees              |
| `elevations` | Rings       | Non-empty array                                                     | Per-ring elevation table in degrees                   |
| `reportrate` | Grid, Rings | Optional, positive and finite; requires sensor `hz`                 | Horizontal columns per second, used to derive `hscan` |
| `hzrange`    | Grid, Rings | Optional; two positive, non-decreasing values                       | Supported inclusive complete-scan frequency range     |

Grid uses `vscan`/`vrange`, while Rings uses `elevations`; these pattern-specific attributes cannot
be mixed.

### `sensor/lidar`

| Attribute | Default / constraint                                | Description                                                               |
| --------- | --------------------------------------------------- | ------------------------------------------------------------------------- |
| `name`    | Optional                                            | Sensor name passed to `get_sensor_value()`                                |
| `asset`   | Required                                            | References one `asset/lidar.name`                                         |
| `site`    | Required                                            | Site defining ray origins and the local frame                             |
| `exclude` | Default `parentbody`                                | `none` / `parentbody` / `parentsubtree` self-filter policy                |
| `hz`      | Optional, positive and finite; `1 / hz >= timestep` | Omit for a complete snapshot every step; set to enable in-frame spreading |

If the profile defines `hzrange`, the sensor's `hz` must fall inside that closed range.

## Coordinate Frame and Output Layout

Lidar uses the site's local frame:

-   `+Z`: forward;
-   `+X`: right;
-   `+Y`: up;
-   `hrange`: horizontal scan range around the up axis, in degrees;
-   `vrange` / `elevations`: elevation relative to the horizontal plane, in degrees.

Both Grid and Rings are ordered with horizontal angle first, so their outputs have stable reshape
layouts:

| Pattern | Point-cloud shape             | No-hit value | Frame |
| ------- | ----------------------------- | ------------ | ----- |
| Grid    | `(hscan, vscan, 3)`           | `(0, 0, 0)`  | World |
| Rings   | `(hscan, len(elevations), 3)` | `(0, 0, 0)`  | World |

Batched data adds batch dimensions in front. Do not apply a distance sensor's `-1` no-hit rule to
high-level Lidar: Lidar always publishes points, and a missed point is the zero vector.

## Scan Patterns

### Grid

Grid samples horizontal and vertical angles uniformly. It is useful for solid-state approximations,
depth perception, and quick scene setup.

| Attribute | Meaning                         |
| --------- | ------------------------------- |
| `hscan`   | Horizontal columns in one frame |
| `vscan`   | Vertical beams in each column   |
| `hrange`  | Horizontal start and end angles |
| `vrange`  | Vertical start and end angles   |
| `cutoff`  | Maximum range in meters         |

### Rings

Rings uses an explicit elevation table per channel. It fits rotating Lidars such as Velodyne and
Ouster whose vertical beams are not uniformly spaced.

```xml
<asset>
  <lidar name="rings_8"
    cutoff="100"
    pattern="rings"
    elevations="-15 1 -13 3 -11 5 -9 7"
    hscan="1800"
    hrange="-180 180"/>
</asset>
```

Pattern-specific attributes cannot be mixed: Rings uses `elevations`, not `vscan` or `vrange`. See
the complete {ref}`MJCF asset/lidar reference <asset-lidar>`.

## Static Snapshots and `hz`

`sensor/lidar.hz` controls scan timing:

-   **Omit `hz`**: emit the complete pattern every physics step using one site pose. This produces
    distortion-free static snapshots and is suitable for RL tasks that require a complete
    observation every step.
-   **Set `hz="10"`**: spread one frame over `0.1s` and emit only the current phase's beams in each
    physics step. Hits use each step's site pose and accumulate in world coordinates. The completed
    frame is published at the end of the period, so a moving carrier exhibits realistic scan-motion
    distortion.

```xml
<sensor>
  <lidar name="roof_lidar"
    site="lidar_site"
    asset="rotating_profile"
    hz="10"
    exclude="parentsubtree"/>
</sensor>
```

The configuration must satisfy `1 / hz >= physics timestep`. For a profile that uses `reportrate`,
the model builder derives the actual horizontal resolution as
`hscan = round(reportrate / hz)`.

## Self-Filtering

`exclude` prevents the Lidar from scanning its own mount or robot:

| Value           | Behavior                                                                        |
| --------------- | ------------------------------------------------------------------------------- |
| `none`          | Do not exclude any self collider                                                |
| `parentbody`    | Exclude the site's parent body; this is the default                             |
| `parentsubtree` | Exclude the parent body and all descendants; recommended for articulated robots |

Lidar hits physics colliders, not visual-only geoms. Changing rendering materials does not change
range measurements.

## Using Bundled Real-Model Profiles

The `examples/assets/lidar-profiles/` directory provides starter profiles for HESAI XT32 and Ouster
OS0/OS1/OS2. Include its entry-point
[`catalog.xml`](../../../../../examples/assets/lidar-profiles/catalog.xml) in MJCF and reference a
profile by name:

```xml
<include file="lidar-profiles/catalog.xml"/>

<sensor>
  <lidar name="roof_lidar"
    site="lidar_site"
    asset="hesai_xt32_sd10"
    hz="10"
    exclude="parentsubtree"/>
</sensor>
```

Include paths are resolved relative to the current MJCF file. See
[`robot_locomotion.py`](../../../../../examples/control/robot_locomotion.py) for a complete mounting
example.

## Point-Cloud Visualization

The renderer does not stream Lidar point clouds by default. Enable it explicitly for debugging with
`set_lidar_point_vis(True)`:

```python
from motrixsim.render import RenderApp

with RenderApp() as render:
    render.launch(model)
    render.opt.set_lidar_point_vis(True)

    while not render.is_closed:
        model.step(data)
        render.sync(data)
```

See [`lidar_point_cloud_demo.py`](../../../../../examples/sensors/lidar_point_cloud_demo.py) for the
complete programmatic scene and visualization code. The example shows a 60° × 20° Solid State-style
static Grid alongside a 360°, 10 Hz rotating Rings Lidar with an explicit 16-channel elevation
table and in-frame spreading. Both Lidars use inline MJCF configuration; the latter's mount moves
to demonstrate scan-motion distortion.

## Performance Reference

The following end-to-end Python benchmark uses the playground scene. Each Lidar uses a 1024×64 Grid
and omits `hz`, so it emits 65,536 rays per step. The test calls `model.step()` one step at a time and
excludes model loading, building, and rendering. It ran with 32 logical CPUs and automatic Rayon
thread selection; values are medians of three rounds.

```{figure} /_static/images/lidar_raycast_benchmark.svg
:alt: Raycast throughput bar chart for three Lidar scale cases
:width: 100%

End-to-end Lidar raycast throughput
```

| Case                             | Total rays/step | Median throughput | Wall time/step |
| -------------------------------- | --------------: | ----------------: | -------------: |
| 1 environment × 1 Lidar          |          65,536 | 63.495 Mraycast/s |       1.032 ms |
| 1 environment × 128 Lidars       |       8,388,608 | 78.324 Mraycast/s |     107.102 ms |
| 1024 environments × 1 Lidar each |      67,108,864 | 80.656 Mraycast/s |     832.036 ms |

Throughput is calculated as:

```text
total rays = hscan × vscan × lidars × environments × timed steps
throughput = total rays / wall-clock time
```

`80.656 Mraycast/s` means an aggregate throughput of about 80.656 million raycasts per second across
all environments. The measurement includes the complete physics pipeline seen by a user calling
`step()`; it is not an isolated raycast-kernel peak.

Reproduce the benchmark with:

```bash
cd motrixsim-python/motrixsim-docs
uv run python examples/bench/lidar.py --case all
```
