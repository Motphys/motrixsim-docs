# 📷 Camera

## System Camera

When you use the renderer feature, MotrixSim automatically creates a system camera. The system camera accepts user mouse operations to enable movement, zooming, and other functions.

```{video} /_static/videos/store_motrixsim.mp4
:poster: /_static/images/poster/store_motrixsim.jpg
:caption: System camera operation effects
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

Operation Instructions:

-   Press and drag left mouse button: Rotate camera around focal point
-   Press and drag right mouse button: Move focal point (red circle indicates current focal point)
-   Mouse wheel: Zoom in/out (cannot zoom in further when reaching focal point)

The system camera supports partial configurations from [mjcf/visual/global](https://mujoco.readthedocs.io/en/stable/XMLreference.html#visual-global), such as:

-   orthographic: Whether to use orthographic projection
-   fovy: Camera field of view
-   azimuth: Initial azimuth angle (rotation around z-axis) of system camera
-   elevation: Initial elevation angle (pitch) of system camera

The system camera can be enabled/disabled.

```
system_camera = render.system_camera # get system camera
system_camera.active = True # enable camera
system_camera.active = False # disable camera
```

## Scene Camera

In addition to the system camera, you can configure additional Camera tags in MJCF files. We refer to these as scene cameras. Scene cameras can provide additional viewing angles for visualization.

### Custom Additional Cameras

Taking [go1.xml](../../../../examples/assets/go1/go1_mjx_fullcollisions.xml) as an example, we define cameras in MJCF as follows:

```xml
<body name="trunk" pos="0 0 0.445" childclass="go1">
    <camera name="track" pos="0.846 -1.3 0.316" xyaxes="0.866 0.500 0.000 -0.171 0.296 0.940" mode="track"/>
    <camera name="top" pos="-1 0 1" xyaxes="0 -1 0 0.7 0 0.7" mode="track"/>
    <camera name="side" pos="0 -2 1" xyaxes="1 0 0 0 1 2" mode="track"/>
    <camera name="back" pos="-2.4 0 0.8" target="trunk" mode="targetbody"/>
</body>
```

This means we've defined 4 additional cameras on the go1's trunk. The camera position and orientation are specified by pos and xyaxes, while mode specifies the camera's movement mode.

Similarly, the scene camera can also be enabled/disabled.

```
camera_index = 0 # The first scene camera index
scene_camera = render.get_camera(camera_index) # get scene camera
scene_camera.active = True # enable camera
scene_camera.active = False # disable camera
```

### Switching Scene Main Camera

By default, MotrixSim uses the system camera as the main camera. If you want to use a scene camera as the main camera, you can switch via the Python API:

```python
cameras = model.cameras # Get all cameras (note: system camera not included here)
preview_cameras = [None,*cameras] # None indicates system camera
```

Switch cameras using keyboard events:

```{literalinclude} ../../../../examples/go1.py
:language: python
:dedent:
:start-after: "# tag: switch camera"
:end-before:  "# endtag"

```

```{video} /_static/videos/switch_camera.mp4
:caption: Switch scene main camera using left/right arrow keys
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

### RGBD Sensors

MotrixSim supports converting scene cameras into RGBD vision sensors, allowing you to obtain both RGB images and depth images. You can use the following interface to render a scene camera to an offline image:

```{literalinclude} ../../../../examples/go1.py
:language: python
:dedent:
:start-after: "# tag: camera render target"
:end-before:  "# endtag"

```

By default, the camera uses RGB rendering mode. If you want the camera to only render depth images, you can set the camera's depth_only property to True:

```{literalinclude} ../../../../examples/go1.py
:language: python
:dedent:
:start-after: "# tag: depth camera"
:end-before:  "# endtag"

```

```{note}
The values stored in the depth map are in NDC (normalized device coordinates) space. If you want to convert them to actual distances from the camera in 3D space, you can use the following formula:

view_z = camera.near_plane / depth

```

The real-time effects of the RGBD camera will be displayed in the Camera panel on the left:

```{video} /_static/videos/rgbd_camera.mp4
:caption: The top-right corner displays real-time RGB and depth camera effects
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

### Reading Camera Image Data

To read camera image data, you need to obtain the RenderCamera object from RenderApp and then perform a capture operation.

```{literalinclude} ../../../../examples/go1.py
:language: python
:dedent:
:start-after: "# tag: camera capture"
:end-before:  "# endtag"
```

Note that our capture operation is asynchronous, so the [`RenderCamera.capture`] method will return a CaptureTask object. You need to keep this CaptureTask object and continuously check its status until it is complete. Once finished, you can obtain the image data through the task.take_image() method.

You can refer to the API documentation for more details:

-   [`RenderCamera`]
-   [`CaptureTask`]
-   [`Image`]

[`RenderCamera`]: motrixsim.render.RenderCamera
[`CaptureTask`]: motrixsim.render.CaptureTask
[`Image`]: motrixsim.render.Image
[`RenderCamera.capture`]: motrixsim.render.RenderCamera.capture
