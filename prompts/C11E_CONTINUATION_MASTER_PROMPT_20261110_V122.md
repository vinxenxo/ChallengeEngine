# C11-E Continuation Master / Overhand Prompt — V121 (2026-11-10)

## Project authority and mission

Continue the full C11-E production system in active checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. This checkout is the sole authority. ZIPs and snapshots are read-only evidence and must never be extracted over it. Operator manages commits; skip Git/HEAD/status/branch/.git checks. Enforce source SHA-256 pins and frozen C11-C manifest only.

Objective: one validated production service for Challenge, Visual Loop and Visual Drill, using D presentation/layout/editorial and family-correct music, FFmpeg mux/FFprobe QA and immutable receipts. Existing Producer GUI is the operator surface; CLI remains a compatibility route over the same E1 shared service. C11-C remains authoritative until E8 independent acceptance, freeze and a separate explicit promotion/cutover.

## Immutable boundaries

C11-C 2.19.12 manifest: 796,318 bytes, SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Never modify frozen manifest, protected C11-C generators/mechanics/core audio/binders/timelines/RNG/simulation truth/canonical definitions, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, or `RenderedFrameStream`. No sixth suite module, second Producer, parallel binder or `c11d-control`.

Operational rules: Windows PowerShell 5.1, Python 3.13, Godot 4.7.1 Mono console. `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`. Installers must check full archive inventory/member hashes/sizes, one canonical 64-character frozen SHA, semantic hash literals, PowerShell AST, all pre/post pins, add-only conflicts, staged tests before writes, non-null backups, journal-before-mutation, hash-guarded rollback, separate stdout/stderr and immediate native exit checks. Stop on first failure; never emit PASS after failure.

## Accepted evidence — do not repeat absent source drift

- E4A accepted within its recorded scope.
- E4B Loop22 CLOSED: 44/44 A/V, 22/22 A/B, 25/25 tests and operator visual/audio approval; no rerun.
- Historical Drill authoring 20/20 on 24 source pins; no rerun.
- E4C dynamic Drill binder V2 active Windows PASS: `DRILLV2_20261110T151200Z_626a7d5e`; 20/20 selectors, 20/20 independent repeats, 20/20 request manifests, 20/20 lineage, 67/67 pins. Receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`.
- E4C Godot console hotfix V3 installed; receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`; exact console version and headless script smoke PASS. Preflight reuse receipt `9484a8fae7382d3e25159c347a6979514256009c5d2b7bbc8d7cbb2741b12672`.

## A.1/A.3/B.1/D.1 decision record

The exact operator record SHA `49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04` explicitly approves A.1, A.3, E4B Loop composition, B.1 and D.1 against exact proposal hashes, limited to D-owned design/contract and technical delivery-envelope scope. B.1 preserves cadence/frame order/duration without resampling but does not resolve phase-specific Drill offset. D.1 does not authorize audio asset selection, generation, mixing, mastering, silence policy or loudness.

## Current E4C lineage/install position

A.3 approval already exists; do not ask again. Active V109 source has review manifest preimage SHA `2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470`. Desired D9.8-lineage-refreshed successor is `5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795`, produced by one JSON-pointer change `/source_lineage/6/sha256` to model SHA `dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb`. V2 treats this as an explicit third replacement, archives the old bytes, and records the transition. Do not assume the postimage already exists or hand-edit it.

V5 installer stages the active sources plus payload and runs only changed-source suites: A.3/lineage 33, phase ownership 5, composition proposal 7, timebase proposal 10; py_compile eight modules. All before checkout writes. It must verify 13 support pins and all 3 replacement pre/post states plus 26 add-only paths, PowerShell AST and full package inventory. No accepted binder/E1/D9/Loop22 suites are repeated.

## Drill source facts and approved proposals

C11-C Drill phases: PRE_ROLL 3s → GAME → END_CTA 3s → DONE. In `VisualContentPlayer`, PRE_ROLL and END_CTA pass global presentation indexes; GAME passes local `_current_frame_index`. Native VisualDrillEndCTA owns the source-frame header during END_CTA; `C11CVisualEditorialLayer` owns native header/footer. D fields must be outside the contained source frame and suppressed during PRE_ROLL/END_CTA.

Both new exact-hash decisions are approved as proposed and recorded in `C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261110_V1.json` (SHA `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`):
1. Outer-band geometry: `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09` — 720×1280, 192px bands, 504×896 contained source frame.
2. GAME→final presentation timebase: `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8` — `final = pre_roll_frames + game_payload_frame_index`.

Approval authorizes D-owned design/contract implementation and focused isolated visual/pixel tests only. Renderer-native input/activation, production dispatch, media/audio creation, C11-C mutation and release remain unauthorized.

Both decisions are explicitly approved. Implement only the single D-owned consumer at the existing family boundary. Do not emit renderer-native input or activate the renderer.

## Forward execution

After V5 installer PASS and receipt review, refresh D-only source pins and implement one D-owned consumer at existing boundary; test fonts/shaping, overflow, clipping, contrast, pixel identity and all 20 Drill selectors. Then qualify Drill family A/V using silent C11-C capture and existing `FAMILY_MUSIC_V4` (`tracking=FLOWING_VECTOR`, `pursuit=ORGANIC_BLOOM`, `saccade=CIRCUIT_PULSE`, `peripheral_scan=ORBITAL_RITUAL`), independent gameplay/music seeds, FFmpeg/FFprobe and human review. D3 V5 is not used for Drill. Observe the existing Qt Producer GUI via E1; verify GUI/CLI parity.

Then E5 determinism/seed isolation/profile and binder non-leakage/GUI-CLI parity → E6 Smoke18 (six full A/V cases per family) → E7 Matrix101 (54 Challenge +27 Loop +20 Drill target; CH_008/009 held, 99 provisional) → E8 historical row-by-row C-to-E regression map, independent acceptance, freeze and separate explicit promotion.

Governance stays locked: renderer OFF, dispatch/media false, D4.8 BLOCKED, D9.10 PREPARE_ONLY, D9.14/16 BLOCKED, D9.17 NO-GO, D10 blocked, `release_authority=NONE`.


V2 installation failed during staging because a stage path reached 269 characters (Windows MAX_PATH); `rollback=NOT_NEEDED`; no repository source or overlay destination was changed, although a run-specific evidence directory/failure JSON was created under `artifacts/tests`. V3 introduced the `%TEMP%` stage tree and 240-character guard; V4 retains those protections and fixes the StrictMode `.mode` lookup against non-payload metadata.


Latest installer diagnostic (2026-11-10): V3 returned `stage=STAGED_VALIDATION; rollback=NOT_NEEDED` after `ZIP_SHA256=PASS`, `POWERSHELL_AST=PASS_1_SCRIPTS`, `OPERATOR_DECISION_RECORD=PASS_2_EXACT_HASH_APPROVALS_SCOPE_LIMITED`, `PACKAGE_INVENTORY=PASS_29_PAYLOAD_FILES`, `SUPPORT_SOURCE_PINS=PASS_13`, `DESTINATION_STATES=PASS_29`, and `STAGING_ROOT=TEMP_SHORT_PATH_55_CHARS`. Root cause: PowerShell StrictMode received a `.mode` property access for a non-payload entry in the contents manifest (README/CORRECTION_RECORD/PACKAGE_MANIFEST). V4 restricts both such lookups to `$operationEntries`, validates each operation row's required fields, and excludes the three metadata records from mode-based checks. No transaction occurred in V3; do not assume A.3 installed. Run V4 and require staged tests `33+5+7+10`, 8-module `py_compile`, pre-transaction rechecks and exact install receipt before continuing to consumer source-pin capture.


Latest Windows diagnostic: V4 passed ZIP SHA, PowerShell AST, operator decision validation, 29-operation inventory, 13 support pins, 29 destination states, short staging, and staged 13+3 pins. It failed at `py_compile` with `Unknown option: -3` because `py.exe` command discovery resolved to a Python 3.13 `python.exe` executable, but V4 passed launcher-only `-3.13`. V5 selects actual `python.exe`, checks `sys.version_info` equals 3.13, and runs `-m py_compile` / test scripts without `-3.13`. V4 stopped pre-transaction; no repository writes.
