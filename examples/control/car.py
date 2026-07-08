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


import math
import os
from dataclasses import dataclass

import numpy as np

from motrixsim import SceneData, msd, run, step
from motrixsim.render import Layout, RenderApp

FORWARD_CTRL = 340.0
REVERSE_CTRL = 380.0
BRAKE_CTRL = 700.0
STEERING_CTRL = 0.2
STEERING_NEUTRAL_TRIM = -0.01
STEERING_JOINT = "car_MFX_CDG_ZXG_ZXG_MIDDLE_joint"
HEADING_HOLD_GAIN = 0.24
HEADING_HOLD_MAX_CORRECTION = 0.08
HEADING_HOLD_RECOVERY_STEPS = 36
REVERSE_HEADING_HOLD_GAIN = 0.3
REVERSE_HEADING_HOLD_MAX_CORRECTION = 0.12
FORWARD_RAMP = 18.0
REVERSE_RAMP = 14.0
BRAKE_RAMP = 800.0
DRIVE_DECAY = 12.0
DRIVE_BRAKE = 28.0
BRAKE_RELEASE_SPEED_MPS = 0.08
STEER_INPUT_STEP = 0.08
STEER_RETURN_STEP = 0.072
STEER_RESPONSE_STEP = 0.09
HIGH_SPEED_STEER_FACTOR = 0.35
HIGH_SPEED_MPS = 8.0
VERY_HIGH_SPEED_STEER_FACTOR = 0.2
VERY_HIGH_SPEED_MPS = 14.0
REVERSE_STABILITY_FADE_START_MPS = 3.4
REVERSE_STABILITY_FADE_END_MPS = 4.0
FORWARD_SPEED_FADE_START_MPS = 11.5
FORWARD_SPEED_LIMIT_MPS = 15.0
STEER_RECENTER_GAIN = 3.2
STEER_RECENTER_DAMPING = 0.3
STEER_RECENTER_MAX = 0.08
STEER_SETTLED_POS = 0.01
STEER_SETTLED_VEL = 0.06
CONTROL_REFERENCE_DT = 1.0 / 60.0
STABILITY_CORRECTION_BLEND_RATE = 0.2
TURN_TAP_MAX_STEPS = 16
TURN_TAP_RELEASE_DAMP = 0.4
TURN_TAP_RELEASE_DAMP_REVERSE = 0.25


@dataclass
class StreetDriveState:
    drive_command: float = 0.0
    steering_target: float = STEERING_NEUTRAL_TRIM
    steering_command: float = STEERING_NEUTRAL_TRIM
    heading_hold_target: float | None = None
    steering_recovery_steps: int = 0
    turn_input_active: bool = False
    stability_blend: float = 1.0
    turn_press_steps: int = 0


# Mouse controls:
# - Press and hold left button then drag to rotate the camera/view
# - Press and hold right button then drag to pan/translate the view
def _is_key_pressed(input, key):
    return input.is_key_pressed(key.lower()) or input.is_key_pressed(key.upper())


def _clamp(value, lower, upper):
    return max(lower, min(upper, value))


def _approach(current, target, max_delta):
    delta = target - current
    if abs(delta) <= max_delta:
        return target
    return current + math.copysign(max_delta, delta)


def _angle_diff(target, current):
    return (target - current + math.pi) % (2 * math.pi) - math.pi


def _get_steering_joint_state(model, data):
    if model is None or data is None:
        return 0.0, 0.0

    steering_joint = model.get_joint(STEERING_JOINT)
    if steering_joint is None:
        return 0.0, 0.0

    steering_pos = float(np.array(steering_joint.get_dof_pos(data))[0])
    steering_vel = float(np.array(steering_joint.get_dof_vel(data))[0])
    return steering_pos, steering_vel


def _steering_is_settled(steering_pos, steering_vel):
    return abs(steering_pos) <= STEER_SETTLED_POS and abs(steering_vel) <= STEER_SETTLED_VEL


def get_vehicle_nose_axis(model, data):
    model.forward_kinematic(data)
    front_left = np.array(model.get_link("car_MFX_L_Wheel").get_position(data))[:2]
    front_right = np.array(model.get_link("car_MFX_R_Wheel").get_position(data))[:2]
    rear_left = np.array(model.get_link("car_NZL_Left_Wheel").get_position(data))[:2]
    rear_right = np.array(model.get_link("car_NZL_Right_Wheel").get_position(data))[:2]

    front_mid = 0.5 * (front_left + front_right)
    rear_mid = 0.5 * (rear_left + rear_right)
    nose_axis = front_mid - rear_mid
    return nose_axis / np.linalg.norm(nose_axis)


def get_vehicle_heading(model, data):
    nose_axis = get_vehicle_nose_axis(model, data)
    return math.atan2(nose_axis[1], nose_axis[0])


def get_vehicle_speed(model, data):
    return abs(get_vehicle_longitudinal_speed(model, data))


def get_vehicle_longitudinal_speed(model, data):
    car = model.get_link("car_CAR_CHA")
    velocity = np.array(car.get_linear_velocity(data))[:2]
    nose_axis = get_vehicle_nose_axis(model, data)
    return float(np.dot(velocity, nose_axis))


def _steer_speed_factor(speed):
    if speed <= HIGH_SPEED_MPS:
        normalized = _clamp(speed / HIGH_SPEED_MPS, 0.0, 1.0)
        return 1.0 - (1.0 - HIGH_SPEED_STEER_FACTOR) * normalized

    if speed >= VERY_HIGH_SPEED_MPS:
        return VERY_HIGH_SPEED_STEER_FACTOR

    normalized = (speed - HIGH_SPEED_MPS) / (VERY_HIGH_SPEED_MPS - HIGH_SPEED_MPS)
    return HIGH_SPEED_STEER_FACTOR + normalized * (VERY_HIGH_SPEED_STEER_FACTOR - HIGH_SPEED_STEER_FACTOR)


def _forward_drive_factor(speed):
    if speed <= FORWARD_SPEED_FADE_START_MPS:
        return 1.0
    if speed >= FORWARD_SPEED_LIMIT_MPS:
        return 0.0
    return (FORWARD_SPEED_LIMIT_MPS - speed) / (FORWARD_SPEED_LIMIT_MPS - FORWARD_SPEED_FADE_START_MPS)


def _reverse_drive_factor(speed):
    if speed <= REVERSE_STABILITY_FADE_START_MPS:
        return 1.0
    if speed >= REVERSE_STABILITY_FADE_END_MPS:
        return 0.0
    return (REVERSE_STABILITY_FADE_END_MPS - speed) / (
        REVERSE_STABILITY_FADE_END_MPS - REVERSE_STABILITY_FADE_START_MPS
    )


def _control_dt(model):
    if model is None:
        return CONTROL_REFERENCE_DT
    options = getattr(model, "options", None)
    if options is None:
        return CONTROL_REFERENCE_DT
    timestep = float(getattr(options, "timestep", CONTROL_REFERENCE_DT))
    return max(1e-4, timestep)


def _scale_step(step_value, dt):
    return step_value * (dt / CONTROL_REFERENCE_DT)


def _coerce_drive_state(controller_state, current_heading):
    if isinstance(controller_state, StreetDriveState):
        return controller_state

    state = StreetDriveState()
    if controller_state is not None:
        state.heading_hold_target = float(controller_state)
    else:
        state.heading_hold_target = current_heading
    return state


def get_keyboard_controls(input, model=None, data=None, controller_state=None):
    pressing_w = _is_key_pressed(input, "w")
    pressing_s = _is_key_pressed(input, "s")
    pressing_a = _is_key_pressed(input, "a")
    pressing_d = _is_key_pressed(input, "d")

    current_heading = None
    speed = 0.0
    longitudinal_speed = 0.0
    steering_pos = 0.0
    steering_vel = 0.0
    if model is not None and data is not None:
        current_heading = get_vehicle_heading(model, data)
        longitudinal_speed = get_vehicle_longitudinal_speed(model, data)
        speed = abs(longitudinal_speed)
        steering_pos, steering_vel = _get_steering_joint_state(model, data)
    dt = _control_dt(model)

    state = _coerce_drive_state(controller_state, current_heading)

    if pressing_w and not pressing_s:
        if longitudinal_speed < -BRAKE_RELEASE_SPEED_MPS or state.drive_command < 0.0:
            drive_target = BRAKE_CTRL
            ramp = BRAKE_RAMP
        else:
            drive_target = FORWARD_CTRL * _forward_drive_factor(speed)
            ramp = FORWARD_RAMP
    elif pressing_s and not pressing_w:
        if longitudinal_speed > BRAKE_RELEASE_SPEED_MPS or state.drive_command > 0.0:
            drive_target = -BRAKE_CTRL
            ramp = BRAKE_RAMP
        else:
            drive_target = -REVERSE_CTRL * _reverse_drive_factor(speed)
            ramp = REVERSE_RAMP
    else:
        drive_target = 0.0
        ramp = DRIVE_DECAY

    state.drive_command = _approach(state.drive_command, drive_target, ramp)

    steer_factor = _steer_speed_factor(speed)
    steer_limit = STEERING_CTRL * steer_factor
    steer_step = _scale_step(STEER_INPUT_STEP * steer_factor, dt)
    steer_return = max(_scale_step(0.02, dt), _scale_step(STEER_RETURN_STEP * steer_factor, dt))
    steer_response = max(_scale_step(0.02, dt), _scale_step(STEER_RESPONSE_STEP * steer_factor, dt))
    turn_input_active = False

    if pressing_a and not pressing_d:
        state.steering_target -= steer_step
        state.heading_hold_target = None
        turn_input_active = True
        state.turn_press_steps += 1
    elif pressing_d and not pressing_a:
        state.steering_target += steer_step
        state.heading_hold_target = None
        turn_input_active = True
        state.turn_press_steps += 1
    else:
        if state.turn_input_active:
            state.heading_hold_target = None
            state.steering_recovery_steps = HEADING_HOLD_RECOVERY_STEPS
            if state.turn_press_steps <= TURN_TAP_MAX_STEPS:
                tap_release_damp = TURN_TAP_RELEASE_DAMP_REVERSE if state.drive_command < 0.0 else TURN_TAP_RELEASE_DAMP
                # For brief taps, damp residual steering command quickly to reduce chassis shake.
                state.steering_command = STEERING_NEUTRAL_TRIM + tap_release_damp * (
                    state.steering_command - STEERING_NEUTRAL_TRIM
                )
                state.steering_target = STEERING_NEUTRAL_TRIM
        state.turn_press_steps = 0
        state.steering_target = _approach(state.steering_target, STEERING_NEUTRAL_TRIM, steer_return)
        if state.drive_command == 0.0:
            state.heading_hold_target = None
            state.steering_recovery_steps = 0
        elif (
            current_heading is not None
            and state.heading_hold_target is None
            and state.steering_recovery_steps == 0
            and abs(state.steering_target - STEERING_NEUTRAL_TRIM) < 0.02
            and abs(steering_pos - STEERING_NEUTRAL_TRIM) < 0.04
        ):
            state.heading_hold_target = current_heading

    state.steering_target = _clamp(state.steering_target, -steer_limit, steer_limit)
    state.steering_command = _approach(state.steering_command, state.steering_target, steer_response)
    state.turn_input_active = turn_input_active
    if turn_input_active:
        state.stability_blend = 0.0
    else:
        state.stability_blend = _approach(
            state.stability_blend,
            1.0,
            _scale_step(STABILITY_CORRECTION_BLEND_RATE, dt),
        )

    steering_value = state.steering_command
    correction_blend = state.stability_blend
    steering_recovery_active = not turn_input_active and state.drive_command > 0.0
    reverse_straight_active = not turn_input_active and state.drive_command < 0.0
    if steering_recovery_active or reverse_straight_active:
        steering_value += correction_blend * _clamp(
            -STEER_RECENTER_GAIN * (steering_pos - STEERING_NEUTRAL_TRIM) - STEER_RECENTER_DAMPING * steering_vel,
            -STEER_RECENTER_MAX,
            STEER_RECENTER_MAX,
        )
    if not turn_input_active and state.steering_recovery_steps > 0:
        if current_heading is not None and state.drive_command > 0.0:
            # Keep refreshing target during the recovery window to avoid locking onto stale turn headings.
            state.heading_hold_target = current_heading
        state.steering_recovery_steps -= 1

    if (
        state.drive_command > 0.0
        and not turn_input_active
        and current_heading is not None
        and state.heading_hold_target is not None
        and state.steering_recovery_steps == 0
    ):
        steering_value -= correction_blend * _clamp(
            HEADING_HOLD_GAIN * _angle_diff(state.heading_hold_target, current_heading),
            -HEADING_HOLD_MAX_CORRECTION,
            HEADING_HOLD_MAX_CORRECTION,
        )
    elif (
        state.drive_command < 0.0
        and not turn_input_active
        and current_heading is not None
        and state.heading_hold_target is not None
        and state.steering_recovery_steps == 0
        and _steering_is_settled(steering_pos, steering_vel)
    ):
        steering_value += correction_blend * _clamp(
            REVERSE_HEADING_HOLD_GAIN * _angle_diff(state.heading_hold_target, current_heading),
            -REVERSE_HEADING_HOLD_MAX_CORRECTION,
            REVERSE_HEADING_HOLD_MAX_CORRECTION,
        )

    steering_value = _clamp(steering_value, -steer_limit, steer_limit)
    return state.drive_command, steering_value, state


def stabilize_vehicle(model, data, steps=1000, steering_trim=STEERING_NEUTRAL_TRIM):
    forward = model.get_actuator("forward")
    steering = model.get_actuator("steering")

    for _ in range(steps):
        forward.set_ctrl(data, 0.0)
        steering.set_ctrl(data, steering_trim)
        step(model, data)


def main():
    path = os.path.abspath("examples/assets/car/world.xml")
    scene = msd.from_file(path)

    # Attach a follower camera and side wheel cameras to the car body
    camera_mjcf = """<mujoco model="camera">
  <worldbody>
    <camera name="follower" pos="8 0 4"
      xyaxes="0 -1 0 0 0 1" trackposspeed="8" trackrotspeed="2" />
    <camera name="front_wheel_side" pos="0 -1.5 0.3"
      xyaxes="1 0 0 0 0 1" fovy="60" />
    <camera name="rear_wheel_side" pos="2.7 -1.5 0.3"
      xyaxes="1 0 0 0 0 1" fovy="60" />
  </worldbody>
</mujoco>"""
    camera_msd = msd.from_str(camera_mjcf)
    scene.attach(camera_msd, "car_CAR_CHA")

    model = scene.build()

    camera = model.cameras["follower"]
    camera.rotation_track = "look_at_link"
    camera.position_track = "fixed_local"
    camera.track_target_link = model.get_link("car_CAR_CHA")

    front_wheel_cam = model.cameras["front_wheel_side"]
    front_wheel_cam.set_render_target("image", 320, 240)

    rear_wheel_cam = model.cameras["rear_wheel_side"]
    rear_wheel_cam.set_render_target("image", 320, 240)

    with RenderApp() as render:
        render.set_main_camera(camera)
        render.widgets.create_camera_viewport(
            front_wheel_cam,
            layout=Layout(right=10, bottom=10, width=320, height=240),
        )
        render.widgets.create_camera_viewport(
            rear_wheel_cam,
            layout=Layout(right=10, bottom=260, width=320, height=240),
        )
        render.launch(model)
        data = SceneData(model)

        forward = model.get_actuator("forward")
        steering = model.get_actuator("steering")
        stabilize_vehicle(model, data)
        render.sync(data)

        class KeyboardState:
            def __init__(self):
                self.pressed = set()

            def update(self, source):
                self.pressed = {key for key in ("w", "a", "s", "d") if _is_key_pressed(source, key)}

            def is_key_pressed(self, key):
                return key.lower() in self.pressed

        keyboard_state = KeyboardState()
        drive_state = None

        print("==========================")
        print("Press 'W' to move forward, 'S' to move backward,")
        print("Press 'A' to turn left, 'D' to turn right.")
        print("==========================")

        def phys_step():
            nonlocal drive_state
            forward_value, steering_value, drive_state = get_keyboard_controls(keyboard_state, model, data, drive_state)
            forward.set_ctrl(data, forward_value)
            steering.set_ctrl(data, steering_value)
            step(model, data)

        def render_step():
            render.sync(data)
            keyboard_state.update(render.input)

        run.render_loop(model.options.timestep, 60, phys_step, render_step)


if __name__ == "__main__":
    main()
