# 🎲 参数随机化

MotrixSim 提供了参数随机化（Domain Randomization）能力，允许您在多环境并行仿真中为每个实例设置不同的物理参数。这对于 Sim-to-Real 迁移和强化学习训练至关重要。

## 支持的随机化参数总览

| 属性         | 对象         | 设置方法                      | 获取方法                      | 数据维度     |
| :----------- | :----------- | :---------------------------- | :---------------------------- | :----------- |
| 质量         | `Link`       | `set_mass_override`           | `get_mass_override`           | `(batch,)`   |
| 质心         | `Link`       | `set_center_of_mass_override` | `get_center_of_mass_override` | `(batch, 3)` |
| 摩擦力       | `Geom`       | `set_friction_override`       | `get_friction_override`       | `(batch, 3)` |
| 几何体尺寸   | `Geom*`      | `set_size_override`           | `get_size_override`           | `(batch, N)` |
| 电枢惯量     | `Joint`      | `set_armature_override`       | `get_armature_override`       | `(batch,)`   |
| 关节摩擦损耗 | `Joint`      | `set_frictionloss_override`   | `get_frictionloss_override`   | `(batch,)`   |
| 比例增益     | `Actuator`   | `set_kp_override`             | `get_kp_override`             | `(batch,)`   |
| 阻尼增益     | `Actuator`   | `set_damping_override`        | `get_kd_override`             | `(batch,)`   |
| 重力         | `SceneModel` | `set_gravity_override`        | `get_gravity_override`        | `(batch, 3)` |

```{note}
所有 override 方法都作用于 `SceneData`，不会修改 `SceneModel` 本身。这使得同一个模型可以在不同实例中使用不同的参数。
```

## 核心概念

参数随机化通过 **Override API** 实现。Override 作用于 `SceneData` 而非 `SceneModel`，这意味着同一个模型的不同仿真实例可以拥有不同的物理参数，而无需重新加载模型。

基本使用模式：

```python
# 创建批量仿真数据
data = mtx.SceneData(model, batch=(16,))

# 获取模型对象
link = model.get_link("body_name")

# 设置 override（shape 包含 batch 维度）
mass = np.random.uniform(0.1, 10.0, size=(16,))
link.set_mass_override(data, mass)

# 读取 override
mass_get = link.get_mass_override(data)
```

## 支持的随机化参数

### 连杆参数

#### 质量随机化

通过 `Link.set_mass_override` 修改连杆质量，影响物体的惯性和重力表现。

```{figure} /_static/images/examples/randomize_mass.jpg
:width: 100%
:align: center
```

```{literalinclude} ../../../../examples/randomize/mass.py
:language: python
:dedent:
:lines: 27-47
```

完整示例：[`examples/randomize/mass.py`](../../../../examples/randomize/mass.py)

#### 质心随机化

通过 `Link.set_center_of_mass_override` 修改连杆质心位置，影响物体的旋转行为和稳定性。

```{figure} /_static/images/examples/randomize_com.jpg
:width: 100%
:align: center
```

```python
com_offset = np.zeros((16, 3), dtype=np.float32)
com_offset[:, 0] = np.random.uniform(-0.25, 0.25, 16)
link.set_center_of_mass_override(data, com_offset)
```

完整示例：[`examples/randomize/com.py`](../../../../examples/randomize/com.py)

### 几何体参数

#### 摩擦力随机化

通过 `Geom.set_friction_override` 修改几何体的摩擦系数。摩擦系数是一个 3 维向量 `(slide, spin, roll)`。

```{figure} /_static/images/examples/randomize_friction.jpg
:width: 100%
:align: center
```

```python
geom = model.get_geom("box_geom")
frictions = np.zeros((16, 3), dtype=np.float32)
frictions[:, 0] = np.linspace(0.01, 2.0, 16)  # slide friction
geom.set_friction_override(data, frictions)
```

完整示例：[`examples/randomize/friction.py`](../../../../examples/randomize/friction.py)

#### 几何体尺寸随机化

通过各几何体子类的 `set_size_override` 方法修改碰撞体尺寸。不同几何体类型的 size 维度不同：

```{figure} /_static/images/examples/randomize_geom_size.jpg
:width: 100%
:align: center
```

| 几何体类型      | size 维度 | 含义           |
| :-------------- | :-------- | :------------- |
| `GeomSphere`    | 1         | 半径           |
| `GeomCapsule`   | 2         | 半径, 半高     |
| `GeomCuboid`    | 3         | X/Y/Z 方向半长 |
| `GeomCylinder`  | 2         | 半径, 半高     |
| `GeomEllipsoid` | 3         | X/Y/Z 方向半径 |

```python
from motrixsim import GeomSphere

sphere = model.get_geom("sphere")
assert isinstance(sphere, GeomSphere)
radii = np.random.uniform(0.1, 0.8, size=(16, 1)).astype(np.float32)
sphere.set_size_override(data, radii)
```

完整示例：[`examples/randomize/geom_size.py`](../../../../examples/randomize/geom_size.py)

### 关节参数

#### 电枢惯量随机化

通过 `Joint.set_armature_override` 修改关节的电枢惯量（虚拟转动惯量），影响关节的动态响应速度。

```{figure} /_static/images/examples/randomize_armature.jpg
:width: 100%
:align: center
```

```python
joint = model.get_joint("rotor_joint")
armature = np.linspace(0.1, 5.0, 16).astype(np.float32)
joint.set_armature_override(data, armature)
```

完整示例：[`examples/randomize/armature.py`](../../../../examples/randomize/armature.py)

#### 关节摩擦损耗随机化

通过 `Joint.set_frictionloss_override` 修改关节的库仑干摩擦，影响关节的阻力特性。

```{figure} /_static/images/examples/randomize_frictionloss.jpg
:width: 100%
:align: center
```

```python
joint = model.get_joint("pendulum_hinge")
frictionloss = np.linspace(0.0, 200.0, 16).astype(np.float32)
joint.set_frictionloss_override(data, frictionloss)
```

完整示例：[`examples/randomize/frictionloss.py`](../../../../examples/randomize/frictionloss.py)

### 驱动器参数

#### Kp/Kd 随机化

通过 `Actuator.set_kp_override` 和 `Actuator.set_damping_override` 修改位置驱动器的比例增益和阻尼增益。

```{figure} /_static/images/examples/randomize_actuator_kp_kd.jpg
:width: 100%
:align: center
```

```python
actuator = model.get_actuator("servo")
kp = np.array([10.0, 30.0, 60.0, 120.0], dtype=np.float32)
kd = np.array([1.0, 3.0, 8.0, 20.0], dtype=np.float32)
actuator.set_kp_override(data, kp)
actuator.set_damping_override(data, kd)
```

完整示例：[`examples/randomize/actuator_kp_kd.py`](../../../../examples/randomize/actuator_kp_kd.py)

### 场景参数

#### 重力方向随机化

通过 `SceneModel.set_gravity_override` 修改每个实例的重力向量。

```{figure} /_static/images/examples/randomize_gravity_direction.jpg
:width: 100%
:align: center
```

```python
gravity = np.random.randn(16, 3).astype(np.float32)
gravity /= np.linalg.norm(gravity, axis=1, keepdims=True)
gravity *= 9.81
model.set_gravity_override(data, gravity)
```

完整示例：[`examples/randomize/gravity_direction.py`](../../../../examples/randomize/gravity_direction.py)
