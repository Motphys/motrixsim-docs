# 🚀 API Quick Reference

## 📋 Core Module - [`motrixsim`](core/motrixsim.md)

| Function Category   | API                                                             | Description                            |
| ------------------- | --------------------------------------------------------------- | -------------------------------------- |
| **Model Loading**   | [`load_model(path)`](motrixsim.load_model)                      | Load MJCF/URDF model files             |
| **Simulation Step** | [`step(model, data)`](motrixsim.step)                           | Execute a single simulation time step  |
| **Kinematics**      | [`forward_kinematic(model, data)`](motrixsim.forward_kinematic) | Perform forward kinematics computation |

### 🔧 Core Objects

| Object                               | Type   | Usage Description                                                                             |
| ------------------------------------ | ------ | --------------------------------------------------------------------------------------------- |
| [`SceneModel`](motrixsim.SceneModel) | Model  | Static simulation world description, including robot geometry, joints, and sensor definitions |
| [`SceneData`](motrixsim.SceneData)   | Data   | Dynamic simulation state, storing real-time data such as positions and velocities             |
| [`Options`](motrixsim.Options)       | Config | Simulation parameter settings, controlling integrator and solver parameters                   |

---

### 🔍 Named Access - Model Component Access

MotrixSim provides convenient named access interfaces for model components, supporting direct access and manipulation of various components by name or index.

#### 🔧 Access Methods

MotrixSim's Named Access supports two access methods:

-   **Access by name**: `model.get_body("my_body")`
-   **Access by index**: `model.get_body(0)`

Each component access method returns the corresponding component object, providing its properties and methods.

#### 🎯 Model Components

| Component    | Access Method                                                               | Returned Object Functionality    | Index Query Method                                                    |
| ------------ | --------------------------------------------------------------------------- | -------------------------------- | --------------------------------------------------------------------- |
| **Body**     | [`model.get_body(name/id)`](motrixsim.SceneModel.get_body)                  | Get rigid body pose, DoF state   | [`get_body_index(name)`](motrixsim.SceneModel.get_body_index)         |
| **Link**     | [`model.get_link(name/id)`](motrixsim.SceneModel.get_link)                  | Get link pose, velocity          | [`get_link_index(name)`](motrixsim.SceneModel.get_link_index)         |
| **Joint**    | [`model.get_joint(name/id)`](motrixsim.SceneModel.get_joint)                | Set/get joint position, velocity | [`get_joint_index(name)`](motrixsim.SceneModel.get_joint_index)       |
| **Site**     | [`model.get_site(name/id)`](motrixsim.SceneModel.get_site)                  | Get site position, orientation   | [`get_site_index(name)`](motrixsim.SceneModel.get_site_index)         |
| **Sensor**   | [`model.get_sensor_value(id, data)`](motrixsim.SceneModel.get_sensor_value) | Read sensor data                 | -                                                                     |
| **Actuator** | [`model.get_actuator(name/id)`](motrixsim.SceneModel.get_actuator)          | Set actuator control, limits     | [`get_actuator_index(name)`](motrixsim.SceneModel.get_actuator_index) |

#### 🔢 Batch Access

| API                                                                         | Type        | Description                                 |
| --------------------------------------------------------------------------- | ----------- | ------------------------------------------- |
| [`model.get_actuator_ctrls(data)`](motrixsim.SceneModel.get_actuator_ctrls) | ndarray     | Get all actuator control values             |
| [`model.get_sensor_values(data)`](motrixsim.SceneModel.get_sensor_values)   | ndarray     | Get all sensor values                       |
| [`model.get_link_poses(data)`](motrixsim.SceneModel.get_link_poses)         | ndarray     | Get positions and orientations of all links |
| [`model.bodies`](motrixsim.SceneModel.bodies)                               | List[Body]  | List of all body objects                    |
| [`model.links`](motrixsim.SceneModel.links)                                 | List[Link]  | List of all link objects                    |
| [`model.joints`](motrixsim.SceneModel.joints)                               | List[Joint] | List of all joint objects                   |
| [`model.sites`](motrixsim.SceneModel.sites)                                 | List[Site]  | List of all site objects                    |

---

### 📊 SceneData - State Data

| Property/Method                                             | Type    | Description                                |
| ----------------------------------------------------------- | ------- | ------------------------------------------ |
| [`data.dof_pos`](motrixsim.SceneData.dof_pos)               | ndarray | DoF position array                         |
| [`data.dof_vel`](motrixsim.SceneData.dof_vel)               | ndarray | DoF velocity array                         |
| [`data.actuator_ctrls`](motrixsim.SceneData.actuator_ctrls) | ndarray | Set/get actuator control values            |
| [`data.reset(model)`](motrixsim.SceneData.reset)            | -       | Reset scene data state                     |
| [`data.low`](motrixsim.SceneData.low)                       | LowData | Low-level data object (contact info, etc.) |

---

## 🎨 Rendering Module - [`motrixsim.render`](rendering/render.md)

| Object/Class                                    | Category       | Main Functionality                   |
| ----------------------------------------------- | -------------- | ------------------------------------ |
| [`RenderApp`](motrixsim.render.RenderApp)       | Main Renderer  | Model loading, scene synchronization |
| [`RenderGizmos`](motrixsim.render.RenderGizmos) | Gizmo Drawing  | Drawing spheres, cubes, etc.         |
| [`RenderUI`](motrixsim.render.RenderUI)         | User Interface | Buttons, switches, controls          |
| [`Input`](motrixsim.render.Input)               | Input Handler  | Keyboard, mouse, ray detection       |
