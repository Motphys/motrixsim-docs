# Lidar 传感器

MotrixSim 的 Lidar 是基于物理碰撞几何体执行批量 raycast 的多束测距传感器。它通过一个
site 确定安装位置和朝向，并输出世界坐标系中的点云，可用于机器人避障、地形感知、定位与
建图，以及强化学习观测。

```{video} /_static/videos/lidar_sensor.mp4
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

视频中的彩色线条和点展示了 Lidar 对地面、墙壁、球体、胶囊体以及机器人周围障碍物的实时
raycast 结果。点云可视化只用于显示，不参与传感器计算。

## 快速开始

一个 Lidar 由三部分组成：

1. `body/site` 定义安装坐标系；
2. `asset/lidar` 定义可复用的型号和扫描几何；
3. `sensor/lidar` 把一个传感器实例挂到 site，并引用 profile。

下面的配置创建一个 1024×64 的 360° Grid Lidar。省略 `hz` 表示每个 physics step 生成一帧
完整的静态快照。

```xml
<mujoco model="lidar_example">
  <asset>
    <lidar name="grid_64"
      cutoff="25"
      pattern="grid"
      hscan="1024" vscan="64"
      hrange="-180 180" vrange="-15 15"/>
  </asset>

  <worldbody>
    <body name="robot">
      <site name="lidar_site"
        pos="0.25 0 0.20"
        quat="0.5 0.5 0.5 0.5"
        size="0.01"/>
    </body>
  </worldbody>

  <sensor>
    <lidar name="roof_lidar"
      site="lidar_site"
      asset="grid_64"
      exclude="parentsubtree"/>
  </sensor>
</mujoco>
```

模型加载后，每次 `step()` 都会推进 Lidar。`get_sensor_value()` 返回扁平化的 point buffer；
Grid 的稳定布局是 `(hscan, vscan, 3)`。

```python
import numpy as np

from motrixsim import SceneData, load_model

HSCAN = 1024
VSCAN = 64

model = load_model("lidar_scene.xml")
data = SceneData(model)

model.step(data)
values = model.get_sensor_value("roof_lidar", data)
points = values.reshape(HSCAN, VSCAN, 3)

# 未命中的 point 是 (0, 0, 0)。
hit_mask = np.any(points != 0.0, axis=-1)
hit_points = points[hit_mask]
print(f"hits: {hit_points.shape[0]}")
```

## MJCF 参数总览

Lidar 的型号/扫描参数属于 `asset/lidar`，实例身份、挂载和运行时扫描频率属于
`sensor/lidar`。不要把 profile 参数写到 sensor 实例上。

### `asset/lidar`

| 参数         | 适用范围    | 默认值/约束                              | 说明                                       |
| ------------ | ----------- | ---------------------------------------- | ------------------------------------------ |
| `name`       | 全部        | 必填、全局唯一                           | profile 名称，供 `sensor/lidar.asset` 引用 |
| `cutoff`     | 全部        | 默认 `100`，正有限值                     | 最大测距，单位为米                         |
| `pattern`    | 全部        | 默认 `grid`；`grid` / `rings`            | 扫描几何类型                               |
| `hscan`      | Grid、Rings | 默认 `1`，正整数；与 `reportrate` 二选一 | 每个完整扫描的水平列数                     |
| `vscan`      | Grid        | 默认 `1`，正整数                         | 每列的垂直 beam 数                         |
| `hrange`     | Grid、Rings | 默认 `0 0`，两个有限值                   | 水平角起止值，单位为度                     |
| `vrange`     | Grid        | 默认 `0 0`，两个有限值                   | 垂直角起止值，单位为度                     |
| `elevations` | Rings       | 非空数组                                 | 每条 ring 的仰角表，单位为度               |
| `reportrate` | Grid、Rings | 可选、正有限值；需要 sensor 设置 `hz`    | 每秒水平列数，用于推导 `hscan`             |
| `hzrange`    | Grid、Rings | 可选，两个正有限值且非降序               | profile 支持的完整扫描频率范围             |

`Grid` 只能使用 `vscan`/`vrange`，`Rings` 只能使用 `elevations`。

### `sensor/lidar`

| 参数      | 默认值/约束                                 | 说明                                                 |
| --------- | ------------------------------------------- | ---------------------------------------------------- |
| `name`    | 可选                                        | 传感器名称；传给 `get_sensor_value()`                |
| `asset`   | 必填                                        | 引用一个 `asset/lidar.name`                          |
| `site`    | 必填                                        | 定义 ray 原点与局部坐标系的 site                     |
| `exclude` | 默认 `parentbody`                           | `none` / `parentbody` / `parentsubtree` 自身过滤策略 |
| `hz`      | 可选、正有限值，并满足 `1 / hz >= timestep` | 省略时每步完整快照；设置后启用帧内分摊               |

如果 profile 定义了 `hzrange`，sensor 的 `hz` 必须落在该闭区间内。

## 坐标系与输出布局

Lidar 使用 site 的局部坐标系：

-   `+Z`：前方；
-   `+X`：右方；
-   `+Y`：上方；
-   `hrange`：绕上方轴扫描的水平角范围，单位为度；
-   `vrange` / `elevations`：相对水平面的仰角，单位为度。

`Grid` 和 `Rings` 都按水平角优先排列，因此输出可以稳定 reshape：

| Pattern | 点云形状                      | 未命中值    | 坐标系     |
| ------- | ----------------------------- | ----------- | ---------- |
| Grid    | `(hscan, vscan, 3)`           | `(0, 0, 0)` | 世界坐标系 |
| Rings   | `(hscan, len(elevations), 3)` | `(0, 0, 0)` | 世界坐标系 |

批量环境会在最前面增加 batch 维度。不要用距离传感器的 `-1` 规则判断 high-level Lidar 的
未命中点；Lidar 固定发布 point，未命中 point 为零向量。

## 扫描 Pattern

### Grid

Grid 在水平角和垂直角上均匀采样，适合固态雷达近似、深度感知和快速搭建场景。

| 属性     | 含义               |
| -------- | ------------------ |
| `hscan`  | 每帧水平列数       |
| `vscan`  | 每列垂直 beam 数   |
| `hrange` | 水平角起止值       |
| `vrange` | 垂直角起止值       |
| `cutoff` | 最大测距，单位为米 |

### Rings

Rings 使用显式的逐线仰角表，适合 Velodyne、Ouster 等垂直线束不均匀的旋转式雷达。

```xml
<asset>
  <lidar name="rings_8"
    cutoff="100"
    pattern="rings"
    elevations="-15 1 -13 3 -11 5 -9 7"
    hscan="1800"
    hrange="-180 180"/>
</asset>
```

不同 pattern 的专用属性不能混用：Rings 使用 `elevations`，不使用 `vscan` 和 `vrange`。
完整字段定义见 {ref}`MJCF asset/lidar <asset-lidar>`。

## 静态快照与 `hz`

`sensor/lidar.hz` 控制扫描时序：

-   **省略 `hz`**：每个 physics step 发射完整 pattern，所有点使用同一个 site 位姿。这是无运动
    畸变的静态快照模式，也适合要求每步都有完整观测的 RL 场景。
-   **设置 `hz="10"`**：一帧在 `0.1s` 内分摊到多个 physics step。每一步只发射当前相位的
    beam，并用当步 site 位姿把命中点写入世界坐标系；周期结束后发布完整帧，因此移动载体会
    产生真实的扫描运动畸变。

```xml
<sensor>
  <lidar name="roof_lidar"
    site="lidar_site"
    asset="rotating_profile"
    hz="10"
    exclude="parentsubtree"/>
</sensor>
```

必须满足 `1 / hz >= physics timestep`。使用 `reportrate` 的 profile 时，实际水平列数按
`hscan = round(reportrate / hz)` 在模型构建阶段推导。

## 自身过滤

`exclude` 防止 Lidar 扫到自己的安装体或机器人：

| 值              | 行为                                                   |
| --------------- | ------------------------------------------------------ |
| `none`          | 不过滤任何自身 collider                                |
| `parentbody`    | 过滤 site 所在 body，默认值                            |
| `parentsubtree` | 过滤 site 所在 body 及其全部后代，推荐用于多连杆机器人 |

Lidar 只命中参与物理碰撞的 collider，不命中 visual-only geom。更改渲染材质不会改变测距结果。

## 使用内置真实型号 Profile

示例目录 `examples/assets/lidar-profiles/` 提供 HESAI XT32 和 Ouster OS0/OS1/OS2 的
starter profiles。入口文件 [`catalog.xml`](../../../../../examples/assets/lidar-profiles/catalog.xml)
可通过 MJCF `include` 引入，然后由 sensor 按名称引用：

```xml
<include file="lidar-profiles/catalog.xml"/>

<sensor>
  <lidar name="roof_lidar"
    site="lidar_site"
    asset="hesai_xt32_sd10"
    hz="10"
    exclude="parentsubtree"/>
</sensor>
```

include 路径相对于当前 MJCF 文件解析。完整挂载示例见
[`robot_locomotion.py`](../../../../../examples/control/robot_locomotion.py)。

## 点云可视化

渲染器默认不传输 Lidar 点云。调试时调用 `set_lidar_point_vis(True)` 显式开启：

```python
from motrixsim.render import RenderApp

with RenderApp() as render:
    render.launch(model)
    render.opt.set_lidar_point_vis(True)

    while not render.is_closed:
        model.step(data)
        render.sync(data)
```

完整的程序化场景和可视化代码见
[`lidar_point_cloud_demo.py`](../../../../../examples/sensors/lidar_point_cloud_demo.py)。该示例同场展示
60° × 20° 的 Solid State 风格静态 Grid，以及采用显式 16 线仰角表、360°、10 Hz 帧内分摊的
旋转 Rings Lidar；两个 Lidar 均使用脚本内嵌 MJCF 配置，后者的安装体会运动，以展示扫描运动畸变。

## 性能参考

下图是 playground 场景中的端到端 Python benchmark。每个 Lidar 使用 1024×64 Grid，省略
`hz`，因此每个 step 发射 65,536 条 ray。测试逐次调用 `model.step()`，不包含模型加载、构建
和渲染；环境为 32 个逻辑 CPU、Rayon 自动线程数，结果取 3 轮中位数。

```{figure} /_static/images/lidar_raycast_benchmark.svg
:alt: 三种 Lidar 规模场景的 raycast 吞吐柱状图
:width: 100%

Lidar 端到端 raycast 吞吐
```

| 场景                       | 总 ray/step |          中位吞吐 | 墙钟耗时/step |
| -------------------------- | ----------: | ----------------: | ------------: |
| 1 环境 × 1 Lidar           |      65,536 | 63.495 Mraycast/s |      1.032 ms |
| 1 环境 × 128 Lidar         |   8,388,608 | 78.324 Mraycast/s |    107.102 ms |
| 1024 环境 × 每环境 1 Lidar |  67,108,864 | 80.656 Mraycast/s |    832.036 ms |

吞吐按下式计算：

```text
总 ray 数 = hscan × vscan × lidar 数 × 环境数 × 计时 step 数
吞吐 = 总 ray 数 / 墙钟耗时
```

`80.656 Mraycast/s` 表示所有环境合计约每秒 8,065.6 万次 raycast。该数字包含完整 physics
pipeline 的耗时，是用户调用 `step()` 时的端到端吞吐，不是孤立 raycast kernel 的峰值。

复现 benchmark：

```bash
cd motrixsim-python/motrixsim-docs
uv run python examples/bench/lidar.py --case all
```
