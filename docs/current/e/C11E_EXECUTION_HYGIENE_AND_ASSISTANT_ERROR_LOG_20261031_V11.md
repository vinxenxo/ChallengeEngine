# C11-E — execution hygiene and assistant error log (V11)

## V6 blank-frame root cause

The V6 pair tests passed 9/9. Godot exit 0 did not mean script load success: stderr reported a GDScript inferred-Variant warning treated as error at line 54 and `Failed to load script`. Movie Maker produced a 540-frame, 540×960, 60 FPS, 9-second AVI whose decoded frames 0/270/539 each contained only RGB(77,77,77). Evidence SHA-256 `1a5d6341fae51152fb9684cc4fc158bf7c9849716a7028015f6d84b013a1cc21`.

## V7 correction

- Type the JSON.parse result explicitly as `Variant`.
- Treat Godot parse/load diagnostics as fatal even when process exit is 0.
- Check deterministic source frames 60/270/480 for actual spatial variation before conversion or A/B comparison.
- Record renderer invocation count, created AVI paths and `media_accepted=false` correctly in failure receipts.

## Checkout commit policy correction

The operator commits locally each iteration. The assistant incorrectly reused old `HEAD/parent` pins for V7 V1. Actual checkout `b92434d` was a valid direct child of `a3c7c5d`, clean and `ahead 2`; V7 V1 correctly stopped before writing. Future installers must pin the current HEAD/parent captured for that package. Runners spanning operator commits must validate ancestor lineage and exact source pins while recording the runtime HEAD/parent. Never label an operator's expected local commit as checkout drift.

## Rejected assistant behaviors

- Do not reuse stale `$Record`, `$Receipt`, `$ActualRunnerSha`, `$LASTEXITCODE` or previous-version evidence after a failed child process.
- Never append a manual green `Write-Host` after a thrown error and treat it as PASS.
- Never infer media creation from process exit, nor media acceptance from container metadata alone.
- Do not ask the operator to re-run E0/E1 or repeat evidence that is already pinned.
- Do not attempt E3/E4 while E2 remains unaccepted.
