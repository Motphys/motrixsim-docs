# 🌡️ 传感器（Sensor）

通过配置传感器，用户可以更方便的获取物理对象状态信息，如位置，旋转，速度，加速度等。传感器不会影响到物理仿真的结果，可以添加在不同的对象上，如刚体（Body），参考点（Site）等。传感器的配置示例可参考 [`examples/assets/site_and_sensor.xml`](../../../../examples/assets/site_and_sensor.xml)

## 现在已经支持的传感器如下：

| 类型                          | 作用                                                                 | 返回值                     |
| :---------------------------- | :------------------------------------------------------------------- | :------------------------- |
| 加速度计（accelerometer）     | 三轴加速度计，用于测量安装点的线性加速度                             | `list[float]` <br> 长度：3 |
| 速度计（velocimeter）         | 三轴速率计， 用于测量安装点的线性速度                                | `list[float]` <br> 长度：3 |
| 角速度计（gryo）              | 用于测量安装点的角速度                                               | `list[float]` <br> 长度：3 |
| 扭矩计（torque）              | 用于测量安装点的扭矩大小                                             | `list[float]` <br> 长度：3 |
| 关节位置（jointpos）          | 用于测量关节的位置或角度                                             | `list[float]` <br> 长度：1 |
| 关节速度（jointvel）          | 用于测量关节的线速度或角速度                                         | `list[float]` <br> 长度：1 |
| 参考框位置（framepos）        | 参考框在全局坐标系下或指定参考坐标系下的位置                         | `list[float]` <br> 长度：3 |
| 参考框旋转（framequat）       | 参考框在全局坐标系下的旋转四元数                                     | `list[float]` <br> 长度：4 |
| 参考框 X 轴（framexaxis）     | 参考框 X 轴在全局坐标系中的单位向量                                  | `list[float]` <br> 长度：3 |
| 参考框 Y 轴（frameyaxis）     | 参考框 Y 轴在全局坐标系中的单位向量                                  | `list[float]` <br> 长度：3 |
| 参考框 Z 轴（framezaxis）     | 参考框 Z 轴在全局坐标系中的单位向量                                  | `list[float]` <br> 长度：3 |
| 参考框线速度（framelinvel）   | 参考框在全局坐标系下的线速度                                         | `list[float]` <br> 长度：3 |
| 参考框角速度（frameangvel）   | 参考框在全局坐标系下的角速度                                         | `list[float]` <br> 长度：3 |
| 参考框线加速度（framelinacc） | 参考框在全局坐标系下的线加速度                                       | `list[float]` <br> 长度：3 |
| 参考框角加速度（frameangacc） | 参考框在全局坐标系下的角加速度                                       | `list[float]` <br> 长度：3 |
| 子树质心（subtreecom）        | 返回以指定刚体为根节点的运动学子树的质心（以全局坐标系表示）         | `list[float]` <br> 长度：3 |
| 子树线速度（subtreelinvel）   | 返回以指定刚体为根节点的运动学子树的质心的线速度（以全局坐标系表示） | `list[float]` <br> 长度：3 |
| 子树角动量（subtreeangmom）   | 返回以指定刚体为根节点的运动学子树质心处的角动量（以全局坐标系表示） | `list[float]` <br> 长度：3 |

## 相关 API 使用示例：

获取某个指定的"sensor_name"的传感器数据

```{literalinclude} ../../../../examples/site_and_sensor.py
:language: python
:dedent:
:start-after: "# tag::get_sensor_value[]"
:end-before:  "# end::get_sensor_value[]"
```

获取模型中所有的传感器数据

```{literalinclude} ../../../../examples/site_and_sensor.py
:language: python
:dedent:
:start-after: "# tag::get_sensor_values[]"
:end-before:  "# end::get_sensor_values[]"
```

完整实例代码参见 [`examples/site_and_sensor.py`](../../../../examples/site_and_sensor.py)
