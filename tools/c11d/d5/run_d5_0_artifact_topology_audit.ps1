[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$receiptPath = Join-Path $repoRoot 'artifacts\tests\c11d_d4\d4_9\d4_9_validation_receipt.json'
if (-not (Test-Path -LiteralPath $receiptPath -PathType Leaf)) { throw 'D4.9 validation receipt is missing.' }
$d4 = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($d4.result -ne 'PASS' -or $d4.status -ne 'CLOSED') { throw 'D4.9 must be PASS/CLOSED before D5.0.' }
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { throw 'Python is required to run the read-only D5.0 audit.' }
$auditScript = Join-Path $PSScriptRoot 'artifact_topology_audit.py'
& $python.Source $auditScript --root $repoRoot
$auditExit = $LASTEXITCODE
if ($auditExit -ne 0) { throw "D5.0 audit gate did not close (exit $auditExit). Inspect artifacts\tests\c11d_d5\d5_0." }

# The runner only updates the two D handover files after the generated receipt proves closure.
$d5Receipt = Get-Content -LiteralPath (Join-Path $repoRoot 'artifacts\tests\c11d_d5\d5_0\d5_0_validation_receipt.json') -Raw | ConvertFrom-Json
if ($d5Receipt.result -ne 'PASS' -or $d5Receipt.status -ne 'CLOSED') { throw 'Generated D5.0 receipt is not PASS/CLOSED.' }
foreach ($relative in @('docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md', 'docs\current\d\START_PROMPT_C11D_CURRENT.md')) {
    $path = Join-Path $repoRoot $relative
    $content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $content = [regex]::Replace($content, '(?m)^NEXT(?:\s*[:=]).*$', 'NEXT = D5.1 - Canonical Artifact Manifest', 1)
    if ($content -notmatch '(?m)^D5\.0(?:\s*[:=]).*PASS\s*/\s*CLOSED') {
        $content = [regex]::Replace($content, '(?m)^(D4(?:\.9)?\s*[:=].*PASS\s*/\s*CLOSED\s*)$', "`$1`r`nD5.0 = PASS / CLOSED", 1)
    }
    $content = [regex]::Replace($content, '(?m)^D5(?:\s*[:=]).*$', 'D5 = ACTIVE', 1)
    [System.IO.File]::WriteAllText($path, $content, [System.Text.UTF8Encoding]::new($false))
}
Write-Output 'D5.0 artifact topology audit PASS/CLOSED. No artifacts were moved or deleted.'
