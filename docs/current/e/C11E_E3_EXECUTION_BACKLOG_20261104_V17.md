# C11-E Execution Backlog — V17

**Date:** 2026-11-04. This revision records E4A.3 V2 acceptance and packages the next bounded E4A.4 audiovisual test. It does not change production authority.

## P0 — E4A.4 Challenge A/V review pilot

Apply `C11E_E4A4_CHALLENGE_AUDIO_MUX_OVERLAY_V1.zip` using `RUN_C11E_E4A4_FROM_DOWNLOADS_V1.ps1`. The script verifies the ZIP and every source pin, applies add-only files, executes 42 focused tests, and launches the bounded A/V runner with durable logs and a heartbeat. Do not rerender C11-C gameplay.

The runner consumes exact E4A.2/E4A.3 evidence and the immutable normalized CHALLENGE_004 video. It prepares three E1 TEST intents then invokes pinned D3 V5 and reuses the accepted E3 D3.3/mux/FFprobe helper path. Fixed gameplay seed 314159; A/B music seed 840001; C music seed 840002; 104 BPM is only the historic D9.2 fixture. It creates test-only MP4s and a ZIP receipt. The MP4s contain the unmodified C11-C normalized review video plus audio; E4A.3 PNGs are separate and are not muxed into those videos.

Accept the bounded automated gate only after inspecting the returned ZIP and its receipt/report. Operator audio listening and sync review are separate required observations. Never label the full D presentation/layout as accepted from this test.

## P1 — resolve Challenge visual layout without guessing

Use live checkout documentation and historical sources. D1.1 provides mapping, not geometry. D1.5 establishes the logical 540x960 Header/Body/Footer partition but explicitly leaves generic safe-area padding, typography and CTA geometry UNKNOWN. D1.7 inherits that contract and says UNKNOWN is not a default. E4A.3 exposed test-title collision with the existing C11-C hook and CTA collision with the existing footer text. Inspect historical `docs/history/c11/C11B0_CONTRACT.md`, `C11B1_CONTRACT.md` and corresponding scene/scripts/tests before a proposal. Do not patch C11-C, fabricate margins or enable Challenge Overlay fields until an exact safe D-owned composition is supported and reviewed.

## P2 — continue ordered family gates

After bounded E4A closure: E4B Loop → E4C Drill → E5 cross-family determinism, seed isolation, profile/adapter non-leakage and GUI/CLI parity → E6 Smoke18 → E7 Matrix101 (99 provisional, CH_008/009 held) → E8 independent historical-corpus acceptance/freeze/promotion.

## Do not repeat or modify

Do not rerun E0/E1/E2/E3/E3.2, accepted E3 negative-control suite, E4A.2 or E4A.3 V2 without a relevant source/test pin change. Do not rerun E4A.3 V1. No C11-C generator/mechanic, `core/audio`, D3 V5 engine, E1 service, frozen manifest or governance lock edits. No sixth suite module, second producer or `c11d-control`.
