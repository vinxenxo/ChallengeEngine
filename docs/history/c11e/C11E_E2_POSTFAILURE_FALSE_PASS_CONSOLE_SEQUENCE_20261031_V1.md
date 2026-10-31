# C11-E — invalid post-failure console PASS sequence (V1)

During the 2026-10-31 E2 V7 attempt, the PowerShell runner returned nonzero (inner Godot process exit 40; runner exit 1). The success receipt and SHA sidecar were absent, as expected for a failed run. The assistant had supplied a follow-on success-validation tail without sufficient short-circuit protection; when the tail was continued in the same interactive console, it issued missing-file and undefined-variable errors, then printed an unconditional green `E2 V7 AUTOMATED ACCEPTANCE CHECKS: PASS`.

That final text is not a receipt, not a test result and not evidence. No E2 pass exists. Any subsequent workflow must keep success-only validation inside an `else` branch or stop after the nonzero child process code. The E2 runner itself already emits and verifies failure evidence; do not manually continue the success flow after a failure.
