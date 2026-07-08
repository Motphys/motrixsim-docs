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

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Sequence

from motrixsim import SceneData, msd
from motrixsim.render import RenderApp

EXAMPLES_DIR = Path(__file__).resolve().parent.parent
CONTROL_DIR = Path(__file__).resolve().parent
UTILS_DIR = EXAMPLES_DIR / "utils"

for path in (CONTROL_DIR, UTILS_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from g1_motion_tracking_helpers import contract, initializer, reference, robot  # noqa: E402
from g1_motion_tracking_helpers import policy as policy_module  # noqa: E402

CAMERA_POSITION = [2.0, 0.0, 0.7]
CAMERA_TARGET = (0.0, 0.0, 0.0)
WORLD_UP = (0.0, 0.0, 1.0)


def _normalize(vector: Sequence[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0.0:
        raise ValueError("camera vector must be non-zero")
    return [value / norm for value in vector]


def _cross(lhs: Sequence[float], rhs: Sequence[float]) -> list[float]:
    return [
        lhs[1] * rhs[2] - lhs[2] * rhs[1],
        lhs[2] * rhs[0] - lhs[0] * rhs[2],
        lhs[0] * rhs[1] - lhs[1] * rhs[0],
    ]


def _build_camera_xyaxes(position: Sequence[float]) -> list[float]:
    camera_back_axis = _normalize([position[index] - CAMERA_TARGET[index] for index in range(3)])
    camera_right_axis = _normalize(_cross(WORLD_UP, camera_back_axis))
    camera_up_axis = _cross(camera_back_axis, camera_right_axis)
    return [*camera_right_axis, *camera_up_axis]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Standalone G1 motion-tracking playback with ONNX.")
    parser.add_argument("--onnx", type=Path, default=contract.DEFAULT_ONNX_PATH, help="Path to the ONNX policy file.")
    parser.add_argument(
        "--motion",
        type=Path,
        default=contract.DEFAULT_MOTION_PATH,
        help="Path to the reference motion .npz file.",
    )
    parser.add_argument("--scene", type=Path, default=contract.DEFAULT_SCENE_PATH, help="Path to the base scene XML.")
    parser.add_argument(
        "--action-scale",
        type=float,
        default=contract.DEFAULT_ACTION_SCALE,
        help="Scale applied to the ONNX action before adding default joint angles.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Preferred ONNX Runtime device hint, e.g. cpu or cuda:0.",
    )
    parser.add_argument(
        "--ctrl-dt",
        type=float,
        default=contract.DEFAULT_CTRL_DT,
        help="Control interval in seconds.",
    )
    parser.add_argument(
        "--render-fps",
        type=float,
        default=contract.DEFAULT_RENDER_FPS,
        help="Render synchronization rate.",
    )
    return parser


def _build_follow_camera():
    pos = " ".join(str(value) for value in CAMERA_POSITION)
    xyaxes = " ".join(f"{value:.17g}" for value in _build_camera_xyaxes(CAMERA_POSITION))
    camera_mjcf = f"""<mujoco model="camera">
  <worldbody>
    <camera name="follower" pos="{pos}" xyaxes="{xyaxes}" trackposspeed="2" trackrotspeed="2" />
  </worldbody>
</mujoco>"""
    return msd.from_str(camera_mjcf)


def _load_model(scene_path: Path, g1_robot_cls):
    scene = msd.from_file(str(scene_path))
    g1_robot = msd.from_file(g1_robot_cls.mjcf_path)
    g1_robot.attach(_build_follow_camera(), g1_robot_cls.base_link_name)
    scene.attach(g1_robot)
    model = scene.build()

    camera = model.cameras["follower"]
    camera.rotation_track = "look_at_link"
    camera.position_track = "fixed_local"
    camera.track_target_link = model.get_link(g1_robot_cls.base_link_name)
    return model, camera


def main() -> None:
    args = _build_parser().parse_args()

    onnx_path = contract.ensure_file_exists(args.onnx, "ONNX")
    motion_path = contract.ensure_file_exists(args.motion, "Motion")
    scene_path = contract.ensure_file_exists(args.scene, "Scene")

    motion_reference = reference.MotionReference(
        str(motion_path),
        body_indices=contract.MOTION_BODY_INDICES,
    )
    model, camera = _load_model(scene_path, robot.G1MotionTrackingRobot)
    model.options.timestep = contract.DEFAULT_SIM_DT
    data = SceneData(model)
    initializer.apply_motion_tracking_profile(model, data)

    contract.ensure_actuator_count(model)
    contract.ensure_body_names(model)
    contract.ensure_sensor_names(model, data)

    body = model.get_body(robot.G1MotionTrackingRobot.base_link_name)
    if body is None:
        raise ValueError(f"Body '{robot.G1MotionTrackingRobot.base_link_name}' not found in model")

    tracking_robot = robot.G1MotionTrackingRobot(body)
    policy = policy_module.G1MotionTrackingPolicy(
        robot=tracking_robot,
        onnx_path=str(onnx_path),
        action_scale=args.action_scale,
        device=args.device,
    )
    initializer.initialize_motion_tracking_state(
        robot=tracking_robot,
        model=model,
        data=data,
        motion_data=motion_reference.current(),
    )

    with RenderApp() as render:
        render.set_main_camera(camera)
        render.launch(model)

        phys_dt = float(model.options.timestep)
        n_ctrl = max(1, round(args.ctrl_dt / phys_dt))
        n_render = max(1, round((1.0 / args.render_fps) / phys_dt))
        step_index = 0

        while True:
            if render.is_closed:
                break

            model.step(data)
            step_index += 1

            if step_index % n_ctrl == 0:
                policy.step(data, motion_reference.current())
                motion_reference.advance_by_dt(args.ctrl_dt)

            if render.input.is_key_just_pressed("escape"):
                break

            if step_index % n_render == 0:
                render.sync(data)


if __name__ == "__main__":
    main()
