# USD Reference

This page lists the main USD elements, hierarchy, and support status currently covered by the MotrixSim USD loading path.

```{note}
Here, "supported" means the converter reads the USD schema or attribute and maps it to an existing MSD / MotrixSim semantic. This page is the current converter support contract, not a complete USD / Omni schema attribute index. For schemas marked as "partial", only the listed subset and major known gaps are covered. USD / PhysX / Omni schemas or attributes that are not listed should not be assumed to work. Unsupported attributes are usually reported as warnings, or skipped when no usable data is available.
```

## Status Legend

| Marker                                             | Meaning                                                                       |
| -------------------------------------------------- | ----------------------------------------------------------------------------- |
| <span class="badge supported">Supported</span>     | Core semantics are converted and are recommended for current use              |
| <span class="badge partial">Partial</span>         | Only the listed subset is guaranteed, or some attributes are ignored / warned |
| <span class="badge unsupported">Unsupported</span> | Not currently converted to MotrixSim semantics                                |

## Index

<div class="usd-index">
<details open>
<summary><a href="#usd-stage-assets">USD Stage / Assets</a> <span class="badge partial">Partial</span></summary>
<ul>
  <li><a href="#usd-entry-points">Loader entry points</a> <span class="badge supported">Supported</span></li>
  <li><a href="#usd-stage-assets">Files, layers, asset paths, remote textures</a> <span class="badge partial">Partial</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-scene-hierarchy">Scene Prim Hierarchy</a> <span class="badge partial">Partial</span></summary>
<ul>
  <li><code>UsdGeom.Xform</code> / instance / instance proxy <span class="badge supported">Supported</span></li>
  <li><a href="#usd-physics-scene"><code>UsdPhysics.Scene</code> / rigid body attributes</a> <span class="badge partial">Partial</span></li>
  <li><code>UsdPhysics.RigidBodyAPI</code> <span class="badge partial">Partial</span></li>
  <li><code>UsdPhysics.MassAPI</code> <span class="badge supported">Supported</span></li>
  <li><code>ArticulationRootAPI</code> <span class="badge partial">Partial</span></li>
  <li><code>UsdPhysics.Joint</code> family <span class="badge partial">Partial</span></li>
  <li><code>UsdGeom.Gprim</code> geometry <span class="badge partial">Partial</span></li>
  <li><code>UsdLux.LightAPI</code> lights <span class="badge partial">Partial</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-joints-drives">Joints / Drives</a> <span class="badge partial">Partial</span></summary>
<ul>
  <li><code>FixedJoint</code>, <code>RevoluteJoint</code>, <code>PrismaticJoint</code>, <code>SphericalJoint</code> <span class="badge supported">Supported</span></li>
  <li><code>PhysicsDriveAPI:angular</code>, <code>PhysicsDriveAPI:linear</code> <span class="badge partial">Partial</span></li>
  <li><code>DistanceJoint</code>, <code>PhysicsDriveAPI:transX/rotX...</code> <span class="badge unsupported">Unsupported</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-geometry-meshes">Geometry / Meshes / Collision</a> <span class="badge partial">Partial</span></summary>
<ul>
  <li><code>Mesh</code>, <code>Cube</code>, <code>Cylinder</code>, <code>Capsule</code>, <code>Sphere</code>, <code>Plane</code> <span class="badge supported">Supported</span></li>
  <li><code>GeomSubset</code>, normals, <code>st</code> texcoords <span class="badge partial">Partial</span></li>
  <li><code>CollisionAPI</code>, <code>MeshCollisionAPI</code>, <code>FilteredPairsAPI</code> <span class="badge partial">Partial</span></li>
  <li><code>boundingSphere</code>, <code>boundingCube</code>, <code>convexDecomposition</code> <span class="badge supported">Supported</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-materials-textures">Materials / Textures</a> <span class="badge partial">Partial</span></summary>
<ul>
  <li><code>OmniPBR</code>, <code>OmniGlass</code>, <code>UsdPreviewSurface</code> <span class="badge partial">Partial</span></li>
  <li><code>PhysicsMaterialAPI</code>, PhysX compliant contact material <span class="badge partial">Partial</span></li>
  <li>Unknown shader ids <span class="badge unsupported">Unsupported</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-lights-environment">Lights / Environment</a> <span class="badge partial">Partial</span></summary>
<ul>
  <li><code>DistantLight</code>, <code>SphereLight</code>, <code>RectLight</code> <span class="badge supported">Supported</span></li>
  <li><code>DomeLight</code> ambient / HDR skybox <span class="badge partial">Partial</span></li>
</ul>
</details>
<details open>
<summary><a href="#usd-unsupported">Unsupported Domains</a> <span class="badge unsupported">Unsupported</span></summary>
<ul>
  <li>camera, sensor, tendon, deformable, particle, time-sampled animation schemas</li>
</ul>
</details>
</div>

(usd-entry-points)=

## Entry Points

| USD / API element               | Status                                         | MotrixSim mapping                                        |
| ------------------------------- | ---------------------------------------------- | -------------------------------------------------------- |
| `motrixsim.load_model(path)`    | <span class="badge supported">Supported</span> | Convert USD and return `SceneModel`                      |
| `motrixsim.msd.from_file(path)` | <span class="badge supported">Supported</span> | Convert USD and return editable / composable `msd.World` |

(usd-stage-assets)=

## Stage, Files, and Assets

| USD element / feature                | Status                                             | MotrixSim mapping                                             |
| ------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------- |
| `.usd` / `.usda` / `.usdc` / `.usdz` | <span class="badge supported">Supported</span>     | Opened through OpenUSD `Stage.Open`                           |
| sublayer / reference / payload       | <span class="badge partial">Partial</span>         | Expanded by OpenUSD; the converter handles the composed prims |
| resolved texture path                | <span class="badge supported">Supported</span>     | Converted to MSD texture file source                          |
| relative texture path                | <span class="badge supported">Supported</span>     | Resolved relative to the USD file directory                   |
| remote texture URL                   | <span class="badge partial">Partial</span>         | Downloaded into a local cache before conversion               |
| time-sampled stage animation         | <span class="badge unsupported">Unsupported</span> | Currently reads the static scene at the default time          |

(usd-scene-hierarchy)=

## Scene Hierarchy and Transforms

| USD element / attribute   | Status                                         | MotrixSim mapping                                                                             |
| ------------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `UsdGeom.Xform` hierarchy | <span class="badge supported">Supported</span> | Traverses scene hierarchy and accumulates world transforms                                    |
| instance / instance proxy | <span class="badge supported">Supported</span> | Traverses instance proxy children                                                             |
| `visibility = invisible`  | <span class="badge supported">Supported</span> | Does not create visual geometry                                                               |
| `purpose = guide`         | <span class="badge supported">Supported</span> | Does not create visual geometry; still creates collision geometry when the prim is a collider |
| scale / non-uniform scale | <span class="badge supported">Supported</span> | Applied to geometry size or `mesh_scale`                                                      |
| negative scale            | <span class="badge supported">Supported</span> | Flips mesh winding to keep face orientation correct                                           |
| `UsdPhysics.RigidBodyAPI` | <span class="badge partial">Partial</span>     | Creates `Link` / `Body`; non-kinematic top-level rigid bodies get `FreeJoint`                 |
| kinematic rigid body      | <span class="badge supported">Supported</span> | Treated as a static link without a free joint                                                 |
| `ArticulationRootAPI`     | <span class="badge partial">Partial</span>     | Used to inherit self-collision settings                                                       |

(usd-physics-scene)=

## Physics Scene and Rigid Body Attributes

| USD element / attribute                                   | Status                                             | MotrixSim mapping                   |
| --------------------------------------------------------- | -------------------------------------------------- | ----------------------------------- |
| `UsdPhysics.Scene.gravityDirection` + `gravityMagnitude`  | <span class="badge supported">Supported</span>     | `simulate_option.gravity`           |
| `physxScene:timeStepsPerSecond`                           | <span class="badge supported">Supported</span>     | `simulate_option.timestep`          |
| `UsdPhysics.MassAPI`                                      | <span class="badge supported">Supported</span>     | Reads the MassAPI attributes below  |
| `MassAPI.mass`                                            | <span class="badge supported">Supported</span>     | `link.inertial.mass`                |
| `MassAPI.centerOfMass`                                    | <span class="badge supported">Supported</span>     | `link.inertial.pos`                 |
| `MassAPI.diagonalInertia`                                 | <span class="badge supported">Supported</span>     | `link.inertial.diag_inertia`        |
| `MassAPI.principalAxes`                                   | <span class="badge supported">Supported</span>     | `link.inertial.orientation`         |
| `MassAPI.density`                                         | <span class="badge supported">Supported</span>     | Collider `physics_material.density` |
| `physxRigidBody:disableGravity`                           | <span class="badge supported">Supported</span>     | `link.gravcomp = 1.0`               |
| `physxRigidBody:linearDamping` / `angularDamping`         | <span class="badge unsupported">Unsupported</span> | Reported as warnings                |
| `physxRigidBody:maxLinearVelocity` / `maxAngularVelocity` | <span class="badge unsupported">Unsupported</span> | Reported as warnings                |
| `physxRigidBody:enableCCD` / `retainAccelerations`        | <span class="badge unsupported">Unsupported</span> | Reported as warnings                |

Non-finite values and non-positive mass values are ignored with warnings. This group is still marked as "partial" in the index because the PhysX rigid-body extension attributes have unsupported gaps; the listed MassAPI attributes themselves are converted.

(usd-joints-drives)=

## Joints and Drives

| USD joint / attribute                                 | Status                                             | MotrixSim mapping                                                                       |
| ----------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `FixedJoint`                                          | <span class="badge supported">Supported</span>     | Converted to a fixed child link with no DOF                                             |
| `RevoluteJoint`                                       | <span class="badge supported">Supported</span>     | `JointType.Revolute`; supports `X/Y/Z` axis, limits, and reference pose                 |
| `PrismaticJoint`                                      | <span class="badge supported">Supported</span>     | `JointType.Slide`; supports `X/Y/Z` axis, limits, and reference pose                    |
| `SphericalJoint`                                      | <span class="badge partial">Partial</span>         | `JointType.Ball`; cone angles are approximated as a ball joint limit                    |
| `DistanceJoint`                                       | <span class="badge unsupported">Unsupported</span> | Reported as a warning                                                                   |
| `PhysicsDriveAPI:angular`                             | <span class="badge partial">Partial</span>         | Applies to revolute joint spring-damper and actuator force limit                        |
| `PhysicsDriveAPI:linear`                              | <span class="badge partial">Partial</span>         | Applies to prismatic joint spring-damper and actuator force limit                       |
| `drive:maxForce`                                      | <span class="badge supported">Supported</span>     | `joint.actuator_force_limit`, and creates `MotorActuator.forcerange` for one-DOF joints |
| `drive:targetPosition`                                | <span class="badge supported">Supported</span>     | Spring target                                                                           |
| `drive:stiffness` / `drive:damping`                   | <span class="badge supported">Supported</span>     | Joint spring-damper                                                                     |
| `physxJoint:jointFriction`                            | <span class="badge supported">Supported</span>     | `joint.friction_loss`                                                                   |
| `physxJoint:armature`                                 | <span class="badge supported">Supported</span>     | `joint.armature`                                                                        |
| `joint:collisionEnabled = false`                      | <span class="badge supported">Supported</span>     | Creates a parent-child link collision ignore                                            |
| `PhysicsDriveAPI:transX/transY/transZ/rotX/rotY/rotZ` | <span class="badge unsupported">Unsupported</span> | Reported as warnings                                                                    |
| `physxJoint:maxJointVelocity`                         | <span class="badge unsupported">Unsupported</span> | Reported as a warning                                                                   |

(usd-geometry-meshes)=

## Geometry, Meshes, and Collision

| USD geometry / attribute                                       | Status                                             | MotrixSim mapping                                                                           |
| -------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `UsdGeom.Mesh`                                                 | <span class="badge partial">Partial</span>         | `ShapeType.Mesh`, with mesh data stored inline in `MeshAsset.source = MeshSource::Buffer`   |
| `Cube`                                                         | <span class="badge supported">Supported</span>     | `ShapeType.Box`                                                                             |
| `Cylinder`                                                     | <span class="badge supported">Supported</span>     | `ShapeType.Cylinder`                                                                        |
| `Capsule`                                                      | <span class="badge supported">Supported</span>     | `ShapeType.Capsule`                                                                         |
| `Sphere`                                                       | <span class="badge supported">Supported</span>     | `ShapeType.Sphere`                                                                          |
| `Plane`                                                        | <span class="badge supported">Supported</span>     | `ShapeType.Plane`                                                                           |
| `GeomSubset` with `elementType = "face"`                       | <span class="badge supported">Supported</span>     | Splits into per-face-subset submeshes and can preserve subset materials                     |
| normals / `st` texcoords: `vertex` / `varying` / `faceVarying` | <span class="badge supported">Supported</span>     | Read and expanded into MSD mesh data                                                        |
| Other normal / texcoord interpolation modes                    | <span class="badge unsupported">Unsupported</span> | Reported as warnings                                                                        |
| `CollisionAPI`                                                 | <span class="badge supported">Supported</span>     | Creates a collider                                                                          |
| `MeshCollisionAPI`                                             | <span class="badge partial">Partial</span>         | Can create a mesh collider; only the approximation values below are supported               |
| `MeshCollisionAPI.approximation = none`                        | <span class="badge supported">Supported</span>     | Default mesh collider                                                                       |
| `convexHull`                                                   | <span class="badge supported">Supported</span>     | Default mesh collider, without runtime ACD                                                  |
| `boundingSphere`                                               | <span class="badge supported">Supported</span>     | Creates a sphere collider from mesh bounds                                                  |
| `boundingCube`                                                 | <span class="badge supported">Supported</span>     | Creates a box collider from mesh bounds; can also preserve the visual mesh                  |
| `convexDecomposition`                                          | <span class="badge supported">Supported</span>     | Marks the mesh asset as `collision_cooking = ConvexDecomposition` and enables `CoACDConfig` |
| Unknown `MeshCollisionAPI.approximation`                       | <span class="badge unsupported">Unsupported</span> | Warns and falls back to the default mesh collider                                           |
| `FilteredPairsAPI`                                             | <span class="badge supported">Supported</span>     | Creates collision ignore pairs                                                              |
| `physxCollider:contactOffset`                                  | <span class="badge supported">Supported</span>     | `geometry.margin`                                                                           |
| `physxCollider:restOffset`                                     | <span class="badge unsupported">Unsupported</span> | Reported as a warning                                                                       |
| `MotrixPhysicsGeomAPI`                                         | <span class="badge supported">Supported</span>     | Supports Motrix custom impedance contact model and priority                                 |

(usd-materials-textures)=

## Physics Materials, Visual Materials, and Textures

| USD material / shader                                                                 | Status                                             | MotrixSim mapping                                                                                                                                                               |
| ------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PhysicsMaterialAPI.staticFriction`                                                   | <span class="badge supported">Supported</span>     | Sliding friction; torsional / rolling friction use fixed ratios                                                                                                                 |
| `PhysicsMaterialAPI.dynamicFriction`                                                  | <span class="badge supported">Supported</span>     | Fallback when static friction is not authored                                                                                                                                   |
| `PhysicsMaterialAPI.density`                                                          | <span class="badge supported">Supported</span>     | Collider density, lower priority than `MassAPI.density`                                                                                                                         |
| `PhysicsMaterialAPI.restitution`                                                      | <span class="badge supported">Supported</span>     | Hard contact restitution                                                                                                                                                        |
| `physxMaterial:compliantContactStiffness` / `Damping`                                 | <span class="badge supported">Supported</span>     | Force spring or acceleration spring contact model                                                                                                                               |
| `physxMaterial:compliantContactAccelerationSpring`                                    | <span class="badge supported">Supported</span>     | Selects acceleration spring                                                                                                                                                     |
| `physxMaterial:dampingCombineMode` / `frictionCombineMode` / `restitutionCombineMode` | <span class="badge unsupported">Unsupported</span> | Reported as warnings                                                                                                                                                            |
| `OmniPBR`                                                                             | <span class="badge partial">Partial</span>         | Converts only diffuse / opacity texture merge, diffuse tint, emissive, metallic, roughness, specular level, normal, detail normal, opacity threshold, texture scale / translate |
| `OmniGlass`                                                                           | <span class="badge partial">Partial</span>         | Converts only glass color, IOR, reflection color, and roughness; outputs a transparent non-metallic material                                                                    |
| `UsdPreviewSurface`                                                                   | <span class="badge partial">Partial</span>         | Converts only diffuse color / texture, normal, emissive, metallic, roughness, IOR, and `UsdTransform2d` texture transform                                                       |
| Parseable local MDL material                                                          | <span class="badge partial">Partial</span>         | Can fall back from local MDL parameters to OmniPBR / OmniGlass mappings                                                                                                         |
| `MaterialBindingAPI`                                                                  | <span class="badge supported">Supported</span>     | Binds visual material or physics material                                                                                                                                       |
| `doubleSided`                                                                         | <span class="badge partial">Partial</span>         | Affects `both_side`; alpha-blended materials have depth-sorting protection                                                                                                      |
| Unknown shader id                                                                     | <span class="badge unsupported">Unsupported</span> | Reported as a warning                                                                                                                                                           |

(usd-lights-environment)=

## Lights and Environment

| USD light                       | Status                                             | MotrixSim mapping                                                                                |
| ------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `DistantLight`                  | <span class="badge supported">Supported</span>     | Directional light                                                                                |
| `SphereLight`                   | <span class="badge supported">Supported</span>     | Point light                                                                                      |
| `RectLight`                     | <span class="badge supported">Supported</span>     | Rect light; preserves width, height, axes, normalize flag, color, and exposure-applied intensity |
| Large `RectLight`               | <span class="badge supported">Supported</span>     | Adds capped ambient brightness                                                                   |
| `DomeLight` without texture     | <span class="badge supported">Supported</span>     | Ambient light                                                                                    |
| `DomeLight` with `.hdr` texture | <span class="badge partial">Partial</span>         | Bakes IBL maps and registers a skybox texture                                                    |
| Other light types               | <span class="badge unsupported">Unsupported</span> | No MotrixSim light is currently generated                                                        |

When a scene contains USD lights, the default head light is disabled to avoid double illumination. Converted worlds enable SSGI by default.

(usd-unsupported)=

## Current Unsupported or Uncovered Domains

| USD / PhysX domain                                                   | Status                                             | Notes                                                     |
| -------------------------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------- |
| `UsdGeom.Camera`                                                     | <span class="badge unsupported">Unsupported</span> | Not currently converted to MotrixSim camera               |
| sensor schemas                                                       | <span class="badge unsupported">Unsupported</span> | Not currently converted to MotrixSim sensors              |
| tendon / cable / actuator-like USD schemas                           | <span class="badge unsupported">Unsupported</span> | Only a subset of joint drives converts to motor actuators |
| deformable / particle / cloth                                        | <span class="badge unsupported">Unsupported</span> | Not handled by the current USD conversion path            |
| time-sampled animation                                               | <span class="badge unsupported">Unsupported</span> | Currently reads static scenes                             |
| Unknown material shaders, unresolved textures, or abnormal mesh data | <span class="badge partial">Partial</span>         | May be warned, skipped, or degraded                       |

For complex USD assets, enable logging during loading and inspect warnings before physics validation.
