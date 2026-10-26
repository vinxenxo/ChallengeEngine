# C11-D final closeout start prompt V24 — 2026-10-26

Continue in the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Use the current authority set: `AGENTS.md`, `.continue/rules/CONTINUE.md`, `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`, `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261026_V24.md`, `docs/current/d/C11D_SOURCE_SNAPSHOT_RECONCILIATION_REPORT_20261026_V1.md`, `docs/current/d/C11D_V2B_ALLOWLISTED_COORDINATE_SOURCE_COMPOSITION_RUNTIME_REVIEW_20261026_V1.md`, and the V24 master prompt.

The user's reference snapshot is `ChallengeEngineV01_STATELESS_C11-D_20261026_013616.zip`, SHA-256 `3e48ee2d815593137f5863139e05c1aa04eb40b4a58ddfb3bed4507125c96874`. Its embedded manifest mismatch is explicitly documented: observed ZIP-copy SHA `f6b2fc6ce36973eb620738c8446d529d98da0fb79892132cf4708e6f453051b5` / `1070256` bytes versus canonical `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` / `796318` bytes. Do not extract over the active checkout or copy this manifest. The live frozen C11-C manifest must remain `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` and must not change.

**First action:** verify the live checkout manifest SHA-256 is `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` and its size is `796318` bytes. The ZIP copy differs (`f6b2fc6ce36973eb620738c8446d529d98da0fb79892132cf4708e6f453051b5`, `1070256` bytes) and must never replace the frozen file. If the live check passes, validate the source-composition evidence V2 against the real temp logs, not by rerunning Godot unless the logs are missing or damaged:

```powershell
& {
    $ErrorActionPreference = "Stop"
    $Repo = "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"
    $EvidenceDir = Join-Path $env:TEMP "C11DCOORDCOMPOSITIONRUNTIME_79683278984b40d7b4fae0209ec4eee2"
    $Python = "C:\Users\vinxe\AppData\Local\Programs\Python\Python313\python.exe"
    if (-not (Test-Path -LiteralPath $EvidenceDir -PathType Container)) { throw "Runtime evidence directory missing; do not claim validation PASS." }
    $Test = Join-Path $Repo "tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_source_composition_runtime_evidence_v2.py"
    $ValidatorOut = Join-Path $EvidenceDir "receipt_validator_stdout.txt"
    $ValidatorErr = Join-Path $EvidenceDir "receipt_validator_stderr.txt"
    $Process = Start-Process -FilePath $Python -ArgumentList @($Test, $Repo, $EvidenceDir) -Wait -PassThru -NoNewWindow -RedirectStandardOutput $ValidatorOut -RedirectStandardError $ValidatorErr
    if (Test-Path -LiteralPath $ValidatorOut) { Get-Content -LiteralPath $ValidatorOut }
    if (Test-Path -LiteralPath $ValidatorErr) { Get-Content -LiteralPath $ValidatorErr }
    Write-Host ("EVIDENCE_VALIDATOR_EXIT_CODE=" + $Process.ExitCode)
    if ($Process.ExitCode -ne 0) { throw "Evidence validator failed. Stop and investigate." }
    if (-not (Select-String -LiteralPath $ValidatorOut -SimpleMatch "C11D_V2B_SOURCE_COMPOSITION_RUNTIME_EVIDENCE_VALIDATION_STATUS=PASS_RECEIPT_AND_CURRENT_SOURCE_PINS" -Quiet)) { throw "Required validation PASS marker missing; stop." }
}
```

For readable stdout and stderr, run the Python command directly in a separate block after any application setup if required, or capture both streams with `Start-Process` as dictated by the execution rules. Required status marker: `PASS_RECEIPT_AND_CURRENT_SOURCE_PINS`.

If PASS, review the V2 receipt and create a distinct operator review decision record; do not change the historical V1 evidence or the source-composition contract's pending pre-run status. No production callsite, renderer, payload materialization, media, render testing, baseline approval, release or cutover is authorized by this gate.
