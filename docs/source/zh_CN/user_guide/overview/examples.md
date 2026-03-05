# 📚 示例程序

:::{tip}
模型和代码详见 [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) 仓库

在运行示例之前，请先参考 {doc}`../overview/environment_setup` 完成环境准备。
:::

我们提供了一系列示例程序帮助您从零开始掌握 MotrixSim 的使用方法。

**在所有平台上**（Linux、Windows、MacOS），您可以通过

```bash
uv run examples/{example_name}.py
```

来运行您感兴趣的示例

````{note}
**关于 MacOS (aarch64-apple-darwin) 平台的特别说明**：

- 如果示例使用了 {doc}`../main_function/render`，则需要使用：
  ```bash
  uv run mxpython examples/{example_name}.py
  ```

-   如果示例**不使用** `RenderApp`（仅进行物理仿真计算），则使用 `uv run` 即可，与其他平台一致

大多数需要可视化渲染的示例（如机械臂控制、机器人运动等）都会使用 RenderApp，需要使用 `uv run mxpython`。

````

## 基础入门

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![empty](/_static/images/examples/empty.png)
  - [`empty.py`](../../../../examples/empty.py)
  - 创建空场景，相当于 Hello World 示例。
* - ![falling_ball](/_static/images/examples/falling_ball.png)
  - [`falling_ball.py`](../../../../examples/falling_ball.py)
  - 小球在重力作用下下落，展示如何创建`model`与`data`。
```

## API 演示

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![actuator](/_static/images/examples/actuator.png)
  - [`actuator.py`](../../../../examples/actuator.py)
  - 获取和配置`actuator`的参数。
* - ![body](/_static/images/examples/body.png)
  - [`body.py`](../../../../examples/body.py)
  - `body`相关 API 的使用，这里的`body`特指根节点的 world body。
* - ![joint](/_static/images/examples/joint.png)
  - [`joint.py`](../../../../examples/joint.py)
  - `joint`相关 API 的使用，包括读写`dof_position`和`dof_velocity`。
* - ![link](/_static/images/examples/link.png)
  - [`link.py`](../../../../examples/link.py)
  - `link`相关 API 的使用。
* - ![model](/_static/images/examples/model.png)
  - [`model.py`](../../../../examples/model.py)
  - `model`相关 API 的使用，包括单模型多实例的场景。
* - ![options](/_static/images/examples/options.png)
  - [`options.py`](../../../../examples/options.py)
  - 使用`options`对模拟器进行参数配置。
* - ![site_and_sensor](/_static/images/examples/site_and_sensor.png)
  - [`site_and_sensor.py`](../../../../examples/site_and_sensor.py)
  - `site`和`sensor`相关 API 的使用。
* - ![friction](/_static/images/examples/friction.png)
  - [`friction.py`](../../../../examples/friction.py)
  - 摩擦力配置的场景。
* - ![parallelsim](/_static/images/examples/parallelsim.png)
  - [`parallelsim.py`](../../../../examples/parallelsim.py)
  - 多环境并行仿真。
* - ![inverse kinematics](/_static/images/examples/ik.png)
  - [`ik.py`](../../../../examples/ik.py)
  - 展示如何使用 MotrixSim 内置的 IK 模块进行逆运动学求解。
* - ![load_from_str](/_static/images/examples/load_from_str.jpg)
  - [`load_from_str.py`](../../../../examples/load_from_str.py)
  - 从字符串加载 MJCF 模型，展示如何直接从 XML 字符串创建场景。
* - ![combine_msd](/_static/images/examples/combine_msd.jpg)
  - [`combine_msd.py`](../../../../examples/combine_msd.py)
  - 组合多个 MSD 模型，展示如何使用 `Scene.attach()` 方法将多个模型附加到一起，支持变换和命名空间前缀。
* - ![geom](/_static/images/examples/geom.jpg)
  - [`geom.py`](../../../../examples/geom.py)
  - 几何体相关 API 的使用，展示如何访问和查询几何体的位置、速度等信息。
* - ![hfield](/_static/images/examples/hfield.jpg)
  - [`hfield.py`](../../../../examples/hfield.py)
  - 高度场 API 的使用，展示如何访问地形高度数据并进行统计分析。
* - ![camera_control](/_static/images/examples/change_camera_state.jpg)
  - [`camera_control.py`](../../../../examples/camera_control.py)
  - 相机控制 API 的使用，展示如何启用/禁用系统相机和场景相机，以及获取相机位姿。
* - ![custom_ui](/_static/images/examples/custom_ui.jpg)
  - [`custom_ui.py`](../../../../examples/custom_ui.py)
  - 自定义 UI 元素的使用，展示如何添加按钮和开关等交互控件。
```

## 交互控制

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![keyboard_car](/_static/images/examples/keyboard_car.png)
  - [`keyboard_car.py`](../../../../examples/keyboard_car.py)
  - 使用键盘操控小车移动，展示键盘事件的使用。使用 W 键向前移动，S 键向后移动。
转向：使用 A 键向左转，D 键向右转
* - ![mouse_click](/_static/images/examples/mouse_click.png)
  - [`mouse_click.py`](../../../../examples/mouse_click.py)
  - 使用鼠标点击地面移动小球，展示鼠标事件的使用。
* - ![gizmos](/_static/images/examples/gizmos.jpg)
  - [`gizmos.py`](../../../../examples/gizmos.py)
  - 3D 辅助绘图系统的使用，展示如何绘制球体、立方体、胶囊体、箭头、网格等可视化辅助元素。
```

## 物理仿真

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![gyroscope](/_static/images/examples/gyroscope.png)
  - [`gyroscope.py`](../../../../examples/gyroscope.py)
  - 陀螺的物理仿真场景。
* - ![gyroscope_zero_gravity](/_static/images/examples/gyroscope_zero_gravity.png)
  - [`gyroscope_zero_gravity.py`](../../../../examples/gyroscope_zero_gravity.py)
  - 零重力环境下的陀螺场景，展示角动量守恒的物理特性。
* - ![newton_cradle](/_static/images/examples/newton_cradle.png)
  - [`newton_cradle.py`](../../../../examples/newton_cradle.py)
  - 牛顿摆的物理仿真场景。
* - ![slope](/_static/images/examples/slope.png)
  - [`slope.py`](../../../../examples/slope.py)
  - 方块在斜坡上滚动的物理仿真模型。
* - ![local_arm](/_static/images/examples/local_arm.png)
  - [`local_arm.py`](../../../../examples/local_arm.py)
  - 由简单几何形状和`joint`组成的机械臂。
* - ![adhesion](/_static/images/examples/adhesion.png)
  - [`adhesion.py`](../../../../examples/adhesion.py)
  - 使用吸附功能的机械臂。
```

## 机器人应用

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![go1](/_static/images/poster/go1.jpg)
  - [`go1.py`](../../../../examples/go1.py)
  - go1 机械狗的随机运动，展示如何引入神经网络和使用`.onnx`文件。
* - ![go2](/_static/images/poster/go2_keyboard_control.jpg)
  - [`robot_locomotion.py`](../../../../examples/robot_locomotion.py)
  - go2 机械狗的键盘控制示例，方向键和wasd控制机械狗行走与转向。使用 `uv run examples/robot_locomotion.py --robot go2` 运行该示例。
* - ![g1](/_static/images/poster/g1_keyboard_control.jpg)
  - [`robot_locomotion.py`](../../../../examples/robot_locomotion.py)
  - g1 人形机器人的键盘控制示例，方向键和wasd控制机器人行走与转向。使用 `uv run examples/robot_locomotion.py --robot g1` 运行该示例。
* - ![g1_parlour](/_static/images/poster/g1_parlour.jpg)
  - [`robot_locomotion.py`](../../../../examples/robot_locomotion.py)
  - g1 人形机器人在室内客厅场景的键盘控制示例，方向键和wasd控制机器人行走与转向。使用 `uv run examples/robot_locomotion.py --robot g1 --scene parlour` 运行该示例。
* - ![robotic_arm](/_static/images/examples/robotic_arm.png)
  - [`robotic_arm.py`](../../../../examples/robotic_arm.py)
  - 斯坦福机械臂使用移动命令序列进行小球的抓取与摆放。
* - ![grasp_shaking_test](/_static/images/examples/grasp_shaking_test.jpg)
  - [`grasp_shaking_test.py`](../../../../examples/grasp_shaking_test.py)
  - Franka Panda 机械臂的抓取与抖动测试，展示机械臂如何抓取物体并保持稳定。支持 `--object` 参数选择物体类型（cube/ball/bottle），`--shake` 参数控制是否抖动，`--record` 参数录制视频。
```

## 渲染与可视化

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![render_settings](/_static/images/examples/render_settings.jpg)
  - [`render_settings.py`](../../../../examples/render_settings.py)
  - 渲染设置配置示例，展示如何使用 `RenderSettings` 配置阴影、屏幕空间环境光遮蔽（SSAO）等渲染效果。
* - ![partial_rendering](/_static/images/examples/partial_rendering.jpg)
  - [`partial_rendering.py`](../../../../examples/partial_rendering.py)
  - 批量渲染中的选择性渲染控制，展示如何在多环境并行仿真中动态控制特定场景的可见性。按 A/D 键切换部分场景可见性，Q/E 键控制所有场景。
* - ![share_lights_between_envs](/_static/images/examples/share_lights_between_envs.jpg)
  - [`share_lights_between_envs.py`](../../../../examples/share_lights_between_envs.py)
  - 多环境间的光源共享优化，展示如何在并行仿真中共享光源以提升性能。使用 `--share_lights=False` 参数可禁用光源共享。
```
