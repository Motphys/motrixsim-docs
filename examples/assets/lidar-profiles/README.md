# MotrixSim Lidar Profiles

This directory contains includeable MJCF `asset/lidar` profiles. Include `catalog.xml` to load
the complete starter catalog, or include one vendor/model file to keep the asset namespace small.

`sensor/lidar.hz` remains an instance field and must match the fixed rate encoded by the selected
profile:

```xml
<mujoco>
  <include file="examples/assets/lidar-profiles/catalog.xml"/>
  <worldbody>
    <site name="lidar_mount"/>
  </worldbody>
  <sensor>
    <lidar name="roof_lidar" site="lidar_mount"
      asset="hesai_xt32_sd10" hz="10" exclude="parentsubtree"/>
  </sensor>
</mujoco>
```

The robot locomotion example can list and select these profiles for Go1, Go2, or G1 at startup:

```bash
uv run examples/control/robot_locomotion.py --list-lidars
uv run examples/control/robot_locomotion.py --robot go2 \
  --lidar ouster_os1_rev6_32ch_10hz_512res
```

Without `--lidar`, the locomotion example does not attach a lidar.

## Included profiles

- HESAI XT32 SD10.
- Ouster OS0 Rev6/Rev7, 128 channels, 10/20 Hz and 512/1024/2048 supported resolution modes.
- Ouster OS1 Rev6, 32 and 128 channels; Rev7, 128 channels; the same supported rate/resolution modes.
- Ouster OS2 Rev6/Rev7, 128 channels; the same supported rate/resolution modes.

The profile names follow `vendor_model_revision_channels_rate_resolution`. Each name denotes one
specific operating mode rather than a runtime-selectable variant.

## Fidelity boundary

These profiles contain only nominal scan geometry, report rate, fixed scan frequency, and far-range
cutoff supported by MotrixSim's current MJCF schema. Ouster vertical beams use the nominal uniform
field of view; per-device calibration, minimum range, range error, intensity, reflectance,
multiple returns, and per-emitter firing time are not represented.

Values are based on public manufacturer specifications.

## Sources

- [HESAI XT32](https://www.hesaitech.com/product/xt32/)
- [Ouster Rev6/Rev7 datasheets](https://ouster.com/downloads)
