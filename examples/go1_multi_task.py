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

from __future__ import annotations

from enum import Enum
from pathlib import Path

import numpy as np
import onnxruntime as ort

from motrixsim import SceneData, load_model
from motrixsim.render import RenderApp

EXAMPLE_DIR = Path(__file__).resolve().parent
GO1_ASSET_DIR = EXAMPLE_DIR / "assets" / "go1"
POLICY_DIR = GO1_ASSET_DIR / "policies"
MODEL_PATH = str(GO1_ASSET_DIR / "scene-multi-task.xml")
JOYSTICK_POLICY_PATH = str(POLICY_DIR / "go1_policy.onnx")
HANDSTAND_POLICY_PATH = str(POLICY_DIR / "go1_hs_stay_still.onnx")
FOOTSTAND_POLICY_PATH = str(POLICY_DIR / "go1_fs_policy.onnx")
GETUP_POLICY_PATH = str(POLICY_DIR / "go1_gu_policy.onnx")

# default joint values will be subtracted for onnx input and added for output
DEFAULT_JOINT_VALUES = np.array([0.1, 0.9, -1.8, -0.1, 0.9, -1.8, 0.1, 0.9, -1.8, -0.1, 0.9, -1.8], dtype=np.float32)
HANDSTAND_TO_GETUP = np.array([0.1, -0.68, -1.8, -0.1, -0.68, -1.8, 0.1, 0.9, -1.8, -0.1, 0.9, -1.8], dtype=np.float32)
FOOTSTAND_TO_GETUP = np.array([-0.2, 0.3, -0.8, 0.2, 0.3, -0.8, -0.2, 0.9, -1.0, 0.2, 0.9, -1.0], dtype=np.float32)
DISTURBING_DEVICE_CTRLS = {
    "h1": 1.5,
    "h2": -1.5,
    "h3": 2.0,
    "s1": 2.0,
    "s2": -2.0,
}

# target angle = action_scale * action + default_angle
ACTION_SCALE = 0.5
CONTROL_DT = 0.02
RENDER_FPS = 60.0
WAITING_TIME = 60
MANUAL_GETUP_PRE_ROLL = 15
CAN_SWITCH_TO_STAND_THRESHOLD = 2.0
COMMAND_LIN_VEL_SCALE = 1.5
COMMAND_ANG_VEL_SCALE = 3.0


class Mode(Enum):
    JOYSTICK = "joystick"
    HANDSTAND = "handstand"
    GETUP = "getup"
    FOOTSTAND = "footstand"


class OnnxPolicy:
    def __init__(self, path: str):
        self._session = ort.InferenceSession(path, providers=["CPUExecutionProvider"])
        self._input_name = self._session.get_inputs()[0].name
        self._output_name = self._session.get_outputs()[0].name

    def run(self, observation: np.ndarray) -> np.ndarray:
        outputs = self._session.run([self._output_name], {self._input_name: observation.reshape(1, -1)})
        return np.asarray(outputs[0][0], dtype=np.float32)


class Go1Robot:
    base_link_name = "trunk"

    def __init__(self, body):
        self.body = body
        self.model = body.model

    def dof_pos(self, data: SceneData) -> np.ndarray:
        return self.body.get_joint_dof_pos(data)

    def dof_vel(self, data: SceneData) -> np.ndarray:
        return self.body.get_joint_dof_vel(data)

    def set_actuator_ctrls(self, data: SceneData, ctrls: np.ndarray) -> None:
        self.body.set_actuator_ctrls(data, ctrls)

    def gravity(self, data: SceneData) -> np.ndarray:
        rotation = self.body.get_rotation_mat(data)
        return rotation.T @ np.array([0.0, 0.0, -1.0], dtype=np.float32)

    def local_linear_vel(self, data: SceneData) -> np.ndarray:
        return self.model.get_sensor_value("local_linvel", data)

    def gyro(self, data: SceneData) -> np.ndarray:
        return self.model.get_sensor_value("gyro", data)


class Go1MultiTaskPolicy:
    def __init__(self, model):
        body = model.get_body("trunk")
        if body is None:
            raise RuntimeError("Missing Go1 body 'trunk' in the scene model.")

        actuator_start = model.get_actuator_index("FR_hip")
        if actuator_start is None:
            raise RuntimeError("Missing Go1 actuator 'FR_hip' in the scene model.")

        self._model = model
        self._robot = Go1Robot(body)
        self._actuator_start = actuator_start
        self._policies = {
            "joystick": OnnxPolicy(JOYSTICK_POLICY_PATH),
            "handstand": OnnxPolicy(HANDSTAND_POLICY_PATH),
            "getup": OnnxPolicy(GETUP_POLICY_PATH),
            "footstand": OnnxPolicy(FOOTSTAND_POLICY_PATH),
        }

        self.mode = Mode.JOYSTICK
        self.wait_to_stand: Mode | None = None
        self.wait_steps_left = 0
        self.mode_to_getup: Mode | None = None
        self.mode_to_getup_wait_steps = 0
        self.last_action = np.zeros_like(DEFAULT_JOINT_VALUES)

    @property
    def status_text(self) -> str:
        if self.wait_to_stand is not None:
            return f"{self.mode.value} -> {self.wait_to_stand.value} ({self.wait_steps_left})"
        return self.mode.value

    def reset(self) -> SceneData:
        data = SceneData(self._model)
        self.mode = Mode.JOYSTICK
        self.wait_to_stand = None
        self.wait_steps_left = 0
        self.mode_to_getup = None
        self.mode_to_getup_wait_steps = 0
        self.last_action.fill(0.0)

        self._robot.body.set_dof_pos(data, DEFAULT_JOINT_VALUES, False)
        self._robot.set_actuator_ctrls(data, DEFAULT_JOINT_VALUES)

        seesaw_joint = self._model.get_joint("seesaw_joint")
        if seesaw_joint is not None:
            seesaw_joint.set_dof_pos(data, [0.1645])

        for actuator_name, ctrl in DISTURBING_DEVICE_CTRLS.items():
            actuator = self._model.get_actuator(actuator_name)
            if actuator is not None:
                actuator.set_ctrl(data, ctrl)

        return data

    def handle_mode_request(self, request: str) -> None:
        old_status = self.status_text

        if request == "handstand":
            if self.wait_to_stand is None:
                if self.mode is Mode.JOYSTICK:
                    self._begin_wait_to_stand(Mode.HANDSTAND)
                elif self.mode in (Mode.HANDSTAND, Mode.FOOTSTAND):
                    self._enter_getup(origin_mode=self.mode, manual=True)
                elif self.mode is Mode.GETUP:
                    self._enter_joystick()
        elif request == "footstand":
            if self.wait_to_stand is None:
                if self.mode is Mode.JOYSTICK:
                    self._begin_wait_to_stand(Mode.FOOTSTAND)
                elif self.mode in (Mode.HANDSTAND, Mode.FOOTSTAND):
                    self._enter_getup(origin_mode=self.mode, manual=True)
                elif self.mode is Mode.GETUP:
                    self._enter_joystick()
        elif request == "recovery":
            if self.mode is Mode.GETUP:
                self._enter_joystick()
            else:
                origin_mode = self.mode if self.mode in (Mode.HANDSTAND, Mode.FOOTSTAND) else None
                self._enter_getup(origin_mode=origin_mode, manual=origin_mode is not None)

        if self.status_text != old_status:
            print(f"Mode: {self.status_text}")

    def step(self, data: SceneData, command: np.ndarray) -> str | None:
        old_status = self.status_text
        camera_name = self._update_transitions(data)
        if self.status_text != old_status:
            print(f"Mode: {self.status_text}")

        observation = self._compute_observation(data, command)
        action = self._policies[self._active_policy_name()].run(observation)
        self._apply_action(data, action)
        return camera_name

    def _begin_wait_to_stand(self, target_mode: Mode) -> None:
        self.wait_to_stand = target_mode
        self.wait_steps_left = WAITING_TIME
        self.mode_to_getup = None
        self.mode_to_getup_wait_steps = 0

    def _enter_joystick(self) -> None:
        self.mode = Mode.JOYSTICK
        self.wait_to_stand = None
        self.wait_steps_left = 0
        self.mode_to_getup = None
        self.mode_to_getup_wait_steps = 0

    def _enter_getup(self, origin_mode: Mode | None, manual: bool) -> None:
        self.mode = Mode.GETUP
        self.wait_to_stand = None
        self.wait_steps_left = 0

        if manual and origin_mode in (Mode.HANDSTAND, Mode.FOOTSTAND):
            self.mode_to_getup = origin_mode
            self.mode_to_getup_wait_steps = MANUAL_GETUP_PRE_ROLL
        else:
            self.mode_to_getup = None
            self.mode_to_getup_wait_steps = 0

    def _active_policy_name(self) -> str:
        if self.mode is Mode.HANDSTAND:
            return "handstand"
        if self.mode is Mode.GETUP:
            return "getup"
        if self.mode is Mode.FOOTSTAND:
            return "footstand"
        return "joystick"

    def _update_transitions(self, data: SceneData) -> str | None:
        if self.mode is Mode.GETUP and self._can_exit_getup(data):
            self._enter_joystick()
            return "back"

        if self.mode is not Mode.GETUP and self._should_enter_getup(data):
            self._enter_getup(origin_mode=None, manual=False)
            return None

        if self.wait_to_stand is not None:
            self.wait_steps_left = max(self.wait_steps_left - 1, 0)
            if self._can_switch_to_stand(data) or self.wait_steps_left == 0:
                self.mode = self.wait_to_stand
                self.wait_to_stand = None
                self.wait_steps_left = 0
            return "side"

        return None

    def _compute_observation(self, data: SceneData, command: np.ndarray) -> np.ndarray:
        joint_pos = self._robot.dof_pos(data)
        joint_vel = self._robot.dof_vel(data)
        joint_offset = joint_pos - DEFAULT_JOINT_VALUES

        if self.mode is Mode.GETUP:
            obs = np.concatenate(
                [
                    self._robot.gyro(data),
                    self._robot.gravity(data),
                    joint_offset,
                    joint_vel,
                    self.last_action,
                ]
            )
            return obs.astype(np.float32)

        obs_parts = [
            self._robot.local_linear_vel(data),
            self._robot.gyro(data),
            self._robot.gravity(data),
            joint_offset,
            joint_vel,
            self.last_action,
        ]

        if self.mode is Mode.JOYSTICK:
            cmd = np.zeros(3, dtype=np.float32) if self.wait_to_stand is not None else self._scale_command(command)
            obs_parts.append(cmd)

        return np.concatenate(obs_parts).astype(np.float32)

    def _scale_command(self, command: np.ndarray) -> np.ndarray:
        scaled = np.asarray(command, dtype=np.float32).copy()
        scaled[:2] *= COMMAND_LIN_VEL_SCALE
        scaled[2] *= COMMAND_ANG_VEL_SCALE
        return scaled

    def _apply_action(self, data: SceneData, action: np.ndarray) -> None:
        self.last_action = np.asarray(action, dtype=np.float32).copy()

        if self.mode is Mode.GETUP:
            if self.mode_to_getup is not None and self.mode_to_getup_wait_steps > 0:
                ctrl = HANDSTAND_TO_GETUP if self.mode_to_getup is Mode.HANDSTAND else FOOTSTAND_TO_GETUP
                self.mode_to_getup_wait_steps -= 1
                if self.mode_to_getup_wait_steps == 0:
                    self.mode_to_getup = None
            else:
                ctrl = self.last_action * ACTION_SCALE + self._robot.dof_pos(data)
        elif self.mode in (Mode.HANDSTAND, Mode.FOOTSTAND):
            current_ctrl = self._model.get_actuator_ctrls(data)[
                self._actuator_start : self._actuator_start + len(self.last_action)
            ]
            ctrl = self.last_action * ACTION_SCALE + current_ctrl
        else:
            ctrl = self.last_action * ACTION_SCALE + DEFAULT_JOINT_VALUES

        self._robot.set_actuator_ctrls(data, np.asarray(ctrl, dtype=np.float32))

    def _upright_alignment(self, data: SceneData) -> float:
        rotation = np.asarray(self._robot.body.get_rotation_mat(data), dtype=np.float32)
        return float(np.dot(rotation[:, 2], np.array([0.0, 0.0, 1.0], dtype=np.float32)))

    def _can_exit_getup(self, data: SceneData) -> bool:
        diff_sum = float(np.abs(self._robot.dof_pos(data) - DEFAULT_JOINT_VALUES).sum())
        return diff_sum < 2.0 and self._upright_alignment(data) > 0.85

    def _should_enter_getup(self, data: SceneData) -> bool:
        threshold = -0.6 if self.mode in (Mode.HANDSTAND, Mode.FOOTSTAND) else 0.3
        return self._upright_alignment(data) < threshold

    def _can_switch_to_stand(self, data: SceneData) -> bool:
        dof_vel = self._robot.dof_vel(data)
        return float(np.dot(dof_vel, dof_vel)) < CAN_SWITCH_TO_STAND_THRESHOLD


def read_keyboard_command(input_state) -> np.ndarray:
    move_x = float(input_state.is_key_pressed("w")) - float(input_state.is_key_pressed("s"))
    move_y = float(input_state.is_key_pressed("a")) - float(input_state.is_key_pressed("d"))
    move = np.array([move_x, move_y], dtype=np.float32)

    norm = np.linalg.norm(move)
    if norm > 1.0:
        move /= norm

    yaw = float(input_state.is_key_pressed("left")) - float(input_state.is_key_pressed("right"))
    return np.array([move[0], move[1], yaw], dtype=np.float32)


def print_controls() -> None:
    print("Go1 Multi-Task Demo")
    print("Controls:")
    print("  W/A/S/D      Move robot")
    print("  Left/Right   Rotate robot")
    print("  U            Enter handstand flow / exit getup")
    print("  I            Enter footstand flow / exit getup")
    print("  O            Manual recovery / exit getup")
    print("  Q / E        Next / previous camera")
    print("  P            Reset scene")
    print("  Esc          Exit")


def main() -> None:
    model = load_model(MODEL_PATH)
    policy = Go1MultiTaskPolicy(model)
    data = policy.reset()

    phys_dt = model.options.timestep
    n_ctrl = max(1, round(CONTROL_DT / phys_dt))
    n_render = max(1, round((1.0 / RENDER_FPS) / phys_dt))

    with RenderApp() as render:
        render.launch(model)

        camera_cycle = [
            None,
            model.cameras["track"],
            model.cameras["top"],
            model.cameras["side"],
            model.cameras["back"],
        ]
        camera_labels = ["free", "track", "top", "side", "back"]
        current_camera_idx = -1

        queued_mode_request: str | None = None
        queued_camera_delta = 0
        queued_reset = False

        def set_camera(index: int, announce: bool = True) -> None:
            nonlocal current_camera_idx
            index %= len(camera_cycle)
            if index == current_camera_idx:
                return
            current_camera_idx = index
            render.set_main_camera(camera_cycle[index])
            if announce:
                print(f"Camera: {camera_labels[index]}")

        def set_named_camera(name: str) -> None:
            set_camera(camera_labels.index(name))

        print_controls()
        set_named_camera("back")
        render.sync(data)

        step_count = 0
        while True:
            if render.is_closed or render.input.is_key_just_pressed("escape"):
                break

            if render.input.is_key_just_pressed("u"):
                queued_mode_request = "handstand"
            if render.input.is_key_just_pressed("i"):
                queued_mode_request = "footstand"
            if render.input.is_key_just_pressed("o"):
                queued_mode_request = "recovery"
            if render.input.is_key_just_pressed("q"):
                queued_camera_delta += 1
            if render.input.is_key_just_pressed("e"):
                queued_camera_delta -= 1
            if render.input.is_key_just_pressed("p"):
                queued_reset = True

            command = read_keyboard_command(render.input)

            if queued_reset:
                data = policy.reset()
                step_count = 0
                queued_mode_request = None
                queued_camera_delta = 0
                queued_reset = False
                set_named_camera("back")
                print("Scene reset")
                render.sync(data)
                continue

            if queued_camera_delta != 0:
                set_camera(current_camera_idx + queued_camera_delta)
                queued_camera_delta = 0

            for _ in range(n_render):
                model.step(data)
                step_count += 1

                if step_count % n_ctrl == 0:
                    if queued_mode_request is not None:
                        policy.handle_mode_request(queued_mode_request)
                        queued_mode_request = None

                    camera_name = policy.step(data, command)
                    if camera_name is not None:
                        set_named_camera(camera_name)

            render.sync(data)


if __name__ == "__main__":
    main()
