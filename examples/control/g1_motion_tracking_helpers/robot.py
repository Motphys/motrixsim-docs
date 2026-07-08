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

import numpy as np
from robot import RobotBase

from . import contract


class G1MotionTrackingRobot(RobotBase):
    """G1 state accessor aligned with motion-tracking playback defaults."""

    mjcf_path = str(contract.DEFAULT_ROBOT_PATH)
    base_link_name = "pelvis"

    _DEFAULT_ANGLES = np.zeros(29, dtype=np.float32)

    def local_linear_vel(self, data) -> np.ndarray:
        return self._model.get_sensor_value(contract.LOCAL_LINEAR_VELOCITY_SENSOR, data)

    def gyro(self, data) -> np.ndarray:
        return self._model.get_sensor_value(contract.GYRO_SENSOR, data)
