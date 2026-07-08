# ACD Convex Decomposition

ACD (Approximate Convex Decomposition) decomposes a non-convex mesh into multiple convex hulls. In MotrixSim, it is mainly used for mesh colliders: complex models can keep their original visual mesh while using a set of convex hulls that is better suited for physical collision.

The demo below first shows the same room scene in render-only mode, then enables collider visualization and compares convex hulls with ACD disabled and enabled. With ACD enabled, the collider is approximated by multiple local convex hulls, which better covers non-convex structures such as cabinets, sofas, and decorative objects.

```{video} /_static/videos/acd_room_ssgi_demo.mp4
:poster: /_static/images/poster/acd_room_ssgi_demo.jpg
:caption: ACD collider comparison
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%

```

MotrixSim supports two ACD workflows:

| Workflow              | Use Case                                                                                  | Output                                               |
| --------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| Online decomposition  | Enable it while loading or building a scene for simple-model debugging and quick testing. | Runtime convex hull colliders; no files are written. |
| Offline decomposition | Preprocess assets for stable commits, reuse, and inspection.                              | `.obj` or `.stl` convex decomposition files.         |

```{note}
Online convex decomposition does not modify MJCF/URDF/USD files and does not generate new mesh files on disk. Offline convex decomposition only processes `.obj` / `.stl` mesh files and does not rewrite MJCF automatically. If you want a model to reference the offline output, update the mesh paths in the model manually.
```

## Run the Documentation Example

`motrixsim-docs` includes ACD example scenes under `examples/assets/acd/`. Paths below are relative to the
`motrixsim-docs` project root:

-   `examples/assets/acd/world.xml`: the original room scene, with meshes loaded directly from the original OBJ assets.
-   `examples/assets/acd/world_acd.xml`: the offline ACD room scene. Visual meshes still use the original OBJ files, while collision meshes reference committed files under `assets/convex_parts/`.
-   `examples/assets/acd/chair_online_acd.xml`: a compact chair scene that keeps collision meshes on the original OBJ files and uses `acd="true"` to exercise online ACD during loading.

Compared with the original scene, `world_acd.xml` keeps the same visual room but replaces mesh colliders with offline convex decomposition output.

Run these commands from the `motrixsim-docs` project root:

```bash
# Open the original scene first
uv run mxview examples/assets/acd/world.xml

# Open the scene that enables the ACD pipeline
uv run mxview examples/assets/acd/world_acd.xml

# Open a compact online ACD example
uv run mxview examples/assets/acd/chair_online_acd.xml
```

The room scenes look almost identical visually; the difference is in the colliders. After `mxview` opens, use
the right-side `Gizmos` panel to enable both `Static Collider` and `ConvexHull`, then inspect the same object
in both scenes:

-   `world.xml` uses colliders compiled from the original meshes, so non-convex objects usually show a
    coarser single-convex-hull approximation.
-   `world_acd.xml` references pre-generated `convex_parts/*_convex.obj` collision meshes; with those
    gizmos enabled, multiple local convex hulls should cover non-convex shapes such as cabinets, sofas,
    and decorative objects more closely.
-   `chair_online_acd.xml` is intentionally separate from the offline room example, so it remains a quick
    way to inspect the online `acd="true"` loading path on one chair.

The room example demonstrates the offline ACD pipeline with committed convex mesh files. The chair example
demonstrates the online ACD pipeline. To wire either workflow into your own MJCF, continue with "Wire It in
MJCF" below.

## What It Solves

Using a non-convex mesh directly as a collider is usually more expensive, and it may not match the engine's internal convex-hull collision path. ACD approximates one non-convex mesh with several local convex hulls, so complex shapes can be represented by multiple simpler convex colliders.

Common use cases include:

-   Generating more appropriate colliders for non-convex structures such as robot grippers, cups, cabinets, and drawers
-   Keeping high-quality visual meshes while optimizing collision meshes separately
-   Quickly checking whether a mesh behaves better with multi-convex collision during debugging
-   Freezing convex decomposition results before publishing assets, avoiding repeated decomposition on every load

## Online Convex Decomposition

Online convex decomposition happens during scene loading or model compilation. Meshes marked as ACD-enabled are decomposed by CoACD into one or more runtime convex hulls; those hulls then enter runtime collision, raycast, bounding-box, and related flows as the real colliders.

Different asset entry points enable ACD independently: MJCF uses `<mesh acd="true">`, while USD uses `MeshCollisionAPI.approximation = "convexDecomposition"`. USD assets do not need to be converted to MJCF first, and no extra MJCF field is required.

### Wire It in MJCF

MJCF can use ACD through either the online or offline workflow. Online ACD can use the same mesh geom for
both rendering and collision. If you need to debug colliders separately, hide collision geometry, or swap in
offline baked assets later, you can still split visual and collision meshes.

#### Online Wiring

The online ACD switch is placed on the `<mesh>` in `<asset>`, not on the `<geom>`. The mesh still points at
the original OBJ/STL file, with only `acd="true"` added. CoACD only runs when that mesh is referenced by a
collidable geom:

```xml
<mujoco>
    <asset>
        <mesh name="cup" file="meshes/cup.obj" acd="true"/>
    </asset>

    <worldbody>
        <body name="cup" pos="0 0 0.4">
            <freejoint/>
            <geom name="cup" type="mesh" mesh="cup" mass="0.2"/>
        </body>
    </worldbody>
</mujoco>
```

`examples/assets/acd/chair_online_acd.xml` uses the online pipeline, for example:

```xml
<mesh name="chair_cushion" file="assets/GEO_chair_001a.obj" acd="true"/>
<mesh name="chair_frame" file="assets/GEO_chair_001b.obj" acd="true"/>
```

#### Offline Wiring

Offline ACD first runs `uv run acd` to decompose OBJ/STL files and write the result to disk. Then the
collision `<mesh>` in MJCF points at the generated convex decomposition file. Offline wiring does not need
`acd="true"`:

```xml
<mesh name="GEO_sofa_001" file="GEO_sofa_001.obj"/>
<mesh name="GEO_sofa_001_acd" file="convex_parts/GEO_sofa_001_convex.obj"/>
```

The committed room example already uses offline wiring. This is how its `convex_parts/` files are generated:

```bash
# Run from the motrixsim-docs project root and preview the generated files first
uv run acd examples/assets/acd/assets --dry-run

# After checking the plan, write offline output into the ACD example's own asset directory
uv run acd examples/assets/acd/assets \
    -o examples/assets/acd/assets/convex_parts
```

Then, in `examples/assets/acd/assets/room_acd.xml`, point collision meshes at those generated files:

```xml
<mesh name="GEO_sofa_001_acd" file="convex_parts/GEO_sofa_001_convex.obj"/>
```

The geom binding for the same object usually does not need to change, because the collision geom still
references the same `GEO_sofa_001_acd` mesh name. What changes is the `file` path behind that mesh asset, and
whether it carries `acd="true"`.

For both online and offline wiring, create two geoms at the same pose: the visual geom has collision
disabled, and the collision geom references the corresponding ACD mesh:

```xml
<geom name="GEO_sofa_001" pos="1.864403 0.9069114 -3.1659286"
      quat="0.7071069 -1e-07 1e-07 -0.7071066"
      type="mesh" mesh="GEO_sofa_001" material="MI_sofa_002"
      group="2" contype="0" conaffinity="0" density="0"/>
<geom name="GEO_sofa_001_acd" pos="1.864403 0.9069114 -3.1659286"
      quat="0.7071069 -1e-07 1e-07 -0.7071066"
      type="mesh" mesh="GEO_sofa_001_acd"
      group="3" contype="1" conaffinity="1"/>
```

When wiring this up, check:

-   Online workflow: `acd="true"` is on the collision `<mesh>`, not on the `<geom>`.
-   Offline workflow: the collision `<mesh file="...">` points at the generated convex decomposition file, and
    the path is relative to the current XML file.
-   The visual geom and collision geom are under the same parent body and use the same `pos` / `quat`.
-   The original visual geom has collision disabled, so the object does not collide through both the original mesh and the ACD result.
-   If the scene uses submodels, you edited the submodel XML, not only the top-level `world.xml`.

Load the model the same way as any other model:

```python
import motrixsim as mx

model = mx.load_model("scene.xml")
data = mx.SceneData(model)
mx.step(model, data)
```

### Enable It in USD

If a USD asset uses `MeshCollisionAPI.approximation = "convexDecomposition"`, MotrixSim maps it to an ACD-enabled mesh and generates runtime convex hulls during loading. For USD support details, see {doc}`../getting_started/usd_reference`.

### Runtime Behavior

Online convex decomposition only affects collision geometry; it does not change the visual mesh. After compilation, the original mesh can still be used for rendering and asset references, while collision uses the decomposed convex hull colliders.

Online ACD now uses the same default `threshold` as the offline command: `0.1`. Because online
decomposition must finish while the scene is being loaded or compiled, complex meshes or large asset sets can
noticeably increase startup time. For those assets, run offline convex decomposition first and commit the
generated `convex_parts` files. Use online ACD for simple-model debugging, quick previews, and temporary
validation.

To quickly test online ACD, open `examples/assets/acd/chair_online_acd.xml` with `mxview`. It marks the chair's two collision meshes with `acd="true"`, generates runtime colliders during loading, and does not write any `convex_parts` files.

If CoACD decomposition fails for a mesh, produces an empty result, exceeds the runtime convex-hull budget, or creates hulls that the collision backend cannot accept, MotrixSim falls back to the single-convex-hull path for that mesh. ACD results for other meshes are not affected.

## Offline Convex Decomposition

Offline convex decomposition decomposes `.obj` / `.stl` mesh files ahead of time and writes the result to disk. It is useful for asset processing and version control: generated results can be committed to the repository and referenced as collision meshes from MJCF/URDF.

### Command Line Usage

First, preview the files that would be generated with `--dry-run`:

```bash
uv run acd meshes/robot.obj --dry-run
```

After confirming the result, write the files:

```bash
uv run acd meshes/robot.obj
```

By default, each source mesh generates `convex_parts/{stem}_convex.obj` next to its source directory:

```text
meshes/robot.obj
meshes/convex_parts/robot_convex.obj
```

You can also specify an output directory or a single output file:

```bash
uv run acd meshes/robot.obj -o baked_collision
uv run acd meshes/robot.obj --output robot_collision.obj
uv run acd meshes/robot.obj --output robot_collision.stl
```

Directory input recursively processes `.obj` / `.stl` files:

```bash
uv run acd meshes/ --dry-run
uv run acd meshes/ -o baked_collision
```

### Python API

In Python, call `motrixsim.acd` directly:

```python
import motrixsim as mx

report = mx.acd("meshes/robot.obj", dry_run=True)

for file in report.files:
    print(file.path, file.fatal_error)
    for mesh in file.meshes:
        print(mesh.name, mesh.part_count, mesh.part_files, mesh.skipped_reason)
```

### Reference Offline Output from MJCF

The offline tool does not modify MJCF automatically. After generating a collision mesh, manually point the
collision `<mesh>` in the model XML to the new convex decomposition file. This flow does not need
`acd="true"`, because decomposition has already been written to disk:

```xml
<asset>
    <mesh name="robot_visual" file="meshes/robot.obj"/>
    <mesh name="robot_collision" file="meshes/convex_parts/robot_convex.obj"/>
</asset>

<worldbody>
    <body name="robot">
        <geom type="mesh" mesh="robot_visual" contype="0" conaffinity="0"/>
        <geom type="mesh" mesh="robot_collision"/>
    </body>
</worldbody>
```

This keeps the original visual mesh while using the offline decomposed mesh for collision. When wiring this
into your own scene, usually check three things:

-   The visual `<mesh>` still points at the original OBJ/STL file; the collision `<mesh>` points at the
    generated offline file, such as `meshes/convex_parts/robot_convex.obj`. The `file` path is relative to
    the XML file that declares the `<mesh>`.
-   The visual geom and collision geom are under the same parent body and use the same `pos` / `quat`. Disable
    collision on the visual geom, and let the collision geom reference the offline decomposed mesh with active
    `contype` / `conaffinity`.
-   If the scene is composed from submodels, you do not need to list every collision mesh in the top-level
    `world.xml`; edit the submodel XML that declares those meshes and geoms.

After wiring the offline output, open the scene with `mxview` and enable both `Static Collider` and
`ConvexHull` in the `Gizmos` panel to check that the offline collider covers the original visual model.

## Parameter Quick Reference

| Parameter             | Location                                 | Description                                          |
| --------------------- | ---------------------------------------- | ---------------------------------------------------- |
| `acd`                 | MJCF `<mesh acd="true">`                 | Enables online convex decomposition.                 |
| `convexDecomposition` | USD `MeshCollisionAPI.approximation`     | Enables online convex decomposition.                 |
| `threshold`           | `--threshold` / `threshold=`             | Error threshold for offline decomposition.           |
| `max_convex_hull`     | `--max-convex-hull` / `max_convex_hull=` | Maximum number of convex hulls for CoACD offline.    |
| `output`              | `-o/--output` / `output=`                | Offline output directory or single-file output path. |
| `dry_run`             | `--dry-run` / `dry_run=True`             | Previews offline results without writing to disk.    |

## How to Choose

| Requirement                                                   | Recommended Workflow  |
| ------------------------------------------------------------- | --------------------- |
| Quickly test multi-convex collision behavior for a mesh       | Online decomposition  |
| Avoid maintaining extra collision mesh files                  | Online decomposition  |
| Reduce approximation error and make asset loading more stable | Offline decomposition |
| Inspect, edit, or commit generated collision meshes manually  | Offline decomposition |
| Reuse the same collision mesh across multiple models          | Offline decomposition |

## FAQ

1. Q: Does online convex decomposition change the visual result?

    A: No. Online ACD only affects collision colliders; the visual mesh still uses the original mesh.

2. Q: Why does it still look like there is only one collider after setting `acd="true"`?

    A: The mesh may already be close to convex, or decomposition may have failed and fallen back to a single convex hull after exceeding the runtime hull budget. When debugging, try lowering `threshold`, or increasing `max_convex_hull` and the runtime budget.

3. Q: Does offline convex decomposition automatically replace mesh paths in XML?

    A: No. The offline tool only reads and writes `.obj` / `.stl` files. Model files must be updated manually.

4. Q: Can directory input merge all meshes into one output file?

    A: No. Directory mode keeps a one-source-file-to-one-output structure. If you specify a single `.obj` / `.stl` output file, the input must also be a single mesh file.
