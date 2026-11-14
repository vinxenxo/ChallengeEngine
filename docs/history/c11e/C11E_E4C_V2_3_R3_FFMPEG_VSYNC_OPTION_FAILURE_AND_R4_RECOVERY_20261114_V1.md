# C11-E E4C V2.3 R4 — FFmpeg review-frame compatibility and existing-output recovery

**Disposition:** R4 patch prepared; Windows installation and recovery execution pending. R3 installation and independent post-install audit remain PASS.

## Incident evidence

The 2026-11-14 R3 run `E4C-CLI-COMPOSITION-V2-20261114T003422Z-a4d913f9` reached `FRAME_COMPOSITION=810/810`, `MUX_B_STARTED`, and `STREAM_HASH_A_STARTED`. The diagnostic bundle confirms:

- `d_composed_silent_v2.mp4`: 785,860 bytes, SHA-256 `d674aa7700414c49c5b5ca957c4390da6e0020cea2de9d84750f30c6f14e14a5`.
- Final A and B: 1,455,889 bytes each, SHA-256 `8808b5244c118dc74d9a6fcf9d5e5b49b8ddae33f686794a170fe76cbc971bc1`.
- Final C: 1,454,787 bytes, SHA-256 `677edb16b0b1fcf47962633624df53ec5c53201080c95d5f563f10b1957c1961`.
- The exact failure was `review frame extraction failed for 0: Unrecognized option 'vsync'`.

`compose_all_frames_v2()` returns to the mux stage only after all 810 frames, exact PRE_ROLL/GAME/END_CTA counts, 630 GAME-body pixel-identities, 180 full-frame passthrough identities, successful FFmpeg decoder/encoder exits, and silent output existence. The operator console trace reached `MUX_B_STARTED` and then `STREAM_HASH_A_STARTED`, so all three mux operations and the A/B/C stream-hash checks were passed before the failure in review-frame extraction.

## R4 change

1. Replace the removed FFmpeg output option `-vsync 0` with `-fps_mode passthrough` in the normal requalifier's seven-frame extraction command.
2. Add a recovery utility bound to the exact R3 output ID above. It verifies the preserved accepted receipt, intent, 91 E1 source pins, frozen C11-C manifest, exact V2 composition plan, silent intermediate, all three MP4 byte counts and SHA-256s, FFprobe contracts, and re-computed video/audio elementary-stream hash relationships.
3. Recovery extracts only the seven operator-review stills. It does not render, recompose, mux, generate music, create a native capture, invoke Godot/C11-C, modify E1 service, or dispatch production.
4. Recovery refuses other run IDs, unknown/changed media, missing outputs, and pre-existing review-frame names. It writes the final technical receipt, recovery audit, review checklist, progress state and an operator-review ZIP.

## Requalification evidence still required

After the R4 install and independent audit, run the one-shot recovery command from the runbook. Expected terminal status: `PASS_V2_TECHNICAL_REQUALIFICATION_PENDING_OPERATOR_VISUAL_AUDIO_ACCEPTANCE`, seven valid PNGs, video hashes A/B/C identical, audio hashes A/B identical and C different, FFprobe 27-second/810-frame H.264 High yuv420p TV + AAC-LC 48 kHz stereo, A/V start delta <=20 ms.

The selector remains **0/20 accepted** until the operator reviews all seven frames and listens to A/B/C. The technical receipt does not grant human acceptance, production dispatch or release authority.

## No-repeat policy

Do not repeat R3 installation, its 10 regression tests, the R3 independent audit, the 810-frame composition, the three audio muxes, GUI/CLI smoke, native capture, Godot, or FAMILY_MUSIC_V4 generation. Use existing R3 outputs only.

`GIT_CHECKS=SKIPPED`; `COMMITS=OPERATOR_MANAGED`; C11-C frozen manifest SHA-256 remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; `release_authority=NONE`.
