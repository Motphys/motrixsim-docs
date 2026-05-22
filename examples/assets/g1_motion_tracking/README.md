# G1 Motion Tracking Assets

This directory contains the default asset bundle for standalone G1 motion-tracking playback in
`motrixsim-python/motrixsim-docs`.

## Files

- `model_4999_single.onnx`
  Bundled ONNX actor for G1 motion-tracking playback.
- `dance1_subject2_part.npz`
  Reference motion clip used to build the 160D actor observation.
- `scene_flat.xml`
  Dedicated flat-ground scene bundle for motion tracking playback. The Python example attaches the
  shared G1 robot model from `../g1/g1.xml` at runtime.

## Usage

Run the playback example from `motrixsim-python/motrixsim-docs`:

```bash
uv run examples/control/g1_motion_tracking.py
```

The full playback path needs the optional demo dependencies from the `motrixsim-python` workspace,
including ONNX Runtime.

The script uses the bundled scene, motion, and ONNX files by default. The robot model comes from the
shared G1 asset directory. To inspect override options:

```bash
uv run examples/control/g1_motion_tracking.py --help
```

## Contract

- ONNX input: `(batch, 160)`
- ONNX output: `(batch, 29)`
- Default scene: `examples/assets/g1_motion_tracking/scene_flat.xml`
- Default robot: `examples/assets/g1/g1.xml`
- Playback sim timestep: `0.02 / 3`
- Sensor mapping for actor obs: shared G1 sensors `local_linvel_pelvis` + `gyro_torso`
- Task-specific actuator and joint profiles are applied at runtime from
  `examples/control/g1_motion_tracking_helpers/contract.py`.
- Default action offset for Motrix playback is the Motrix model init pose, i.e. all-zero 29D joint offset
- Motion body axis must be sliced by the precomputed `MOTION_BODY_INDICES` from
  `examples/control/g1_motion_tracking_helpers/contract.py`. The bundled `.npz` keeps the full
  exported body layout, and these indices match the shared G1 MuJoCo body order.

If any of these assets or the shared G1 model are updated, re-check actuator count, body-name
mapping, sensor names, task profile values, and the actor observation layout before using the new
files as defaults.
