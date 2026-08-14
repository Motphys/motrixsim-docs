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

"""Benchmark end-to-end lidar raycast throughput in the playground scene."""

from __future__ import annotations

import argparse
import os
import statistics
import time
from dataclasses import dataclass
from pathlib import Path

from motrixsim import SceneData, msd

DEFAULT_SCENE = Path(__file__).resolve().parents[1] / "assets" / "ssgi" / "ssgi_playground.xml"
LIDAR_SENSOR_PREFIX = "benchmark_lidar"
TARGET_RAYCASTS_PER_ROUND = 1024 * 64 * 100
MAX_AUTO_STEPS = 100


@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    label: str
    num_lidars: int
    num_envs: int


BENCHMARK_CASES = {
    "single": BenchmarkCase("single", "1 environment x 1 lidar", num_lidars=1, num_envs=1),
    "multi-lidar": BenchmarkCase(
        "multi-lidar",
        "1 environment x 128 lidars",
        num_lidars=128,
        num_envs=1,
    ),
    "multi-env": BenchmarkCase(
        "multi-env",
        "1024 environments x 1 lidar",
        num_lidars=1,
        num_envs=1024,
    ),
}


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return parsed


def nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must not be negative")
    return parsed


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0.0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return parsed


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        choices=(*BENCHMARK_CASES, "all"),
        default="single",
        help="benchmark scale case",
    )
    parser.add_argument(
        "--scene",
        type=Path,
        default=DEFAULT_SCENE,
        help="playground MJCF path",
    )
    parser.add_argument("--hscan", type=positive_int, default=1024, help="horizontal beams per scan")
    parser.add_argument("--vscan", type=positive_int, default=64, help="vertical beams per scan")
    parser.add_argument("--cutoff", type=positive_float, default=25.0, help="maximum ray distance in meters")
    parser.add_argument(
        "--warmup",
        type=nonnegative_int,
        help="untimed physics steps per round (default: min(10, timed steps))",
    )
    parser.add_argument(
        "--steps",
        type=positive_int,
        help="timed physics steps per round (default: auto-scaled by total raycasts)",
    )
    parser.add_argument("--rounds", type=positive_int, default=3, help="number of benchmark rounds")
    return parser


def lidar_sensor_name(index: int) -> str:
    return f"{LIDAR_SENSOR_PREFIX}_{index}"


def build_model(scene_path: Path, hscan: int, vscan: int, cutoff: float, num_lidars: int):
    scene_path = scene_path.resolve()
    if not scene_path.is_file():
        raise FileNotFoundError(f"scene does not exist: {scene_path}")

    scene = msd.from_file(scene_path)
    sites = "\n".join(
        f'      <site name="benchmark_lidar_site_{index}" quat="0.5 0.5 0.5 0.5" size="0.01" />'
        for index in range(num_lidars)
    )
    sensors = "\n".join(
        f'    <lidar name="{lidar_sensor_name(index)}" site="benchmark_lidar_site_{index}" '
        'asset="benchmark_lidar_profile" exclude="parentbody" />'
        for index in range(num_lidars)
    )
    lidar_mjcf = f"""<mujoco model="lidar_benchmark_mount">
  <asset>
    <lidar name="benchmark_lidar_profile" cutoff="{cutoff:g}" pattern="grid"
      hscan="{hscan}" vscan="{vscan}" hrange="-180 180" vrange="-15 15" />
  </asset>
  <worldbody>
    <body name="benchmark_lidar_mount" pos="0 0 1">
{sites}
    </body>
  </worldbody>
  <sensor>
{sensors}
  </sensor>
</mujoco>"""
    scene.attach(msd.from_str(lidar_mjcf))
    return scene.build()


def make_scene_data(model, num_envs: int) -> SceneData:
    if num_envs == 1:
        return SceneData(model)
    return SceneData(model, batch=(num_envs,))


def run_round(
    model,
    warmup: int,
    steps: int,
    benchmark_case: BenchmarkCase,
    raycasts_per_lidar: int,
    validate: bool,
) -> float:
    data = make_scene_data(model, benchmark_case.num_envs)
    for _ in range(warmup):
        model.step(data)
    if validate:
        validate_lidars(model, data, benchmark_case, raycasts_per_lidar)

    start = time.perf_counter()
    for _ in range(steps):
        model.step(data)
    return time.perf_counter() - start


def validate_lidars(model, data: SceneData, benchmark_case: BenchmarkCase, raycasts_per_lidar: int) -> None:
    expected_values = benchmark_case.num_envs * raycasts_per_lidar * 3
    for lidar_index in range(benchmark_case.num_lidars):
        values = model.get_sensor_value(lidar_sensor_name(lidar_index), data)
        if values.size != expected_values:
            raise RuntimeError(
                f"lidar {lidar_index} output has {values.size} values; expected {expected_values} "
                f"for {benchmark_case.num_envs * raycasts_per_lidar} point-return raycasts"
            )


def selected_cases(case_name: str) -> list[BenchmarkCase]:
    if case_name == "all":
        return list(BENCHMARK_CASES.values())
    return [BENCHMARK_CASES[case_name]]


def auto_steps(raycasts_per_step: int) -> int:
    return min(MAX_AUTO_STEPS, max(1, TARGET_RAYCASTS_PER_ROUND // raycasts_per_step))


def run_case(args: argparse.Namespace, benchmark_case: BenchmarkCase) -> None:
    model = build_model(
        args.scene,
        args.hscan,
        args.vscan,
        args.cutoff,
        benchmark_case.num_lidars,
    )
    raycasts_per_lidar = args.hscan * args.vscan
    raycasts_per_step = raycasts_per_lidar * benchmark_case.num_lidars * benchmark_case.num_envs
    steps = args.steps or auto_steps(raycasts_per_step)
    warmup = args.warmup if args.warmup is not None else min(10, steps)
    total_raycasts = raycasts_per_step * steps

    print("=" * 78)
    print(f"Case:               {benchmark_case.name} ({benchmark_case.label})")
    print(f"  Scene:             {args.scene.resolve()}")
    print(f"  Grid/lidar:        {args.hscan} x {args.vscan}")
    print(f"  Lidars/model:      {benchmark_case.num_lidars}")
    print(f"  Environments:      {benchmark_case.num_envs}")
    print(f"  Raycasts/step:     {raycasts_per_step:,}")
    print(f"  Timed steps/round: {steps:,}")
    print(f"  Warmup steps:      {warmup:,}")
    print(f"  Rounds:            {args.rounds}")
    print(f"  Logical CPUs:      {os.cpu_count() or 'unknown'}")
    print(f"  RAYON_NUM_THREADS: {os.environ.get('RAYON_NUM_THREADS', 'auto')}")
    print()

    elapsed_rounds = []
    for round_index in range(args.rounds):
        elapsed = run_round(
            model,
            warmup,
            steps,
            benchmark_case,
            raycasts_per_lidar,
            validate=round_index == 0,
        )
        elapsed_rounds.append(elapsed)
        raycast_throughput = total_raycasts / elapsed
        environment_step_throughput = steps * benchmark_case.num_envs / elapsed
        print(
            f"Round {round_index + 1}: {raycast_throughput / 1e6:,.3f} Mraycast/s, "
            f"{environment_step_throughput:,.3f} env-step/s, "
            f"{elapsed / steps * 1e3:,.3f} wall ms/step ({elapsed:.3f} s)"
        )

    median_elapsed = statistics.median(elapsed_rounds)
    print()
    print("Median")
    print(f"  Throughput: {total_raycasts / median_elapsed / 1e6:,.3f} Mraycast/s")
    print(f"  Env rate:   {steps * benchmark_case.num_envs / median_elapsed:,.3f} env-step/s")
    print(f"  Step time:  {median_elapsed / steps * 1e3:,.3f} wall ms/step")
    print()


def main() -> None:
    args = create_argument_parser().parse_args()
    print("Lidar Raycast Benchmark")
    print()
    for benchmark_case in selected_cases(args.case):
        run_case(args, benchmark_case)


if __name__ == "__main__":
    main()
