# C11-D Unified Audio/Music Delivery Policy Integration Overlay V1

## Intent

Integrate a **proposal-only** shared technical audio-delivery envelope and audio-timeline arithmetic for Visual Loops, Visual Drills and Challenges. This complements the existing shared 30 FPS video-delivery timebase without selecting music or emitting audio.

## Strict scope

The policy is based on the pinned `REVIEW_720` registry fields: AAC-LC (`aac_low`), 192 kb/s, 48 kHz, stereo. It proposes that the pre-encode audio timeline match the proposed video delivery duration exactly. Target 48 kHz sample counts are 960,000 for 20-second Loops, 1,008,000 for 21-second Drills, and 720,000 for 15-second Challenges.

Music selection/licensing, soundtrack per content family, SFX/synthesis, mixing, ducking, gains, fades, loops/crossfades, loudness and normalization are still undefined. The no-asset case is unresolved—this overlay does not assume silence. AAC encoder priming and post-encode duration tolerance are also unresolved. Nothing is encoded or materialized.

## Overlay contents

- Add `D_RENDERER_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_PROPOSAL_V1.json` and strict schema.
- Add standalone Python proposal validator and its 14-test suite.
- Integrate the preview and parity cross-check into the unified content review; source lineage becomes 19 contracts and cross-artifact checks become 16.
- Add the explicit unresolved gate `AUDIO_MUSIC_DELIVERY_AND_EDITORIAL_POLICY_NOT_APPROVED` (total open gates: 9).
- Update the runner output and current/history checkpoints.

## Governance locks

C11-C is untouched. No audio payload/samples, music asset, renderer-native input, renderer dispatch, media creation or persistent review report is produced. The proposal cannot approve itself. `D4.8=BLOCKED`, `release_authority=NONE`, and D9.14/D9.16/D9.17/D10 remain blocked as previously recorded.

## Apply and verify (PowerShell, repository root)

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\C11D_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_INTEGRATION_OVERLAY_V1.zip" -Algorithm SHA256
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_UNIFIED_AUDIO_MUSIC_DELIVERY_POLICY_INTEGRATION_OVERLAY_V1.zip" `
  -DestinationPath "." `
  -Force

python -m py_compile `
  .\tools\c11d\d9\d_renderer_unified_audio_music_delivery_policy.py `
  .\tools\c11d\d9\test_d_renderer_unified_audio_music_delivery_policy.py `
  .\tools\c11d\d9\d_renderer_unified_content_review.py `
  .\tools\c11d\d9\test_d_renderer_unified_content_review.py `
  .\tools\c11d\d9\run_d_renderer_unified_content_review.py

python .\tools\c11d\d9\test_d_renderer_unified_audio_music_delivery_policy.py
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

## Expected key markers

- `cross_artifact=16/16`
- `unified_audio=48KHZ_AACLC_192KBPS_STEREO_3_CONTENT_TYPES_TIMELINE_ONLY_PROPOSAL`
- `unresolved_gates=9`
- `review=CONSISTENT_NOT_VIDEO_READY`
- `renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE`

The integrated Godot run still uses the same seven pre-existing harnesses. A passing result is contract consistency evidence only; it does not authorize rendering or release.
