# Production and Distribution — Current

## Standard video delivery

The default product master is `MASTER_1080`:

- MP4 container.
- 9:16.
- 1080×1920.
- Constant frame rate, progressive.
- H.264 / yuv420p for the current default implementation.
- Closed GOP, 3 seconds in the current 30 FPS profiles.
- AAC-LC, 48 kHz stereo, 192 kbps in master delivery profiles.

The delivery system is profile-driven and can emit 540×960, 720×1280 or 1080×1920 without changing the runtime mechanics.

## Capture versus delivery

### Challenges

Historical Challenge production captures the native source at 540×960. Delivery scaling is a post-capture FFmpeg operation.

```text
Challenge runtime
    ↓
540×960 source AVI/MP4
    ↓
FFmpeg delivery profile
    ├── MIN_540
    ├── REVIEW_720
    └── MASTER_1080
```

### Visual Loops / Visual Drills

The proven C11-C review geometry is 720×1280. Visual Loops retain their established capture path; the single-Visual-Drill Producer captures a temporary PNG sequence at 720×1280 and immediately encodes it to MP4 before delivery processing.

```text
C11-C runtime / review capture
    ↓
720×1280 source (Loop: established Movie Maker path; Drill: temporary PNG sequence)
    ↓
FFmpeg source MP4 / delivery profile
    ├── MIN_540
    ├── REVIEW_720
    └── MASTER_1080
```

## Audio

The delivery layer normalizes master output to AAC-LC / 48 kHz / stereo. Historical review runners may use an older source sample rate internally; that is normalized during master delivery rather than changing C7 ownership.

## Social limitations

The 3–90 second range is treated as a social delivery constraint for ordinary short-form profiles. `LONGFORM_1080` is not subject to that social-duration gate.

## Producer

`c11c-suite/c11c-producer` exposes the delivery profile for A LA CARTA production. Historical batch-review operations retain their established C11-C review behavior and do not silently reinterpret old batch contracts.

## Artifact policy

Generated product files belong under `artifacts/`. Historical Challenge source AVI remains part of the legacy C11-A production path; the single-Visual-Drill Producer does not use AVI and removes its temporary PNG sequence with the scratch stage. Historical evidence must not be silently replaced by later renders.
