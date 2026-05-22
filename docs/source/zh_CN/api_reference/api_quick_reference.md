# 🚀 API 快速参考

## 📋 核心模块 - [`motrixsim`](core/motrixsim.md)

| 功能类别     | API                                                             | 说明                    |
| ------------ | --------------------------------------------------------------- | ----------------------- |
| **模型加载** | [`load_model(path)`](motrixsim.load_model)                      | 加载 MJCF/URDF 模型文件 |
| **仿真步进** | [`step(model, data)`](motrixsim.step)                           | 执行一个仿真时间步      |
| **运动学**   | [`forward_kinematic(model, data)`](motrixsim.forward_kinematic) | 前向运动学计算          |

### 🔧 核心对象

| 对象                                 | 类型 | 用途描述                                           |
| ------------------------------------ | ---- | -------------------------------------------------- |
| [`SceneModel`](motrixsim.SceneModel) | 模型 | 静态仿真世界描述，包含机器人几何、关节、传感器定义 |
| [`SceneData`](motrixsim.SceneData)   | 数据 | 动态仿真状态，存储位置、速度等实时数据             |
| [`Options`](motrixsim.Options)       | 配置 | 仿真参数设置，控制积分器、求解器参数               |

---

### 🔍 Named Access - 模型组件访问

MotrixSim 为模型组件提供便捷的命名访问接口，支持通过名称或索引直接访问和操作各种组件。

#### 🔧 访问方式

MotrixSim 的 Named Access 支持两种访问方式：

-   **按名称访问**：`model.get_body("my_body")`
-   **按索引访问**：`model.get_body(0)`

每个组件访问方法都返回对应的组件对象，提供该组件的属性和操作方法。

#### 🎯 模型组件

| 组件         | 访问方法                                                                    | 返回对象功能            | 索引查询                                                              |
| ------------ | --------------------------------------------------------------------------- | ----------------------- | --------------------------------------------------------------------- |
| **Body**     | [`model.get_body(name/id)`](motrixsim.SceneModel.get_body)                  | 获取刚体位姿、DoF 状态  | [`get_body_index(name)`](motrixsim.SceneModel.get_body_index)         |
| **Link**     | [`model.get_link(name/id)`](motrixsim.SceneModel.get_link)                  | 获取连杆位姿、速度      | [`get_link_index(name)`](motrixsim.SceneModel.get_link_index)         |
| **Joint**    | [`model.get_joint(name/id)`](motrixsim.SceneModel.get_joint)                | 设置/获取关节位置、速度 | [`get_joint_index(name)`](motrixsim.SceneModel.get_joint_index)       |
| **Site**     | [`model.get_site(name/id)`](motrixsim.SceneModel.get_site)                  | 获取参考点位置、朝向    | [`get_site_index(name)`](motrixsim.SceneModel.get_site_index)         |
| **Sensor**   | [`model.get_sensor_value(id, data)`](motrixsim.SceneModel.get_sensor_value) | 读取传感器数据          | -                                                                     |
| **Actuator** | [`model.get_actuator(name/id)`](motrixsim.SceneModel.get_actuator)          | 设置执行器控制、限制    | [`get_actuator_index(name)`](motrixsim.SceneModel.get_actuator_index) |

#### 🔢 批量访问

| API                                                                         | 类型        | 说明                     |
| --------------------------------------------------------------------------- | ----------- | ------------------------ |
| [`model.get_actuator_ctrls(data)`](motrixsim.SceneModel.get_actuator_ctrls) | ndarray     | 获取所有执行器控制值     |
| [`model.get_link_poses(data)`](motrixsim.SceneModel.get_link_poses)         | ndarray     | 获取所有连杆的位置和旋转 |
| [`model.bodies`](motrixsim.SceneModel.bodies)                               | List[Body]  | 所有刚体对象列表         |
| [`model.links`](motrixsim.SceneModel.links)                                 | List[Link]  | 所有连杆对象列表         |
| [`model.joints`](motrixsim.SceneModel.joints)                               | List[Joint] | 所有关节对象列表         |
| [`model.sites`](motrixsim.SceneModel.sites)                                 | List[Site]  | 所有参考点对象列表       |

---

### 📊 SceneData - 状态数据

| 属性/方法                                                   | 类型    | 说明                       |
| ----------------------------------------------------------- | ------- | -------------------------- |
| [`data.dof_pos`](motrixsim.SceneData.dof_pos)               | ndarray | DoF 位置数组               |
| [`data.dof_vel`](motrixsim.SceneData.dof_vel)               | ndarray | DoF 速度数组               |
| [`data.actuator_ctrls`](motrixsim.SceneData.actuator_ctrls) | ndarray | 设置/获取执行器控制值      |
| [`data.reset(model)`](motrixsim.SceneData.reset)            | -       | 重置场景数据状态           |
| [`data.low`](motrixsim.SceneData.low)                       | LowData | 底层数据对象（接触信息等） |

---

## 🔨 模型构建模块 - [`motrixsim.msd`](msd/index.md)

| 函数/方法                                                | 说明                            |
| -------------------------------------------------------- | ------------------------------- |
| [`msd.from_file(path)`](motrixsim.msd.from_file)         | 加载模型文件用于组合和构建      |
| [`world.attach(other, ...)`](motrixsim.msd.World.attach) | 附加另一个模型并设置变换和前缀  |
| [`world.build()`](motrixsim.msd.build)                   | 构建用于仿真的最终 `SceneModel` |

---

## 🎨 渲染模块 - [`motrixsim.render`](rendering/render.md)

| 对象/类                                         | 类别     | 主要功能             |
| ----------------------------------------------- | -------- | -------------------- |
| [`RenderApp`](motrixsim.render.RenderApp)       | 主渲染器 | 模型加载、场景同步   |
| [`RenderGizmos`](motrixsim.render.RenderGizmos) | 即时绘制 | 球体、立方体绘制     |
| [`RenderUI`](motrixsim.render.RenderUI)         | 用户界面 | 按钮、开关控件       |
| [`Input`](motrixsim.render.Input)               | 输入处理 | 键盘、鼠标、射线检测 |
