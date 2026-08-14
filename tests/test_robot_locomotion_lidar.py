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

import sys
from pathlib import Path

import pytest

from motrixsim import SceneData, msd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))

from control.robot_locomotion import (
    LIDAR_PROFILE_RATES,
    ROBOT_LIDAR_MOUNTS,
    attach_robot_lidar,
    create_argument_parser,
    load_robot_lidar,
)
from utils.robot import G1Robot, G1Robot12Dof, Go1Robot, Go2Robot


def test_robot_locomotion_defaults():
    args = create_argument_parser().parse_args([])
    assert args.scene == "playground"
    assert args.lidar is None
    assert not args.list_lidars


def test_all_catalog_lidar_profiles_compile():
    assert len(LIDAR_PROFILE_RATES) == 36
    for profile, expected_hz in LIDAR_PROFILE_RATES.items():
        world = load_robot_lidar(Go2Robot, profile)
        assert len(world.sensors.lidar) == 1
        lidar = world.sensors.lidar[0]
        assert lidar.name == "go2_lidar"
        assert lidar.site == "go2_lidar_site"
        assert lidar.hz == expected_hz


@pytest.mark.parametrize("robot_class", [G1Robot, G1Robot12Dof, Go1Robot, Go2Robot])
def test_selected_lidar_profile_builds_with_supported_robot(robot_class):
    mount = ROBOT_LIDAR_MOUNTS[robot_class]
    robot = msd.from_file(robot_class.mjcf_path)
    attach_robot_lidar(robot, robot_class, "ouster_os1_rev6_32ch_10hz_512res")
    assert robot.sensors.lidar[-1].hz == 10.0
    model = robot.build()
    data = SceneData(model)
    assert model.get_sensor_value(f"{mount['name']}_lidar", data).size > 0
