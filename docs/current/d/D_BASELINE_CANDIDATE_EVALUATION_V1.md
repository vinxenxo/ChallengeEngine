# C11-D Baseline Candidate Evaluation V1

**Candidate:** `C11-D-BASELINE-CANDIDATE-0.1`  
**Status:** `PREFLIGHT_PASS_CANDIDATE_FREEZE_BLOCKED_AS_REQUIRED`  
**Purpose:** test whether the integrated D working tree can become the next frozen operating baseline while C11-C 2.19.12 remains an immutable historical/certified reference.

## Decision boundary

This is a candidate-evaluation track, not a freeze or release. C11-C is not replaced in-place: its source tree, renderer/simulation truth, and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` stay immutable. D is being evaluated as a prospective successor baseline for future D development, including a future D-owned renderer implementation if approved. No reuse of the frozen C11-C renderer to materialize universal D editorial bindings is authorized by this candidate preflight.

## Current integrity results

- Historical C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- The source manifest lists 2,545 original entries. The audit distinguishes entries present at their original paths from missing historical references.
- Missing non-legacy paths are fatal integrity errors. The only exception is the exact `c11c-suite/c11d-control/` legacy tree; missing references remain a freeze blocker unless the D9.11 append-only ledger proves `QUARANTINED`, the destination path is in the exact quarantine allowlist, the destination tree hash matches, all four manifest-listed file hashes/sizes match, and the historical manifest hash is unchanged.
- Protected C paths (core, assets, challenges, schemas, tests, plus critical root engine/project files) must match each historical entry byte-for-byte. The summary distinguishes source-path presence from hash-verified archival reconciliation.
- Existing D integration changes to C-manifest-listed files are accepted only inside the declared integration/documentation roots (`c11c-suite/`, `definitions/c11d/`, `docs/current/d/`, `docs/current/suite/`, `tools/c11d/`). Any drift outside these roots fails the candidate audit.
- The active GUI topology remains exactly five surfaces: Test, Producer, Catalog, Config and Maintenance.
- The candidate tree fingerprint is recomputed from current non-transient source files on every run; the report is sealed and is not written to disk by the evaluator.

## Why a freeze is not eligible

1. D9.14 has no real-media acceptance evidence authorized through the universal GUI. The real-media gate correctly remains blocked.
2. D4.8 is `BLOCKED`; no candidate tool or GUI route may change this.
3. D9.15 operator evidence covering all eight capabilities across all five surfaces is not recorded as a consolidated ledger.
4. D9.16 has only a fail-closed preflight PASS, not full acceptance against real-media/operator evidence.
5. D9.17 records NO-GO; D9 remains open and D10 remains blocked.
6. The D renderer baseline approval checkpoint is absent. The candidate track does not itself supply approval or a renderer adapter.
7. The unregistered `c11c-suite/c11d-control` legacy tree requires explicit, reversible Maintenance disposition. If absent without a valid QUARANTINED ledger and matching archived tree, the audit reports four unresolved manifest references and remains blocked. This evaluator never moves it.

## Run

```powershell
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python .\c11c-suite\c11c-config\self_test.py
python .\c11c-suite\c11c-config\test_config_gui_contract.py
python .\c11c-suite\c11c-test\test_d9_test_integration.py
python -u .\c11c-suite\self_test.py
```

The first test is also registered in the existing Test 0.2.0 GUI as `D BASELINE CANDIDATE INTEGRITY PREFLIGHT (NO FREEZE)`. Expected status is a **passing preflight with freeze eligibility false**. On trees where `c11d-control` is physically missing and there is no valid D9.11 quarantine ledger, expect `manifest_paths_present=2541/2545`, `legacy_missing=4/4`, and `legacy_disposition=SOURCE_MISSING_UNTRACKED`. This is an explicit blocker, not an accepted quarantine. Passing proves the audit classifies the condition correctly and C protected source integrity is preserved; it does not close D9 or grant release authority.

## Non-negotiable invariants

`master_seed=NOT_ADOPTED`; gameplay seed remains `request.seed`; music seed remains `request.music_seed`; cross-domain sharing forbidden; auto/runtime derivation disabled; `D4.8=BLOCKED`; renderer and production execution false; media creation false; `release_authority=NONE`; Longform remains disabled. No release or freeze archive is created.
