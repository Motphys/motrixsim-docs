# 📚 示例程序

:::{tip}
模型和代码详见 [MotrixSim Docs](https://github.com/Motphys/motrixsim-docs) 仓库

在运行示例之前，请先参考 {doc}`../overview/environment_setup` 完成环境准备。
:::

我们提供了一系列示例程序帮助您从零开始掌握 MotrixSim 的使用方法。您可以通过

```bash
pdm run examples/{example_name}.py
```

来运行您感兴趣的示例

## 基础入门

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![empty](../../_static/images/examples/empty.png)
  - [`empty.py`](../../../../examples/empty.py)
  - 创建空场景，相当于 Hello World 示例。
* - ![falling_ball](../../_static/images/examples/falling_ball.png)
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
* - ![actuator](../../_static/images/examples/actuator.png)
  - [`actuator.py`](../../../../examples/actuator.py)
  - 获取和配置`actuator`的参数。
* - ![body](../../_static/images/examples/body.png)
  - [`body.py`](../../../../examples/body.py)
  - `body`相关 API 的使用，这里的`body`特指根节点的 world body。
* - ![joint](../../_static/images/examples/joint.png)
  - [`joint.py`](../../../../examples/joint.py)
  - `joint`相关 API 的使用，包括读写`dof_position`和`dof_velocity`。
* - ![link](../../_static/images/examples/link.png)
  - [`link.py`](../../../../examples/link.py)
  - `link`相关 API 的使用。
* - ![model](../../_static/images/examples/model.png)
  - [`model.py`](../../../../examples/model.py)
  - `model`相关 API 的使用，包括单模型多实例的场景。
* - ![option](../../_static/images/examples/option.png)
  - [`options.py`](../../../../examples/options.py)
  - 使用`options`对模拟器进行参数配置。
* - ![site_and_sensor](../../_static/images/examples/site_and_sensor.png)
  - [`site_and_sensor.py`](../../../../examples/site_and_sensor.py)
  - `site`和`sensor`相关 API 的使用。
* - ![friction](../../_static/images/examples/friction.png)
  - [`friction.py`](../../../../examples/friction.py)
  - 摩擦力配置的场景。
```

## 交互控制

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![read_keyboard](../../_static/images/examples/read_keyboard.png)
  - [`read_keyboard.py`](../../../../examples/read_keyboard.py)
  - 使用键盘操控小车移动，展示键盘事件的使用。使用 W 键向前移动，S 键向后移动。
转向：使用 A 键向左转，D 键向右转
* - ![mouse_click](../../_static/images/examples/mouse_click.png)
  - [`mouse_click.py`](../../../../examples/mouse_click.py)
  - 使用鼠标点击地面移动小球，展示鼠标事件的使用。
```

## 物理仿真

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![gyroscope](../../_static/images/examples/gyroscope.png)
  - [`gyroscope.py`](../../../../examples/gyroscope.py)
  - 陀螺的物理仿真场景。
* - ![gyroscope_zero_gravity](../../_static/images/examples/gyroscope_zero_gravity.png)
  - [`gyroscope_zero_gravity.py`](../../../../examples/gyroscope_zero_gravity.py)
  - 零重力环境下的陀螺场景，展示角动量守恒的物理特性。
* - ![newton_cradle](../../_static/images/examples/newton_cradle.png)
  - [`newton_cradle.py`](../../../../examples/newton_cradle.py)
  - 牛顿摆的物理仿真场景。
* - ![slope](../../_static/images/examples/slope.png)
  - [`slope.py`](../../../../examples/slope.py)
  - 方块在斜坡上滚动的物理仿真模型。
* - ![local_arm](../../_static/images/examples/local_arm.png)
  - [`local_arm.py`](../../../../examples/local_arm.py)
  - 由简单几何形状和`joint`组成的机械臂。
```

## 机器人应用

```{list-table}
:header-rows: 1
:class: longtable
:widths: 30 30 40

* - **展示**
  - **文件**
  - **简介**
* - ![go1](../../_static/images/examples/go1.png)
  - [`go1.py`](../../../../examples/go1.py)
  - go1 机械狗的随机运动，展示如何引入神经网络和使用`.onnx`文件。
* - ![robotic_arm](../../_static/images/examples/robotic_arm.png)
  - [`robotic_arm.py`](../../../../examples/robotic_arm.py)
  - 斯坦福机械臂使用移动命令序列进行小球的抓取与摆放。
```
