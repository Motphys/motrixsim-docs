# 🖥️ 无 GPU 环境下的 CPU 软渲染

在一些环境中没有可用的渲染 GPU（例如只配了计算卡的算力中心节点、不带显卡的云主机或 CI runner），但仍然希望在跑完仿真/训练之后离线生成回放视频或截图。本章介绍如何让 MotrixSim 的 [headless 渲染](../main_function/managed_viewer.md)运行在纯 CPU 的软件光栅化路径上。

```{note}
CPU 软渲染只适合**离线**生成图像/视频（训练效果回放、批量截图、自动化测试），不适合实时交互。软件光栅化的帧率远低于 GPU。
```

## 原理

MotrixSim 的渲染底层基于 wgpu。wgpu 不会直接操作 GPU，而是通过一个图形 API（Vulkan / Metal / DX12 / GL）后端工作。因此只要提供一个**软件实现的 Vulkan 驱动**，整条渲染管线就能在 CPU 上跑：

-   **lavapipe / llvmpipe**（由 Mesa 提供）—— Vulkan / OpenGL 的纯 CPU 软件实现，是最常用、最易获取的方案。

只要装好 lavapipe，wgpu 会把它当成一个 `Cpu` 类型的 adapter 选中，渲染结果与 GPU 路径一致，只是更慢。

## 环境准备

以 Ubuntu/Debian 为例，安装 Mesa 的 Vulkan 驱动（包含 lavapipe）。下面用于验证的 `vulkaninfo` 由单独的 `vulkan-tools` 包提供，因此一并安装：

```bash
sudo apt-get install -y mesa-vulkan-drivers vulkan-tools
```

安装后会得到软件 Vulkan 驱动 `libvulkan_lvp.so` 以及对应的 ICD 描述文件，通常是 `/usr/share/vulkan/icd.d/lvp_icd.json`。其确切文件名在不同发行版/Mesa 版本下可能不同（部分会带架构后缀，如 `lvp_icd.x86_64.json`），可用下面命令列出本机的实际路径：

```bash
ls /usr/share/vulkan/icd.d/lvp_icd*.json
```

可用 `vulkaninfo` 确认 lavapipe 可用（输出里应出现 `llvmpipe` / `driverName = llvmpipe`）：

```bash
vulkaninfo | grep -iE 'deviceName|driverName'
```

```{note}
在**本身没有任何 GPU** 的机器上，装好 `mesa-vulkan-drivers` 后，wgpu 通常会自动选中 lavapipe，无需任何额外配置。下面的环境变量主要用于在**同时装有 GPU 驱动**的机器上强制走软渲染（例如本地复现无 GPU 行为）。
```

## 运行

设置以下环境变量，把 Vulkan loader 限制到只加载 lavapipe，从而强制走 CPU 软渲染：

```bash
# 路径请用上面 `ls` 列出的实际文件名，架构后缀可能不同。
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json
export WGPU_BACKEND=vulkan
```

-   `VK_ICD_FILENAMES` 指向 lavapipe 的 ICD 文件后，Vulkan loader 会忽略机器上其它（GPU 的）ICD，从而保证选中 CPU adapter。这比 `WGPU_POWER_PREF=low` 更可靠——后者在有独显时仍可能选到 GPU。
-   `WGPU_BACKEND=vulkan` 显式指定走 Vulkan 后端。

之后正常运行你的 headless 渲染脚本即可。下面是一个最小的 headless 截图示例，使用 [`RenderApp`] 的 `headless=True` 模式，把系统相机渲染到离屏图像并读取像素：

```{literalinclude} ../../../../examples/viewer/headless.py
:language: python
:dedent:
:start-after: "with RenderApp(headless=True) as renderer:"
:end-before:  "image_index = 0"
```

完整示例见 [`examples/viewer/headless.py`](../../../../examples/viewer/headless.py)。运行：

```bash
# ICD 路径请替换为上面 `ls` 找到的实际文件。
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json \
WGPU_BACKEND=vulkan \
  python examples/viewer/headless.py
```

## 限制与注意事项

```{warning}
软件光栅化非常慢，仅适合离线出图，切勿用于实时可视化或对帧率敏感的场景。
```

-   **依赖**：只需要 Mesa lavapipe，不需要 NVIDIA/AMD 驱动，也不需要 `/dev/dri` 设备。
-   **不支持的高级特性**：依赖 GPU 能力的高级渲染特性（如光线追踪、DLSS 等）在软渲染下不可用；建议关闭这类特性，使用基础 PBR 渲染。
-   **退出**：headless 模式下需要让脚本在渲染/采集到所需帧数后主动结束循环（参考示例中的计数退出），否则进程会一直运行。

## 相关章节

-   [📷 相机（Camera）](camera.md)：系统相机、场景相机与离屏渲染目标的配置。
-   [🎮 交互式查看器](../main_function/managed_viewer.md)：headless 与渲染器的整体说明。
-   [🛠️ 安装 Python SDK](../getting_started/installation.md)：CPU/GPU 平台支持与安装。

[`RenderApp`]: motrixsim.render.RenderApp
