# ​🔀 Multi-Environment Parallel Simulation

MotrixSim has built-in multi-environment parallel simulation capabilities, allowing you to easily run high-performance parallel simulations for thousands of model instances.

```{figure} /_static/images/examples/parallelsim.png
:width: 100%
:align: center

Visualization of 900 tidybot instances in parallel simulation with MotrixSim
```

## Creating Multiple Instances

In MotrixSim, creating multiple instances is simple. You just need to pass a `batch` parameter when constructing `SceneData`:

```{literalinclude} ../../../../examples/parallelsim.py
:language: python
:dedent:
:start-after: "# tag::init batch data"
:end-before:  "# end::init batch data"
```

In the example above, we create 30x30=900 model instances. For visualization, we set a different offset position for each instance when launching the renderer, arranging them in a grid on a plane. These 900 instances are automatically distributed across multiple CPU cores for parallel simulation.

```{note}
The render_offset parameter of the renderer only affects the visualization offset and does not affect the actual physical simulation positions of the models.
```

You can also run the above example with the following command:

```sh
uv run examples/parallelsim.py
```

## Accessing Multi-Instance Data

In batch mode, model state data is stored in `SceneData` as batches. All data fields related to Data will automatically have an added batch dimension. For example, position data `dof_pos` will be a 2D array of shape `(batch_size, num_dof_pos)`.

```python
batch = (1000,)
data = mtx.SceneData(model, batch=batch)
assert data.dof_vel.shape == (*batch, model.num_dof_vel)
```

Similarly, data setting interfaces also require an added batch dimension:

```{literalinclude} ../../../../examples/parallelsim.py
:dedent:
:start-after: "# tag:: set actuator ctrl in batch"
:end-before:  "# end:: set actuator ctrl in batch"
```

## Indexing

When SceneData is in batch mode, you can access subsets of instance data in several ways.

### 1. Accessing a Single Instance

```{literalinclude} ../../../../examples/parallelsim.py
:dedent:
:start-after: "# tag:: set actuator ctrl in single"
:end-before:  "# end:: set actuator ctrl in single"
```

In the code above, we access the data of the first instance via `data[0]`. The returned `single_data` is a new SceneData object with shape `()`, indicating scalar instance data. This instance shares memory with the original `data`, so modifications to `single_data` are reflected in `data`.

### 2. Accessing via Mask

SceneData also supports indexing with `NDArray[bool]`, returning a new SceneData containing only the instances where the mask index is True.

```{literalinclude} ../../../../examples/parallelsim.py
:dedent:
:start-after: "# tag:: set actuator ctrl in mask"
:end-before:  "# end:: set actuator ctrl in mask"
```

## Benchmarks

In the examples directory, we provide a simple script `parallel_bench.py` to test MotrixSim's performance in multi-instance parallel simulation. You can run this script with:

```bash
uv run examples/parallel_bench.py --file examples/assets/go1/scene.xml
```

You will get output similar to:

```
Summary: 3000 steps for 1024 instances in 7.101 seconds
Average: 432605.091 steps/second
```

The CPU used in this test: `AMD Ryzen™ 9 9950X × 32`. The results show that MotrixSim can achieve over 400,000 simulation steps per second on this hardware.
