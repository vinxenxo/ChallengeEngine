# C11-D Phase AB — Authority Evidence Adjudication Criteria

## Decision standard

A source is not an authority record merely because it is named an acceptance, PASS receipt, handover, engineering standing approval or historical test. The reviewer must evaluate the issuer, delegated authority, scope, exact adopted text, effective date, provenance and record integrity separately.

## Required review per R-row

1. Identity/role: independently confirm the named issuer and role from a trusted source.
2. Delegation: show that authority covers the exact decision and scope.
3. Policy content: preserve exact wording and option; do not normalize ambiguous text into a decision.
4. Temporal validity: decision date, effective date, supersession and revocation state.
5. Integrity: immutable original bytes, exact SHA-256, provenance/signature reference and record location.
6. Scope: do not expand historical specification-only permissions into runtime, renderer or release authorization.
7. Verification obligations: enumerate acceptance tests and how the decision is independently checked.
8. Adjudication: accept only with sufficient provenance and scope; otherwise reject the authority claim or retain `KEEP_BLOCKED_NO_POLICY_ADOPTION`.

## R-08/R-09

CHALLENGE_008/009 duration remains 11 s declared versus 12 s phase sum. The adjudication must reference the exact conflict, record the authoritative selected resolution, pin its source and specify a regression acceptance test. No code edit or duration change is implied by the docket.

## Dependent gates after valid authority

Input admissibility, seed domains/master seed, semantic and custom-data bindings, renderer projection, D9.17 and isolated-render acceptance are separate gates. Passing authority review for one R-row does not pass these gates implicitly. The first isolated render needs a separate explicit execution decision after all required preconditions pass. D10 and C11-D promotion remain separate later decisions.

## No evidence / invalid evidence

Missing, unsigned where signature is required, unverifiable, stale, conflicting or out-of-scope authority evidence results in `KEEP_BLOCKED_NO_POLICY_ADOPTION`. No fallback to majority vote, inference from tests, engineering intent or standing approval is allowed.
