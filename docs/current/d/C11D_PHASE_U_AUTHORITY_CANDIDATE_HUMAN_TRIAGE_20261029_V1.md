# C11-D Phase U — Authority Candidate Human Triage V1

## Purpose

Convert the recorded Phase T inventory into a review queue. This is a prioritization helper only: it does not inspect source files outside the Phase T report, does not declare a candidate authoritative and does not approve policy or bindings.

## Input

`docs/current/d/C11D_PHASE_T_AUTHORITY_EVIDENCE_DISCOVERY_RESULT_20261029_V1.json` — immutable Phase T scan report. Phase U writes a derived JSON and Markdown report to a caller-supplied TEMP path. It does not rescan the checkout and does not modify the recorded Phase T report.

## Deterministic prioritization

- `HIGH_REVIEW_PRIORITY`: path or recorded snippet indicates issuer/signature/explicit approval, authority, release authority, baseline approval, policy adoption, decision identity, or adopted option.
- `MEDIUM_REVIEW_PRIORITY`: path or snippet signals governance, binding, renderer, policy, baseline, freeze, acceptance, release, adjudication or validation gates.
- `LOW_REVIEW_PRIORITY`: candidates that matched the Phase T discovery rules but contain no additional high/medium priority signal in the recorded path/snippets.

The score is only a stable ordering heuristic. It is not a probability and is not an authority verdict. Each candidate remains `NOT_REVIEWED` with `authority_finding=UNDETERMINED`.

## Human review checklist

For each candidate, inspect actual file bytes and source history only through a separately allowed process; compare SHA-256 to Phase T; establish issuer and role, exact decision IDs and scope, clear adopted option/value, effective version/date, immutable record/signature, conditions, and required gates. Distinguish proposals, tests, examples, generated artifacts, and rejection/parking decisions from actual approvals.

Every Phase T unsearched document remains `NOT_INSPECTED`; triage preserves its path and exclusion reason. No global absence claim can be made from Phase T/Triage coverage.

## Acceptance conditions for Phase U inventory

- Input Phase T report SHA verified and status consistent.
- All 107 candidate records preserved exactly by path/hash, unless the input changes (then rerun from the updated source report and create a new version).
- All seven unsearched-document records preserved.
- Output JSON schema and 40 static tests pass.
- Human adjudication remains separate; no policy adoption and no renderer/bindings changes.

## Governance locks

`renderer=OFF`; media and payload not materialized; all approved binding counters 0; `release_authority=NONE`. CHALLENGE_008/009 remains blocked at 11 s declared versus 12 s phase sum, with no inferred correction. C11-C remains authoritative.
