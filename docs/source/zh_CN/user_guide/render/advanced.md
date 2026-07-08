# 🖌️ 高质量渲染

## 概述

高质量渲染以物理正确的灯光为能量源，基于物理的材质定义交互规则，全局光照模拟能量在场景中的完整传播路径，三者协同实现照片级真实感。

## 全局光照（Global Illumination）

全局光照（Global Illumination, GI） 是一种模拟光线在三维场景中传播的渲染技术。它不仅计算光源直接照射到物体表面的直接光照，还计算光线经过其他物体一次或多次反射、折射后才进入视野的间接光照（如颜色溢出、柔和阴影、焦散等）。其物理基础由渲染方程描述，核心挑战在于计算量巨大。

### SSGI

Motrix-Sim 集成了 SSGI（Screen Space Global Illumination）：一种基于屏幕空间的光照计算技术。能在有限的条件下提升渲染质量，使得画面更加真实。

开启 SSGI 渲染效果：

```{video} /_static/videos/ssgi.mp4
:poster: /_static/images/poster/ssgi.png
:caption: SSGI渲染效果
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%

```

#### 主要特性

-   **屏幕空间间接光照**: 在渲染画面中模拟光照的多次反弹效果
-   **屏幕空间反射**: 在渲染画面中模拟表面反射效果

#### GI 效果对比

| ![](/_static/images/render/direct_only.png) | ![](/_static/images/render/direct_env.png) |
| :-----------------------------------------: | :----------------------------------------: |
|            **Direct Light Only**            |         **Direct Light + Env IBL**         |

| ![](/_static/images/render/ssao_env.png) | ![](/_static/images/render/ssgi_env.png) |
| :--------------------------------------: | :--------------------------------------: |
|    **Direct Light + Env IBL + SSAO**     |    **Direct Light + Env IBL + SSGI**     |

```{note}
GI 是高真实感渲染的核心技术，SSGI 是实时动态GI的“性价比之选”——以屏幕空间限制为代价，换取无预计算、全动态、与场景复杂度解耦的高性能间接光照。同时不需要限制显卡品牌。

它最适合室内/近景、重视光影动态但可接受“物理近似”的实时应用预览；不适合需要屏幕外信息、物理精度、或运行在低功耗/高帧率平台上的场景。

```

#### 启用方式

##### XML 配置

在 MJCF 文件中，使用 `<ssgi>` 标签来配置渲染参数：

```xml
<mujoco>
  <visual>
    <ssgi
      active="true"
      resolutionscale="2"
      raycount="2"
      stepcount="8"
      thickness="0.25"
      intensity="1.0"
      gidenoiseoffset="3"
      rraycount="64"
      rdenoiseoffset="3"
    />
  </visual>
</mujoco>
```

##### Tag 说明

-   **active**: 启用/关闭 SSGI，默认 false
-   **resolutionscale**: 控制快速全局光照的质量。更高的分辨率缩放占用更少的内存（缓冲区大小 = 1 / 分辨率比例）。输入值为 1、2 或 4 时，其他值将默认为 2
-   **raycount**: 每个像素要追踪的全局光照光线数量，范围 1 - 16 增加射线数量增加性能消耗
-   **stepcount**: 每条全局光照光线的屏幕采样数量，范围 1 - 64 增加采样数量增加性能消耗
-   **thickness**: 计算快速 GI、反射和 AO 时表面的几何厚度。减少漏光和接触遮蔽缺失
-   **intensity**: GI 的强度
-   **gidenoiseoffset**: 间接光降噪偏移范围，为 0 时无降噪
-   **rraycount**: 每条反射光线的屏幕采样数量，范围：32 - 512 增加采样次数增加性能消耗
-   **rdenoiseoffset**: 反射降噪偏移范围，为 0 时无降噪

代码示例：

```{literalinclude} ../../../../examples/viewer/ssgi.py
:language: python
:dedent:
:start-after: "# tag: ssgi on"
:end-before:  "# endtag"

```

```{attention}
- 当且仅当全局配置开启，且场景描述文件（mjcf/msd）中也启用SSGI渲染项时，才会有最终的效果

- 当 SSGI 和 SSAO 同时开启时 SSAO 被忽略，SSGI 能免费得到 SSAO 效果，且更加准确

- 目前 Python API 只支持是否启用SSGI渲染设置，暂不支持渲染参数配置
```

_[完整示例场景](https://github.com/Motphys/motrixsim-docs/tree/main/examples/assets/ssgi)_
_[完整示例代码](https://github.com/Motphys/motrixsim-docs/blob/main/examples/viewer/ssgi.py)_

示例视频图片实机配置：

|  软/硬件  |            型号            |
| :-------: | :------------------------: |
|    OS     |     Ubuntu 24.04.4 LTS     |
| Processor |  Intel CoreTM i5-14600KF   |
|  Memory   |          32.0 GiB          |
| Graphics  | NVIDIA GeForce RTX 5060 Ti |

该配置在不同复杂度的场景下的 SSGI 性能消耗为（1-2ms），更高的分辨率缩放（resolutionscale）能显著提高渲染性能。

```{attention}
- SSGI 需要硬件支持 Compute Shader 计算，集成显卡不建议开启 SSGI。
```

## 灯光与材质

前面介绍了全局光照，那么想达到更加真实的渲染效果还需要合理的灯光和材质配置。

### 灯光与阴影

万物皆有影，没有阴影场景就会显得比较平。阴影开启/关闭对比：

|                    开启阴影                     |                  关闭阴影                  |
| :---------------------------------------------: | :----------------------------------------: |
| ![](/_static/images/render/correct_shading.png) | ![](/_static/images/render/shadow_off.png) |

如果没有阴影需检查`render_settings.enable_shadow`设置是否为 true，mjcf 文件灯光标签里`castshadow`是否为 true

```{attention}
- 过多的灯光和阴影会导致性能下降严重，不适合在多世界仿真训练模拟里采用大量的独立聚光灯和点光源。使用全局方向光替代。
```

### 材质质感

为了正确的还原真实物体的材质质感需要正确的配置材质参数`reflectance`、`roughness`、`metallic`：

```xml
<asset>
  <material name="mat_sample_m_0_r_0" rgba="0.8 0.8 0.8 1.0"
    reflectance="0.5"
    roughness="0.0"
    metallic="0.0"
  />
</asset>
```

#### 核心概念

-   **reflectance（反射率）**: 0 - 1 控制材质的反射率，调整反射的强弱（只影响非金属）, 一般默认 0.5
-   **roughness（粗糙度）**: 0 - 1 控制表面的粗糙程度
-   **metallic（金属性）**: 0 或 1 确定非金属或金属（一般不用中间值，除非要表达 NPR 质感）

#### 核心参数质感示例

```{figure} /_static/images/render/metallic0_roughness0-1.png
:alt: reflectance = 0.5，metallic = 0.0， roughness 0.0 - 1.0 从左到右
:width: 100%

**reflectance = 0.5，metallic = 0.0， roughness 0.0 - 1.0 从左到右**
```

```{figure} /_static/images/render/metallic1_roughness0-1.png
:alt: reflectance = 0.5，metallic = 1.0， roughness 0.0 - 1.0 从左到右
:width: 100%

**reflectance = 0.5，metallic = 1.0， roughness 0.0 - 1.0 从左到右**
```

以[go2.xml](../../../../examples/assets/go2/go2_mjx.xml)材质配置为例，正确的材质参数呈现真实的表面质感：

| ![](/_static/images/render/correct_shading.png) | ![](/_static/images/render/incorrect_shading.png) |
| :---------------------------------------------: | :-----------------------------------------------: |
|                 正确的材质参数                  |                  错误的材质参数                   |

## 故障排查

### GI 没有效果

可能导致没有 GI 效果的情况：

-   mjcf 文件标签设置`<ssgi active="true"/>`，Python 脚本设置`render_settings.enable_ssgi = True`，但是`intensity`设置为 0 了
-   mjcf 文件标签设置`<ssgi active="true"/>`，Python 脚本没有设置`render_settings.enable_ssgi = True`
-   mjcf 文件标签没有设置`<ssgi active="true"/>`，Python 脚本设置`render_settings.enable_ssgi = True`
-   mjcf 文件引用不对：mjcf 文件使用了`attach`，而 ssgi 标签设置在了被`attach`的 model 文件，`attach`忽略全局 visual 标签设置

### 场景过暗或过曝

mjcf 文件标签里设置类似下面的效果且没开启 SSGI 将会导致渲染效果较暗：

```xml
<visual>
    <headlight diffuse="0.0 0.0 0.0" ambient="0.0 0.0 0.0" specular="0 0 0"/>
    <map envmapintensity="0.0"/>
</visual>
```

类似下图效果：

![](/_static/images/render/direct_only.png)

如果出现类似下图效果，则说明灯光强度过高，导致渲染画面过曝，颜色失真，需要检查并降低相应的灯光强度和`envmapintensity`强度。

![](/_static/images/render/bright.png)

### 性能明显下降

如果遇到性能下降情况，先关闭 SSGI，测试关闭 SSGI 对帧率下降的影响：

-   SSGI 关闭/开启对帧率的影响很小：
    -   则需要考虑检查多体资产：贴图，模型，碰撞以及多体的配置情况
    -   检查 policy 同步和模拟情况
-   SSGI 关闭/开启对帧率的影响较大：
    -   降低快速全局光照的质量。使用更高的分辨率缩放，减少 GI 计算量
    -   硬件配置过低，关闭 SSGI，仅在离线输出视频或静态图时开启
    -   检查硬件配置，更新硬件

```{attention}
- 目前只有Windows，Linux，Mac 平台支持SSGI， Web端和手机端暂不支持
```

## 相关 API 链接

-   [`render.launch(model)`]

[`render.launch(model)`]: motrixsim.render.RenderApp.launch
