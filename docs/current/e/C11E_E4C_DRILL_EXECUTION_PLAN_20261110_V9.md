# C11-E E4C Visual Drill Execution Plan — V8 (2026-11-10)

## Accepted gates retained

- Dynamic binder V2 active-Windows PASS: run `DRILLV2_20261110T151200Z_626a7d5e`; 20/20 selectors, 20/20 independent runtime repeats, 20/20 request manifests, 20/20 lineage, 67/67 source pins. Receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`.
- Godot console runtime hotfix V3 and headless smoke: PASS; receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`. Preflight reuse receipt `9484a8fae7382d3e25159c347a6979514256009c5d2b7bbc8d7cbb2741b12672`.
- E1 service 32/32, existing D9 regressions and Loop22/authoring proofs are reusable; no repeat absent pin drift.

## A.1/A.3/B.1/D.1 policy scope

Operator decision record SHA `49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04` explicitly approves A.1, A.3, E4B Loop composition, B.1 and D.1 by exact proposal hashes. Its scope is D-owned design/contract implementation and technical delivery-envelope review only. D.1 does not authorize selecting/generating/mixing/mastering audio or loudness policy. Renderer, media and release remain unauthorized.

A.3 stale dependency is reconciled as one exact D9.8 pointer change. V4 installs a 3rd replacement: current editorial review manifest preimage `2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470` → postimage `5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795`; the sole JSON Pointer delta is `/source_lineage/6/sha256`, updated to D9.8 model `dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb`. The archived historical bytes are added separately. The bridge V2 truthfully marks the current manifest replacement and confirms approval booleans unchanged.

## Source phase / ownership facts

Pinned C11-C source confirms PRE_ROLL 3s → GAME → END_CTA 3s → DONE. During PRE_ROLL, the player passes the global presentation index; during GAME it passes `_current_frame_index` (local GAME payload index); during END_CTA it passes the global presentation index. Native `VisualDrillEndCTA` owns the C11-C source-frame header during END_CTA; the C11-C shared editorial layer owns native header/footer. D fields must not occupy those source-frame slots and are proposed suppressed during PRE_ROLL/END_CTA.

## Two new exact-hash decisions — approved

1. Outer-band geometry/composition proposal, exact SHA `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09`, approved as proposed in the exact-hash operator decision record. Candidate: REVIEW_720 720×1280, 192px top and bottom bands, 504×896 uniform-contained original C11-C frame. Preserve source frame order/FPS/count; no crop/stretch. Approved as proposed for D-owned design/contract implementation and focused isolated visual tests only.
2. GAME payload → final presentation timebase proposal, exact SHA `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8`, approved as proposed in the exact-hash operator decision record. Candidate formula: `final_presentation_frame_index = pre_roll_frames + game_payload_frame_index`; at 30fps and 630 GAME frames, PRE_ROLL=90, GAME maps `[0,630)` to `[90,720)`, END_CTA `[720,810)`. D editorial suppressed during PRE_ROLL/END_CTA; native CTA remains. Approved as proposed for D-owned design/contract implementation only; no renderer input or media creation.

A.3's approved field span is `[0, actual_GAME_payload_frame_count)`; this proposal maps that window to the correct final stream interval without resampling or altering C11-C. B.1 cadence approval is not itself approval of this phase-specific offset.

## Overlay V4 pre-write acceptance

V4 installer must verify full package file inventory/bytes/SHA; canonical frozen C11-C hash; 13 supporting source pins; all three replacement pre/post states; all 26 add-only destinations; PowerShell 5.1 AST; stage active source plus payload; compile eight Python modules; run only changed suites 33+5+7+10; recheck support pins/replacement states immediately before writes. Use journal-before-mutation, non-null backups, atomic replacement, hash-guarded reverse rollback and separate stdout/stderr. No Git.

## Next implementation and family closeout

With both exact-hash decisions recorded: source-pin the D-owned consumer, implement at the existing family boundary, and prove all 20 selectors with phase-specific text visibility, long/empty/UNKNOWN cases, font shaping/coverage, clipping/overflow/contrast and deterministic source-frame identity. Do not mutate C11-C. Then native Drill A/V using silent protected C11-C capture, existing `FAMILY_MUSIC_V4` (not D3 V5), separate gameplay/music seeds, FFmpeg/FFprobe and human listen/review. Observe existing Producer GUI through E1 shared service.

E4C full closure → E5 cross-family determinism/seed isolation/profile non-leakage/GUI-CLI parity → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held) → E8 historical regression map/independent acceptance/freeze/separate promotion.

Renderer OFF; dispatch/media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 NO-GO; D10 blocked; release NONE.


The explicit operator approval record is `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`. It does not authorize renderer-native input, renderer activation, dispatch, media/audio creation or release.


## V4 installer recovery test

V2 path-length failure was corrected by V3: stage root now uses `%TEMP%` (55 chars) with a 240-character projected-path ceiling. V3 then exposed a PowerShell StrictMode bug: two replacement-mode filters traversed all content-manifest rows, including three package metadata rows without a `.mode` property. V4 limits both filters to `$operationEntries` (payload-only), adds a required-field guard, and keeps package metadata outside operation-state logic. Both failures occurred before the payload transaction, so no repository source or overlay destination was changed. The installers did create their run-specific evidence directories and failure JSON under `artifacts/tests`.


## V5 Python runtime correction

V4 reached `STAGED_VALIDATION` and stopped at `py_compile` with `Unknown option: -3`. The selected executable was `Python313\python.exe`, not the `py.exe` launcher. V5 resolves an actual `python.exe`, runs a `-c` version probe, requires `sys.version_info[:2] == (3,13)`, then invokes `python.exe -m py_compile` and `python.exe <test.py>` without `-3.13`. This is the correct invocation for the executable path present on the operator's Windows machine. The V4 failure was pre-transaction; no repository writes occurred.
