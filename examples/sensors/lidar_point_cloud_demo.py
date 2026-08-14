# Copyright (C) 2020-2026 Motphys Technology Co., Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import annotations

import time

import numpy as np

from motrixsim import SceneData, msd
from motrixsim.render import Color, RenderApp, RenderSettings

ROTATING_LIDAR_BODY_NAME = "rotating_lidar_mount"
ROTATING_LIDAR_SENSOR_NAME = "rotating_lidar"
LIDAR_SITE_ORIENTATION = np.array([0.5, 0.5, 0.5, 0.5], dtype=np.float32)
ROTATING_LIDAR_BASE_Z = 0.45
ROTATING_LIDAR_Z_AMPLITUDE = 0.25
ROTATING_LIDAR_Z_FREQUENCY = 0.8
ROTATING_LIDAR_SCAN_HZ = 10.0
ROTATING_LIDAR_HSCAN = 360
ROTATING_LIDAR_HRANGE = (-180.0, 180.0)
SOLID_STATE_LIDAR_SENSOR_NAME = "solid_state_lidar"
SOLID_STATE_LIDAR_POSITION = np.array([-1.75, 0.0, 0.75], dtype=np.float32)
# Keep reusable scan profiles, mounting sites, and sensor instances in MJCF so the configuration
# can be copied directly into another model. Python below only builds the procedural debug room.
LIDAR_MJCF = """<mujoco model="lidar_point_cloud_sensors">
  <asset>
    <lidar name="rotating_16_channel" cutoff="6" pattern="rings"
      hscan="360" hrange="-180 180"
      elevations="-15 1 -13 3 -11 5 -9 7 -7 9 -5 11 -3 13 -1 15"/>
    <lidar name="solid_state_grid" cutoff="6" pattern="grid"
      hscan="64" vscan="32" hrange="-15 15" vrange="-10 10"/>
  </asset>

  <worldbody>
    <body name="rotating_lidar_mount" pos="0 0 0.45">
      <freejoint/>
      <geom name="rotating_lidar_mount_mass" type="sphere" size="0.02" mass="0.01"
        contype="0" conaffinity="0" rgba="0 1 0.2 0.35"/>
      <site name="rotating_lidar_site" quat="0.5 0.5 0.5 0.5"
        size="0.04" rgba="0 1 0.2 1"/>
    </body>
    <site name="solid_state_lidar_site" pos="-1.75 0 0.75"
      quat="0.5 0.5 0.5 0.5" size="0.04" rgba="0 0.8 1 1"/>
  </worldbody>

  <sensor>
    <!-- hz spreads one complete 360-degree scan across a 0.1-second period. -->
    <lidar name="rotating_lidar" site="rotating_lidar_site"
      asset="rotating_16_channel" exclude="parentbody" hz="10"/>
    <!-- Omitting hz fires the complete Solid State grid every physics step. -->
    <lidar name="solid_state_lidar" site="solid_state_lidar_site"
      asset="solid_state_grid" exclude="none"/>
  </sensor>
</mujoco>"""
ROOM_OBSTACLE_SEED = 20260613
ROOM_OBSTACLE_COUNT = 14
SHAPE_GALLERY_RADIUS = 1.35
HFIELD_NAME = "debug_terrain_hfield"
HFIELD_GEOM_NAME = "debug_terrain"
HFIELD_GRID_SIZE = 33
HFIELD_HALF_EXTENT = 2.4
HFIELD_HEIGHT_SCALE = 0.42
HFIELD_Z_OFFSET = -0.18
TERRAIN_GRAY = [0.46, 0.46, 0.42, 1.0]
OBJECT_GRAY = [0.56, 0.56, 0.56, 1.0]
OBJECT_GRAY_LIGHT = [0.66, 0.66, 0.66, 1.0]
OBJECT_GRAY_DARK = [0.40, 0.40, 0.40, 1.0]


def box(name: str, position: list[float], half_size: list[float], color: list[float]):
    return primitive_geom(name, msd.ShapeType.Box, position, half_size, color)


def primitive_geom(
    name: str,
    shape: msd.ShapeType,
    position: list[float],
    size: list[float],
    color: list[float],
    orientation: list[float] | None = None,
):
    geom = msd.Geometry()
    geom.name = name
    geom.shape = shape
    geom.position = position
    geom.size = size
    if orientation is not None:
        geom.orientation = orientation
    geom.visual.color = color
    return geom


def shape_gallery():
    return [
        box(
            "gallery_box",
            [SHAPE_GALLERY_RADIUS, 0.0, 0.23],
            [0.20, 0.16, 0.23],
            OBJECT_GRAY_LIGHT,
        ),
        primitive_geom(
            "gallery_sphere",
            msd.ShapeType.Sphere,
            [0.42, 1.28, 0.24],
            [0.24, 0.0, 0.0],
            OBJECT_GRAY,
        ),
        primitive_geom(
            "gallery_capsule",
            msd.ShapeType.Capsule,
            [-1.10, 0.78, 0.33],
            [0.12, 0.32, 0.0],
            OBJECT_GRAY_DARK,
            [0.0, 0.38268343, 0.0, 0.9238795],
        ),
        primitive_geom(
            "gallery_cylinder",
            msd.ShapeType.Cylinder,
            [-1.10, -0.78, 0.32],
            [0.18, 0.32, 0.0],
            OBJECT_GRAY,
        ),
        primitive_geom(
            "gallery_ellipsoid",
            msd.ShapeType.Ellipsoid,
            [0.42, -1.28, 0.28],
            [0.30, 0.16, 0.22],
            OBJECT_GRAY_LIGHT,
            [0.0, 0.0, 0.25881905, 0.9659258],
        ),
    ]


def terrain_hfield_source():
    coords = np.linspace(-1.0, 1.0, HFIELD_GRID_SIZE, dtype=np.float32)
    x, y = np.meshgrid(coords, coords)
    heights = (
        0.55 + 0.22 * np.sin(2.7 * np.pi * x) + 0.16 * np.cos(2.1 * np.pi * y) + 0.12 * np.exp(-3.5 * (x * x + y * y))
    ).astype(np.float32)

    source = msd.HFieldSource()
    source.nrow = HFIELD_GRID_SIZE
    source.ncol = HFIELD_GRID_SIZE
    source.size = [HFIELD_HALF_EXTENT, HFIELD_HALF_EXTENT]
    source.height_scale = HFIELD_HEIGHT_SCALE
    source.source_type = msd.HFieldSourceType.buffer(
        heights.reshape(-1),
        HFIELD_NAME,
    )
    return source


def terrain_hfield_geom():
    geom = msd.Geometry()
    geom.name = HFIELD_GEOM_NAME
    geom.shape = msd.ShapeType.HField
    geom.hfield = HFIELD_NAME
    geom.position = [0.0, 0.0, HFIELD_Z_OFFSET]
    geom.visual.color = TERRAIN_GRAY
    return geom


def sun_light():
    desc = msd.DirectionalLightDesc()
    desc.illuminance = 4500.0

    light = msd.Light()
    light.name = "debug_sun"
    light.type_ = msd.LightType.directional(desc)
    light.direction = [-0.45, -0.35, -0.82]
    light.color = [1.0, 0.95, 0.86]
    light.cast_shadows = True
    return light


def random_room_obstacles():
    rng = np.random.default_rng(ROOM_OBSTACLE_SEED)
    obstacles = []
    palette = [OBJECT_GRAY_DARK, OBJECT_GRAY, OBJECT_GRAY_LIGHT]

    while len(obstacles) < ROOM_OBSTACLE_COUNT:
        x = float(rng.uniform(-1.55, 1.55))
        y = float(rng.uniform(-1.55, 1.55))
        if x * x + y * y < 0.45 * 0.45:
            continue

        half_x = float(rng.uniform(0.08, 0.22))
        half_y = float(rng.uniform(0.08, 0.22))
        half_z = float(rng.uniform(0.15, 0.55))
        color = palette[len(obstacles) % len(palette)]
        obstacles.append(([x, y, half_z], [half_x, half_y, half_z], color))

    return obstacles


def build_lidar_debug_world():
    world = msd.World()
    world.name = "lidar_point_cloud_debug"
    world.statistic.center = [0.0, 0.0, 0.4]
    world.statistic.extent = [3.0, 3.0, 1.0]
    world.visual.z_far = 20.0
    world.visual.sensor.lidar_point_cloud.point_size_px = 6.0
    world.visual.sensor.lidar_point_cloud.max_color_distance = 4.0
    world.assets.hfields[HFIELD_NAME] = terrain_hfield_source()

    world.hierarchy.lights = [sun_light()]
    world.hierarchy.geoms.append(terrain_hfield_geom())
    world.hierarchy.geoms.extend(shape_gallery())

    obstacles = [
        ([2.2, 0.0, 0.6], [0.08, 2.2, 0.6], OBJECT_GRAY_DARK),
        ([0.0, 2.2, 0.6], [2.2, 0.08, 0.6], OBJECT_GRAY),
        ([0.0, -2.2, 0.6], [2.2, 0.08, 0.6], OBJECT_GRAY_LIGHT),
    ] + random_room_obstacles()
    world.hierarchy.geoms.extend(
        box(f"obstacle_{idx}", position, half_size, color) for idx, (position, half_size, color) in enumerate(obstacles)
    )

    world.attach(msd.from_str(LIDAR_MJCF))

    return world


def lidar_pose(elapsed: float) -> np.ndarray:
    z = ROTATING_LIDAR_BASE_Z + ROTATING_LIDAR_Z_AMPLITUDE * np.sin(ROTATING_LIDAR_Z_FREQUENCY * elapsed)
    return np.array(
        [0.0, 0.0, z, 0.0, 0.0, 0.0, 1.0],
        dtype=np.float32,
    )


def quat_multiply(lhs: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    lx, ly, lz, lw = lhs
    rx, ry, rz, rw = rhs
    return np.array(
        [
            lw * rx + lx * rw + ly * rz - lz * ry,
            lw * ry - lx * rz + ly * rw + lz * rx,
            lw * rz + lx * ry - ly * rx + lz * rw,
            lw * rw - lx * rx - ly * ry - lz * rz,
        ],
        dtype=np.float32,
    )


def quat_rotate(quat: np.ndarray, vec: np.ndarray) -> np.ndarray:
    q_vec = np.array([vec[0], vec[1], vec[2], 0.0], dtype=np.float32)
    q_inv = np.array([-quat[0], -quat[1], -quat[2], quat[3]], dtype=np.float32)
    return quat_multiply(quat_multiply(quat, q_vec), q_inv)[:3]


def rotating_lidar_scan_direction(sim_time: float) -> np.ndarray:
    phase = (sim_time * ROTATING_LIDAR_SCAN_HZ) % 1.0
    column = min(int(phase * ROTATING_LIDAR_HSCAN), ROTATING_LIDAR_HSCAN - 1)
    azimuth = np.deg2rad(
        ROTATING_LIDAR_HRANGE[0]
        + (ROTATING_LIDAR_HRANGE[1] - ROTATING_LIDAR_HRANGE[0]) * column / (ROTATING_LIDAR_HSCAN - 1)
    )
    local_direction = np.array([np.sin(azimuth), 0.0, np.cos(azimuth)], dtype=np.float32)
    return quat_rotate(LIDAR_SITE_ORIENTATION, local_direction)


def update_lidar_mount(floating_base, data: SceneData, pose: np.ndarray) -> None:
    floating_base.set_translation(data, pose[:3])
    floating_base.set_rotation(data, pose[3:])
    floating_base.set_global_linear_velocity(data, np.zeros(3, dtype=np.float32))
    floating_base.set_global_angular_velocity(
        data,
        np.zeros(3, dtype=np.float32),
    )


def print_lidar_stats(model, data: SceneData, sensor_name: str, origin: np.ndarray) -> None:
    values = model.get_sensor_value(sensor_name, data)
    points = values.reshape(-1, 3)
    hit_mask = np.isfinite(points).all(axis=1) & np.any(points != 0.0, axis=1)
    hits = points[hit_mask]
    distances = np.linalg.norm(hits - origin, axis=1) if hits.size else np.array([])
    hit_min = float(np.min(distances)) if distances.size else float("nan")
    hit_max = float(np.max(distances)) if distances.size else float("nan")
    print(f"{sensor_name}: shape={values.shape}, hits={hits.shape[0]}, min={hit_min:.3f}, max={hit_max:.3f}")


def main():
    model = build_lidar_debug_world().build()
    data = SceneData(model)
    lidar_body = model.get_body(ROTATING_LIDAR_BODY_NAME)
    if lidar_body is None or lidar_body.floatingbase is None:
        raise RuntimeError(f"missing free lidar body: {ROTATING_LIDAR_BODY_NAME}")
    lidar_floating_base = lidar_body.floatingbase

    render_settings = RenderSettings(
        simplify_render_mesh=True,
        enable_shadow=True,
        enable_ssao=False,
        enable_oit=False,
        share_lights_between_envs=False,
        enable_ssgi=False,
    )

    with RenderApp() as render:
        render.launch(model, render_settings=render_settings)
        render.opt.set_lidar_point_vis(True)
        print("Lidar point cloud debug scene")
        print("- Green sphere marks the moving lidar origin.")
        print("- The floor is a generated HField terrain and participates in raycast hits.")
        print("- A directional light highlights terrain slope and obstacle shadows.")
        print("- Box, sphere, capsule, cylinder, and ellipsoid primitives surround the lidar.")
        print("- Three gray box walls are raycast obstacles.")
        print("- Randomly distributed boxes fill the room interior.")
        print("- The green 360-degree Rings lidar runs at 10 Hz with 16 explicit elevations.")
        print("- Its mount only moves vertically to demonstrate scan-motion distortion.")
        print("- The yellow arrow shows its current azimuth phase; the site axes stay fixed.")
        print("- The cyan fixed lidar uses a 60 x 20 degree solid-state Grid snapshot.")
        print("- Press ESC or close the window to exit.")

        step = 0
        start_time = time.monotonic()
        while not render.is_closed:
            pose = lidar_pose(time.monotonic() - start_time)
            update_lidar_mount(lidar_floating_base, data, pose)
            model.step(data)
            if step % 30 == 0:
                print_lidar_stats(model, data, ROTATING_LIDAR_SENSOR_NAME, pose[:3])
                print_lidar_stats(
                    model,
                    data,
                    SOLID_STATE_LIDAR_SENSOR_NAME,
                    SOLID_STATE_LIDAR_POSITION,
                )

            render.gizmos.draw_sphere(
                0.05,
                pose[:3],
                color=Color.rgb(0.0, 1.0, 0.2),
            )
            render.gizmos.draw_axes(pose[:3], LIDAR_SITE_ORIENTATION, 0.35)
            scan_direction = rotating_lidar_scan_direction((step + 1) * model.options.timestep)
            ray_end = pose[:3] + 0.6 * scan_direction
            render.gizmos.draw_arrow(
                pose[:3],
                ray_end,
                color=Color.rgb(1.0, 1.0, 0.0),
            )
            render.gizmos.draw_sphere(
                0.05,
                SOLID_STATE_LIDAR_POSITION,
                color=Color.rgb(0.0, 0.8, 1.0),
            )
            render.gizmos.draw_axes(
                SOLID_STATE_LIDAR_POSITION,
                LIDAR_SITE_ORIENTATION,
                0.35,
            )
            solid_state_ray_end = SOLID_STATE_LIDAR_POSITION + quat_rotate(
                LIDAR_SITE_ORIENTATION,
                np.array([0.0, 0.0, 0.6], dtype=np.float32),
            )
            render.gizmos.draw_arrow(
                SOLID_STATE_LIDAR_POSITION,
                solid_state_ray_end,
                color=Color.rgb(0.0, 0.8, 1.0),
            )
            render.sync(data)
            step += 1
            time.sleep(1.0 / 60.0)


if __name__ == "__main__":
    main()
