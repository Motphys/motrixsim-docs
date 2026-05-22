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
Per-Instance Dynamic Texture Demo — Camera Frustum Billboard

Spawns 4 camera-frustum shaped objects, each with a per-instance dynamic
texture on the screen plane. The 4 white edges connect an apex point to
the corners of a rectangular screen.

Controls:
    1-4   - Set instance 0-3 to a random checkerboard
    SPACE - Toggle auto-cycling on/off
    B     - Batch update all instances at once

Usage:
    uv run python examples/viewer/dynamic_texture_per_instance.py
"""

import numpy as np

import motrixsim as mx
from motrixsim import run
from motrixsim.render import RenderApp

TEX_W, TEX_H = 64, 64
NUM_INSTANCES = 4

# Screen half-sizes and apex height
SW, SH = 0.5, 0.4
SZ = 0.3  # screen z position
AZ = 1.5  # apex z position
R = 0.015  # edge capsule radius

# Screen corners
BL = f"{-SW} {-SH} {SZ}"
BR = f"{SW} {-SH} {SZ}"
TR = f"{SW} {SH} {SZ}"
TL = f"{-SW} {SH} {SZ}"
APEX = f"0 0 {AZ}"

SCENE_MJCF = f"""
<mujoco>
  <asset>
    <material name="screen_mat" texture="screen_tex"/>
    <material name="edge_mat" rgba="1 1 1 1" emission="0.6 0.6 0.6 1"/>
    <texture name="screen_tex" type="2d" builtin="dynamic" width="{TEX_W}" height="{TEX_H}"
             _perinstance="true"/>
  </asset>
  <worldbody>
    <light pos="0 0 5" directional="true"/>
    <geom type="plane" size="10 10 0.1"/>

    <!-- Screen plane with dynamic texture -->
    <geom type="box" size="{SW} {SH} 0.005" pos="0 0 {SZ}"
          material="screen_mat" contype="0" conaffinity="0"/>

    <!-- 4 frustum edges: apex to each screen corner -->
    <geom type="capsule" size="{R}" fromto="{APEX} {BL}"
          material="edge_mat" contype="0" conaffinity="0"/>
    <geom type="capsule" size="{R}" fromto="{APEX} {BR}"
          material="edge_mat" contype="0" conaffinity="0"/>
    <geom type="capsule" size="{R}" fromto="{APEX} {TR}"
          material="edge_mat" contype="0" conaffinity="0"/>
    <geom type="capsule" size="{R}" fromto="{APEX} {TL}"
          material="edge_mat" contype="0" conaffinity="0"/>

    <!-- 4 border edges around the screen rectangle -->
    <geom type="capsule" size="{R}" fromto="{BL} {BR}"
          material="edge_mat" contype="0" conaffinity="0"/>
    <geom type="capsule" size="{R}" fromto="{BR} {TR}"
          material="edge_mat" contype="0" conaffinity="0"/>
    <geom type="capsule" size="{R}" fromto="{TR} {TL}"
          material="edge_mat" contype="0" conaffinity="0"/>
    <geom type="capsule" size="{R}" fromto="{TL} {BL}"
          material="edge_mat" contype="0" conaffinity="0"/>
  </worldbody>
</mujoco>
"""

INSTANCE_COLORS = [
    [255, 50, 50],  # red
    [50, 255, 50],  # green
    [50, 50, 255],  # blue
    [255, 255, 50],  # yellow
]


def make_gradient(base_color, w, h):
    """Create a gradient pattern from black to the given color."""
    pixels = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        t = y / max(h - 1, 1)
        pixels[y, :] = [int(c * t) for c in base_color]
    return pixels


def make_checkerboard(color1, color2, w, h, sq=8):
    """Create a checkerboard with two colors."""
    pixels = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            if ((x // sq) + (y // sq)) % 2 == 0:
                pixels[y, x] = color1
            else:
                pixels[y, x] = color2
    return pixels


def make_stripe(color, w, h, phase=0):
    """Create horizontal stripes that shift with phase."""
    pixels = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        if ((y + phase) // 8) % 2 == 0:
            pixels[y, :] = color
        else:
            pixels[y, :] = [30, 30, 30]
    return pixels


UPDATE_EVERY_N_FRAMES = 4


def main():
    scene = mx.msd.from_str(SCENE_MJCF)
    model = scene.build()
    data = mx.SceneData(model, batch=(NUM_INSTANCES,))

    print("=" * 55)
    print("  Camera Frustum Billboard Demo (TextureAtlas)")
    print("=" * 55)
    print(f"  {NUM_INSTANCES} frustums, each {TEX_W}x{TEX_H} texture")
    print()
    print("  Controls:")
    print("    SPACE - Toggle auto-cycling")
    print("    B     - Batch update all to random gradients")
    print("    C     - Batch update all to random checkerboards")
    print("=" * 55)

    render_offset = [[i * 2.5, 0.0, 0.0] for i in range(NUM_INSTANCES)]

    with RenderApp() as renderer:
        renderer.launch(model, batch=NUM_INSTANCES, render_offset=render_offset)

        img = renderer.get_texture_image("screen_tex")

        # Set initial colors via batch 4D update
        batch = np.zeros((NUM_INSTANCES, TEX_H, TEX_W, 3), dtype=np.uint8)
        for i, color in enumerate(INSTANCE_COLORS):
            batch[i, :, :] = color
        img.pixels = batch
        print("Initial: each frustum screen set to a solid color")

        frame = 0
        auto_cycle = True

        def phys_step():
            mx.step(model, data)

        def render_step():
            nonlocal frame, auto_cycle

            inp = renderer.input

            if inp.is_key_just_pressed("space"):
                auto_cycle = not auto_cycle
                print(f"  Auto-cycle: {'ON' if auto_cycle else 'OFF'}")

            if inp.is_key_just_pressed("b"):
                batch = np.zeros((NUM_INSTANCES, TEX_H, TEX_W, 3), dtype=np.uint8)
                for i in range(NUM_INSTANCES):
                    color = np.random.randint(50, 256, size=3).tolist()
                    batch[i] = make_gradient(color, TEX_W, TEX_H)
                img.pixels = batch
                print("  Batch update: all -> random gradients")

            if inp.is_key_just_pressed("c"):
                batch = np.zeros((NUM_INSTANCES, TEX_H, TEX_W, 3), dtype=np.uint8)
                for i in range(NUM_INSTANCES):
                    color = np.random.randint(50, 256, size=3).tolist()
                    batch[i] = make_checkerboard(color, [30, 30, 30], TEX_W, TEX_H)
                img.pixels = batch
                print("  Batch update: all -> random checkerboards")

            # Auto-cycle: animated stripes per instance (batch update)
            if auto_cycle and frame % UPDATE_EVERY_N_FRAMES == 0:
                batch = np.zeros((NUM_INSTANCES, TEX_H, TEX_W, 3), dtype=np.uint8)
                for i in range(NUM_INSTANCES):
                    phase = (frame // UPDATE_EVERY_N_FRAMES + i) % TEX_H
                    batch[i] = make_stripe(INSTANCE_COLORS[i], TEX_W, TEX_H, phase)
                img.pixels = batch

            frame += 1
            renderer.sync(data)

        run.render_loop(model.options.timestep, 60, phys_step, render_step)


if __name__ == "__main__":
    main()
