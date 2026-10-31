# C11-E — execution hygiene and assistant error log (V12)

## E2 V7 failure: JSON numeric Variant mismatch

Evidence ZIP `C11E_E2_CH001_AB_FAILURE_EVIDENCE_20261031_191440_13012eef.zip`: 29,568 bytes, 47 entries, SHA-256 `27fa769c35165e8171120bc0fce16fc3739505198157a874360c2de432c6bbe7`. Pair tests 9/9 pass; Godot 4.7.1 Mono starts and runs the A scene, then emits `[C11E_E2] Editorial sidecar contract validation failed.` from `C11EChallenge001E2.gd:62`, exit 40. Only one frame is recorded in the partial AVI. Failure receipt: renderer invocation count 1, media-created path present, media accepted false, release authority NONE. No B render, final MP4, or success receipt exists.

Root cause: the sidecar is valid, but Godot's `JSON.parse_string()` maps JSON number tokens to `TYPE_FLOAT`; E2 validation required `TYPE_INT` for both `seed_domains.gameplay.value` and `seed_domains.music.value`. The V8 fix requires a numeric Variant, finite, >=1, <=2147483646 and equal to its floor. The new Godot-native preflight verifies float decoding and accepts only valid integer-valued seeds. Do not loosen the contract to arbitrary floats or numeric strings.

## PowerShell false-PASS sequence — rejected

After the runner returned nonzero exit code 1, the assistant-supplied follow-on validation tail did not short-circuit: its success-only commands were still entered in the same interactive PowerShell session. The success receipt and `.sha256` file did not exist; subsequent variable lookups failed. The tail then unconditionally printed `Write-Host 'E2 V7 AUTOMATED ACCEPTANCE CHECKS: PASS'`. This was an assistant-instruction defect, not evidence of user error or a real PASS. Future instructions must use a single guarded block with success checks only in the success branch, or run the runner directly and stop after any nonzero exit. No success receipt/ZIP path or hash may be inferred.

## Execution rules

- Capture `$LASTEXITCODE` immediately after every native process; a nonzero code terminates the current verification flow. Do not continue with success-only checks.
- Use one complete PowerShell 5.1 block/script. Avoid sending an interactive sequence where the operator can inadvertently execute later success commands after a `throw`.
- Do not trust `Write-Host PASS`; acceptance is based on verified receipt schema/status, hashes, files and substantive output.
- Godot Movie Maker output or process exit 0 never proves scene load or visible content. Parse/load diagnostics are fatal; source video frames must be spatially nonuniform.
- E2 V8 now runs a Godot-native JSON numeric test before Python pair preparation and before either renderer invocation. Its explicit marker must be present.
- Failure output is immutable and has `media_accepted=false`; the new attempt must use a new RequestId.
- Never reuse stale `$Record`, `$Receipt`, `$EvidenceZip`, `$ActualSha`, `$LASTEXITCODE`, or prior-version variables after failure.
- Do not repeat accepted E0/E1 work. Do not start E3/E4 while E2 is unaccepted.
- Operator local commits after each successful iteration are expected. Bind each installer to exact current HEAD/parent and let runtime runners verify ancestor lineage plus exact source hashes.
