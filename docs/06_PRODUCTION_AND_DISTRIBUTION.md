# Production and Distribution

## Visual Drill production envelope

```text
Authoring
  ↓
request-specific envelope + authoring.json
  ↓
VisualDrillRuntime
  ↓
UnifiedSocialFrame / C11-C presentation
  ↓
Movie Maker
  ↓
AVI
  ↓
FFmpeg
  ↓
MP4 + FFprobe
  ↓
manifest + social.txt + review artifacts
```

## Physical contract

- 720×1280
- 9:16
- 30 FPS
- Tracking: 27 s total
- Saccade/Pursuit/Peripheral Scan: 23 s total
- 3 s countdown + gameplay + 3 s terminal CTA

## Audio

C11-C 2.9.0 uses one shared Visual Drill ambient master, profile `drill_motion_ambient_v2`. The master is intentionally independent of family/seed and contains no event-locked timing.

`-NoSound` / `-Silent` remain supported by the review runner.

## Social sidecar

Every review render creates a sibling `.txt` with:

- title;
- description;
- family;
- seed;
- resolution;
- FPS;
- gameplay duration/frames;
- countdown and CTA durations;
- CTA text and Header placement;
- audio mode;
- font;
- procedural background statement;
- family-specific hashtags.

Actual answer counts remain in `authoring.json`, not in the public social sidecar.

## Release readiness

2.9.0 is not production-frozen until the final Windows/Godot runtime validation and physical visual review are green.

C11-D remains the later checkpoint for locking final export profiles, media QA, provenance and release-candidate packaging.
