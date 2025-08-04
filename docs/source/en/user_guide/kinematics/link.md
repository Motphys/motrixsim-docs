# 📏 Link

We refer to the rigid components in a multibody system as links. In MotrixSim, a link is an important concept representing each rigid part of a multibody system. Each link can have different properties and behaviors, and is connected to other links via joints.

![link](../../../_static/images/link.png)

## MJCF Mapping

When you use MJCF to describe a multibody system, MotrixSim maps all `<body>` elements to `Link` objects.

For the current support status of `<body>` tag attributes in MJCF, see [MJCF Support Status](../getting_started/mjcf.md#scene).

```{note}
The `<worldbody>` element in MJCF is not treated as a Link object.
```

## Main Interfaces

In MotrixSim, you can access Link objects as follows:

-   [`model.num_links`]: Get the number of Link objects in the current world.
-   [`model.links`]: Get all Link objects in the current world.
-   [`model.get_link(key)`]: Get a specific Link object by name or index.

Once you have a Link object, you can manipulate it using a variety of properties and methods. For more detailed APIs, refer to the [`Link API`].

## Example

You can run a simple example demonstrating link API usage with:

```bash
pdm run examples/link.py
```

See the source code at [`examples/link.py`](../../../../../examples/link.py).

## API Reference

For more APIs related to Link, see [`Link API`]

[`model.num_links`]: motrixsim.SceneModel.num_links
[`model.links`]: motrixsim.SceneModel.links
[`model.get_link(key)`]: motrixsim.SceneModel.get_link
[`Link API`]: motrixsim.Link
