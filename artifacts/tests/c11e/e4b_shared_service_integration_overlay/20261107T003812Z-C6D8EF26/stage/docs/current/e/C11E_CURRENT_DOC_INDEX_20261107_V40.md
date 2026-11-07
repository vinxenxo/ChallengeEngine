# C11-E Current Document Index — V40

**Date:** 2026-11-07. Authority: active Windows checkout only. See `C11E_CURRENT_AUTHORITY_20261107_V80.md` first.

## Current authority and execution

- `docs/current/e/C11E_CURRENT_AUTHORITY_20261107_V80.md` — live state, accepted evidence, exact Loop service integration scope and global controls.
- `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261107_V55.md` — ordered next work and expected operator actions.
- `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261107_V78.md` — gate-by-gate status; no implicit promotion.
- `docs/current/e/C11D_E_BLOCKER_REMEDIATION_REGISTER_20261107_V1.md` — consolidated D/E blocker owner, evidence, dependency and exit criteria.

## D9.8 / D9.9 and E4B Loop

- `docs/current/e/C11E_E4B_D98_D99_SEMANTIC_RECONCILIATION_20261107_V2.md` — plan-only versus executable compatibility.
- `docs/current/e/C11E_E4B_LOOP_SHARED_SERVICE_INTEGRATION_REVIEW_20261107_V1.md` — six source deltas, 27-selector shared service contract, tests and non-dispatch boundary.
- `docs/current/e/C11E_E4B_LOOP_FAMILY_CONTRACT_AUDIT_SEMANTICS_20261107_V2.md` — V2 audit semantics; historic file-existence count is not visual evidence.
- `docs/current/e/C11E_E4B_LOOP_FAMILY_CONTRACT_TEST_FAILURE_REVIEW_20261107_V1.md` — preserved V1 test incident.
- `docs/history/c11d/C11E_E4B_LOOP_INTEGRATION_DECISION_HISTORY_20261107_V1.md` — V1 failure, V2 repair, operator approvals and current integration stage.
- `tools/c11d/d9/C11E_E4B_SHARED_SERVICE_INTEGRATION_V1_SOURCE_PINS.json` — preimage/postimage hashes for the six narrowly patched source/test files.
- `tools/c11d/d9/RUN_C11E_E4B_SHARED_SERVICE_INTEGRATION_V1.ps1` — PS 5.1 focused runner with separate read-only D9.15 and D baseline diagnostics.
- `tools/c11d/d9/C11E_D_BASELINE_READ_ONLY_DIAGNOSTIC_V1.py` — read-only D baseline candidate preflight; never repairs or synthesizes evidence.

## Roadmap and prompts

- `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261107_V68.md`
- `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261107_V78.md`
- `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261107_V78.md`
- `prompts/C11E_FIRST_PROMPT_20261107_V22.md`

## Historical references — preserve, do not overwrite

- E4B V1 failed runner remains historical; V2 corrected its `ProjectRoot` MP4-observation semantics.
- E4B V2 Windows evidence remains accepted for its stated static scope (8/8, 27/27 selectors, 40/40 base pins, 8/8 local pins). Its pinned audit test is not rerun after this service integration changes the referenced E service/GUI hashes.
- D9.15 original sealed checkpoint and append-only ledger remain historical evidence; V79 snapshot revalidation is separately reported as blocked by absent image evidence. Revalidate on the live checkout; do not reinitialize.

## Do not repeat

E4A accepted test-only evidence; E4B 81-case family matrix; five operator policy decisions; E4B V2 Windows audit. Reopen only on source drift or a regression directly affecting the accepted evidence.
