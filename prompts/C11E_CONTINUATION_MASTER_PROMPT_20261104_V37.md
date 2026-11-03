# C11-E Continuation Master Prompt — V37

Continue in the authoritative Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The active checkout is the source of truth; ZIPs are evidence/overlays only and must never be extracted over the checkout. Use PowerShell 5.1. Prefer direct engineering and one integrated apply/test action; do not add redundant launchers or repeat accepted suites without relevant source drift.

## Product objective — do not lose focus

Deliver one coherent C11-E service that produces final audiovisual MP4s on demand for **Challenge + Visual Loop + Visual Drill**. Preserve the existing C11-C generators and mechanics. Add D-owned visual presentation, editable family-scoped editorial, correct family music, independent gameplay/music seed domains, FFmpeg mux, FFprobe QA, and GUI/CLI parity through the existing shared service and five existing suite surfaces. No second producer, parallel binder or sixth module.

## Accepted and reusable gates

E0/E1; bounded E2 R4; E3.2; E3 Challenge D3 V5/audio/mux pilot; E3 50/50 negative controls; E4A source discovery; GUI contract successor; Gate A assessment; and operator-approved Challenge Editorial Presentation Policy V1 remain accepted only within their recorded scopes. Do not rerun them unless a dependent source pin changes.

E4A.1 is accepted only as a neutral-body off-screen fixture: Windows Godot 4.7.1, 23/23 tests, 18 PNGs at 540×960, 12 comparisons, receipt SHA `d90394548ae9dc5ac7b75199c96d423605e9c645dedf0616b8bdfbd1b165ea53`. It did not rasterize gameplay.

## E4A.2 failure evidence — accurate state

The Windows E4A.2 V1 runner's focused tests passed 25/25. The existing C11-C Challenge script completed and produced the operator-reviewed-as-OK CHALLENGE_004 test MP4; the runner then exited 1 before PNG extraction. Uploaded archive:

- `RUN_20261103_235800_fd6fb07c.zip`
- SHA-256 `2430588990a6d82aad68082fab000b71b5218af42f27cce75633b7153e06a53d`
- Base MP4 SHA-256 `fdd0598e20ddc6201e54cc2dad7fd3362c2ef80961df44f3ef4676fb97a765de`
- FFprobe source: H.264 720×1280, `yuvj420p/pc`, 60fps, 900 frames, 15 seconds, no audio.
- Adjacent C11-C manifest reports REVIEW_720, 60fps, 900 frames, audio off, and `pixel_format=yuv420p`, which differs from encoded source stream.

The V1 runner wrongly expected the raw C11-C MP4 already to be 30fps/450 frames/yuv420p. Its `FAIL`/exit 1 is authoritative. The later manually typed `...=PASS` line after the exception is invalid and must never be used as evidence. Frozen C11-C manifest was unchanged.

## E4A.2 corrected V2 ready for Windows replay

The corrected runner probes and retains the original 60fps/900-frame C11-C MP4, then creates a **separate test-only derivative** at 30fps/450 frames/`yuv420p` limited range (`tv`). Full-range `yuvj420p/pc` is converted via `scale=in_range=full:out_range=tv`; already limited-range `yuv420p/tv` is not expanded as full range. Unknown source pixel/range pairs fail closed. FFprobe records both original and normalized files.

The runner accepts `--reuse-c11c-base-run` restricted to an existing `RUN_*` directory directly below `artifacts/tests/c11e/e4a_real_body_pixel_review`. It copies the existing MP4, manifest and logs into a fresh evidence run and does **not** relaunch Godot or the C11-C generator. Require its source identity, CHALLENGE_004, seed 314159, REVIEW_720 and audio-off manifest.

Corrected pins:
- `tools/c11d/d9/c11e_e4a_challenge_real_body_pixel_review.py` SHA-256 `5c0e8765bb29b58ddefc1b9593be188227e77725431c3dc959c1ce6866529a9b`
- `tools/c11d/d9/test_c11e_e4a_challenge_real_body_pixel_review.py` SHA-256 `657f459ce11621a2dde133da5234ea27754c56b3acb5a10c8b37ff952a48d07b`
- Preparation tests: 33/33 PASS; `py_compile` PASS.
- Preparation replay against the exact uploaded MP4: normalized FFprobe 720×1280 H.264 `yuv420p/tv`, 30fps, 450 frames, 15s; 18/18 PNGs; 12/12 comparisons; zero A/B BODY changes; B/C identity. This is not yet Windows gate acceptance.

**Immediate command after applying the V2 overlay:**

```powershell
python -B .\tools\c11d\d9\test_c11e_e4a_challenge_real_body_pixel_review.py
if ($LASTEXITCODE -ne 0) { throw "E4A.2 focused tests failed: $LASTEXITCODE" }
python -B .\tools\c11d\d9\c11e_e4a_challenge_real_body_pixel_review.py --reuse-c11c-base-run ".\artifacts\tests\c11e\e4a_real_body_pixel_review\RUN_20261103_235800_fd6fb07c"
$RunExit = $LASTEXITCODE
if ($RunExit -ne 0) { throw "E4A.2 corrected replay failed: $RunExit" }
```

Do not type a success marker after a failed command. Upload the new full `RUN_*` ZIP. Verify receipt hashes, retained original MP4, normalizer logs/command, FFprobe for both videos, PNGs, 12 comparisons, body crop hashes and source pins. Require unchanged BODY across all six samples. E4A.2 remains open until the Windows result is verified.

## Important visual/layout finding

The 18-image preparation montage shows the test-only title/subtitle placeholder text overlaps the existing C11-C hook headline in HEADER/HOOK. D1.5 defines only region geometry and explicitly leaves generic safe-area inset, margins and typography UNKNOWN. The fixture text coordinates prove region confinement only and are not production-approved. Do not guess replacement coordinates, change existing C11-C content or mark visual placement accepted. E4A.3 must resolve actual D-owned composition stacking/layout using canonical evidence.

## Sequence after E4A.2

1. **E4A.3:** connect D-owned composition to the actual D Challenge visual consumer; no `hook_text` / `cta_main` aliases, no second binder/producer. Resolve or formally retain blocked Challenge overlay geometry.
2. **E4A.4:** test-only A/V qualification using the accepted E3 D3 V5/music-seed/mux/FFprobe path; then operator visual review and E4A closure.
3. **E4B:** Visual Loop grammar/variant timeline, presentation/editorial binding; retain existing C11-C Loop music and footer omission.
4. **E4C:** Visual Drill type/tier, phase/END_CTA precedence and presentation/editorial; retain existing C11-C Drill music.
5. **E5:** determinism, independent gameplay/music seed isolation, family/profile leakage and GUI/CLI parity.
6. **E6:** Smoke18, six audiovisual scenarios per family.
7. **E7:** Matrix101: 54 Challenge + 27 Loop + 20 Drill; CH_008/009 stay held because declared 11s conflicts with phase sum 12s, leaving 99 provisional runnable cases.
8. **E8:** row-by-row historic C11-C corpus reconciliation, independent acceptance, immutable freeze and separate explicit promotion.

## Invariants and authority

C11-C 2.19.12 remains sole production authority. Frozen manifest `release/C11C_FREEZE_PACKAGE_MANIFEST.json`, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796,318 bytes. Do not modify C11-C mechanics, generators, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, `FrameSnapshot.custom_data`, protected presentation binder/editorial, `core/audio`, D3 V5 or E1 service. Do not change the frozen manifest. Production D renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`; no freeze/promotion.

At the start of the next window, verify actual checkout branch/HEAD/worktree and exact installed V2 hashes; read this prompt, the V37 current authority, V37 gate matrix, V14 backlog, V3 E4A.2 increment, V1 failure analysis and V27 roadmap. Do not rely on partial handoff ZIP as a replacement for the checkout.
