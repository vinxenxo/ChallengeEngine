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

C11-C 2.10.1 uses `FAMILY_MUSIC_V3`: one semantic profile per audiovisual family grammar, selected deterministically by family/route and seed. The active Drill/Loop pairings are defined in `profiles/presentation/c11c_visual_music_profiles.json`.

Delivery constraints: 44.1 kHz stereo source WAV, peak target ≤ 0.20 before AAC mux, low-transient/low-high-frequency-energy design, no kick/snare layer, and no gameplay-event coupling. Drill audio gently settles during the terminal three seconds.

The family music layer is presentation/delivery only; C7 ownership/contracts remain untouched.

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
- audio profile;
- font roles (Header/Footer);
- procedural background statement;
- family-specific hashtags.

Actual answer counts remain in `authoring.json`, not in the public social sidecar.

## Release readiness

2.10.1 is not production-frozen until the final Windows/Godot runtime validation and physical Visual Drill + Visual Loop review are green.

C11-D remains the later checkpoint for locking final export profiles, media QA, provenance and release-candidate packaging.
