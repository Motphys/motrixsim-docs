# 📷 相机（Camera）

## 系统相机

当您使用渲染器功能时，MotrixSim 会自动创建一个系统相机。 系统相机可以接受用户的鼠标操作，实现移动、缩放等等。

```{video} /_static/videos/store_motrixsim.mp4
:poster: /_static/images/poster/store_motrixsim.jpg
:caption: 系统相机操作效果
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

操作说明：

-   鼠标左键按下并拖动：绕着焦点旋转摄像头
-   鼠标右键按下并拖动：移动焦点（此时显示红圈为焦点）
-   鼠标滚轮：缩放（到焦点位置不可再放大）

系统相机支持[mjcf/visual/global](https://mujoco.readthedocs.io/en/stable/XMLreference.html#visual-global)中的部分配置，例如:

-   orthographic： 是否采用正交投影
-   fovy： 相机视野
-   azimuth： 初始化下，系统相机绕 z 轴的方位角
-   elevation： 初始化下，系统相机的俯仰角

## 场景相机

除了系统相机之外，您可以在 MJCF 文件中配置额外的 Camera 标签。 我们把这种相机称为场景相机。场景相机可以为可视化提供额外的视角

### 自定义额外相机

以[go1.xml](../../../../examples/assets/go1/go1_mjx_fullcollisions.xml)为例，我们在 mjcf 中定义通过如下方式定义了相机:

```xml
<body name="trunk" pos="0 0 0.445" childclass="go1">
    <camera name="track" pos="0.846 -1.3 0.316" xyaxes="0.866 0.500 0.000 -0.171 0.296 0.940" mode="track"/>
    <camera name="top" pos="-1 0 1" xyaxes="0 -1 0 0.7 0 0.7" mode="track"/>
    <camera name="side" pos="0 -2 1" xyaxes="1 0 0 0 1 2" mode="track"/>
    <camera name="back" pos="-2.4 0 0.8" target="trunk" mode="targetbody"/>
</body>
```

这意味着我们在 go1 的 trunk 上定义了 4 个额外的相机。 相机的位置和朝向由 pos 和 xyaxes 指定，mode 指定了相机的运动模式。

### 切换场景主相机

默认情况下，MotrixSim 使用系统相机作为主相机。 如果您想使用场景相机作为主相机，可以在 Python API 中通过如下方式切换:

```python
cameras = model.cameras # 获取所有相机(注意这里不包括系统相机)
preview_cameras = [None,*cameras] # None表示系统相机
```

通过键盘事件切换相机：

```{literalinclude} ../../../../examples/go1.py
:language: python
:dedent:
:start-after: "# tag: switch camera"
:end-before:  "# endtag"

```

```{video} /_static/videos/switch_camera.mp4
:caption: 通过左右按键切换场景主相机
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

### RGBD 传感器

MotrixSim 支持将场景相机转变为 RGBD 视觉传感器，从而允许您获取相机的 RGB 图像和深度图像。 您可以通过以下接口来让一个场景相机渲染到一个离线图片上:

```{literalinclude} ../../../../examples/go1.py
:language: python
:dedent:
:start-after: "# tag: camera render target"
:end-before:  "# endtag"

```

默认情况下，相机采用 RGB 渲染模式。 如果您想让相机只渲染深度图像，可以设置相机的 depth_only 属性为 True:

```{literalinclude} ../../../../examples/go1.py
:language: python
:dedent:
:start-after: "# tag: depth camera"
:end-before:  "# endtag"

```

```{note}
深度图里保存的数值是NDC（normalized device coordinates）空间的。 如果您想将其转换为实际3D空间中与摄像机的距离，可以使用如下公式:

view_z = camera.near_plane / depth

```

RGBD 相机的实时效果会在左侧的 Camera 面板中显示：

```{video} /_static/videos/rgbd_camera.mp4
:caption: 左侧面板展示RGB相机和深度相机实时效果
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

### 读取相机图像数据

要读取相机图像数据，您需要从 RenderApp 上获取 RenderCamera 对象，然后执行 capture 操作。

```{literalinclude} ../../../../examples/go1.py
:language: python
:dedent:
:start-after: "# tag: camera capture"
:end-before:  "# endtag"
```

注意到，我们的 capture 操作是异步的，因此[`RenderCamera.capture`]方法会返回一个 CaptureTask 对象，您需要保存这个 CaptureTask 对象，并持续去检查它的状态，直到它完成。完成后，您可以通过 task.take_image()方法获取图像数据。

您可以看 Api 文档来获取更多细节:

-   [`RenderCamera`]
-   [`CaptureTask`]
-   [`Image`]

[`RenderCamera`]: motrixsim.render.RenderCamera
[`CaptureTask`]: motrixsim.render.CaptureTask
[`Image`]: motrixsim.render.Image
[`RenderCamera.capture`]: motrixsim.render.RenderCamera.capture
