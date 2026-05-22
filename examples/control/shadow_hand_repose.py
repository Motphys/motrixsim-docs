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

from pathlib import Path

import numpy as np
import onnxruntime as ort

from motrixsim import SceneData, SceneModel, load_model
from motrixsim.render import RenderApp

ASSET_DIR = Path(__file__).resolve().parents[1] / "assets" / "shadow_hand_repose"
MODEL_FILE = ASSET_DIR / "repose_cube.xml"
ONNX_FILE = ASSET_DIR / "shadow_hand_repose.onnx"

OBS_DIM = 157
ACTION_DIM = 20
HAND_DOF_DIM = 24
NUM_FINGERTIPS = 5
CTRL_DT = 0.01
VEL_OBS_SCALE = 0.2

CUBE_INITIAL_POS = np.array([0.33, 0.0, 0.295], dtype=np.float32)
CUBE_INITIAL_ROT = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)
GOAL_POS = CUBE_INITIAL_POS.copy()
GOAL_ROT = np.array([0.0, 0.0, 0.70710677, 0.70710677], dtype=np.float32)
TARGET_VIZ_OFFSET = np.array([0.0, 0.0, 0.2], dtype=np.float32)

HAND_JOINTS = [
    "rh_WRJ2",
    "rh_WRJ1",
    "rh_FFJ4",
    "rh_FFJ3",
    "rh_FFJ2",
    "rh_FFJ1",
    "rh_MFJ4",
    "rh_MFJ3",
    "rh_MFJ2",
    "rh_MFJ1",
    "rh_RFJ4",
    "rh_RFJ3",
    "rh_RFJ2",
    "rh_RFJ1",
    "rh_LFJ5",
    "rh_LFJ4",
    "rh_LFJ3",
    "rh_LFJ2",
    "rh_LFJ1",
    "rh_THJ5",
    "rh_THJ4",
    "rh_THJ3",
    "rh_THJ2",
    "rh_THJ1",
]

HAND_DOF_LOWER = np.array(
    [
        -0.523599,
        -0.698132,
        -0.349066,
        -0.261799,
        0.0,
        0.0,
        -0.349066,
        -0.261799,
        0.0,
        0.0,
        -0.349066,
        -0.261799,
        0.0,
        0.0,
        0.0,
        -0.349066,
        -0.261799,
        0.0,
        0.0,
        -1.0472,
        0.0,
        -0.20944,
        -0.698132,
        -0.261799,
    ],
    dtype=np.float32,
)
HAND_DOF_UPPER = np.array(
    [
        0.174533,
        0.488692,
        0.349066,
        1.5708,
        1.5708,
        1.5708,
        0.349066,
        1.5708,
        1.5708,
        1.5708,
        0.349066,
        1.5708,
        1.5708,
        1.5708,
        0.785398,
        0.349066,
        1.5708,
        1.5708,
        1.5708,
        1.0472,
        1.22173,
        0.20944,
        0.698132,
        1.5708,
    ],
    dtype=np.float32,
)

FINGERTIP_LINKS = [
    "rh_ffdistal",
    "rh_mfdistal",
    "rh_rfdistal",
    "rh_lfdistal",
    "rh_thdistal",
]

ACTUATORS = [
    "rh_A_WRJ2",
    "rh_A_WRJ1",
    "rh_A_THJ5",
    "rh_A_THJ4",
    "rh_A_THJ3",
    "rh_A_THJ2",
    "rh_A_THJ1",
    "rh_A_FFJ4",
    "rh_A_FFJ3",
    "rh_A_FFJ0",
    "rh_A_MFJ4",
    "rh_A_MFJ3",
    "rh_A_MFJ0",
    "rh_A_RFJ4",
    "rh_A_RFJ3",
    "rh_A_RFJ0",
    "rh_A_LFJ5",
    "rh_A_LFJ4",
    "rh_A_LFJ3",
    "rh_A_LFJ0",
]

ACTUATOR_LOWER = np.array(
    [
        -0.523599,
        -0.698132,
        -1.0472,
        0.0,
        -0.20944,
        -0.698132,
        -0.261799,
        -0.349066,
        -0.261799,
        0.0,
        -0.349066,
        -0.261799,
        0.0,
        -0.349066,
        -0.261799,
        0.0,
        0.0,
        -0.349066,
        -0.261799,
        0.0,
    ],
    dtype=np.float32,
)
ACTUATOR_UPPER = np.array(
    [
        0.174533,
        0.488692,
        1.0472,
        1.22173,
        0.20944,
        0.698132,
        1.5708,
        0.349066,
        1.5708,
        3.1415,
        0.349066,
        1.5708,
        3.1415,
        0.349066,
        1.5708,
        3.1415,
        0.785398,
        0.349066,
        1.5708,
        3.1415,
    ],
    dtype=np.float32,
)


def quat_conjugate(q: np.ndarray) -> np.ndarray:
    return np.array([-q[0], -q[1], -q[2], q[3]], dtype=np.float32)


def quat_mul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    q = np.array(
        [
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz,
        ],
        dtype=np.float32,
    )
    norm = np.linalg.norm(q)
    return q / norm if norm > 1e-6 else CUBE_INITIAL_ROT.copy()


def random_unit_quat(rng: np.random.Generator) -> np.ndarray:
    u1, u2, u3 = rng.random(3)
    q = np.array(
        [
            np.sqrt(1.0 - u1) * np.sin(2.0 * np.pi * u2),
            np.sqrt(1.0 - u1) * np.cos(2.0 * np.pi * u2),
            np.sqrt(u1) * np.sin(2.0 * np.pi * u3),
            np.sqrt(u1) * np.cos(2.0 * np.pi * u3),
        ],
        dtype=np.float32,
    )
    return q / np.linalg.norm(q)


def unscale(value: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
    return 2.0 * (value - lower) / np.maximum(upper - lower, 1e-6) - 1.0


def scale_actions(actions: np.ndarray) -> np.ndarray:
    actions = np.clip(actions, -1.0, 1.0)
    targets = ACTUATOR_LOWER + (actions + 1.0) * 0.5 * (ACTUATOR_UPPER - ACTUATOR_LOWER)
    return np.clip(targets, ACTUATOR_LOWER, ACTUATOR_UPPER).astype(np.float32)


class ShadowHandReposePolicy:
    def __init__(self, model: SceneModel):
        self.model = model
        self.hand_joints = [self._require(model.get_joint(name), f"joint {name}") for name in HAND_JOINTS]
        self.fingertip_links = [self._require(model.get_link(name), f"link {name}") for name in FINGERTIP_LINKS]
        self.actuators = [self._require(model.get_actuator(name), f"actuator {name}") for name in ACTUATORS]
        self.cube_body = self._require(model.get_body("cube"), "body cube")
        self.target_body = self._require(model.get_body("target"), "body target")
        self.target_mocap = self._require(self.target_body.mocap, "target mocap")

        self.session = ort.InferenceSession(str(ONNX_FILE), providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

        self.rng = np.random.default_rng()
        self.goal_pos = GOAL_POS.copy()
        self.goal_rot = GOAL_ROT.copy()
        self.prev_actions = np.zeros(ACTION_DIM, dtype=np.float32)

    @staticmethod
    def _require(value, description: str):
        if value is None:
            raise RuntimeError(f"missing {description}")
        return value

    def reset_data(self, data: SceneData) -> None:
        for joint in self.hand_joints:
            joint.set_dof_pos(data, [0.0])
        self.cube_body.floatingbase.set_translation(data, CUBE_INITIAL_POS)
        self.cube_body.floatingbase.set_rotation(data, CUBE_INITIAL_ROT)
        data.set_dof_vel(np.zeros_like(data.dof_vel))
        for actuator in self.actuators:
            actuator.set_ctrl(data, 0.0)
        self.goal_pos = GOAL_POS.copy()
        self.goal_rot = random_unit_quat(self.rng)
        self.prev_actions = np.zeros(ACTION_DIM, dtype=np.float32)
        self.update_target_visual(data)
        self.model.forward_kinematic(data)

    def update_target_visual(self, data: SceneData) -> None:
        target_pos = self.goal_pos + TARGET_VIZ_OFFSET
        self.target_mocap.set_pose(data, np.concatenate([target_pos, self.goal_rot]).astype(np.float32))

    def compute_observation(self, data: SceneData) -> np.ndarray:
        hand_pos = np.array([joint.get_dof_pos(data)[0] for joint in self.hand_joints], dtype=np.float32)
        hand_vel = np.array([joint.get_dof_vel(data)[0] for joint in self.hand_joints], dtype=np.float32)
        cube_pose = np.asarray(self.cube_body.get_pose(data), dtype=np.float32)
        cube_vel = np.asarray(data.dof_vel[self.cube_body.get_dof_vel_indices(True)], dtype=np.float32)

        fingertip_pos = []
        fingertip_quat = []
        fingertip_vel = []
        for link in self.fingertip_links:
            pose = np.asarray(link.get_pose(data), dtype=np.float32)
            fingertip_pos.append(pose[:3])
            fingertip_quat.append(pose[3:7])
            fingertip_vel.append(
                np.concatenate(
                    [
                        np.asarray(link.get_linear_velocity(data), dtype=np.float32),
                        np.asarray(link.get_angular_velocity(data), dtype=np.float32),
                    ]
                )
            )

        relative_quat = quat_mul(cube_pose[3:7], quat_conjugate(self.goal_rot))
        obs = np.concatenate(
            [
                unscale(hand_pos, HAND_DOF_LOWER, HAND_DOF_UPPER),
                VEL_OBS_SCALE * hand_vel,
                cube_pose[:3],
                cube_pose[3:7],
                cube_vel[:3],
                VEL_OBS_SCALE * cube_vel[3:6],
                self.goal_pos,
                self.goal_rot,
                relative_quat,
                np.concatenate(fingertip_pos),
                np.concatenate(fingertip_quat),
                np.concatenate(fingertip_vel),
                self.prev_actions,
            ]
        ).astype(np.float32)
        assert obs.shape == (OBS_DIM,)
        return obs

    def apply_action(self, data: SceneData, action: np.ndarray) -> None:
        targets = scale_actions(np.asarray(action, dtype=np.float32).reshape(ACTION_DIM))
        for actuator, ctrl in zip(self.actuators, targets):
            actuator.set_ctrl(data, float(ctrl))
        self.prev_actions = targets.copy()

    def step(self, data: SceneData) -> None:
        obs = self.compute_observation(data).reshape(1, -1).astype(np.float32)
        actions = self.session.run([self.output_name], {self.input_name: obs})[0][0]
        self.apply_action(data, actions)


def main() -> None:
    model = load_model(str(MODEL_FILE))
    data = SceneData(model)
    policy = ShadowHandReposePolicy(model)
    policy.reset_data(data)

    phys_dt = float(model.options.timestep)
    ctrl_interval = max(1, round(CTRL_DT / phys_dt))
    render_interval = max(1, round((1.0 / 60.0) / phys_dt))

    print("Running shadow_hand_repose. Press R to reset, ESC to exit.")
    with RenderApp() as render:
        render.launch(model)
        step_index = 0
        while not render.is_closed:
            model.step(data)
            step_index += 1

            if step_index % ctrl_interval == 0:
                policy.step(data)

            if render.input.is_key_just_pressed("r"):
                data = SceneData(model)
                policy.reset_data(data)
                step_index = 0
            if render.input.is_key_just_pressed("esc"):
                break

            if step_index % render_interval == 0:
                render.sync(data)


if __name__ == "__main__":
    main()
