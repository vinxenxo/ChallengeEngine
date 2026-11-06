# C11-E Current Authority — V67

**Date:** 2026-11-05. This authority records the E4A.6 reserved-band correction, the V2 false-negative, the retired Git gate, and two documentation-package preflight defects in recovery V1.1. It does not supersede any production or promotion lock. It does not supersede any production or promotion lock.

## Active checkout and immutable baseline

The sole working checkout is `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. It remains authoritative. Never extract snapshots or evidence archives over it. The operator creates a commit at each iteration. Per-iteration runners must not invoke Git, inspect HEAD/status, require `.git`, compare commit IDs or record Git state. Exact source-file SHA-256 pins and the frozen C11-C manifest remain mandatory; runner source changes remain limited by explicit path/hash guards.

Frozen C11-C 2.19.12 manifest: 796,318 bytes; SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## E4A.6 reserved-band result

Operator requirement: while the optional D editorial envelope is enabled, the full HEADER (logical y=0..144) and FOOTER (y=816..960) bands remain opaque pure black on every source frame. Optional `title`/`subtitle` may appear only in HOOK/HEADER; optional `call_to_action` only in CTA/FOOTER. Inactive/empty regions retain black and hide the text/separator. BODY and no-envelope legacy C rendering remain unchanged. The video/body background colour is not a blocker for this gate; making that background user-selectable is a separate future editorial feature and must not alter the reserved-black-band invariant.

### Evidence recovered from the V2 Windows run

- Windows PowerShell `5.1.26100.9818`; AST parse PASS.
- Python focused tests: 22/22 PASS.
- Godot 4.7.1 editor import PASS.
- Godot live-root runtime: 900 frames, one mount, 900 black-band frames; runtime summary `PASS_TEST_ONLY`.
- Movie Maker stdout records the matching `C11E_E4A6_LIVE_CONSUMER_CONFIGURED` envelope, 900-frame phase telemetry (180 HOOK + 420 GAME + 180 REVEAL + 120 CTA), `audio_enabled=false`, `Done recording movie`, and the 900-frame AVI output.
- Uploaded capture ZIP source AVI SHA-256: `2f6d0c73cb09571584db68e37760c933706473a07e559fc93113f26eabb89f45`; FFprobe confirms MJPEG 540x960, 60/1 FPS, 900 frames, 15 seconds. It also contains an unexpected PCM S16LE 48 kHz stereo stream; this stream is discarded, never used as D3 audio.
- The original V2 overall BLOCKED status is a runner false-negative: `Test-CaptureLog` is path-based (`Test-Path` + `ReadAllText`) but the new-capture branch passed `$movie.Stdout` (text) rather than a path. Therefore it returned false before evaluating the already-valid semantic markers. No consumer/test failure is evidenced by this exception.
- Recovery-only postprocessing independently exercised against the uploaded AVI: H.264 High, 720x1280, 30 FPS, 450 frames, 15.000 s, yuv420p, limited/tv range, no audio; eight boundary stills; 12 inactive-band region/frame checks at 0 non-black samples (31,680 samples each); four active HOOK/CTA text checks above threshold. This independent container check used FFmpeg 7.1.5 and is analysis corroboration, not a substitute for the Windows FFmpeg 9.0 recovery receipt.

The first recovery-only runner V1 passed AST but stopped immediately at `EVIDENCE_AND_SOURCE_PREFLIGHT`: it required the old V2 `git HEAD` (`0b24934f423763513540e31ba9104052617c4e4f`), while the operator-managed checkout had advanced to `d5589fde1e5132c653c1ac5604a34a524c02a47a`. No evidence validation, FFmpeg/FFprobe, file copy, pixel processing, source write or documentation write ran. This HEAD gate was contrary to the standing operator workflow and is retired.

Recovery-only V1.1 removed all Git interaction correctly, and its Windows run passed AST, V2 evidence/source validation and confirmed it would not rerender or rerun Python. It then stopped twice at documentation preflight: first because the recovery documentation manifest was not beside the script; second because copying only the manifest to Downloads did not provide the 15 referenced `docs/...` and `prompts/...` payloads. Both attempts stopped before FFmpeg/media processing, source writes or documentation writes. No further manual extraction of separate manifest/doc files is an acceptable recovery workflow. Recovery V1.2 embeds the compressed, hash-pinned documentation package inside the runner and self-extracts it into the unique recovery evidence directory. The runner is therefore standalone: only the `.ps1` file is required in Downloads. It still does not invoke Git, rerun Python/Godot/Movie Maker, or write runtime source. It reuses the same AVI and installs the 15 versioned documents add-only only after Windows FFmpeg 9.0 and all eight-still/pixel validations pass. Its output namespace is `RECOVERY_V1_2`; require its receipt before marking the bounded gate `PASS_TEST_ONLY_RESERVED_BANDS_BLACK_CAPTURED`.

## Source boundaries

The reserved-band change is confined to D-owned `tools/c11d/d9/C11EChallengeLiveEditorialConsumer.gd` plus `tools/c11d/d9/test_c11e_e4a6_reserved_bands_black.py`. Current consumer SHA-256 `eba81fff4c24ca75033c8f963665df1961136046c41fee0e88681fe55a631203`; focused test SHA-256 `9845eda094037f8748493171755b32d3479ddf6548612e9a6ecebba187cbc512`. Frozen shared layer `core/presentation/C11CVisualEditorialLayer.gd` remains read-only at `f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d`. Active D-only `GeneradorMaestro.gd` SHA remains `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82`, distinct from the frozen manifest entry; do not edit or restore it under E4A.6.

## Immediate next gate — full Challenge E4A audiovisual closure

Use the corrected, silent D-composited MP4 **unchanged** as the video source. Reconcile the exact active D3 V5 engine/spec/profile and accepted E4A.4 mux/FFprobe pins; generate actual D3 V5 audio and apply D3.3 mastering. Keep gameplay `request.seed` independent of `request.music_seed`. A/B: same gameplay and music seeds. C: same gameplay seed/video, changed music seed only. Prove raw/mastered/decoded audio A/B repeatability and C audio difference; identical H.264 elementary video stream/frame identity across A/B/C; one H.264 plus one AAC-LC 48 kHz stereo stream; non-silence; exactly 15 seconds; A/V drift <=0.15 seconds. Preserve WAVs, muxed MP4s, FFprobe JSON, volume reports, commands, logs, hashes and immutable receipt. Complete operator visual/listening disposition and E1 GUI/CLI parity before closing E4A.

Do not rerender gameplay, re-run the accepted 22 tests, or repeat Godot capture for this step absent concrete source drift or a new defect. Recovery V1.2 only normalizes the already-created AVI and audits its visual samples; it self-hydrates its embedded documentation and has no external docs/manifest prerequisite. Git state is not part of any iteration gate.

## Ordered full campaign

After full E4A: E4B Visual Loop; E4C Visual Drill; E5 cross-family determinism, seed isolation, family/profile non-leakage and GUI/CLI parity; E6 Smoke18 (six A/V cases per family); E7 Matrix101 (54 Challenges + 27 Loop grammars + 20 Drill variants); E8 full C-to-E regression map, independent acceptance, immutable freeze and separately authorized promotion. CH_008/009 remain held for the declared 11 s versus 12 s phase-sum discrepancy.

## Governance

C11-C 2.19.12 remains production authority. Production renderer OFF, dispatch OFF, media OFF. D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`. No sixth suite module, second Producer, parallel binder or change to protected C mechanics/RNG/timeline/binders.
