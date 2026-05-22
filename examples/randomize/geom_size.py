# Copyright (C) 2020-2025 Motphys Technology Co., Ltd. All Rights Reserved.
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


"""
Geom Size Randomization — Multi-Shape Size Override

This example demonstrates per-instance geom size override by randomizing
the collision and primitive visual sizes of a sphere, a capsule, a box,
a cylinder, and an ellipsoid falling onto a floor.

Physical intuition:
- Five objects (sphere, capsule, box, cylinder, ellipsoid) fall under gravity.
- The objects are spaced apart so the example highlights floor contact rather
  than object-object contact.
- Each of the 16 batch instances has randomly scaled collision sizes.
- Larger collision shapes touch the floor sooner and settle higher.
- Primitive visual sizes follow the size override, so you can inspect the
  randomized geometry directly and observe different settling heights across
  instances.

Key concepts:
- Per-geom size override using typed subclass APIs:
  ``GeomSphere.set_size_override``, ``GeomCapsule.set_size_override``,
  ``GeomCuboid.set_size_override``, ``GeomCylinder.set_size_override``,
  ``GeomEllipsoid.set_size_override``
- Batch simulation to compare multiple sizes simultaneously

Mouse controls:
- Press and hold left button then drag to rotate the camera/view
- Press and hold right button then drag to pan/translate the view
"""

import numpy as np

from motrixsim import (
    GeomCapsule,
    GeomCuboid,
    GeomCylinder,
    GeomEllipsoid,
    GeomSphere,
    SceneData,
    load_mjcf_str,
)
from motrixsim.render import RenderApp

MJCF = """
<mujoco>
  <option timestep="0.02" solver="PGS"/>
  <worldbody>
    <light pos="0 0 6" dir="-1 -1 -1" directional="true"/>
    <geom name="floor" type="plane" size="0 0 0.01"
          rgba="0.3 0.3 0.3 1" contype="1" conaffinity="0" priority="1"/>

    <body name="sphere_body" pos="-2 -2 3">
      <freejoint/>
      <geom name="sphere" type="sphere" size="0.3" rgba="0.2 0.6 1.0 1"/>
    </body>

    <body name="capsule_body" pos="2 -2 3">
      <freejoint/>
      <geom name="capsule" type="capsule" size="0.2 0.3" rgba="0.8 0.3 1.0 1"/>
    </body>

    <body name="box_body" pos="0 0 3">
      <freejoint/>
      <geom name="box" type="box" size="0.25 0.25 0.25" rgba="1.0 0.4 0.2 1"/>
    </body>

    <body name="cyl_body" pos="-2 2 3">
      <freejoint/>
      <geom name="cyl" type="cylinder" size="0.2 0.3" rgba="0.3 0.9 0.3 1"/>
    </body>

    <body name="ellipsoid_body" pos="2 2 3">
      <freejoint/>
      <geom name="ellipsoid" type="ellipsoid" size="0.25 0.35 0.2" rgba="1.0 0.8 0.2 1"/>
    </body>
  </worldbody>
</mujoco>
"""

BATCH = 16


def main():
    with RenderApp() as render:
        model = load_mjcf_str(MJCF)

        # 4x4 grid layout
        render_offset = []
        for i in range(4):
            for j in range(4):
                render_offset.append([-i * 9.0, j * 9.0, 0])

        render.launch(model, batch=BATCH, render_offset=render_offset)
        render.system_camera.set_view(lookat=[-13.5, 13.5, 0.5], distance=40.0, elevation=-35, azimuth=90)
        data = SceneData(model, batch=(BATCH,))

        rng = np.random.default_rng(42)

        # --- Sphere: randomize radius ---
        sphere_geom = model.get_geom("sphere")
        assert isinstance(sphere_geom, GeomSphere)
        sphere_radii = rng.uniform(0.1, 0.8, size=(BATCH, 1)).astype(np.float32)
        sphere_geom.set_size_override(data, sphere_radii)

        # --- Capsule: randomize [radius, half_height] ---
        capsule_geom = model.get_geom("capsule")
        assert isinstance(capsule_geom, GeomCapsule)
        capsule_sizes = np.column_stack(
            [
                rng.uniform(0.1, 0.5, size=BATCH),
                rng.uniform(0.1, 0.6, size=BATCH),
            ]
        ).astype(np.float32)
        capsule_geom.set_size_override(data, capsule_sizes)

        # --- Box: randomize half-extents ---
        box_geom = model.get_geom("box")
        assert isinstance(box_geom, GeomCuboid)
        box_sizes = rng.uniform(0.1, 0.6, size=(BATCH, 3)).astype(np.float32)
        box_geom.set_size_override(data, box_sizes)

        # --- Cylinder: randomize [radius, half_height] ---
        cyl_geom = model.get_geom("cyl")
        assert isinstance(cyl_geom, GeomCylinder)
        cyl_sizes = np.column_stack(
            [
                rng.uniform(0.1, 0.5, size=BATCH),
                rng.uniform(0.1, 0.6, size=BATCH),
            ]
        ).astype(np.float32)
        cyl_geom.set_size_override(data, cyl_sizes)

        # --- Ellipsoid: randomize half-extents ---
        ellipsoid_geom = model.get_geom("ellipsoid")
        assert isinstance(ellipsoid_geom, GeomEllipsoid)
        ellipsoid_sizes = rng.uniform(0.1, 0.6, size=(BATCH, 3)).astype(np.float32)
        ellipsoid_geom.set_size_override(data, ellipsoid_sizes)

        # Print summary
        print("\n" + "=" * 65)
        print("Geom Size Override — Multi-Shape")
        print("=" * 65)
        for i in range(BATCH):
            r = sphere_radii[i, 0]
            cap = capsule_sizes[i]
            b = box_sizes[i]
            c = cyl_sizes[i]
            e = ellipsoid_sizes[i]
            print(
                f"  Instance {i:2d}:  sphere r={r:.2f}"
                f"  cap r={cap[0]:.2f} hh={cap[1]:.2f}"
                f"  box=[{b[0]:.2f},{b[1]:.2f},{b[2]:.2f}]"
                f"  cyl r={c[0]:.2f} hh={c[1]:.2f}"
                f"  ell=[{e[0]:.2f},{e[1]:.2f},{e[2]:.2f}]"
            )
        print("=" * 65 + "\n")

        while True:
            model.step(data)
            render.sync(data)


if __name__ == "__main__":
    main()
