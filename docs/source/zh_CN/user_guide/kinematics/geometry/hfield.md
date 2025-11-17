# 高度场（Height Field）

高度场（Height Field，简称 HField）是一种用于表示地形表面的高效几何体类型。它通过二维网格数据存储高程信息，为机器人仿真、地形跟随和表面交互提供真实的物理碰撞响应。

## 高度场特点

高度场具有以下优势：

-   **高效存储**：使用规则网格存储高程数据，内存占用较小
-   **快速碰撞检测**：基于网格的空间分割算法，提供高效的碰撞查询
-   **真实地形模拟**：支持复杂的地形特征，如山坡、沟壑、平原等
-   **大规模场景**：适合表示大面积地形，常用于户外机器人仿真

## MJCF 配置

在 MJCF 文件中，高度场通过 `<hfield>` 标签定义，支持三种数据来源方式：

### 1. 内联高程数据

直接在 XML 中指定高程数据矩阵：

```xml
<asset>
    <hfield name="terrain1"
            nrow="15"
            ncol="15"
            elevation="0.0 0.43 0.78 0.97 ..."
            size="5 5 2 0.1"/>
</asset>
```

### 2. PNG 图像文件

使用 PNG 图像作为高程数据源（推荐用于可视化地形）：

```xml
<asset>
    <hfield name="png_terrain"
            file="terrain.png"
            content_type="image/png"
            size="10 10 3 0.2"/>
</asset>
```

**说明：**

-   PNG 图像会被自动转换为灰度图像
-   白色像素对应高程，黑色像素对应低程
-   强度值用作高程数据并标准化到 [0, 1] 范围

### 3. 自定义二进制文件

使用 MuJoCo 自定义二进制格式：

```xml
<asset>
    <hfield name="binary_terrain"
            file="terrain.hfield"
            content_type="image/vnd.mujoco.hfield"
            size="8 8 2.5 0.15"/>
</asset>
```

**二进制文件格式：**

-   文件大小：`4 × (2 + nrow × ncol)` 字节
-   结构：
    -   `int32 nrow`：行数
    -   `int32 ncol`：列数
    -   `float32 data[nrow×ncol]`：高程数据（行主序）

### MJCF 属性说明

| 属性           | 类型                 | 默认值 | 说明                                                                                          |
| -------------- | -------------------- | ------ | --------------------------------------------------------------------------------------------- |
| `name`         | 字符串               | 可选   | 高度场的名称，用于引用。如果省略且指定了文件名，则使用文件名（不含路径和扩展名）              |
| `content_type` | 字符串               | 可选   | **MotrixSim 目前忽略此属性**                                                                  |
| `file`         | 字符串               | 可选   | 外部文件路径。`.png` 文件会被转换为灰度图像，强度值用作高程数据；其他格式视为自定义二进制格式 |
| `nrow`         | 整数                 | "0"    | 高程数据矩阵的行数。默认值 0 表示从文件加载数据并自动推断矩阵大小                             |
| `ncol`         | 整数                 | "0"    | 高程数据矩阵的列数                                                                            |
| `elevation`    | 浮点数组 (nrow×ncol) | 可选   | 内联高程数据矩阵。数据会自动标准化到 [0, 1] 范围。未提供时默认为 0                            |
| `size`         | 浮点数组 (4 个元素)  | 必需   | 物理尺寸：`[radius_x, radius_y, elevation_z, base_z]`                                         |

### size 属性详细说明

`size` 属性包含四个浮点数：`[radius_x, radius_y, elevation_z, base_z]`，每个参数的含义如下：

-   **radius_x**：X 方向的半径（半宽）。高度场在 X 轴上的总宽度为 `2 × radius_x`
-   **radius_y**：Y 方向的半径（半长）。高度场在 Y 轴上的总长度为 `2 × radius_y`
-   **elevation_z**：最大高程。这个值缩放标准化到 [0-1] 的高程数据，因此最低点在 Z=0，最高点在 Z=elevation_z
-   **base_z**：基础深度。**MotrixSim**目前忽略此属性

**重要说明：**

-   高度场以引用几何体的局部坐标系为中心
-   高程方向为 +Z 方向
-   与平面不同，高度场被视为常规几何体的联合，没有"在高度场下方"的概念，几何体要么在高度场内部，要么在外部
-   因此基础部分必须有非零厚度以避免穿透问题

**示例：**

```xml
<!-- 创建一个 10×10 单位、最大高程 2 单位、基础厚度 0.1 单位的高度场 -->
<hfield name="terrain" size="5 5 2 0.1" nrow="50" ncol="50"/>
```

### 碰撞检测特性

高度场的碰撞检测具有以下重要特性：

**碰撞模型：**

-   高度场被视为三角棱柱的联合体
-   首先根据几何体边界框选择可能碰撞的子网格棱柱
-   然后使用通用凸碰撞器进行精确碰撞计算

**支持的碰撞类型：**

-   ✅ 高度场与球体、胶囊体、圆柱体、立方体、多面体
-   ❌ 高度场与平面的碰撞（不支持）
-   ❌ 高度场与其他高度场的碰撞（不支持）

更详细的 hfield 字段说明，请参考[MJCF 官方文档](https://mujoco.readthedocs.io/en/3.3.7/XMLreference.html#asset-hfield)。

### 几何体引用

在 `<worldbody>` 中使用高度场：

```xml
<worldbody>
    <geom name="terrain" type="hfield" hfield="terrain1" material="ground_material"/>
    <geom pos="10 0 0" name="terrain2" type="hfield" hfield="file_terrain" material="ground_material"/>
</worldbody>
```

## 主要接口

在 MotrixSim 中，您可以通过以下方式访问 HField 对象：

-   [`model.num_hfields`]： 获取当前场景中的高度场数量。
-   [`model.get_hfield(name_or_index)`]： 根据名称或索引获取特定的高度场对象。

### HField 对象属性

获取到 HField 对象后，可以访问以下属性：

```python
hfield = model.get_hfield("terrain1")

# 基本属性
name = hfield.name          # 高度场名称
nrow = hfield.nrow          # 网格行数
ncol = hfield.ncol          # 网格列数
bound = hfield.bound        # 边界框 [-x, -y, 0, x, y, z]

# 高程数据
height_matrix = hfield.height_matrix  # 完整的高程矩阵 (nrow × ncol)

# 查询特定点的高程值
height = hfield.get(row=5, col=10)    # 获取指定行列的高程
```

## 使用示例

### 基本高度场操作

```{literalinclude} ../../../../../examples/hfield.py
:language: python
:dedent:
:start-after: "# tag::basic_access"
:end-before: "# end::basic_access"
```

### 高程数据分析

```{literalinclude} ../../../../../examples/hfield.py
:language: python
:dedent:
:start-after: "# tag::height_analysis"
:end-before: "# end::height_analysis"
```

### 完整仿真示例

```{literalinclude} ../../../../../examples/hfield.py
:language: python
:dedent:
```

运行高度场仿真示例：

```bash
uv run examples/hfield.py
```

## 文件格式

MotrixSim 支持二进制高度场文件格式（`.hfield`）：

### 文件结构

-   **头部**：前 8 字节
    -   `nrow` (int32)：网格行数
    -   `ncol` (int32)：网格列数
-   **数据部分**：剩余字节
    -   高程数据数组 (float32)，长度为 `nrow × ncol`

### 生成高度场文件

您可以使用以下方式创建自定义高度场文件：

```python
import numpy as np

def create_hfield_file(filename, height_data):
    """创建二进制高度场文件"""
    nrow, ncol = height_data.shape

    with open(filename, 'wb') as f:
        # 写入头部信息
        f.write(np.array([nrow, ncol], dtype=np.int32).tobytes())
        # 写入高程数据
        f.write(height_data.astype(np.float32).tobytes())

# 示例：创建简单的地形
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = 0.5 * np.sin(X) * np.cos(Y)  # 正弦波形地形

create_hfield_file("custom_terrain.hfield", Z)
```

## API Reference

更多与 HField 相关的 API，请参考：

-   [`HField API`]\: 完整的高度场类接口文档
-   [`SceneModel.get_hfield()`]\: 获取高度场对象的方法
-   [`SceneModel.num_hfields`]\: 获取高度场数量

[`model.num_hfields`]: motrixsim.SceneModel.num_hfields
[`model.get_hfield(name_or_index)`]: motrixsim.SceneModel.get_hfield
[`HField API`]: motrixsim.HField
[`SceneModel.get_hfield()`]: motrixsim.SceneModel.get_hfield
[`SceneModel.num_hfields`]: motrixsim.SceneModel.num_hfields
