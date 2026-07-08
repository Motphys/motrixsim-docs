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

"""Shared constants, control logic, and contact analysis for grasp benchmarks."""

import numpy as np


def lerp(a, b, t):
    return a + t * (b - a)


INIT_QPOS = np.array([0.0, 0.0, 0.0, -1.5708, 0.0, 1.5708, -0.7853, 0.04, 0.04])
GRASP_QPOS = np.array([-1.0104, 1.5623, 1.3601, -1.6840, -1.5863, 1.7810, 1.4598, 0.04, 0.04])
LIFT_QPOS = np.array([-1.0426, 1.4028, 1.5634, -1.7114, -1.4055, 1.6015, 1.4510, 0.0, 0.0])
MOVE_TO_LIFT_DURATION = 1.0
MOVE_TO_GRASP_DURATION = 1.0
CLOSE_GRIPPER_DURATION = 1.0
LIFT_DURATION = 1.0
SETTLING_DURATION = 0.4
SETTLING_START_TIME = MOVE_TO_LIFT_DURATION + MOVE_TO_GRASP_DURATION + CLOSE_GRIPPER_DURATION + LIFT_DURATION
SETTLING_END_TIME = SETTLING_START_TIME + SETTLING_DURATION
DEFAULT_TOTAL_DURATION = 10.0
DEFAULT_HOLD_DURATION = DEFAULT_TOTAL_DURATION - SETTLING_END_TIME
DROP_Z_THRESHOLD = 0.03
LEFT_CONTACT_SENSOR = "grasp contact 1"
RIGHT_CONTACT_SENSOR = "grasp contact 2"
MOTRIXSIM_CONTACT_STRIDE = 16
MUJOCO_CONTACT_SLOT_SIZE = 17


def get_phase_label_for_time(sim_time, shake=False):
    if sim_time < MOVE_TO_LIFT_DURATION:
        return "move_to_lift"
    elif sim_time < MOVE_TO_LIFT_DURATION + MOVE_TO_GRASP_DURATION:
        return "move_to_grasp"
    elif sim_time < MOVE_TO_LIFT_DURATION + MOVE_TO_GRASP_DURATION + CLOSE_GRIPPER_DURATION:
        return "close_gripper"
    elif sim_time < SETTLING_START_TIME:
        return "lift"
    elif sim_time < SETTLING_END_TIME:
        return "settling"
    elif shake:
        return "shake"
    else:
        return "hold"


def compute_ctrl_for_time(sim_time, shake, rng=None, shake_step=None):
    """Compute control targets for the current simulation time."""
    arm = None
    gripper = None

    if 0.0 <= sim_time < MOVE_TO_LIFT_DURATION:
        arm = lerp(INIT_QPOS[:7], LIFT_QPOS[:7], sim_time / MOVE_TO_LIFT_DURATION)
    elif sim_time < MOVE_TO_LIFT_DURATION + MOVE_TO_GRASP_DURATION:
        t = (sim_time - MOVE_TO_LIFT_DURATION) / MOVE_TO_GRASP_DURATION
        arm = lerp(LIFT_QPOS[:7], GRASP_QPOS[:7], t)
    elif sim_time < MOVE_TO_LIFT_DURATION + MOVE_TO_GRASP_DURATION + CLOSE_GRIPPER_DURATION:
        t = (sim_time - MOVE_TO_LIFT_DURATION - MOVE_TO_GRASP_DURATION) / CLOSE_GRIPPER_DURATION
        gripper = lerp(0.04, 0, t)
    elif sim_time < SETTLING_START_TIME:
        t = (sim_time - MOVE_TO_LIFT_DURATION - MOVE_TO_GRASP_DURATION - CLOSE_GRIPPER_DURATION) / LIFT_DURATION
        arm = lerp(GRASP_QPOS[:7], LIFT_QPOS[:7], t)
    elif sim_time >= SETTLING_START_TIME and shake:
        if shake_step is not None and shake_step % 2 != 0:
            return arm, gripper
        if rng is not None:
            arm = LIFT_QPOS[:7] + rng.normal(0, 0.025, size=7)
        else:
            arm = LIFT_QPOS[:7] + np.random.normal(0, 0.025, size=7)

    return arm, gripper


def parse_motrixsim_contact_sensor(contact_data):
    """Parse the MotrixSim contact sensor payload into contact dicts.

    Layout: num_contacts(1), then per contact:
        force(3) + torque(3) + dist(1) + pos(3) + normal(3) + tangent(3)
    """
    contact_data = np.asarray(contact_data)
    if contact_data.size <= 1:
        return []

    num_contacts = int(contact_data[0])
    if num_contacts <= 0:
        return []

    contacts = []
    for i in range(num_contacts):
        off = 1 + i * MOTRIXSIM_CONTACT_STRIDE
        force = contact_data[off : off + 3]
        pos = contact_data[off + 7 : off + 10]
        normal = contact_data[off + 10 : off + 13]
        tangent0 = contact_data[off + 13 : off + 16]
        if force.size != 3 or pos.size != 3 or normal.size != 3 or tangent0.size != 3:
            continue
        tangent1 = np.cross(normal, tangent0)
        contacts.append(
            dict(
                force_normal=force[0],
                force_tangent0=force[1],
                force_tangent1=force[2],
                dist=contact_data[off + 6],
                pos=pos,
                normal=normal,
                tangent0=tangent0,
                tangent1=tangent1,
            )
        )
    return contacts


def parse_mujoco_contact_sensor(sensor_data, num_slots):
    """Parse MuJoCo contact sensor (data='found force torque dist pos normal tangent')."""
    contacts = []
    for i in range(num_slots):
        off = i * MUJOCO_CONTACT_SLOT_SIZE
        if off + MUJOCO_CONTACT_SLOT_SIZE > sensor_data.size:
            break
        if sensor_data[off] == 0:
            continue
        force = sensor_data[off + 1 : off + 4]
        pos = sensor_data[off + 8 : off + 11]
        normal = sensor_data[off + 11 : off + 14]
        tangent0 = sensor_data[off + 14 : off + 17]
        tangent1 = np.cross(normal, tangent0)
        contacts.append(
            dict(
                force_normal=force[0],
                force_tangent0=force[1],
                force_tangent1=force[2],
                dist=sensor_data[off + 7],
                pos=pos,
                normal=normal,
                tangent0=tangent0,
                tangent1=tangent1,
            )
        )
    return contacts


# ---------------------------------------------------------------------------
# Contact aggregation
# ---------------------------------------------------------------------------


def aggregate_contacts(contacts):
    """Aggregate parsed contact points into summary values.

    Each contact dict must have keys:
        force_normal, force_tangent0, force_tangent1,
        normal, tangent0, tangent1, dist, pos
    """
    zero = dict(
        num_contacts=0,
        total_normal_force=0.0,
        total_tangent_force=0.0,
        force_world=np.zeros(3),
        friction_world=np.zeros(3),
        normal_world=np.zeros(3),
        mean_dist=0.0,
        mean_pos=np.zeros(3),
    )
    if len(contacts) == 0:
        return zero

    total_normal = 0.0
    total_tangent = 0.0
    force_world = np.zeros(3)
    friction_world = np.zeros(3)
    normal_world = np.zeros(3)

    for c in contacts:
        total_normal += c["force_normal"]
        total_tangent += np.sqrt(c["force_tangent0"] ** 2 + c["force_tangent1"] ** 2)
        f_n = c["normal"] * c["force_normal"]
        f_t0 = c["tangent0"] * c["force_tangent0"]
        f_t1 = c["tangent1"] * c["force_tangent1"]
        normal_world += f_n
        friction_world += f_t0 + f_t1
        force_world += f_n + f_t0 + f_t1

    mean_dist = np.mean([c["dist"] for c in contacts])
    mean_pos = np.mean([c["pos"] for c in contacts], axis=0)
    return dict(
        num_contacts=len(contacts),
        total_normal_force=total_normal,
        total_tangent_force=total_tangent,
        force_world=force_world,
        friction_world=friction_world,
        normal_world=normal_world,
        mean_dist=mean_dist,
        mean_pos=mean_pos,
    )


def build_bench_row(
    step_cnt,
    shake,
    obj_pos,
    obj_quat,
    left_agg,
    right_agg,
    expected_gravity_force,
    object_mass,
    sim_time,
):
    """Build a benchmark row dict from aggregated contact data."""
    total_normal = left_agg["total_normal_force"] + right_agg["total_normal_force"]
    total_tangent = left_agg["total_tangent_force"] + right_agg["total_tangent_force"]
    total_force_world = left_agg["force_world"] + right_agg["force_world"]
    total_friction_world = left_agg["friction_world"] + right_agg["friction_world"]
    vertical_friction = total_friction_world[2]

    friction_ratio = total_tangent / total_normal if total_normal > 1e-8 else 0.0
    gravity_err = (
        abs(vertical_friction - expected_gravity_force) / expected_gravity_force
        if expected_gravity_force > 1e-8
        else 0.0
    )

    left_fn = float(np.linalg.norm(left_agg["force_world"]))
    right_fn = float(np.linalg.norm(right_agg["force_world"]))

    return dict(
        step=step_cnt,
        time=round(sim_time, 6),
        phase=get_phase_label_for_time(sim_time, shake),
        obj_x=obj_pos[0],
        obj_y=obj_pos[1],
        obj_z=obj_pos[2],
        obj_qx=obj_quat[0],
        obj_qy=obj_quat[1],
        obj_qz=obj_quat[2],
        obj_qw=obj_quat[3],
        left_num_contacts=left_agg["num_contacts"],
        left_normal_force=left_agg["total_normal_force"],
        left_tangent_force=left_agg["total_tangent_force"],
        left_mean_dist=left_agg["mean_dist"],
        left_contact_x=left_agg["mean_pos"][0],
        left_contact_y=left_agg["mean_pos"][1],
        left_contact_z=left_agg["mean_pos"][2],
        right_num_contacts=right_agg["num_contacts"],
        right_normal_force=right_agg["total_normal_force"],
        right_tangent_force=right_agg["total_tangent_force"],
        right_mean_dist=right_agg["mean_dist"],
        right_contact_x=right_agg["mean_pos"][0],
        right_contact_y=right_agg["mean_pos"][1],
        right_contact_z=right_agg["mean_pos"][2],
        total_normal_force=total_normal,
        total_tangent_force=total_tangent,
        total_force_x=total_force_world[0],
        total_force_y=total_force_world[1],
        total_force_z=total_force_world[2],
        vertical_friction=vertical_friction,
        expected_gravity_force=expected_gravity_force,
        object_mass=object_mass,
        friction_ratio=friction_ratio,
        gravity_balance_error=gravity_err,
        force_norm_left=left_fn,
        force_norm_right=right_fn,
    )


class BenchRecorder:
    """Collect benchmark rows in memory for downstream analysis."""

    def __init__(self):
        self.rows = []

    def write(self, row):
        self.rows.append(row)

    def to_rows(self):
        return list(self.rows)
