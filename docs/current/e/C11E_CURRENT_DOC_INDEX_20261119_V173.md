# C11-E Current Document Index — V173 (2026-11-19)

## Current authority
- `C11E_CURRENT_AUTHORITY_20261119_V177.md`
- `C11E_GATES_ACCEPTANCE_MATRIX_20261119_V172.md`
- `C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261119_V122.md`
- `C11E_E3_EXECUTION_BACKLOG_20261119_V148.md`

## E6 Smoke18 — Challenge editorial binding
- `C11E_E6_CHALLENGE_EDITORIAL_BINDING_PREPARE_ONLY_20261119_V1.md`
- Inputs: `definitions/c11e/test_only/C11E_E6_CHALLENGE_EDITORIAL_BINDING_PREPARE_ONLY_INPUTS_V1.json` + SHA-256 sidecar.
- Python runner: `tools/c11d/d9/c11e_e6_challenge_editorial_binding_prepare_only_v1.py`
- PowerShell 5.1 runner: `tools/c11d/d9/RUN_C11E_E6_CHALLENGE_EDITORIAL_BINDING_PREPARE_ONLY_V1.ps1`
- Tests: `tests/test_c11e_e6_challenge_editorial_binding_prepare_only_v1.py`
- Expected derived evidence: `artifacts/tests/c11e/e6_challenge_editorial_binding_prepare_only/<RUN_ID>/`.

## Challenge / family editorial predecessors
- `E6_CHALLENGE_PREPARE_ONLY_ORCHESTRATOR_RECEIPT_V1.json` — 18 intents / 18 envelopes, PREPARE_ONLY.
- `E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_AUDIT_RECEIPT_V1.json` — 18 rows / 30 assignments, runtime readback not proven.
- `E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_PLAN_V1.json` — family editorial assignments.
- E4A Challenge presentation approval V1 remains the operative policy; zero-duration phase windows intentionally suppress their fields, with no phase fallback.

## Continuity prompts
- `docs/master-prompts/C11E_MASTER_HANDOVER_20261119_V16.md`
- `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261119_V186.md`
- `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261119_V187.md`
- `prompts/C11E_FIRST_PROMPT_20261119_V104.md`

## Governance
C11-C frozen manifest `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; D4.8 V2 immutable/BLOCKED; E1 PREPARE_ONLY; renderer OFF; dispatch/media false; release authority NONE. No Git checks; commits operator-managed; SHA-256 source pins enforced.
