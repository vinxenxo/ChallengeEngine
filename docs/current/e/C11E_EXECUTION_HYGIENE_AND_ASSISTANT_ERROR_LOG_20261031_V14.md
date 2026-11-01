# C11-E execution hygiene and assistant error log — V14

## Mandatory execution discipline

- The active Windows checkout is authoritative. Never infer local file state from snapshots or generated package payloads.
- Every installer must verify branch/lineage, frozen C11-C manifest, relevant receipts/evidence, payload hashes, and every destination before its first repository write.
- Every replacement accepts only an explicitly declared preimage. A postimage can be treated as already applied only when the installer is intentionally idempotent and the current hash exactly equals the intended postimage. Any other hash aborts. Add-only paths may be missing or exactly match the desired payload; a conflicting existing file aborts.
- Preflight the complete operation set before writing. Recheck each destination immediately before mutation. Use same-volume atomic replacement and preserve preimage backups. Record per-file outcome `APPLIED` or `ALREADY_PRESENT`.
- Capture native exit codes immediately. A nonzero process exit, missing structured result, malformed receipt or incomplete output halts the sequence. Never execute success checks after a failure; never print manual PASS after failed checks.
- PowerShell 5.1 safe: no `&&`, no `Read-Host`, no reliance on stale `$LASTEXITCODE`/`$?` or stale variables. Prefer child process isolation with captured stdout/stderr and exit code.
- Installer and test harness must not modify Git refs/commits or invoke the renderer unless the runtime gate expressly calls for it.

## Incident: E2 V9 V1 installer rejected an exact postimage

The first V9 installer hard-coded V8 postimage equality before the V9 manifest preflight. Operator's active `C11EChallenge001E2.gd` hash `4787b4459eb509117c6d752d1b6744236bb5a291372f2ef5a5cb1eb58755dae5` equaled the V9 payload postimage, but the installer expected V8 hash `af142fc5fc41f4e398e981e60c014d9ddd09dccc888c1d3fbc2e1b0e77911493`. It failed before writes. V9 V2 adds explicit idempotent three-state handling and complete preflight.

## Incident: V8 native preflight did not produce markers

The user's V8 test invocation ended without both expected markers; stdout/stderr were not included in that report. No PASS can be inferred. V9 architecture removes the test's dependency on loading the full gameplay scene: production and test share a lightweight sidecar validator, the test writes structured JSON, and runner gates require schema/status/types/full sidecar/30-of-30 results.

## Incident: E2 V7 physical run and false PASS console sequence

V7 `godot_render_A` failed with exit 40 while validating sidecar seed values; the failure ZIP remains evidence. The operator's console then continued through success checks after a `throw` and emitted a manually printed PASS despite missing receipt/evidence variables. Those lines are invalid and must never be cited as successful E2 evidence. E2 remains not accepted.

## Current status

V7 render failed; V8 preflight unaccepted; V9 V1 installer rejected preflight due non-idempotent preimage pin; V9 V2 is the corrected install package. No E2 accepted, no E3 audio/mux, no promotion authority. The full Challenge/Loop/Drill goal is unchanged.
