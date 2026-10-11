# C11-D — Unified audio/music delivery policy proposal checkpoint

Date: 2026-10-11  
State: `PROPOSED_NOT_APPROVED` — included in the unified Loop/Drill/Challenge review for consistency checking only.

## What this milestone defines

A separate technical audio-delivery envelope based on the pinned `REVIEW_720` fields in `profiles/delivery/c11c_video_delivery_profiles.json`:

- AAC Low Complexity (`aac_low`), 192 kb/s.
- 48,000 Hz, stereo (2 channels).
- The **pre-encode audio timeline** matches each content type's proposed delivery-video duration.
- Exact 48 kHz PCM timeline sample counts are checked arithmetically: Loops 20 s = 960,000 samples; Drills 21 s = 1,008,000 samples; Challenges 15 s = 720,000 samples.

These counts describe a proposal's target timeline only. No PCM samples or audio payload are generated. AAC encoder priming, final container duration tolerances and post-encode measurement remain undefined and unapproved.

## Explicitly not decided

This is **not** a music-selection or sound-design policy. It does not choose licensed tracks, synthesize sound, assume silence when an asset is missing, set per-family music, or define mixing, ducking, gains, fades, looping, crossfades, loudness targets or normalization. Those decisions require a separate editorial/policy gate before any renderer use.

## Unified review integration

The console-only unified review includes `unified_audio_music_policy` and `unified_audio_music_policy_parity`. It checks duration alignment against the common delivery timebase, profile metadata and sample-count arithmetic. A new explicit unresolved gate is added: `AUDIO_MUSIC_DELIVERY_AND_EDITORIAL_POLICY_NOT_APPROVED`.

The prior audio field in the timebase policy remains `OUT_OF_SCOPE_NOT_DEFINED_NOT_EMITTED`; the independent policy above supplies only the technical delivery envelope and leaves musical/editorial choices open.

## Governance

- Audio/music delivery policy, soundtrack selection, mixing, loudness and audio timeline approval remain false.
- Renderer activation/dispatch/native input: false; audio payload/samples: not emitted; media creation: false.
- Frozen C11-C sources and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` remain immutable.
- `D4.8=BLOCKED`, renderer baseline not approved/frozen, D9.14/D9.16 acceptance blocked, D9.17 NO-GO, D10 blocked and release authority `NONE`.
- Passing tests show contract consistency only; they do not authorize an audio or video render.

## Focused commands

```powershell
python .\tools\c11d\d9\test_d_renderer_unified_audio_music_delivery_policy.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
```
