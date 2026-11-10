# E4C A.3 lineage, phase ownership and Drill design contract reconciliation — V2

**Date:** 2026-11-10. This version supersedes the uninstalled V1 overlay package. It corrects the installer assumption that the current D editorial review manifest was already present at its postimage.

## Active-source discrepancy and correction

The V109 source inventory contains `D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json` at preimage SHA `2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470`. The target D9.8-lineage refresh is deterministically produced by replacing exactly one occurrence of old D9.8 model pointer `50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53` with current model SHA `dabb458fc2215156ddb5ebea7e8ebec811098886ce2858733ba9fb13f6075ccb`; resulting postimage SHA is `5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795` and byte length remains `8591`. JSON structural diff is exactly `/source_lineage/6/sha256`; approval booleans and all other JSON values remain unchanged. The archived preimage is added at `docs/history/c11e/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1_PRE_D98_LINEAGE_REFRESH_20261106.json`.

V2 includes this as the third explicit REPLACE operation (preimage `2075da9c33c689861a68d3bd8fb19b7ed593c6e76010ab200880746aa6d1a470` → postimage `5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795`), not as an assumed source pin. The A.3 proposal and operator decision record remain immutable. Bridge V2 SHA `aec0e387f167f4b821b7d94f06a67f78f498be939fe3cda857d20ce550819cac` accurately records the replacement. The D9.8 predecessor and successor models are not claimed byte- or semantically equivalent.

## Operator decision semantics

A.1, A.3, E4B Loop composition, B.1 and D.1 already have explicit exact-hash `APPROVE_AS_PROPOSED` decisions in record `49efd5494f351f09d7597c4699e9c12e361b36884b6bfadacd822e6ff1480e04`, limited to D-owned design/contract and technical delivery-envelope scope. B.1 does not define the phase-specific Drill GAME offset. D.1 does not authorize audio asset selection or audio generation.

## C11-C Drill source behavior

Eight protected C11-C source files are pinned. The player executes PRE_ROLL 3s, GAME N frames, END_CTA 3s, DONE; the GAME binder argument is local `_current_frame_index`, whereas PRE_ROLL and END_CTA arguments are global presentation indices. Native VisualDrillEndCTA owns the source header during END_CTA, and the shared C11CVisualEditorialLayer owns the native three-line header/footer. D must preserve the source frame and avoid overlaying these native regions.

## New proposal-only work

- Outer-band composition SHA `b22f9eb6fce39f877e432ff5f0051ecf5ab8575ecb9f580fe5f158994222fc09`: 720×1280, 192px top/bottom, 504×896 uniform-contained source frame; D editorials visible only in GAME, suppressed during PRE_ROLL/END_CTA. Approved as proposed for D-owned design/contract implementation only.
- Phase-to-final timebase SHA `44ab3b0fa09a6f7d42cd8cf2f1122cada6cbffe16a7a6b53c2af5e88d5daddc8`: candidate formula `final = pre_roll_frames + game_payload_frame_index`; 30fps example 90 PRE_ROLL + 630 GAME + 90 END_CTA = 810 final frames. Exact proposal approved as proposed for D-owned design/contract implementation only.

## Validation

Prepared against V109-derived source tree with explicit manifest postimage and all package payload applied only to a disposable validation tree: 33/33 A.3/lineage tests, 5/5 phase ownership tests, 7/7 composition tests, 10/10 timebase tests, 8-module py_compile. This is isolated reference validation, not active Windows acceptance. Windows installer repeats only changed-source suites before any checkout writes. Accepted binder 20×2, E1 32/32, D9, Loop22 and authoring evidence are reused.

## Governance

C11-C 2.19.12 remains authoritative; no C11-C files changed. Renderer OFF; dispatch/media/audio generation false; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/16 BLOCKED; D9.17 NO-GO; D10 blocked; release NONE.


## Operator approval update (2026-11-10)

The operator message `APPROVED AS PROPOSAL` is stored in the separate decision record with SHA-256 `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`. Both proposals remain immutable; approval does not enable renderer-native input, media/audio creation, dispatch, C11-C mutation or release.


## Installer recovery history

- V2: staged source path reached 269 characters; stopped before transaction, rollback not needed.
- V3: `%TEMP%` stage root 55 characters and all package/pin/destination preflight checks passed; staged validation then hit PowerShell StrictMode because `.mode` was queried on non-payload package metadata entries. Stopped before payload transaction, rollback not needed; run evidence/failure JSON was written under `artifacts/tests`, with no repository source or overlay destination changed.
- V4: mode-based replacement postimage verification and receipt enumeration are restricted to `$operationEntries`, the validated payload-only subset. Three package metadata rows remain hash/inventory members but are not transaction operations. The next expected validation is active Windows staged compile/tests before the first write.


## V4 → V5 Python invocation correction

V4's active Windows run confirmed ZIP SHA, PowerShell AST, 29 operations/3 metadata, two exact operator approvals, 13 support pins, 29 destination states, short staging, and 13+3 staged source/replacement pins. It then failed at `py_compile`: the resolved executable was `C:\Users\...\Python313\python.exe`, but the argument vector included `-3.13`, a `py.exe` launcher option. CPython reported `Unknown option: -3`. V5 removes the launcher selector, discovers `python.exe`, verifies Python 3.13 via `sys.version_info`, and runs compile/tests directly. Failure was pre-transaction; rollback not needed.
