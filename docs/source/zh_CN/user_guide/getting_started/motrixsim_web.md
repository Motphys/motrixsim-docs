# 🌐 网页仿真器

本文介绍如何使用 MotrixSim Web Viewer，包括如何加载文件、如何理解左侧文件树、顶部按钮的作用，以及常用的鼠标和键盘操作方式。

## 打开 Viewer

请使用支持 WebAssembly 的现代浏览器打开 MotrixSim Web Viewer 页面。

仿真页面地址：<https://motrix.motphys.com/>

页面加载完成后，通常会看到：

-   左侧文件面板，其中包含 `Online` 和 `Customize`
-   中间的 3D 视图区域
-   顶部工具栏

```{figure} /_static/images/web_viewer/viewer-overview.jpg
:alt: MotrixSim Web Viewer 界面总览
:width: 90%

MotrixSim Web Viewer 的界面总览，包括左侧文件树、中间 3D 视图和顶部工具栏。
```

## 通过拖拽文件夹加载模型

在 Web 平台上，Viewer 不能像本地桌面程序一样直接访问你的本地文件系统。推荐的使用方式是将包含完整模型资源的整个文件夹拖拽到浏览器窗口中。

### 推荐的文件夹结构

拖拽的文件夹应当包含场景文件以及它依赖的所有资源，例如：

```text
boston_dynamics_spot/
├── scene.xml
├── meshes/
├── textures/
└── ...
```

### 加载步骤

1. 打开 Viewer 页面
2. 将整个模型文件夹拖拽到浏览器窗口
3. 等待左侧 `Customize` 分区出现对应文件
4. 在文件树中点击 `.xml`、`.urdf` 或 `.json` 等场景文件开始加载

```{figure} /_static/images/web_viewer/drag_folder_here.jpg
:alt: 将模型文件夹拖拽到 Web Viewer 页面
:width: 90%

推荐将包含场景文件及其依赖资源的整个模型文件夹拖拽到页面中。
```

```{note}
推荐拖拽整个文件夹，而不是只拖拽场景文件，因为网格、纹理和其他依赖资源通常依赖相对路径一起被解析。
```

## `Online` 与 `Customize` 的区别

左侧文件树包含两个来源。

### `Online`

-   由 Mothphys 提供的官方在线资源

### `Customize`

-   来自你拖拽进页面的文件或文件夹
-   只存在于当前浏览器会话中
-   适合测试你自己的 MJCF、URDF、网格和纹理资源

## 从左侧文件树加载场景

当文件出现在左侧面板后：

1. 展开 `Online` 或 `Customize`
2. 找到目标场景文件
3. 点击该场景文件条目

场景文件会以可点击条目的形式显示在文件树中。点击后会触发资源加载，并将场景加载到 Viewer 中。

## 顶部按钮说明

顶部工具栏包含播放控制和场景操作按钮。

```{figure} /_static/images/web_viewer/buttons.jpg
:alt: MotrixSim Web Viewer 顶部按钮说明
:width: 90%

顶部工具栏中的常用按钮，包括播放控制、场景控制和帮助入口。
```

### 播放控制

-   `Play`：开始或继续仿真
-   `Pause`：暂停仿真
-   `Next`：向前执行一帧

### 场景控制

这些是当前顶栏中明确提供的通用场景控制按钮：

-   `Reset`：将场景状态重置到初始仿真状态
-   `Reload`：重新加载当前模型文件及其资源

### Viewer 自带按钮

MotrixSim viewer 在顶部右侧还可能显示额外按钮，例如：

-   `Help`：打开当前这篇 Web Viewer 操作指南

## 输入指南

下面总结了在 MotrixSim 中最常用的鼠标和键盘操作。

### 鼠标操作

-   左键拖动：围绕场景旋转相机
-   滚轮：缩放
-   中键拖动，或触控板对应手势：平移相机

### 键盘操作

-   `Space`：暂停或继续仿真
-   `F10`：单步执行一帧
-   `Ctrl+E`：重置场景
-   `Ctrl+R`：重新加载当前模型
-   `F11`：在支持的平台上切换全屏

### 物体拖拽交互

如果当前应用配置启用了 physics drag：

-   按住 `Ctrl`
-   用鼠标左键点击可拖拽物体
-   移动鼠标拖动物体

```{video} /_static/videos/physics_drag.mp4
:poster: /_static/images/poster/physics_drag.jpg
:caption: Physics drag 交互示例：按住 Ctrl 后拖拽物体
:playsinline:
:width: 100%
```

## 典型使用流程

1. 打开 Web Viewer
2. 将完整模型文件夹拖拽进页面
3. 在 `Customize` 中点击场景文件
4. 使用鼠标观察场景
5. 使用顶部按钮播放、暂停、重置或重载

## 相关内容

-   [安装指南](installation.md)
-   [Hello MotrixSim](hello_motrixsim.md)
-   [渲染](../main_function/render.md)
