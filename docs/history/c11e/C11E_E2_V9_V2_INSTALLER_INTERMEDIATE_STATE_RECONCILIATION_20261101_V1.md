# C11-E E2 â€” V9 V2 installer intermediate-state reconciliation (2026-11-01)

## Incident

The first V9 V2 installer attempt stopped during global preflight with no repository writes. It found `docs/current/e/README.md` at SHA-256 `c8ab9772268291873567fc4a4762f71b061c216010b1a9919b4a723d7105a7ea`, which is the exact V9 V1 README postimage, while V9 V2 only allowed the V8 preimage and V9 V2 postimage. The same V9 V1 intermediate state existed for `AGENTS.md` and `.continue/rules/CONTINUE.md`.

## Reconciliation

The reconciled installer accepts only three explicit states per replacement: the V8 receipt postimage, the exact V9 V1 intermediate postimage (only for the three documented text files), or the V9 V2 target postimage. Any other hash aborts before repository writes. Add-only paths must be absent or equal to their exact V9 V2 payload. The package archive SHA and every manifest payload hash are verified; a package sidecar filename difference is not treated as a content-integrity failure when the actual archive SHA matches.

## Execution boundary

This installer only applies the V9 test-harness and documentation payloads. It does not invoke Godot, Python tests, FFmpeg, a renderer, or create media. Installation success is not an E2 pass. E2 remains blocked until the native Godot numeric preflight and the two physical CHALLENGE_001 A/B renders pass their full automated and human review gates. E3 audio remains blocked.

## Operational correction

The earlier manual post-install sequence was not fail-fast when pasted incrementally into an interactive PowerShell session. It continued after installer errors, reused a prior V8 receipt variable, and printed an unsupported APPLIED message. Those lines are not evidence and must not be repeated. This reconciled launcher performs installation and receipt/postimage verification in one child process and exits nonzero on any failure.