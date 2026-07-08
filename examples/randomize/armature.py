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


"""
Rotating Arm Armature Randomization Experiment

This example demonstrates how armature (virtual rotor inertia) affects the
oscillation frequency of a torsion-spring-driven rotating arm.

Physical intuition:
- Armature adds virtual rotational inertia to a joint, modelling the reflected
  inertia of a motor rotor through a gearbox.
- The arm rotates around a vertical axis (hinge joint) with a torsion spring.
  Gravity is parallel to the hinge axis and creates no torque, so the spring
  alone governs the motion.
- Natural frequency: omega = sqrt(k / (I_body + armature))
- Higher armature -> greater effective rotational inertia -> lower frequency
  -> arm sweeps more slowly.

Parameter derivation for spring_rotor.xml:

  Body inertia (hub + arm + tip, density=1000 kg/m³):
    I_hub  = 0.5 × 1.539 × 0.07²            = 0.004 kg·m²
    I_arm  = 1.810 × (0.030² + 0.30²)  ≈    = 0.224 kg·m²  (parallel-axis)
    I_tip  = 0.905 × (2/5 × 0.06² + 0.60²)  = 0.327 kg·m²
    I_body = 0.555 kg·m²

  Stiffness (target T₀ ≈ 3.0 s at armature → 0, visually comfortable):
    k = I_body × (2π / T₀)²  = 0.555 × (2π / 2.96)²  ≈ 2.5 N·m/rad
    tip peak velocity = (π/2) × sqrt(k/I_eff_min) × 0.6 m ≈ 0.93 m/s  (comfortable)

  Damping (target: fastest instance shows ≥ 5 visible oscillations):
    amplitude decay per cycle = e^(-c·T / (2·I_eff))
    for 5 cycles to amplitude e^(-1): c = 2·I_eff_min / (5·T_min)
                                         = 2 × 0.684 / (5 × 3.0)  ≈ 0.091
    → use c = 0.1 N·m·s/rad  (~5 cycles clearly visible before fading)

  Armature range (quadratic spacing for uniform period gradient):
    T ∝ sqrt(I_eff)  →  linear linspace in armature bunches most change
    at the low end.  Instead choose T_min..T_max linearly, then invert:
      armature = k × (T / 2π)²  −  I_body
    T range 3.0 s → 9.0 s  gives armature 0.13 → 4.67 kg·m²,
    each ΔT = 0.40 s step → same perceptual speed change per instance.

Physics summary:
- armature = 0.13 kg·m²  -> T ≈ 3.0 s  (fast sweep)
- armature = 1.8  kg·m²  -> T ≈ 5.6 s  (moderate)
- armature = 4.67 kg·m²  -> T ≈ 9.0 s  (slow, 3× longer than fastest)

Key concepts:
- Armature randomization across a hinge joint
- Effect on natural oscillation frequency of a torsional spring-mass system
- Batch simulation to compare multiple instances side-by-side

Mouse controls:
- Press and hold left button then drag to rotate the camera/view
- Press and hold right button then drag to pan/translate the view
"""

import numpy as np

from motrixsim import SceneData, load_model
from motrixsim.render import RenderApp

# Physics constants matching spring_rotor.xml
# stiffness k =  2.5 N·m/rad  (derived: k = I_body × (2π/T₀)², T₀=2.96 s)
# damping  c =  0.1 N·m·s/rad (derived: ~5 visible cycles on fastest instance)
# I_body   ≈  0.555 kg·m²    (hub + arm + tip, density=1000 kg/m³)
_K_TORSION = 2.5
_I_BODY = 0.555


def _armature_for_period(period: np.ndarray) -> np.ndarray:
    """Return armature values (kg·m²) that produce the given oscillation periods.

    Inverts T = 2π × sqrt((I_body + armature) / k).
    """
    return _K_TORSION * (period / (2 * np.pi)) ** 2 - _I_BODY


def main():
    # Create render window for visualization
    with RenderApp() as render:
        # The scene description file
        path = "examples/assets/randomize/spring_rotor.xml"
        # Load the scene model
        model = load_model(path)

        # Create 16 instances in a 4x4 grid
        render_offset = []
        for i in range(4):
            for j in range(4):
                render_offset.append([-i * 2, j * 2, 0])

        # Create the render instance of the model
        render.launch(model, batch=16, render_offset=render_offset)
        render.system_camera.set_view(lookat=[-3, 3, 0.3], distance=8.0, elevation=-35, azimuth=90)

        # Create the physics data of the model
        data = SceneData(model, batch=(16,))

        # Get the rotor hinge joint by name
        joint = model.get_joint("rotor_joint")

        # Generate armature values for linearly-spaced oscillation periods.
        #
        # Using linear armature spacing (linspace) would concentrate most of the
        # visual effect in the first few instances because T ∝ sqrt(I_eff).
        # Instead, we choose evenly-spaced target periods and invert the formula:
        #   armature = k × (T / 2π)² − I_body
        #
        # T range: 3.0 s  (armature ≈ 0.13 kg·m², near-zero virtual inertia)
        #          9.0 s  (armature ≈ 4.67 kg·m², ~8× body inertia)
        # Each step advances the period by ΔT ≈ 0.40 s → uniform visual gradient.
        T_min = 3.0  # seconds
        T_max = 9.0  # seconds
        periods = np.linspace(T_min, T_max, 16)
        armature = _armature_for_period(periods).astype(np.float32)

        joint.set_armature_override(data, armature)

        # Verify the override was applied correctly
        armature_get = joint.get_armature_override(data)
        assert np.allclose(armature_get, armature)

        # Print summary table
        print("\n" + "=" * 70)
        print("Armature Randomization Summary")
        print("=" * 70)
        for i in range(16):
            val = armature_get[i]
            # Thresholds derived from period boundaries:
            #   armature < 0.8  -> T < ~4.5 s  (fast)
            #   armature < 2.8  -> T < ~7.0 s  (moderate)
            #   armature >= 2.8 -> T >= ~7.0 s  (slow)
            if val < 0.8:
                behavior = "Fast oscillation"
            elif val < 2.8:
                behavior = "Moderate oscillation"
            else:
                behavior = "Slow oscillation"
            t = 2 * np.pi * np.sqrt((_I_BODY + val) / _K_TORSION)
            print(f"Instance {i:2d}: armature = {val:.3f} kg·m²  T ≈ {t:.2f} s  -> {behavior}")
        print("=" * 70 + "\n")

        while True:
            model.step(data)
            render.sync(data)


if __name__ == "__main__":
    main()
