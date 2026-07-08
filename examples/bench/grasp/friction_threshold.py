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

"""Critical-friction slip test from a grasp hold state.

Usage:
    uv run examples/bench/grasp/friction_threshold.py
    uv run examples/bench/grasp/friction_threshold.py --mu_factors=0.95,1.0,1.05
    uv run examples/bench/grasp/friction_threshold.py --normal_force=0.25
"""

import pathlib
from dataclasses import dataclass

import mujoco
import numpy as np
import pandas as pd
from absl import app, flags
from common import (
    INIT_QPOS,
    LEFT_CONTACT_SENSOR,
    LIFT_QPOS,
    MUJOCO_CONTACT_SLOT_SIZE,
    RIGHT_CONTACT_SENSOR,
    SETTLING_END_TIME,
    aggregate_contacts,
    compute_ctrl_for_time,
    parse_motrixsim_contact_sensor,
    parse_mujoco_contact_sensor,
)

from motrixsim import SceneData, load_model, step

_Engines = flags.DEFINE_list(
    "engines",
    ["motrixsim", "mujoco", "mujoco_fastimplicit"],
    "Engines to run: motrixsim,mujoco,mujoco_fastimplicit.",
)
_MuFactors = flags.DEFINE_list(
    "mu_factors",
    ["0.90", "0.98", "1.00", "1.02", "1.10"],
    "Comma-separated multipliers around each engine's critical friction.",
)
_NormalForce = flags.DEFINE_float(
    "normal_force",
    None,
    "Optional total normal force in newtons. If omitted, estimate it from warm-up contact sensors.",
)
_WarmupHoldDuration = flags.DEFINE_float(
    "warmup_hold_duration",
    0.6,
    "Extra hold time after settling used to initialize the hold state and estimate normal force.",
)
_NormalSampleWindow = flags.DEFINE_float(
    "normal_sample_window",
    0.2,
    "Tail window of the warm-up hold phase used for average normal-force estimation.",
)
_TestDuration = flags.DEFINE_float("test_duration", 5.0, "Duration of each fixed-hold slip test in seconds.")
_DropDelta = flags.DEFINE_float("drop_delta", 0.005, "Relative z drop threshold in meters.")
_DropZ = flags.DEFINE_float("drop_z", 0.03, "Absolute object z threshold in meters.")

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[3]
_OBJECT_NAME = "cube"
_MOTRIXSIM_ENGINE = "motrixsim"
_MUJOCO_ENGINE = "mujoco"
_MUJOCO_FASTIMPLICIT_ENGINE = "mujoco_fastimplicit"
_VALID_ENGINES = (_MOTRIXSIM_ENGINE, _MUJOCO_ENGINE, _MUJOCO_FASTIMPLICIT_ENGINE)
_CONTACT_LINK_NAMES = ("left_finger", "right_finger", "obj")


@dataclass
class HoldState:
    qpos: np.ndarray
    qvel: np.ndarray
    start_z: float
    normal_force: float
    gravity_force: float
    object_mass: float
    dt: float


def _scene_path():
    return _PROJECT_ROOT / "examples" / "assets" / "franka_emika_panda" / f"scene_pick_{_OBJECT_NAME}.xml"


def _parse_requested_engines() -> list[str]:
    engines = [engine.strip().lower() for engine in _Engines.value if engine.strip()]
    if not engines:
        raise app.UsageError("--engines must contain at least one engine")
    invalid = [engine for engine in engines if engine not in _VALID_ENGINES]
    if invalid:
        raise app.UsageError(f"Unsupported engines: {', '.join(invalid)}")
    return engines


def _parse_mu_factors() -> list[float]:
    factors = [float(value) for value in _MuFactors.value if value.strip()]
    if not factors:
        raise app.UsageError("--mu_factors must contain at least one value")
    if any(factor <= 0.0 for factor in factors):
        raise app.UsageError("--mu_factors values must be positive")
    return factors


def _set_motrixsim_contact_friction(model, data, slide_mu: float):
    updated = 0
    for link_name in _CONTACT_LINK_NAMES:
        link = model.get_link(link_name)
        if link is None:
            raise RuntimeError(f"MotrixSim link not found: {link_name}")
        for geom in link.geoms:
            friction = np.asarray(geom.get_friction_override(data), dtype=np.float32).copy()
            friction[0] = slide_mu
            geom.set_friction_override(data, friction)
            updated += 1
    if updated == 0:
        raise RuntimeError("No MotrixSim contact geoms were updated")


def _set_mujoco_contact_friction(model, slide_mu: float):
    updated = 0
    for body_name in _CONTACT_LINK_NAMES:
        body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, body_name)
        if body_id < 0:
            raise RuntimeError(f"MuJoCo body not found: {body_name}")
        start = model.body_geomadr[body_id]
        end = start + model.body_geomnum[body_id]
        for geom_id in range(start, end):
            model.geom_friction[geom_id, 0] = slide_mu
            updated += 1
    if updated == 0:
        raise RuntimeError("No MuJoCo contact geoms were updated")


def _set_motrixsim_hold_ctrl(model, data):
    start = model.get_actuator_index("actuator1")
    for i, val in enumerate(LIFT_QPOS[:7]):
        model.get_actuator(start + i).set_ctrl(data, val)
    model.get_actuator(model.get_actuator_index("actuator8")).set_ctrl(data, LIFT_QPOS[7])


def _set_motrixsim_initial_ctrl(model, data):
    start = model.get_actuator_index("actuator1")
    for i, val in enumerate(INIT_QPOS[:7]):
        model.get_actuator(start + i).set_ctrl(data, val)
    model.get_actuator(model.get_actuator_index("actuator8")).set_ctrl(data, INIT_QPOS[7])


def _set_mujoco_hold_ctrl(model, data):
    for i, val in enumerate(LIFT_QPOS[:7], start=1):
        data.ctrl[mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, f"actuator{i}")] = val
    data.ctrl[mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, "actuator8")] = LIFT_QPOS[7]


def _mujoco_sensor_layout(model, sensor_name: str):
    sensor_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SENSOR, sensor_name)
    adr = model.sensor_adr[sensor_id]
    dim = model.sensor_dim[sensor_id]
    return adr, dim, dim // MUJOCO_CONTACT_SLOT_SIZE


def _aggregate_normal_force(left_contacts, right_contacts) -> float:
    left = aggregate_contacts(left_contacts)
    right = aggregate_contacts(right_contacts)
    return float(left["total_normal_force"] + right["total_normal_force"])


def _estimate_normal_force(samples: list[float]) -> float:
    valid = np.asarray([value for value in samples if value > 1e-8], dtype=float)
    if valid.size == 0:
        raise RuntimeError("No valid normal-force samples collected during hold warm-up")
    return float(np.mean(valid))


def _warmup_motrixsim(scene_path: pathlib.Path) -> HoldState:
    model = load_model(str(scene_path))
    data = SceneData(model)
    dt = float(model.options.timestep)
    total_duration = SETTLING_END_TIME + _WarmupHoldDuration.value
    sample_start = max(SETTLING_END_TIME, total_duration - _NormalSampleWindow.value)

    panda = model.get_body(model.get_body_index("link0"))
    panda.set_dof_pos(data, INIT_QPOS)
    obj = model.get_body("obj")
    _set_motrixsim_initial_ctrl(model, data)

    samples = []
    step_cnt = 0
    while step_cnt * dt < total_duration:
        sim_time = step_cnt * dt
        arm, gripper = compute_ctrl_for_time(sim_time, False)
        if arm is not None:
            start = model.get_actuator_index("actuator1")
            for i, val in enumerate(arm):
                model.get_actuator(start + i).set_ctrl(data, val)
        if gripper is not None:
            model.get_actuator(model.get_actuator_index("actuator8")).set_ctrl(data, gripper)

        step(model, data)
        if sim_time >= sample_start:
            left = parse_motrixsim_contact_sensor(model.get_sensor_value(LEFT_CONTACT_SENSOR, data))
            right = parse_motrixsim_contact_sensor(model.get_sensor_value(RIGHT_CONTACT_SENSOR, data))
            samples.append(_aggregate_normal_force(left, right))
        step_cnt += 1

    qpos = np.asarray(data.low.dof_positions, dtype=np.float32).copy()
    qvel = np.zeros_like(np.asarray(data.low.dof_velocities, dtype=np.float32))
    obj_mass = float(obj.base_link.mass)
    gravity_force = float(obj_mass * np.linalg.norm(model.options.gravity))
    normal_force = _NormalForce.value if _NormalForce.value is not None else _estimate_normal_force(samples)
    return HoldState(qpos, qvel, float(obj.get_pose(data)[2]), normal_force, gravity_force, obj_mass, dt)


def _warmup_mujoco(scene_path: pathlib.Path, integrator=None) -> HoldState:
    model = mujoco.MjModel.from_xml_path(str(scene_path))
    if integrator is not None:
        model.opt.integrator = integrator
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, model.key("home").id)

    dt = float(model.opt.timestep)
    total_duration = SETTLING_END_TIME + _WarmupHoldDuration.value
    sample_start = max(SETTLING_END_TIME, total_duration - _NormalSampleWindow.value)
    obj_body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "obj")
    left_adr, left_dim, left_slots = _mujoco_sensor_layout(model, LEFT_CONTACT_SENSOR)
    right_adr, right_dim, right_slots = _mujoco_sensor_layout(model, RIGHT_CONTACT_SENSOR)

    samples = []
    step_cnt = 0
    while step_cnt * dt < total_duration:
        sim_time = step_cnt * dt
        arm, gripper = compute_ctrl_for_time(sim_time, False)
        if arm is not None:
            for i, val in enumerate(arm, start=1):
                data.ctrl[mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, f"actuator{i}")] = val
        if gripper is not None:
            data.ctrl[mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, "actuator8")] = gripper

        mujoco.mj_step(model, data)
        if sim_time >= sample_start:
            left_raw = data.sensordata[left_adr : left_adr + left_dim]
            right_raw = data.sensordata[right_adr : right_adr + right_dim]
            left = parse_mujoco_contact_sensor(left_raw, left_slots)
            right = parse_mujoco_contact_sensor(right_raw, right_slots)
            samples.append(_aggregate_normal_force(left, right))
        step_cnt += 1

    obj_mass = float(model.body_mass[obj_body_id])
    gravity_force = float(obj_mass * np.linalg.norm(model.opt.gravity))
    normal_force = _NormalForce.value if _NormalForce.value is not None else _estimate_normal_force(samples)
    return HoldState(
        np.asarray(data.qpos, dtype=np.float64).copy(),
        np.zeros_like(np.asarray(data.qvel, dtype=np.float64)),
        float(data.xpos[obj_body_id][2]),
        normal_force,
        gravity_force,
        obj_mass,
        dt,
    )


def _run_motrixsim_case(scene_path: pathlib.Path, hold_state: HoldState, slide_mu: float):
    model = load_model(str(scene_path))
    data = SceneData(model)
    _set_motrixsim_contact_friction(model, data, slide_mu)
    data.low.set_dof_positions_unchecked(hold_state.qpos)
    data.low.dof_velocities = hold_state.qvel
    model.forward_kinematic(data)

    obj = model.get_body("obj")
    _set_motrixsim_hold_ctrl(model, data)

    start_z = float(obj.get_pose(data)[2])
    min_z = start_z
    final_z = start_z
    drop_time = None
    step_cnt = 0
    while step_cnt * hold_state.dt < _TestDuration.value:
        sim_time = step_cnt * hold_state.dt
        _set_motrixsim_hold_ctrl(model, data)
        step(model, data)
        final_z = float(obj.get_pose(data)[2])
        min_z = min(min_z, final_z)
        if drop_time is None and _is_dropped(start_z, final_z):
            drop_time = sim_time
        step_cnt += 1
    return start_z, final_z, min_z, drop_time


def _run_mujoco_case(scene_path: pathlib.Path, hold_state: HoldState, slide_mu: float, integrator=None):
    model = mujoco.MjModel.from_xml_path(str(scene_path))
    if integrator is not None:
        model.opt.integrator = integrator
    _set_mujoco_contact_friction(model, slide_mu)
    data = mujoco.MjData(model)
    data.qpos[:] = hold_state.qpos
    data.qvel[:] = hold_state.qvel
    _set_mujoco_hold_ctrl(model, data)
    mujoco.mj_forward(model, data)

    obj_body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "obj")
    start_z = float(data.xpos[obj_body_id][2])
    min_z = start_z
    final_z = start_z
    drop_time = None
    step_cnt = 0
    while step_cnt * hold_state.dt < _TestDuration.value:
        sim_time = step_cnt * hold_state.dt
        _set_mujoco_hold_ctrl(model, data)
        mujoco.mj_step(model, data)
        final_z = float(data.xpos[obj_body_id][2])
        min_z = min(min_z, final_z)
        if drop_time is None and _is_dropped(start_z, final_z):
            drop_time = sim_time
        step_cnt += 1
    return start_z, final_z, min_z, drop_time


def _is_dropped(start_z: float, current_z: float) -> bool:
    return current_z < _DropZ.value or (start_z - current_z) > _DropDelta.value


def _make_row(engine, factor, hold_state: HoldState, start_z, final_z, min_z, drop_time):
    mu_critical = hold_state.gravity_force / hold_state.normal_force
    slide_mu = mu_critical * factor
    return dict(
        engine=engine,
        factor=factor,
        mu=slide_mu,
        start_z=start_z,
        final_z=final_z,
        min_z=min_z,
        drop_mm=(start_z - min_z) * 1000.0,
        held=drop_time is None,
        drop_time=drop_time,
    )


def _make_preamble_row(engine, hold_state: HoldState):
    return dict(
        engine=engine,
        mu_critical=hold_state.gravity_force / hold_state.normal_force,
        normal_force=hold_state.normal_force,
        gravity_force=hold_state.gravity_force,
        object_mass=hold_state.object_mass,
        dt=hold_state.dt,
    )


def _format_table(rows, columns) -> str:
    lines = []
    header = " ".join(title.ljust(width) for _, title, width in columns)
    lines.append(header)
    lines.append("-" * len(header))
    for row in rows:
        values = []
        for key, _, width in columns:
            value = row[key]
            if key == "held":
                text = "YES" if bool(value) else "NO"
            elif key == "drop_time" and pd.isna(value):
                text = "-"
            elif key == "drop_time":
                text = f"{float(value):.4f}"
            elif key == "drop_mm":
                text = f"{float(value):.3f}"
            elif key in {"factor", "mu", "mu_critical", "normal_force", "gravity_force", "object_mass", "dt"}:
                text = f"{float(value):.4f}"
            elif key in {"start_z", "final_z"}:
                text = f"{float(value):.4f}"
            else:
                text = str(value)
            values.append(text.ljust(width))
        lines.append(" ".join(values))
    return "\n".join(lines)


def _field_descriptions() -> str:
    return "\n".join(
        [
            "Field meanings",
            "- Engine: physics engine and solver variant used by the case.",
            "- MuCrit: theoretical sliding-friction coefficient needed to hold the object, computed as mg / N.",
            "- N(N): average total normal gripping force from the warm-up hold state, in newtons.",
            "- mg(N): object weight, in newtons.",
            "- Mass(kg): object mass.",
            "- dt(s): simulation timestep.",
            "- Factor: multiplier applied to MuCrit for this case.",
            "- Mu: actual sliding-friction coefficient used in this case, equal to MuCrit * Factor.",
            "- StartZ: object height at the beginning of the fixed-hold slip test, in meters.",
            "- FinalZ: object height at the end of the fixed-hold slip test, in meters.",
            "- Drop(mm): maximum downward displacement during the test, in millimeters.",
            "- Held: YES means the object never crossed the configured drop thresholds.",
            "- DropTime: first time when the object crossed a drop threshold; '-' means no drop was detected.",
        ]
    )


def _build_report(preamble_df: pd.DataFrame, result_df: pd.DataFrame) -> str:
    preamble_columns = [
        ("engine", "Engine", 20),
        ("mu_critical", "MuCrit", 9),
        ("normal_force", "N(N)", 9),
        ("gravity_force", "mg(N)", 9),
        ("object_mass", "Mass(kg)", 10),
        ("dt", "dt(s)", 9),
    ]
    columns = [
        ("engine", "Engine", 20),
        ("factor", "Factor", 8),
        ("mu", "Mu", 9),
        ("start_z", "StartZ", 9),
        ("final_z", "FinalZ", 9),
        ("drop_mm", "Drop(mm)", 10),
        ("held", "Held", 6),
        ("drop_time", "DropTime", 9),
    ]

    return "\n\n".join(
        [
            _field_descriptions(),
            "Critical friction preamble",
            _format_table(preamble_df.to_dict("records"), preamble_columns),
            "Critical friction slip test",
            _format_table(result_df.to_dict("records"), columns),
        ]
    )


def _print_report(report: str):
    print()
    print(report)


def main(argv):
    del argv
    scene_path = _scene_path()
    factors = _parse_mu_factors()
    preamble_rows = []
    rows = []

    for engine in _parse_requested_engines():
        if engine == _MOTRIXSIM_ENGINE:
            hold_state = _warmup_motrixsim(scene_path)
            preamble_rows.append(_make_preamble_row(engine, hold_state))
            for factor in factors:
                mu = (hold_state.gravity_force / hold_state.normal_force) * factor
                start_z, final_z, min_z, drop_time = _run_motrixsim_case(scene_path, hold_state, mu)
                rows.append(_make_row(engine, factor, hold_state, start_z, final_z, min_z, drop_time))
        elif engine == _MUJOCO_ENGINE:
            hold_state = _warmup_mujoco(scene_path)
            preamble_rows.append(_make_preamble_row(engine, hold_state))
            for factor in factors:
                mu = (hold_state.gravity_force / hold_state.normal_force) * factor
                start_z, final_z, min_z, drop_time = _run_mujoco_case(scene_path, hold_state, mu)
                rows.append(_make_row(engine, factor, hold_state, start_z, final_z, min_z, drop_time))
        elif engine == _MUJOCO_FASTIMPLICIT_ENGINE:
            integrator = mujoco.mjtIntegrator.mjINT_IMPLICITFAST
            hold_state = _warmup_mujoco(scene_path, integrator=integrator)
            preamble_rows.append(_make_preamble_row(engine, hold_state))
            for factor in factors:
                mu = (hold_state.gravity_force / hold_state.normal_force) * factor
                start_z, final_z, min_z, drop_time = _run_mujoco_case(
                    scene_path,
                    hold_state,
                    mu,
                    integrator=integrator,
                )
                rows.append(_make_row(engine, factor, hold_state, start_z, final_z, min_z, drop_time))

    preamble_df = pd.DataFrame(preamble_rows)
    result_df = pd.DataFrame(rows)
    report = _build_report(preamble_df, result_df)
    _print_report(report)


if __name__ == "__main__":
    app.run(main)
