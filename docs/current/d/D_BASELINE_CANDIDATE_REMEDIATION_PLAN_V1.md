# C11-D Baseline Candidate — Remediation Plan V1

**Current candidate:** `C11-D-BASELINE-CANDIDATE-0.1`  
**Current decision:** `PREFLIGHT_PASS_CANDIDATE_FREEZE_BLOCKED_AS_REQUIRED`  
**C11-C 2.19.12:** immutable historical reference; do not alter its manifest or protected source.

## Gate 1 — Reconcile the missing legacy `c11d-control` references

The C11-C historical manifest contains four paths under `c11c-suite/c11d-control/`. The current operator tree has the directory absent and a prior quarantine event whose tree seal is internally valid, but whose per-file contents do not match the historical manifest. That prior archive and ledger event are historical evidence and must not be overwritten or deleted.

The recovery bundle `C11D_BASELINE_CANDIDATE_LEGACY_SNAPSHOT_RECONCILIATION_V1.zip` contains only the four exact historical files validated against the C manifest. Use it only if the active source directory is absent. The flow is deliberately two-step: restore the exact historical snapshot, verify each file hash, review the Maintenance dry-run, then explicitly apply canonical Maintenance quarantine with the confirmation token. The quarantine is a new append-only event with a new destination; the earlier mismatched archive remains untouched.

Before extraction:

```powershell
if (Test-Path '.\c11c-suite\c11d-control') { throw 'Legacy source already exists; stop and inspect; do not overwrite.' }
Get-FileHash '.\release\C11C_FREEZE_PACKAGE_MANIFEST.json' -Algorithm SHA256
```

The manifest hash must remain `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Extract the exact snapshot bundle at the repository root, verify the following hashes, and do not launch its `run.bat`:

```powershell
Get-FileHash '.\c11c-suite\c11d-control\main.py' -Algorithm SHA256
Get-FileHash '.\c11c-suite\c11d-control\README.md' -Algorithm SHA256
Get-FileHash '.\c11c-suite\c11d-control\run.bat' -Algorithm SHA256
Get-FileHash '.\c11c-suite\c11d-control\self_test.py' -Algorithm SHA256
```

Expected SHA-256 values:

- `main.py`: `6f428e356ba266977b4d6be1539ad5f35598040590d16c9568e29c534946f385`
- `README.md`: `05b554b7a3c3c4f34ac53c513ca8dc0a8b3342d39b4acd773290371de0ab8ec6`
- `run.bat`: `55420b2c9fe260d4af8e9654a566a63fd67afd065721e7cea6200713f8cb0150`
- `self_test.py`: `fd50a98b08cf60e72b63f1975cc1ef30de6de7bc2c2d9cbbcb9e5ce82090fda7`

Preview first:

```powershell
python .\tools\c11d\d9\maintenance.py quarantine-legacy-control
```

Review that the JSON says `WOULD_QUARANTINE`, lists four manifest references, and reports the unchanged historical manifest hash. Only if all four file hashes match the values above and no source conflict exists, apply the canonical reversible operation explicitly:

```powershell
python .\tools\c11d\d9\maintenance.py quarantine-legacy-control --apply --confirm QUARANTINE_C11D_CONTROL
```

This moves the temporary unregistered directory to a fresh allowlisted `docs/history/root_conflicts/c11d-control_quarantine_*` destination and appends the new event to the Maintenance ledger. It must not modify `release/C11C_FREEZE_PACKAGE_MANIFEST.json`, register a sixth surface, create media or grant authority. The previous mismatched archive remains preserved as historical evidence.

Verify afterward:

```powershell
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python .\c11c-suite\c11c-maintenance\self_test.py
```

Expected reconciliation state: `legacy_missing=4/4` because the historic files are absent at their original source paths, but `legacy_disposition=QUARANTINED_LEDGER_RECONCILED`, `legacy_reconciled_files=4/4`, `legacy_mismatch_files=none`, and no legacy disposition/pending-entry blockers. `freeze_eligible` remains false.

## Gate 2 — Record remaining approval/evidence gates

After the operator's confirmed D9.15 PASS/CLOSED and legacy reconciliation, this candidate preflight should still block for five independent reasons:

1. `D9_14_REAL_MEDIA_CERTIFICATION_BLOCKED` and `D4.8=BLOCKED`.
2. `D9_16_FULL_ACCEPTANCE_NOT_CLOSED` — preflight only; rerun full acceptance after authorized D9.14 evidence exists.
3. `D9_17_CLOSURE_NO_GO` — remains open until the required D9.14/D9.16 evidence is accepted and formally adjudicated.
4. `D_RENDERER_BASELINE_APPROVAL_NOT_RECORDED` — a separate D-owned renderer/baseline checkpoint with explicit approval and D4.8 governance.
5. `D_BASELINE_APPROVAL_NOT_RECORDED` — a separate checkpoint JSON bound to the exact candidate source fingerprint (excluding its own file), immutable C11-C manifest hash, approved renderer checkpoint hash, reviewer and timestamp.

Canonical D9.15 operator evidence is now PASS/CLOSED (13/13) and is consumed by the evaluator; it is no longer an outstanding blocker. The old candidate-only waiver remains historical only.

Neither this candidate preflight nor its tests may authorize D4.8, turn on a renderer, create media, create a freeze/release archive or grant release authority. `D10=BLOCKED` until a separately approved D freeze and release path exists.

## Candidate-evaluator hardening

- The read-only report includes per-file expected, ledger and archived sizes/hashes plus explicit reasons when a quarantine archive does not match C11-C historical bytes.
- The audit now requires a separate renderer baseline checkpoint and a separate exact-source candidate approval checkpoint; a missing or malformed approval cannot be unlocked by mere file presence.
- Negative acceptance is `22/22`, including a synthetic quarantine whose tree seal is valid but one file differs from the historical manifest.


## Current Windows outcome and next work — 2026-10-09

Canonical D9.15 is validated PASS/CLOSED and the last operator run reports five remaining blockers with `freeze_eligible=false`. Continue with the no-dispatch D renderer baseline preparation plan in `D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md`. Do not create an approved renderer checkpoint or exact-source baseline approval JSON until implementation, acceptance evidence and the independent governance decision genuinely exist.
