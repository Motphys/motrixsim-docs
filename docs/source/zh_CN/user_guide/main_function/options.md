# ⚙️ 全局设置（Options）

`Options` 是 MotrixSim 中的全局配置对象，用于设置物理仿真的各项参数。这些参数会影响仿真的精度、稳定性和性能。

## 基本概念

常用的配置参数包括：

| 参数             | 说明                     | 默认值        |
| ---------------- | ------------------------ | ------------- |
| `timestep`       | 仿真时间步长（秒）       | 0.002         |
| `gravity`        | 重力加速度 [x, y, z]     | [0, 0, -9.81] |
| `max_iterations` | 约束求解器的最大迭代次数 | 100           |

## 配置方式

### 通过 XML 配置

在 MJCF 文件中，可以使用 `<option>` 标签来配置参数：

```xml
<mujoco>
    <option timestep="0.002" gravity="0 0 -9.81" iterations="100"/>
</mujoco>
```

### 通过代码配置

可以通过 `SceneModel` 的 `options` 属性来获取和修改配置。

```{literalinclude} ../../../../examples/options.py
:language: python
:dedent:
:start-after: "# tag::options_code[]"
:end-before:  "# end::options_code[]"
```

完整示例代码参见 [`examples/options.py`](../../../../examples/options.py)。

## API Reference

更多与 Options 相关的 API，请参考 [`Options API`]

[`Options API`]: motrixsim.Options
