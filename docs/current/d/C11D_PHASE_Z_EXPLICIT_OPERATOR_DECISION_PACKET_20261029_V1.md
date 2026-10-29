# C11-D Phase Z — Explicit Operator Decision Packet V1

**Packet ID:** `C11D-PHASE-Z-EXPLICIT-OPERATOR-DECISIONS-20261029-V1`  
**Status:** `PREPARED_AWAITING_EXPLICIT_AUTHORITY_DECISIONS`  
**Preparation-only:** Yes · **Signed/adopted:** No

## Instructions

This packet is a template, not an approval. Record an explicit disposition for each R-01..R-09. For any adoption, complete all mandatory fields and attach the verifiable approval record. A generic instruction to continue engineering, a historical test PASS, a proposed implementation, or a narrow future-specification decision is not sufficient authority for broad product-policy adoption.

If a decision is deferred, rejected, incomplete or unverifiable, record that disposition plainly and retain `KEEP_BLOCKED_NO_POLICY_ADOPTION`. Do not enter a value by inference. Do not grant renderer, binding, payload/media, seed, freeze, promotion or release authority unless a separate valid authority record expressly grants that exact scope and the controlling gate accepts it.

## Required fields — mandatory for every adoption

1. Decision ID and exact policy text / selected option.
2. Named approving authority, role, and delegation basis/scope.
3. Decision date and effective date.
4. Rationale.
5. Source paths and SHA-256 pins.
6. Acceptance-test obligations.
7. Verifiable approval provenance or signature reference.
8. Immutable decision-record location.

## Decision rows

### R-01 — TIMEBASE-SAMPLING
- Current disposition: `NOT_ADOPTED_KEEP_BLOCKED`
- Question: Specify deterministic source-to-delivery sampling/timebase mapping and boundary/tie behavior.
- Missing: exact rule, authority scope/effective date, provenance and acceptance tests.
- Operator disposition: `PENDING` — do not infer.

### R-02 — SPATIAL-MAPPING
- Current disposition: `NOT_ADOPTED_KEEP_BLOCKED`
- Question: Adopt an exact production spatial-mapping policy, if authorized.
- Historical limitation: coordinate choices are only accepted for future consumer specification; transforms, bindings, projection and pixel placement are not authorized; crop/rounding unresolved.
- Operator disposition: `PENDING` — do not infer.

### R-03 — PILOT-SCALAR-X-AND-PRESENTATION-Y
- Current disposition: `NOT_ADOPTED_KEEP_BLOCKED`
- Question: Specify per-challenge visual semantics and separately decide whether/which production bindings are authorized.
- Historical limitation: semantics for CHALLENGE_003/005/006/007 are future-binding-specification-only.
- Operator disposition: `PENDING` — do not infer.

### R-04 — VISIBILITY-AND-REGION-OWNERSHIP
- Current disposition: `NOT_ADOPTED_KEEP_BLOCKED`
- Question: Adopt exact field ownership, visibility, region and precedence/lifecycle rules.
- Historical limitation: four fields are accepted for future coordinate-policy specification only.
- Operator disposition: `PENDING` — do not infer.

### R-05 — ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING
- Current disposition: `NOT_ADOPTED_KEEP_BLOCKED`
- Question: Adopt complete geometry, anchor, clipping, crop and rounding policy.
- Historical limitation: some geometry choices are future-specification-only; final crop and pixel rounding are unresolved.
- Operator disposition: `PENDING` — do not infer.

### R-06 — INVALID-DATA-AND-TRACK-INTEGRITY
- Current disposition: `NOT_ADOPTED_KEEP_BLOCKED`
- Question: Adopt exact invalid-data, missing-track, frame-continuity and fail-closed/recovery behavior.
- Historical limitation: contracts/tests are not an independent product-policy authority record.
- Operator disposition: `PENDING` — do not infer.

### R-07 — SEMANTIC-VISUAL-OWNERSHIP
- Current disposition: `NOT_ADOPTED_KEEP_BLOCKED`
- Question: Adopt producer/consumer ownership, conflict resolution and semantic-to-visual publication rules.
- Historical limitation: semantic definitions permit future binding specification only.
- Operator disposition: `PENDING` — do not infer.

### R-08 — CHALLENGE-008
- Current disposition: `BLOCKED_EXPLICIT_AUTHORITY_REQUIRED`
- Question: Resolve the declared 11s versus phase-sum 12s conflict and define `active_selection` semantics.
- Operator disposition: `PENDING` — no timing correction or representation may be inferred.

### R-09 — CHALLENGE-009
- Current disposition: `BLOCKED_EXPLICIT_AUTHORITY_REQUIRED`
- Question: Resolve the declared 11s versus phase-sum 12s conflict and define `displayed_count` representation.
- Operator disposition: `PENDING` — no timing correction or representation may be inferred.

## Approval record template (copy per decision)

```yaml
decision_id: REQUIRED
operator_disposition: ADOPT | DEFER_KEEP_BLOCKED | REJECT | REVISE
exact_policy_text_and_selected_option: REQUIRED_FOR_ADOPT
named_approving_authority_and_role: REQUIRED_FOR_ADOPT
authority_scope_and_delegation_basis: REQUIRED_FOR_ADOPT
decision_date: REQUIRED_FOR_ADOPT
effective_date: REQUIRED_FOR_ADOPT
rationale: REQUIRED_FOR_ADOPT
source_paths_and_sha256_pins: REQUIRED_FOR_ADOPT
acceptance_test_obligations: REQUIRED_FOR_ADOPT
verifiable_approval_provenance_or_signature: REQUIRED_FOR_ADOPT
immutable_decision_record_location: REQUIRED_FOR_ADOPT
```

## Global acknowledgements

- Renderer activation: **not requested/granted by this packet**.
- Production payload/media creation: **not requested/granted**.
- Candidate input and seed admissibility: **not granted**.
- Binding or renderer-projection approvals: **not granted**.
- Baseline freeze/promotion and release authority: **not granted**.

Current locks remain `renderer=OFF`, `approved_bindings=0`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION`, `baseline_approval=MISSING`, `release_authority=NONE`.
