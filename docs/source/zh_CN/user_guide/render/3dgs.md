# ✨ 3DGS 支持

<p class="motphys-pro-license-note">🔒 该功能需要商业或学术授权（license），<a class="pro-license-btn">联系 Motphys 获取授权</a></p>

MotrixSim Pro 支持在 MJCF 场景中加载 3D Gaussian Splatting 点云资产，并在渲染器中把点云实例绑定到 world 或指定 body 上。该能力适合把扫描得到的真实环境、物体外观或背景场景作为高保真视觉层，与 MotrixSim 的刚体、关节、碰撞体和传感器一起使用。

3DGS 点云与传统网格在同一帧中被一起渲染，构成一条**混合渲染管线**：扫描得到的真实环境以 3DGS
形式提供逼真的背景与外观，机器人、操作物体等需要参与物理仿真的对象仍由网格 `geom` 表示，并通过
IBL 与真实环境的光照保持一致。这条管线对机器人任务有直接意义：

-   **缩小 sim-to-real 差距**：相机传感器看到的是接近真实拍摄的画面，而非手工搭建的合成场景，
    有利于训练和验证视觉策略、VLA 等依赖图像输入的模型。
-   **低成本构建多样化场景**：只需扫描真实场景即可得到可用的仿真背景，省去逐物体建模与材质调校，
    便于批量生成用于导航、操作的训练环境。
-   **物理与视觉解耦**：高保真外观由 3DGS 承担，碰撞与动力学仍使用简化几何，既保证渲染真实度，
    又不牺牲仿真性能与可控性。

## 演示视频

```{video} /_static/videos/g1-3dgs-mix.mp4
:caption: G1 与 3DGS 场景混合渲染效果
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

## 支持范围

-   在 `<asset>` 中声明可复用的 3DGS 点云资产。
-   在 `<worldbody>` 或任意 `<body>` 下创建 3DGS 实例。
-   支持 `.ply` 和 `.gcloud` 点云文件。
-   支持位置、旋转、缩放、透明度、splat 尺寸倍率和可见性 group。
-   当 3DGS 实例挂在运动 body 下时，渲染位姿会随该 body 同步更新。
-   支持通过相机渲染和常规 `RenderApp` 同步流程显示 3DGS 内容。

3DGS 只提供视觉表示，不会自动生成碰撞形状或惯量。需要参与物理仿真的物体仍应使用常规 `geom`、`body/inertial` 和碰撞相关配置。

## MJCF 写法

首先在 `<asset>` 中定义一个 `gsplat` 资产，然后在 `<worldbody>` 或某个 `<body>` 下通过 `asset` 引用它：

```xml
<mujoco model="gsplat_scene">
    <asset>
        <gsplat name="office_scan" file="assets/office_scan.ply"/>
    </asset>

    <worldbody>
        <gsplat
            name="static_office"
            asset="office_scan"
            pos="0 0 0"
            quat="1 0 0 0"
            scale="1 1 1"
            opacity="1"
            splatscale="1"
            group="0"/>

        <body name="tracked_object" pos="0 0 0.5">
            <freejoint/>
            <geom type="box" size="0.2 0.2 0.2" mass="1"/>
            <gsplat name="object_visual" asset="office_scan" scale="0.2 0.2 0.2"/>
        </body>
    </worldbody>
</mujoco>
```

`asset/gsplat` 用于定义点云文件：

| 属性           | 说明                              |
| :------------- | :-------------------------------- |
| `name`         | 点云资产名，供 `body/gsplat` 引用 |
| `file`         | `.ply` 或 `.gcloud` 文件路径      |
| `content_type` | 可选的媒体类型覆盖                |

`body/gsplat` 用于创建实例：

| 属性                                                | 说明                                   |
| :-------------------------------------------------- | :------------------------------------- |
| `name`                                              | 可选实例名                             |
| `asset`                                             | 引用的 `asset/gsplat` 名称             |
| `pos`                                               | 点云实例局部坐标系位置，默认 `0 0 0`   |
| `quat` / `euler` / `axisangle` / `xyaxes` / `zaxis` | 点云实例局部坐标系旋转                 |
| `scale`                                             | 三轴缩放，默认 `1 1 1`                 |
| `opacity`                                           | 全局透明度倍率，默认 `1`               |
| `splatscale`                                        | Gaussian covariance 缩放倍率，默认 `1` |
| `group`                                             | 可见性分组，默认 `0`                   |

## IBL 烘焙

为了让 3DGS 点云中放置的刚体（机器人、物体等）能融入扫描场景的真实光照，MotrixSim 提供
`mx-ibl-bake` 命令：它从 3DGS `.ply` 或 `.gcloud` 点云捕获环境贴图，并烘焙为基于图像的光照
（Image-Based Lighting, IBL）所需的 KTX2 贴图。烘焙出的 diffuse / specular 贴图随后在 MJCF
里以环境贴图的形式引用，为 PBR 材质提供与点云一致的环境光与反射。

下图对比了同一场景中关闭与开启环境光照的渲染效果：关闭时（上）只剩内置 headlight，机器人偏暗
且与背景点云的光照割裂；开启后（下），机器人受到点云环境的漫反射与高光影响，金属材质呈现出与
房间一致的反射与亮度。

```{figure} /_static/images/pro/env_light_compare.jpg
:width: 80%
:align: center

关闭（上）与开启（下）IBL 环境光照的渲染对比
```

使用该工具需要安装 `gs-ibl` extra：

```bash
uv add "motrixsim[gs-ibl]"
```

### 烘焙命令

基础用法：

```bash
uv run mx-ibl-bake \
    --ply assets/office_scan.ply \
    --out assets/office_ibl \
    --auto-center bounds \
    --resolution 1024
```

常用参数：

| 参数                   | 说明                               |
| :--------------------- | :--------------------------------- |
| `--ply`                | 输入 `.ply` 或 `.gcloud` 点云路径  |
| `--out`                | 输出目录                           |
| `--center X Y Z`       | 手动指定 probe 位置                |
| `--auto-center mean`   | 使用点云均值作为 probe 位置        |
| `--auto-center bounds` | 使用点云包围盒中心作为 probe 位置  |
| `--resolution`         | 捕获分辨率                         |
| `--near` / `--far`     | 捕获相机近远裁剪面                 |
| `--debug`              | 保留六面捕获图和 `environment.png` |

默认烘焙完成后只保留两个 KTX2 文件：

```text
assets/office_ibl/
├── diffuse.ktx2    # 漫反射辐照度（irradiance）环境贴图
└── specular.ktx2   # 高光预过滤（prefiltered）环境贴图
```

需要检查捕获质量时再使用 `--debug` 保留 `capture/` 下的六面图和合成的 `environment.png`。

### 在 MJCF 中使用烘焙结果

烘焙出的 `diffuse.ktx2` 和 `specular.ktx2` 在 MJCF 中通过 `<asset>` 下的 `texture` 元素引用：
分别使用 `type="envdiff"`（漫反射环境贴图）和 `type="envspec"`（高光环境贴图）。文件路径相对于
`compiler` 的 `texturedir`：

```xml
<mujoco model="gsplat_scene_ibl">
    <!-- 在已有的 3DGS 场景基础上叠加 IBL，可以用 include 复用 -->
    <include file="scene.xml"/>

    <compiler texturedir="."/>

    <asset>
        <texture name="env_diff" type="envdiff" file="office_ibl/diffuse.ktx2"/>
        <texture name="env_spec" type="envspec" file="office_ibl/specular.ktx2"/>
    </asset>

    <visual>
        <!-- 已有 IBL 时通常调暗内置 headlight，避免双重打光 -->
        <headlight diffuse="0.2 0.2 0.2" ambient="0.05 0.05 0.05" specular="0 0 0"/>
        <!-- 控制环境贴图对场景的整体光照强度 -->
        <map envmapintensity="1000"/>
        <!-- HDR 环境贴图建议配合 tonemapping 一起使用 -->
        <tonemapping method="aces"/>
    </visual>
</mujoco>
```

关键点：

-   只要 `<asset>` 中声明了 `envdiff` / `envspec` 两个 texture，渲染器就会自动把它们作为场景的
    IBL 环境光，无需在 `geom` 上手动绑定；diffuse 与 specular 应成对提供。
-   环境贴图只影响使用 PBR 材质的常规 `geom` 的受光，不会改变 3DGS 点云本身的外观（点云已包含
    其自身的烘焙颜色）。其作用是让放进场景的刚体与点云环境光照一致。
-   `envmapintensity` 控制环境贴图的整体强度，需要与烘焙时的曝光相匹配；偏暗或偏亮时优先调节
    该值，再考虑重新烘焙。
-   KTX2 为 HDR 贴图，建议搭配 `<tonemapping>` 把高动态范围映射到显示范围；可选地再叠加
    `<ssgi>` 等屏幕空间全局光照以增强真实感。

完整示例可参考仓库中的 `examples/pro/assets/nav_scene_1/scene_ibl.xml`，它在 3DGS 导航场景上
叠加了 IBL 与 SSGI 配置。

## 相关参考

-   {doc}`../main_function/render`
-   {doc}`../render/camera`
-   {doc}`../getting_started/mjcf_reference`
