# 🤖 Rigid Body (Body)

In the world of MotrixSim, a Body can be a single rigid body or an articulated body composed of joints and links. Visually, it can be represented as follows:

![body](/_static/images/body.png)

Note that the connection between a Body and the World can be floating (floating base), fixed, or connected via a joint.

## MJCF Mapping

When you use MJCF for scene description, MotrixSim treats each top-level `<body>` element under `<worldbody>` and its entire subtree as a Body, forming a kinematic tree structure.

Consider the following example:

```{literalinclude} ../../../../../examples/assets/body.xml
:language: xml
:dedent:
```

In this MJCF file, there are three `<body>` elements at the top level under `<worldbody>`, so MotrixSim parses them as three Bodies.

```{literalinclude} ../../../../../examples/body.py
:language: python
:dedent:
:start-after: "# tag::num_bodies"
:end-before:  "# end::num_bodies"
```

Note the third body named "capsule". It has a child body and is connected via a hinge joint. Therefore, in MotrixSim, this body is parsed as an articulated body, which contains two links and one joint.

```{literalinclude} ../../../../../examples/body.py
:language: python
:dedent:
:start-after: "# tag::articulated_body"
:end-before:  "# end::articulated_body"

```

```{note}
Do not confuse the `<body>` tag in MJCF with the `Body` object in MotrixSim.
The `<body>` tag in MJCF is mapped to a `Link` object in MotrixSim. For more information about links, see [Link](link.md).
```

### freejoint

If a `<body>` element in MJCF contains a `<freejoint>` element, the corresponding `Body` object will have the floatingbase property:

```{literalinclude} ../../../../../examples/body.py
:language: python
:dedent:
:start-after: "# tag::floatingbase"
:end-before:  "# end::floatingbase"
```

With the floatingbase object, you can perform additional operations that are only available to free-moving bodies. For more details, see [FloatingBase](floating_base.md).

## API Reference

For more APIs related to Body, see [`Body API`]

[`Body API`]: motrixsim.Body
