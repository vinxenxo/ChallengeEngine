# C11-E R1V / E4B Loop Qualification Runbook — V20

## Latest closed gate

R1V is closed `PASS_TEST_ONLY_OPERATOR_ACCEPTED`. Technical A/V is 10/10; human visual/layer/editorial/layout is 10/10 PASS; audio/music listening is 10/10 PASS. Human acceptance was operator-attested on 2026-11-09. See closeout receipt `artifacts/tests/c11e/r1v_operator_human_review_closeout/R1V_HUMAN_REVIEW_CLOSEOUT_RECEIPT_V1.json` (SHA-256 `a9e1de310ba1f52bab029a6fc6f926892264dd25cfa5edd8ec90aec460a2662a`). Do not reopen or repeat R1V absent a concrete regression.

## Next bounded operation: R1P projection and policy fingerprint refresh

Use `C11E_E4B_LOOP22_R1P_POLICY_REFRESH_V1`. The PowerShell runner first confirms the frozen manifest, R1V V7 install receipt, closeout receipt and exact source-audit report/sidecar, executes eight new focused tests, then runs one read-only Python projector. The projector:
- validates the exact R1P archive SHA and ZIP CRC;
- validates the canonical report hash and sidecar;
- validates all 27 canonical receipt hashes and individual sidecars;
- validates receipt-hash-set SHA and the 30-entry source manifest;
- validates request-bound hashes, plan-only materialization boundary, distinct gameplay/music seed domains, family music profile and 20/22/23s duration mapping;
- checks the exact 22-selector complement against active source audit rows;
- verifies every one of the 30 R1P source pins on the active checkout and reconciles the earlier 17/17 pin report;
- fingerprints the five live policy proposal JSON files.

Expected report status `PASS_R1P_RECEIPTS_PROJECTED_27_OF_27_POLICY_FINGERPRINTS_REFRESHED_5_OF_5`. Outputs are new evidence only under `artifacts/tests/c11e/e4b_loop22_r1p_policy_refresh/`.

## Current policy decisions required

Review generated `C11E_E4B_LOOP_POLICY_DECISION_DOCKET_V2.md`. For each of A.1, A.3, E4B_LOOP, B.1 and D.1, choose `APPROVE AS PROPOSED`, `REQUEST CHANGES` or `DEFER` and explicitly confirm the full SHA-256 captured from the active checkout. The continuation approval does not replace this hash-specific policy gate.

- A.1/A.3/E4B_LOOP: visual consumer gate.
- B.1/D.1: native family music/AAC/AV delivery gate.

No policy approval grants renderer-native input, D4 executable compatibility, dispatch or production authority.

## Never do in this step

No Git, no accepted-stage reruns, no C11-C launchers, no prototype execution, no music generation, no FFmpeg/FFprobe, no renderer, no dispatch and no media. Do not alter C11-C or its frozen manifest.
