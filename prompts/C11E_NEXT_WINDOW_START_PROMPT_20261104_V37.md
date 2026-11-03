# C11-E Next Window Start Prompt — V37

Continue in the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`; it is the only source of truth. PowerShell 5.1. Never extract old snapshots over it. The product objective remains one coherent audiovisual production service for Challenge, Visual Loop and Visual Drill using the existing C11-C generators/mechanics plus D-owned presentation/editorial/audio orchestration. Keep GUI and CLI on the same service. No parallel producer/binder or sixth suite module.

## Read current authority

- `docs/current/e/C11E_CURRENT_AUTHORITY_20261104_V37.md`
- `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261104_V37.md`
- `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261104_V14.md`
- `docs/current/e/C11E_E4A_REAL_BODY_PIXEL_INCREMENT_20261104_V3.md`
- `docs/current/e/C11E_E4A_REAL_BODY_PIXEL_FAILURE_ANALYSIS_20261104_V1.md`
- `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261104_V27.md`
- `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261104_V37.md`

## Immediate action: corrected E4A.2 — reuse, do not rerender

The user already generated CHALLENGE_004 / seed 314159 / REVIEW_720 / NoSound. Its source MP4 is in:

`artifacts/tests/c11e/e4a_real_body_pixel_review/RUN_20261103_235800_fd6fb07c/c11c_base_render/CHALLENGE_004/CHALLENGE_004_seed_314159.mp4`

Source MP4 SHA `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de`. FFprobe: H.264 720×1280, `yuvj420p/pc`, 60fps, 900 frames, 15s, silent. C11-C manifest says `pixel_format=yuv420p`; record this mismatch; do not modify the source or manifest. The V1 runner failed before PNG extraction because it wrongly assumed the raw input was already 30fps/450/yuv420p. The user later typed a PASS marker after the thrown error; it is invalid. The C11-C video generation succeeded and operator says video visually OK.

Apply `C11E_E4A_REAL_BODY_PIXEL_OVERLAY_V2.zip` with its exact sidecar. It replaces only the runner and tests against these exact V1 preimages (or accepts exact V2 postimages):
- runner preimage `a852e5f4238f14b30a887f579bad3e4284c420c427dc625667a0ec60190fff1a`; V2 postimage `5c0e8765bb29b58ddefc1b9593be188227e77725431c3dc959c1ce6866529a9b`.
- tests preimage `5e967ec3b8fd87cc9effe079356912e8f6b69f8994a368dc8f1c15cfb95dcb0c`; V2 postimage `657f459ce11621a2dde133da5234ea27754c56b3acb5a10c8b37ff952a48d07b`.
- new V37/V14/V27 documentation and prompts are add-only.

The corrected runner creates a **test-only derivative** from source 60fps/900 to limited-range 30fps/450 `yuv420p/tv`; it keeps the original source media and normalizer logs. It accepts the existing run directory through `--reuse-c11c-base-run` and does not call Godot.

Run from repository root:

```powershell
python -B .\tools\c11d\d9\test_c11e_e4a_challenge_real_body_pixel_review.py
$TestExit = $LASTEXITCODE
if ($TestExit -ne 0) { throw "E4A.2 tests FAIL: $TestExit" }
python -B .\tools\c11d\d9\c11e_e4a_challenge_real_body_pixel_review.py --reuse-c11c-base-run ".\artifacts\tests\c11e\e4a_real_body_pixel_review\RUN_20261103_235800_fd6fb07c"
$RunExit = $LASTEXITCODE
if ($RunExit -ne 0) { throw "E4A.2 replay FAIL: $RunExit" }
```

Capture and report the new `EVIDENCE_DIR`, receipt SHA and complete ZIP. Never manually print PASS after a failure. Inspect the original MP4, normalized derivative FFprobe, normalizer logs, 18 PNGs, 12 comparisons, body hashes, E1 intents, source pins and C11-C manifest before acceptance.

## Strict visual caveat

The preparation montage shows test-only title/subtitle text overlaps the existing C11-C hook headline. D1.5 safe-area and generic typography positions are UNKNOWN. This proof validates pixel-region confinement and gameplay BODY identity only; fixture text positions are not accepted production geometry. Do not guess coordinates or edit C11-C. E4A.3 must solve D-owned composition stacking/layout using authoritative evidence.

## Then continue the roadmap

After corrected Windows E4A.2 evidence: E4A.3 actual D Challenge consumer → E4A.4 test-only A/V using already accepted E3 D3 V5/mux/FFprobe + operator review → E4A closure → E4B Loop → E4C Drill → E5 determinism/seeds/profile-leakage/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 (99 provisional while CH_008/009 11s/12s discrepancy held) → E8 full historic C11-C corpus row-by-row review, independent acceptance, freeze and separate promotion.

## Non-negotiable controls

C11-C 2.19.12 remains production authority; manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` unchanged. No protected C11-C mechanics/generator/RNG/presentation/core/audio changes, no D3 V5 or E1 service change, no sixth module, no parallel binder/producer, no production dispatch/media. D renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.
