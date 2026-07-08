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
Unified grasp contact force analysis for MotrixSim and MuJoCo.

Usage:
    uv run examples/bench/grasp/force_analy.py
    uv run examples/bench/grasp/force_analy.py --hold_duration=20
    uv run examples/bench/grasp/force_analy.py --engines=motrixsim,mujoco_fastimplicit
"""

import pathlib

import mujoco
import numpy as np
import pandas as pd
from absl import app, flags
from bench_report import analyze_engines
from common import (
    DEFAULT_HOLD_DURATION,
    DROP_Z_THRESHOLD,
    INIT_QPOS,
    LEFT_CONTACT_SENSOR,
    MUJOCO_CONTACT_SLOT_SIZE,
    RIGHT_CONTACT_SENSOR,
    SETTLING_END_TIME,
    SETTLING_START_TIME,
    BenchRecorder,
    aggregate_contacts,
    build_bench_row,
    compute_ctrl_for_time,
    parse_motrixsim_contact_sensor,
    parse_mujoco_contact_sensor,
)

from motrixsim import SceneData, load_model, step

_HoldDuration = flags.DEFINE_float("hold_duration", DEFAULT_HOLD_DURATION, "Hold phase duration in seconds")
_OutDir = flags.DEFINE_string("out_dir", "examples/bench/grasp/.result", "Output directory for plots and report")
_Engines = flags.DEFINE_list(
    "engines",
    ["motrixsim", "mujoco", "mujoco_fastimplicit"],
    "Engines to run: motrixsim,mujoco,mujoco_fastimplicit",
)

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[3]
_OBJECT_NAME = "cube"
_MOTRIXSIM_ENGINE = "motrixsim"
_MUJOCO_ENGINE = "mujoco"
_MUJOCO_FASTIMPLICIT_ENGINE = "mujoco_fastimplicit"
_VALID_ENGINES = (_MOTRIXSIM_ENGINE, _MUJOCO_ENGINE, _MUJOCO_FASTIMPLICIT_ENGINE)


def _resolve_paths():
    scene_path = _PROJECT_ROOT / "examples" / "assets" / "franka_emika_panda" / f"scene_pick_{_OBJECT_NAME}.xml"
    out_dir = pathlib.Path(_OutDir.value)
    if not out_dir.is_absolute():
        out_dir = _PROJECT_ROOT / out_dir
    return scene_path, out_dir


def _parse_requested_engines():
    engines = [engine.strip().lower() for engine in _Engines.value if engine.strip()]
    if not engines:
        raise app.UsageError("--engines must contain at least one engine")
    invalid = [engine for engine in engines if engine not in _VALID_ENGINES]
    if invalid:
        raise app.UsageError(f"Unsupported engines: {', '.join(invalid)}")
    return engines


def _total_sim_duration() -> float:
    return SETTLING_END_TIME + _HoldDuration.value


def get_mujoco_sensor_layout(model, sensor_name):
    sensor_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SENSOR, sensor_name)
    adr = model.sensor_adr[sensor_id]
    dim = model.sensor_dim[sensor_id]
    num_slots = dim // MUJOCO_CONTACT_SLOT_SIZE
    return adr, dim, num_slots


def run_motrixsim(scene_path):
    model = load_model(str(scene_path))
    data = SceneData(model)
    dt = model.options.timestep
    total_duration = _total_sim_duration()

    panda = model.get_body(model.get_body_index("link0"))
    panda.set_dof_pos(data, INIT_QPOS)
    obj = model.get_body("obj")

    obj_mass = obj.base_link.mass
    expected_gf = obj_mass * np.linalg.norm(model.options.gravity)

    def set_arm_ctrl(target_qpos):
        start = model.get_actuator_index("actuator1")
        for i, val in enumerate(target_qpos):
            model.get_actuator(start + i).set_ctrl(data, val)

    def set_gripper_ctrl(val):
        model.get_actuator(model.get_actuator_index("actuator8")).set_ctrl(data, val)

    set_arm_ctrl(INIT_QPOS[:7])
    set_gripper_ctrl(INIT_QPOS[7])

    recorder = BenchRecorder()

    final_z = obj.get_pose(data)[2]
    step_cnt = 0
    drop_time = None
    while True:
        sim_time = step_cnt * dt
        if sim_time >= total_duration:
            break
        arm, gripper = compute_ctrl_for_time(sim_time, False)
        if arm is not None:
            set_arm_ctrl(arm)
        if gripper is not None:
            set_gripper_ctrl(gripper)

        step(model, data)

        obj_pose = obj.get_pose(data)
        final_z = obj_pose[2]
        left_contacts = parse_motrixsim_contact_sensor(model.get_sensor_value(LEFT_CONTACT_SENSOR, data))
        right_contacts = parse_motrixsim_contact_sensor(model.get_sensor_value(RIGHT_CONTACT_SENSOR, data))
        recorder.write(
            build_bench_row(
                step_cnt,
                False,
                obj_pose[:3],
                obj_pose[3:],
                aggregate_contacts(left_contacts),
                aggregate_contacts(right_contacts),
                expected_gf,
                obj_mass,
                sim_time=sim_time,
            )
        )

        if sim_time >= SETTLING_START_TIME and final_z < DROP_Z_THRESHOLD:
            drop_time = sim_time
            break
        step_cnt += 1

    rows = recorder.to_rows()
    last_step = rows[-1]["step"] if rows else step_cnt
    summary = dict(
        engine=_MOTRIXSIM_ENGINE,
        integrator="-",
        dt=float(dt),
        mass=float(obj_mass),
        expected_gf=float(expected_gf),
        total_duration=float(total_duration),
        last_step=last_step,
        final_z=float(final_z),
        held=final_z > DROP_Z_THRESHOLD,
        drop_time=drop_time,
    )
    return pd.DataFrame(rows), summary


def run_mujoco(scene_path, engine_label, integrator=None):
    model = mujoco.MjModel.from_xml_path(str(scene_path))
    if integrator is not None:
        model.opt.integrator = integrator
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, model.key("home").id)

    dt = model.opt.timestep
    total_duration = _total_sim_duration()
    init_qpos = model.key("home").qpos[:8].copy()

    act_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, f"actuator{i}") for i in range(1, 9)]
    obj_body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "obj")
    obj_mass = model.body_mass[obj_body_id]
    expected_gf = obj_mass * np.linalg.norm(model.opt.gravity)

    left_sensor_adr, left_sensor_dim, left_num_slots = get_mujoco_sensor_layout(model, LEFT_CONTACT_SENSOR)
    right_sensor_adr, right_sensor_dim, right_num_slots = get_mujoco_sensor_layout(model, RIGHT_CONTACT_SENSOR)

    def set_arm_ctrl(target_qpos):
        for i, val in enumerate(target_qpos):
            data.ctrl[act_ids[i]] = val

    def set_gripper_ctrl(val):
        data.ctrl[act_ids[7]] = val

    set_arm_ctrl(init_qpos[:7])
    set_gripper_ctrl(init_qpos[7])
    mujoco.mj_forward(model, data)

    recorder = BenchRecorder()
    integrator_name = mujoco.mjtIntegrator(model.opt.integrator).name.removeprefix("mjINT_").lower()

    final_z = data.xpos[obj_body_id][2]
    step_cnt = 0
    drop_time = None
    while True:
        sim_time = step_cnt * dt
        if sim_time >= total_duration:
            break
        arm, gripper = compute_ctrl_for_time(sim_time, False)
        if arm is not None:
            set_arm_ctrl(arm)
        if gripper is not None:
            set_gripper_ctrl(gripper)

        mujoco.mj_step(model, data)

        obj_qpos = data.qpos[9:16]
        obj_pos = obj_qpos[:3]
        obj_quat = np.array([obj_qpos[4], obj_qpos[5], obj_qpos[6], obj_qpos[3]])
        final_z = obj_pos[2]

        left_raw = data.sensordata[left_sensor_adr : left_sensor_adr + left_sensor_dim]
        right_raw = data.sensordata[right_sensor_adr : right_sensor_adr + right_sensor_dim]
        left_contacts = parse_mujoco_contact_sensor(left_raw, left_num_slots)
        right_contacts = parse_mujoco_contact_sensor(right_raw, right_num_slots)
        recorder.write(
            build_bench_row(
                step_cnt,
                False,
                obj_pos,
                obj_quat,
                aggregate_contacts(left_contacts),
                aggregate_contacts(right_contacts),
                expected_gf,
                obj_mass,
                sim_time=sim_time,
            )
        )

        if sim_time >= SETTLING_START_TIME and final_z < DROP_Z_THRESHOLD:
            drop_time = sim_time
            break
        step_cnt += 1

    rows = recorder.to_rows()
    last_step = rows[-1]["step"] if rows else step_cnt
    summary = dict(
        engine=engine_label,
        integrator=integrator_name,
        dt=float(dt),
        mass=float(obj_mass),
        expected_gf=float(expected_gf),
        total_duration=float(total_duration),
        last_step=last_step,
        final_z=float(final_z),
        held=final_z > DROP_Z_THRESHOLD,
        drop_time=drop_time,
    )
    return pd.DataFrame(rows), summary


def main(argv):
    del argv
    scene_path, out_dir = _resolve_paths()
    engines = {}
    summaries = []

    for engine_name in _parse_requested_engines():
        if engine_name == _MOTRIXSIM_ENGINE:
            engines[_MOTRIXSIM_ENGINE], summary = run_motrixsim(scene_path)
        elif engine_name == _MUJOCO_ENGINE:
            engines[_MUJOCO_ENGINE], summary = run_mujoco(scene_path, _MUJOCO_ENGINE)
        elif engine_name == _MUJOCO_FASTIMPLICIT_ENGINE:
            engines[_MUJOCO_FASTIMPLICIT_ENGINE], summary = run_mujoco(
                scene_path,
                _MUJOCO_FASTIMPLICIT_ENGINE,
                integrator=mujoco.mjtIntegrator.mjINT_IMPLICITFAST,
            )
        summaries.append(summary)

    analyze_engines(engines, out_dir, run_summaries=summaries)


if __name__ == "__main__":
    app.run(main)
