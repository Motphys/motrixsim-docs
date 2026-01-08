# Contact Sensor

Contact sensors are used to detect and report contact information between two objects (or geometries), including contact point position, contact force, normal vectors, and other detailed data. In robot simulation, contact sensors are commonly used for foot contact detection, grasping force feedback, collision detection, and other application scenarios.

## 🎯 Functionality Description

Contact sensors monitor contact events between specified geometry pairs or object pairs and return detailed contact information. The sensor can be configured to return different types of data, including contact status, contact force, contact position, normal vectors, etc.

## 📋 Return Value Format

```python
contact_data = model.get_sensor_value("contact_sensor_name", data)
# Type: numpy.ndarray[float32]
```

## ⚙️ MJCF Configuration Parameters

In MotrixSim, contact sensors support the following MJCF configurations:

### Basic Configuration Format

```xml
<sensor>
    <contact name="sensor_name"
             geom1="geom1_name"
             geom2="geom2_name"
             data="found force pos normal tangent"
             num="4"
             reduce="none"
           />
</sensor>
```

### Supported Attributes

| Attribute Name | Type   | Required | Default | Description                                |
| -------------- | ------ | -------- | ------- | ------------------------------------------ |
| **name**       | string | ✅       | -       | Unique identifier name for the sensor      |
| **geom1**      | string | ❌       | -       | First geometry name (used with geom2)      |
| **geom2**      | string | ❌       | -       | Second geometry name (used with geom1)     |
| **body1**      | string | ❌       | -       | First body name (used with body2)          |
| **body2**      | string | ❌       | -       | Second body name (used with body1)         |
| **subtree1**   | string | ❌       | -       | First subtree name (used with subtree2)    |
| **subtree2**   | string | ❌       | -       | Second subtree name (used with subtree1)   |
| **site**       | string | ❌       | -       | Reference point name                       |
| **data**       | string | ❌       | "found" | Data types to return, separated by spaces  |
| **num**        | int    | ❌       | 1       | Maximum number of contact points to report |
| **reduce**     | string | ❌       | "none"  | Data reduction method                      |

### Target Object Configuration (Four Methods)

#### 1. Geometry Pair (Recommended)

```xml
<contact name="floor_contact" geom1="bar" geom2="freebox"/>
```

#### 2. Body Pair

```xml
<contact name="body_contact" body1="body1_name" body2="body2_name"/>
```

#### 3. Subtree Pair

```xml
<contact name="subtree_contact" subtree1="subtree1_name" subtree2="subtree2_name"/>
```

#### 4. Site Point

```xml
<contact name="site_contact" site="site_name"/>
```

### Data Types (data attribute)

The following values can be combined:

| Value       | Description                                      | Data Usage                 |
| ----------- | ------------------------------------------------ | -------------------------- |
| **found**   | Contact point count                              | 1 value                    |
| **force**   | Contact force projection (normal + 2 tangential) | 3 values per contact point |
| **torque**  | Contact torque                                   | 3 values per contact point |
| **dist**    | Penetration depth                                | 1 value per contact point  |
| **pos**     | Contact point position                           | 3 values per contact point |
| **normal**  | Normal vector                                    | 3 values per contact point |
| **tangent** | First tangential vector                          | 3 values per contact point |

### Data Reduction Methods (reduce attribute)

| Value        | Description                                                          |
| ------------ | -------------------------------------------------------------------- |
| **none**     | Return all contact points (up to num)                                |
| **mindist**  | Return only the closest contact point                                |
| **maxforce** | Return only the contact point with maximum force                     |
| **netforce** | Return the resultant force of all contact points (simplified format) |

## 📐 Return Array Length and Content Layout

The length and content layout of the array returned by the contact sensor depend on three key configuration parameters: the `data` attribute (specifying data types), the `num` attribute (maximum number of contact points), and the `reduce` attribute (data reduction method).

### Array Length Calculation Formula

```python
total_size = 1 + max_num_contacts × values_per_contact
```

-   **1**: The `found` field, indicating the actual number of contact points
-   **max_num_contacts**: Maximum number of contact points set by the `num` parameter in MJCF configuration (fixed array size)
-   **values_per_contact**: Number of data values per contact point (depends on `data` configuration)

**Important**: The array size is fixed and unaffected by the actual number of contact points. If there are fewer actual contact points than `max_num_contacts`, the remaining positions are filled with 0.

### Impact of data Attribute on Data Per Contact Point

Different `data` type combinations produce different `values_per_contact`:

| data configuration                 | Values per contact point | Data layout (in order)                                                                 |
| ---------------------------------- | ------------------------ | -------------------------------------------------------------------------------------- |
| `"found"`                          | 0                        | Contact status only                                                                    |
| `"found force"`                    | 3                        | [normal force, tangential 0 force, tangential 1 force]                                 |
| `"found force pos"`                | 6                        | [3 force components, 3 position coordinates]                                           |
| `"found force pos normal"`         | 9                        | [3 force components, 3 position coordinates, 3 normal vectors]                         |
| `"found force pos normal tangent"` | 12                       | [3 force components, 3 position coordinates, 3 normal vectors, 3 tangential vectors 0] |
| `"found pos normal"`               | 6                        | [3 position coordinates, 3 normal vectors]                                             |
| `"found force torque"`             | 6                        | [3 force components, 3 torque components]                                              |

**Note**: Space occupied by each data type:

-   `found`: 1 value (included in all configurations)
-   `force`: 3 values (normal + 2 tangential force projections)
-   `torque`: 3 values (contact torque)
-   `dist`: 1 value (penetration depth)
-   `pos`: 3 values (contact point position)
-   `normal`: 3 values (normal vector)
-   `tangent`: 3 values (first tangential vector)

### Impact of reduce Attribute on Contact Point Count

The `reduce` attribute determines which contact points are returned and how many:

#### reduce="none" (default)

-   **Behavior**: Returns the first `num` contact points that meet matching criteria, in the order they appear in mjData.contact
-   **Characteristics**: Fastest option, but may be non-deterministic (collision detection algorithm changes may alter contact point identity and order)
-   **Contact point count**: Up to `num`, possibly fewer than `num` (if fewer actual contact points)

#### reduce="mindist"

-   **Behavior**: Returns the `num` contact points with smallest penetration depth, sorted by depth in ascending order
-   **Contact point count**: Up to `num`, possibly fewer than `num`

#### reduce="maxforce"

-   **Behavior**: Returns the `num` contact points with largest force norm, sorted by force magnitude in descending order
-   **Contact point count**: Up to `num`, possibly fewer than `num`

#### reduce="netforce"

-   **Behavior**: Returns a "synthetic" contact point with the following characteristics:
    -   Position: Force-weighted centroid of all matching contact points
    -   Coordinate system: **Global coordinate system** (normal and tangent lose original semantic meaning)
    -   Forces and torques: Calculated as forces and torques applied at the calculated position, producing the same net effect as all matching contact points
-   **Contact point count**: **Always exactly 1** (ignores `num` setting)
-   **Special note**: Due to using the global coordinate system, data interpretation differs from other reduce types

### Specific Configuration Examples

#### Example 1: Complete Contact Information (reduce="none")

```xml
<contact name="full_contact"
         geom1="bar" geom2="freebox"
         data="found force pos normal tangent"
         num="4"
         reduce="none"/>
```

**Returned data layout**:

```python
contact_data = model.get_sensor_value("full_contact", data)
# Shape: shape = (1 + 4×12,) = (49,) fixed size (determined by num="4")
# Array size is fixed, insufficient contact points are padded with 0

# Data structure:
contact_data[0]              # Actual contact point count (e.g., 2, remaining 2 are padding)

# First contact point (offset = 1, valid data):
contact_data[1:4]           # Force components: [normal force, tangential 0 force, tangential 1 force]
contact_data[4:7]           # Position: [x, y, z]
contact_data[7:10]          # Normal vector: [nx, ny, nz]
contact_data[10:13]         # Tangential vector 0: [tx0, ty0, tz0]

# Second contact point (offset = 13, valid data):
contact_data[13:16]         # Force components
contact_data[16:19]         # Position
contact_data[19:22]         # Normal vector
contact_data[22:25]         # Tangential vector 0

# Third contact point (offset = 25, padded with 0):
contact_data[25:37]         # All zeros (no contact)

# Fourth contact point (offset = 37, padded with 0):
contact_data[37:49]         # All zeros (no contact)
```

#### Example 2: Simplified Contact Information (reduce="maxforce")

```xml
<contact name="force_contact"
         geom1="bar" geom2="freebox"
         data="found force pos"
         num="5"
         reduce="maxforce"/>
```

**Returned data layout**:

```python
contact_data = model.get_sensor_value("force_contact", data)
# Shape: shape = (1 + 5×6,) = (31,) fixed size (determined by num="5")
# Array size is fixed, returns up to 5 contact points with maximum force, sorted by force in descending order
# Insufficient contact points are padded with 0

contact_data[0]              # Actual contact point count (e.g., 3)

# i-th contact point: 6 values per contact point
# Only the first contact_data[0] contact points contain valid data
offset = 1 + i * 6
contact_data[offset + 0:offset + 3]  # Force components
contact_data[offset + 3:offset + 6]  # Position
# Note: when i >= contact_data[0], the above data are all 0
```

#### Example 3: Contact Status Only (Most Simplified)

```xml
<contact name="touch_only"
         geom1="bar" geom2="freebox"
         data="found"
         num="1"/>
```

**Returned data layout**:

```python
contact_data = model.get_sensor_value("touch_only", data)
# Shape: shape = (1,) always only 1 value

contact_data[0]  # Contact point count (0 = no contact, 1 = has contact)
```

#### Example 4: Resultant Force Information (reduce="netforce")

```xml
<contact name="net_force"
         geom1="bar" geom2="freebox"
         data="found force pos normal tangent"
         num="10"
         reduce="netforce"/>
```

**Returned data layout**:

```python
contact_data = model.get_sensor_value("net_force", data)
# Shape: shape = (1 + 1×12,) = (13,) always returns 1 synthetic contact point (ignores num="10")

contact_data[0]              # Always 1 (synthetic contact point)

# Synthetic contact point data (global coordinate system):
contact_data[1:4]           # Resultant force components
contact_data[4:7]           # Force-weighted centroid position
contact_data[7:10]          # Normal vector (global coordinate system, semantic changed)
contact_data[10:13]         # Tangential vector 0 (global coordinate system, semantic changed)
```

### Important Notes

1. **Fixed array size**: The returned array size is fixed, determined by the `num` parameter: `shape = (1 + num × values_per_contact,)`
2. **Zero padding mechanism**: If the actual number of contact points is less than `num`, remaining positions are filled with 0, need to use `contact_data[0]` to determine valid data
3. **found field reliability**: Always use `contact_data[0]` to determine the actual number of contact points, do not assume the entire array is valid
4. **netforce special handling**: `reduce="netforce"` has different coordinate system and data interpretation from other types, and always returns 1 contact point
5. **Performance optimization**: For applications that only need contact status, using `data="found"` can significantly improve performance

## 🐍 Python Demo

Below is a complete contact sensor visualization example, showing how to obtain and render contact force data in real-time. This example comes from the `site_and_sensor.py` file, demonstrating the practical application effects of contact sensors.

### Scene Configuration

First, we define a scene containing a contact sensor:

```{literalinclude} ../../../../../examples/assets/site_and_sensor.xml
:language: xml
:lines: 50-51
```

This configuration creates a contact sensor named `box_floor_contact` that monitors contact between two geometries `bar` and `freebox`, returning complete contact information (force, position, normal vector, tangential vector).

### Python Code

Below is the complete contact sensor visualization code:

```{literalinclude} ../../../../../examples/site_and_sensor.py
:language: python
:lines: 16-19
:lines: 91-142
```

**Note**: Only contact sensor related parts are shown here. The complete example code also includes scene setup, other sensor types, rendering loops, and other content.

### Visualization Description

This example displays the various components of contact force in real-time through color-coded arrows:

-   **White sphere**: Contact point position
-   **Green arrow**: Normal force (perpendicular to contact surface)
-   **Red arrow**: Tangential friction force component 0
-   **Blue arrow**: Tangential friction force component 1 (calculated via cross product)

### Effect Demonstration

```{video} /_static/videos/contact_sensor.mp4
:nocontrols:
:autoplay:
:playsinline:
:muted:
:loop:
:width: 100%
```

This video demonstrates the real-time visualization effect of the contact sensor, including:

-   Contact point detection when objects contact the ground
-   Real-time calculation and display of contact forces
-   Visualization of force components in different directions
-   Dynamic process of force magnitude changing with object motion

## 📊 Physical Principles

### Contact Coordinate System

Contact sensors use a local contact coordinate system to report contact data:

1. **Normal vector**: Perpendicular to the contact surface, pointing from object 1 to object 2
2. **Tangential vectors (tangent0, tangent1)**: Form an orthogonal basis within the contact plane
3. **Force projection**: Projection values of contact force on the three axes

### Contact Force Decomposition

```
Total contact force = Normal force + Tangential force (friction)
F_total = F_normal + F_tangent0 + F_tangent1
```

-   **Normal force**: Positive pressure, preventing objects from penetrating each other
-   **Tangential force**: Friction, preventing relative sliding between contact surfaces

### Contact Detection

Contact sensors work based on the collision detection system:

1. Detect spatial overlap between two geometries
2. Calculate contact point position and normal vector
3. Calculate contact force based on penetration depth and material properties
4. Project contact force into local contact coordinate system

## ⚠️ Important Notes

1. **Force components are scalars**: `force_normal_mag`, `force_tangent0_mag`, `force_tangent1_mag` are force projection values, not complete force vectors
2. **Second tangential vector**: Needs to be calculated via `tangent1 = cross(normal, tangent0)`
3. **Coordinate system**: All data are represented in the local contact coordinate system, not the global coordinate system
4. **Performance considerations**: Contact sensor computation is intensive, recommend setting the `num` attribute reasonably to limit the number of reported contact points
5. **Configuration mutual exclusion**: `geom1/geom2`, `body1/body2`, `subtree1/subtree2`, `site` - these four configuration methods can only be used one at a time
