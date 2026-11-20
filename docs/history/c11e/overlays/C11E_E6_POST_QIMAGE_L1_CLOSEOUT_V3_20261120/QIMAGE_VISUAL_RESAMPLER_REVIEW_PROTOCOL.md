# QImage visual resampler review protocol — operator decision required

## Scope

Inspect the three exact synthetic PNG previews produced by the V2.7 QImage L1 probe. Their file hashes, PNG chunk CRCs and 720×1280 RGB24 structure passed automated validation. That evidence does not determine whether `SmoothTransformation` produces acceptable visual quality.

## Exact files and hashes

All three files are in:

`artifacts/tests/c11e/e6_option_c_native_qt_probe_v2_7/E6OPTCQTV2_7_20261119T225516Z_6DCBCB1C/`

| Preview | File | SHA-256 | PNG contract |
|---|---|---|---|
| Color bars / registration | `OPTION_C_QT_color_bars_registration.png` | `8e9944581d69906b53762c9d84801c5ee5a7217f0756499acb8be48d386f2509` | 720×1280, 8-bit RGB24, CRC PASS |
| Smooth RGB gradient | `OPTION_C_QT_smooth_rgb_gradient.png` | `bb5c9bfdee636efb60e36cfdc2cf4a39f328ad6100e02c05946c43a14b755654` | 720×1280, 8-bit RGB24, CRC PASS |
| One-pixel checkerboard | `OPTION_C_QT_one_pixel_checkerboard.png` | `517185c1bac5434618b970a8e35b1d21612585ccc4adcd4a1ef883ba5c8b1685` | 720×1280, 8-bit RGB24, CRC PASS |

## Already approved geometry

The approved output geometry is 720×1280, with the 504×896 body placed at (108,192). This approval is retained. It is not an approval of the resampling filter.

## Visual review checklist

- Color bars: check registration, boundaries, geometry and channel alignment; identify unintended shifts, clipping or scaling artifacts.
- Smooth gradient: check continuity, visible banding, discontinuities, unexpected hue shifts and edge behavior.
- One-pixel checkerboard: check expected high-frequency response, symmetry and unexpected directional artifacts. Do not assume that a smooth resampler must preserve one-pixel contrast; record the actual trade-off observed.
- Confirm that the previews correspond to the exact hashes above before review.

## Required operator record

Record one explicit decision: `ACCEPT_SMOOTH_TRANSFORMATION` or `DECLINE_SMOOTH_TRANSFORMATION`, plus a brief observation for each preview. If declined, do not silently substitute another filter; create a separately versioned engineering decision and test plan.

**Current state:** `PENDING_OPERATOR_VISUAL_REVIEW`. No acceptance is inferred by this protocol.
