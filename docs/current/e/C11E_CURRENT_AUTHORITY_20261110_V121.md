# C11-E Current Authority — V120 (2026-11-10)

## Active authority and frozen boundaries

The active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` is authoritative. ZIPs/snapshots are read-only and are never extracted over it. Operator manages commits; Git/HEAD/status/branch checks are skipped. Source SHA-256 pins and the frozen C11-C manifest are mandatory.

C11-C 2.19.12 remains the only production authority. Frozen manifest: 796,318 bytes / `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Preserve all protected mechanics, generators, core audio, binders, timelines, RNG, simulation truth and canonical definitions. No sixth suite module, second Producer, parallel binder or `c11d-control`.

## Accepted evidence — never repeat absent pin drift

- E4A Challenge: accepted within its recorded scope.
- E4B mapping, R1P 27/27, Loop22 projection 22/22, policy fingerprints and R1V ten-output pilot: accepted.
- E4B Loop22: CLOSED/operator-approved; 44/44 A/V, 22/22 A/B, 25/25 tests. Run `L22_191801_27ABF3`; bridge receipt `009c9c4f3dfda17fd3455b0a26a427bc5cd55e78b4437e265a5b7a0a9d291b32`; report `d8f7050f952b7248b24763abde20ce52bf812c3934738f14670a0a3dc0c72068`; evidence ZIP `5ab13d933b4c4535b9cf90d417ff51d7342c7673329203d72fceaeea8b127f4f`.
- Historical Drill authoring adapter: accepted 20/20 on 24 source pins.
- E4C dynamic binder V2: **active Windows PASS**. Run `DRILLV2_20261110T151200Z_626a7d5e`; 20/20 selectors, 20/20 independent repeats, 20/20 request manifests, 20/20 lineage, 67/67 source pins. Receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`.
- E4C Godot console hotfix V3: installed PASS; receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`; exact Godot 4.7.1 Mono console smoke PASS; preflight reuse receipt `9484a8fae7382d3e25159c347a6979514256009c5d2b7bbc8d7cbb2741b12672`.

## A.1/A.3/B.1/D.1 approval reconciliation

The exact operator record `docs/current/e/C11E_E4B_OPERATOR_POLICY_DECISION_RECORD_20261106_V1.json` (SHA `49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04`) explicitly approves A.1, A.3, E4B Loop composition, B.1 and D.1 against their recorded exact proposal hashes. Scope is D-owned design/contract implementation only. B.1 approves preservation of delivery cadence/frame order/duration without resampling. D.1 approves only a technical delivery envelope; it does **not** authorize audio asset selection, generation, mixing, mastering, silence policy or loudness. No decision authorizes renderer input, dispatch, media or release.

A.3 proposal remains SHA `609a4d183aac07c2cbe1abaf41444160fdd137217faffbead3aef618320d57dc`. The approved A.3 source lineage points to the historical review manifest `2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470`. Active V109 source has that same preimage. The current D review manifest successor is exactly `5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795`, produced by replacing only `/source_lineage/6/sha256` from old D9.8 model hash `50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53` to current D9.8 model hash `dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb`. The byte length remains 8,591 and all approval booleans remain false.

**Important installer correction:** the first prepared A.3 overlay assumed the current manifest already had the `5702092…` postimage. That assumption did not match the V109 source (preimage `2075da…`). V2 corrects this by explicitly including the manifest as a third pinned replacement, preimage `2075da…` → postimage `5702092…`, and adds the exact historical bytes as an add-only archive. It no longer treats the desired postimage as an existing source pin. The bridge V2 records this transition honestly; it does not claim the current file was never changed.

The D9.8 model itself is not asserted byte- or semantically equivalent to its predecessor. D9.9 plan-only compatibility remains distinct from D4 executable compatibility.

## New Drill operator decisions — exact-hash approvals

The explicit operator message `APPROVED AS PROPOSAL` is recorded in `C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261110_V1.json` (SHA-256 `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`). Geometry SHA `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09` and timebase SHA `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8` are each marked `APPROVE_AS_PROPOSED`. This grants D-owned design/contract implementation and focused isolated visual/pixel tests only. Renderer input/activation, dispatch, media/audio creation, C11-C mutation and release remain unauthorized.

## E4C Drill source findings

Read-only C11-C source audit (8 exact C11-C pins / 12 checks) confirms `PRE_ROLL` 3s → `GAME` → `END_CTA` 3s → `DONE`. `VisualContentPlayer` passes a global frame index for PRE_ROLL and END_CTA but passes `_current_frame_index` (local GAME index) to the binder during GAME. Native `VisualDrillEndCTA` owns the source-frame header during END_CTA; `C11CVisualEditorialLayer` owns native header/footer. D must remain outside the contained native frame and must suppress D editorial during PRE_ROLL/END_CTA to avoid a duplicate CTA.

The Drill outer-band geometry is approved as proposed by exact hash `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09`: 720×1280 REVIEW_720, 192px top/bottom bands and a 504×896 uniformly contained source viewport at x=108,y=192; no crop/stretch/resampling. D editorial is visible only during GAME and suppressed in PRE_ROLL/END_CTA.

A separate timebase proposal now states the source-derived candidate formula `final_presentation_frame_index = pre_roll_frames + game_payload_frame_index`; at 30 fps, PRE_ROLL=90, GAME=630, END_CTA=90, total=810, and GAME frames map `[0,630)` → `[90,720)`. The D fields are proposed visible only during GAME and suppressed during PRE_ROLL/END_CTA. The timebase proposal is approved as proposed by exact hash `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8`. Both decisions are recorded independently in `C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261110_V1.json`; the proposals remain immutable and their own status fields remain `PROPOSED_NOT_APPROVED_NOT_RENDERER_INPUT`.

## A.3/Drill staged validation

Reference-tree validation against V109-derived sources plus the three pinned replacement postimages passed: field-window/lineage 33/33 (the prior 31 plus explicit positive/negative manifest-replacement disclosure tests), phase ownership 5/5, Drill composition 7/7, timebase 10/10, and py_compile for eight Python modules. This is isolated reference-tree validation, **not** a Windows active-checkout result. V4 installer repeats only these changed-source tests in a short `%TEMP%` staging root (to avoid Windows MAX_PATH) before any write. The previous V2 attempt stopped during staging at a 269-character path; it reported `rollback=NOT_NEEDED` and performed no source or overlay-destination writes; the installer did create its run-specific evidence directory and failure JSON under `artifacts/tests`. V4 retains the short-stage strategy introduced by V3 and adds the StrictMode-safe payload-only operation scope. Accepted E4C 20×2 binder, E1 32/32, D9 preflights, Loop22 and historical authoring remain reused.

## E4C remaining gates

- A.3 source lineage pointer replacement + bridge: pending installation of V4 overlay; postimage `5702092…` only after receipt.
- Drill phase ownership audit: PASS_READ_ONLY design evidence.
- Drill outer-band geometry/composition: APPROVED_AS_PROPOSED, D-owned design/contract scope only; exact record SHA is in the V4 docket.
- GAME→final-presentation timebase: APPROVED_AS_PROPOSED, D-owned design/contract scope only; exact record SHA is in the V4 docket.
- D-owned visual consumer, typography/font shaping, clipping/overflow/contrast/pixel tests: now authorized for implementation and focused isolated testing at the existing D boundary; not renderer-native input and not media creation.
- Native Drill A/V: not qualified; preserve `FAMILY_MUSIC_V4`, silent C11-C capture, independent gameplay/music seeds, FFmpeg/FFprobe and human playback review. D.1 does not authorize audio creation.
- Existing Producer Qt GUI runtime observation: OPEN.

## Forward roadmap

Complete approved D-owned visual consumer and pixel proof → native family A/V/human/GUI acceptance → E5 cross-family determinism, seed isolation and profile/binder non-leakage plus GUI/CLI parity → E6 Smoke18 (six full A/V scenarios per family) → E7 Matrix101 (54 Challenge + 27 Loop + 20 Drill; CH_008/009 held; 99 provisional) → E8 full historical C-to-E regression map, independent acceptance, immutable freeze and separate explicit promotion/cutover.

## Permanent controls

PowerShell 5.1; Python 3.13; Godot 4.7.1 Mono console. `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`. Installers verify complete package inventory, canonical frozen SHA, every pin/preimage/postimage, AST, staged tests, separate stdout/stderr, exit codes, non-null backups and rollback. Never repeat accepted evidence without drift; stop at the first failure. Renderer OFF; dispatch/media false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 NO-GO; D10 blocked; `release_authority=NONE`.


## A.3 / Drill overlay installation recovery — V4 current handoff

V2 stopped at `STAGED_VALIDATION` because a source path was 269 characters; rollback was not needed. V3 proved the short `%TEMP%` stage (55-character root), PowerShell 5.1 AST, package inventory (29 payload files), 13 supporting source pins, 29 destination states and both exact-hash operator approvals. It then stopped in `STAGED_VALIDATION` because `Set-StrictMode -Version 2.0` rejects reading a missing `.mode` property from non-payload rows in `PACKAGE_CONTENTS_MANIFEST.json` (README, correction record and package manifest). No payload transaction began; rollback remained `NOT_NEEDED`. The run-specific evidence directory and failure JSON were written under `artifacts/tests`, but no repository source or overlay destination was changed.

V4 fixes the root cause by using `$operationEntries`—the already validated `payload/` subset—for both staged replacement-postimage verification and receipt replacement enumeration. It validates required operation metadata on those 29 rows and keeps the three package metadata rows outside all mode-based operations. It retains the 55-character `%TEMP%` staging design and 240-character guard. V4 must pass PowerShell 5.1 AST, complete inventory/member hashes, 13 pins, 3 replacement preimages / 26 add-only destination states, staged 8-module `py_compile`, tests `33+5+7+10`, and pre-transaction rechecks before writes.

Both Drill proposals remain approved under exact operator record SHA `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`, but only for D-owned design/contract implementation and isolated visual/pixel tests. No renderer input/activation, dispatch, media/audio creation, C11-C mutation or release authority.
