# C11-D Final Closeout Start Prompt — V15 (2026-10-21)

Continue in the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. The live checkout is authoritative. Never extract a whole context archive over it. C11-C remains frozen and immutable at manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Latest verified state

The operator-approved semantic-decision record passed **146/146** on Windows (receipt `3cf2284c454a06571ea97a2e771a259d2b73a8f4616432063a581b5c3e57ecf9`). The field-region/visibility proposal passed **551/551** on Windows with 4/4 candidates, 81/81 source pins, 9/9 authority pins and 6/6 semantic decision pins (receipt `87c8ab97db18a7531dc2df610b51fe819c8bf746b2b66475b544220c37c95cbb`; stdout `dc6ecb960fc59852c4b3251a1146ef6425675c44be4cf03304d3fc0026942d27`; stderr empty `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

A separate immutable record now accepts the four candidate field-region proposals only for future coordinate-policy specification:

- `CHALLENGE_003.target_x` — scalar X-only in `PILOT_0X100`, no inferred Y or normalization.
- `CHALLENGE_005.target_position` — per-run constant Vector2 repeated across source frames.
- `CHALLENGE_006.target_position` — per-frame target Vector2 independent of catcher position.
- `CHALLENGE_007.target_position` — per-frame target Vector2 independent of scanner position.

`CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked. The four new decisions are **not** coordinate-transform, binding, consumer or rendering approvals.

## Next gate

Apply and test `C11D_V2B_CANDIDATE_FIELD_REGION_VISIBILITY_DECISION_RECORD_OVERLAY_20261021_V2.zip` by its verified SHA. Confirm the independent decision record suite passes at its embedded denominator, with 81/81 source pins, 9/9 authority-input pins and 6/6 semantic-input pins, and that the prior proposal receipt/hash remains consistent.

Then continue directly to a distinct coordinate-policy proposal; do not ask for redundant confirmation of the approved scope. The coordinate proposal must explicitly cover source-space semantics, source-to-logical 540x960 mapping, logical-to-delivery mapping, axis/origin/units, intrinsic asset sizing/anchor, out-of-bounds behavior, source frame cardinality, and fail-closed handling. Keep all unresolved rules `PROPOSED_NOT_APPROVED`. For `CHALLENGE_003`, either propose an explicit source-supported treatment of missing Y for review or leave actual point placement unavailable. Do not infer Y or normalize X silently.

## Mandatory locks

`renderer=OFF`; payload/media false; candidate input inadmissible; approved bindings/custom-data/projection bindings zero; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; baseline approval missing; freeze ineligible; release authority none. Do not modify C11-C, challenge JSONs, or `CHALLENGE_004` V1 fixture. Do not rerun the prior 45/45 Godot matrix for static-only increments.

The product goal remains a controlled real-render test on D, followed by formal D approval/freeze/promotion before C11-C can be replaced. Proceed gate by gate with evidence; do not represent this record as authorizing a renderer run.

V2 correction note: the failed 652/653 run exposed a malformed empty-stderr digest constant in the unaccepted V1 overlay. V2 fixes that digest consistently in the decision JSON, test script, and manifest. The receipt from the prior 551/551 Windows suite remains pinned; rerun the V2 regression gate and report its full receipt.
