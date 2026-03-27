---
title: 📖 MJCF XML Reference
description: Complete MJCF XML reference with hierarchy
outline: [2, 6]
---

# 📖 MJCF XML Reference

This document provides a hierarchical reference for all supported MJCF XML elements.

```{note}
Items marked with <span class="badge mpex">MPEX</span> (**M**ot**p**hys **Ex**tension) are Motphys-specific extensions to the standard MJCF specification and are not part of the original MuJoCo format.
```

## Index

<div class="mjcf-index">
<div style="margin-bottom: 6px;">
<details open>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#mujoco" style="text-decoration: none; color: inherit;">mujoco</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#mujoco-model" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">model</a></div>
</div>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#extension" style="text-decoration: none; color: inherit;">extension</a></summary>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#plugin" style="text-decoration: none; color: inherit;">plugin</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#plugin-plugin" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">plugin</a></div>
</div>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#instance" style="text-decoration: none; color: inherit;">instance</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#instance-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
</div>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#config" style="text-decoration: none; color: inherit;">config</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#config-key" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">key</a></div>
  <div><a href="#config-value" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">value</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#compiler" style="text-decoration: none; color: inherit;">compiler</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#compiler-angle" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">angle</a></div>
  <div><a href="#compiler-assetdir" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">assetdir</a></div>
  <div><a href="#compiler-autolimits" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">autolimits</a></div>
  <div><a href="#compiler-eulerseq" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">eulerseq</a></div>
  <div><a href="#compiler-fitaabb" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">fitaabb</a></div>
  <div><a href="#compiler-meshdir" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">meshdir</a></div>
  <div><a href="#compiler-texturedir" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">texturedir</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#asset" style="text-decoration: none; color: inherit;">asset</a></summary>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#material" style="text-decoration: none; color: inherit;">material</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#material-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#material-depthbias" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">depthbias</a></div>
  <div><a href="#material-detailpara" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">detailpara</a></div>
  <div><a href="#material-emission" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">emission</a></div>
  <div><a href="#material-emissionintensity" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">emissionintensity</a></div>
  <div><a href="#material-metallic" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">metallic</a></div>
  <div><a href="#material-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#material-reflectance" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">reflectance</a></div>
  <div><a href="#material-rgba" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">rgba</a></div>
  <div><a href="#material-roughness" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">roughness</a></div>
  <div><a href="#material-texrepeat" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">texrepeat</a></div>
  <div><a href="#material-texture" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">texture</a></div>
  <div><a href="#material-texuniform" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">texuniform</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#mesh" style="text-decoration: none; color: inherit;">mesh</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#mesh-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#mesh-face" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">face</a></div>
  <div><a href="#mesh-file" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">file</a></div>
  <div><a href="#mesh-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#mesh-normal" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">normal</a></div>
  <div><a href="#mesh-refpos" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">refpos</a></div>
  <div><a href="#mesh-refquat" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">refquat</a></div>
  <div><a href="#mesh-scale" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">scale</a></div>
  <div><a href="#mesh-texcoord" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">texcoord</a></div>
  <div><a href="#mesh-vertex" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">vertex</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#texture" style="text-decoration: none; color: inherit;">texture</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#texture-builtin" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">builtin</a></div>
  <div><a href="#texture-colorspace" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">colorspace</a></div>
  <div><a href="#texture-file" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">file</a></div>
  <div><a href="#texture-gridlayout" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gridlayout</a></div>
  <div><a href="#texture-gridsize" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gridsize</a></div>
  <div><a href="#texture-height" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">height</a></div>
  <div><a href="#texture-mark" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">mark</a></div>
  <div><a href="#texture-markrgb" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">markrgb</a></div>
  <div><a href="#texture-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#texture-rgb1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">rgb1</a></div>
  <div><a href="#texture-rgb2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">rgb2</a></div>
  <div><a href="#texture-type" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">type</a></div>
  <div><a href="#texture-width" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">width</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#hfield" style="text-decoration: none; color: inherit;">hfield</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#hfield-content_type" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">content_type</a></div>
  <div><a href="#hfield-elevation" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">elevation</a></div>
  <div><a href="#hfield-file" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">file</a></div>
  <div><a href="#hfield-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#hfield-ncol" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ncol</a></div>
  <div><a href="#hfield-nrow" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">nrow</a></div>
  <div><a href="#hfield-size" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">size</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#model" style="text-decoration: none; color: inherit;">model</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#model-file" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">file</a></div>
  <div><a href="#model-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#default" style="text-decoration: none; color: inherit;">default</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#default-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
</div>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#default" style="text-decoration: none; color: inherit;">default</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#geom" style="text-decoration: none; color: inherit;">geom</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#joint" style="text-decoration: none; color: inherit;">joint</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#light" style="text-decoration: none; color: inherit;">light</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#mesh" style="text-decoration: none; color: inherit;">mesh</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#material" style="text-decoration: none; color: inherit;">material</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#general" style="text-decoration: none; color: inherit;">general</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#motor" style="text-decoration: none; color: inherit;">motor</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#position" style="text-decoration: none; color: inherit;">position</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#velocity" style="text-decoration: none; color: inherit;">velocity</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#adhesion" style="text-decoration: none; color: inherit;">adhesion</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#camera" style="text-decoration: none; color: inherit;">camera</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#site" style="text-decoration: none; color: inherit;">site</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#tendon" style="text-decoration: none; color: inherit;">tendon</a></div>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<div style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; font-weight: 600; font-family: monospace;"><a href="#equality" style="text-decoration: none; color: inherit;">equality</a></div>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#worldbody" style="text-decoration: none; color: inherit;">(world)body</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#worldbody-axisangle" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">axisangle</a></div>
  <div><a href="#worldbody-childclass" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">childclass</a></div>
  <div><a href="#worldbody-euler" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">euler</a></div>
  <div><a href="#worldbody-gravcomp" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gravcomp</a></div>
  <div><a href="#worldbody-mocap" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">mocap</a></div>
  <div><a href="#worldbody-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#worldbody-pos" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">pos</a></div>
  <div><a href="#worldbody-quat" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">quat</a></div>
  <div><a href="#worldbody-xyaxes" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">xyaxes</a></div>
  <div><a href="#worldbody-zaxis" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">zaxis</a></div>
</div>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#inertial" style="text-decoration: none; color: inherit;">inertial</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#inertial-axisangle" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">axisangle</a></div>
  <div><a href="#inertial-diaginertia" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">diaginertia</a></div>
  <div><a href="#inertial-euler" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">euler</a></div>
  <div><a href="#inertial-fullinertia" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">fullinertia</a></div>
  <div><a href="#inertial-mass" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">mass</a></div>
  <div><a href="#inertial-pos" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">pos</a></div>
  <div><a href="#inertial-quat" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">quat</a></div>
  <div><a href="#inertial-xyaxes" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">xyaxes</a></div>
  <div><a href="#inertial-zaxis" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">zaxis</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#joint" style="text-decoration: none; color: inherit;">joint</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#joint-actuatorfrclimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">actuatorfrclimited</a></div>
  <div><a href="#joint-actuatorfrcrange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">actuatorfrcrange</a></div>
  <div><a href="#joint-armature" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">armature</a></div>
  <div><a href="#joint-axis" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">axis</a></div>
  <div><a href="#joint-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#joint-damping" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">damping</a></div>
  <div><a href="#joint-frictionloss" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">frictionloss</a></div>
  <div><a href="#joint-group" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">group</a></div>
  <div><a href="#joint-hardlimit" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">hardlimit</a></div>
  <div><a href="#joint-limited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">limited</a></div>
  <div><a href="#joint-margin" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">margin</a></div>
  <div><a href="#joint-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#joint-pos" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">pos</a></div>
  <div><a href="#joint-range" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">range</a></div>
  <div><a href="#joint-ref" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ref</a></div>
  <div><a href="#joint-solimpfriction" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solimpfriction</a></div>
  <div><a href="#joint-solimplimit" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solimplimit</a></div>
  <div><a href="#joint-solreffriction" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solreffriction</a></div>
  <div><a href="#joint-solreflimit" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solreflimit</a></div>
  <div><a href="#joint-springdamper" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">springdamper</a></div>
  <div><a href="#joint-springref" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">springref</a></div>
  <div><a href="#joint-stiffness" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">stiffness</a></div>
  <div><a href="#joint-type" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">type</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#freejoint" style="text-decoration: none; color: inherit;">freejoint</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#freejoint-group" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">group</a></div>
  <div><a href="#freejoint-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#attach" style="text-decoration: none; color: inherit;">attach</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#attach-body" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body</a></div>
  <div><a href="#attach-model" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">model</a></div>
  <div><a href="#attach-prefix" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">prefix</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#camera" style="text-decoration: none; color: inherit;">camera</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#camera-axisangle" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">axisangle</a></div>
  <div><a href="#camera-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#camera-depth" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">depth</a></div>
  <div><a href="#camera-euler" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">euler</a></div>
  <div><a href="#camera-fovy" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">fovy</a></div>
  <div><a href="#camera-mode" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">mode</a></div>
  <div><a href="#camera-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#camera-orthographic" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">orthographic</a></div>
  <div><a href="#camera-pos" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">pos</a></div>
  <div><a href="#camera-quat" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">quat</a></div>
  <div><a href="#camera-target" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">target</a></div>
  <div><a href="#camera-trackposspeed" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">trackposspeed</a></div>
  <div><a href="#camera-trackrotspeed" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">trackrotspeed</a></div>
  <div><a href="#camera-xyaxes" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">xyaxes</a></div>
  <div><a href="#camera-zaxis" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">zaxis</a></div>
  <div><a href="#camera-zfar" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">zfar</a></div>
  <div><a href="#camera-znear" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">znear</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#frame" style="text-decoration: none; color: inherit;">frame</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#frame-axisangle" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">axisangle</a></div>
  <div><a href="#frame-childclass" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">childclass</a></div>
  <div><a href="#frame-euler" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">euler</a></div>
  <div><a href="#frame-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#frame-pos" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">pos</a></div>
  <div><a href="#frame-quat" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">quat</a></div>
  <div><a href="#frame-xyaxes" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">xyaxes</a></div>
  <div><a href="#frame-zaxis" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">zaxis</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#geom" style="text-decoration: none; color: inherit;">geom</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#geom-axisangle" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">axisangle</a></div>
  <div><a href="#geom-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#geom-conaffinity" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">conaffinity</a></div>
  <div><a href="#geom-condim" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">condim</a></div>
  <div><a href="#geom-contype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">contype</a></div>
  <div><a href="#geom-density" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">density</a></div>
  <div><a href="#geom-euler" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">euler</a></div>
  <div><a href="#geom-friction" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">friction</a></div>
  <div><a href="#geom-fromto" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">fromto</a></div>
  <div><a href="#geom-gap" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gap</a></div>
  <div><a href="#geom-group" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">group</a></div>
  <div><a href="#geom-hfield" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">hfield</a></div>
  <div><a href="#geom-margin" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">margin</a></div>
  <div><a href="#geom-mass" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">mass</a></div>
  <div><a href="#geom-material" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">material</a></div>
  <div><a href="#geom-mesh" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">mesh</a></div>
  <div><a href="#geom-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#geom-pos" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">pos</a></div>
  <div><a href="#geom-priority" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">priority</a></div>
  <div><a href="#geom-quat" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">quat</a></div>
  <div><a href="#geom-rgba" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">rgba</a></div>
  <div><a href="#geom-size" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">size</a></div>
  <div><a href="#geom-solimp" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solimp</a></div>
  <div><a href="#geom-solmix" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solmix</a></div>
  <div><a href="#geom-solref" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solref</a></div>
  <div><a href="#geom-type" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">type</a></div>
  <div><a href="#geom-xyaxes" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">xyaxes</a></div>
  <div><a href="#geom-zaxis" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">zaxis</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#light" style="text-decoration: none; color: inherit;">light</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#light-ambient" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ambient</a></div>
  <div><a href="#light-attenuation" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">attenuation</a></div>
  <div><a href="#light-bulbradius" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">bulbradius</a></div>
  <div><a href="#light-castshadow" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">castshadow</a></div>
  <div><a href="#light-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#light-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#light-diffuse" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">diffuse</a></div>
  <div><a href="#light-dir" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">dir</a></div>
  <div><a href="#light-directional" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">directional</a></div>
  <div><a href="#light-innerangle" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">innerangle</a></div>
  <div><a href="#light-intensity" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">intensity</a></div>
  <div><a href="#light-mode" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">mode</a></div>
  <div><a href="#light-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#light-nearz" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">nearz</a></div>
  <div><a href="#light-pos" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">pos</a></div>
  <div><a href="#light-range" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">range</a></div>
  <div><a href="#light-specular" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">specular</a></div>
  <div><a href="#light-target" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">target</a></div>
  <div><a href="#light-type" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">type</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#replicate" style="text-decoration: none; color: inherit;">replicate</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#replicate-count" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">count</a></div>
  <div><a href="#replicate-euler" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">euler</a></div>
  <div><a href="#replicate-offset" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">offset</a></div>
  <div><a href="#replicate-sep" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">sep</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#site" style="text-decoration: none; color: inherit;">site</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#site-axisangle" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">axisangle</a></div>
  <div><a href="#site-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#site-euler" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">euler</a></div>
  <div><a href="#site-fromto" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">fromto</a></div>
  <div><a href="#site-group" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">group</a></div>
  <div><a href="#site-material" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">material</a></div>
  <div><a href="#site-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#site-pos" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">pos</a></div>
  <div><a href="#site-quat" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">quat</a></div>
  <div><a href="#site-rgba" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">rgba</a></div>
  <div><a href="#site-size" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">size</a></div>
  <div><a href="#site-type" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">type</a></div>
  <div><a href="#site-xyaxes" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">xyaxes</a></div>
  <div><a href="#site-zaxes" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">zaxes</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#option" style="text-decoration: none; color: inherit;">option</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#option-gravity" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gravity</a></div>
  <div><a href="#option-iterations" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">iterations</a></div>
  <div><a href="#option-o_friction" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">o_friction</a></div>
  <div><a href="#option-o_margin" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">o_margin</a></div>
  <div><a href="#option-o_solimp" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">o_solimp</a></div>
  <div><a href="#option-o_solref" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">o_solref</a></div>
  <div><a href="#option-timestep" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">timestep</a></div>
  <div><a href="#option-tolerance" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">tolerance</a></div>
</div>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#flag" style="text-decoration: none; color: inherit;">flag</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#flag-actuation" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">actuation</a></div>
  <div><a href="#flag-constraint" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">constraint</a></div>
  <div><a href="#flag-contact" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">contact</a></div>
  <div><a href="#flag-equality" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">equality</a></div>
  <div><a href="#flag-frictionloss" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">frictionloss</a></div>
  <div><a href="#flag-gravity" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gravity</a></div>
  <div><a href="#flag-limit" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">limit</a></div>
  <div><a href="#flag-override" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">override</a></div>
  <div><a href="#flag-refsafe" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">refsafe</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#actuator" style="text-decoration: none; color: inherit;">actuator</a></summary>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#adhesion" style="text-decoration: none; color: inherit;">adhesion</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#adhesion-body" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body</a></div>
  <div><a href="#adhesion-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#adhesion-ctrllimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrllimited</a></div>
  <div><a href="#adhesion-ctrlrange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrlrange</a></div>
  <div><a href="#adhesion-forcelimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">forcelimited</a></div>
  <div><a href="#adhesion-forcerange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">forcerange</a></div>
  <div><a href="#adhesion-gain" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gain</a></div>
  <div><a href="#adhesion-gear" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gear</a></div>
  <div><a href="#adhesion-group" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">group</a></div>
  <div><a href="#adhesion-joint" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint</a></div>
  <div><a href="#adhesion-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#adhesion-tendon" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">tendon</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#general" style="text-decoration: none; color: inherit;">general</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#general-actearly" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">actearly</a></div>
  <div><a href="#general-biasprm" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">biasprm</a></div>
  <div><a href="#general-biastype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">biastype</a></div>
  <div><a href="#general-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#general-ctrllimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrllimited</a></div>
  <div><a href="#general-ctrlrange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrlrange</a></div>
  <div><a href="#general-dynprm" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">dynprm</a></div>
  <div><a href="#general-dyntype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">dyntype</a></div>
  <div><a href="#general-forcelimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">forcelimited</a></div>
  <div><a href="#general-forcerange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">forcerange</a></div>
  <div><a href="#general-gainprm" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gainprm</a></div>
  <div><a href="#general-gaintype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gaintype</a></div>
  <div><a href="#general-gear" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gear</a></div>
  <div><a href="#general-group" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">group</a></div>
  <div><a href="#general-joint" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint</a></div>
  <div><a href="#general-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#general-tendon" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">tendon</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#motor" style="text-decoration: none; color: inherit;">motor</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#motor-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#motor-ctrllimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrllimited</a></div>
  <div><a href="#motor-ctrlrange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrlrange</a></div>
  <div><a href="#motor-forcelimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">forcelimited</a></div>
  <div><a href="#motor-forcerange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">forcerange</a></div>
  <div><a href="#motor-gear" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gear</a></div>
  <div><a href="#motor-group" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">group</a></div>
  <div><a href="#motor-joint" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint</a></div>
  <div><a href="#motor-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#motor-tendon" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">tendon</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#position" style="text-decoration: none; color: inherit;">position</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#position-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#position-ctrllimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrllimited</a></div>
  <div><a href="#position-ctrlrange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrlrange</a></div>
  <div><a href="#position-forcelimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">forcelimited</a></div>
  <div><a href="#position-forcerange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">forcerange</a></div>
  <div><a href="#position-gear" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gear</a></div>
  <div><a href="#position-group" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">group</a></div>
  <div><a href="#position-inheritrange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">inheritrange</a></div>
  <div><a href="#position-joint" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint</a></div>
  <div><a href="#position-kp" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">kp</a></div>
  <div><a href="#position-kv" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">kv</a></div>
  <div><a href="#position-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#position-tendon" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">tendon</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#velocity" style="text-decoration: none; color: inherit;">velocity</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#velocity-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#velocity-ctrllimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrllimited</a></div>
  <div><a href="#velocity-ctrlrange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrlrange</a></div>
  <div><a href="#velocity-forcelimited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">forcelimited</a></div>
  <div><a href="#velocity-forcerange" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">forcerange</a></div>
  <div><a href="#velocity-gear" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gear</a></div>
  <div><a href="#velocity-group" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">group</a></div>
  <div><a href="#velocity-joint" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint</a></div>
  <div><a href="#velocity-kv" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">kv</a></div>
  <div><a href="#velocity-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#velocity-tendon" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">tendon</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#visual" style="text-decoration: none; color: inherit;">visual</a></summary>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#headlight" style="text-decoration: none; color: inherit;">headlight</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#headlight-active" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">active</a></div>
  <div><a href="#headlight-ambient" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ambient</a></div>
  <div><a href="#headlight-diffuse" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">diffuse</a></div>
  <div><a href="#headlight-specular" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">specular</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#global" style="text-decoration: none; color: inherit;">global</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#global-azimuth" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">azimuth</a></div>
  <div><a href="#global-elevation" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">elevation</a></div>
  <div><a href="#global-fovy" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">fovy</a></div>
  <div><a href="#global-orthographic" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">orthographic</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#map" style="text-decoration: none; color: inherit;">map</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#map-envmapintensity" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">envmapintensity</a></div>
  <div><a href="#map-fogend" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">fogend</a></div>
  <div><a href="#map-fogstart" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">fogstart</a></div>
  <div><a href="#map-zfar" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">zfar</a></div>
  <div><a href="#map-znear" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">znear</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#rgba" style="text-decoration: none; color: inherit;">rgba</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#rgba-bv" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">bv</a></div>
  <div><a href="#rgba-contactforce" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">contactforce</a></div>
  <div><a href="#rgba-fog" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">fog</a></div>
  <div><a href="#rgba-haze" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">haze</a></div>
  <div><a href="#rgba-joint" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#probe" style="text-decoration: none; color: inherit;">probe</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#probe-position" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">position</a></div>
  <div><a href="#probe-scale" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">scale</a></div>
  <div><a href="#probe-texture" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">texture</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#ssao" style="text-decoration: none; color: inherit;">ssao</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#ssao-active" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">active</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#tonemapping" style="text-decoration: none; color: inherit;">tonemapping</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#tonemapping-method" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">method</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#equality" style="text-decoration: none; color: inherit;">equality</a></summary>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#connect" style="text-decoration: none; color: inherit;">connect</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#connect-active" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">active</a></div>
  <div><a href="#connect-anchor" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">anchor</a></div>
  <div><a href="#connect-body1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body1</a></div>
  <div><a href="#connect-body2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body2</a></div>
  <div><a href="#connect-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#connect-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#connect-site1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">site1</a></div>
  <div><a href="#connect-site2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">site2</a></div>
  <div><a href="#connect-solimp" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solimp</a></div>
  <div><a href="#connect-solref" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solref</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#joint" style="text-decoration: none; color: inherit;">joint</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#joint-active" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">active</a></div>
  <div><a href="#joint-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#joint-joint1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint1</a></div>
  <div><a href="#joint-joint2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint2</a></div>
  <div><a href="#joint-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#joint-polycoef" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">polycoef</a></div>
  <div><a href="#joint-solimp" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solimp</a></div>
  <div><a href="#joint-solref" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solref</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#weld" style="text-decoration: none; color: inherit;">weld</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#weld-active" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">active</a></div>
  <div><a href="#weld-anchor" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">anchor</a></div>
  <div><a href="#weld-body1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body1</a></div>
  <div><a href="#weld-body2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body2</a></div>
  <div><a href="#weld-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#weld-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#weld-relpose" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">relpose</a></div>
  <div><a href="#weld-site1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">site1</a></div>
  <div><a href="#weld-site2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">site2</a></div>
  <div><a href="#weld-solimp" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solimp</a></div>
  <div><a href="#weld-solref" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solref</a></div>
  <div><a href="#weld-torquescale" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">torquescale</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#contact" style="text-decoration: none; color: inherit;">contact</a></summary>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#exclude" style="text-decoration: none; color: inherit;">exclude</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#exclude-body1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body1</a></div>
  <div><a href="#exclude-body2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body2</a></div>
  <div><a href="#exclude-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#pair" style="text-decoration: none; color: inherit;">pair</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#pair-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#pair-condim" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">condim</a></div>
  <div><a href="#pair-friction" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">friction</a></div>
  <div><a href="#pair-gap" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">gap</a></div>
  <div><a href="#pair-geom1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">geom1</a></div>
  <div><a href="#pair-geom2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">geom2</a></div>
  <div><a href="#pair-margin" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">margin</a></div>
  <div><a href="#pair-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#pair-solref" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solref</a></div>
  <div><a href="#pair-solreffriction" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solreffriction</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#tendon" style="text-decoration: none; color: inherit;">tendon</a></summary>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#fixed" style="text-decoration: none; color: inherit;">fixed</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#fixed-class" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">class</a></div>
  <div><a href="#fixed-damping" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">damping</a></div>
  <div><a href="#fixed-frictionloss" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">frictionloss</a></div>
  <div><a href="#fixed-group" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">group</a></div>
  <div><a href="#fixed-limited" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">limited</a></div>
  <div><a href="#fixed-margin" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">margin</a></div>
  <div><a href="#fixed-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#fixed-range" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">range</a></div>
  <div><a href="#fixed-rgba" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">rgba</a></div>
  <div><a href="#fixed-solimpfriction" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solimpfriction</a></div>
  <div><a href="#fixed-solimplimit" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solimplimit</a></div>
  <div><a href="#fixed-solreffriction" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solreffriction</a></div>
  <div><a href="#fixed-solreflimit" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">solreflimit</a></div>
  <div><a href="#fixed-springlength" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">springlength</a></div>
  <div><a href="#fixed-stiffness" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">stiffness</a></div>
  <div><a href="#fixed-width" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">width</a></div>
</div>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#joint" style="text-decoration: none; color: inherit;">joint</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#joint-coef" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">coef</a></div>
  <div><a href="#joint-joint" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#custom" style="text-decoration: none; color: inherit;">custom</a></summary>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#numeric" style="text-decoration: none; color: inherit;">numeric</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#numeric-data" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">data</a></div>
  <div><a href="#numeric-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#numeric-size" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">size</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#text" style="text-decoration: none; color: inherit;">text</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#text-data" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">data</a></div>
  <div><a href="#text-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#sensor" style="text-decoration: none; color: inherit;">sensor</a></summary>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#touch" style="text-decoration: none; color: inherit;">touch</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#touch-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#touch-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#touch-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#touch-site" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">site</a></div>
  <div><a href="#touch-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#accelerometer" style="text-decoration: none; color: inherit;">accelerometer</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#accelerometer-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#accelerometer-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#accelerometer-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#accelerometer-site" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">site</a></div>
  <div><a href="#accelerometer-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#velocimeter" style="text-decoration: none; color: inherit;">velocimeter</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#velocimeter-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#velocimeter-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#velocimeter-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#velocimeter-site" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">site</a></div>
  <div><a href="#velocimeter-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#gyro" style="text-decoration: none; color: inherit;">gyro</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#gyro-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#gyro-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#gyro-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#gyro-site" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">site</a></div>
  <div><a href="#gyro-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#jointpos" style="text-decoration: none; color: inherit;">jointpos</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#jointpos-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#jointpos-joint" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint</a></div>
  <div><a href="#jointpos-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#jointpos-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#jointpos-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#jointvel" style="text-decoration: none; color: inherit;">jointvel</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#jointvel-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#jointvel-joint" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">joint</a></div>
  <div><a href="#jointvel-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#jointvel-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#jointvel-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#framepos" style="text-decoration: none; color: inherit;">framepos</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#framepos-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#framepos-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#framepos-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#framepos-objname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objname</a></div>
  <div><a href="#framepos-objtype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objtype</a></div>
  <div><a href="#framepos-refname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">refname</a></div>
  <div><a href="#framepos-reftype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">reftype</a></div>
  <div><a href="#framepos-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#framequat" style="text-decoration: none; color: inherit;">framequat</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#framequat-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#framequat-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#framequat-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#framequat-objname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objname</a></div>
  <div><a href="#framequat-objtype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objtype</a></div>
  <div><a href="#framequat-refname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">refname</a></div>
  <div><a href="#framequat-reftype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">reftype</a></div>
  <div><a href="#framequat-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#framexaxis" style="text-decoration: none; color: inherit;">framexaxis</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#framexaxis-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#framexaxis-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#framexaxis-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#framexaxis-objname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objname</a></div>
  <div><a href="#framexaxis-objtype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objtype</a></div>
  <div><a href="#framexaxis-refname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">refname</a></div>
  <div><a href="#framexaxis-reftype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">reftype</a></div>
  <div><a href="#framexaxis-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#frameyaxis" style="text-decoration: none; color: inherit;">frameyaxis</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#frameyaxis-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#frameyaxis-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#frameyaxis-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#frameyaxis-objname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objname</a></div>
  <div><a href="#frameyaxis-objtype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objtype</a></div>
  <div><a href="#frameyaxis-refname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">refname</a></div>
  <div><a href="#frameyaxis-reftype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">reftype</a></div>
  <div><a href="#frameyaxis-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#framezaxis" style="text-decoration: none; color: inherit;">framezaxis</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#framezaxis-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#framezaxis-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#framezaxis-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#framezaxis-objname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objname</a></div>
  <div><a href="#framezaxis-objtype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objtype</a></div>
  <div><a href="#framezaxis-refname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">refname</a></div>
  <div><a href="#framezaxis-reftype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">reftype</a></div>
  <div><a href="#framezaxis-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#framelinvel" style="text-decoration: none; color: inherit;">framelinvel</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#framelinvel-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#framelinvel-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#framelinvel-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#framelinvel-objname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objname</a></div>
  <div><a href="#framelinvel-objtype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objtype</a></div>
  <div><a href="#framelinvel-refname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">refname</a></div>
  <div><a href="#framelinvel-reftype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">reftype</a></div>
  <div><a href="#framelinvel-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#frameangvel" style="text-decoration: none; color: inherit;">frameangvel</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#frameangvel-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#frameangvel-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#frameangvel-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#frameangvel-objname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objname</a></div>
  <div><a href="#frameangvel-objtype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">objtype</a></div>
  <div><a href="#frameangvel-refname" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">refname</a></div>
  <div><a href="#frameangvel-reftype" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">reftype</a></div>
  <div><a href="#frameangvel-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#subtreecom" style="text-decoration: none; color: inherit;">subtreecom</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#subtreecom-body" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body</a></div>
  <div><a href="#subtreecom-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#subtreecom-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#subtreecom-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#subtreecom-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#subtreelinvel" style="text-decoration: none; color: inherit;">subtreelinvel</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#subtreelinvel-body" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body</a></div>
  <div><a href="#subtreelinvel-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#subtreelinvel-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#subtreelinvel-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#subtreelinvel-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#subtreeangmom" style="text-decoration: none; color: inherit;">subtreeangmom</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#subtreeangmom-body" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body</a></div>
  <div><a href="#subtreeangmom-cutoff" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">cutoff</a></div>
  <div><a href="#subtreeangmom-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#subtreeangmom-noise" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">noise</a></div>
  <div><a href="#subtreeangmom-user" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">user</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#contact" style="text-decoration: none; color: inherit;">contact</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#contact-body1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body1</a></div>
  <div><a href="#contact-body2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">body2</a></div>
  <div><a href="#contact-data" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">data</a></div>
  <div><a href="#contact-geom1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">geom1</a></div>
  <div><a href="#contact-geom2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">geom2</a></div>
  <div><a href="#contact-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#contact-num" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">num</a></div>
  <div><a href="#contact-reduce" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">reduce</a></div>
  <div><a href="#contact-site" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">site</a></div>
  <div><a href="#contact-subtree1" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">subtree1</a></div>
  <div><a href="#contact-subtree2" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">subtree2</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#statistic" style="text-decoration: none; color: inherit;">statistic</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#statistic-center" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">center</a></div>
  <div><a href="#statistic-extent" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">extent</a></div>
</div>
</details>
</div>
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#keyframe" style="text-decoration: none; color: inherit;">keyframe</a></summary>
<div style="margin-top: 4px;">
<div style="margin-bottom: 6px; margin-left: 16px; border-left: 2px solid rgba(127, 127, 127, 0.3); padding-left: 12px;">
<details>
<summary style="padding: 8px 12px; background-color: rgba(127, 127, 127, 0.08); border-radius: 6px; cursor: pointer; font-weight: 600; font-family: monospace; transition: background-color 0.2s;"><a href="#key" style="text-decoration: none; color: inherit;">key</a></summary>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; padding: 8px 12px; margin: 4px 0;">
  <div><a href="#key-ctrl" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">ctrl</a></div>
  <div><a href="#key-name" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">name</a></div>
  <div><a href="#key-qpos" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">qpos</a></div>
  <div><a href="#key-qvel" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">qvel</a></div>
  <div><a href="#key-time" style="text-decoration: none; font-size: 0.95em; opacity: 0.85;">time</a></div>
</div>
</details>
</div>
</div>
</details>
</div>
</div>
</details>
</div>
</div>

---

(mujoco)=

## `mujoco`

Top-level MJCF element.

**Attributes:**

(mujoco-model)=

-   **`model`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Model name.

**Child Elements**: [`extension`](#extension), [`compiler`](#compiler), [`asset`](#asset), [`default`](#default), [`(world)body`](<#(world)body>), [`option`](#option), [`actuator`](#actuator), [`visual`](#visual), [`equality`](#equality), [`contact`](#contact), [`tendon`](#tendon), [`custom`](#custom), [`sensor`](#sensor), [`statistic`](#statistic), [`keyframe`](#keyframe)

---

(extension)=

### `extension`

This element is used to declare plugins and their instances.

**Parent Elements**: [`mujoco`](#mujoco)

**Child Elements**: [`plugin`](#plugin)

---

(plugin)=

#### `plugin`

A plugin declaration.

**Attributes:**

(plugin-plugin)=

-   **`plugin`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    Name of the plugin.

**Parent Elements**: [`extension`](#extension)

**Child Elements**: [`instance`](#instance)

---

(instance)=

##### `instance`

An instance of a plugin.

**Attributes:**

(instance-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    Name of the plugin instance.

**Parent Elements**: [`plugin`](#plugin)

**Child Elements**: [`config`](#config)

---

(config)=

###### `config`

A configuration key-value pair for a plugin instance.

**Attributes:**

(config-key)=

-   **`key`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    Key of the configuration.

(config-value)=

-   **`value`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    Value of the configuration.

**Parent Elements**: [`instance`](#instance)

---

(compiler)=

### `compiler`

This element is used to set options for the built-in parser and
compiler. After parsing and compilation it no longer has any effect. The
settings here are global and apply to the entire model.

**Attributes:**

(compiler-angle)=

-   **`angle`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `degree` ]

    **Choice:** [ `radian` | `degree` ]

    This attribute specifies whether the angles in the MJCF model are
    expressed in units of degrees or radians. The compiler converts degrees
    into radians internally. For URDF models the parser sets this attribute
    to \"radian\" internally, regardless of the XML setting.

(compiler-eulerseq)=

-   **`eulerseq`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `xyz` ]

    **Choice:** [ `zyx` | `zxy` | `yxz` | `yzx` | `xyz` | `xzy` ]

    This attribute specifies the sequence of Euler rotations for all
    euler attributes of elements that have spatial frames. This must be a
    string with exactly 3 characters from the set {x, y, z, X, Y, Z}. The
    character at position n determines the axis around which the n-th
    rotation is performed. Lower case letters denote axes that rotate with
    the frame (intrinsic), while upper case letters denote axes that remain
    fixed in the parent frame (extrinsic). The \"rpy\" convention used in
    URDF corresponds to \"XYZ\" in MJCF.

(compiler-meshdir)=

-   **`meshdir`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    This attribute instructs the compiler where to look for mesh and height
    field files. The full path to a file is determined as follows. If the
    strippath attribute is \"true\", all path information from the file name
    is removed. The following checks are then applied in order: (1) if the
    file name contains an absolute path, it is used without further changes;
    (2) if this attribute is set and contains an absolute path, the full
    path is the string given here appended with the file name; (3) the full
    path is the path to the main MJCF model file, appended with the value
    of this attribute if specified, appended with the file name.

(compiler-assetdir)=

-   **`assetdir`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    This attribute sets the values of both meshdir and texturedir. Values
    in the latter attributes take precedence over assetdir.

(compiler-texturedir)=

-   **`texturedir`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    This attribute is used to instruct the compiler where to look for
    texture files. It works in the same way as meshdir.

(compiler-autolimits)=

-   **`autolimits`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `true` ]

    This attribute affects the behavior of attributes such as \"limited\" (on
    body-joint or tendon), \"forcelimited\", \"ctrllimited\", and \"actlimited\"
    (on actuator). If \"true\", these attributes are unnecessary and their
    value will be inferred from the presence of their corresponding \"range\"
    attribute. If \"false\", no such inference will happen: for a joint to be
    limited, both limited=\"true\" and range=\"min max\" must be specified. In
    this mode, it is an error to specify a range without a limit.

(compiler-fitaabb)=

-   **`fitaabb`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `false` ]

    The compiler is able to replace a mesh with a geometric primitive fitted
    to that mesh. If this attribute is \"true\", the fitting procedure uses the
    axis-aligned bounding box (AABB) of the mesh, choosing the smallest
    primitive whose AABB contains the mesh AABB. Otherwise it uses the
    equivalent-inertia box of the mesh. The type of geometric primitive used
    for fitting is specified separately for each geom.

**Parent Elements**: [`mujoco`](#mujoco)

---

(asset)=

### `asset`

This is a grouping element for defining assets. It does not have
attributes. Assets are created in the model so that they can be
referenced from other model elements. Assets opened from a file can
be identified in two different ways: filename extensions or the
`content_type` attribute. The parser will attempt to open a file
specified by the content type provided, and only defaults to the
filename extension if no `content_type` attribute is specified. The
content type is ignored if the asset is not loaded from a file.

**Parent Elements**: [`mujoco`](#mujoco)

**Child Elements**: [`material`](#material), [`mesh`](#mesh), [`texture`](#texture), [`hfield`](#hfield), [`model`](#model)

---

(material)=

#### `material`

This element creates a material asset. It can be referenced from
skins, geoms, sites and tendons to set their appearance. Note that
all these elements also have a local rgba attribute, which is more
convenient when only colors need to be adjusted, because it does not
require creating materials and referencing them. Materials are useful
for adjusting appearance properties beyond color. However once a
material is created, it is more natural to specify the color using
the material, so that all appearance properties are grouped together.

**Attributes:**

(material-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the material, used for referencing.

(material-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

(material-rgba)=

-   **`rgba`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `1. 1. 1. 1.` ]

    Color and transparency of the material. All components should be in the
    range [0 1]. Note that the texture color (if assigned) and the color
    specified here are multiplied component-wise. Thus the default value of
    \"1 1 1 1\" has the effect of leaving the texture unchanged. When the
    material is applied to a model element which defines its own local rgba
    attribute, the local definition has precedence. The remaining material
    properties always apply.

(material-texture)=

-   **`texture`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If this attribute is specified, the material has a texture associated
    with it. Referencing the material from a model element will cause the
    texture to be applied to that element. The value of this attribute is
    the name of a texture asset, not a texture file name. Textures cannot
    be loaded in the material definition; instead they must be loaded
    explicitly via the texture element and then referenced here. The
    texture referenced here is used for specifying the RGB values. For
    advanced rendering (e.g., Physics-Based Rendering), more texture types
    need to be specified. In that case, this texture attribute should be
    omitted, and the texture types should be specified using layer child
    elements. Note that the built-in renderer does not support PBR
    properties, so these advanced rendering features are only available
    when using an external renderer.

(material-texuniform)=

-   **`texuniform`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `false` ]

    For cube textures, this attribute controls how cube mapping is applied.
    The value \"false\" means apply cube mapping directly, using the actual
    size of the object. The value \"true\" maps the texture to a unit object
    before scaling it to its actual size. For 2d textures, this attribute
    interacts with texrepeat: when \"false\", the 2d texture is repeated N
    times over the object; when \"true\", the texture is repeated N times
    over one spatial unit, regardless of object size.

(material-texrepeat)=

-   **`texrepeat`** [ <span class="badge array">real(2)</span> | <span class="badge required">Required</span> | **Default:** `1. 1.` ]

    This attribute applies to textures of type \"2d\". It specifies how many
    times the texture image is repeated, relative to either the object size
    or the spatial unit, as determined by the texuniform attribute.

(material-reflectance)=

-   **`reflectance`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    This attribute should be in the range [0 1]. If the value is greater
    than 0, and the material is applied to a plane or a box geom, the
    renderer will simulate reflectance. The larger the value, the stronger
    the reflectance. For boxes, only the face in the direction of the local
    +Z axis is reflective. Simulating reflectance properly requires
    ray-tracing. Only the first reflective geom in the model is rendered
    as such.

(material-metallic)=

-   **`metallic`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    This attribute corresponds to uniform metallicity coefficient applied to
    the entire material. This attribute is only used by physically-based
    renderers and has no effect in Phong-based rendering. If a non-negative
    value is specified, this metallic value should be multiplied by the
    metallic texture sampled value to obtain the final metallicity of the material.

(material-roughness)=

-   **`roughness`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    This attribute corresponds to uniform roughness coefficient applied to
    the entire material. This attribute is only used by physically-based
    renderers and has no effect in Phong-based rendering. If a non-negative
    value is specified, this roughness value should be multiplied by the
    roughness texture sampled value to obtain the final roughness of the material.

(material-emission)=

-   **`emission`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `0. 0. 0. 0.` ]

    Emission in OpenGL has the RGBA format, however we only provide a scalar
    setting. The RGB components of the OpenGL emission vector are the RGB
    components of the material color multiplied by the value specified here.
    The alpha component is 1.

<div class="motphys-extension-block">
<div class="motphys-extension-label">MPEX</div>

(material-emissionintensity)=

-   **`emissionintensity`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Emission intensity multiplier applied on top of the emission color.

(material-detailpara)=

-   **`detailpara`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `1. 1. 1. 1.` ]

    Detail normal map parameters packed as four
    floats: x = detail normal map u scale, y = detail normal map v scale,
    z = normal strength, w = padding.

(material-depthbias)=

-   **`depthbias`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Depth bias for rendering.

</div>

**Parent Elements**: [`asset`](#asset), [`default`](#default)

**Child Elements**: `layer`

---

(mesh)=

#### `mesh`

This element creates a mesh asset, which can then be referenced from geoms.
If the referencing geom type is \"mesh\" the mesh is instantiated in the
model, otherwise a geometric primitive is automatically fitted to it.

The parser works with triangulated meshes. They can be loaded from binary
STL files, OBJ files or MSH files with a custom format, or vertex and face
data can be specified directly in the XML. While any collection of triangles
can be loaded as a mesh and rendered, collision detection works with the
convex hull of the mesh. The mesh appearance (including texture mapping) is
controlled by the material and rgba attributes of the referencing geom.

Meshes can have explicit texture coordinates instead of relying on the
automated texture mapping mechanism. When provided, these explicit
coordinates have priority. Texture coordinates can be specified with OBJ
files and MSH files, as well as explicitly in the XML with the texcoord
attribute, but not via STL files.

The size of the mesh is determined by the 3D coordinates of the vertex data
multiplied by the components of the scale attribute. Scaling is applied
separately for each coordinate axis. Negative scaling values can be used to
flip the mesh. The compiler pre-processes the mesh so that it is centered
around (0,0,0) and its principal axes of inertia are the coordinate axes,
saving the translation and rotation offsets for subsequent geom-related
computations.

```{note}
Vertex data in source assets is often relative to coordinate frames whose
 origin is not inside the mesh. This is resolved by centering the mesh at
 compile time. The translation and rotation offsets are saved for use when
 re-applying the transform. Positioning and orienting is done by the
 referencing geom, while sizing (scale) is done by the mesh asset itself.
```

**Attributes:**

(mesh-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `-` ]

    Name of the mesh, used for referencing. If omitted, the mesh name equals
    the file name without the path and extension.

(mesh-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes (only scale in this case).

(mesh-file)=

-   **`file`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    The file from which the mesh will be loaded. The path is determined as
    described in the meshdir attribute of the compiler element. The file
    extension must be \"stl\", \"msh\", or \"obj\" (not case sensitive) specifying
    the file type. If the file name is omitted, the vertex attribute becomes
    required.

(mesh-scale)=

-   **`scale`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    This attribute specifies the scaling that will be applied to the vertex
    data along each coordinate axis. Negative values are allowed, resulting
    in flipping the mesh along the corresponding axis.

(mesh-vertex)=

-   **`vertex`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Vertex 3D position data. You can specify position data in the XML using
    this attribute, or using a binary file, but not both.

(mesh-texcoord)=

-   **`texcoord`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Vertex 2D texture coordinates, which are numbers between 0 and 1. If
    specified, the number of texture coordinate pairs must equal the number
    of vertices.

(mesh-normal)=

-   **`normal`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Vertex 3D normal data. If specified, the number of normals must equal
    the number of vertices. The model compiler normalizes the normals
    automatically.

(mesh-face)=

-   **`face`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Faces of the mesh. Each face is a sequence of 3 vertex indices, in
    counter-clockwise order. The indices must be integers between 0 and
    nvert-1.

(mesh-refpos)=

-   **`refpos`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Reference position relative to which the 3D vertex coordinates are
    defined. This vector is subtracted from the positions.

(mesh-refquat)=

-   **`refquat`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Reference orientation relative to which the 3D vertex coordinates and
    normals are defined. The conjugate of this quaternion is used to rotate
    the positions and normals. The model compiler normalizes the quaternion
    automatically.

**Parent Elements**: [`asset`](#asset), [`default`](#default)

---

(texture)=

#### `texture`

This element creates a texture asset, which is then referenced from a
material asset, which is finally referenced from a model element that
needs to be textured.

The texture data can be loaded from files or can be generated by the
compiler as a procedural texture. Because different texture types require
different parameters, only a subset of the attributes below are used for
any given texture. Currently, three file formats are supported for loading
textures: PNG, KTX, and a custom MSH texture format. The loader will
use the extension of the file name to determine which format to use,
defaulting to the custom format if the extension is not recognized.

```{note}
As with all other assets, a texture must have a name in order to be
 referenced. However if the texture is loaded from a single file with the
 file attribute, the explicit name can be omitted and the file name (without
 the path and extension) becomes the texture name. If the name after parsing
 is empty and the texture type is not \"skybox\", the compiler will generate
 an error.
```

**Attributes:**

(texture-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the texture, used for referencing. If omitted, the texture name
    equals the file name without the path and extension.

(texture-file)=

-   **`file`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If this attribute is specified, and the builtin attribute is set to
    \"none\", the texture data is loaded from a single file. See the
    texturedir attribute of the compiler element regarding the file path.

(texture-builtin)=

-   **`builtin`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `none` ]

    **Choice:** [ `none` | `gradient` | `checker` | `flat` ]

    Controls the generation of procedural textures. If the value is
    different from \"none\", the texture is treated as procedural and any file
    names are ignored.

(texture-type)=

-   **`type`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `cube` ]

    **Choice:** [ `cube` | `2d` | `skybox` | `envdiff` | `envspec` | `probe` ]

    This attribute determines how the texture is represented and mapped to
    objects. It also determines which of the remaining attributes are
    relevant.

(texture-rgb1)=

-   **`rgb1`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.8 0.8 0.8` ]

    The first color used for procedural texture generation. This color is
    also used to fill missing sides of cube and skybox textures loaded from
    files. The components should be in the range [0 1].

(texture-rgb2)=

-   **`rgb2`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.5 0.5 0.5` ]

    The second color used for procedural texture generation.

(texture-width)=

-   **`width`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The width of a procedural texture, i.e., the number of columns in the
    image. Larger values usually result in higher quality images. For
    textures loaded from files, this attribute is ignored.

(texture-height)=

-   **`height`** [ <span class="badge real">real</span> | <span class="badge optional">Optional</span> ]

    The height of the procedural texture, i.e., the number of rows in the
    image. For cube and skybox textures, this attribute is ignored and the
    height is set to 6 times the width. For textures loaded from files, this
    attribute is ignored.

(texture-colorspace)=

-   **`colorspace`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    **Choice:** [ `sRGB` | `linear` ]

    This attribute determines the color space of the texture. When set,
    overrides the color space information embedded in the image file.

(texture-mark)=

-   **`mark`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    **Choice:** [ `none` | `edge` | `cross` | `random` ]

    Procedural textures can be marked with the markrgb color, on top of the
    colors determined by the builtin type. \"edge\" means that the edges of
    all texture images are marked. \"cross\" means that a cross is marked in
    the middle of each image. \"random\" means that randomly chosen pixels are
    marked. All markings are one-pixel wide.

(texture-markrgb)=

-   **`markrgb`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    The color used for procedural texture markings.

(texture-gridsize)=

-   **`gridsize`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    -

(texture-gridlayout)=

-   **`gridlayout`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    -

**Parent Elements**: [`asset`](#asset)

---

(hfield)=

#### `hfield`

This element creates a height field asset, which can then be referenced
from geoms with type \"hfield\". A height field, also known as a terrain map,
is a 2D matrix of elevation data. The data can be specified by loading from
a PNG file (where pixel intensity maps to elevation), loading from a binary
file in a custom format, or by providing inline elevation data via the
elevation attribute.

Regardless of which method is used to specify the elevation data, the
compiler always normalizes it to the range [0 1].

The position and orientation of the height field is determined by the geom
that references it. The spatial extent is specified by the height field
asset itself via the size attribute, and cannot be modified by the
referencing geom (the geom size parameters are ignored in this case).

```{note}
For collision detection, a height field is treated as a union of triangular
 prisms. The number of possible contacts between a height field and a geom
 is limited to 50; any contacts beyond that are discarded. To avoid
 penetration due to discarded contacts, the spatial features of the height
 field should be large compared to the geoms it collides with. Collisions
 between height fields and other height fields or planes are not supported.
```

**Attributes:**

(hfield-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the height field, used for referencing. If the name is omitted
    and a file name is specified, the height field name equals the file name
    without the path and extension.

(hfield-content_type)=

-   **`content_type`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If the file attribute is specified, this sets the Media Type (formerly
    known as MIME type) of the file to be loaded. Any filename extensions
    will be overloaded. Currently \"image/png\" and
    \"image/vnd.mujoco.hfield\" are supported.

(hfield-file)=

-   **`file`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If this attribute is specified, the elevation data is loaded from the
    given file. If the file extension is \".png\" (not case-sensitive), the
    file is treated as a PNG file. Otherwise it is treated as a binary file
    in the custom format. The number of rows and columns in the data are
    determined from the file contents. Loading data from a file and setting
    nrow or ncol to non-zero values results in a compile error.

(hfield-nrow)=

-   **`nrow`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Specifies the number of rows in the elevation data matrix. A value of 0 means
    that the data will be loaded from a file, which will be used to infer
    the size of the matrix.

(hfield-ncol)=

-   **`ncol`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    This attribute specifies the number of columns in the elevation data
    matrix.

(hfield-elevation)=

-   **`elevation`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    This attribute specifies the elevation data matrix. Values are
    automatically normalized to lie between 0 and 1 by first subtracting
    the minimum value and then dividing by the (maximum-minimum) difference.
    If not provided, values are set to 0. Note that the row order in the model
    is flipped with respect to the order in XML, i.e., it is bottom-to-top.

(hfield-size)=

-   **`size`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    The four numbers here are (radius_x, radius_y, elevation_z, base_z).
    The height field is centered at the referencing geom's local frame.
    Elevation is in the +Z direction. The first two numbers specify the X
    and Y extent (or \"radius\") of the rectangle over which the height field
    is defined. The third number is the maximum elevation; it scales the
    elevation data which is normalized to [0-1], so the minimum elevation
    is at Z=0 and the maximum is at Z=elevation_z. The last number is the
    depth of a box in the -Z direction serving as a \"base\" for the height
    field, ensuring non-zero thickness at places where the normalized
    elevation data is zero.

**Parent Elements**: [`asset`](#asset)

---

(model)=

#### `model`

This element specifies other MJCF models which may be used for attachment
in the current model.

**Attributes:**

(model-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sub-model, used for referencing in attach. If unspecified,
    the model name from the sub-model's root element is used.

(model-file)=

-   **`file`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The file from which the sub-model will be loaded. The sub-model must be
    a valid MJCF model.

**Parent Elements**: [`asset`](#asset)

---

(default)=

### `default`

This element is used to define default settings for various model elements.
For each `Option` field, generate a `apply_default` method to merge with default class
You should compile this struct into `DefaultMap` which is input of `apply_default`

**Attributes:**

(default-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the default class.

**Parent Elements**: [`default`](#default), [`mujoco`](#mujoco)

**Child Elements**: [`default`](#default), [`geom`](#geom), [`joint`](#joint), [`light`](#light), [`mesh`](#mesh), [`material`](#material), [`general`](#general), [`motor`](#motor), [`position`](#position), [`velocity`](#velocity), [`adhesion`](#adhesion), [`camera`](#camera), [`site`](#site), [`tendon`](#tendon), [`equality`](#equality)

#### `adhesion`

→ See [`adhesion`](#adhesion) for the full documentation.

#### `camera`

→ See [`camera`](#camera) for the full documentation.

#### `equality`

→ See [`equality`](#equality) for the full documentation.

#### `general`

→ See [`general`](#general) for the full documentation.

#### `geom`

→ See [`geom`](#geom) for the full documentation.

#### `joint`

→ See [`joint`](#joint) for the full documentation.

#### `light`

→ See [`light`](#light) for the full documentation.

#### `material`

→ See [`material`](#material) for the full documentation.

#### `mesh`

→ See [`mesh`](#mesh) for the full documentation.

#### `motor`

→ See [`motor`](#motor) for the full documentation.

#### `position`

→ See [`position`](#position) for the full documentation.

#### `site`

→ See [`site`](#site) for the full documentation.

#### `tendon`

→ See [`tendon`](#tendon) for the full documentation.

#### `velocity`

→ See [`velocity`](#velocity) for the full documentation.

---

((world)body)=

### `(world)body`

This element is used to construct the kinematic tree via nesting. The element worldbody is used
for the top-level body, while the element body is used for all other bodies.

Bodies form the nodes of the kinematic tree. Each body can have child bodies, joints, geoms,
sites, cameras, and lights. The inertial properties of a body can be specified explicitly via
the inertial child element, or inferred automatically from the geoms attached to the body.

**Attributes:**

(worldbody-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the body.

(worldbody-childclass)=

-   **`childclass`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If this attribute is present, all descendant elements that admit a defaults class will use
    the class specified here, unless they specify their own class or another body or frame with
    a childclass attribute is encountered along the chain of nested bodies and frames.

(worldbody-pos)=

-   **`pos`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    The 3D position of the body frame, in the parent coordinate frame. If undefined it defaults
    to (0,0,0).

(worldbody-quat)=

-   **`quat`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the body frame as unit quaternion.
    → See [rotation representation](#rotation-attrs-quat).

(worldbody-euler)=

-   **`euler`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the body frame as Euler angles.
    → See [rotation representation](#rotation-attrs-euler).

(worldbody-axisangle)=

-   **`axisangle`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the body frame as an axis-angle pair.
    → See [rotation representation](#rotation-attrs-axisangle).

(worldbody-xyaxes)=

-   **`xyaxes`** [ <span class="badge array">real(6)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the body frame via X and Y axes.
    → See [rotation representation](#rotation-attrs-xyaxes).

(worldbody-zaxis)=

-   **`zaxis`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the body frame via Z axis direction.
    → See [rotation representation](#rotation-attrs-zaxis).

(worldbody-mocap)=

-   **`mocap`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `false` ]

    If this attribute is \"true\", the body is labeled as a mocap body. This is allowed only for
    bodies that are children of the world body and have no joints. Such bodies are fixed from
    the viewpoint of the dynamics, but nevertheless the forward kinematics set their position
    and orientation via the mocap system at each time step. This mechanism
    can be used to stream motion capture data into the simulation. Mocap bodies can also be
    moved via mouse perturbations in the interactive visualizer, even in dynamic simulation
    mode, which can be useful for creating props with adjustable position and orientation.

(worldbody-gravcomp)=

-   **`gravcomp`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Gravity compensation force, specified as fraction of body weight. This attribute creates an
    upwards force applied to the body's center of mass, countering the force of gravity. A
    value of 1 creates an upward force equal to the body's weight and compensates for gravity
    exactly. Values greater than 1 will create a net upwards force or buoyancy effect.

**Parent Elements**: [`(world)body`](<#(world)body>), [`mujoco`](#mujoco)

**Child Elements**: [`inertial`](#inertial), [`joint`](#joint), [`freejoint`](#freejoint), [`(world)body`](<#(world)body>), [`attach`](#attach), [`camera`](#camera), [`frame`](#frame), [`geom`](#geom), [`light`](#light), [`replicate`](#replicate), [`site`](#site)

---

(inertial)=

#### `inertial`

This element specifies the mass and inertial properties of the body. If this element is not
included in a given body, the inertial properties are inferred from the geoms attached to the
body. When a compiled MJCF model is saved, the XML writer saves the inertial properties
explicitly using this element, even if they were inferred from geoms. The inertial frame is
such that its center coincides with the center of mass of the body, and its axes coincide with
the principal axes of inertia of the body. Thus the inertia matrix is diagonal in this frame.

```{note}
The presence of the `inertial` element itself disables the automatic inertia inference
 mechanism from geoms. Even when inertial properties could be inferred from geoms, `pos` is
 required whenever this element is present.
```

**Attributes:**

(inertial-pos)=

-   **`pos`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    Position of the inertial frame. This attribute is required even when the inertial
    properties can be inferred from geoms. This is because the presence of the inertial
    element itself disables the automatic inference mechanism.

(inertial-quat)=

-   **`quat`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the inertial frame as unit quaternion.
    → See [rotation representation](#rotation-attrs-quat).

(inertial-euler)=

-   **`euler`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the inertial frame as Euler angles.
    → See [rotation representation](#rotation-attrs-euler).

(inertial-axisangle)=

-   **`axisangle`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the inertial frame as an axis-angle pair.
    → See [rotation representation](#rotation-attrs-axisangle).

(inertial-xyaxes)=

-   **`xyaxes`** [ <span class="badge array">real(6)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the inertial frame via X and Y axes.
    → See [rotation representation](#rotation-attrs-xyaxes).

(inertial-zaxis)=

-   **`zaxis`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the inertial frame via Z axis direction.
    → See [rotation representation](#rotation-attrs-zaxis).

(inertial-mass)=

-   **`mass`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Mass of the body. Negative values are not allowed. The inertia matrix in generalized
    coordinates must be positive-definite, which can sometimes be achieved even if some bodies
    have zero mass. In general however there is no reason to use massless bodies.

(inertial-diaginertia)=

-   **`diaginertia`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Diagonal inertia matrix, expressing the body inertia relative to the inertial frame. If
    this attribute is omitted, the `fullinertia` attribute becomes required.

(inertial-fullinertia)=

-   **`fullinertia`** [ <span class="badge array">real(6)</span> | <span class="badge optional">Optional</span> ]

    Full inertia matrix M. Since M is 3-by-3 and symmetric, it is specified using only 6
    numbers in the following order: M(1,1), M(2,2), M(3,3), M(1,2), M(1,3), M(2,3). The
    compiler computes the eigenvalue decomposition of M and sets the frame orientation and
    diagonal inertia accordingly. If non-positive eigenvalues are encountered (i.e., if M is
    not positive definite) a compile error is generated.

**Parent Elements**: [`(world)body`](<#(world)body>)

---

(joint-body-joint)=

#### `joint`

This element creates a joint. A joint creates motion degrees of freedom between the body where
it is defined and the body's parent. If multiple joints are defined in the same body, the
corresponding spatial transformations (of the body frame relative to the parent frame) are
applied in order. If no joints are defined, the body is welded to its parent. Joints cannot be
defined in the world body. At runtime the positions and orientations of all joints defined in
the model are stored in the DOF positions array, in the order in which they appear in the
kinematic tree. The linear and angular velocities are stored in the DOF velocities array. These
two vectors have different dimensionality when free or ball joints are used, because such joints
represent rotations as unit quaternions.

```{note}
Free joints do not have a position within the body frame and cannot have limits. Ball joints
 cannot be combined with other rotational joints in the same body. The axis attribute is ignored
 for free and ball joints.
```

**Attributes:**

(joint-body-joint-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the joint.

(joint-body-joint-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

(joint-body-joint-group)=

-   **`group`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    -

(joint-body-joint-type)=

-   **`type`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `hinge` ]

    **Choice:** [ `free` | `ball` | `slide` | `hinge` ]

    Type of the joint. The keywords have the following meaning: the free type creates a free
    \"joint\" with three translational and three rotational degrees of freedom making the body
    floating; the ball type creates a ball joint with three rotational degrees of freedom; the
    slide type creates a sliding or prismatic joint with one translational degree of freedom;
    the hinge type creates a hinge joint with one rotational degree of freedom.

(joint-body-joint-axis)=

-   **`axis`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 1.0` ]

    This attribute specifies the axis of rotation for hinge joints and the direction of
    translation for slide joints. It is ignored for free and ball joints. The vector specified
    here is automatically normalized to unit length as long as its length is greater than
    10E-14; otherwise a compile error is generated.

(joint-body-joint-pos)=

-   **`pos`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 0.0` ]

    Position of the joint, specified in the frame of the body where the joint is defined. For
    free joints this attribute is ignored.

(joint-body-joint-ref)=

-   **`ref`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The reference position or angle of the joint. This attribute is only used for slide and
    hinge joints. It defines the joint value corresponding to the initial model configuration.
    Note that the initial configuration itself is unmodified, only the value of the joint at
    this configuration. The amount of spatial transformation that the joint applies at runtime
    equals the current joint value stored in the DOF positions minus this reference value.

(joint-body-joint-margin)=

-   **`margin`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The distance threshold below which limits become active. The constraint solver normally
    generates forces as soon as a constraint becomes active, even if the margin parameter makes
    that happen at a distance. This attribute together with solreflimit and solimplimit can be
    used to model a soft joint limit.

(joint-body-joint-range)=

-   **`range`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    The joint limits. Limits can be imposed on all joint types except for free joints. For
    hinge and ball joints, the range is specified in degrees or radians depending on the angle
    attribute of the compiler element. For ball joints, the limit is imposed on the angle of
    rotation (relative to the reference configuration) regardless of the axis of rotation. Only
    the second range parameter is used for ball joints; the first range parameter should be set
    to 0. Setting this attribute without specifying limited is an error if autolimits is
    \"false\" in the compiler element.

(joint-body-joint-limited)=

-   **`limited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    This attribute specifies if the joint has limits. It interacts with the range attribute. If
    this attribute is \"false\", joint limits are disabled. If this attribute is \"true\", joint
    limits are enabled. If this attribute is \"auto\", and autolimits is set in the compiler
    element, joint limits will be enabled if range is defined.

(joint-body-joint-actuatorfrcrange)=

-   **`actuatorfrcrange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping total actuator forces acting on this joint. It is available only for
    scalar joints (hinge and slider) and ignored for ball and free joints. The compiler expects
    the first value to be smaller than the second value. Setting this attribute without
    specifying actuatorfrclimited is an error if compiler-autolimits is \"false\".

(joint-body-joint-actuatorfrclimited)=

-   **`actuatorfrclimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    This attribute specifies whether actuator forces acting on the joint should be clamped. It
    is available only for scalar joints (hinge and slider) and ignored for ball and free
    joints. This attribute interacts with the actuatorfrcrange attribute. If this attribute
    is \"false\", actuator force clamping is disabled. If it is \"true\", actuator force
    clamping is enabled. If this attribute is \"auto\", and autolimits is set in the compiler
    element, actuator force clamping will be enabled if actuatorfrcrange is defined.

(joint-body-joint-springdamper)=

-   **`springdamper`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    When both numbers are positive, the compiler will override any stiffness and damping values
    specified with the attributes below, and will instead set them automatically so that the
    resulting mass-spring-damper for this joint has the desired time constant (first value) and
    damping ratio (second value). This is done by taking into account the joint inertia in the
    model reference configuration. Note that the format is the same as the solref parameter of
    the constraint solver.

(joint-body-joint-solreflimit)=

-   **`solreflimit`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    Solver reference parameters for joint limits.
    → See [solver parameters](#solver-attrs-solref).

(joint-body-joint-solimplimit)=

-   **`solimplimit`** [ <span class="badge array">real(5)</span> | <span class="badge required">Required</span> | **Default:** `0.9 0.95 0.001 0.5 2.0` ]

    Solver impedance parameters for joint limits.
    → See [solver parameters](#solver-attrs-solimp).

(joint-body-joint-stiffness)=

-   **`stiffness`** [ <span class="badge real">real</span> | <span class="badge optional">Optional</span> ]

    Joint stiffness. If this value is positive, a spring will be created with equilibrium
    position given by springref. The spring force is computed along with the other passive
    forces.

(joint-body-joint-springref)=

-   **`springref`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The joint position or angle in which the joint spring (if any) achieves equilibrium. All
    spring reference values specified with this attribute are collected into the spring
    reference configuration, which is also used to compute the spring reference lengths of
    all tendons.

(joint-body-joint-armature)=

-   **`armature`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Additional inertia associated with movement of the joint that is not due to body mass. This
    added inertia is usually due to a rotor (a.k.a armature) spinning faster than the joint
    itself due to a geared transmission. Because the gear ratio appears twice, multiplying both
    forces and lengths, the effect is known as \"reflected inertia\" and the equivalent value is
    the inertia of the spinning body multiplied by the square of the gear ratio. The value
    applies to all degrees of freedom created by this joint. Besides increasing the realism of
    joints with geared transmission, positive armature significantly improves simulation
    stability, even for small values, and is a recommended possible fix when encountering
    stability issues.

(joint-body-joint-damping)=

-   **`damping`** [ <span class="badge real">real</span> | <span class="badge optional">Optional</span> ]

    Damping applied to all degrees of freedom created by this joint. Unlike friction loss which
    is computed by the constraint solver, damping is simply a force linear in velocity. It is
    included in the passive forces. Despite this simplicity, larger damping values can make
    numerical integrators unstable, which is why the Euler integrator handles damping
    implicitly.

(joint-body-joint-frictionloss)=

-   **`frictionloss`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Friction loss due to dry friction. This value is the same for all degrees of freedom
    created by this joint. Semantically friction loss does not make sense for free joints, but
    the compiler allows it. To enable friction loss, set this attribute to a positive value.

(joint-body-joint-solreffriction)=

-   **`solreffriction`** [ <span class="badge array">real(2)</span> | <span class="badge required">Required</span> | **Default:** `0.02 1.0` ]

    -

(joint-body-joint-solimpfriction)=

-   **`solimpfriction`** [ <span class="badge array">real(5)</span> | <span class="badge required">Required</span> | **Default:** `0.9 0.95 0.001 0.5 2.0` ]

    -

<div class="motphys-extension-block">
<div class="motphys-extension-label">MPEX</div>

(joint-body-joint-hardlimit)=

-   **`hardlimit`** [ <span class="badge bool">bool</span> | <span class="badge optional">Optional</span> ]

    If true, the limit constraint is hard.

</div>

**Parent Elements**: [`(world)body`](<#(world)body>), [`default`](#default), [`equality`](#equality), [`fixed`](#fixed)

---

(freejoint)=

#### `freejoint`

This element creates a free joint whose only attributes are name and group. The freejoint
element is an XML shortcut for:

```xml
<joint type="free" stiffness="0" damping="0" frictionloss="0" armature="0"/>
```

While this joint can evidently be created with the joint element, default joint settings
could affect it. This is usually undesirable as physical free bodies do not have nonzero
stiffness, damping, friction or armature. To avoid this complication, the freejoint element
was introduced, ensuring joint defaults are not inherited. If the XML model is saved, it will
appear as a regular joint of type free.

**Attributes:**

(freejoint-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the joint.

(freejoint-group)=

-   **`group`** [ <span class="badge int">int</span> | <span class="badge optional">Optional</span> ]

    Integer group to which the joint belongs. This attribute can be used for custom tags. It is
    also used by the visualizer to enable and disable the rendering of entire groups of joints.

**Parent Elements**: [`(world)body`](<#(world)body>)

---

(attach)=

#### `attach`

The `attach` element is used to attach an external MJCF model's body subtree
to the current body. This is useful for modular model composition.

Unlike `include` which merges the entire external model at the root level,
`attach` inserts a specific body's children into the current body hierarchy.

**Attributes:**

(attach-model)=

-   **`model`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The model defined in asset element.

(attach-body)=

-   **`body`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the body in the sub-model to attach here.
    `None` means attaching the whole world body.

(attach-prefix)=

-   **`prefix`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    Prefix to prepend to all names in the sub-model. (e.g. bodys, joints, actuators, meshes...)
    Empty string (\"\") is allowed, but be careful of naming collisions.

**Parent Elements**: [`(world)body`](<#(world)body>)

---

(camera)=

#### `camera`

This element creates a camera, which moves with the body where it is defined. To create a fixed
camera, define it in the world body. The cameras created here are in addition to the default
free camera which is always defined and is adjusted via the visual element. The cameras have
a viewpoint that is always centered in front of the projection surface. The viewpoint coincides
with the center of the camera frame. The camera is looking along the -Z axis of its frame.
The +X axis points to the right, and the +Y axis points up. Thus the frame position and
orientation are the key adjustments that need to be made here.

```{note}
The `xyaxes` orientation attribute is semantically convenient for cameras, as the X and Y axes
 correspond to the directions \"right\" and \"up\" in pixel space, respectively.
```

**Attributes:**

(camera-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the camera.

(camera-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

(camera-mode)=

-   **`mode`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `fixed` ]

    **Choice:** [ `fixed` | `track` | `trackcom` | `targetbody` | `targetbodycom` ]

    This attribute specifies how the camera position and orientation in world coordinates are
    computed in forward kinematics (which in turn determine what the camera sees). \"fixed\"
    means that the position and orientation specified below are fixed relative to the body
    where the camera is defined. \"track\" means that the camera position is at a constant
    offset from the body in world coordinates, while the camera orientation is constant in
    world coordinates. These constants are determined by applying forward kinematics in
    qpos0 and treating the camera as fixed. Tracking can be used for example to position a
    camera above a body, point it down so it sees the body, and have it always remain above
    the body no matter how the body translates and rotates. \"trackcom\" is similar to
    \"track\" but the constant spatial offset is defined relative to the center of mass of
    the kinematic subtree starting at the body in which the camera is defined. This can be
    used to keep an entire mechanism in view. Note that the subtree center of mass for the
    world body is the center of mass of the entire model. So if a camera is defined in the
    world body in mode \"trackcom\", it will track the entire model. \"targetbody\" means that
    the camera position is fixed in the body frame, while the camera orientation is
    adjusted so that it always points towards the targeted body (which is specified with
    the target attribute below). This can be used for example to model an eye that fixates
    a moving object; the object will be the target, and the camera/eye will be defined in
    the body corresponding to the head. \"targetbodycom\" is the same as \"targetbody\" but the
    camera is oriented towards the center of mass of the subtree starting at the target
    body.

(camera-target)=

-   **`target`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    When the camera mode is \"targetbody\" or \"targetbodycom\", this attribute becomes required.
    It specifies which body should be targeted by the camera. In all other modes this
    attribute is ignored.

(camera-orthographic)=

-   **`orthographic`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `false` ]

    Whether the camera uses a perspective (the default) or orthographic projection. Setting
    this attribute to orthographic changes the semantic of the fovy attribute.

(camera-fovy)=

-   **`fovy`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `45.0` ]

    Vertical field-of-view of the camera. If the camera uses a perspective projection, the
    field-of-view is expressed in degrees, regardless of the global compiler/angle setting. If
    the camera uses an orthographic projection, the field-of-view is expressed in units of
    length; note that in this case the default of 45 is too large for most scenes and should
    likely be reduced. In either case, the horizontal field of view is computed automatically
    given the window size and the vertical field of view.

(camera-pos)=

-   **`pos`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 0.0` ]

    Position of the camera frame.

(camera-quat)=

-   **`quat`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the camera frame as unit quaternion.
    → See [rotation representation](#rotation-attrs-quat).

(camera-euler)=

-   **`euler`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the camera frame as Euler angles.
    → See [rotation representation](#rotation-attrs-euler).

(camera-axisangle)=

-   **`axisangle`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the camera frame as an axis-angle pair.
    → See [rotation representation](#rotation-attrs-axisangle).

(camera-xyaxes)=

-   **`xyaxes`** [ <span class="badge array">real(6)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the camera frame via X and Y axes. Semantically convenient for cameras:
    X and Y correspond to \"right\" and \"up\" in pixel space, respectively.
    → See [rotation representation](#rotation-attrs-xyaxes).

(camera-zaxis)=

-   **`zaxis`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the camera frame via Z axis direction.
    → See [rotation representation](#rotation-attrs-zaxis).

(camera-trackposspeed)=

-   **`trackposspeed`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Motphys-only extension. When not zero, the camera will move to target pose with this speed.

(camera-trackrotspeed)=

-   **`trackrotspeed`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Motphys-only extension. When not zero, the camera will rotate to target pose with this
    speed.

(camera-depth)=

-   **`depth`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `false` ]

    Motphys-only extension. When enabled, the camera renders depth information only.

(camera-znear)=

-   **`znear`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Motphys-only extension. The near clipping plane distance. If not specified, it will be
    automatically computed.

(camera-zfar)=

-   **`zfar`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Motphys-only extension. The far clipping plane distance. If not specified, it will be
    automatically computed.

**Parent Elements**: [`(world)body`](<#(world)body>), [`default`](#default)

---

(frame)=

#### `frame`

This element introduces a local coordinate frame without making it a distinct physical body.

**Attributes:**

(frame-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the frame.

(frame-childclass)=

-   **`childclass`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Child class for setting unspecified attributes.

(frame-pos)=

-   **`pos`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 0.0` ]

    Position of the frame.

(frame-quat)=

-   **`quat`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the frame as quaternion.

(frame-euler)=

-   **`euler`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the frame as euler angles.

(frame-axisangle)=

-   **`axisangle`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the frame as axis-angle.

(frame-xyaxes)=

-   **`xyaxes`** [ <span class="badge array">real(6)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the frame as xy-axes.

(frame-zaxis)=

-   **`zaxis`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the frame as z-axis.

**Parent Elements**: [`(world)body`](<#(world)body>)

---

(geom)=

#### `geom`

A geometric element attached rigidly to the body within which it is defined.

Multiple geoms can be attached to the same body. At runtime they determine the appearance
and collision properties of the body. At compile time they can also determine the inertial
properties of the body, depending on the presence of the `inertial` element and the setting
of the `inertiafromgeom` attribute of `compiler`. Inertial properties are computed by summing
the masses and inertias of all geoms attached to the body whose geom group falls within the
range specified by the `inertiagrouprange` attribute of `compiler`. The geom masses and
inertias are computed using the geom shape, a specified density or a geom mass which implies
a density, and the assumption of uniform density.

Geoms are not strictly required for physics simulation. One can create and simulate a model
that only has bodies and joints — such a model can even be visualized using equivalent inertia
boxes to represent bodies, with only contact forces missing.

```{note}
The following MJCF attributes are not currently supported:
 - `shellinertia`: Treat geom as a thin shell for inertia computation
 - `fitscale`: Scale factor for auto-fitting mesh geoms
 - `fluidshape`: Enable fluid interaction with ellipsoid shape
 - `fluidcoef`: Fluid interaction coefficients
 - `user`: User data array

 The following motrixsim-specific attribute is available:
 - `hard`: Enable hard contact mode
```

**Attributes:**

(geom-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the geom.

(geom-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

(geom-type)=

-   **`type`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `sphere` ]

    **Choice:** [ `plane` | `hfield` | `sphere` | `capsule` | `cylinder` | `box` | `mesh` ]

    Type of geometric shape. The keywords have the following meaning: the plane type defines
    a plane which is infinite for collision detection purposes; it can only be attached to the
    world body or static children of the world. The sphere type defines a sphere centered at
    the geom's position, using one size parameter for the radius. The capsule type defines a
    capsule — a cylinder capped with two half-spheres — oriented along the Z axis of the
    geom's frame. The cylinder type defines a right circular cylinder oriented along the Z
    axis of the geom's frame. The box type defines a box whose half-sizes along X, Y and Z
    are given by the three size parameters. The mesh type defines a mesh referenced by the
    mesh attribute. The hfield type defines a height field referenced by the hfield
    attribute.

(geom-contype)=

-   **`contype`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `1` ]

    This attribute and the next specify 32-bit integer bitmasks used for contact filtering of
    dynamically generated contact pairs. Two geoms can collide if the contype of one geom is
    compatible with the conaffinity of the other geom or vice versa. Compatible means that the
    two bitmasks have a common bit set to 1.

(geom-condim)=

-   **`condim`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `3` ]

    The dimensionality of the contact space for a dynamically generated contact pair is set to
    the maximum of the condim values of the two participating geoms. The allowed values and
    their meaning are: 1 for frictionless contact; 3 for regular frictional contact opposing
    slip in the tangent plane; 4 for frictional contact opposing slip in the tangent plane and
    rotation around the contact normal, useful for modeling soft contacts; 6 for frictional
    contact opposing slip in the tangent plane, rotation around the contact normal, and
    rotation around the two axes of the tangent plane, the latter being useful for preventing
    objects from rolling indefinitely.

(geom-conaffinity)=

-   **`conaffinity`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `1` ]

    Bitmask for contact filtering; see contype above.

(geom-mesh)=

-   **`mesh`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If the geom type is \"mesh\", this attribute is required and references the mesh asset to be
    instantiated. This attribute can also be specified if the geom type corresponds to a
    geometric primitive such as sphere, capsule, cylinder, ellipsoid, or box, in which case
    the primitive is automatically fitted to the referenced mesh asset. In the compiled model
    the geom is represented as a regular geom of the specified primitive type with no
    reference to the mesh used for fitting.

(geom-group)=

-   **`group`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    This attribute specifies an integer group to which the geom belongs. The only effect on
    the physics is at compile time, when body masses and inertias are inferred from geoms
    selected based on their group via the `inertiagrouprange` attribute of `compiler`. At
    runtime this attribute is used by the visualizer to enable and disable the rendering of
    entire geom groups. By default, groups 0, 1 and 2 are visible while all other groups are
    invisible. The group attribute can also be used as a tag for custom computations.

(geom-size)=

-   **`size`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    Geom size parameters. The number of required parameters and their meaning depends on the
    geom type as documented under the type attribute. All required size parameters must be
    positive. Note that when a non-mesh geom type references a mesh, a geometric primitive of
    that type is fitted to the mesh and the geom size parameters are ignored. When using the
    fromto attribute, only the first size parameter is used (specifying the radius or
    half-size perpendicular to the elongation direction).

(geom-priority)=

-   **`priority`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    The geom priority determines how the properties of two colliding geoms are combined to
    form the properties of the contact. This interacts with the solmix attribute. When the
    priorities of the two geoms differ, the contact parameters of the higher-priority geom
    are used. When priorities are equal, the parameters are mixed according to solmix.

(geom-material)=

-   **`material`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, this attribute applies a material to the geom. Otherwise, if unspecified
    and the type of the geom is a mesh, the compiler will apply the mesh asset material if
    present. The material determines the visual properties of the geom. The only exception is
    color: if the rgba attribute is different from its internal default, rgba takes precedence
    while the remaining material properties are still applied.

(geom-rgba)=

-   **`rgba`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `0.5 0.5 0.5 1.0` ]

    Instead of creating material assets and referencing them, this attribute can be used to
    set color and transparency only. This is not as flexible as the material mechanism, but
    is more convenient and is often sufficient. If the value of this attribute is different
    from the internal default, it takes precedence over the material.

(geom-friction)=

-   **`friction`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `1.0 0.005 0.0001` ]

    Contact friction parameters for dynamically generated contact pairs. The first number is
    the sliding friction, acting along both axes of the tangent plane. The second number is
    the torsional friction, acting around the contact normal. The third number is the rolling
    friction, acting around both axes of the tangent plane. The friction parameters for the
    contact pair are combined depending on the solmix and priority attributes.

(geom-mass)=

-   **`mass`** [ <span class="badge real">real</span> | <span class="badge optional">Optional</span> ]

    If this attribute is specified, the density attribute below is ignored and the geom
    density is computed from the given mass, using the geom shape and the assumption of
    uniform density. The computed density is then used to obtain the geom inertia. The geom
    mass and inertia are only used during compilation to infer the body mass and inertia if
    necessary; at runtime only the body inertial properties affect the simulation.

(geom-density)=

-   **`density`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `1000` ]

    Material density used to compute the geom mass and inertia. The computation is based on
    the geom shape and the assumption of uniform density. This attribute is used only when
    the mass attribute above is unspecified. The density has semantics of mass per unit volume
    (unless shellinertia is true, in which case it has semantics of mass per unit area).

(geom-margin)=

-   **`margin`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Distance threshold below which contacts are detected and included in the global array
    the contact data. A contact is considered active only if the distance between the two geom
    surfaces is below margin minus gap. Constraint impedance can be a function of distance,
    and the quantity this function is applied to is the distance between the two geoms minus
    the margin plus the gap.

(geom-gap)=

-   **`gap`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    This attribute is used to enable the generation of inactive contacts, i.e., contacts that
    are ignored by the constraint solver but are included in the contact data for the purpose
    of custom computations. When this value is positive, geom distances between margin and
    margin minus gap correspond to such inactive contacts.

(geom-fromto)=

-   **`fromto`** [ <span class="badge array">real(6)</span> | <span class="badge optional">Optional</span> ]

    This attribute can only be used with capsule, box, cylinder and ellipsoid geoms. It
    provides an alternative specification of the geom length as well as the frame position
    and orientation. The six numbers are the 3D coordinates of one point followed by the 3D
    coordinates of another point. The elongated part of the geom connects these two points,
    with the +Z axis of the geom's frame oriented from the first towards the second point,
    while in the perpendicular direction the geom sizes are both equal to the first value of
    the size attribute. The frame position is in the middle between the end points. If this
    attribute is specified, the remaining position and orientation-related attributes are
    ignored. Note that the fromto semantics of capsule are unique: the two end points specify
    the segment around which the radius defines the capsule surface.

(geom-pos)=

-   **`pos`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0. 0. 0.` ]

    Position of the geom, specified in the frame of the body where the geom is defined.

(geom-quat)=

-   **`quat`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the geom frame as unit quaternion.
    → See [rotation representation](#rotation-attrs-quat).

(geom-euler)=

-   **`euler`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the geom frame as Euler angles.
    → See [rotation representation](#rotation-attrs-euler).

(geom-axisangle)=

-   **`axisangle`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the geom frame as an axis-angle pair.
    → See [rotation representation](#rotation-attrs-axisangle).

(geom-xyaxes)=

-   **`xyaxes`** [ <span class="badge array">real(6)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the geom frame via X and Y axes.
    → See [rotation representation](#rotation-attrs-xyaxes).

(geom-zaxis)=

-   **`zaxis`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the geom frame via Z axis direction.
    → See [rotation representation](#rotation-attrs-zaxis).

(geom-solmix)=

-   **`solmix`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `1.0` ]

    This attribute specifies the weight used for averaging of contact parameters, and
    interacts with the priority attribute. When two geoms with equal priority collide, their
    contact parameters are mixed using solmix as the weight for one geom and (1 - solmix)
    for the other.

(geom-solref)=

-   **`solref`** [ <span class="badge array">real(2)</span> | <span class="badge required">Required</span> | **Default:** `0.02 1.0` ]

    Solver reference parameters for contact simulation.
    → See [solver parameters](#solver-attrs-solref).

(geom-solimp)=

-   **`solimp`** [ <span class="badge array">real(5)</span> | <span class="badge required">Required</span> | **Default:** `0.9 0.95 0.001 0.5 2.0` ]

    Solver impedance parameters for contact simulation.
    → See [solver parameters](#solver-attrs-solimp).

(geom-hfield)=

-   **`hfield`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    This attribute must be specified if and only if the geom type is \"hfield\". It references
    the height field asset to be instantiated at the position and orientation of the geom
    frame.

**Parent Elements**: [`(world)body`](<#(world)body>), [`default`](#default)

---

(light)=

#### `light`

This element creates a light, which moves with the body where it is defined. To create a fixed
light, define it in the world body. The lights created here are in addition to the headlight
which is always defined and is configured via the visual element. Lights shine along the
direction specified by the dir attribute. They do not have a full spatial frame with three
orthogonal axes.

MJCF supports multiple lighting models (e.g. Phong lighting with shadow mapping and
physically-based rendering). Attributes may be applied or ignored depending on the lighting
model being used by the renderer.

```{note}
To create a fixed light that does not move with any body, define it in the world body.
```

**Attributes:**

(light-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the light.

(light-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

(light-mode)=

-   **`mode`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `fixed` ]

    **Choice:** [ `fixed` | `track` | `trackcom` | `targetbody` | `targetbodycom` ]

    This attribute specifies how the light position and orientation in world coordinates are
    computed in forward kinematics, which in turn determines what the light illuminates.
    \"fixed\" means that the position and orientation specified below are fixed relative to the
    body where the light is defined. \"track\" means that the light position is at a constant
    offset from the body in world coordinates, while the orientation is constant in world
    coordinates. \"trackcom\" is similar to \"track\" but the constant spatial offset is defined
    relative to the center of mass of the kinematic subtree starting at the body in which the
    light is defined. \"targetbody\" means that the light position is fixed in the body frame,
    while the orientation is adjusted so that it always points towards the targeted body
    specified with the target attribute. \"targetbodycom\" is the same as \"targetbody\" but the
    light is oriented towards the center of mass of the subtree starting at the target body.

(light-target)=

-   **`target`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    This attribute specifies which body should be targeted in \"targetbody\" and \"targetbodycom\"
    modes. In all other modes this attribute is ignored.

(light-type)=

-   **`type`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `spot` ]

    **Choice:** [ `spot` | `point` | `directional` ]

    Determines the type of light. Note that some light types may not be supported by some
    renderers (e.g. only spot and directional lights are supported by the default native
    renderer).

(light-directional)=

-   **`directional`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `false` ]

    This is a deprecated legacy attribute. Please use the type attribute instead. If set to
    \"true\", and no type is specified, this will change the light type to be directional.

(light-castshadow)=

-   **`castshadow`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `true` ]

    If this attribute is \"true\" the light will cast shadows. More precisely, the geoms
    illuminated by the light will cast shadows, however this is a property of lights rather
    than geoms. Since each shadow-casting light causes one extra rendering pass through all
    geoms, this attribute should be used with caution. Higher quality shadows are achieved by
    increasing the value of the shadowsize attribute of quality, as well as positioning
    spotlights closer to the surface on which shadows appear, and limiting the volume in which
    shadows are cast. For spotlights this volume is a cone, whose angle is the cutoff attribute
    multiplied by the shadowscale attribute of map. For directional lights this volume is a
    box, whose half-sizes in the directions orthogonal to the light are the model extent
    multiplied by the shadowclip attribute of map. Internally the shadow-mapping mechanism
    renders the scene from the light viewpoint into a depth texture, and then renders again
    from the camera viewpoint, using the depth texture to create shadows.

(light-dir)=

-   **`dir`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 -1.0` ]

    Direction of the light.

(light-pos)=

-   **`pos`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 0.0` ]

    Position of the light. This attribute only affects the rendering for spotlights, but it
    should also be defined for directional lights because they are rendered as decorative
    elements.

(light-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `45.0` ]

    Cutoff angle for spotlights, always in degrees regardless of the global angle setting.

(light-range)=

-   **`range`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `10.0` ]

    The effective range of the light. Objects further than this distance from the light
    position will not be illuminated by this light. This only applies to spotlights.

(light-bulbradius)=

-   **`bulbradius`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.02` ]

    The radius of the light source which can affect shadow softness depending on the renderer.
    This only applies to spotlights.

(light-attenuation)=

-   **`attenuation`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `1.0 0.0 0.0` ]

    The constant, linear and quadratic attenuation coefficients for Phong lighting. The default
    corresponds to no attenuation.

(light-intensity)=

-   **`intensity`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The intensity of the light source, measured in candela, used for physically-based lighting
    models. This is unused by the default Phong lighting model.

(light-ambient)=

-   **`ambient`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 0.0` ]

    The ambient color of the light, used by the default Phong lighting model.

(light-diffuse)=

-   **`diffuse`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.7 0.7 0.7` ]

    The color of the light. For the Phong (default) lighting model, this defines the diffuse
    color of the light.

(light-specular)=

-   **`specular`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.3 0.3 0.3` ]

    The specular color of the light, used by the default Phong lighting model.

(light-innerangle)=

-   **`innerangle`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `35.0` ]

    ----------Motphys Only----------
    Cutoff angle for spotlights in degrees as inner angle. Motphys-only extension.

(light-nearz)=

-   **`nearz`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.1` ]

    The distance from the light to the near Z plane in the shadow map. Motphys-only extension.

**Parent Elements**: [`(world)body`](<#(world)body>), [`default`](#default)

---

(replicate)=

#### `replicate`

This element is used to replicate a sub-tree of the model.

**Attributes:**

(replicate-count)=

-   **`count`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Number of times to replicate the child nodes.

(replicate-sep)=

-   **`sep`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Separator used to generate new names for the replicated elements.

(replicate-offset)=

-   **`offset`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Translation offset between consecutive replications.

(replicate-euler)=

-   **`euler`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Rotation offset between consecutive replications.

**Parent Elements**: [`(world)body`](<#(world)body>)

---

(site)=

#### `site`

A site is a simplified and restricted kind of geom. Semantically, sites represent locations of
interest relative to the body frames. Sites do not participate in collisions and computation of
body masses and inertias. The geometric shapes that can be used to render sites are limited to a
subset of the available geom types. However, sites can be used in some places where geoms are
not allowed: mounting sensors, specifying via-points of spatial tendons, and constructing
slider-crank transmissions for actuators.

```{note}
Sites do not participate in collision detection. Only a subset of geom types are supported for
 rendering: sphere, capsule, ellipsoid, cylinder, and box.
```

**Attributes:**

(site-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the site.

(site-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

(site-type)=

-   **`type`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `sphere` ]

    **Choice:** [ `sphere` | `capsule` | `cylinder` | `box` ]

    Type of geometric shape. This is used for rendering, and also determines the active sensor
    zone for touch sensors.

(site-group)=

-   **`group`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Integer group to which the site belongs. This attribute can be used for custom tags. It is
    also used by the visualizer to enable and disable the rendering of entire groups of sites.

(site-material)=

-   **`material`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Material used to specify the visual properties of the site.

(site-rgba)=

-   **`rgba`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `0.5 0.5 0.5 1.0` ]

    Color and transparency. If this value is different from the internal default, it overrides
    the corresponding material properties.

(site-size)=

-   **`size`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    Sizes of the geometric shape representing the site.

(site-fromto)=

-   **`fromto`** [ <span class="badge array">real(6)</span> | <span class="badge optional">Optional</span> ]

    This attribute can only be used with capsule, cylinder, ellipsoid and box sites. It
    provides an alternative specification of the site length as well as the frame position and
    orientation. The six numbers are the 3D coordinates of one point followed by the 3D
    coordinates of another point. The elongated part of the site connects these two points,
    with the +Z axis of the site's frame oriented from the first towards the second point. The
    frame position is in the middle between the two points. If this attribute is specified, the
    remaining position and orientation-related attributes are ignored.

(site-pos)=

-   **`pos`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 0.0` ]

    Position of the site frame.

(site-quat)=

-   **`quat`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the site frame as unit quaternion.
    → See [rotation representation](#rotation-attrs-quat).

(site-euler)=

-   **`euler`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the site frame as Euler angles.
    → See [rotation representation](#rotation-attrs-euler).

(site-axisangle)=

-   **`axisangle`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the site frame as an axis-angle pair.
    → See [rotation representation](#rotation-attrs-axisangle).

(site-xyaxes)=

-   **`xyaxes`** [ <span class="badge array">real(6)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the site frame via X and Y axes.
    → See [rotation representation](#rotation-attrs-xyaxes).

(site-zaxes)=

-   **`zaxes`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Orientation of the site frame via Z axis direction.
    → See [rotation representation](#rotation-attrs-zaxis).

**Parent Elements**: [`(world)body`](<#(world)body>), [`default`](#default)

---

(option)=

### `option`

Global simulation options that control physics behavior and solver settings.

These are simulation options and do not affect the compilation process in any way; they are
simply copied into the low level model. Even though these options can be modified at runtime,
it is nevertheless a good idea to adjust them properly through the XML.

```{note}
The most important parameter affecting the speed-accuracy trade-off is `timestep`. Stability
 is determined not only by the time step but also by the solver parameters; in particular,
 softer constraints can be simulated with larger time steps.
```

**Attributes:**

(option-timestep)=

-   **`timestep`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.002` ]

    The simulation time step in seconds. This is the single most important parameter affecting
    the speed-accuracy trade-off which is inherent in every physics simulation. Smaller values
    result in better accuracy and stability. To achieve real-time performance, the time step
    must be larger than the CPU time per step (or 4 times larger when using the RK4
    integrator). Models with many floating objects (resulting in many contacts) are more
    demanding computationally. When fine-tuning a challenging model, it is recommended to
    experiment with both time step and solver parameter settings jointly. In
    optimization-related applications where real-time is insufficient, the time step should be
    made as large as possible.

(option-gravity)=

-   **`gravity`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 -9.81` ]

    Gravitational acceleration vector. In the default world orientation the Z-axis points up,
    which is the convention used throughout the simulation stack and is not recommended to
    deviate from.

(option-iterations)=

-   **`iterations`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `100` ]

    Maximum number of iterations of the constraint solver. When the warmstart flag is enabled
    (which is the default), accurate results are obtained with fewer iterations. Larger and
    more complex systems with many interacting constraints require more iterations. Note that
    the solver computes convergence statistics during simulation, which can be accessed via the
    simulation data.

(option-tolerance)=

-   **`tolerance`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `1e-8` ]

    Tolerance threshold used for early termination of the iterative solver. For PGS, the
    threshold is applied to the cost improvement between two iterations. For CG and Newton, it
    is applied to the smaller of the cost improvement and the gradient norm. Set the tolerance
    to 0 to disable early termination.

(option-o_solref)=

-   **`o_solref`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    These attributes replace the solref, solimp and friction parameters of all active contact
    pairs when contact override is enabled.

(option-o_solimp)=

-   **`o_solimp`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    These attributes replace the solref, solimp and friction parameters of all active contact
    pairs when contact override is enabled.

(option-o_friction)=

-   **`o_friction`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    These attributes replace the solref, solimp and friction parameters of all active contact
    pairs when contact override is enabled.

(option-o_margin)=

-   **`o_margin`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    This attribute replaces the margin parameter of all active contact pairs when Contact
    override is enabled. Otherwise the element-specific margin attribute of geom or pair is
    used depending on how the contact pair was generated. The related gap parameter does not
    have a global override.

**Parent Elements**: [`mujoco`](#mujoco)

**Child Elements**: [`flag`](#flag)

---

(flag)=

#### `flag`

Flags that enable and disable different parts of the simulation pipeline.

The actual flags used at runtime are represented as the bits of two integers, used to disable
standard features and enable optional features respectively. The reason for this separation is
that setting both integers to 0 restores the default.

```{note}
In the XML, the separation between disableflags and enableflags is not made explicit, except
 for the default attribute values — which are \"enable\" for flags corresponding to standard
 features, and \"disable\" for flags corresponding to optional features.
```

**Attributes:**

(flag-constraint)=

-   **`constraint`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `enable` ]

    **Choice:** [ `disable` | `enable` ]

    When set to disable, all standard computations related to the constraint solver are
    skipped and no constraint forces are applied. Note that the equality, frictionloss, limit,
    and contact flags each disable computations for a specific type of constraint; both this
    flag and the type-specific flag must be set to enable for a given computation to be
    performed.

(flag-equality)=

-   **`equality`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `enable` ]

    **Choice:** [ `disable` | `enable` ]

    When set to disable, all standard computations related to equality constraints are skipped.

(flag-frictionloss)=

-   **`frictionloss`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `enable` ]

    **Choice:** [ `disable` | `enable` ]

    When set to disable, all standard computations related to friction loss constraints are
    skipped.

(flag-limit)=

-   **`limit`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `enable` ]

    **Choice:** [ `disable` | `enable` ]

    When set to disable, all standard computations related to joint and tendon limit
    constraints are skipped.

(flag-contact)=

-   **`contact`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `enable` ]

    **Choice:** [ `disable` | `enable` ]

    When set to disable, collision detection and all standard computations related to contact
    constraints are skipped.

(flag-gravity)=

-   **`gravity`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `enable` ]

    **Choice:** [ `disable` | `enable` ]

    When set to disable, the gravitational acceleration vector is replaced with (0 0 0) at
    runtime, without changing the stored value. Once the flag is re-enabled, the stored value
    is used again.

(flag-actuation)=

-   **`actuation`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `enable` ]

    **Choice:** [ `disable` | `enable` ]

    When set to disable, all standard computations related to actuator forces are skipped,
    including the actuator dynamics. As a result, no actuator forces are applied to the
    simulation.

(flag-refsafe)=

-   **`refsafe`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `enable` ]

    **Choice:** [ `disable` | `enable` ]

    -

(flag-override)=

-   **`override`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `disable` ]

    **Choice:** [ `disable` | `enable` ]

    When set to enable, activates the Contact override mechanism, which causes the global
    o_margin, o_solref, o_solimp, and o_friction values to replace the corresponding
    per-contact parameters for all active contact pairs.

**Parent Elements**: [`option`](#option)

---

(actuator)=

### `actuator`

This is a grouping element for actuator definitions. The first 13 common attributes of all
actuator-related elements are the same and are documented under the general actuator type.

**Parent Elements**: [`mujoco`](#mujoco)

**Child Elements**: [`adhesion`](#adhesion), [`general`](#general), [`motor`](#motor), [`position`](#position), [`velocity`](#velocity)

---

(adhesion)=

#### `adhesion`

This element defines an active adhesion actuator which injects forces at contacts in the
normal direction. The transmission target is a body, and adhesive forces are injected into
all contacts involving geoms which belong to this body. The force is divided equally
between multiple contacts.

When the gap attribute is not used, this actuator requires active contacts and cannot
apply a force at a distance, more like the active adhesion on the feet of geckos and
insects rather than an industrial vacuum gripper. In order to enable suction at a
distance, inflate the body's geoms by margin and add a corresponding gap which activates
contacts only after gap penetration distance.

```{note}
An adhesion actuator's length is always 0. ctrlrange is required and must be nonnegative
 (no repulsive forces are allowed). The body attribute is required.
```

**Attributes:**

(adhesion-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Element name.

(adhesion-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Active defaults class for setting unspecified attributes.

(adhesion-group)=

-   **`group`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Integer group to which the actuator belongs. This attribute can be used for custom
    tags. It is also used by the visualizer to enable and disable the rendering of
    entire groups of actuators.

(adhesion-ctrllimited)=

-   **`ctrllimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If true, the control input to this actuator is automatically clamped to ctrlrange
    at runtime. If false, control input clamping is disabled. If \"auto\" and autolimits
    is set in compiler, control clamping will automatically be set to true if ctrlrange
    is defined without explicitly setting this attribute to \"true\". Note that control
    input clamping can also be globally disabled with the clampctrl attribute of
    option/flag.

(adhesion-forcelimited)=

-   **`forcelimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If true, the force output of this actuator is automatically clamped to forcerange
    at runtime. If false, force clamping is disabled. If \"auto\" and autolimits is set
    in compiler, force clamping will automatically be set to true if forcerange is
    defined without explicitly setting this attribute to \"true\".

(adhesion-ctrlrange)=

-   **`ctrlrange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping the control input. The first value must be smaller than the
    second value. Setting this attribute without specifying ctrllimited is an error if
    autolimits is \"false\" in compiler.

(adhesion-forcerange)=

-   **`forcerange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping the force output. The first value must be no greater than the
    second value. Setting this attribute without specifying forcelimited is an error if
    autolimits is \"false\" in compiler.

(adhesion-gear)=

-   **`gear`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `1. 0. 0. 0. 0. 0.` ]

    Scales the length (and consequently moment arms, velocity and force) of the
    actuator, for all transmission types. It is different from the gain in the force
    generation mechanism, because the gain only scales the force output and does not
    affect the length, moment arms and velocity. For actuators with scalar
    transmission, only the first element of this vector is used. The remaining
    elements are needed for joint, jointinparent and site transmissions where this
    attribute is used to specify 3D force and torque axes.

(adhesion-joint)=

-   **`joint`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, the actuator acts on the given joint. For hinge and slide joints,
    the actuator length equals the joint position/angle times the first element of
    gear. For ball joints, the first three elements of gear define a 3D rotation axis
    in the child frame around which the actuator produces torque. For free joints,
    gear defines a 3D translation axis in the world frame followed by a 3D rotation
    axis in the child frame.

(adhesion-tendon)=

-   **`tendon`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, the actuator acts on the given tendon. The actuator length equals
    the tendon length times the gear ratio. Both spatial and fixed tendons can be
    used.

(adhesion-body)=

-   **`body`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    The actuator acts on all contacts involving this body's geoms. This attribute is
    required.

(adhesion-gain)=

-   **`gain`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `1.0` ]

    Gain of the adhesion actuator, in units of force. The total adhesion force applied by
    the actuator is the control value multiplied by the gain. This force is distributed
    equally between all the contacts involving geoms belonging to the target body.

**Parent Elements**: [`actuator`](#actuator), [`default`](#default)

---

(general)=

#### `general`

This element creates a general actuator, providing full access to all actuator components
and allowing the user to specify them independently.

The general actuator combines three independently configurable subsystems: activation
dynamics (dyntype/dynprm), gain (gaintype/gainprm), and bias (biastype/biasprm). The
output force is computed as: scalar_force = gain_term \* (act or ctrl) + bias_term, where
the activation state is used when present and the control input otherwise.

**Attributes:**

(general-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Element name.

(general-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Active defaults class for setting unspecified attributes.

(general-group)=

-   **`group`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Integer group to which the actuator belongs. This attribute can be used for custom
    tags. It is also used by the visualizer to enable and disable the rendering of
    entire groups of actuators.

(general-ctrllimited)=

-   **`ctrllimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If true, the control input to this actuator is automatically clamped to ctrlrange
    at runtime. If false, control input clamping is disabled. If \"auto\" and autolimits
    is set in compiler, control clamping will automatically be set to true if ctrlrange
    is defined without explicitly setting this attribute to \"true\". Note that control
    input clamping can also be globally disabled with the clampctrl attribute of
    option/flag.

(general-forcelimited)=

-   **`forcelimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If true, the force output of this actuator is automatically clamped to forcerange
    at runtime. If false, force clamping is disabled. If \"auto\" and autolimits is set
    in compiler, force clamping will automatically be set to true if forcerange is
    defined without explicitly setting this attribute to \"true\".

(general-ctrlrange)=

-   **`ctrlrange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping the control input. The first value must be smaller than the
    second value. Setting this attribute without specifying ctrllimited is an error if
    autolimits is \"false\" in compiler.

(general-forcerange)=

-   **`forcerange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping the force output. The first value must be no greater than the
    second value. Setting this attribute without specifying forcelimited is an error if
    autolimits is \"false\" in compiler.

(general-gear)=

-   **`gear`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `1. 0. 0. 0. 0. 0.` ]

    Scales the length (and consequently moment arms, velocity and force) of the
    actuator, for all transmission types. It is different from the gain in the force
    generation mechanism, because the gain only scales the force output and does not
    affect the length, moment arms and velocity. For actuators with scalar
    transmission, only the first element of this vector is used. The remaining
    elements are needed for joint, jointinparent and site transmissions where this
    attribute is used to specify 3D force and torque axes.

(general-joint)=

-   **`joint`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, the actuator acts on the given joint. For hinge and slide joints,
    the actuator length equals the joint position/angle times the first element of
    gear. For ball joints, the first three elements of gear define a 3D rotation axis
    in the child frame around which the actuator produces torque. For free joints,
    gear defines a 3D translation axis in the world frame followed by a 3D rotation
    axis in the child frame.

(general-tendon)=

-   **`tendon`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, the actuator acts on the given tendon. The actuator length equals
    the tendon length times the gear ratio. Both spatial and fixed tendons can be
    used.

(general-dyntype)=

-   **`dyntype`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `none` ]

    **Choice:** [ `none` | `integrator` | `filter` | `filterexact` | `muscle` | `user` ]

    Activation dynamics type for the actuator. Determines how the internal activation
    state evolves in response to control input. Available types are: none (no internal
    state), integrator (act_dot = ctrl), filter (act_dot = (ctrl - act) / dynprm[0]),
    filterexact (like filter but with exact integration), muscle (act_dot =
    mju_muscleDynamics(...)), and user (act_dot = mjcb_act_dyn(...)).

(general-gaintype)=

-   **`gaintype`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `fixed` ]

    **Choice:** [ `fixed` | `affine` | `muscle` | `user` ]

    The gain type determines the gain_term in the force generation formula. Available
    types are: fixed (gain_term = gainprm[0]), affine (gain_term = gainprm[0] +
    gainprm[1]*length + gainprm[2]*velocity), muscle (gain_term = mju_muscleGain(...)),
    and user (gain_term = mjcb_act_gain(...)).

(general-biastype)=

-   **`biastype`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `none` ]

    **Choice:** [ `none` | `affine` | `muscle` | `user` ]

    The bias type determines the bias_term in the force generation formula. Available
    types are: none (bias_term = 0), affine (bias_term = biasprm[0] +
    biasprm[1]*length + biasprm[2]*velocity), muscle (bias_term =
    mju_muscleBias(...)), and user (bias_term = mjcb_act_bias(...)).

(general-dynprm)=

-   **`dynprm`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.` ]

    Activation dynamics parameters. The built-in activation types (except for muscle)
    use only the first parameter, but additional parameters are provided in case user
    callbacks implement a more elaborate model. The length of this array is not enforced
    by the parser, so the user can enter as many parameters as needed.

(general-gainprm)=

-   **`gainprm`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.` ]

    Gain parameters. The built-in gain types (except for muscle) use only the first
    parameter, but additional parameters are provided in case user callbacks implement a
    more elaborate model. The length of this array is not enforced by the parser, so the
    user can enter as many parameters as needed.

(general-biasprm)=

-   **`biasprm`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `0.; 10` ]

    Bias parameters. The affine bias type uses three parameters. The length of this array
    is not enforced by the parser, so the user can enter as many parameters as needed.

(general-actearly)=

-   **`actearly`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `false` ]

    If true, force computation will use the next value of the activation variable rather
    than the current one. Setting this flag reduces the delay between the control and
    accelerations by one time-step.

**Parent Elements**: [`actuator`](#actuator), [`default`](#default)

---

(motor)=

#### `motor`

This element creates a direct-drive actuator. It is one of the actuator shortcuts that
maps to a general actuator with fixed gain, no activation dynamics, and no bias
(dyntype=none, gaintype=fixed, biastype=none). The control input is transmitted directly
as force or torque scaled by the gear ratio and gainprm[0].

**Attributes:**

(motor-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Element name.

(motor-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Active defaults class for setting unspecified attributes.

(motor-group)=

-   **`group`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Integer group to which the actuator belongs. This attribute can be used for custom
    tags. It is also used by the visualizer to enable and disable the rendering of
    entire groups of actuators.

(motor-ctrllimited)=

-   **`ctrllimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If true, the control input to this actuator is automatically clamped to ctrlrange
    at runtime. If false, control input clamping is disabled. If \"auto\" and autolimits
    is set in compiler, control clamping will automatically be set to true if ctrlrange
    is defined without explicitly setting this attribute to \"true\". Note that control
    input clamping can also be globally disabled with the clampctrl attribute of
    option/flag.

(motor-forcelimited)=

-   **`forcelimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If true, the force output of this actuator is automatically clamped to forcerange
    at runtime. If false, force clamping is disabled. If \"auto\" and autolimits is set
    in compiler, force clamping will automatically be set to true if forcerange is
    defined without explicitly setting this attribute to \"true\".

(motor-ctrlrange)=

-   **`ctrlrange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping the control input. The first value must be smaller than the
    second value. Setting this attribute without specifying ctrllimited is an error if
    autolimits is \"false\" in compiler.

(motor-forcerange)=

-   **`forcerange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping the force output. The first value must be no greater than the
    second value. Setting this attribute without specifying forcelimited is an error if
    autolimits is \"false\" in compiler.

(motor-gear)=

-   **`gear`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `1. 0. 0. 0. 0. 0.` ]

    Scales the length (and consequently moment arms, velocity and force) of the
    actuator, for all transmission types. It is different from the gain in the force
    generation mechanism, because the gain only scales the force output and does not
    affect the length, moment arms and velocity. For actuators with scalar
    transmission, only the first element of this vector is used. The remaining
    elements are needed for joint, jointinparent and site transmissions where this
    attribute is used to specify 3D force and torque axes.

(motor-joint)=

-   **`joint`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, the actuator acts on the given joint. For hinge and slide joints,
    the actuator length equals the joint position/angle times the first element of
    gear. For ball joints, the first three elements of gear define a 3D rotation axis
    in the child frame around which the actuator produces torque. For free joints,
    gear defines a 3D translation axis in the world frame followed by a 3D rotation
    axis in the child frame.

(motor-tendon)=

-   **`tendon`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, the actuator acts on the given tendon. The actuator length equals
    the tendon length times the gear ratio. Both spatial and fixed tendons can be
    used.

**Parent Elements**: [`actuator`](#actuator), [`default`](#default)

---

(position)=

#### `position`

This element creates a position servo with an optional first-order filter. It is an
actuator shortcut that configures a general actuator with gaintype=fixed (gainprm=kp),
biastype=affine (biasprm = [0, -kp, -kv]), and optionally dyntype=filterexact when a
non-zero timeconst is specified.

```{note}
This actuator cannot be combined with both ctrlrange and inheritrange simultaneously;
 exactly one must be used if range clamping is desired.
```

**Attributes:**

(position-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Element name.

(position-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Active defaults class for setting unspecified attributes.

(position-group)=

-   **`group`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Integer group to which the actuator belongs. This attribute can be used for custom
    tags. It is also used by the visualizer to enable and disable the rendering of
    entire groups of actuators.

(position-ctrllimited)=

-   **`ctrllimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If true, the control input to this actuator is automatically clamped to ctrlrange
    at runtime. If false, control input clamping is disabled. If \"auto\" and autolimits
    is set in compiler, control clamping will automatically be set to true if ctrlrange
    is defined without explicitly setting this attribute to \"true\". Note that control
    input clamping can also be globally disabled with the clampctrl attribute of
    option/flag.

(position-forcelimited)=

-   **`forcelimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If true, the force output of this actuator is automatically clamped to forcerange
    at runtime. If false, force clamping is disabled. If \"auto\" and autolimits is set
    in compiler, force clamping will automatically be set to true if forcerange is
    defined without explicitly setting this attribute to \"true\".

(position-ctrlrange)=

-   **`ctrlrange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping the control input. The first value must be smaller than the
    second value. Setting this attribute without specifying ctrllimited is an error if
    autolimits is \"false\" in compiler.

(position-forcerange)=

-   **`forcerange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping the force output. The first value must be no greater than the
    second value. Setting this attribute without specifying forcelimited is an error if
    autolimits is \"false\" in compiler.

(position-gear)=

-   **`gear`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `1. 0. 0. 0. 0. 0.` ]

    Scales the length (and consequently moment arms, velocity and force) of the
    actuator, for all transmission types. It is different from the gain in the force
    generation mechanism, because the gain only scales the force output and does not
    affect the length, moment arms and velocity. For actuators with scalar
    transmission, only the first element of this vector is used. The remaining
    elements are needed for joint, jointinparent and site transmissions where this
    attribute is used to specify 3D force and torque axes.

(position-joint)=

-   **`joint`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, the actuator acts on the given joint. For hinge and slide joints,
    the actuator length equals the joint position/angle times the first element of
    gear. For ball joints, the first three elements of gear define a 3D rotation axis
    in the child frame around which the actuator produces torque. For free joints,
    gear defines a 3D translation axis in the world frame followed by a 3D rotation
    axis in the child frame.

(position-tendon)=

-   **`tendon`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, the actuator acts on the given tendon. The actuator length equals
    the tendon length times the gear ratio. Both spatial and fixed tendons can be
    used.

(position-kp)=

-   **`kp`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `1.0` ]

    Position feedback gain. Used internally as gainprm[0] and also negated into
    biasprm[1] to produce a restoring force proportional to position error.

(position-kv)=

-   **`kv`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Damping applied by the actuator. Used internally as biasprm[2] (negated) to produce
    a force proportional to velocity. When using this attribute, it is recommended to use
    the implicitfast or implicit integrators.

(position-inheritrange)=

-   **`inheritrange`** [ <span class="badge real">real</span> | <span class="badge optional">Optional</span> ]

    Automatically sets the actuator's ctrlrange to match the transmission target's range.
    A positive value X sets the ctrlrange around the midpoint of the target range, scaled
    by X. For example if the target joint has range [0, 1], then a value of 1.0 will set
    ctrlrange to [0, 1]; values of 0.8 and 1.2 will set the ctrlrange to [0.1, 0.9] and
    [-0.1, 1.1], respectively. Values smaller than 1 are useful for not hitting the
    limits; values larger than 1 are useful for maintaining control authority at the
    limits. This attribute is exclusive with ctrlrange and available only for joint and
    tendon transmissions which have range defined.

**Parent Elements**: [`actuator`](#actuator), [`default`](#default)

---

(velocity)=

#### `velocity`

This element creates a velocity servo. It is an actuator shortcut that configures a
general actuator with gaintype=fixed (gainprm=kv), biastype=affine (biasprm = [0, 0,
-kv]), and dyntype=none. The actuator produces a force proportional to the difference
between the reference velocity (ctrl) and the actual velocity.

```{note}
In order to create a PD controller, one has to define two actuators: a position servo and
 a velocity servo. This is because MJCF actuators are SISO (single-input single-output)
 while a PD controller takes two control inputs (reference position and reference velocity).
 When using this actuator, it is recommended to use the implicitfast or implicit integrators.
```

**Attributes:**

(velocity-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Element name.

(velocity-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Active defaults class for setting unspecified attributes.

(velocity-group)=

-   **`group`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Integer group to which the actuator belongs. This attribute can be used for custom
    tags. It is also used by the visualizer to enable and disable the rendering of
    entire groups of actuators.

(velocity-ctrllimited)=

-   **`ctrllimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If true, the control input to this actuator is automatically clamped to ctrlrange
    at runtime. If false, control input clamping is disabled. If \"auto\" and autolimits
    is set in compiler, control clamping will automatically be set to true if ctrlrange
    is defined without explicitly setting this attribute to \"true\". Note that control
    input clamping can also be globally disabled with the clampctrl attribute of
    option/flag.

(velocity-forcelimited)=

-   **`forcelimited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If true, the force output of this actuator is automatically clamped to forcerange
    at runtime. If false, force clamping is disabled. If \"auto\" and autolimits is set
    in compiler, force clamping will automatically be set to true if forcerange is
    defined without explicitly setting this attribute to \"true\".

(velocity-ctrlrange)=

-   **`ctrlrange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping the control input. The first value must be smaller than the
    second value. Setting this attribute without specifying ctrllimited is an error if
    autolimits is \"false\" in compiler.

(velocity-forcerange)=

-   **`forcerange`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range for clamping the force output. The first value must be no greater than the
    second value. Setting this attribute without specifying forcelimited is an error if
    autolimits is \"false\" in compiler.

(velocity-gear)=

-   **`gear`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `1. 0. 0. 0. 0. 0.` ]

    Scales the length (and consequently moment arms, velocity and force) of the
    actuator, for all transmission types. It is different from the gain in the force
    generation mechanism, because the gain only scales the force output and does not
    affect the length, moment arms and velocity. For actuators with scalar
    transmission, only the first element of this vector is used. The remaining
    elements are needed for joint, jointinparent and site transmissions where this
    attribute is used to specify 3D force and torque axes.

(velocity-joint)=

-   **`joint`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, the actuator acts on the given joint. For hinge and slide joints,
    the actuator length equals the joint position/angle times the first element of
    gear. For ball joints, the first three elements of gear define a 3D rotation axis
    in the child frame around which the actuator produces torque. For free joints,
    gear defines a 3D translation axis in the world frame followed by a 3D rotation
    axis in the child frame.

(velocity-tendon)=

-   **`tendon`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    If specified, the actuator acts on the given tendon. The actuator length equals
    the tendon length times the gear ratio. Both spatial and fixed tendons can be
    used.

(velocity-kv)=

-   **`kv`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `1.0` ]

    Velocity feedback gain. Used internally as gainprm[0] and also negated into
    biasprm[2] to produce a damping force proportional to velocity.

**Parent Elements**: [`actuator`](#actuator), [`default`](#default)

---

(visual)=

### `visual`

Settings that affect the visualizer.

The settings here affect the visualizer, or more precisely the abstract phase of visualization
which yields a list of geometric entities for subsequent rendering. The settings here are
global, in contrast with the element-specific visual settings. The global and element-specific
settings refer to non-overlapping properties. Some of the global settings affect properties such
as triangulation of geometric primitives that cannot be set per element. Other global settings
affect the properties of decorative objects, i.e., objects such as contact points and force
arrows which do not correspond to model elements. The visual settings are grouped semantically
into several subsections.

This element is a good candidate for the file include mechanism. One can create an XML file
with coordinated visual settings corresponding to a \"theme\", and then include this file in
multiple models.

**Parent Elements**: [`mujoco`](#mujoco)

**Child Elements**: [`headlight`](#headlight), [`global`](#global), [`map`](#map), [`rgba`](#rgba), [`probe`](#probe), [`ssao`](#ssao), [`tonemapping`](#tonemapping)

---

(headlight)=

#### `headlight`

Properties of the headlight used during visualization.

There is always a built-in headlight, in addition to any lights explicitly defined in the
model. The headlight is a directional light centered at the current camera and pointed in
the direction in which the camera is looking. It does not cast shadows (which would be
invisible anyway).

```{note}
Lights are additive, so if explicit lights are defined in the model, the intensity of the
 headlight would normally need to be reduced.
```

**Attributes:**

(headlight-ambient)=

-   **`ambient`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    The ambient component of the headlight, in the sense of OpenGL. The alpha component is
    set to 1 and cannot be adjusted.

(headlight-diffuse)=

-   **`diffuse`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    The diffuse component of the headlight, in the sense of OpenGL.

(headlight-specular)=

-   **`specular`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    The specular component of the headlight, in the sense of OpenGL.

(headlight-active)=

-   **`active`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Enables or disables the headlight. A value of 0 means disabled; any other value means
    enabled.

**Parent Elements**: [`visual`](#visual)

---

(global)=

#### `global`

Miscellaneous global settings for the visualizer.

While all visual settings are global, the settings here could not be fit into any of the
other subsections. So this is effectively a miscellaneous subsection.

**Attributes:**

(global-orthographic)=

-   **`orthographic`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `false` ]

    Whether the free camera uses a perspective projection (false) or an orthographic
    projection (true). Setting this attribute changes the semantic of the fovy attribute.

(global-fovy)=

-   **`fovy`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The vertical field of view of the free camera, i.e., the camera that is always available
    in the visualizer even if no cameras are explicitly defined in the model. If the camera
    uses a perspective projection, the field-of-view is expressed in degrees, regardless of
    the global compiler/angle setting. If the camera uses an orthographic projection, the
    field-of-view is expressed in units of length. In either case, the horizontal field of
    view is computed automatically given the window size and the vertical field of view.

(global-azimuth)=

-   **`azimuth`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The initial azimuth of the free camera around the vertical z-axis, in degrees. A value
    of 0 corresponds to looking in the positive x direction, while the value of 90
    corresponds to looking in the positive y direction. The look-at point itself is specified
    by the statistic/center attribute, while the distance from the look-at point is
    controlled by the statistic/extent attribute.

(global-elevation)=

-   **`elevation`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The initial elevation of the free camera with respect to the lookat point. Since this is
    a rotation around a vector parallel to the camera's X-axis (right in pixel space),
    negative numbers correspond to moving the camera up from the horizontal plane, and
    vice-versa. The look-at point itself is specified by the statistic/center attribute,
    while the distance from the look-at point is controlled by the statistic/extent
    attribute.

**Parent Elements**: [`visual`](#visual)

---

(map)=

#### `map`

Scaling quantities and fog settings that affect both visualization and built-in mouse
perturbations.

This element is used to specify scaling quantities that affect both the visualization and
built-in mouse perturbations. Unlike the scaling quantities in the scale element which are
specific to spatial extent, the quantities here are miscellaneous.

**Attributes:**

(map-fogstart)=

-   **`fogstart`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The start position of the linear fog, as a multiplier of the model extent. The visualizer
    can simulate linear fog, in the sense of OpenGL. The start position of the fog is the
    model extent multiplied by the value of this attribute.

(map-fogend)=

-   **`fogend`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The end position of the linear fog, as a multiplier of the model extent. The end position
    of the fog is the model extent multiplied by the value of this attribute.

(map-znear)=

-   **`znear`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The distance to the near clipping plane as a multiplier of the model extent. Setting it
    too close causes loss of resolution in the depth buffer, while setting it too far causes
    objects of interest to be clipped. Must be strictly positive.

(map-zfar)=

-   **`zfar`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The distance to the far clipping plane as a multiplier of the model extent.

<div class="motphys-extension-block">
<div class="motphys-extension-label">MPEX</div>

(map-envmapintensity)=

-   **`envmapintensity`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Intensity of the environment map.

</div>

**Parent Elements**: [`visual`](#visual)

---

(rgba)=

#### `rgba`

Color and transparency settings for various decorative objects in the visualizer.

The settings in this element control the color and transparency (rgba) of various decorative
objects. All values should be in the range [0 1]. An alpha value of 0 disables the rendering
of the corresponding object.

**Attributes:**

(rgba-fog)=

-   **`fog`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    When fog is enabled, the color of all pixels fades towards the color specified here. The
    spatial extent of the fading is controlled by the fogstart and fogend attributes of the
    map element.

(rgba-haze)=

-   **`haze`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Haze color at the horizon, used to transition between an infinite plane and a skybox
    smoothly. To create a seamless transition, make sure the skybox colors near the horizon
    are similar to the plane color/texture, and set the haze color somewhere in that color
    gamut.

(rgba-joint)=

-   **`joint`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    Color of the arrows used to render joint axes. If a joint is limited and the joint value
    exceeds the limit, the constraint impedance is used to mix this color and the constraint
    color.

(rgba-bv)=

-   **`bv`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    Color used to render bounding volumes.

(rgba-contactforce)=

-   **`contactforce`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    Color of the arrows used to render contact forces. When splitting of contact forces into
    normal and tangential components is enabled, this color is used to render the normal
    components.

**Parent Elements**: [`visual`](#visual)

---

(probe)=

#### `probe` <span class="badge mpex">MPEX</span>

<div class="motphys-extension-block">

Reflection probe settings.

Defines an image-based lighting probe used for reflections in the visualizer.

**Attributes:**

(probe-texture)=

-   **`texture`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Texture asset name used as the reflection source for this probe.

(probe-position)=

-   **`position`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 0.0` ]

    Position of the probe in world space.

(probe-scale)=

-   **`scale`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `1.0 1.0 1.0` ]

    Scale of the probe's influence volume.

**Parent Elements**: [`visual`](#visual)

</div>

---

(ssao)=

#### `ssao` <span class="badge mpex">MPEX</span>

<div class="motphys-extension-block">

Screen-space ambient occlusion (SSAO) settings.

Controls SSAO post-processing effect in the visualizer.

**Attributes:**

(ssao-active)=

-   **`active`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `false` ]

    Whether SSAO post-processing is active.

**Parent Elements**: [`visual`](#visual)

</div>

---

(tonemapping)=

#### `tonemapping` <span class="badge mpex">MPEX</span>

<div class="motphys-extension-block">

Tonemapping settings.

Controls the tonemapping method applied during rendering.

**Attributes:**

(tonemapping-method)=

-   **`method`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `none` ]

    **Choice:** [ `none` | `aces` ]

    The tonemapping method to apply during rendering.

**Parent Elements**: [`visual`](#visual)

</div>

---

(equality)=

### `equality`

This is a grouping element for equality constraints. It does not have attributes. Several
attributes are common to all equality constraint types and are documented once under the connect
element.

**Parent Elements**: [`default`](#default), [`mujoco`](#mujoco)

**Child Elements**: [`connect`](#connect), [`joint`](#joint), [`weld`](#weld)

---

(connect)=

#### `connect`

This element creates an equality constraint that connects two bodies at a point. The
constraint effectively defines a ball joint outside the kinematic tree.

Connect constraints can be specified in one of two ways. The first uses body1 and anchor
(both required) and optionally body2; when using this specification the constraint is
assumed to be satisfied at the configuration in which the model is defined.
The second uses site1 and site2 (both required); when using this specification the two
sites will be pulled together by the constraint regardless of their position in the default
configuration.

```{note}
The body-based and site-based specifications are mutually exclusive and cannot be combined.
```

**Attributes:**

(connect-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the equality constraint.

(connect-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

(connect-active)=

-   **`active`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `true` ]

    If this attribute is set to \"true\", the constraint is active and the constraint
    solver will try to enforce it. This value is used to initialize the runtime constraint activation state, which is user-settable at
    runtime.

(connect-solref)=

-   **`solref`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    Solver reference parameters for equality constraints.
    → See [solver parameters](#solver-attrs-solref).

(connect-solimp)=

-   **`solimp`** [ <span class="badge array">real(5)</span> | <span class="badge required">Required</span> | **Default:** `0.9 0.95 0.001 0.5 2.0` ]

    Solver impedance parameters for equality constraints.
    → See [solver parameters](#solver-attrs-solimp).

(connect-body1)=

-   **`body1`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the first body participating in the constraint. Either this attribute and
    anchor must be specified, or site1 and site2 must be specified.

(connect-body2)=

-   **`body2`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the second body participating in the constraint. If this attribute is omitted,
    the second body is the world body.

(connect-anchor)=

-   **`anchor`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Coordinates of the 3D anchor point where the two bodies are connected, in the local
    coordinate frame of body1. The constraint is assumed to be satisfied in the
    configuration at which the model is defined, which lets the compiler
    compute the associated anchor point for body2.

(connect-site1)=

-   **`site1`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of a site belonging to the first body participating in the constraint. When
    specified, site2 must also be specified. The (site1, site2) specification is a more
    flexible alternative to the body-based specification: the sites are not required to
    overlap at the default configuration (if they do not overlap they will snap together
    at the beginning of the simulation), and changing the site positions at runtime will
    correctly change the position of the constraint.

(connect-site2)=

-   **`site2`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of a site belonging to the second body participating in the constraint. When
    specified, site1 must also be specified. See the site1 description for more details.

**Parent Elements**: [`equality`](#equality)

---

(joint-equality)=

#### `joint`

This element constrains the position or angle of one joint to be a quartic polynomial of
another joint. Only scalar joint types (slide and hinge) can be used.

If joint values of joint1 and joint2 are respectively y and x, and their reference
positions (corresponding to the joint values in the initial model configuration) are y0
and x0, the constraint enforced is:
y - y0 = a0 + a1*(x - x0) + a2*(x - x0)^2 + a3*(x - x0)^3 + a4*(x - x0)^4

```{note}
Omitting joint2 is equivalent to setting x = x0, in which case the constraint reduces to
 y = y0 + a0.
```

**Attributes:**

(joint-equality-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the equality constraint.

(joint-equality-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

(joint-equality-active)=

-   **`active`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `true` ]

    If this attribute is set to \"true\", the constraint is active and the constraint
    solver will try to enforce it. This value is used to initialize the runtime constraint activation state, which is user-settable at
    runtime.

(joint-equality-solref)=

-   **`solref`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    Solver reference parameters for equality constraints.
    → See [solver parameters](#solver-attrs-solref).

(joint-equality-solimp)=

-   **`solimp`** [ <span class="badge array">real(5)</span> | <span class="badge required">Required</span> | **Default:** `0.9 0.95 0.001 0.5 2.0` ]

    Solver impedance parameters for equality constraints.
    → See [solver parameters](#solver-attrs-solimp).

(joint-equality-joint1)=

-   **`joint1`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    Name of the first joint.

(joint-equality-joint2)=

-   **`joint2`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the second joint. If this attribute is omitted, the first joint is fixed to a
    constant.

(joint-equality-polycoef)=

-   **`polycoef`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    Coefficients a0 through a4 of the quartic polynomial relating the positions of joint1
    and joint2. If the joint values of joint1 and joint2 are respectively y and x, and
    their reference positions are y0 and x0, the constraint is:
    y - y0 = a0 + a1*(x - x0) + a2*(x - x0)^2 + a3*(x - x0)^3 + a4*(x - x0)^4.

**Parent Elements**: [`(world)body`](<#(world)body>), [`default`](#default), [`equality`](#equality), [`fixed`](#fixed)

---

(weld)=

#### `weld`

This element creates a weld equality constraint. It attaches two bodies to each other,
removing all relative degrees of freedom between them via the constraint solver. The two
bodies are not required to be close to each other. The relative body position and
orientation being enforced by the constraint solver is the one in which the model was
defined.

Weld constraints can be specified in one of two ways. The first uses body1 (and optionally
anchor, relpose, body2); when using this specification the constraint is assumed to be
satisfied at the configuration in which the model is defined. The second uses site1 and
site2 (both required); when using this specification the frames of the two sites will be
aligned by the constraint regardless of their position in the default configuration.

```{note}
Two bodies can also be welded together rigidly by defining one body as a child of the
 other body without any joint elements in the child body. The weld equality constraint
 provides a soft (constraint-based) alternative. The body-based and site-based
 specifications are mutually exclusive and cannot be combined. Welding a body to the world
 and toggling the constraint activation state at runtime can be used to fix a body temporarily.
```

**Attributes:**

(weld-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the equality constraint.

(weld-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

(weld-active)=

-   **`active`** [ <span class="badge bool">bool</span> | <span class="badge required">Required</span> | **Default:** `true` ]

    If this attribute is set to \"true\", the constraint is active and the constraint
    solver will try to enforce it. This value is used to initialize the runtime constraint activation state, which is user-settable at
    runtime.

(weld-solref)=

-   **`solref`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    Solver reference parameters for equality constraints.
    → See [solver parameters](#solver-attrs-solref).

(weld-solimp)=

-   **`solimp`** [ <span class="badge array">real(5)</span> | <span class="badge required">Required</span> | **Default:** `0.9 0.95 0.001 0.5 2.0` ]

    Solver impedance parameters for equality constraints.
    → See [solver parameters](#solver-attrs-solimp).

(weld-body1)=

-   **`body1`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the first body participating in the constraint. Either this attribute must be
    specified or site1 and site2 must be specified.

(weld-body2)=

-   **`body2`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the second body. If this attribute is omitted, the second body is the world
    body. Welding a body to the world and changing the corresponding component of
    the runtime constraint activation state can be used to fix the body temporarily.

(weld-anchor)=

-   **`anchor`** [ <span class="badge array">real(3)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0 0.0` ]

    Coordinates of the weld point relative to body2. If relpose is not specified, the
    meaning of this parameter is the same as for connect constraints except that it is
    relative to body2. If relpose is specified, body1 will use the pose to compute its
    anchor point.

(weld-site1)=

-   **`site1`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of a site belonging to the first body participating in the constraint. When
    specified, site2 must also be specified. The (site1, site2) specification is a more
    flexible alternative to the body-based specification: the sites are not required to
    overlap at the default configuration (if they do not, the sites will snap together
    at the beginning of the simulation), and changing the site position and orientation at
    runtime will correctly change the position and orientation of the constraint. Note that torquescale still takes effect even when
    using the site-based specification.

(weld-site2)=

-   **`site2`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of a site belonging to the second body participating in the constraint. When
    specified, site1 must also be specified. See the site1 description for more details.

(weld-relpose)=

-   **`relpose`** [ <span class="badge array">real(7)</span> | <span class="badge required">Required</span> | **Default:** `0.0 1.0 0.0 0.0 0.0 0.0 0.0` ]

    This attribute specifies the relative pose (3D position followed by 4D quaternion
    orientation) of body2 relative to body1. If the quaternion part (the last 4
    components) are all zeros, as in the default setting, this attribute is ignored and
    the relative pose is the one corresponding to the model reference pose in qpos0.

(weld-torquescale)=

-   **`torquescale`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `1.0` ]

    A constant that scales the angular residual (angular constraint violation). Intuitively
    this coefficient defines how much the weld cares about rotational displacements versus
    translational displacements. Setting this value to 0 makes the weld behave like a
    connect constraint. This value has units of length and can be understood as the
    diameter of a flat patch of glue sticking the two bodies together.

**Parent Elements**: [`equality`](#equality)

---

(contact-contact)=

### `contact`

This is a grouping element that groups elements used to adjust the generation of candidate
contact pairs for collision checking. It does not have any attributes of its own.

**Parent Elements**: [`mujoco`](#mujoco), [`sensor`](#sensor)

**Child Elements**: [`exclude`](#exclude), [`pair`](#pair)

---

(exclude)=

#### `exclude`

This element is used to exclude a pair of bodies from collision checking.

Unlike all other contact-related elements which refer to geoms, this element refers to bodies.
Experience has shown that exclusion is more useful on the level of bodies. Collisions between
any geom defined in the first body and any geom defined in the second body are excluded.

**Attributes:**

(exclude-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of this exclude pair.

(exclude-body1)=

-   **`body1`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the first body in the pair.

(exclude-body2)=

-   **`body2`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the second body in the pair.

**Parent Elements**: [`contact`](#contact)

---

(pair)=

#### `pair`

This element creates a predefined geom pair which will be checked for collision.

Unlike dynamically generated pairs whose properties are inferred from the corresponding geom
properties, the pairs created here specify all their properties explicitly or through defaults,
and the properties of the individual geoms are not used. Anisotropic friction can only be
created with this element.

**Attributes:**

(pair-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of this contact pair.

(pair-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

(pair-geom1)=

-   **`geom1`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the first geom in the pair.

(pair-geom2)=

-   **`geom2`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the second geom in the pair. The contact force vector computed by the solver
    points from the first towards the second geom by convention.
    The forces applied to the system are of course equal and opposite, so the order of geoms
    does not affect the physics.

(pair-condim)=

-   **`condim`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `3` ]

    The dimensionality of the contacts generated by this geom pair.

(pair-friction)=

-   **`friction`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `1.0 1.0 0.005 0.0001 0.0001` ]

    The friction coefficients of the contacts generated by this geom pair. Making the first two
    coefficients different results in anisotropic tangential friction. Making the last two
    coefficients different results in anisotropic rolling friction. The length of this array is
    not enforced by the parser, and can be smaller than 5. This is because some of the
    coefficients may not be used, depending on the contact dimensionality. Unspecified
    coefficients remain equal to their defaults.

(pair-solref)=

-   **`solref`** [ <span class="badge array">real(2)</span> | <span class="badge required">Required</span> | **Default:** `0.02 1.0` ]

    Solver reference parameters for contact simulation.
    → See [solver parameters](#solver-attrs-solref).

(pair-solreffriction)=

-   **`solreffriction`** [ <span class="badge array">real(2)</span> | <span class="badge required">Required</span> | **Default:** `0.0 0.0` ]

    Solver reference parameters for friction dimensions. This attribute has the same semantics
    as other solref attributes, with two important distinctions: the default value of \"0 0\"
    means \"use the same values as solref\", and this attribute only takes effect for elliptic
    friction cones, since pyramidal cones mix normal and frictional forces.
    → See [solver parameters](#solver-attrs-solref).

(pair-margin)=

-   **`margin`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Distance threshold below which contacts are detected and included in the global array
    the contact data.

(pair-gap)=

-   **`gap`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Used to enable the generation of inactive contacts, i.e., contacts that are ignored by the
    constraint solver but are included in the contact data for the purpose of custom
    computations. When this value is positive, geom distances between margin and margin-gap
    correspond to such inactive contacts.

**Parent Elements**: [`contact`](#contact)

---

(tendon)=

### `tendon`

Grouping element for tendon definitions.

Tendons can be used to impose length limits, simulate spring, damping and dry friction forces,
as well as attach actuators to them. When used in equality constraints, tendons can also
represent different forms of mechanical coupling.

**Parent Elements**: [`default`](#default), [`mujoco`](#mujoco)

**Child Elements**: [`fixed`](#fixed)

---

(fixed)=

#### `fixed`

Abstract tendon whose length is defined as a linear combination of joint positions.

The tendon length and its gradient are the only quantities needed for simulation. The
length is computed by multiplying the position or angle of each included joint by the
corresponding coefficient value and summing the results. The attributes of fixed tendons
are a subset of the attributes of spatial tendons and have the same meaning.

**Attributes:**

(fixed-group)=

-   **`group`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `0` ]

    Integer group to which the tendon belongs. This attribute can be used for custom
    tags. It is also used by the visualizer to enable and disable the rendering of
    entire groups of tendons.

(fixed-limited)=

-   **`limited`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `auto` ]

    **Choice:** [ `false` | `true` | `auto` ]

    If this attribute is \"true\", the length limits defined by the range attribute are
    imposed by the constraint solver. If this attribute is \"auto\", and autolimits is
    set in compiler, length limits will be enabled if range is defined.

(fixed-range)=

-   **`range`** [ <span class="badge array">real(2)</span> | <span class="badge optional">Optional</span> ]

    Range of allowed tendon lengths. Setting this attribute without specifying limited
    is an error, unless autolimits is set in compiler.

(fixed-solreflimit)=

-   **`solreflimit`** [ <span class="badge array">real(n)</span> | <span class="badge optional">Optional</span> ]

    Solver reference parameters for tendon limits.
    → See [solver parameters](#solver-attrs-solref).

(fixed-solimplimit)=

-   **`solimplimit`** [ <span class="badge array">real(5)</span> | <span class="badge required">Required</span> | **Default:** `0.9 0.95 0.001 0.5 2.0` ]

    Solver impedance parameters for tendon limits.
    → See [solver parameters](#solver-attrs-solimp).

(fixed-frictionloss)=

-   **`frictionloss`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Friction loss caused by dry friction. To enable friction loss, set this attribute
    to a positive value.

(fixed-solreffriction)=

-   **`solreffriction`** [ <span class="badge array">real(2)</span> | <span class="badge required">Required</span> | **Default:** `0.02 1.0` ]

    Solver reference parameters for tendon dry friction.
    → See [solver parameters](#solver-attrs-solref).

(fixed-solimpfriction)=

-   **`solimpfriction`** [ <span class="badge array">real(5)</span> | <span class="badge required">Required</span> | **Default:** `0.9 0.95 0.001 0.5 2.0` ]

    Solver impedance parameters for tendon dry friction.
    → See [solver parameters](#solver-attrs-solimp).

(fixed-margin)=

-   **`margin`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The limit constraint becomes active when the absolute value of the difference
    between the tendon length and either limit of the specified range falls below this
    margin. Similar to contacts, the margin parameter is subtracted from the difference
    between the range limit and the tendon length. The resulting constraint distance is
    always negative when the constraint is active.

(fixed-width)=

-   **`width`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.003` ]

    Radius of the cross-section area of the spatial tendon, used for rendering. Parts
    of the tendon that wrap around geom obstacles are rendered with reduced width.

(fixed-rgba)=

-   **`rgba`** [ <span class="badge array">real(4)</span> | <span class="badge required">Required</span> | **Default:** `0.5 0.5 0.5 1.` ]

    Color and transparency of the tendon. When this value is different from the
    internal default, it overrides the corresponding material properties. If a material
    is unspecified and rgba has the default value, limited tendons whose length exceeds
    the limit are recolored based on the constraint impedance.

(fixed-springlength)=

-   **`springlength`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    Spring resting position, can take either one or two values. If one value is given,
    it corresponds to the length of the tendon at rest. If it is -1, the tendon resting
    length is determined from the model reference configuration. If two non-decreasing
    values are given, they define a dead-band range: if the tendon length is between
    the two values the force is zero, and outside this range the force behaves like a
    regular spring with the rest-point corresponding to the nearest springlength value.

(fixed-stiffness)=

-   **`stiffness`** [ <span class="badge real">real</span> | <span class="badge optional">Optional</span> ]

    Stiffness coefficient. A positive value generates a spring force (linear in
    position) acting along the tendon.

(fixed-damping)=

-   **`damping`** [ <span class="badge real">real</span> | <span class="badge optional">Optional</span> ]

    Damping coefficient. A positive value generates a damping force (linear in
    velocity) acting along the tendon. Unlike joint damping which is integrated
    implicitly by the Euler method, tendon damping is not integrated implicitly, thus
    joint damping should be used if possible.

(fixed-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the tendon.

(fixed-class)=

-   **`class`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Defaults class for setting unspecified attributes.

**Parent Elements**: [`tendon`](#tendon)

**Child Elements**: [`joint`](#joint)

---

(joint-tendon)=

##### `joint`

A joint contributing to the length computation of a fixed tendon.

This element adds a joint to the computation of the fixed tendon length. The position or angle
of each included joint is multiplied by the corresponding coef value, and added up to obtain
the tendon length.

**Attributes:**

(joint-tendon-joint)=

-   **`joint`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    Name of the joint to be added to the fixed tendon. Only scalar joints (slide and hinge)
    can be referenced here.

(joint-tendon-coef)=

-   **`coef`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    Scalar coefficient multiplying the position or angle of the specified joint.

**Parent Elements**: [`(world)body`](<#(world)body>), [`default`](#default), [`equality`](#equality), [`fixed`](#fixed)

---

(custom)=

### `custom`

This element is used to add custom numeric and text data to the model.

**Parent Elements**: [`mujoco`](#mujoco)

**Child Elements**: [`numeric`](#numeric), [`text`](#text)

---

(numeric)=

#### `numeric`

A custom numeric array.

**Attributes:**

(numeric-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    Name of the custom array.

(numeric-size)=

-   **`size`** [ <span class="badge int">int</span> | <span class="badge optional">Optional</span> ]

    Size of the array.

(numeric-data)=

-   **`data`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    Array data.

**Parent Elements**: [`custom`](#custom)

---

(text)=

#### `text`

A custom text field.

**Attributes:**

(text-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    Name of the custom text.

(text-data)=

-   **`data`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    Text data.

**Parent Elements**: [`custom`](#custom)

---

(sensor)=

### `sensor`

This element is a grouping element for sensors.

**Parent Elements**: [`mujoco`](#mujoco)

**Child Elements**: [`touch`](#touch), [`accelerometer`](#accelerometer), [`velocimeter`](#velocimeter), [`gyro`](#gyro), `force`, `torque`, [`jointpos`](#jointpos), [`jointvel`](#jointvel), `jointactuatorfrc`, `ballquat`, `ballangvel`, `jointlimitpos`, `jointlimitvel`, `jointlimitfrc`, `tendonpos`, `tendonvel`, `tendonlimitpos`, `tendonlimitvel`, `tendonlimitfrc`, `actuatorpos`, `actuatorvel`, `actuatorfrc`, [`framepos`](#framepos), [`framequat`](#framequat), [`framexaxis`](#framexaxis), [`frameyaxis`](#frameyaxis), [`framezaxis`](#framezaxis), [`framelinvel`](#framelinvel), [`frameangvel`](#frameangvel), `framelinacc`, `frameangacc`, [`subtreecom`](#subtreecom), [`subtreelinvel`](#subtreelinvel), [`subtreeangmom`](#subtreeangmom), `distance`, `normal`, `fromto`, [`contact`](#contact)

---

(touch)=

#### `touch`

Common sensor data for sensors that attach to a site.

This type is shared by site-based sensors such as touch, accelerometer, velocimeter,
gyro, force, torque, and magnetometer. The active sensing zone or measurement origin
is defined by the named site, and the sensor uses the site's position and orientation.

**Attributes:**

(touch-site)=

-   **`site`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the site where the sensor is mounted. The sensor is centered and aligned
    with the site local frame.

(touch-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(touch-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(touch-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(touch-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(accelerometer)=

#### `accelerometer`

Common sensor data for sensors that attach to a site.

This type is shared by site-based sensors such as touch, accelerometer, velocimeter,
gyro, force, torque, and magnetometer. The active sensing zone or measurement origin
is defined by the named site, and the sensor uses the site's position and orientation.

**Attributes:**

(accelerometer-site)=

-   **`site`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the site where the sensor is mounted. The sensor is centered and aligned
    with the site local frame.

(accelerometer-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(accelerometer-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(accelerometer-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(accelerometer-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(velocimeter)=

#### `velocimeter`

Common sensor data for sensors that attach to a site.

This type is shared by site-based sensors such as touch, accelerometer, velocimeter,
gyro, force, torque, and magnetometer. The active sensing zone or measurement origin
is defined by the named site, and the sensor uses the site's position and orientation.

**Attributes:**

(velocimeter-site)=

-   **`site`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the site where the sensor is mounted. The sensor is centered and aligned
    with the site local frame.

(velocimeter-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(velocimeter-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(velocimeter-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(velocimeter-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(gyro)=

#### `gyro`

Common sensor data for sensors that attach to a site.

This type is shared by site-based sensors such as touch, accelerometer, velocimeter,
gyro, force, torque, and magnetometer. The active sensing zone or measurement origin
is defined by the named site, and the sensor uses the site's position and orientation.

**Attributes:**

(gyro-site)=

-   **`site`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the site where the sensor is mounted. The sensor is centered and aligned
    with the site local frame.

(gyro-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(gyro-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(gyro-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(gyro-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(jointpos)=

#### `jointpos`

Common sensor data for sensors that attach to a scalar joint.

This type is shared by joint-based sensors such as jointpos, jointvel, ballquat,
ballangvel, jointlimitpos, jointlimitvel, jointlimitfrc, and jointactuatorfrc. Only
scalar joints (slide or hinge) can be referenced by most of these sensors; ball joints
are used by ballquat and ballangvel.

**Attributes:**

(jointpos-joint)=

-   **`joint`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the joint to which the sensor is attached. For most joint sensors only
    scalar joints (slide or hinge) can be referenced; for ballquat and ballangvel the
    referenced joint must be a ball joint.

(jointpos-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(jointpos-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(jointpos-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(jointpos-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(jointvel)=

#### `jointvel`

Common sensor data for sensors that attach to a scalar joint.

This type is shared by joint-based sensors such as jointpos, jointvel, ballquat,
ballangvel, jointlimitpos, jointlimitvel, jointlimitfrc, and jointactuatorfrc. Only
scalar joints (slide or hinge) can be referenced by most of these sensors; ball joints
are used by ballquat and ballangvel.

**Attributes:**

(jointvel-joint)=

-   **`joint`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the joint to which the sensor is attached. For most joint sensors only
    scalar joints (slide or hinge) can be referenced; for ballquat and ballangvel the
    referenced joint must be a ball joint.

(jointvel-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(jointvel-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(jointvel-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(jointvel-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(framepos)=

#### `framepos`

Common sensor data for sensors that track a spatial coordinate frame.

This type is shared by frame-based sensors such as framepos, framequat, framexaxis,
frameyaxis, framezaxis, framelinvel, and frameangvel. The sensor reports properties
of the spatial frame of the specified object, either in global coordinates or
optionally with respect to a given frame-of-reference.

```{note}
Both `ref_type` and `ref_name` must be set together; providing one without the other
 is invalid. If neither is given, the sensor values are measured with respect to the
 global frame.
```

**Attributes:**

(framepos-objtype)=

-   **`objtype`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `body` ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the sensor is attached. This must be an object type
    that has a spatial frame. \"body\" refers to the inertial frame of the body, while
    \"xbody\" refers to the regular frame of the body (usually centered at the joint
    with the parent body).

(framepos-objname)=

-   **`objname`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the object to which the sensor is attached.

(framepos-reftype)=

-   **`reftype`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the frame-of-reference is attached. The semantics are
    identical to the objtype attribute. If reftype and refname are both given, the
    sensor values will be measured with respect to this frame.

(framepos-refname)=

-   **`refname`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    The name of the object to which the frame-of-reference is attached. If reftype and
    refname are both given, the sensor values will be measured with respect to the
    frame defined by this object.

(framepos-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(framepos-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(framepos-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(framepos-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(framequat)=

#### `framequat`

Common sensor data for sensors that track a spatial coordinate frame.

This type is shared by frame-based sensors such as framepos, framequat, framexaxis,
frameyaxis, framezaxis, framelinvel, and frameangvel. The sensor reports properties
of the spatial frame of the specified object, either in global coordinates or
optionally with respect to a given frame-of-reference.

```{note}
Both `ref_type` and `ref_name` must be set together; providing one without the other
 is invalid. If neither is given, the sensor values are measured with respect to the
 global frame.
```

**Attributes:**

(framequat-objtype)=

-   **`objtype`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `body` ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the sensor is attached. This must be an object type
    that has a spatial frame. \"body\" refers to the inertial frame of the body, while
    \"xbody\" refers to the regular frame of the body (usually centered at the joint
    with the parent body).

(framequat-objname)=

-   **`objname`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the object to which the sensor is attached.

(framequat-reftype)=

-   **`reftype`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the frame-of-reference is attached. The semantics are
    identical to the objtype attribute. If reftype and refname are both given, the
    sensor values will be measured with respect to this frame.

(framequat-refname)=

-   **`refname`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    The name of the object to which the frame-of-reference is attached. If reftype and
    refname are both given, the sensor values will be measured with respect to the
    frame defined by this object.

(framequat-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(framequat-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(framequat-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(framequat-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(framexaxis)=

#### `framexaxis`

Common sensor data for sensors that track a spatial coordinate frame.

This type is shared by frame-based sensors such as framepos, framequat, framexaxis,
frameyaxis, framezaxis, framelinvel, and frameangvel. The sensor reports properties
of the spatial frame of the specified object, either in global coordinates or
optionally with respect to a given frame-of-reference.

```{note}
Both `ref_type` and `ref_name` must be set together; providing one without the other
 is invalid. If neither is given, the sensor values are measured with respect to the
 global frame.
```

**Attributes:**

(framexaxis-objtype)=

-   **`objtype`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `body` ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the sensor is attached. This must be an object type
    that has a spatial frame. \"body\" refers to the inertial frame of the body, while
    \"xbody\" refers to the regular frame of the body (usually centered at the joint
    with the parent body).

(framexaxis-objname)=

-   **`objname`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the object to which the sensor is attached.

(framexaxis-reftype)=

-   **`reftype`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the frame-of-reference is attached. The semantics are
    identical to the objtype attribute. If reftype and refname are both given, the
    sensor values will be measured with respect to this frame.

(framexaxis-refname)=

-   **`refname`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    The name of the object to which the frame-of-reference is attached. If reftype and
    refname are both given, the sensor values will be measured with respect to the
    frame defined by this object.

(framexaxis-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(framexaxis-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(framexaxis-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(framexaxis-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(frameyaxis)=

#### `frameyaxis`

Common sensor data for sensors that track a spatial coordinate frame.

This type is shared by frame-based sensors such as framepos, framequat, framexaxis,
frameyaxis, framezaxis, framelinvel, and frameangvel. The sensor reports properties
of the spatial frame of the specified object, either in global coordinates or
optionally with respect to a given frame-of-reference.

```{note}
Both `ref_type` and `ref_name` must be set together; providing one without the other
 is invalid. If neither is given, the sensor values are measured with respect to the
 global frame.
```

**Attributes:**

(frameyaxis-objtype)=

-   **`objtype`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `body` ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the sensor is attached. This must be an object type
    that has a spatial frame. \"body\" refers to the inertial frame of the body, while
    \"xbody\" refers to the regular frame of the body (usually centered at the joint
    with the parent body).

(frameyaxis-objname)=

-   **`objname`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the object to which the sensor is attached.

(frameyaxis-reftype)=

-   **`reftype`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the frame-of-reference is attached. The semantics are
    identical to the objtype attribute. If reftype and refname are both given, the
    sensor values will be measured with respect to this frame.

(frameyaxis-refname)=

-   **`refname`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    The name of the object to which the frame-of-reference is attached. If reftype and
    refname are both given, the sensor values will be measured with respect to the
    frame defined by this object.

(frameyaxis-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(frameyaxis-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(frameyaxis-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(frameyaxis-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(framezaxis)=

#### `framezaxis`

Common sensor data for sensors that track a spatial coordinate frame.

This type is shared by frame-based sensors such as framepos, framequat, framexaxis,
frameyaxis, framezaxis, framelinvel, and frameangvel. The sensor reports properties
of the spatial frame of the specified object, either in global coordinates or
optionally with respect to a given frame-of-reference.

```{note}
Both `ref_type` and `ref_name` must be set together; providing one without the other
 is invalid. If neither is given, the sensor values are measured with respect to the
 global frame.
```

**Attributes:**

(framezaxis-objtype)=

-   **`objtype`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `body` ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the sensor is attached. This must be an object type
    that has a spatial frame. \"body\" refers to the inertial frame of the body, while
    \"xbody\" refers to the regular frame of the body (usually centered at the joint
    with the parent body).

(framezaxis-objname)=

-   **`objname`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the object to which the sensor is attached.

(framezaxis-reftype)=

-   **`reftype`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the frame-of-reference is attached. The semantics are
    identical to the objtype attribute. If reftype and refname are both given, the
    sensor values will be measured with respect to this frame.

(framezaxis-refname)=

-   **`refname`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    The name of the object to which the frame-of-reference is attached. If reftype and
    refname are both given, the sensor values will be measured with respect to the
    frame defined by this object.

(framezaxis-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(framezaxis-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(framezaxis-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(framezaxis-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(framelinvel)=

#### `framelinvel`

Common sensor data for sensors that track a spatial coordinate frame.

This type is shared by frame-based sensors such as framepos, framequat, framexaxis,
frameyaxis, framezaxis, framelinvel, and frameangvel. The sensor reports properties
of the spatial frame of the specified object, either in global coordinates or
optionally with respect to a given frame-of-reference.

```{note}
Both `ref_type` and `ref_name` must be set together; providing one without the other
 is invalid. If neither is given, the sensor values are measured with respect to the
 global frame.
```

**Attributes:**

(framelinvel-objtype)=

-   **`objtype`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `body` ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the sensor is attached. This must be an object type
    that has a spatial frame. \"body\" refers to the inertial frame of the body, while
    \"xbody\" refers to the regular frame of the body (usually centered at the joint
    with the parent body).

(framelinvel-objname)=

-   **`objname`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the object to which the sensor is attached.

(framelinvel-reftype)=

-   **`reftype`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the frame-of-reference is attached. The semantics are
    identical to the objtype attribute. If reftype and refname are both given, the
    sensor values will be measured with respect to this frame.

(framelinvel-refname)=

-   **`refname`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    The name of the object to which the frame-of-reference is attached. If reftype and
    refname are both given, the sensor values will be measured with respect to the
    frame defined by this object.

(framelinvel-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(framelinvel-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(framelinvel-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(framelinvel-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(frameangvel)=

#### `frameangvel`

Common sensor data for sensors that track a spatial coordinate frame.

This type is shared by frame-based sensors such as framepos, framequat, framexaxis,
frameyaxis, framezaxis, framelinvel, and frameangvel. The sensor reports properties
of the spatial frame of the specified object, either in global coordinates or
optionally with respect to a given frame-of-reference.

```{note}
Both `ref_type` and `ref_name` must be set together; providing one without the other
 is invalid. If neither is given, the sensor values are measured with respect to the
 global frame.
```

**Attributes:**

(frameangvel-objtype)=

-   **`objtype`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `body` ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the sensor is attached. This must be an object type
    that has a spatial frame. \"body\" refers to the inertial frame of the body, while
    \"xbody\" refers to the regular frame of the body (usually centered at the joint
    with the parent body).

(frameangvel-objname)=

-   **`objname`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the object to which the sensor is attached.

(frameangvel-reftype)=

-   **`reftype`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    **Choice:** [ `body` | `xbody` | `geom` | `site` | `camera` ]

    The type of object to which the frame-of-reference is attached. The semantics are
    identical to the objtype attribute. If reftype and refname are both given, the
    sensor values will be measured with respect to this frame.

(frameangvel-refname)=

-   **`refname`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    The name of the object to which the frame-of-reference is attached. If reftype and
    refname are both given, the sensor values will be measured with respect to the
    frame defined by this object.

(frameangvel-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(frameangvel-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(frameangvel-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(frameangvel-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(subtreecom)=

#### `subtreecom`

Common sensor data for sensors that are rooted at a body.

This type is shared by body-rooted sensors such as subtreecom, subtreelinvel, and
subtreeangmom. These sensors return properties of the kinematic subtree rooted at
the specified body, computed in global coordinates.

**Attributes:**

(subtreecom-body)=

-   **`body`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the body where the kinematic subtree is rooted.

(subtreecom-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(subtreecom-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(subtreecom-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(subtreecom-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(subtreelinvel)=

#### `subtreelinvel`

Common sensor data for sensors that are rooted at a body.

This type is shared by body-rooted sensors such as subtreecom, subtreelinvel, and
subtreeangmom. These sensors return properties of the kinematic subtree rooted at
the specified body, computed in global coordinates.

**Attributes:**

(subtreelinvel-body)=

-   **`body`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the body where the kinematic subtree is rooted.

(subtreelinvel-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(subtreelinvel-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(subtreelinvel-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(subtreelinvel-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(subtreeangmom)=

#### `subtreeangmom`

Common sensor data for sensors that are rooted at a body.

This type is shared by body-rooted sensors such as subtreecom, subtreelinvel, and
subtreeangmom. These sensors return properties of the kinematic subtree rooted at
the specified body, computed in global coordinates.

**Attributes:**

(subtreeangmom-body)=

-   **`body`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `""` ]

    The name of the body where the kinematic subtree is rooted.

(subtreeangmom-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(subtreeangmom-noise)=

-   **`noise`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The standard deviation of zero-mean Gaussian noise added to the sensor output. Noise
    is added in the same units as the sensor output.

(subtreeangmom-cutoff)=

-   **`cutoff`** [ <span class="badge real">real</span> | <span class="badge required">Required</span> | **Default:** `0.0` ]

    The cutoff value for the sensor output. If the sensor output exceeds this value in
    absolute terms, it is clipped to this value.

(subtreeangmom-user)=

-   **`user`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `` ]

    User-defined scalar data associated with the sensor. These values are not used by
    the simulator and are passed through to the model without change.

**Parent Elements**: [`sensor`](#sensor)

---

(contact-sensor-sensors)=

#### `contact`

Sensor data for a contact sensor that detects and reports properties of contact events.

The contact sensor detects contacts between pairs of
geoms, bodies, or subtrees, or contacts associated with a site. Multiple filtering
attributes can be specified to narrow the set of contacts detected. The sensor can
report various contact properties such as whether contact was found, the contact force,
torque, distance, position, normal, or tangent direction.

```{note}
Exactly one of the following filter groups may be used at a time: (geom1, geom2),
 (body1, body2), (subtree1, subtree2), or site. These groups are mutually exclusive
 and cannot be combined.

 The following describes how motrixsim's contact sensor output differs from MuJoCo:
 - `found`: Reports the total **count** of matching contacts, not a 0/1 boolean.
 - `site` filter: Parsed but **not yet supported** at runtime; the sensor will be ignored.
```

**Attributes:**

(contact-sensor-sensors-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the sensor.

(contact-sensor-sensors-geom1)=

-   **`geom1`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the first geom used to filter contacts. Must be paired with geom2; cannot
    be combined with body, subtree, or site filters.

(contact-sensor-sensors-geom2)=

-   **`geom2`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the second geom used to filter contacts. Must be paired with geom1; cannot
    be combined with body, subtree, or site filters.

(contact-sensor-sensors-body1)=

-   **`body1`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the first body used to filter contacts. Must be paired with body2; cannot
    be combined with geom, subtree, or site filters.

(contact-sensor-sensors-body2)=

-   **`body2`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the second body used to filter contacts. Must be paired with body1; cannot
    be combined with geom, subtree, or site filters.

(contact-sensor-sensors-subtree1)=

-   **`subtree1`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the first body subtree used to filter contacts. All contacts involving any
    geom in this subtree will be considered. Must be paired with subtree2; cannot be
    combined with geom, body, or site filters.

(contact-sensor-sensors-subtree2)=

-   **`subtree2`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the second body subtree used to filter contacts. Must be paired with
    subtree1; cannot be combined with geom, body, or site filters.

(contact-sensor-sensors-site)=

-   **`site`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the site used to filter contacts. Contacts associated with this site will
    be considered. Cannot be combined with geom, body, or subtree filters.

(contact-sensor-sensors-num)=

-   **`num`** [ <span class="badge int">int</span> | <span class="badge required">Required</span> | **Default:** `1` ]

    The maximum number of contacts to detect and report. When more contacts are found
    than this value, only the first contacts (up to this limit) are used, unless a
    reduction method is specified.

(contact-sensor-sensors-data)=

-   **`data`** [ <span class="badge array">real(n)</span> | <span class="badge required">Required</span> | **Default:** `found` ]

    The type or types of contact data to report in the sensor output. Multiple data
    types may be listed in sequence.

(contact-sensor-sensors-reduce)=

-   **`reduce`** [ <span class="badge string">string</span> | <span class="badge required">Required</span> | **Default:** `none` ]

    **Choice:** [ `none` | `mindist` | `maxforce` | `netforce` ]

    The method used to reduce multiple contacts to a single output value.

**Parent Elements**: [`mujoco`](#mujoco), [`sensor`](#sensor)

---

(statistic)=

### `statistic`

This element is used to override model statistics computed by the compiler.

These statistics are not only informational but are also used to scale various components of
the rendering and perturbation. An override mechanism is provided in the XML because it is
sometimes easier to adjust a small number of model statistics than a larger number of visual
parameters.

**Attributes:**

(statistic-extent)=

-   **`extent`** [ <span class="badge real">real</span> | <span class="badge optional">Optional</span> ]

    Replaces the extent value computed by the compiler. The computed value is half the side of
    the bounding box of the model in the initial configuration. At runtime this value is
    multiplied by some of the attributes of the `map` element. When the model is first loaded,
    the free camera's initial distance from the center is 1.5 times the extent. Must be
    strictly positive.

(statistic-center)=

-   **`center`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Replaces the center value computed by the compiler. The computed value is the center of the
    bounding box of the entire model in the initial configuration. This 3D vector is used to
    center the view of the free camera when the model is first loaded.

**Parent Elements**: [`mujoco`](#mujoco)

---

(keyframe)=

### `keyframe`

This element is a grouping element for keyframes.

**Parent Elements**: [`mujoco`](#mujoco)

**Child Elements**: [`key`](#key)

---

(key)=

#### `key`

This element sets the data of a keyframe.

**Attributes:**

(key-name)=

-   **`name`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Name of the keyframe.

(key-time)=

-   **`time`** [ <span class="badge real">real</span> | <span class="badge optional">Optional</span> ]

    Simulation time.

(key-qpos)=

-   **`qpos`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Joint positions.

(key-qvel)=

-   **`qvel`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Joint velocities.

(key-ctrl)=

-   **`ctrl`** [ <span class="badge string">string</span> | <span class="badge optional">Optional</span> ]

    Actuator controls.

**Parent Elements**: [`keyframe`](#keyframe)

---

## Appendix

(rotation-attrs)=

### `rotation-attrs`

Rotation representation shared by `body`, `geom`, `camera`, `site`, and `inertial`.

Frame orientation can be specified in one of the following five mutually exclusive ways.
Only one attribute should be provided per element.

**Attributes:**

(rotation-attrs-quat)=

-   **`quat`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Unit quaternion specifying the orientation in scalar-first format \\[w, x, y, z\\]. The
    identity rotation is \\[1, 0, 0, 0\\]. If specified, all other orientation attributes
    must be absent.

(rotation-attrs-euler)=

-   **`euler`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Euler angles \\[r1, r2, r3\\] in degrees (or radians when `angle=\"radian\"` in compiler).
    Axis order is given by the `eulerseq` compiler attribute (default `xyz`). If specified,
    all other orientation attributes must be absent.

(rotation-attrs-axisangle)=

-   **`axisangle`** [ <span class="badge array">real(4)</span> | <span class="badge optional">Optional</span> ]

    Axis-angle pair \\[ax, ay, az, angle\\]. The first three components define the rotation
    axis; the fourth is the rotation angle in degrees (or radians). The axis need not be
    unit-length. If specified, all other orientation attributes must be absent.

(rotation-attrs-xyaxes)=

-   **`xyaxes`** [ <span class="badge array">real(6)</span> | <span class="badge optional">Optional</span> ]

    X and Y axes of the frame \\[x0, y0, z0, x1, y1, z1\\]. Z = X × Y. Neither X nor Y
    needs to be unit-length; they are normalized automatically. If specified, all other
    orientation attributes must be absent.

(rotation-attrs-zaxis)=

-   **`zaxis`** [ <span class="badge array">real(3)</span> | <span class="badge optional">Optional</span> ]

    Z axis direction \\[ax, ay, az\\]. The X and Y axes are chosen automatically to form a
    right-handed frame. If specified, all other orientation attributes must be absent.

(solver-attrs)=

### `solver-attrs`

Constraint solver parameters shared by contacts, joint limits, equality constraints,
friction losses, and tendons.

Each constraint has two groups of solver parameters: reference and impedance. Together they
define the constraint behavior in terms of error reduction and response characteristics.

**Attributes:**

(solver-attrs-solref)=

-   **`solref`** [ <span class="badge array">real(2)</span> | <span class="badge required">Required</span> | **Default:** `0.02 1.0` ]

    Constraint reference parameters, with two elements `[timeconst, dampratio]`.

    The default is `0.02 1`. These can be interpreted in two ways depending on sign:

    -   **Positive (default)**: `[timeconst, dampratio]`. The time constant `timeconst` (in
        seconds) determines how quickly the constraint violation is resolved. The damping ratio
        `dampratio` determines the amount of damping; 1 is critical damping. With positive
        semantics the constraint acts as a mass-spring-damper whose parameters are computed from
        the constraint-space inertia, so that the resulting dynamics has the specified time
        constant and damping ratio.

    -   **Negative**: `[-stiffness, -damping]`. The stiffness and damping of the virtual spring
        are set directly without taking the constraint-space inertia into account.

(solver-attrs-solimp)=

-   **`solimp`** [ <span class="badge array">real(5)</span> | <span class="badge required">Required</span> | **Default:** `0.9 0.95 0.001 0.5 2.0` ]

    Constraint impedance parameters, with up to five elements
    `[dmin, dmax, width, midpoint, power]`.

    The default is `0.9 0.95 0.001 0.5 2`. These parameters define a smooth function
    that maps constraint violation (distance) to an impedance value between `dmin` and `dmax`:

    -   `dmin`: minimum impedance, applied at large violations.
    -   `dmax`: maximum impedance, applied near the constraint boundary.
    -   `width`: transition zone width over which impedance changes.
    -   `midpoint`: position of the impedance midpoint within the transition zone.
    -   `power`: power of the polynomial used for the impedance transition.
