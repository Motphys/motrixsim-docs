# 接触传感器（Contact Sensor）

接触传感器用于检测和报告两个物体（或几何体）之间的接触信息，包括接触点位置、接触力、法向量等详细数据。在机器人仿真中，接触传感器常用于足端触地检测、抓取力反馈、碰撞检测等应用场景。

## 🎯 功能描述

接触传感器监测指定的几何体对或物体对之间的接触事件，并返回详细的接触信息。该传感器可以配置返回不同类型的数据，包括接触状态、接触力、接触位置、法向量等。

## 📋 返回值格式

```python
contact_data = model.get_sensor_value("contact_sensor_name", data)
# 类型：numpy.ndarray[float32]
```

## ⚙️ MJCF 配置参数

在 MotrixSim 中，接触传感器支持以下 MJCF 配置：

### 基本配置格式

```xml
<sensor>
    <contact name="sensor_name"
             geom1="geom1_name"
             geom2="geom2_name"
             data="found force pos normal tangent"
             num="4"
             reduce="none"
           />
</sensor>
```

### 支持的属性

| 属性名       | 类型   | 必需 | 默认值  | 描述                                   |
| ------------ | ------ | ---- | ------- | -------------------------------------- |
| **name**     | string | ✅   | -       | 传感器的唯一标识名称                   |
| **geom1**    | string | ❌   | -       | 第一个几何体名称（与 geom2 配对使用）  |
| **geom2**    | string | ❌   | -       | 第二个几何体名称（与 geom1 配对使用）  |
| **body1**    | string | ❌   | -       | 第一个物体名称（与 body2 配对使用）    |
| **body2**    | string | ❌   | -       | 第二个物体名称（与 body1 配对使用）    |
| **subtree1** | string | ❌   | -       | 第一个子树名称（与 subtree2 配对使用） |
| **subtree2** | string | ❌   | -       | 第二个子树名称（与 subtree1 配对使用） |
| **site**     | string | ❌   | -       | 参考点名称                             |
| **data**     | string | ❌   | "found" | 返回的数据类型，用空格分隔             |
| **num**      | int    | ❌   | 1       | 最大报告接触点数量                     |
| **reduce**   | string | ❌   | "none"  | 数据约简方式                           |

### 目标对象配置（四种方式）

#### 1. 几何体对（推荐）

```xml
<contact name="floor_contact" geom1="bar" geom2="freebox"/>
```

#### 2. 物体对

```xml
<contact name="body_contact" body1="body1_name" body2="body2_name"/>
```

#### 3. 子树对

```xml
<contact name="subtree_contact" subtree1="subtree1_name" subtree2="subtree2_name"/>
```

#### 4. Site 点

```xml
<contact name="site_contact" site="site_name"/>
```

### 数据类型（data 属性）

可组合使用以下值：

| 值          | 描述                        | 数据占用        |
| ----------- | --------------------------- | --------------- |
| **found**   | 接触点数量                  | 1 个值          |
| **force**   | 接触力投影（法向 + 2 切向） | 每接触点 3 个值 |
| **torque**  | 接触力矩                    | 每接触点 3 个值 |
| **dist**    | 穿透深度                    | 每接触点 1 个值 |
| **pos**     | 接触点位置                  | 每接触点 3 个值 |
| **normal**  | 法向量                      | 每接触点 3 个值 |
| **tangent** | 第一切向量                  | 每接触点 3 个值 |

### 数据约简方式（reduce 属性）

| 值           | 描述                              |
| ------------ | --------------------------------- |
| **none**     | 返回所有接触点数据（最多 num 个） |
| **mindist**  | 只返回距离最近的接触点            |
| **maxforce** | 只返回接触力最大的接触点          |
| **netforce** | 返回所有接触点的合力（简化格式）  |

## 📐 返回数组长度与内容布局

接触传感器返回的数组长度和内容布局取决于三个关键配置参数：`data` 属性（指定数据类型）、`num` 属性（最大接触点数量）和 `reduce` 属性（数据约简方式）。

### 数组长度计算公式

```python
total_size = 1 + max_num_contacts × values_per_contact
```

-   **1**: `found` 字段，表示实际接触点数量
-   **max_num_contacts**: MJCF 配置中 `num` 参数设定的最大接触点数量（数组固定大小）
-   **values_per_contact**: 每个接触点的数据值数量（取决于 `data` 配置）

**重要**：数组大小固定，不受实际接触点数量影响。如果实际接触点少于 `max_num_contacts`，剩余位置用 0 填充。

### data 属性对每接触点数据量的影响

不同的 `data` 类型组合会产生不同的 `values_per_contact`：

| data 配置                          | 每接触点值数量 | 数据布局（按顺序）                                   |
| ---------------------------------- | -------------- | ---------------------------------------------------- |
| `"found"`                          | 0              | 仅接触状态                                           |
| `"found force"`                    | 3              | [法向力, 切向 0 力, 切向 1 力]                       |
| `"found force pos"`                | 6              | [3 个力分量, 3 个位置坐标]                           |
| `"found force pos normal"`         | 9              | [3 个力分量, 3 个位置坐标, 3 个法向量]               |
| `"found force pos normal tangent"` | 12             | [3 个力分量, 3 个位置坐标, 3 个法向量, 3 个切向量 0] |
| `"found pos normal"`               | 6              | [3 个位置坐标, 3 个法向量]                           |
| `"found force torque"`             | 6              | [3 个力分量, 3 个力矩分量]                           |

**注意**：每个数据类型的占用空间：

-   `found`: 1 个值（所有配置都包含）
-   `force`: 3 个值（法向 + 2 个切向力投影）
-   `torque`: 3 个值（接触力矩）
-   `dist`: 1 个值（穿透深度）
-   `pos`: 3 个值（接触点位置）
-   `normal`: 3 个值（法向量）
-   `tangent`: 3 个值（第一切向量）

### reduce 属性对接触点数量的影响

`reduce` 属性决定了返回哪些接触点以及返回多少个：

#### reduce="none"（默认）

-   **行为**：返回满足匹配条件的前 `num` 个接触点，按在 mjData.contact 中出现的顺序
-   **特点**：最快选项，但可能非确定性（碰撞检测算法变化可能改变接触点的身份和顺序）
-   **接触点数量**：最多 `num` 个，可能少于 `num` 个（如果实际接触点较少）

#### reduce="mindist"

-   **行为**：返回穿透深度最小的 `num` 个接触点，按深度升序排列
-   **接触点数量**：最多 `num` 个，可能少于 `num` 个

#### reduce="maxforce"

-   **行为**：返回力范数最大的 `num` 个接触点，按力大小降序排列
-   **接触点数量**：最多 `num` 个，可能少于 `num` 个

#### reduce="netforce"

-   **行为**：返回一个"合成"接触点，具有以下特性：
    -   位置：所有匹配接触点的力加权质心
    -   坐标系：**全局坐标系**（normal 和 tangent 失去原有语义）
    -   力和力矩：计算为在计算位置施加的力和力矩，产生与所有匹配接触点相同的净效果
-   **接触点数量**：**始终恰好 1 个**（忽略 `num` 设置）
-   **特殊注意**：由于使用全局坐标系，数据解释与其他 reduce 类型不同

### 具体配置示例

#### 示例 1：完整接触信息（reduce="none"）

```xml
<contact name="full_contact"
         geom1="bar" geom2="freebox"
         data="found force pos normal tangent"
         num="4"
         reduce="none"/>
```

**返回数据布局**：

```python
contact_data = model.get_sensor_value("full_contact", data)
# 形状：shape = (1 + 4×12,) = (49,) 固定大小（由num="4"决定）
# 数组大小固定，不足的接触点用0填充

# 数据结构：
contact_data[0]              # 实际接触点数量 (例如：2，其余2个为填充)

# 第1个接触点（offset = 1，有效数据）：
contact_data[1:4]           # 力分量：[法向力, 切向0力, 切向1力]
contact_data[4:7]           # 位置：[x, y, z]
contact_data[7:10]          # 法向量：[nx, ny, nz]
contact_data[10:13]         # 切向量0：[tx0, ty0, tz0]

# 第2个接触点（offset = 13，有效数据）：
contact_data[13:16]         # 力分量
contact_data[16:19]         # 位置
contact_data[19:22]         # 法向量
contact_data[22:25]         # 切向量0

# 第3个接触点（offset = 25，填充0）：
contact_data[25:37]         # 全部为0（无接触）

# 第4个接触点（offset = 37，填充0）：
contact_data[37:49]         # 全部为0（无接触）
```

#### 示例 2：简化接触信息（reduce="maxforce"）

```xml
<contact name="force_contact"
         geom1="bar" geom2="freebox"
         data="found force pos"
         num="5"
         reduce="maxforce"/>
```

**返回数据布局**：

```python
contact_data = model.get_sensor_value("force_contact", data)
# 形状：shape = (1 + 5×6,) = (31,) 固定大小（由num="5"决定）
# 数组大小固定，最多返回力最大的5个接触点，按力降序排列
# 不足的接触点用0填充

contact_data[0]              # 实际接触点数量（例如：3）

# 第i个接触点：每接触点6个值
# 只有前 contact_data[0] 个接触点包含有效数据
offset = 1 + i * 6
contact_data[offset + 0:offset + 3]  # 力分量
contact_data[offset + 3:offset + 6]  # 位置
# 注意：i >= contact_data[0] 时，以上数据全部为0
```

#### 示例 3：仅接触状态（最简化）

```xml
<contact name="touch_only"
         geom1="bar" geom2="freebox"
         data="found"
         num="1"/>
```

**返回数据布局**：

```python
contact_data = model.get_sensor_value("touch_only", data)
# 形状：shape = (1,) 始终只有1个值

contact_data[0]  # 接触点数量 (0 = 无接触, 1 = 有接触)
```

#### 示例 4：合力信息（reduce="netforce"）

```xml
<contact name="net_force"
         geom1="bar" geom2="freebox"
         data="found force pos normal tangent"
         num="10"
         reduce="netforce"/>
```

**返回数据布局**：

```python
contact_data = model.get_sensor_value("net_force", data)
# 形状：shape = (1 + 1×12,) = (13,) 始终返回1个合成接触点（忽略num="10"）

contact_data[0]              # 始终为1（合成接触点）

# 合成接触点数据（全局坐标系）：
contact_data[1:4]           # 合力分量
contact_data[4:7]           # 力加权质心位置
contact_data[7:10]          # 法向量（全局坐标系，语义改变）
contact_data[10:13]         # 切向量0（全局坐标系，语义改变）
```

### 重要注意事项

1. **固定数组大小**：返回的数组大小是固定的，由 `num` 参数决定：`shape = (1 + num × values_per_contact,)`
2. **零填充机制**：如果实际接触点数量少于 `num`，剩余位置用 0 填充，需要使用 `contact_data[0]` 判断有效数据
3. **found 字段可靠性**：始终使用 `contact_data[0]` 来确定实际接触点数量，不要假设数组全部有效
4. **netforce 特殊处理**：`reduce="netforce"` 的坐标系和数据解释与其他类型不同，且始终返回 1 个接触点
5. **性能优化**：对于只需要接触状态的应用，使用 `data="found"` 可以显著提高性能

## 🐍 Python Demo

下面是一个完整的接触传感器可视化示例，展示了如何实时获取和渲染接触力数据。该示例来自 `site_and_sensor.py` 文件，演示了接触传感器的实际应用效果。

### 场景配置

首先，我们定义一个包含接触传感器的场景：

```{literalinclude} ../../../../../examples/assets/site_and_sensor.xml
:language: xml
:lines: 50-51
```

这个配置创建了一个名为 `box_floor_contact` 的接触传感器，监测 `bar` 和 `freebox` 两个几何体之间的接触，返回完整的接触信息（力、位置、法向量、切向量）。

### Python 代码

下面是完整的接触传感器可视化代码：

```{literalinclude} ../../../../../examples/site_and_sensor.py
:language: python
:lines: 16-19
:lines: 91-142
```

**注意**：这里只显示了接触传感器的相关部分，完整的示例代码还包括场景设置、其他传感器类型和渲染循环等内容。

### 可视化说明

该示例通过颜色编码的箭头实时显示接触力的各个分量：

-   **白色球体**：接触点位置
-   **绿色箭头**：法向力（垂直于接触表面）
-   **红色箭头**：切向摩擦力分量 0
-   **蓝色箭头**：切向摩擦力分量 1（通过叉积计算得到）

### 效果演示

```{video} /_static/videos/contact_sensor.mp4
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

该视频展示了接触传感器的实时可视化效果，包括：

-   物体与地面接触时的接触点检测
-   接触力的实时计算和显示
-   不同方向力的分量可视化
-   力的大小随物体运动变化的动态过程

## 📊 物理原理

### 接触坐标系

接触传感器使用局部接触坐标系来报告接触数据：

1. **法向量（normal）**：垂直于接触表面，从物体 1 指向物体 2
2. **切向量（tangent0, tangent1）**：构成接触平面内的正交基底
3. **力投影**：接触力在三个轴上的投影值

### 接触力分解

```
总接触力 = 法向力 + 切向力（摩擦力）
F_total = F_normal + F_tangent0 + F_tangent1
```

-   **法向力**：正压力，防止物体相互穿透
-   **切向力**：摩擦力，阻止接触面之间的相对滑动

### 接触检测

接触传感器基于碰撞检测系统工作：

1. 检测两个几何体之间的空间重叠
2. 计算接触点的位置和法向量
3. 根据穿透深度和材料属性计算接触力
4. 将接触力投影到局部接触坐标系

## ⚠️ 注意事项

1. **力分量是标量**：`force_normal_mag`、`force_tangent0_mag`、`force_tangent1_mag` 是力的投影值，不是完整的力向量
2. **第二切向量**：需要通过 `tangent1 = cross(normal, tangent0)` 计算得到
3. **坐标系**：所有数据都在局部接触坐标系中表示，不是全局坐标系
4. **性能考虑**：接触传感器计算量较大，建议合理设置 `num` 属性限制报告的接触点数量
5. **配置互斥**：`geom1/geom2`、`body1/body2`、`subtree1/subtree2`、`site` 四种配置方式只能使用一种
