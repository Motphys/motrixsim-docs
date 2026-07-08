# USD 支持参考

本文档列出 MotrixSim 当前 USD 加载流程支持的主要元素、层级关系和支持状态。

```{note}
这里的“支持”表示转换器会读取对应 USD schema 或属性，并映射到 MSD / MotrixSim 中已有的语义。本文档是当前转换器的支持契约，不是 USD / Omni schema 的全量属性索引；对于标记为“部分支持”的 schema，只承诺表中列出的子集和主要已知缺口。没有列出的 USD / PhysX / Omni schema 或属性不应假定已支持；转换器通常会对无法表达的属性输出 warning，或跳过没有可用数据的 prim。
```

## 状态标记

| 标记                                          | 含义                                               |
| --------------------------------------------- | -------------------------------------------------- |
| <span class="badge supported">支持</span>     | 核心语义已转换，可作为当前推荐用法                 |
| <span class="badge partial">部分支持</span>   | 只承诺表中列出的子集，或部分属性会被忽略 / warning |
| <span class="badge unsupported">未支持</span> | 当前不会转换为 MotrixSim 语义                      |

## 目录

<div class="usd-index">
<details open>
<summary><a href="#usd-stage-assets">USD Stage / Assets</a> <span class="badge partial">部分支持</span></summary>
<ul>
  <li><a href="#usd-entry-points">加载入口</a> <span class="badge supported">支持</span></li>
  <li><a href="#usd-stage-assets">文件、layer、资产路径、远程纹理</a> <span class="badge partial">部分支持</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-scene-hierarchy">Scene Prim Hierarchy</a> <span class="badge partial">部分支持</span></summary>
<ul>
  <li><code>UsdGeom.Xform</code> / instance / instance proxy <span class="badge supported">支持</span></li>
  <li><a href="#usd-physics-scene"><code>UsdPhysics.Scene</code> / 刚体属性</a> <span class="badge partial">部分支持</span></li>
  <li><code>UsdPhysics.RigidBodyAPI</code> <span class="badge partial">部分支持</span></li>
  <li><code>UsdPhysics.MassAPI</code> <span class="badge supported">支持</span></li>
  <li><code>ArticulationRootAPI</code> <span class="badge partial">部分支持</span></li>
  <li><code>UsdPhysics.Joint</code> family <span class="badge partial">部分支持</span></li>
  <li><code>UsdGeom.Gprim</code> geometry <span class="badge partial">部分支持</span></li>
  <li><code>UsdLux.LightAPI</code> lights <span class="badge partial">部分支持</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-joints-drives">Joints / Drives</a> <span class="badge partial">部分支持</span></summary>
<ul>
  <li><code>FixedJoint</code>, <code>RevoluteJoint</code>, <code>PrismaticJoint</code>, <code>SphericalJoint</code> <span class="badge supported">支持</span></li>
  <li><code>PhysicsDriveAPI:angular</code>, <code>PhysicsDriveAPI:linear</code> <span class="badge partial">部分支持</span></li>
  <li><code>DistanceJoint</code>, <code>PhysicsDriveAPI:transX/rotX...</code> <span class="badge unsupported">未支持</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-geometry-meshes">Geometry / Meshes / Collision</a> <span class="badge partial">部分支持</span></summary>
<ul>
  <li><code>Mesh</code>, <code>Cube</code>, <code>Cylinder</code>, <code>Capsule</code>, <code>Sphere</code>, <code>Plane</code> <span class="badge supported">支持</span></li>
  <li><code>GeomSubset</code>, normals, <code>st</code> texcoords <span class="badge partial">部分支持</span></li>
  <li><code>CollisionAPI</code>, <code>MeshCollisionAPI</code>, <code>FilteredPairsAPI</code> <span class="badge partial">部分支持</span></li>
  <li><code>boundingSphere</code>, <code>boundingCube</code>, <code>convexDecomposition</code> <span class="badge supported">支持</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-materials-textures">Materials / Textures</a> <span class="badge partial">部分支持</span></summary>
<ul>
  <li><code>OmniPBR</code>, <code>OmniGlass</code>, <code>UsdPreviewSurface</code> <span class="badge partial">部分支持</span></li>
  <li><code>PhysicsMaterialAPI</code>, PhysX compliant contact material <span class="badge partial">部分支持</span></li>
  <li>未知 shader id <span class="badge unsupported">未支持</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-lights-environment">Lights / Environment</a> <span class="badge partial">部分支持</span></summary>
<ul>
  <li><code>DistantLight</code>, <code>SphereLight</code>, <code>RectLight</code> <span class="badge supported">支持</span></li>
  <li><code>DomeLight</code> ambient / HDR skybox <span class="badge partial">部分支持</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-unsupported">Unsupported Domains</a> <span class="badge unsupported">未支持</span></summary>
<ul>
  <li>camera、sensor、tendon、deformable、particle、time-sampled animation 等 schema</li>
</ul>
</details>
</div>

(usd-entry-points)=

## 入口

| USD / API 元素                  | 状态                                      | MotrixSim 映射                                |
| ------------------------------- | ----------------------------------------- | --------------------------------------------- |
| `motrixsim.load_model(path)`    | <span class="badge supported">支持</span> | 转换 USD 并直接返回 `SceneModel`              |
| `motrixsim.msd.from_file(path)` | <span class="badge supported">支持</span> | 转换 USD 并返回可继续编辑、组合的 `msd.World` |

(usd-stage-assets)=

## Stage、文件和资产

| USD 元素 / 功能                      | 状态                                          | MotrixSim 映射                               |
| ------------------------------------ | --------------------------------------------- | -------------------------------------------- |
| `.usd` / `.usda` / `.usdc` / `.usdz` | <span class="badge supported">支持</span>     | 使用 OpenUSD `Stage.Open` 打开               |
| sublayer / reference / payload       | <span class="badge partial">部分支持</span>   | 由 OpenUSD 负责展开；转换器处理展开后的 prim |
| resolved texture path                | <span class="badge supported">支持</span>     | 转换为 MSD texture file source               |
| 相对纹理路径                         | <span class="badge supported">支持</span>     | 按 USD 文件所在目录解析                      |
| 远程纹理 URL                         | <span class="badge partial">部分支持</span>   | 下载到本地 cache 后转换                      |
| time-sampled stage animation         | <span class="badge unsupported">未支持</span> | 当前按默认 time 读取静态场景                 |

(usd-scene-hierarchy)=

## 场景层级和变换

| USD 元素 / 属性           | 状态                                        | MotrixSim 映射                                              |
| ------------------------- | ------------------------------------------- | ----------------------------------------------------------- |
| `UsdGeom.Xform` 层级      | <span class="badge supported">支持</span>   | 遍历场景层级并累计世界变换                                  |
| instance / instance proxy | <span class="badge supported">支持</span>   | 遍历 instance proxy children                                |
| `visibility = invisible`  | <span class="badge supported">支持</span>   | 不生成视觉几何                                              |
| `purpose = guide`         | <span class="badge supported">支持</span>   | 不生成视觉几何；如果同时是 collider，仍可生成碰撞几何       |
| scale / 非均匀 scale      | <span class="badge supported">支持</span>   | 应用到几何尺寸或 `mesh_scale`                               |
| 负 scale                  | <span class="badge supported">支持</span>   | 翻转 mesh winding，避免背面剔除方向错误                     |
| `UsdPhysics.RigidBodyAPI` | <span class="badge partial">部分支持</span> | 创建 `Link` / `Body`；非 kinematic 顶层刚体创建 `FreeJoint` |
| kinematic rigid body      | <span class="badge supported">支持</span>   | 作为无 free joint 的静态 link 处理                          |
| `ArticulationRootAPI`     | <span class="badge partial">部分支持</span> | 用于继承 self-collision 设置                                |

(usd-physics-scene)=

## 物理场景和刚体属性

| USD 元素 / 属性                                           | 状态                                          | MotrixSim 映射                      |
| --------------------------------------------------------- | --------------------------------------------- | ----------------------------------- |
| `UsdPhysics.Scene.gravityDirection` + `gravityMagnitude`  | <span class="badge supported">支持</span>     | `simulate_option.gravity`           |
| `physxScene:timeStepsPerSecond`                           | <span class="badge supported">支持</span>     | `simulate_option.timestep`          |
| `UsdPhysics.MassAPI`                                      | <span class="badge supported">支持</span>     | 读取下列 MassAPI 属性               |
| `MassAPI.mass`                                            | <span class="badge supported">支持</span>     | `link.inertial.mass`                |
| `MassAPI.centerOfMass`                                    | <span class="badge supported">支持</span>     | `link.inertial.pos`                 |
| `MassAPI.diagonalInertia`                                 | <span class="badge supported">支持</span>     | `link.inertial.diag_inertia`        |
| `MassAPI.principalAxes`                                   | <span class="badge supported">支持</span>     | `link.inertial.orientation`         |
| `MassAPI.density`                                         | <span class="badge supported">支持</span>     | collider `physics_material.density` |
| `physxRigidBody:disableGravity`                           | <span class="badge supported">支持</span>     | `link.gravcomp = 1.0`               |
| `physxRigidBody:linearDamping` / `angularDamping`         | <span class="badge unsupported">未支持</span> | 输出 warning                        |
| `physxRigidBody:maxLinearVelocity` / `maxAngularVelocity` | <span class="badge unsupported">未支持</span> | 输出 warning                        |
| `physxRigidBody:enableCCD` / `retainAccelerations`        | <span class="badge unsupported">未支持</span> | 输出 warning                        |

非有限值或非正质量会被忽略并输出 warning。该分组在目录中仍标为“部分支持”，是因为 PhysX 刚体扩展属性仍有未支持项；MassAPI 自身当前列出的属性均已转换。

(usd-joints-drives)=

## 关节和驱动

| USD joint / 属性                                      | 状态                                          | MotrixSim 映射                                                                   |
| ----------------------------------------------------- | --------------------------------------------- | -------------------------------------------------------------------------------- |
| `FixedJoint`                                          | <span class="badge supported">支持</span>     | 转换为无自由度的固定子 link                                                      |
| `RevoluteJoint`                                       | <span class="badge supported">支持</span>     | `JointType.Revolute`，支持 `X/Y/Z` axis、limit、reference pose                   |
| `PrismaticJoint`                                      | <span class="badge supported">支持</span>     | `JointType.Slide`，支持 `X/Y/Z` axis、limit、reference pose                      |
| `SphericalJoint`                                      | <span class="badge partial">部分支持</span>   | `JointType.Ball`，用 cone angle 近似 ball joint limit                            |
| `DistanceJoint`                                       | <span class="badge unsupported">未支持</span> | 输出 warning                                                                     |
| `PhysicsDriveAPI:angular`                             | <span class="badge partial">部分支持</span>   | 应用于 revolute joint spring-damper 和 actuator force limit                      |
| `PhysicsDriveAPI:linear`                              | <span class="badge partial">部分支持</span>   | 应用于 prismatic joint spring-damper 和 actuator force limit                     |
| `drive:maxForce`                                      | <span class="badge supported">支持</span>     | `joint.actuator_force_limit`，并为一自由度 joint 生成 `MotorActuator.forcerange` |
| `drive:targetPosition`                                | <span class="badge supported">支持</span>     | spring target                                                                    |
| `drive:stiffness` / `drive:damping`                   | <span class="badge supported">支持</span>     | joint spring-damper                                                              |
| `physxJoint:jointFriction`                            | <span class="badge supported">支持</span>     | `joint.friction_loss`                                                            |
| `physxJoint:armature`                                 | <span class="badge supported">支持</span>     | `joint.armature`                                                                 |
| `joint:collisionEnabled = false`                      | <span class="badge supported">支持</span>     | 生成父子 link collision ignore                                                   |
| `PhysicsDriveAPI:transX/transY/transZ/rotX/rotY/rotZ` | <span class="badge unsupported">未支持</span> | 输出 warning                                                                     |
| `physxJoint:maxJointVelocity`                         | <span class="badge unsupported">未支持</span> | 输出 warning                                                                     |

(usd-geometry-meshes)=

## 几何、网格和碰撞

| USD geometry / 属性                                            | 状态                                          | MotrixSim 映射                                                                  |
| -------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------- |
| `UsdGeom.Mesh`                                                 | <span class="badge partial">部分支持</span>   | `ShapeType.Mesh`，mesh 数据内联到 `MeshAsset.source = MeshSource::Buffer`       |
| `Cube`                                                         | <span class="badge supported">支持</span>     | `ShapeType.Box`                                                                 |
| `Cylinder`                                                     | <span class="badge supported">支持</span>     | `ShapeType.Cylinder`                                                            |
| `Capsule`                                                      | <span class="badge supported">支持</span>     | `ShapeType.Capsule`                                                             |
| `Sphere`                                                       | <span class="badge supported">支持</span>     | `ShapeType.Sphere`                                                              |
| `Plane`                                                        | <span class="badge supported">支持</span>     | `ShapeType.Plane`                                                               |
| `GeomSubset` with `elementType = "face"`                       | <span class="badge supported">支持</span>     | 拆分为按 face subset 的子 mesh，可保留 subset 材质                              |
| normals / `st` texcoords: `vertex` / `varying` / `faceVarying` | <span class="badge supported">支持</span>     | 读取并展开到 MSD mesh                                                           |
| 其他 normal / texcoord interpolation                           | <span class="badge unsupported">未支持</span> | 输出 warning                                                                    |
| `CollisionAPI`                                                 | <span class="badge supported">支持</span>     | 生成 collider                                                                   |
| `MeshCollisionAPI`                                             | <span class="badge partial">部分支持</span>   | 可生成 mesh collider；只支持下列 approximation                                  |
| `MeshCollisionAPI.approximation = none`                        | <span class="badge supported">支持</span>     | 默认 mesh collider                                                              |
| `convexHull`                                                   | <span class="badge supported">支持</span>     | 默认 mesh collider，不启用运行时 ACD                                            |
| `boundingSphere`                                               | <span class="badge supported">支持</span>     | 从 mesh 包围盒生成 sphere collider                                              |
| `boundingCube`                                                 | <span class="badge supported">支持</span>     | 从 mesh 包围盒生成 box collider；可同时保留 visual mesh                         |
| `convexDecomposition`                                          | <span class="badge supported">支持</span>     | 标记 mesh asset `collision_cooking = ConvexDecomposition`，并启用 `CoACDConfig` |
| 未知 `MeshCollisionAPI.approximation`                          | <span class="badge unsupported">未支持</span> | 输出 warning，并回退为默认 mesh collider                                        |
| `FilteredPairsAPI`                                             | <span class="badge supported">支持</span>     | 生成 collision ignore pair                                                      |
| `physxCollider:contactOffset`                                  | <span class="badge supported">支持</span>     | `geometry.margin`                                                               |
| `physxCollider:restOffset`                                     | <span class="badge unsupported">未支持</span> | 输出 warning                                                                    |
| `MotrixPhysicsGeomAPI`                                         | <span class="badge supported">支持</span>     | 支持 Motrix 自定义 impedance contact model 和 priority                          |

(usd-materials-textures)=

## 物理材质、视觉材质和纹理

| USD material / shader                                                                 | 状态                                          | MotrixSim 映射                                                                                                                                                          |
| ------------------------------------------------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PhysicsMaterialAPI.staticFriction`                                                   | <span class="badge supported">支持</span>     | sliding friction，torsional / rolling friction 使用固定比例                                                                                                             |
| `PhysicsMaterialAPI.dynamicFriction`                                                  | <span class="badge supported">支持</span>     | static friction 未写入时作为 fallback                                                                                                                                   |
| `PhysicsMaterialAPI.density`                                                          | <span class="badge supported">支持</span>     | collider density，优先级低于 `MassAPI.density`                                                                                                                          |
| `PhysicsMaterialAPI.restitution`                                                      | <span class="badge supported">支持</span>     | hard contact restitution                                                                                                                                                |
| `physxMaterial:compliantContactStiffness` / `Damping`                                 | <span class="badge supported">支持</span>     | force spring 或 acceleration spring contact model                                                                                                                       |
| `physxMaterial:compliantContactAccelerationSpring`                                    | <span class="badge supported">支持</span>     | 选择 acceleration spring                                                                                                                                                |
| `physxMaterial:dampingCombineMode` / `frictionCombineMode` / `restitutionCombineMode` | <span class="badge unsupported">未支持</span> | 输出 warning                                                                                                                                                            |
| `OmniPBR`                                                                             | <span class="badge partial">部分支持</span>   | 只转换 diffuse / opacity texture 合并、diffuse tint、emissive、metallic、roughness、specular level、normal、detail normal、opacity threshold、texture scale / translate |
| `OmniGlass`                                                                           | <span class="badge partial">部分支持</span>   | 只转换 glass color、IOR、reflection color、roughness，转换为透明非金属材质                                                                                              |
| `UsdPreviewSurface`                                                                   | <span class="badge partial">部分支持</span>   | 只转换 diffuse color / texture、normal、emissive、metallic、roughness、IOR、`UsdTransform2d` texture transform                                                          |
| 可解析的本地 MDL 材质                                                                 | <span class="badge partial">部分支持</span>   | 可从本地 MDL fallback 到 OmniPBR / OmniGlass 参数                                                                                                                       |
| `MaterialBindingAPI`                                                                  | <span class="badge supported">支持</span>     | 绑定 visual material 或 physics material                                                                                                                                |
| `doubleSided`                                                                         | <span class="badge partial">部分支持</span>   | 影响 `both_side`；alpha blend 材质有深度排序保护                                                                                                                        |
| 未知 shader id                                                                        | <span class="badge unsupported">未支持</span> | 输出 warning                                                                                                                                                            |

(usd-lights-environment)=

## 灯光和环境

| USD light                       | 状态                                          | MotrixSim 映射                                                                |
| ------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------- |
| `DistantLight`                  | <span class="badge supported">支持</span>     | directional light                                                             |
| `SphereLight`                   | <span class="badge supported">支持</span>     | point light                                                                   |
| `RectLight`                     | <span class="badge supported">支持</span>     | rect light，保留 width、height、axis、normalize、color、exposure 后 intensity |
| 大面积 `RectLight`              | <span class="badge supported">支持</span>     | 额外提高 ambient brightness，并设置上限                                       |
| `DomeLight` without texture     | <span class="badge supported">支持</span>     | ambient light                                                                 |
| `DomeLight` with `.hdr` texture | <span class="badge partial">部分支持</span>   | 烘焙 IBL map，注册 skybox texture                                             |
| 其他 light 类型                 | <span class="badge unsupported">未支持</span> | 当前不生成 MotrixSim light                                                    |

当场景中存在 USD light 时，默认 head light 会被关闭，以避免重复照明。转换后的世界默认启用 SSGI。

(usd-unsupported)=

## 当前未支持或未覆盖的领域

| USD / PhysX 领域                                | 状态                                          | 说明                                            |
| ----------------------------------------------- | --------------------------------------------- | ----------------------------------------------- |
| `UsdGeom.Camera`                                | <span class="badge unsupported">未支持</span> | 当前不转换为 MotrixSim camera                   |
| sensor schemas                                  | <span class="badge unsupported">未支持</span> | 当前不转换为 MotrixSim sensor                   |
| tendon / cable / actuator-like USD schema       | <span class="badge unsupported">未支持</span> | 当前只支持 joint drive 到 motor actuator 的子集 |
| deformable / particle / cloth                   | <span class="badge unsupported">未支持</span> | MotrixSim 当前 USD 转换链路不处理               |
| time-sampled animation                          | <span class="badge unsupported">未支持</span> | 当前读取静态场景                                |
| 未知材质 shader、无法解析的纹理或异常 mesh 数据 | <span class="badge partial">部分支持</span>   | 可能被 warning、跳过或降级处理                  |

对复杂 USD 资产，应在加载时开启 logging，检查 warning 后再进入物理验证。
