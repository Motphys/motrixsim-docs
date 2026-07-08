# 🖥️ CPU Software Rendering on GPU-less Machines

In some environments there is no usable rendering GPU (for example a compute-only node in a data center, a cloud host without a graphics card, or a CI runner), yet you still want to generate replay videos or screenshots offline after running a simulation/training. This chapter explains how to run MotrixSim's [headless rendering](../main_function/managed_viewer.md) on a pure-CPU software rasterization path.

```{note}
CPU software rendering is only suitable for **offline** image/video generation (training-result replay, batch screenshots, automated tests), not for real-time interaction. The frame rate of software rasterization is far lower than a GPU.
```

## How it works

MotrixSim's rendering is built on top of wgpu. wgpu does not drive the GPU directly; it works through a graphics-API backend (Vulkan / Metal / DX12 / GL). Therefore, as long as a **software implementation of Vulkan** is available, the whole rendering pipeline can run on the CPU:

-   **lavapipe / llvmpipe** (provided by Mesa) — a pure-CPU software implementation of Vulkan / OpenGL, and the most common and easily obtained option.

Once lavapipe is installed, wgpu selects it as a `Cpu` adapter. The rendered result is identical to the GPU path, only slower.

## Prerequisites

Taking Ubuntu/Debian as an example, install Mesa's Vulkan drivers (which include lavapipe). The `vulkaninfo` tool used for verification below is provided by the separate `vulkan-tools` package, so install both:

```bash
sudo apt-get install -y mesa-vulkan-drivers vulkan-tools
```

This provides the software Vulkan driver `libvulkan_lvp.so` and its ICD descriptor file, usually `/usr/share/vulkan/icd.d/lvp_icd.json`. The exact filename can vary across distros and Mesa versions (some carry an architecture suffix such as `lvp_icd.x86_64.json`), so list it to find the real path on your machine:

```bash
ls /usr/share/vulkan/icd.d/lvp_icd*.json
```

You can confirm lavapipe is available with `vulkaninfo` (the output should contain `llvmpipe` / `driverName = llvmpipe`):

```bash
vulkaninfo | grep -iE 'deviceName|driverName'
```

```{note}
On a machine that has **no GPU at all**, once `mesa-vulkan-drivers` is installed, wgpu usually selects lavapipe automatically with no extra configuration. The environment variables below are mainly used to force software rendering on a machine that **also has GPU drivers installed** (for example, to reproduce the GPU-less behavior locally).
```

## Running

Set the following environment variables to restrict the Vulkan loader to lavapipe only, forcing the CPU software rendering path:

```bash
# Use the path you found with `ls` above; the architecture suffix may differ.
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json
export WGPU_BACKEND=vulkan
```

-   With `VK_ICD_FILENAMES` pointing to lavapipe's ICD file, the Vulkan loader ignores the other (GPU) ICDs on the machine, ensuring the CPU adapter is selected. This is more reliable than `WGPU_POWER_PREF=low`, which may still pick the GPU when a discrete card is present.
-   `WGPU_BACKEND=vulkan` explicitly selects the Vulkan backend.

Then run your headless rendering script as usual. Below is a minimal headless screenshot example that uses [`RenderApp`] in `headless=True` mode, renders the system camera to an off-screen image, and reads back the pixels:

```{literalinclude} ../../../../examples/viewer/headless.py
:language: python
:dedent:
:start-after: "with RenderApp(headless=True) as renderer:"
:end-before:  "image_index = 0"
```

See the full example at [`examples/viewer/headless.py`](../../../../examples/viewer/headless.py). Run it with:

```bash
# Adjust the ICD path to match the file found by `ls` above.
VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json \
WGPU_BACKEND=vulkan \
  python examples/viewer/headless.py
```

## Limitations and notes

```{warning}
Software rasterization is very slow and is only suitable for offline image generation. Do not use it for real-time visualization or frame-rate-sensitive scenarios.
```

-   **Dependencies**: only Mesa lavapipe is required — no NVIDIA/AMD driver and no `/dev/dri` device are needed.
-   **Unsupported advanced features**: advanced rendering features that rely on GPU capabilities (such as ray tracing, DLSS, etc.) are unavailable under software rendering; it is recommended to disable such features and use basic PBR rendering.
-   **Exiting**: in headless mode the script must break out of its loop once it has rendered/captured the desired number of frames (see the counter-based exit in the example), otherwise the process keeps running.

## Related chapters

-   [📷 Camera](camera.md): configuring the system camera, scene cameras, and off-screen render targets.
-   [🎮 Interactive Viewer](../main_function/managed_viewer.md): an overview of headless mode and the renderer.
-   [🛠️ Install Python SDK](../getting_started/installation.md): CPU/GPU platform support and installation.

[`RenderApp`]: motrixsim.render.RenderApp
