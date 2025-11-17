# 📋 MJCF Files

MJCF is a widely used format in the field of robotics simulation. You can learn more about the MJCF format via the following link:

-   [MJCF Format Documentation](https://mujoco.readthedocs.io/en/stable/XMLreference.html)

MotrixSim provides extensive compatibility support for MJCF while maintaining its own simulation capabilities and features.

You can load robot models in MJCF format as follows:

```py
import motrixsim
model = motrixsim.load_model("path/to/robot.xml")  # Load a model in MJCF format
```

## MJCF Support Status

MJCF contains a rich set of tags and attributes. This section lists the current support status for MJCF in MotrixSim.

### Global Configuration

```{list-table}
:header-rows: 1
:widths: 25 30 30 40
:class: longtable
* - **Tag**
  - **Supported Attributes**
  - **Planned Attributes**
  - **Unsupported Attributes**
* - option
  - timestep, gravity, iterations, tolerance, o_margin, o_solref, o_solimp, o_friction
  - apirate, wind, magnetic, density, viscosity, actuatorgroupdisable
  - impratio, integrator, cone, jacobian, solver, ls_iterations, ls_tolerance, noslip_iterations, noslip_tolerance, ccd_iterations, ccd_tolerance, sdf_iterations,  sdf_initpoints
* - compiler
  - autolimits, angle, eulerseq, meshdir, texturedir, assetdir
  - settotalmass, balanceinertia, strippath, discardvisual, usethread, inertiafromgeom, alignfree, inertiagrouprange, saveinertial, fitaabb
  - boundmass, boundinertia, coordinate, fusestatic
* - statistic
  - extent,center
  - meanmass, meaninertia, meansize
  - \\
```

Unsupported tag: `size`

### Asset

Supported tags:

```{list-table}
:header-rows: 1
:widths: 25 50 40 20
:class: longtable
* - **Tag**
  - **Supported Attributes**
  - **Planned Attributes**
  - **Unsupported Attributes**
* - mesh
  - file, vertex, normal, texcoord, face, scale, refpos, refquat
  - content_type, smoothnormal, maxhullvert, inertia
  - \\
* - hfield
  - nrow, ncol, elevation, size,content_type, file
  - \\
  - \\
* - texture
  - type, file, builtin, rgb1, rgb2, width, height, colorspace
  - content_type, gridsize, gridlayout, fileright, fileleft, fileup, filedown, filefront, fileback, mark, markrgb, random, hflip, vflip, nchannel
  - \\
* - material
  - texture, rgba, texrepeat, texuniform, reflectance, metallic, roughness
  - emission, specular, shininess
  - \\
* - material/layer
  - texture, role
  - \\
  - \\
```

Planned tags:

`skin`, `model`，`mesh/plugin`

```{note}
Currently, mesh files support stl, obj, and dae formats.
For the type attribute in texture, only 2d and skybox are supported; cube is not supported.
```

### Scene

Supported tags:

```{list-table}
:header-rows: 1
:widths: 25 50 40 20
:class: longtable
* - **Tag**
  - **Supported Attributes**
  - **Planned Attributes**
  - **Unsupported Attributes**
* - body
  - mocap, pos, orientation, gravcomp
  - \\
  - \\
* - inertial
  - pos, orientation, mass, diaginertia, fullinertia
  - \\
  - \\
* - joint
  - pos, axis, springdamper, solreflimit, solimplimit, solreffriction, solimpfriction, stiffness, range, limited, actuatorfrcrange, actuatorfrclimited, margin, ref, springref, armature, damping, frictionloss
  - actuatorgravcomp
  - \\
* - geom
  - type, group, condim, contype, conaffinity, priority, size, mass, density, solmix, solref, solimp, margin, gap, fromto, pos, orientation, hfield, mesh
  - fitscale, fluidshape, fluidcoef, shellinertia
  - \\
* - geom.type
  - plane, hfield, sphere, capsule, cylinder, box, mesh
  - ellipsoid, sdf
  - \\
* - site
  - size, pos, orientation, type, group
  - material, rgb, fromto
  - \\
* - contact/exclude
  - body1, body2
  - \\
  - \\
* - camera
  - pos, orientation, orthographic, fovy, target
  - ipd, resolution, focal, focalpixel, principal, principalpixel, sensorsize
  - \\
* - camera.mode
  - fixed, track, targetbody
  - trackcom, targetbodycom
  - \\
* - light
  - pos, dir, target, type, directional, castshadow, diffuse, cutoff
  - active, bulbradius, intensity, range, attenuation, exponent, ambient, specular, texture
  - \\
* - light.type
  - spot, directional, point
  - image
  - \\
* - light.mode
  - fixed, track, targetbody
  - trackcom, targetbodycom
  - \\
```

Planned tags:

`flexcomp`, `frame`, `attach`, `contact/pair`, `deformable`

Unsupported tags:

`compisite`

### Equality

Supported tags:

```{list-table}
:header-rows: 1
:widths: 25 50 40 20
:class: longtable
* - **Tag**
  - **Supported Attributes**
  - **Planned Attributes**
  - **Unsupported Attributes**
* - connect
  - active, solref, solimp, body1, body2, anchor, site1, site2
  - \\
  - \\
* - weld
  - active, solref, solimp, body1, body2, relpose, anchor, site1, site2
  - torquescale
  - \\
* - joint
  - active, solref, solimp, joint1, joint2, polycoef
  - \\
  - \\
```

Planned tags:

`tendon`, `flex`, `distance`

### Tendons

Supported tags:

```{list-table}
:header-rows: 1
:widths: 25 50 40 20
:class: longtable
* - **Tag**
  - **Supported Attributes**
  - **Planned Attributes**
  - **Unsupported Attributes**
* - fixed
  - limited, range, solreflimit, solimplimit, springlength, stiffness, damping
  - solreffriction, solimpfriction, frictionloss
  - \\
```

Planned tags: `spatial`

### Actuator

Supported tags:

```{list-table}
:header-rows: 1
:widths: 25 50 40 20
:class: longtable
* - **Tag**
  - **Supported Attributes**
  - **Planned Attributes**
  - **Unsupported Attributes**
* - general
  - ctrllimited, forcelimited, ctrlrange, forcerange, gear, joint, tendon, gaintype, biastype, dynprm, gainprm, biasprm
  - dyntype, actlimited, actrange, lengthrange, cranklength, jointinparent, site, refsite, body, cranksite, slidersite, actdim, actearly
  - \\
* - general.gaintype
  - fixed,affine
  - muscle
  - user
* - general.biastype
  - none, affine
  - muscle
  - user
* - motor
  - \\
  - \\
  - \\
* - position
  - kp,kv, inheritrange
  - dampratio,timeconst
  - \\
* - velocity
  - kv
  - \\
  - \\
* - adhesion
  - body,gain
  - \\
  - \\
```

Planned tags:

`intvelocity`, `damper`, `cylinder`, `muscle`

### Sensors

```{list-table}
:header-rows: 1
:widths: 25 50 40 20
:class: longtable
* - **Tag**
  - **Supported Attributes**
  - **Planned Attributes**
  - **Unsupported Attributes**
* - accelerometer<br>velocimeter<br>
  - site
  - \\
  - \\
* - jointpos<br>jointvel
  - joint
  - \\
  - \\
* - framepos<br>framequat<br>framexaxis<br>frameyaxis<br>framezaxis
  - objtype, objname, reftype, refname
  - \\
  - \\
* - framelinvel<br>frameangvel
  - objtype, objname
  - \\
  - \\
* - subtreecom<br>subtreelinvel<br>subtreeangmom
  - body
  - \\
  - \\
```

Planned tags:

`touch`,`force`,`torque`,`magnetometer`,`cameraprojection`,`rangefinder`,
`tendonpos`,`tendonvel`,`actuatorpos`,`actuatorvel`,`actuatorfrc`,
`jointactuatorfrc`,`tendonactuatorfrc`,`ballquat`,`ballangvel`,
`jointlimitpos`,`jointlimitvel`,`jointlimitfrc`,
`tendonlimitpos`,`tendonlimitvel`,`tendonlimitfrc`,`framelinacc`,`frameangacc`,
`distance`,`normal`,`fromto`,`e_potential`,`e_kinetic`,`clock`

```{note}
For the objtype attribute in sensor, currently supported values are body, xbody, geom, site; camera is not supported.
```

### Meta

Supported tags:

```{list-table}
:header-rows: 1
:widths: 25 50 40 20
:class: longtable
* - **Tag**
  - **Supported Attributes**
  - **Planned Attributes**
  - **Unsupported Attributes**
* - replicate
  - count, sep, offset, euler
  - \\
  - \\
* - include
  - file
  - \\
  - \\
* - frame
  - name, childclass, pos, orientation
  - \\
  - \\
```

```{note}
Please note that MotrixSim currently handles meta tags differently from Mujoco. The main differences are as follows:
- The `replicate` tag is currently only partially supported. If a body referenced by an actuator or sensor is included within replicate, it may cause reference errors.
```

### Keyframe

```{list-table}
:header-rows: 1
:widths: 25 50 40 20
:class: longtable
* - **Tag**
  - **Supported Attributes**
  - **Planned Attributes**
  - **Unsupported Attributes**
* - key
  - time, qpos, qvel, ctrl
  - act, mpos, mquat
  - \\
```

### Default

Supported sub tags:

`mesh`,`material`,`joint`,`geom`,`site`,`camera`,`light`,`tendon`,`general`,`motor`,
`position`,`velocity`,`equality`,`adhesion`

Planned:

`pair`,,`intvelocity`,`damper`,`cylinder`,`muscle`,

### Visual

Supported tags:

```{list-table}
:header-rows: 1
:widths: 25 50 40 20
:class: longtable
* - **Tag**
  - **Supported Attributes**
  - **Planned Attributes**
  - **Unsupported Attributes**
* - global
  - orthographic, fovy, azimuth, elevation
  - ipd, linewidth, glow, offwidth, offheight, realtime, ellipsoidinertia, bvactive
  - \\
* - headlight
  - ambient, diffuse, active
  - specular
  - \\
* - map
  - fogstart, fogend, znear, zfar
  - stiffness, stiffnessrot, force, torque, alpha, haze, shadowclip, shadowscale, actuatortendon
  - \\
* - rgba
  - fog, haze, joint, bv, contactforce
  - force, inertia, actuator, actuatornegative, actuatorpositive, com, camera, light, selectpoint, connect, contactpoint, contactfriction, contacttorque, contactgap, rangefinder, constraint, slidercrank, crankbroken, frustum, bvactive
  - \\
```

```{note}
There will always be a free camera configured according to the global settings as the initial camera.
There will always be two light sources: a headlight and ambient light, neither of which cast shadows.
```

Planned tags: `quality`, `scale`
