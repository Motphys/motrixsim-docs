# 📚 示例程序

:::{tip}
模型和代码详见 [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) 仓库

在运行示例之前，请先参考 {doc}`../overview/environment_setup` 完成环境准备。
:::

我们提供了一系列示例程序帮助您从零开始掌握 MotrixSim 的使用方法。

**在所有平台上**（Linux、Windows、MacOS），您可以通过

```bash
uv run examples/{category}/{example_name}.py
```

来运行您感兴趣的示例

````{note}
**关于 MacOS (aarch64-apple-darwin) 平台的特别说明**：

- 如果示例使用了 {doc}`../main_function/render`，则需要使用：
  ```bash
  uv run mxpython examples/{category}/{example_name}.py
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
  - [`empty.py`](../../../../examples/getting_started/empty.py)
  - 创建空场景，相当于 Hello World 示例。
* - ![falling_ball](/_static/images/examples/falling_ball.png)
  - [`falling_ball.py`](../../../../examples/getting_started/falling_ball.py)
  - 小球在重力作用下下落，展示如何创建`model`与`data`。
* - ![load_from_str](/_static/images/examples/load_from_str.jpg)
  - [`load_from_str.py`](../../../../examples/getting_started/load_from_str.py)
  - 从字符串加载 MJCF 模型，展示如何直接从 XML 字符串创建场景。
* - ![slope](/_static/images/examples/slope.png)
  - [`slope.py`](../../../../examples/getting_started/slope.py)
  - 方块在斜坡上滚动的物理仿真模型。
```

## 物理仿真

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![actuator](/_static/images/examples/actuator.png)
  - [`actuator.py`](../../../../examples/physics/actuator.py)
  - 获取和配置`actuator`的参数。
* - ![body](/_static/images/examples/body.png)
  - [`body.py`](../../../../examples/physics/body.py)
  - `body`相关 API 的使用，这里的`body`特指根节点的 world body。
* - ![joint](/_static/images/examples/joint.png)
  - [`joint.py`](../../../../examples/physics/joint.py)
  - `joint`相关 API 的使用，包括读写`dof_position`和`dof_velocity`。
* - ![link](/_static/images/examples/link.png)
  - [`link.py`](../../../../examples/physics/link.py)
  - `link`相关 API 的使用。
* - ![model](/_static/images/examples/model.png)
  - [`model.py`](../../../../examples/physics/model.py)
  - `model`相关 API 的使用，包括单模型多实例的场景。
* - ![options](/_static/images/examples/options.png)
  - [`options.py`](../../../../examples/physics/options.py)
  - 使用`options`对模拟器进行参数配置。
* - ![site_and_sensor](/_static/images/examples/site_and_sensor.png)
  - [`site_and_sensor.py`](../../../../examples/physics/site_and_sensor.py)
  - `site`和`sensor`相关 API 的使用。
* - ![friction](/_static/images/examples/friction.png)
  - [`friction.py`](../../../../examples/physics/friction.py)
  - 摩擦力配置的场景。
* - ![geom](/_static/images/examples/geom.jpg)
  - [`geom.py`](../../../../examples/physics/geom.py)
  - 几何体相关 API 的使用，展示如何访问和查询几何体的位置、速度等信息。
* - ![hfield](/_static/images/examples/hfield.jpg)
  - [`hfield.py`](../../../../examples/physics/hfield.py)
  - 高度场 API 的使用，展示如何访问地形高度数据并进行统计分析。
* - ![combine_msd](/_static/images/examples/combine_msd.jpg)
  - [`combine_msd.py`](../../../../examples/physics/combine_msd.py)
  - 组合多个 MSD 模型，展示如何使用 `Scene.attach()` 方法将多个模型附加到一起，支持变换和命名空间前缀。
* - ![adhesion](/_static/images/examples/adhesion.png)
  - [`adhesion.py`](../../../../examples/physics/adhesion.py)
  - 使用吸附功能的机械臂。
* - ![external_force](/_static/images/examples/external_force.jpg)
  - [`external_force.py`](../../../../examples/physics/external_force.py)
  - 外力与外力矩施加示例，展示如何使用 `add_external_force` 和 `add_external_torque` API 在局部坐标系中对刚体施加力和力矩。包含质心推力、绕轴力矩、偏移点施力三个阶段的演示。
```

## 控制

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![keyboard_car](/_static/images/examples/keyboard_car.png)
  - [`keyboard_car.py`](../../../../examples/control/keyboard_car.py)
  - 使用键盘操控小车移动，展示键盘事件的使用。使用 W 键向前移动，S 键向后移动。转向：使用 A 键向左转，D 键向右转。
* - ![mouse_click](/_static/images/examples/mouse_click.png)
  - [`mouse_click.py`](../../../../examples/control/mouse_click.py)
  - 使用鼠标点击地面移动小球，展示鼠标事件的使用。
* - ![inverse kinematics](/_static/images/examples/ik.png)
  - [`ik.py`](../../../../examples/control/ik.py)
  - 展示如何使用 MotrixSim 内置的 IK 模块进行逆运动学求解。
* - ![local_arm](/_static/images/examples/local_arm.png)
  - [`local_arm.py`](../../../../examples/control/local_arm.py)
  - 由简单几何形状和`joint`组成的机械臂。
* - ![robotic_arm](/_static/images/examples/robotic_arm.png)
  - [`robotic_arm.py`](../../../../examples/control/robotic_arm.py)
  - 斯坦福机械臂使用移动命令序列进行小球的抓取与摆放。
* - ![go1](/_static/images/poster/go1.jpg)
  - [`go1.py`](../../../../examples/control/go1.py)
  - go1 机械狗的随机运动，展示如何引入神经网络和使用`.onnx`文件。
* - ![go2](/_static/images/poster/go2_keyboard_control.jpg)
  - [`robot_locomotion.py`](../../../../examples/control/robot_locomotion.py)
  - go2 机械狗的键盘控制示例，方向键和wasd控制机械狗行走与转向。使用 `uv run examples/control/robot_locomotion.py --robot go2` 运行该示例。
* - ![g1](/_static/images/poster/g1_keyboard_control.jpg)
  - [`robot_locomotion.py`](../../../../examples/control/robot_locomotion.py)
  - g1 人形机器人的键盘控制示例，方向键和wasd控制机器人行走与转向。使用 `uv run examples/control/robot_locomotion.py --robot g1` 运行该示例。
* - ![g1_motion_tracking](/_static/images/poster/g1_motion_tracking.png)
  - [`g1_motion_tracking.py`](../../../../examples/control/g1_motion_tracking.py)
  - g1 人形机器人的运动跟踪播放示例，加载内置 motion 参考轨迹和 ONNX actor 进行单环境播放。使用 `uv run examples/control/g1_motion_tracking.py` 运行该示例。
* - ![g1_parlour](/_static/images/poster/g1_parlour.jpg)
  - [`robot_locomotion.py`](../../../../examples/control/robot_locomotion.py)
  - g1 人形机器人在室内客厅场景的键盘控制示例，方向键和wasd控制机器人行走与转向。使用 `uv run examples/control/robot_locomotion.py --robot g1 --scene parlour` 运行该示例。
* - ![rm65_open_cabinet](/_static/images/examples/rm65_open_cabinet.png)
  - [`rm65_open_cabinet.py`](../../../../examples/control/rm65_open_cabinet.py)
  - RM65 开抽屉策略示例，展示如何加载 ONNX 策略并控制机械臂完成柜体抽屉操作。[演示视频](/_static/videos/rm65_open_cabinet.mp4)。按 `R` 重置，按 `ESC` 退出。
* - ![shadow_hand_repose](/_static/images/examples/shadow_hand_repose.jpg)
  - [`shadow_hand_repose.py`](../../../../examples/control/shadow_hand_repose.py)
  - Shadow Hand 方块重定向策略示例，展示如何加载 ONNX 策略并控制灵巧手调整方块姿态。[演示视频](/_static/videos/shadow_hand_repose.mp4)。按 `R` 重置，按 `ESC` 退出。
* - ![osc](/_static/images/examples/osc.jpg)
  - [`osc.py`](../../../../examples/control/osc.py)
  - 操作空间控制（OSC）交互示例，展示如何使用 `OscSolver` 配合 `IkChain` 通过计算力矩控制机械臂末端执行器的位置和姿态。方向键和 WASD 控制目标移动，Q/E 旋转，R 重置。
* - ![go1_multi_task](/_static/images/examples/go1_multi_task.jpg)
  - [`go1_multi_task.py`](../../../../examples/go1_multi_task.py)
  - Go1 机械狗多任务策略示例，支持行走、倒立、脚立、起身恢复等多种运动模式切换。WASD 控制移动，U 倒立，I 脚立，O 恢复，P 重置。
```

## 并行仿真

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![parallelsim](/_static/images/examples/parallelsim.png)
  - [`parallelsim.py`](../../../../examples/parallel/parallelsim.py)
  - 多环境并行仿真。
```

## 随机化

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![randomize_mass](/_static/images/examples/randomize_mass.jpg)
  - [`mass.py`](../../../../examples/randomize/mass.py)
  - 随机化刚体质量，在 16 个并行实例中将质量从 0.1 kg 到 500 kg 变化，展示质量对下落动力学的影响。
* - ![randomize_friction](/_static/images/examples/randomize_friction.jpg)
  - [`friction.py`](../../../../examples/randomize/friction.py)
  - 随机化几何体摩擦系数，在 0.01 到 2.0 范围内变化，展示物体在 30° 斜面上从滑动到静止的过渡。
* - ![randomize_armature](/_static/images/examples/randomize_armature.jpg)
  - [`armature.py`](../../../../examples/randomize/armature.py)
  - 随机化关节转动惯量（虚拟转子惯量），展示 armature 参数对扭转弹簧驱动臂的固有频率的影响。
* - ![randomize_frictionloss](/_static/images/examples/randomize_frictionloss.jpg)
  - [`frictionloss.py`](../../../../examples/randomize/frictionloss.py)
  - 随机化关节干摩擦力（库仑摩擦），从 0 到 200 N·m 变化，展示摩擦力如何使摆锤在不同角度停止。
* - ![randomize_com](/_static/images/examples/randomize_com.jpg)
  - [`com.py`](../../../../examples/randomize/com.py)
  - 随机化质心位置，在圆柱体截面内偏移质心，展示质心偏移对滚动行为的影响。
* - ![randomize_actuator_kp_kd](/_static/images/examples/randomize_actuator_kp_kd.jpg)
  - [`actuator_kp_kd.py`](../../../../examples/randomize/actuator_kp_kd.py)
  - 在 4×4 网格中随机化位置执行器的 PD 增益，行方向变化 kp（10–120 N·m/rad），列方向变化 kd（1–20 N·m·s/rad），可视化 PD 伺服动力学。
* - ![randomize_geom_size](/_static/images/examples/randomize_geom_size.jpg)
  - [`geom_size.py`](../../../../examples/randomize/geom_size.py)
  - 随机化五种几何体（球体、胶囊体、盒体、圆柱体、椭球体）的碰撞和视觉尺寸，展示尺寸对沉降高度和接触行为的影响。
* - ![randomize_gravity_direction](/_static/images/examples/randomize_gravity_direction.jpg)
  - [`gravity_direction.py`](../../../../examples/randomize/gravity_direction.py)
  - 随机化重力方向，在 16 个并行实例的透明盒子中为每个实例设置不同的重力向量，展示 `set_gravity_override` 的逐实例重力覆盖能力。
```

## 可视化与渲染

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![camera_control](/_static/images/examples/change_camera_state.jpg)
  - [`camera_control.py`](../../../../examples/viewer/camera_control.py)
  - 相机控制 API 的使用，展示如何启用/禁用系统相机和场景相机，以及获取相机位姿。
* - ![camera_viewport](/_static/images/examples/camera_viewport.png)
  - [`camera_viewport.py`](../../../../examples/viewer/camera_viewport.py)
  - 相机视口组件的使用，展示不同相机画面的显示，以及切换相机、调整大小和位置等交互控制。
* - ![custom_ui](/_static/images/examples/custom_ui.jpg)
  - [`custom_ui.py`](../../../../examples/viewer/custom_ui.py)
  - 自定义 UI 元素的使用，展示如何添加按钮和开关等交互控件。
* - ![gizmos](/_static/images/examples/gizmos.jpg)
  - [`gizmos.py`](../../../../examples/viewer/gizmos.py)
  - 3D 辅助绘图系统的使用，展示如何绘制球体、立方体、胶囊体、箭头、网格等可视化辅助元素。
* - ![image_widget](/_static/images/examples/image_widget.jpg)
  - [`image_widget.py`](../../../../examples/viewer/image_widget.py)
  - 图像组件系统的使用，展示如何显示和交互操作多个图像面板。
* - ![render_settings](/_static/images/examples/render_settings.jpg)
  - [`render_settings.py`](../../../../examples/viewer/render_settings.py)
  - 渲染设置配置示例，展示如何使用 `RenderSettings` 配置阴影、屏幕空间环境光遮蔽（SSAO）等渲染效果。
* - ![partial_rendering](/_static/images/examples/partial_rendering.jpg)
  - [`partial_rendering.py`](../../../../examples/viewer/partial_rendering.py)
  - 批量渲染中的选择性渲染控制，展示如何在多环境并行仿真中动态控制特定场景的可见性。按 A/D 键切换部分场景可见性，Q/E 键控制所有场景。
* - ![share_lights_between_envs](/_static/images/examples/share_lights_between_envs.jpg)
  - [`share_lights_between_envs.py`](../../../../examples/viewer/share_lights_between_envs.py)
  - 多环境间的光源共享优化，展示如何在并行仿真中共享光源以提升性能。使用 `--share_lights=False` 参数可禁用光源共享。
* - ![ssgi](/_static/images/poster/go2-ssgi.jpg)
  - [`ssgi.py`](../../../../examples/viewer/ssgi.py)
  - 屏幕空间全局光照（SSGI）渲染示例，展示如何使用 `RenderSettings` 启用高质量 SSGI 渲染效果。
* - ![headless](/_static/images/examples/empty.png)
  - [`headless.py`](../../../../examples/viewer/headless.py)
  - 无头渲染示例，展示如何使用 `RenderApp(headless=True)` 在无窗口模式下运行仿真并通过系统相机批量截取图像。支持 `--no-wait` 参数切换同步/异步捕获模式。
```

## 基准测试

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![gyroscope](/_static/images/examples/gyroscope.png)
  - [`gyroscope_mx.py`](../../../../examples/bench/gyroscope/gyroscope_mx.py)
  - 陀螺的物理仿真场景。
* - ![gyroscope_zero_gravity](/_static/images/examples/gyroscope_zero_gravity.png)
  - [`gyroscope_zero_gravity_mx.py`](../../../../examples/bench/gyroscope_zero_gravity/gyroscope_zero_gravity_mx.py)
  - 零重力环境下的陀螺场景，展示角动量守恒的物理特性。
* - ![newton_cradle](/_static/images/examples/newton_cradle.png)
  - [`newton_cradle_mx.py`](../../../../examples/bench/newton_cradle/newton_cradle_mx.py)
  - 牛顿摆的物理仿真场景。
* - ![grasp_shaking_test](/_static/images/examples/grasp_shaking_test.jpg)
  - [`shake_test_mx.py`](../../../../examples/bench/grasp/shake_test_mx.py)
  - Franka Panda 机械臂的抓取与抖动测试，展示机械臂如何抓取物体并保持稳定。支持 `--object` 参数选择物体类型（cube/ball/bottle），`--shake` 参数控制是否抖动，`--record` 参数录制视频。
```
