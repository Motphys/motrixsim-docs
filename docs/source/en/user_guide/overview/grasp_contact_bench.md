# Grasp Contact Mechanics Benchmark

:::{tip}
For models and code, see the [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) repository.

Before running the examples, please refer to {doc}`../overview/environment_setup` to complete the environment setup.
:::

In robot simulation, "grasping" seems simple — the gripper closes, the object is held, the arm lifts. But for policy training and sim-to-real transfer, **merely holding the object is far from enough**. Whether the contact forces are smooth and physically consistent directly affects whether trained policies can transfer to real robots.

This page presents two quantitative experiments that evaluate MotrixSim and MuJoCo's contact mechanics during grasping tasks:

-   **Experiment 1 (Contact Force Analysis)**: Records contact force data step-by-step throughout a complete grasp-lift-hold sequence, comparing force balance and force smoothness across engines.
-   **Experiment 2 (Critical Friction Slip Test)**: Validates whether each engine's friction model obeys Coulomb's friction law — when the friction coefficient reaches the theoretical critical value, the object should be just barely held.

## Experiment Setup

Both experiments share the same scene: a **Franka Emika Panda** robotic arm with a parallel-jaw gripper, grasping a cube placed on a table.

![franka_grasp](/_static/images/grasp_bench/franka_grasp.png)

The grasp sequence is divided into the following phases:

| Phase           | Action                                               | Duration     |
| --------------- | ---------------------------------------------------- | ------------ |
| `move_to_lift`  | Arm moves from initial pose to lift-ready position   | 1.0s         |
| `move_to_grasp` | Arm moves from lift position to grasp position       | 1.0s         |
| `close_gripper` | Gripper closes, establishing contact with the object | 1.0s         |
| `lift`          | Arm returns to lift pose, lifting the object         | 1.0s         |
| `settling`      | Transition and stabilization after lifting           | 0.4s         |
| `hold`          | Steady-state holding                                 | Configurable |

All engines use **identical** scene files, control trajectories, timesteps, and sensor configurations, ensuring that observed differences come solely from the engine's contact solving and friction modeling.

---

## Experiment 1: Contact Force Analysis

**Script**: [`force_analy.py`](../../../../examples/bench/grasp/force_analy.py)

### Goal

Run MotrixSim, MuJoCo (Euler), and MuJoCo (FastImplicit) under identical conditions and compare two dimensions:

1. **Force balance**: Does the vertical friction force accurately match the object's weight?
2. **Force smoothness**: Does the contact force change gradually between timesteps?

### Physics Background

When a gripper horizontally clamps an object and lifts it, the normal forces (horizontal clamping forces) from the left and right fingers cancel each other out. What actually supports the object is the **vertical friction force** — it must equal the object's weight $mg$ for the object to remain stationary.

An ideal physics engine should output during the `hold` (steady-state) phase:

$$
F_z \approx mg
$$

where $F_z$ is the total vertical friction force, $m$ is the object mass, and $g$ is gravitational acceleration.

### Results

Running the script generates analysis plots in `examples/bench/grasp/.result/`.

#### Force Balance

![force_balance](/_static/images/grasp_bench/force_balance.png)

The top panel shows vertical friction force $F_z$ over time during the `lift`, `settling`, and `hold` phases. The black dashed line marks the theoretical gravity value $mg$. The bottom panel uses a bar chart to compare the mean force error $|F_z - mg|$ across engines during the `hold` phase.

**Conclusion**: MotrixSim's vertical friction force closely tracks the $mg$ line with minimal error. MuJoCo exhibits noticeable periodic oscillations, with the Euler integrator showing larger fluctuations.

#### Force Smoothness

![force_smoothness](/_static/images/grasp_bench/force_smoothness.png)

Force smoothness measures the magnitude of contact force changes between adjacent timesteps. Specifically, the step-to-step difference of the vertical friction force is computed as $\Delta F_z(k) = F_z(t_{k+1}) - F_z(t_k)$, and the standard deviation of all differences during the `hold` phase is used as the **Jitter** metric — lower Jitter means smoother forces. The plot shows Jitter for both vertical friction force ($\Delta F_z$) and normal clamping force ($\Delta F_n$).

**Conclusion**: MuJoCo Euler's Jitter is several orders of magnitude higher than MotrixSim and MuJoCo FastImplicit, indicating significant high-frequency numerical oscillations in its contact forces. Both MotrixSim and MuJoCo FastImplicit have Jitter at an extremely small scale (near numerical precision limits), with virtually no observable step-to-step force fluctuation during the `hold` phase — their contact response is very smooth.

### How to Run

```bash
uv run examples/bench/grasp/force_analy.py
```

After execution, plots are saved to `examples/bench/grasp/.result/`.

---

## Experiment 2: Critical Friction Slip Test

**Script**: [`friction_threshold.py`](../../../../examples/bench/grasp/friction_threshold.py)

### Goal

Validate whether each engine's friction model correctly obeys **Coulomb's friction law** — specifically, whether the hold/slip behavior around the theoretical critical friction coefficient matches physical predictions.

### Physics Principle

![friction_principle](/_static/images/grasp_bench/friction_principle.svg)

Imagine holding a block horizontally between two fingers and lifting it. The fingers provide a normal force (clamping force) $N$, and the friction coefficient is $\mu$. According to Coulomb's friction law, the maximum static friction force is:

$$
f_{\max} = \mu \times N
$$

To support the block, friction must be greater than or equal to its weight:

$$
\mu \times N \geq mg
$$

This gives the **critical friction coefficient**:

$$
\mu_{\text{crit}} = \frac{mg}{N}
$$

-   When $\mu < \mu_{\text{crit}}$: friction is insufficient, and the object should slip
-   When $\mu \geq \mu_{\text{crit}}$: friction is sufficient, and the object should remain held

A physically correct simulator should show a **clear hold/slip boundary** at $\mu_{\text{crit}}$.

### Method

1. **Warm-up phase**: Complete a normal grasp and lift to reach a stable hold state; record the gripper normal force $N$
2. **Compute critical value**: Calculate $\mu_{\text{crit}} = mg / N$ from the object mass and normal force
3. **Parameter sweep**: Test 5 multipliers around $\mu_{\text{crit}}$ (0.90, 0.98, 1.00, 1.02, 1.10), modifying the friction coefficient for each
4. **Observe results**: Simulate 5 seconds from the hold state and observe whether the object slips

### Results

The following table shows results for all three engines at different friction coefficient multipliers:

| Engine              | Factor   | Actual $\mu$ | Predicted | Actual      | Drop (mm) | Matches Theory |
| ------------------- | -------- | ------------ | --------- | ----------- | --------: | :------------: |
| **MotrixSim**       | 0.90     | 0.0812       | Slip      | Slipped     |     154.2 |       ✅       |
| **MotrixSim**       | 0.98     | 0.0884       | Slip      | Slipped     |     150.0 |       ✅       |
| **MotrixSim**       | **1.00** | **0.0902**   | **Hold**  | **Held**    |   **0.0** |       ✅       |
| **MotrixSim**       | 1.02     | 0.0920       | Hold      | Held        |       0.0 |       ✅       |
| **MotrixSim**       | 1.10     | 0.0992       | Hold      | Held        |       0.0 |       ✅       |
| MuJoCo Euler        | 0.90     | 0.0812       | Slip      | Slipped     |     153.5 |       ✅       |
| MuJoCo Euler        | 0.98     | 0.0884       | Slip      | Slipped     |     153.2 |       ✅       |
| MuJoCo Euler        | **1.00** | **0.0902**   | **Hold**  | **Slipped** | **151.2** |       ❌       |
| MuJoCo Euler        | 1.02     | 0.0920       | Hold      | Slipped     |     152.0 |       ❌       |
| MuJoCo Euler        | 1.10     | 0.0992       | Hold      | Slipped     |     150.5 |       ❌       |
| MuJoCo FastImplicit | 0.90     | 0.0812       | Slip      | Slipped     |     152.5 |       ✅       |
| MuJoCo FastImplicit | 0.98     | 0.0884       | Slip      | Slipped     |     150.9 |       ✅       |
| MuJoCo FastImplicit | **1.00** | **0.0902**   | **Hold**  | **Slipped** | **151.7** |       ❌       |
| MuJoCo FastImplicit | 1.02     | 0.0920       | Hold      | Slipped     |     149.7 |       ❌       |
| MuJoCo FastImplicit | 1.10     | 0.0992       | Hold      | Slipped     |      11.3 |       ❌       |

:::{note}
The normal force $N$ and object weight $mg$ are nearly identical across engines ($N \approx 6.96$ N, $mg \approx 0.628$ N), so $\mu_{\text{crit}} \approx 0.0902$ is the same for all three.
:::

### Analysis

**MotrixSim** matches physical predictions exactly:

-   $\mu < \mu_{\text{crit}}$ (factors 0.90, 0.98): object slips
-   $\mu = \mu_{\text{crit}}$ (factor 1.00): object is just barely held
-   $\mu > \mu_{\text{crit}}$ (factors 1.02, 1.10): object is stably held

The boundary falls precisely at the theoretical critical value $\mu_{\text{crit}}$, demonstrating that MotrixSim's friction model strictly obeys Coulomb's friction law.

**MuJoCo Euler** deviates from physical predictions: even at 1.10x the critical friction coefficient, the object still slips. This indicates a systematic deficiency in MuJoCo's Euler integrator for maintaining friction constraints in this scenario.

**MuJoCo FastImplicit** shows some improvement but remains imprecise: at the highest multiplier (1.10), the object does not fully drop but still slips noticeably (11.3 mm), and all cases are classified as slipped.

### How to Run

```bash
uv run examples/bench/grasp/friction_threshold.py
```

---

## Summary

The two experiments validate MotrixSim's contact mechanics advantages from complementary perspectives:

| Dimension                | Experiment 1 (Contact Force Analysis)                         | Experiment 2 (Critical Friction Test)                          |
| ------------------------ | ------------------------------------------------------------- | -------------------------------------------------------------- |
| **Force accuracy**       | Vertical friction precisely matches gravity $mg$              | Hold/slip boundary at critical friction matches theory exactly |
| **Force smoothness**     | Minimal step-to-step variation, no high-frequency oscillation | —                                                              |
| **Friction consistency** | —                                                             | Strictly obeys Coulomb's friction law                          |

These advantages have practical implications for:

-   **Dexterous manipulation and precision assembly**: Policy training relies on low-noise, physically consistent contact force feedback
-   **Sim-to-real transfer**: The closer simulated contact behavior is to physical laws, the higher the success rate when transferring policies to real robots
-   **Grasp benchmarking**: Research that needs to distinguish between "barely holding" and "stably held" requires high-quality contact force data
