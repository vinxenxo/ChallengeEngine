# C11-D Phase W — Authority Candidate Source Human Review V1

## Goal

Prepare a read-only review queue from the accepted Phase U triage and Phase V current-source inventory. Confirm current source hashes/bytes against both inputs; preserve all candidates and excerpts; keep findings undetermined. This phase facilitates human review and does not itself establish authority.

## Inputs

- Phase U triage result JSON SHA-256: `4db4ab20040b68872c4501dc39dda61b7ca2d8716303a536dbdd4121929ec418`.
- Phase V source review result JSON SHA-256: `1c36ee0afc5bcb4a9ea5b9060487d172c9f251fe366205a8cdaaea2bfc31de67`.
- Expected records: 107 candidate sources (50 high, 55 medium, 2 low) and 7 previously unsearched documents.

## Required handling

1. Verify root-containment, current SHA-256 and byte length for all 107 candidates against Phase U and V records.
2. Keep all candidate records `NOT_REVIEWED`, `UNDETERMINED`, `full_document_inspected=false`. Excerpts are bounded navigation aids only.
3. Re-verify the seven unsearched paths and capture only path, reason, existence, hash and size. Do not read their content in this automated preparation step. Mark `content_read=false`.
4. Retain the 11s declared versus 12s phase-sum conflicts for CHALLENGE_008/009 without correction.
5. Emit an immutable-content JSON/Markdown packet and test it with Phase W's 40-test suite and verifier.

## Human authority-review checklist

For every full source selected for review, record the exact source path and current SHA, issuer and evidence of delegated authority, effective date/version, decision IDs, exact adopted option and scope, constraints/exceptions, signature or immutable record identity, dependencies and required follow-on tests. Distinguish authoritative decision record from proposals, test fixtures, issue text, logs and stale copies. A file name, keyword match, high priority or green test does not constitute authorization.

## Governance locks

`renderer=OFF`; approved binding counters zero; release authority `NONE`; policy adoption `NONE`; source review must not modify candidate files. No global absence claim is allowed because Git history, external files and the contents of seven unsearched documents remain outside this preparation. C11-C remains the production baseline. This queue is not approval to enable renderer, materialize payload/media or run a production render.
