# C11-D Phase X — Governance Subset Validation Hotfix V2

Date: 2026-10-29.

## Defect
The V1 bundle-preparation utility compared every canonical governance lock against both Phase V and W JSON reports as if all reports serialized every field. The actual Phase W report contract records `renderer`, approved-binding counters and `release_authority`, but omits optional locks such as `media_created` and `payload_materialized`. This caused a false `GOVERNANCE_LOCK_MISMATCH=media_created` although the omitted key was not an observed contrary value.

## Correction
V2 compares every governance field that an upstream report actually serializes and rejects any present conflicting value without type coercion. It additionally requires `renderer=OFF`, all three approved-binding counters zero, and `release_authority=NONE` in Phase V and W inputs. It records which optional lock fields each upstream report omits and emits the canonical full lock set in the Phase X output. Omission is not evidence for an alternative value and is never treated as authorization.

Regression suite: 56 tests; includes omitted optional lock accepted, present `true` rejected, string `false` not coerced to Boolean, missing required core lock rejected, and nonzero approved binding rejected. Source candidates, Phase U/V/W records and governance locks are unchanged.

Phase X remains read-only source packaging: no source writes, no renderer invocation, no payload/media creation, no authority adjudication, no policy adoption. CHALLENGE_008/009 stays blocked at 11 seconds declared vs 12 seconds phase sum.
