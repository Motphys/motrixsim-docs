# Height Fields (HField)

Height Fields (HField) are an efficient geometry type for representing terrain surfaces. They store elevation information through 2D grid data, providing realistic physical collision responses for robot simulation, terrain following, and surface interaction.

## Height Field Features

Height fields offer the following advantages:

-   **Efficient Storage**: Uses regular grids to store elevation data with low memory footprint
-   **Fast Collision Detection**: Grid-based spatial partitioning algorithms provide efficient collision queries
-   **Realistic Terrain Simulation**: Supports complex terrain features such as hillsides, ravines, plains, etc.
-   **Large-scale Scenes**: Suitable for representing large terrain areas, commonly used in outdoor robot simulation

## MJCF Configuration

In MJCF files, height fields are defined using the `<hfield>` tag, supporting three data source methods:

### 1. Inline Elevation Data

Directly specify elevation data matrix in XML:

```xml
<asset>
    <hfield name="terrain1"
            nrow="15"
            ncol="15"
            elevation="0.0 0.43 0.78 0.97 ..."
            size="5 5 2 0.1"/>
</asset>
```

### 2. PNG Image Files

Use PNG images as elevation data source (recommended for visual terrain):

```xml
<asset>
    <hfield name="png_terrain"
            file="terrain.png"
            content_type="image/png"
            size="10 10 3 0.2"/>
</asset>
```

**Notes:**

-   PNG images are automatically converted to grayscale
-   White pixels correspond to high elevation, black pixels to low elevation
-   Intensity values are used as elevation data and normalized to [0, 1] range

### 3. Custom Binary Files

Use MuJoCo custom binary format:

```xml
<asset>
    <hfield name="binary_terrain"
            file="terrain.hfield"
            content_type="image/vnd.mujoco.hfield"
            size="8 8 2.5 0.15"/>
</asset>
```

**Binary file format:**

-   File size: `4 × (2 + nrow × ncol)` bytes
-   Structure:
    -   `int32 nrow`: Number of rows
    -   `int32 ncol`: Number of columns
    -   `float32 data[nrow×ncol]`: Elevation data (row-major order)

### MJCF Attribute Description

| Attribute      | Type                     | Default  | Description                                                                                                                                         |
| -------------- | ------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`         | string                   | optional | Height field name for reference. If omitted and file name is specified, uses filename (without path and extension)                                  |
| `content_type` | string                   | optional | **Currently ignored by MotrixSim**                                                                                                                  |
| `file`         | string                   | optional | External file path. `.png` files are converted to grayscale, intensity values used as elevation data; other formats treated as custom binary format |
| `nrow`         | integer                  | "0"      | Number of rows in elevation data matrix. Default 0 means load from file and automatically infer matrix size                                         |
| `ncol`         | integer                  | "0"      | Number of columns in elevation data matrix                                                                                                          |
| `elevation`    | float array (nrow×ncol)  | optional | Inline elevation data matrix. Data automatically normalized to [0, 1] range. Defaults to 0 if not provided                                          |
| `size`         | float array (4 elements) | required | Physical dimensions: `[radius_x, radius_y, elevation_z, base_z]`                                                                                    |

### Detailed size Attribute Description

The `size` attribute contains four floats: `[radius_x, radius_y, elevation_z, base_z]`, with each parameter meaning:

-   **radius_x**: Radius in X direction (half-width). Total width of height field on X axis is `2 × radius_x`
-   **radius_y**: Radius in Y direction (half-length). Total length of height field on Y axis is `2 × radius_y`
-   **elevation_z**: Maximum elevation. This value scales normalized [0-1] elevation data, so lowest point is at Z=0, highest point at Z=elevation_z
-   **base_z**: Base depth. **Currently ignored by MotrixSim**

**Important Notes:**

-   Height fields are centered in the local coordinate system of the referencing geometry
-   Elevation direction is +Z direction
-   Unlike planes, height fields are treated as unions of regular geometry, with no concept of "below height field" - geometry is either inside or outside the height field
-   Therefore, base parts must have non-zero thickness to avoid penetration issues

**Example:**

```xml
<!-- Create a 10×10 unit height field with max elevation 2 units and base thickness 0.1 units -->
<hfield name="terrain" size="5 5 2 0.1" nrow="50" ncol="50"/>
```

### Collision Detection Features

Height field collision detection has the following important characteristics:

**Collision Model:**

-   Height fields are treated as unions of triangular prisms
-   First select potentially colliding sub-grid prisms based on geometry bounding boxes
-   Then use general convex colliders for precise collision calculation

**Supported Collision Types:**

-   ✅ Height field with sphere, capsule, cylinder, cube, polyhedron
-   ❌ Height field with plane collision (not supported)
-   ❌ Height field with other height field collision (not supported)

For more detailed hfield field descriptions, please refer to the [MJCF official documentation](https://mujoco.readthedocs.io/en/3.3.7/XMLreference.html#asset-hfield).

### Geometry Reference

Use height fields in `<worldbody>`:

```xml
<worldbody>
    <geom name="terrain" type="hfield" hfield="terrain1" material="ground_material"/>
    <geom pos="10 0 0" name="terrain2" type="hfield" hfield="file_terrain" material="ground_material"/>
</worldbody>
```

## Main Interfaces

In MotrixSim, you can access HField objects through the following methods:

-   [`model.num_hfields`]: Get the number of height fields in the current scene.
-   [`model.get_hfield(name_or_index)`]: Get a specific height field object by name or index.

### HField Object Properties

After obtaining an HField object, you can access the following properties:

```python
hfield = model.get_hfield("terrain1")

# Basic properties
name = hfield.name          # Height field name
nrow = hfield.nrow          # Number of grid rows
ncol = hfield.ncol          # Number of grid columns
bound = hfield.bound        # Bounding box [-x, -y, 0, x, y, z]

# Elevation data
height_matrix = hfield.height_matrix  # Complete elevation matrix (nrow × ncol)

# Query elevation at specific point
height = hfield.get(row=5, col=10)    # Get elevation at specified row and column
```

## Usage Examples

### Basic Height Field Operations

```{literalinclude} ../../../../../examples/hfield.py
:language: python
:dedent:
:start-after: "# tag::basic_access"
:end-before: "# end::basic_access"
```

### Elevation Data Analysis

```{literalinclude} ../../../../../examples/hfield.py
:language: python
:dedent:
:start-after: "# tag::height_analysis"
:end-before: "# end::height_analysis"
```

### Complete Simulation Example

```{literalinclude} ../../../../../examples/hfield.py
:language: python
:dedent:
```

Run the height field simulation example:

```bash
uv run examples/hfield.py
```

## File Format

MotrixSim supports binary height field file format (`.hfield`):

### File Structure

-   **Header**: First 8 bytes
    -   `nrow` (int32): Number of grid rows
    -   `ncol` (int32): Number of grid columns
-   **Data section**: Remaining bytes
    -   Elevation data array (float32), length `nrow × ncol`

### Generating Height Field Files

You can create custom height field files using the following method:

```python
import numpy as np

def create_hfield_file(filename, height_data):
    """Create binary height field file"""
    nrow, ncol = height_data.shape

    with open(filename, 'wb') as f:
        # Write header information
        f.write(np.array([nrow, ncol], dtype=np.int32).tobytes())
        # Write elevation data
        f.write(height_data.astype(np.float32).tobytes())

# Example: Create simple terrain
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = 0.5 * np.sin(X) * np.cos(Y)  # Sine wave terrain

create_hfield_file("custom_terrain.hfield", Z)
```

## API Reference

For more HField-related APIs, please refer to:

-   [`HField API`]: Complete height field class interface documentation
-   [`SceneModel.get_hfield()`]: Method to get height field objects
-   [`SceneModel.num_hfields`]: Get number of height fields

[`model.num_hfields`]: motrixsim.SceneModel.num_hfields
[`model.get_hfield(name_or_index)`]: motrixsim.SceneModel.get_hfield
[`HField API`]: motrixsim.HField
[`SceneModel.get_hfield()`]: motrixsim.SceneModel.get_hfield
[`SceneModel.num_hfields`]: motrixsim.SceneModel.num_hfields
