# C11-B.0.2 v4 — Deferred Audit / QA Framing Metadata

## What changed

v3 exposed a lifecycle defect in the audit path: the C11-B audit was executed before
FamilyAssets, target base position and final presentation asset state had been initialized.
That caused secondary targets to be audited at `(0,0)` and produced false geometry failures.

v4 defers `initialize_presentation_framing()` and `run_c11b_visibility_audit()` until after:

1. `FamilyAssets.configure_presentation()`;
2. target initial position / `static_target_base_position` resolution;
3. asset validation / presentation calibration.

The canonical challenge fixture is not modified.

## QA-only framing metadata

Because the C10 challenge fixtures remain frozen, `CHALLENGE_001` receives the
`PRIMARY_FOCUS` presentation policy only in the six C11-A.1 QA copies.

Run:

```powershell
.\tools\apply_c11b02_qa_framing_policy.ps1
```

This modifies only:

`qa/c11a1_challenge_qa/runs/*/challenge_definition.json`

for `CHALLENGE_001` and adds:

```json
"presentation": {
  "framing_policy": "PRIMARY_FOCUS"
}
```

It does not modify `challenges/CHALLENGE_001.json`.

## Verification

```powershell
.\tools\verify_c11b02_installation.ps1
.\tools\apply_c11b02_qa_framing_policy.ps1
godot --headless --path . -s .\tests\C11B02PresentationFramingContractTest.gd
.\tools\run_c11b_body_visibility_audit.ps1
```

No video rerender is required.
