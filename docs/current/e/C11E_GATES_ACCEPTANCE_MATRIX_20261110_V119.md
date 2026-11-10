# C11-E Gates and Acceptance Matrix — V118 (2026-11-10)

| Gate | State | Evidence / boundary |
|---|---|---|
| E0–E3 | Accepted within recorded scopes | Reuse receipts; no blanket scope expansion. |
| E4A Challenge | Accepted within recorded scope | Do not repeat accepted visual/A/V/GUI evidence. |
| E4B Loop22 | CLOSED/operator-approved | 44/44 A/V, 22/22 A/B, 25/25 tests and human visual/audio review. No rerun absent regression. |
| Historical Drill authoring | PASS | 20/20 on 24 pins; authoring adapter only. |
| E4C dynamic binder V2 | PASS active Windows | 20/20 selectors, 20/20 independent repeats, 20/20 request manifests, 20/20 lineage, 67/67 pins. Receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`. |
| E4C console runtime V3 | PASS active Windows | Console binary, exact 4.7.1 Mono and headless GDScript smoke PASS. Hotfix receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`. |
| A.1/A.3/B.1/D.1 operator decisions | PASS / bounded | Exact-hash approvals in decision record `49efd549…`; D-owned design/contract and technical delivery envelope only. No renderer/media/audio selection/generation authority. |
| A.3 review-manifest lineage refresh | PREPARED / pending install | V4 makes explicit third replacement: old manifest `2075da…` → current `570209…`, only `/source_lineage/6/sha256`; preserves historical archive and approval state. |
| A.3 field-window + lineage tests | PASS isolated | 33/33; active Windows staged pre-write execution pending. |
| E4C phase/ownership audit | PASS isolated | 5/5; 8 protected C11-C source pins, 12 checks. Read-only. |
| E4C composition proposal + operator decision | PASS isolated / APPROVED_AS_PROPOSED | 7/7; exact geometry SHA approved for D-owned design/contract implementation and focused isolated visual tests only. No renderer input. |
| E4C timebase proposal + operator decision | PASS isolated / APPROVED_AS_PROPOSED | 10/10; exact GAME→final mapping SHA approved for D-owned design/contract implementation only. No resampling or renderer input. |
| E4C visual consumer | READY_FOR_D_OWNED_IMPLEMENTATION_AND_ISOLATED_PIXEL_TESTS | Both exact decisions recorded; implement only at existing D-owned boundary. Renderer-native input remains OFF. |
| E4C family A/V | NOT QUALIFIED | Existing `FAMILY_MUSIC_V4`; silent capture, independent seeds, FFmpeg/FFprobe and human review still required. D.1 is not audio-generation permission. |
| E4C Producer GUI runtime | OPEN | Must observe the existing Qt Producer route through E1 shared service. |
| E5 | PENDING | Cross-family determinism, seed isolation, profile/binder non-leakage, GUI/CLI parity. |
| E6 Smoke18 | PENDING | Six complete A/V scenarios per family. |
| E7 Matrix101 | PENDING / scoped | 54 Challenge + 27 Loop + 20 Drill target; CH_008/009 held (99 provisional) due 11s declaration vs 12s phase sum. |
| E8 | BLOCKED pending E7 | Historical C-to-E regression map, independent acceptance, freeze and separate promotion. |

C11-C 2.19.12 remains sole production authority; manifest 796,318 bytes / SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Renderer OFF; dispatch/media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 NO-GO; D10 blocked; `release_authority=NONE`.


Decision record: `C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261110_V1.json`, SHA `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`. The previous V2 installer failure was a staging-only Windows MAX_PATH issue (269-character path); no transaction began and no rollback was needed. V3 moved its temporary stage root to `%TEMP%`; V4 also fixes StrictMode mode-property enumeration and retains durable evidence under `artifacts/tests`.


V3 install gate: `STAGED_VALIDATION` failed closed after preflight because `.mode` was accessed for three non-payload manifest metadata rows. No transaction or rollback occurred. V4 changes both mode-based replacement enumerations to the 29-row `$operationEntries` subset and verifies each operation row shape; active Windows staged tests remain pending V4 execution.


V4 active Windows run: all package/AST/decision/pin/staging checks passed through `STAGED_SOURCE_AND_REPLACEMENT_PINS=PASS_13_PLUS_3`; Python compile failed closed because the resolved command was `python.exe` while the installer supplied the launcher-only `-3.13` selector. V5 adds a Python 3.13 runtime probe and uses executable-compatible arguments. No transaction occurred in V4.
