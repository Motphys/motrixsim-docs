# 🔷 几何体（Geometry）

几何体决定了场景中物体的外观和碰撞属性。几何体可以添加在`<body>`或`<worldbody>`下，或者用于配置 default 的相关属性。 [MJCF 几何体标签可配置属性](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-geom)

## 几何体类型

目前支持的几何体类型如下:
| 类型 | 说明 |
| :-----------------| :------------------------------------------------------------------- |
| 平面（`plane`） | 无限平面，分割整个场景，只能配置在`worldbody`或者静态的`body`下，平面本地坐标系下的 Z 轴为法线方向，平面下方（-Z 方向）为发生碰撞的区域。`size`参数的前两位用于绘制平面的示意，不改变碰撞体积。 |
| 高度场（`hfield`） | 需要引用对应的`hfield`标签下的资产，无需配置`size`属性，具体用例可参考[`examples/assets/hfield.xml`](../../../../examples/assets/hfield.xml) |
| 球体（`sphere`） | `size`属性只有 1 位，定义球的半径 |
| 胶囊体（`capsule`） | 胶囊体可以看做由两个半球和一个圆柱体组成，`size`由半球的半径和圆柱体的半高组成。 |
| 圆柱体（`cylinder`） | `size`由圆形的半径，和圆柱体的半高组成。 |
| 立方体（`box`） | `size`由 X, Y, Z 三个方向上的半长组成。 |
| 多面体（`mesh`） | 需要引用对应的`mesh`标签下的资产，无需配置`size`属性, 用例可参考[`examples/assets/boston_dynamics_spot/spot.xml`](../../../../examples/assets/boston_dynamics_spot/spot.xml)中对`mesh`的配置。 |

## 主要接口

在 MotrixSim 中，您可以通过以下方式访问 Geom 对象：

-   [`model.num_geoms`]: 获取当前世界中的 Geom 数量。
-   [`model.geoms`]: 获取当前世界中的所有 Geom 对象。
-   [`model.get_geom(key)`]: 根据名称或索引获取特定的 Geom 对象。

当您获取到一个 Geom 对象后，可以读取相关的位置，姿态，速度等信息，具体的 API 请参考 [`Geom API`]。

## 例子

您可以通过

```bash
pdm run examples/geom.py
```

来运行一个简单的关于 geom api 调用的例子。

源码可以参考 [`examples/geom.py`](../../../../examples/geom.py)。

[`model.num_geoms`]: motrixsim.SceneModel.num_geoms
[`model.geoms`]: motrixsim.SceneModel.geoms
[`model.get_geom(key)`]: motrixsim.SceneModel.get_geom
[`Geom API`]: motrixsim.Geom
