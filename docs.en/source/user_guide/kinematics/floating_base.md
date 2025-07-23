# 🛸 浮动基（FloatingBase）

在 [Body](body.md) 中，我们介绍了 Body 与 World 有三种连接方式，分别是：

-   固定连接（Fixed）
-   关节连接（Joint）
-   自由移动（FloatingBase）

自由移动的 Body，我们认为它的基座是浮动的，因而它拥有一个浮动基（FloatingBase）对象。FloatingBase 拥有 3 位移自由度和 3 旋转自由度。 通过 floatingbase 对象，MotrixSim 提供了一些额外的功能和属性，允许用户更方便地控制和获取浮动基的状态。

当我们对机器狗、或者人形机器人进行仿真时，他们通常都拥有浮动基。

## MJCF 映射

在 MJCF 中，如果一个 `<body>` 元素下有 `<freejoint>` 元素，则 MotrixSim 会自动将其解析为一个浮动基（FloatingBase）对象。 关于 MJCF 中 `<freejoint>` 的介绍，请参考官方文档：
[freejoint](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-freejoint)

## 访问 FloatingBase

一般来说，您可以通过以下方式访问 FloatingBase 对象：

```python
# 获取 Body 对象
cube = model.get_body('free_cube')
fb = cube.floatingbase
if fb is not None:
    # This body has a floating base
    # call some methods or properties on fb
    print(fb.get_translation(data))  # get position in global frame
    print(fb.set_translation(data, [1.0, 2.0, 3.0]))  # set position in global frame
```

```{note}
FloatingBase 对象拥有普通的 Joint 没有的方法，例如它可以直接通过笛卡尔坐标系来设置位置、旋转、速度等，MotrixSim 会自动将参数从笛卡尔坐标系转换为广义坐标系，并更新到 [`data.dof_pos`] 以及 [`data.dof_vel`] 中。

需要注意的是，通过 [`floatingbase.set_translation`] 等方法设置位置、旋转、速度时，MotrixSim 只更新了 Data 中的 dof 数据， 对整个 link tree 的 kinematics 状态更新需要在用户调用`motrixsim.step`或者`motrixsim.forward`方法后才会进行

```

## API Reference

更多与 FloatingBase 相关的 API，请参考 [`FloatingBase API`]

[`FloatingBase API`]: motrixsim.FloatingBase
[`data.dof_pos`]: motrixsim.SceneData.dof_pos
[`data.dof_vel`]: motrixsim.SceneData.dof_vel
[`floatingbase.set_translation`]: motrixsim.FloatingBase.set_translation
[`motrixsim.step`]: motrixsim.step
[`motrixsim.forward`]: motrixsim.forward
