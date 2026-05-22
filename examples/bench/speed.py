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

"""Speed benchmark comparing motrixsim and MuJoCo.

Supports single-env mode (default) and batch mode (--num_envs).
In batch mode, multiple environments are stepped in parallel per step call.
"""

import importlib.util
import os
import time
from pathlib import Path
from typing import Callable

import numpy as np
from absl import app, flags

from motrixsim import SceneData, load_model, step

_HAS_MUJOCO = importlib.util.find_spec("mujoco") is not None

_File = flags.DEFINE_string("file", None, "path to model file (omit to run all default models)")
_NumSteps = flags.DEFINE_integer("steps", 3000, "number of simulation steps to run", lower_bound=1)
_Warmup = flags.DEFINE_integer("warmup", 100, "number of warmup steps", lower_bound=0)
_Rounds = flags.DEFINE_integer("rounds", 1, "number of rounds to repeat per engine", lower_bound=1)
_Engine = flags.DEFINE_string("engine", "all", "engine to benchmark: mujoco, motrixsim, or all")
_NumEnvs = flags.DEFINE_integer("num_envs", 0, "number of parallel environments (0 = single-env mode)", lower_bound=0)
_MaxIterations = flags.DEFINE_integer(
    "max_iterations",
    None,
    "override each engine's main constraint solver iteration limit; omit to use the model default",
    lower_bound=1,
)

_DEFAULT_MODELS = [
    ("go1", "go1/scene.xml"),
    ("go2", "go2/scene_flat.xml"),
    ("spot", "boston_dynamics_spot/scene.xml"),
    ("panda", "franka_emika_panda/scene.xml"),
]


def _bench_mujoco(model_path: str, num_steps: int, warmup: int) -> tuple[float, float, float]:
    import mujoco  # noqa: F811

    model = mujoco.MjModel.from_xml_path(str(Path(model_path).resolve()))
    if _MaxIterations.value is not None:
        model.opt.iterations = _MaxIterations.value
    data = mujoco.MjData(model)

    for _ in range(warmup):
        mujoco.mj_step(model, data)

    data = mujoco.MjData(model)
    t0 = time.monotonic()
    for _ in range(num_steps):
        mujoco.mj_step(model, data)
    elapsed = time.monotonic() - t0

    return elapsed, num_steps / elapsed, elapsed / num_steps * 1000


def _bench_motrixsim(model_path: str, num_steps: int, warmup: int) -> tuple[float, float, float]:
    model = load_model(model_path)
    if _MaxIterations.value is not None:
        model.options.max_iterations = _MaxIterations.value
    data = SceneData(model)

    for _ in range(warmup):
        step(model, data)

    data = SceneData(model)
    t0 = time.monotonic()
    for _ in range(num_steps):
        step(model, data)
    elapsed = time.monotonic() - t0

    return elapsed, num_steps / elapsed, elapsed / num_steps * 1000


def _bench_mujoco_batch(model_path: str, num_steps: int, warmup: int, num_envs: int) -> tuple[float, float, float]:
    import mujoco
    import mujoco.rollout

    model = mujoco.MjModel.from_xml_path(str(Path(model_path).resolve()))
    if _MaxIterations.value is not None:
        model.opt.iterations = _MaxIterations.value
    nstate = mujoco.mj_stateSize(model, mujoco.mjtState.mjSTATE_FULLPHYSICS)
    nu = model.nu
    n_threads = min(num_envs, os.cpu_count() or 1)

    worker_data = [mujoco.MjData(model) for _ in range(n_threads)]
    runner = mujoco.rollout.Rollout(nthread=n_threads)

    initial_data = mujoco.MjData(model)
    mujoco.mj_forward(model, initial_data)
    state0 = np.empty(nstate, dtype=np.float64)
    mujoco.mj_getState(model, initial_data, state0, mujoco.mjtState.mjSTATE_FULLPHYSICS)
    physics_state = np.tile(state0, (num_envs, 1))
    ctrl = np.zeros((num_envs, 1, nu))

    for _ in range(warmup):
        state_traj, _ = runner.rollout(model, worker_data, initial_state=physics_state, control=ctrl, nstep=1)
        physics_state[:] = state_traj[:, -1, :]

    t0 = time.monotonic()
    for _ in range(num_steps):
        state_traj, _ = runner.rollout(model, worker_data, initial_state=physics_state, control=ctrl, nstep=1)
        physics_state[:] = state_traj[:, -1, :]
    elapsed = time.monotonic() - t0

    total = num_envs * num_steps
    return elapsed, total / elapsed, elapsed / num_steps * 1000


def _bench_motrixsim_batch(model_path: str, num_steps: int, warmup: int, num_envs: int) -> tuple[float, float, float]:
    model = load_model(model_path)
    if _MaxIterations.value is not None:
        model.options.max_iterations = _MaxIterations.value
    data = SceneData(model, batch=(num_envs,))

    for _ in range(warmup):
        model.step(data)

    data = SceneData(model, batch=(num_envs,))
    t0 = time.monotonic()
    for _ in range(num_steps):
        model.step(data)
    elapsed = time.monotonic() - t0

    total = num_envs * num_steps
    return elapsed, total / elapsed, elapsed / num_steps * 1000


def _resolve_engines(engine_choice: str, batch: bool = False) -> list[tuple[str, Callable]]:
    engines: list[tuple[str, Callable]] = []
    if engine_choice in ("all", "motrixsim"):
        engines.append(("motrixsim", _bench_motrixsim_batch if batch else _bench_motrixsim))
    if engine_choice in ("all", "mujoco"):
        if not _HAS_MUJOCO:
            print("Warning: mujoco is not installed, skipping.")
        else:
            engines.append(("mujoco", _bench_mujoco_batch if batch else _bench_mujoco))
    return engines


def _run_benchmark(
    name: str,
    model_path: str,
    engines: list[tuple[str, Callable]],
    num_steps: int,
    warmup: int,
    rounds: int,
    num_envs: int = 0,
) -> dict[str, tuple[float, float, float]]:
    print(f"[{name}] {model_path}")
    print()

    results: dict[str, list[tuple[float, float, float]]] = {}

    for engine_name, bench_fn in engines:
        engine_results = []
        for i in range(rounds):
            label = f"{engine_name}" + (f" (round {i + 1}/{rounds})" if rounds > 1 else "")
            print(f"  [{label}]")

            if num_envs > 0:
                elapsed, throughput, avg_step = bench_fn(model_path, num_steps, warmup, num_envs)
            else:
                elapsed, throughput, avg_step = bench_fn(model_path, num_steps, warmup)
            engine_results.append((elapsed, throughput, avg_step))

            print(f"    Elapsed time:  {elapsed:.3f} s")
            if num_envs > 0:
                print(f"    Throughput:    {throughput:.3f} env-steps/s ({num_envs} envs)")
            else:
                print(f"    Throughput:    {throughput:.3f} steps/s")
            print(f"    Avg per step:  {avg_step:.3f} ms")
            print()

        results[engine_name] = engine_results

    # Per-model summary
    avg: dict[str, tuple[float, float, float]] = {}
    for ename, rounds_data in results.items():
        n = len(rounds_data)
        e = sum(r[0] for r in rounds_data) / n
        t = sum(r[1] for r in rounds_data) / n
        a = sum(r[2] for r in rounds_data) / n
        avg[ename] = (e, t, a)

    mj_t = avg.get("mujoco", (0, 0, 0))[1]
    mx_t = avg.get("motrixsim", (0, 0, 0))[1]
    if mj_t > 0 and mx_t > 0:
        ratio = mx_t / mj_t
        tag = "faster" if ratio > 1 else "slower"
        print(f"  motrixsim / mujoco: {ratio:.3f}x ({tag})")
        print()

    return avg


def main(argv):
    num_steps = _NumSteps.value
    warmup = _Warmup.value
    rounds = _Rounds.value
    engine_choice = _Engine.value
    num_envs = _NumEnvs.value

    batch_mode = num_envs > 0
    engines = _resolve_engines(engine_choice, batch=batch_mode)
    if not engines:
        return

    if _File.value is not None:
        models = [("model", _File.value)]
    else:
        assets_dir = Path(__file__).parent.parent / "assets"
        models = [(name, str(assets_dir / path)) for name, path in _DEFAULT_MODELS]

    print("=" * 60)
    print("Speed Benchmark" + (" (batch mode)" if batch_mode else ""))
    print(f"  Steps:   {num_steps}")
    print(f"  Warmup:  {warmup}")
    print(f"  Rounds:  {rounds}")
    if batch_mode:
        print(f"  Envs:    {num_envs}")
    if _MaxIterations.value is not None:
        print(f"  Max iters: {_MaxIterations.value}")
    print(f"  Engines: {', '.join(name for name, _ in engines)}")
    print(f"  Models:  {', '.join(name for name, _ in models)}")
    print("=" * 60)
    print()

    all_results: dict[str, dict[str, tuple[float, float, float]]] = {}
    for name, path in models:
        all_results[name] = _run_benchmark(name, path, engines, num_steps, warmup, rounds, num_envs)

    # Final summary table
    if len(all_results) > 1:
        print("=" * 60)
        unit = "env-steps/s" if batch_mode else "steps/s"
        print(f"Final Summary (avg throughput, {unit})")
        print("=" * 60)
        print()

        engine_names = [name for name, _ in engines]
        header = f"{'Model':<12}" + "".join(f"{e:<18}" for e in engine_names)
        if len(engine_names) == 2:
            header += f"{'Ratio':<12}"
        print(header)
        print("-" * len(header))

        for model_name, avg in all_results.items():
            row = f"{model_name:<12}"
            for ename in engine_names:
                t = avg.get(ename, (0, 0, 0))[1]
                row += f"{t:<18.3f}"
            if len(engine_names) == 2:
                mj_t = avg.get("mujoco", (0, 0, 0))[1]
                mx_t = avg.get("motrixsim", (0, 0, 0))[1]
                if mj_t > 0 and mx_t > 0:
                    row += f"{mx_t / mj_t:<12.3f}"
                else:
                    row += f"{'N/A':<12}"
            print(row)
        print()


if __name__ == "__main__":
    app.run(main)
