# C11-E E4A.7 — D-Composited Challenge A/V Plan — V1

**Status:** READY_FOR_EXECUTION_RECEIPT_GOVERNED. This is a bounded technical test only, not production rendering, release approval or full E4A acceptance.

## Input visual authority

Use exactly `artifacts/tests/c11e/e4a6_reserved_bands_black/RECOVERY_V1_2/CHALLENGE_004_D_BLACK_BANDS_720x1280_30FPS_SILENT.mp4`.

- 671,647 bytes; SHA-256 `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`.
- H.264 High / 720×1280 / 30 FPS / 450 frames / 15 seconds / yuv420p / TV range / one video stream / zero audio streams.
- This source already includes the D live editorial composition and the reserved-black-band correction. Its visual user-review disposition is PASS. Do not render again, apply filters, scale, or re-encode its video stream.
- Validate Recovery V1.2 receipt SHA `3279011fa16479d4901c5b271463707a437ce7458d306c1667ab222cb1603980`, MP4 SHA/bytes, `review_mp4_source.json`, `boundary_stills_source.json`, eight stills, contact sheet and pixel audit. Inactive black 12/12 (RGB max tolerance 3); active HOOK/CTA 4/4.

The E4A.4 A/V pilot input MP4 SHA `edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e` was the earlier uncomposited C11-C visual base. Do not reuse that video. E4A.4 supplies only the D3.3/mux/FFprobe method and bounded predicate precedent.

## Live source pins

The worker pins the current reviewed source set before generating audio. Core D3 pins:

| Source | SHA-256 |
|---|---|
| E1 production service | `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951` |
| D9 resolver | `9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1` |
| D9 editorial model | `5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5` |
| GUI request adapter | `0e95109ffd3ba5655d28292309196349470ab7958a467f096543a2c98c22976e` |
| E3 audio pipeline | `46b087683a3dcb460601c925373b84e390999d44d73141328285e6c8a633ba5d` |
| D3 V5 engine | `03ae7e2997796e0c67ca15c8886b1e5b290791a142b6631a572d1cba6eba4eb1` |
| D3 V5 specification | `8970f4e93c878285b727697f3d269f5ee464b6029fe79eabc5fcbf4245e9dbf2` |
| Challenge 8-bit profile | `0c877cbe6e1c288890da31fc4481a58e1051749b45a50b2290cbef5d1120d2de` |
| E1 D3 V5 contract | `12c59ce2a2135a49ce0d5968a29905a1e5890743507db1ee0039da1374efcfe8` |
| Approved Challenge policy | `764629384896a255cf992da89fa427c19f60f9b2e623b81ad17d909674b466b5` |

Also verify the immutable C11-C manifest and file pins for D-only consumer, active `GeneradorMaestro.gd` and frozen shared C11-C layer. The current E1 service pin supersedes the older E4A.4 pilot pin `f0655d8...`; if any active file mismatches, stop before D3 audio generation. Never inspect Git.

## E1 test intents and unresolved engine fields

Build three sealed `request_origin=TEST` E1 intents for Challenge / CHALLENGE_004 / REVIEW_720. `audio_enabled=true`; `presentation_options.show_hook_countdown=true`; `dispatch_authorized=false`; `production_execution=false`. Keep gameplay and music seed domains independent.

- Gameplay seed 314159 for A/B/C.
- Music seed 840001 for A and B; 840002 for C.
- Variation index 0; profile `challenge_8bit_v1` version `1.0`.
- Seeds are historical E4A.4 fixtures reused as test controls, not product defaults.

The E1 music contract currently emits `tempo_bpm=null` and `duration_seconds=null` and lists both as unresolved. Do not mutate that contract or E1. For this technical test only, use tempo 104 BPM with explicit role `HISTORICAL_D9_2_PILOT_FIXTURE_NOT_PRODUCT_DEFAULT`; derive duration from FFprobe on the supplied MP4 (450 / 30 = 15.0 s).

## D3 V5 → D3.3 → mux procedure

1. Render three raw D3 V5 WAVs from the exact pinned engine/spec/profile. Require output hash matches engine record, A/B raw bytes + parameter hash equal, C differs.
2. For each, create a 30-second repeated QA window; apply deterministic FFmpeg `loudnorm=I=-14:TP=-1:LRA=7`; inspect integrated loudness, true peak, no clipping and mono compatibility. Require PCM S16LE 48 kHz stereo and audible output. Trim mastered delivery WAV to exactly 15.0 s.
3. Mux each delivery WAV with the unchanged D-composited MP4. FFmpeg mapping: video from source MP4, audio from mastered WAV; video `-c:v copy`; audio AAC-LC 192 kbps / 48 kHz / stereo. Do not map the silent review's nonexistent audio and do not reuse the AVI's incidental PCM.
4. FFprobe each mux: one H.264 video + one AAC audio stream; 720×1280 / 30 FPS / 450 frames / 15 s; yuv420p / TV range; 48 kHz stereo; non-silent audio; A/V start/end drift <=0.15 s.
5. Extract H.264 elementary streams and require A/B/C each equal the source bitstream SHA. Decode AAC to PCM and require A=B, C differs. Preserve all WAVs, mux MP4s, probes, loudness/volume data, commands, stdout/stderr, exit codes, hashes and report/receipt.

## Acceptance and stop conditions

- A/B raw/mastered/decoded audio repeatability PASS; C differs in raw/mastered/decoded audio.
- Source video H.264 bitstream byte-identical across all muxes.
- All three muxes pass FFprobe, stream cardinality, AAC codec/rate/layout, non-silence, exact timing and <=0.15 s drift.
- Any source pin or recovery evidence mismatch stops before music generation. Any D3, D3.3, mux or QA failure writes a BLOCKED receipt with retained logs; do not repeat whole V2/E4A6 visual work.
- On technical PASS, operator must listen to A/B/C and review audiovisual sync. The next separate requirement is GUI/CLI parity through the same E1 service. Full E4A remains open until both are accepted.

## Scope lock

No gameplay rerender, Godot, Movie Maker, D renderer, production dispatch or production media. This runner creates test-only WAV/MP4 artifacts. No source-file write. C11-C 2.19.12 remains production authority; `release_authority=NONE`.
