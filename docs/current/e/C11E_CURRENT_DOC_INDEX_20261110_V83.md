# C11-E Current Document Index — V82 (2026-11-10)

## Active authority and phase

- Current authority: `C11E_CURRENT_AUTHORITY_20261110_V121.md`
- Gates matrix: `C11E_GATES_ACCEPTANCE_MATRIX_20261110_V119.md`
- Execution backlog: `C11E_E3_EXECUTION_BACKLOG_20261110_V95.md`
- E4C Drill execution plan: `C11E_E4C_DRILL_EXECUTION_PLAN_20261110_V9.md`
- Blocker register: `C11D_E_BLOCKER_REMEDIATION_REGISTER_20261110_V41.md`
- Full-family roadmap: `C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261110_V67.md`

## E4C A.3 + Drill design/contract V4 recovery overlay

- Package: `C11E_E4C_A3_DRILL_DESIGN_CONTRACT_RECONCILIATION_V4_20261110.zip`
- Three pinned replacements: current review manifest pointer refresh, field-window validator, field-window regression test.
- 26 add-only files: history bridge/archive, Drill phase audit, outer-band composition proposal/schema, phase-to-final timebase proposal/schema, validators/tests, current docs and all three prompts.
- Windows staging test counts: 33 +5 +7 +10; py_compile eight modules. V2 path-length issue and V3 StrictMode `.mode` scope issue are both corrected before transaction in V4.
- A.3 bridge V2: `C11E_E4C_A3_REVIEW_MANIFEST_LINEAGE_RECONCILIATION_20261110_V2.json`.
- Drill geometry and timebase are approved as proposed in the exact-hash operator decision record.

## Accepted evidence not to repeat

- E4B Loop22 44/44 A/V +22/22 A/B +25 focused tests + operator visual/audio approval.
- Historical Drill authoring 20/20 on 24 pins.
- E4C dynamic binder V2 `DRILLV2_20261110T151200Z_626a7d5e`, receipt `31f631c3c23c6c1d277d67f52dd887010ee51be869798ab8db3fbdec8658fa01`.
- Godot console hotfix V3 receipt `526c7d360863af8fb53707c9c83162173f4c1f1eb349ee8d767fb97665167a31`; headless smoke and preflight reuse PASS.

## Prompts (always use current versions)

- Continuation Master / Overhand: `C11E_CONTINUATION_MASTER_PROMPT_20261110_V122.md`
- Next Window Start: `C11E_NEXT_WINDOW_START_PROMPT_20261110_V122.md`
- First Prompt: `C11E_FIRST_PROMPT_20261110_V46.md`

## Roadmap

E4C visual/geometry/timebase/A/V/GUI closure → E5 → E6 Smoke18 → E7 Matrix101 (99 provisional; CH_008/009 held) → E8 historical regression, independent acceptance, freeze and separate promotion. C11-C remains production authority until E8.


- `C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD_20261110_V1.json` — exact-hash geometry and timebase approvals; SHA `eb95da188065b8ebcb2371e2a6bcff6762ce000a5ca74f8ea384ecec4ee58303`.
- `C11E_E4C_DRILL_COMPOSITION_DECISION_DOCKET_20261110_V5.md` — consolidated decision scope and next gate.
- V3 installer relocates temporary staging to `%TEMP%` to avoid MAX_PATH; V2 failure was pre-transaction (`rollback=NOT_NEEDED`).


V4 root-cause correction: `PACKAGE_CONTENTS_MANIFEST.json` deliberately contains 3 non-payload package metadata rows in addition to 29 payload operation rows. Under PowerShell StrictMode, `$contents.files | Where-Object {$_.mode...}` fails on the metadata rows. Both such filters now use `$operationEntries`, which contains payload rows only. A runtime shape guard confirms mode/repo_path/preimage metadata exists on each operation row.
