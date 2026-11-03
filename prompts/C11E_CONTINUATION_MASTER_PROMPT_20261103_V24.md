# C11-E Continuation Master Prompt — V24

## Mission

Continue the real C11-E engineering work in `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Deliver the complete three-family audiovisual production product: Challenge, Visual Loop and Visual Drill, with C11-C generators/mechanics preserved, D presentation/editorial, family-correct music with independent `request.music_seed`, FFmpeg mux, FFprobe QA and immutable run receipts.

The Producer GUI is now the primary and only manual operator workflow. CLI remains a thin compatibility adapter used by automated separate-process parity tests. Both must call one shared C11-E production service; do not duplicate business logic or create another Producer/suite surface.

## Current code authority

- Latest code commit supplied by operator: `3cc1caa6d740b1525a4ebb30a4ff7f02868ac5a8`.
- Parent: `a30b63d31b2d071ebab9c67ec9f8ff7393731488`.
- Tree: `de8a1180f04eb0f5e0ea5c8130eedaaccf7e78fa`.
- Branch `main`; last supplied status clean, `ahead 4` of origin/main.
- User commits locally each iteration. Never reset, clean, rebase, amend, push or manipulate refs.
- C11-C manifest: 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Read order

Read V24 current authority, gate matrix, execution hygiene, GUI-primary contract, E3 execution backlog, E3.2 closure record, architecture decision/backlog, E3 Challenge audiovisual plan and V14 roadmap. Then inspect active `AGENTS.md`, `.continue/rules/CONTINUE.md` and the live checkout. These generic instructions do not supersede the C11-E authority/locks. Treat E2/E3 snapshots and previous ZIPs as support only.

## Accepted state

- E0: PASS/CLOSED; reuse.
- E1 shared service automated tests: accepted; manual GUI observation was pending in historical record. Do not relabel GUI as observed without an actual Windows launch/interaction.
- E2 R4: ACCEPTED/CLOSED only for CHALLENGE_001 title-to-pixels. R4 RequestId `C11E-E2-CH001-AB-20261101-V9-R4`, receipt SHA `2f8c355453d8558c6af42aa5da35f603b767726d64ba04f842dc799a2cadef7f`, evidence ZIP SHA `f33431bb131697baf9dc3df6ed1ed8e4ca14ecb40d7b9ef07c812a5bca67a3de`. Two video-only 720×1280, 30fps, 270-frame, 9-second MP4s. Do not rerun E2.
- E3.2: PASS/committed at `3cc1caa6d740b1525a4ebb30a4ff7f02868ac5a8`. Operator ran 21/21 tests (8 E3.2 +13 E1) and seven-file postimage/protected-path audit; C11-C manifest unchanged.
- E3 physical music render, D3.3 mastering, mux, FFprobe and E3 GUI execution: NOT RUN.
- E4A/B/C, E5, E6, E7 and E8: pending/blocked behind prior evidence.

## Immediate next sequence

1. Apply and locally commit the V24 documentation overlay. Its add-only installer is pinned to the current E3.2 commit. Do not run the next code overlay until the docs commit SHA is known.
2. Capture new live HEAD/tree/status and refresh source pins from the active checkout. Reconcile the D3.0–D3.3, D9.2, C11-C family music, D9.8 editorial, D9.9 service and D9.10 boundaries. The previous V23 E3 discovery runner invocation stopped on a dirty checkout; it was not a PASS, and its pins/HEAD may be stale.
3. Launch the existing Producer GUI and record a real Windows runtime smoke. GUI is the operator workflow; no manual CLI production use.
4. Implement E3 Challenge audio attachment to the accepted R4 video, through the existing GUI and shared E service. Do not rerender gameplay. Resolve source MP4 through the immutable receipt and verify its hash.
5. Use D3 V5 + `challenge_8bit_v1`, independent music seed. For the first historical D9.2 pilot fixture only, use 104 BPM and variation 0; 104 is not a global default. Derive duration from the FFprobe-validated video (R4: 270/30 = 9 seconds); never use V5's four-second CLI fallback.
6. Preserve raw WAV. Reproduce the active D3.3 deterministic 30-second measurement/mastering process (`loudnorm I=-14, TP=-1, LRA=7`, 48kHz stereo PCM) and validate the final audio segment trimmed/aligned to the actual video duration. Never mux the 30-second measurement window untrimmed into a 9-second output.
7. Mux per the pinned D9.2 Challenge precedent (video copy, AAC 192k, 48kHz stereo, `-shortest`, `+faststart`); validate with FFprobe, exactly one video+one audio stream and duration difference <=0.15s. Compare decoded video frames to prove no visual change.
8. Prove same music seed => identical raw/mastered audio, different music seed => audio changes, and changing only music seed never changes visual frames. Add negative cases and structured receipts.
9. Test CLI in a separate process only for parity through the same service. Do not build a parallel CLI workflow.
10. After E3 acceptance, continue E4A Challenge, E4B Loop and E4C Drill, then E5, E6 Smoke18, E7 Matrix101 and E8.

## Family policy

Challenge uses D3 V5. Visual Loop and Visual Drill preserve their existing C11-C family/grammar music generator and profiles; E orchestration may call their existing audio-only entry point with `request.music_seed`, independently from visual `request.seed`, but must not modify or fork the generator. This adapter seam requires live-source verification and family regression tests. Do not force the Challenge 8-bit profile onto other families.

## Editorial/layout policy

Common enabled D9.8 fields: title, subtitle, call_to_action, language. Challenge-only: player_name, challenge_label. Reserved hook/preparation/final/header/footer/visibility fields remain disabled. Never map title to hook or CTA. Use family-specific binders/render models, preserve Loop footer omission and Drill END_CTA/phase precedence. Logical canvas 540×960 (Header 0–144, Body 144–816, Footer 816–960); REVIEW_720 720×1280 at 30fps. The CH001 E2 title slot is not a universal mapping.

## Governance

C11-C 2.19.12 remains the production baseline until E8. No `core/audio`, C generator/mechanics, manifest, D4.8 or D9.10 authority changes. Exactly five suite modules, no `c11d-control`, no auto seeds, no cross-domain RNG, fresh RequestId per physical run, isolated test roots, immutable evidence. `release_authority=NONE` until E8.
