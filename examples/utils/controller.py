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

from abc import ABC, abstractmethod

import numpy as np
import onnxruntime as ort


class BaseController(ABC):
    """Base class for controllers."""

    @abstractmethod
    def get_actions(self, obs: np.ndarray) -> np.ndarray:
        """Get actions given observations."""
        pass


class OnnxController(BaseController):
    """Controller that uses an ONNX model to compute actions.

    Note:
        This controller loads an ONNX model and uses it to compute actions
        from observations. It uses CPU execution provider by default.
    """

    def __init__(self, onnx_model_path: str):
        """Initialize ONNX controller.

        Args:
            onnx_model_path: Path to the ONNX model file
        """
        self._policy = ort.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])
        self._input_name = self._policy.get_inputs()[0].name
        self._output_name = self._policy.get_outputs()[0].name

    def get_actions(self, obs: np.ndarray) -> np.ndarray:
        """Get actions given observations.

        Args:
            obs: Observation vector

        Returns:
            Action vector
        """
        outputs = self._policy.run([self._output_name], {self._input_name: obs.reshape(1, -1)})
        actions = outputs[0][0]
        return actions

    # Alias for consistency with plan
    get_action = get_actions


class KeyboardCommandAdapter:
    """Adapter to convert keyboard input to command signals.

    Note:
        This class maps keyboard input to raw robot velocity commands:
        - command[0]: forward/backward (x-axis, raw value in [-1, 1])
        - command[1]: left/right (y-axis, raw value in [-0.5, 0.5])
        - command[2]: angular velocity (yaw, raw value in [-2, 2])

        The raw values should be scaled by the policy before use.

    Example:
        >>> adapter = KeyboardCommandAdapter()
        >>> adapter.update_from_input(render.input)
        >>> print(adapter.command)  # [x, y, yaw] raw values
    """

    def __init__(self):
        """Initialize keyboard command adapter."""
        self.command = np.zeros(3, dtype=np.float32)

    def update_from_input(self, input) -> None:
        """Update command based on keyboard input state.

        Note:
            Key mappings (raw values):
            - W/Up Arrow: forward (x=1.0)
            - S/Down Arrow: backward (x=-1.0)
            - Left Arrow: left (y=0.5)
            - Right Arrow: right (y=-0.5)
            - A: rotate left (yaw=2.0)
            - D: rotate right (yaw=-2.0)

        Args:
            input: Input object from render.input (is_key_pressed method)
        """
        # Forward/backward (x-axis) - raw values
        if input.is_key_pressed("up") or input.is_key_pressed("w"):
            self.command[0] = 1.0
        elif input.is_key_pressed("down") or input.is_key_pressed("s"):
            self.command[0] = -1.0
        else:
            self.command[0] = 0.0

        # Left/right (y-axis) - raw values
        if input.is_key_pressed("left"):
            self.command[1] = 0.5
        elif input.is_key_pressed("right"):
            self.command[1] = -0.5
        else:
            self.command[1] = 0.0

        # Rotation (yaw) - raw values
        if input.is_key_pressed("a"):
            self.command[2] = 2.0
        elif input.is_key_pressed("d"):
            self.command[2] = -2.0
        else:
            self.command[2] = 0.0
