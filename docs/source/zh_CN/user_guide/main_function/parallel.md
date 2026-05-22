# ​🔀 多环境并行仿真

MotrixSim 内置了多环境并行仿真能力， 可以让您非常轻松地对数千个模型实例进行高性能并行仿真。

```{figure} /_static/images/examples/parallelsim.png
:width: 100%
:align: center

MotrixSim 并行仿真 900 个 tidybot 实例的可视化效果
```

## 创建多实例

在 MotrixSim 中，想要创建多实例非常简单，您只需要在构造`SceneData`时， 传入一个 batch 参数:

```{literalinclude} ../../../../examples/parallel/parallelsim.py
:language: python
:dedent:
:start-after: "# tag::init batch data"
:end-before:  "# end::init batch data"
```

在上面的例子中，我们创建了 30x30=900 个模型实例， 为了可视化方便，我们在启动渲染器的时候为每个实例都设置了一个不同的偏移位置，让其分布在一个平面网格上。 这 900 个实例会被自动分配到 CPU 的多个核心上进行并行仿真。

```{note}
渲染器的render_offset参数只影响可视化时的位置偏移， 并不会影响物理仿真本身的模型位置。
```

您也可以通过如下命令来运行上述的例子:

```sh
uv run examples/parallel/parallelsim.py
```

## 访问多实例数据

在多实例模式下，模型的状态数据会以批量的形式存储在 `SceneData` 中。所有与 Data 相关的数据字段都会自动增加一个 Batch 维度。 例如，位置数据 `dof_pos` 会是一个形状为 `(batch_size, num_dof_pos)` 的二维数组。

```python
batch = (1000,)
data = mtx.SceneData(model, batch=batch)
assert data.dof_vel.shape == (*batch, model.num_dof_vel)
```

同时，与 Data 相关的数据设置接口，也需要增加一个 Batch 维度:

```{literalinclude} ../../../../examples/parallel/parallelsim.py
:dedent:
:start-after: "# tag:: set actuator ctrl in batch"
:end-before:  "# end:: set actuator ctrl in batch"
```

## 索引

当 SceneData 处于批量模式时，我们可以通过几种不同的索引方式来访问其中的部分实例数据

### 1. 访问单个实例

```{literalinclude} ../../../../examples/parallel/parallelsim.py
:dedent:
:start-after: "# tag:: set actuator ctrl in single"
:end-before:  "# end:: set actuator ctrl in single"
```

上面的代码中，我们通过`data[0]`访问了第一个实例的数据， 这里返回的`single_data`是一个新的 SceneData 对象， 其 shape 为 `()`，表示这是一个标量实例数据。 该实例数据与原始的`data`共享内存， 因此对`single_data`的修改会直接反映到原始的`data`上。

### 2. 通过 mask 来访问

SceneData 也支持通过`NDArray[bool]`进行索引，返回新的 SceneData 将只包含 mask 中 index 为 True 的那些实例

```{literalinclude} ../../../../examples/parallel/parallelsim.py
:dedent:
:start-after: "# tag:: set actuator ctrl in mask"
:end-before:  "# end:: set actuator ctrl in mask"
```

## Bench

在 examples 目录下，我们提供了一个简单的脚本`parallel_bench.py`， 用于测试 MotrixSim 在多实例并行仿真下的性能表现。您可以通过下面的命令来运行这个脚本:

```bash
uv run examples/parallel/parallel_bench.py --file examples/assets/go1/scene.xml
```

会得到类似下面的输出:

```
Summary: 3000 steps for 1024 instances in 7.101 seconds
Average: 432605.091 steps/second
```

上述测试的 CPU 型号为: `AMD Ryzen™ 9 9950X × 32`， 该测试结果表明 MotrixSim 在该硬件上可以达到每秒超过 40 万步的仿真速度。
