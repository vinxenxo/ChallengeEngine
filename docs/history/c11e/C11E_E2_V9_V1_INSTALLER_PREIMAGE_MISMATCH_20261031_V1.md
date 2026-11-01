# C11-E E2 V9 V1 installer preimage mismatch — incident record

**Observed:** 2026-10-31, operator installation attempt.  
**Installer:** `APPLY_C11E_E2_V9_TEST_HARNESS_OVERLAY_20261031_V1.ps1`.  
**Target:** `tools/c11e/e2/C11EChallenge001E2.gd`.

The installer expected V8 preimage SHA-256 `af142fc5fc41f4e398e981e60c014d9ddd09dccc888c1d3fbc2e1b0e77911493`. Windows PowerShell reported actual SHA-256 `4787b4459eb509117c6d752d1b6744236bb5a291372f2ef5a5cb1eb58755dae5`.

The actual hash exactly matches the GDScript payload postimage in the V9 V1 overlay. Thus the path was already at the exact desired V9 content before the installer ran. The transcript does not establish how that postimage reached the active checkout; do not infer provenance from its hash alone.

Root cause: V9 V1 applied a hard-coded V8 equality precheck over all replacement paths, and failed before the manifest's per-file preimage decision could run. The installer did not support a valid `already at exact postimage` state. It therefore rejected a safe, deterministic state and was not idempotent.

Impact: the V9 V1 installer stopped during preflight. Its code order places receipt-directory creation and all writes after this check. This invocation did not write overlay payloads and did not invoke Godot or create media. Existing checkout state was not modified by this installer attempt.

Correction: V9 V2 removes the blanket V8 pin equality loop and checks the V8 receipt against the V8 expected postimages. For every V9 replacement, current content must equal either the exact declared V8 preimage (then replace) or exact V9 postimage (then record `ALREADY_PRESENT`). For add-only paths, absence means add and exact V9 postimage means `ALREADY_PRESENT`. Any third hash, conflicting add-only content, missing receipt, manifest mismatch or C11-C pin mismatch stops before writes. The entire set is preflighted before the first mutation, and each preimage is rechecked immediately before mutation.

No E2 PASS, no human review, no E3 authorization and no release/promotion authority result from this incident.
