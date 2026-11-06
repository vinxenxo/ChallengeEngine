# C11-E Execution Backlog — V42

## Immediate — finish E4A.6 from the already-captured AVI

Do **not** rerun the V2 full runner, Python tests, Godot import/runtime or Movie Maker capture. Their source/runtime/capture components passed. The V2 overall BLOCKED result is a launcher defect: `Test-CaptureLog` is file-path based but its new Movie Maker branch supplied `$movie.Stdout` text. The evidence log itself contains the expected configure envelope, full phase telemetry, `audio_enabled=false`, successful Movie Maker completion and a 900-frame AVI.

The recovery-only `RUN_C11E_E4A6_RESERVED_BANDS_RECOVERY_V1_2.ps1` is the sole completion step for E4A.6: it validates the uploaded V2 evidence and exact file-level source pins (no Git/HEAD/status checks), reuses the already-created 540x960/60 FPS/900-frame AVI, drops all AVI audio, emits the 720x1280/30 FPS/450-frame silent H.264 review MP4, extracts eight boundary frames, audits inactive black bands and active HOOK/CTA text, then installs new versioned docs add-only. The recovery V1 attempt stopped before evidence processing because it incorrectly required the previous Git HEAD. The operator makes a commit each iteration; no per-iteration runner may consult Git or require `.git`. V1.1 removes those checks and keeps source SHA/manifest validation. The recovery receipt must be present with `PASS_TEST_ONLY_RESERVED_BANDS_BLACK_CAPTURED`; otherwise stop at the exact failure stage rather than rerun V2. It performs no gameplay rerender and no source writes.

The delivery background colour is not a gate issue. Keep the current dark body/background presentation; user-selectable video background colour is a separate later editorial capability. Do not alter the black reserved-band rule.

## Next — full Challenge E4A audiovisual closure

After the recovery receipt reports `PASS_TEST_ONLY_RESERVED_BANDS_BLACK_CAPTURED`:

1. Reconcile exact active D3 V5 engine/spec/profile, E1 intent/resolver, D3.3 mastering and accepted E4A.4 mux/FFprobe pins with the live checkout. Reuse E4A.4 predicates/method only: its MP4 input was the prior uncomposited C11-C review video and must not be reused as this stage’s visual input. Do not guess or reuse stale pins.
2. Use the corrected D-composited MP4 unchanged. Generate actual D3 V5 audio and D3.3 mastering only; no gameplay rerender and no video re-encode.
3. Hold gameplay seed/video fixed. A/B use the same `music_seed`; C changes only `music_seed`. The earlier E4A.4 pilot used gameplay seed 314159 and music seeds 840001/840001/840002 as historical fixtures; reuse them only if the current E1 resolver and exact source pins still accept them, never as hard-coded defaults. Prove A/B raw/mastered/decoded audio repeatability and C audio difference.
4. Require identical H.264 elementary video stream/frame identity across A/B/C; one H.264 video + one AAC-LC audio stream, 48 kHz stereo, non-silent audio, exact 15 s, and start/end A/V drift <=0.15 s.
5. Preserve raw/mastered WAVs, muxed MP4s, FFprobe JSON, volume reports, commands, logs, hashes and immutable receipt. Complete operator visual/listening review and E1 GUI/CLI parity before closing E4A.

## Full family campaign

After E4A: E4B Loop (preserve C11-C grammar/variant timeline, binder and family music); E4C Drill (preserve phase timeline, binder, END_CTA precedence and family music); E5 determinism, gameplay/music seed isolation, family/profile non-leakage and GUI/CLI parity; E6 Smoke18 (six A/V cases per family); E7 Matrix101 (54 Challenge + 27 Loop + 20 Drill); E8 complete regression corpus, independent acceptance, freeze and separately authorized promotion.

CH_008/009 remain held because declared duration 11 seconds conflicts with 12-second phase sum. Do not claim Matrix101 101/101 until explicitly resolved.

## Do not repeat

Do not rerun E0–E3, E4A.2, E4A.3D.1, E4A.4, E4A.5B, E4A.6 runtime V3/V2 Python suite or V2 Movie Maker capture absent concrete pin drift or a new defect. Do not rerun recovery V1 or V1.1. Use V1.2 only if no successful receipt exists. No Git command or Git-state check is permitted in iteration runners; the operator manages commits. Never extract snapshots over checkout; no C source write or runtime source modification by recovery runner.

C11-C 2.19.12 remains production authority. Renderer/dispatch/production media OFF; `release_authority=NONE`.
