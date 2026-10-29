# C11-D D9.15 Checkpoint Consumption Integration Fix — Overlay V1

## Purpose

The canonical D9.15 operator-evidence ledger and sealed checkpoint have been finalized and validated on the user's Windows checkout (13/13 PASS pairings). The subsequent D9.16 and candidate preflight outputs still reported the operator evidence as required / candidate-only waived. This overlay wires those consumers to the existing canonical checkpoint validator.

## Contents

- Updated `tools/c11d/baseline_candidate/d_baseline_candidate.py` to validate the D9.15 checkpoint and current evidence ledger, prefer a valid canonical closure over the historical candidate-only waiver, fail closed on a present invalid/stale checkpoint, and report the remaining active D9.16 blocker count.
- Updated `tools/c11d/d9/full_acceptance.py` so D9.16 projects D9.15 as `PASS_CLOSED` only when the sealed checkpoint and live evidence hashes validate. It removes only the satisfied D9.15 blocker from the dynamic blocker list; D9.14 remains blocked and D9.16 full acceptance remains blocked.
- Added a candidate regression that creates a synthetic ledger/checkpoint in an isolated temporary folder and rejects checkpoint tampering and evidence-byte drift.
- Updated the focused tests and aggregate Suite contract so the current sealed D9.15 result is recognized, while the older candidate-only waiver path remains covered for trees with no canonical checkpoint.
- Updated current handover, start prompt, roadmap, D9.14/D9.15/D9.16 checkpoints, D9 changelog and a history record.

## Preparation verification

- Python compilation: PASS for all modified Python files.
- `test_full_acceptance.py`: PASS in both states: checkpoint absent (`D9.15_operator_evidence=REQUIRED`) and canonical sealed checkpoint present (`D9.15_operator_evidence=PASS_CLOSED`). In both states the preflight remains `full_acceptance=BLOCKED_AS_REQUIRED`, D9.14 blocked, renderer off and no media.
- `test_d_baseline_candidate.py`: PASS in both states: candidate-only waiver fallback and canonical D9.15 closure. Candidate remains `freeze_eligible=false`; the five non-D9.15 blockers remain when legacy quarantine evidence is reconciled.
- `test_operator_evidence.py`: PASS, 13/13 fixture pairings and 10/10 negatives.
- D9.15 static preflight: PASS, 8/8 capabilities, 5/5 surfaces, 19/19 negatives. It still says `operator_confirmation=REQUIRED` by design because static preflight is not allowed to infer human evidence.
- D9.14 gate test: PASS with `BLOCKED_AS_REQUIRED`, 10/10 cases and 20/20 negatives.
- The aggregate Suite run in the reconstructed preparation tree stopped at the Maintenance step because that isolated base lacks the active Windows D9.11 quarantine ledger. That is not claimed as a pass or as a defect fixed by this overlay; the user's active Windows checkout must rerun the aggregate.

## Governance invariants

- C11-C 2.19.12 and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` remain immutable. Expected manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- D9.10 adapter remains `PREPARE_ONLY`; no renderer input or dispatch.
- D9.14 remains `BLOCKED_AS_REQUIRED`; D4.8 remains `BLOCKED`; renderer OFF; no media; `release_authority=NONE`.
- D9 remains OPEN; D9.16 and D9.17 are not closed; D10 remains BLOCKED. No baseline freeze is authorized.
