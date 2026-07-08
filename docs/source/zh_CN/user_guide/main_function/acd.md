# 🧩 ACD 凸分解

ACD（Approximate Convex Decomposition）用于把非凸 mesh 分解为多个凸包。在 MotrixSim 中，
它主要服务于 mesh 碰撞体：复杂模型可以保留原始视觉 mesh，同时用更适合物理碰撞的凸包集合参与
仿真。

下面的示例先展示同一房间场景的渲染效果，然后打开碰撞体可视化，对比 ACD 关闭和开启后的
convex hull 精细度。ACD 开启后，碰撞体会由多个局部凸包近似原始物体外形，能更好覆盖柜体、沙发、
装饰物等非凸结构。

```{video} /_static/videos/acd_room_ssgi_demo.mp4
:poster: /_static/images/poster/acd_room_ssgi_demo.jpg
:caption: ACD 碰撞体效果对比
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%

```

MotrixSim 支持两种 ACD 使用方式：

| 方式       | 适用场景                                             | 产物                                    |
| ---------- | ---------------------------------------------------- | --------------------------------------- |
| 在线凸分解 | 加载或构建场景时直接启用，适合简单模型调试和快速验证 | 运行时 convex hull collider，不写出文件 |
| 离线凸分解 | 预处理资产，适合稳定提交、复用和人工检查碰撞 mesh    | `.obj` 或 `.stl` 凸分解文件             |

```{note}
在线凸分解不会修改 MJCF/URDF/USD 文件，也不会在磁盘生成新的 mesh 文件。离线凸分解只处理
`.obj` / `.stl` mesh 文件，不会自动改写 MJCF。需要让模型引用离线产物时，请手动更新模型里的
mesh 路径。
```

## 跑通文档示例

`motrixsim-docs` 在 `examples/assets/acd/` 下提供了 ACD 示例场景，下面的路径都相对于
`motrixsim-docs` 项目根：

-   `examples/assets/acd/world.xml`：原始房间场景，mesh 直接来自原始 OBJ 资产。
-   `examples/assets/acd/world_acd.xml`：离线 ACD 房间场景，视觉 mesh 保持原始 OBJ，碰撞 mesh 指向
    已提交的 `assets/convex_parts/` 产物。
-   `examples/assets/acd/chair_online_acd.xml`：单独的椅子小场景，碰撞 mesh 仍指向原始 OBJ，
    通过 `acd="true"` 在加载时走在线 ACD。

相对原始场景，`world_acd.xml` 保持相同房间视觉效果，但把 mesh 碰撞体替换为离线凸分解产物。

进入 `motrixsim-docs` 项目根后运行：

```bash
# 先打开原始场景
uv run mxview examples/assets/acd/world.xml

# 打开开启 ACD 管线后的场景
uv run mxview examples/assets/acd/world_acd.xml

# 打开一个小型在线 ACD 示例
uv run mxview examples/assets/acd/chair_online_acd.xml
```

房间场景的视觉效果基本一致，差异主要在碰撞体。打开 `mxview` 后，在右侧面板找到 `Gizmos`，同时开启
`Static Collider` 和 `ConvexHull`，再观察同一个物体的碰撞轮廓：

-   `world.xml` 使用原始 mesh 编译出的碰撞体，非凸结构通常只能看到较粗的单凸包近似。
-   `world_acd.xml` 引用预生成的 `convex_parts/*_convex.obj` 碰撞 mesh，开启 gizmo 后可以看到多个
    局部 convex hull 更贴近柜体、沙发、装饰物等非凸外形。
-   `chair_online_acd.xml` 刻意和离线房间示例分开，用一把椅子快速检查在线 `acd="true"` 加载路径。

房间示例展示的是带已提交 convex mesh 文件的离线 ACD 管线；椅子示例展示的是在线 ACD 管线。
如果要把任一管线接到自己的 MJCF，请继续看下面的“通过 MJCF 启用”小节。

## 它解决了什么问题

非凸 mesh 直接作为碰撞体时，通常会带来更高的计算成本，也可能和引擎内部的凸包碰撞路径不匹配。
ACD 的作用是把一个非凸 mesh 拆成若干个局部凸包，让复杂外形能够用多个简单凸碰撞体近似。

常见使用场景包括：

-   为机器人夹爪、杯子、柜体、抽屉等非凸结构生成更合理的碰撞体
-   保留高质量视觉 mesh，同时单独优化碰撞 mesh
-   在调试阶段快速检查某个 mesh 用多凸包碰撞后是否更符合预期
-   在资产发布前把凸分解结果固定下来，避免每次加载时重复分解

## 在线凸分解

在线凸分解发生在场景加载或模型编译阶段。被标记为允许 ACD 的 mesh 会被 CoACD 分解为一个或多个
运行时凸包；随后这些凸包会作为真实 collider 进入碰撞、raycast、包围盒等运行时流程。

不同资产入口启用 ACD 的方式彼此独立：MJCF 使用 `<mesh acd="true">`，USD 使用
`MeshCollisionAPI.approximation = "convexDecomposition"`。USD 资产不需要先转换成 MJCF，也不需要额外写
MJCF 字段。

### 通过 MJCF 接入

MJCF 可以用在线或离线两种方式接入 ACD。在线 ACD 可以直接让同一个 mesh geom 同时负责渲染和碰撞；
如果需要单独调试碰撞体、隐藏碰撞几何或替换离线产物，也可以把视觉 mesh 和碰撞 mesh 分开。

#### 在线接入

在线 ACD 的开关写在 `<asset>` 里的 `<mesh>` 上，而不是写在 `<geom>` 上。mesh 仍然指向原始 OBJ/STL，
只额外加上 `acd="true"`；只有这个 mesh 被可碰撞 geom 引用时，加载或编译场景才会真正运行 CoACD：

```xml
<mujoco>
    <asset>
        <mesh name="cup" file="meshes/cup.obj" acd="true"/>
    </asset>

    <worldbody>
        <body name="cup" pos="0 0 0.4">
            <freejoint/>
            <geom name="cup" type="mesh" mesh="cup" mass="0.2"/>
        </body>
    </worldbody>
</mujoco>
```

`examples/assets/acd/chair_online_acd.xml` 使用的就是在线管线，例如：

```xml
<mesh name="chair_cushion" file="assets/GEO_chair_001a.obj" acd="true"/>
<mesh name="chair_frame" file="assets/GEO_chair_001b.obj" acd="true"/>
```

#### 离线接入

离线 ACD 先用 `uv run acd` 把 OBJ/STL 分解并写到磁盘，然后在 MJCF 里让碰撞 `<mesh>` 指向生成好的
凸分解文件。离线方式不需要再写 `acd="true"`：

```xml
<mesh name="GEO_sofa_001" file="GEO_sofa_001.obj"/>
<mesh name="GEO_sofa_001_acd" file="convex_parts/GEO_sofa_001_convex.obj"/>
```

已提交的房间示例已经使用离线接入。它的 `convex_parts/` 文件可以按下面的方式生成：

```bash
# 在 motrixsim-docs 项目根执行，先预览会生成哪些凸分解文件
uv run acd examples/assets/acd/assets --dry-run

# 确认后，把离线产物写到 ACD 示例自己的资产目录
uv run acd examples/assets/acd/assets \
    -o examples/assets/acd/assets/convex_parts
```

然后在 `examples/assets/acd/assets/room_acd.xml` 中，让碰撞 mesh 指向这些生成文件：

```xml
<mesh name="GEO_sofa_001_acd" file="convex_parts/GEO_sofa_001_convex.obj"/>
```

同一个物体的 geom 绑定通常不需要改，因为碰撞 geom 仍然引用同一个 `GEO_sofa_001_acd` mesh 名称；
变化的是这个 mesh asset 背后的 `file` 路径，以及是否带 `acd="true"`。

无论在线还是离线，随后都在同一个位姿上建立两条 geom 引用：视觉 geom 关闭碰撞，碰撞 geom 引用
对应的 ACD mesh 并开启碰撞：

```xml
<geom name="GEO_sofa_001" pos="1.864403 0.9069114 -3.1659286"
      quat="0.7071069 -1e-07 1e-07 -0.7071066"
      type="mesh" mesh="GEO_sofa_001" material="MI_sofa_002"
      group="2" contype="0" conaffinity="0" density="0"/>
<geom name="GEO_sofa_001_acd" pos="1.864403 0.9069114 -3.1659286"
      quat="0.7071069 -1e-07 1e-07 -0.7071066"
      type="mesh" mesh="GEO_sofa_001_acd"
      group="3" contype="1" conaffinity="1"/>
```

接入时请重点检查：

-   在线方式：`acd="true"` 是否写在碰撞 `<mesh>` 上，而不是写在 `<geom>` 上。
-   离线方式：碰撞 `<mesh file="...">` 是否指向生成的凸分解文件，路径是否相对于当前 XML 文件。
-   视觉 geom 和碰撞 geom 是否在同一个父 body 下，并使用相同的 `pos` / `quat`。
-   原始视觉 geom 是否已经关闭碰撞，避免同一个物体同时用原始 mesh 和 ACD 结果参与碰撞。
-   如果使用子模型，是否改的是子模型 XML，而不是只改顶层 `world.xml`。

加载方式与普通模型一致：

```python
import motrixsim as mx

model = mx.load_model("scene.xml")
data = mx.SceneData(model)
mx.step(model, data)
```

### 通过 USD 启用

USD 资产中如果使用 `MeshCollisionAPI.approximation = "convexDecomposition"`，MotrixSim 会把它映射为
允许 ACD 的 mesh，并在加载时生成运行时凸包。USD 支持状态可参考 {doc}`../getting_started/usd_reference`。

### 运行时行为

在线凸分解只影响碰撞几何，不改变视觉 mesh。编译完成后，原始 mesh 仍可用于渲染和资产引用；
碰撞路径会使用分解得到的 convex hull collider。

在线 ACD 的默认 `threshold` 与离线命令保持一致，都是 `0.1`。由于在线分解需要在加载或编译场景时完成，
复杂 mesh 或大规模资产会明显增加启动耗时；这类资产建议先用离线凸分解生成并提交 `convex_parts` 结果。
在线方式更适合简单模型调试、快速预览和临时验证。

如果只是快速验证在线 ACD 效果，可以用 `mxview` 打开
`examples/assets/acd/chair_online_acd.xml`。它给椅子的两个碰撞 mesh 加上 `acd="true"`，会在加载时生成
运行时 collider，不会写出 `convex_parts` 文件。

如果某个 mesh 的 CoACD 分解失败、结果为空、超过运行时凸包数量预算，或生成的凸包无法被碰撞后端
接受，MotrixSim 会对这个 mesh 回退到单凸包路径。其它 mesh 的 ACD 结果不受影响。

## 离线凸分解

离线凸分解用于把 `.obj` / `.stl` mesh 文件提前分解并写到磁盘。它适合资产处理和版本化管理：
生成结果可以提交到仓库，也可以在 MJCF/URDF 中作为碰撞 mesh 引用。

### 命令行使用

先用 `--dry-run` 预览会生成哪些产物：

```bash
uv run acd meshes/robot.obj --dry-run
```

确认结果后写出文件：

```bash
uv run acd meshes/robot.obj
```

默认情况下，每个源 mesh 会在自身所在目录旁生成 `convex_parts/{stem}_convex.obj`：

```text
meshes/robot.obj
meshes/convex_parts/robot_convex.obj
```

也可以指定输出目录或单文件输出：

```bash
uv run acd meshes/robot.obj -o baked_collision
uv run acd meshes/robot.obj --output robot_collision.obj
uv run acd meshes/robot.obj --output robot_collision.stl
```

目录输入会递归处理其中的 `.obj` / `.stl` 文件：

```bash
uv run acd meshes/ --dry-run
uv run acd meshes/ -o baked_collision
```

### Python API

在 Python 中可以直接调用 `motrixsim.acd`：

```python
import motrixsim as mx

report = mx.acd("meshes/robot.obj", dry_run=True)

for file in report.files:
    print(file.path, file.fatal_error)
    for mesh in file.meshes:
        print(mesh.name, mesh.part_count, mesh.part_files, mesh.skipped_reason)
```

### 在 MJCF 中引用离线产物

离线工具不会自动修改 MJCF。生成碰撞 mesh 后，需要在模型 XML 里手动把碰撞 mesh 指向新的凸分解
文件。这个流程不需要 `acd="true"`，因为凸分解已经提前写到了磁盘：

```xml
<asset>
    <mesh name="robot_visual" file="meshes/robot.obj"/>
    <mesh name="robot_collision" file="meshes/convex_parts/robot_convex.obj"/>
</asset>

<worldbody>
    <body name="robot">
        <geom type="mesh" mesh="robot_visual" contype="0" conaffinity="0"/>
        <geom type="mesh" mesh="robot_collision"/>
    </body>
</worldbody>
```

这样可以保留原始视觉 mesh，同时使用离线分解后的 mesh 参与碰撞。接入自己的场景时通常需要检查
三件事：

-   视觉 `<mesh>` 继续指向原始 OBJ/STL；碰撞 `<mesh>` 指向离线生成文件，例如
    `meshes/convex_parts/robot_convex.obj`。`file` 路径相对于声明这个 `<mesh>` 的 XML 文件。
-   视觉 geom 和碰撞 geom 位于同一个父 body 下，并使用相同的 `pos` / `quat`。视觉 geom 关闭碰撞，
    碰撞 geom 引用离线凸分解 mesh 并保留有效的 `contype` / `conaffinity`。
-   如果场景通过子模型组合，不需要把每个碰撞 mesh 都写到顶层 `world.xml`；应该修改声明这些
    mesh 和 geom 的子模型 XML。

离线接入完成后，用 `mxview` 打开对应场景，并在 `Gizmos` 面板同时开启 `Static Collider` 和
`ConvexHull`，检查离线碰撞体是否覆盖原始视觉模型。

## 参数速览

| 参数                  | 位置                                     | 说明                         |
| --------------------- | ---------------------------------------- | ---------------------------- |
| `acd`                 | MJCF `<mesh acd="true">`                 | 启用在线凸分解               |
| `convexDecomposition` | USD `MeshCollisionAPI.approximation`     | 启用在线凸分解               |
| `threshold`           | `--threshold` / `threshold=`             | 离线分解误差阈值             |
| `max_convex_hull`     | `--max-convex-hull` / `max_convex_hull=` | 离线 CoACD 后端最大凸包数    |
| `output`              | `-o/--output` / `output=`                | 离线输出目录或单文件输出路径 |
| `dry_run`             | `--dry-run` / `dry_run=True`             | 离线预览结果，不写磁盘       |

## 如何选择

| 需求                                    | 推荐方式   |
| --------------------------------------- | ---------- |
| 快速验证某个 mesh 的多凸包碰撞效果      | 在线凸分解 |
| 不想维护额外碰撞 mesh 文件              | 在线凸分解 |
| 希望误差更小、资产加载更稳定            | 离线凸分解 |
| 需要人工检查、编辑或提交生成的碰撞 mesh | 离线凸分解 |
| 需要把同一份碰撞 mesh 复用于多个模型    | 离线凸分解 |

## FAQ

1. Q：在线凸分解会改变视觉效果吗？  
   A：不会。在线 ACD 只影响碰撞 collider，视觉 mesh 仍然使用原始 mesh。

2. Q：为什么设置了 `acd="true"` 后看起来还是只有一个碰撞体？  
   A：可能是 mesh 本身接近凸形，也可能是分解失败或超过运行时凸包数量预算后回退到单凸包。调试时可以
   降低 `threshold`，或提高 `max_convex_hull` 与运行时预算。

3. Q：离线凸分解会自动替换 XML 里的 mesh 路径吗？  
   A：不会。离线工具只读写 `.obj` / `.stl`，模型文件需要手动更新。

4. Q：目录输入时能把所有 mesh 合成一个输出文件吗？  
   A：不能。目录模式保持“一源文件一产物”的结构；如果要指定单个 `.obj` / `.stl` 输出文件，输入也必须是
   单个 mesh 文件。
