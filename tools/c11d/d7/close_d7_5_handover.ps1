#requires -Version 5.1
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$artifactDir = Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_5'
$receiptPath = Join-Path $artifactDir 'd7_5_acceptance_receipt.json'
$handoverPath = Join-Path $repoRoot 'docs\current\d\D7.5_HANDOVER.md'
$masterPath = Join-Path $repoRoot 'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md'
$startPath = Join-Path $repoRoot 'docs\current\d\START_PROMPT_C11D_CURRENT.md'

if(-not (Test-Path -LiteralPath $receiptPath)) { throw 'D7.5 receipt not found.' }
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D7.5 receipt is not PASS/CLOSED.' }

$enc = New-Object System.Text.UTF8Encoding($false)

$handover = @'
# C11-D D7.5 — Full D7 Acceptance

## Status

PASS / CLOSED.

## Acceptance

D7.0, D7.1, D7.2, D7.3 and D7.4 are all PASS/CLOSED. The canonical matrix, catalog and identity/provenance authorities remain coherent across 90 core cases.

Governance remains locked to explicit domain seeds; `master_seed` is `NOT_ADOPTED`; runtime seed derivation and automatic generation remain disabled; cross-domain seed sharing remains `FORBIDDEN`.

D4.8 remains `BLOCKED`. Runtime authority is `NONE`. Production and renderer execution remain disabled. D7.5 does not create or modify `release/` and writes evidence only under `artifacts/tests/c11d_d7/d7_5/`.

## Evidence

- `artifacts/tests/c11d_d7/d7_5/d7_5_full_acceptance.json`
- `artifacts/tests/c11d_d7/d7_5/d7_5_governance_validation.json`
- `artifacts/tests/c11d_d7/d7_5/d7_5_negative_tests.json`
- `artifacts/tests/c11d_d7/d7_5/d7_5_acceptance_receipt.json`

## Next

D8 — Media QA + Release Pipeline.
'@
if(Test-Path -LiteralPath $handoverPath) { [System.IO.File]::WriteAllText($handoverPath,$handover,$enc) }

function Update-Current([string]$path,[string]$marker,[string]$text) {
    if(-not (Test-Path -LiteralPath $path)) { return }
    $raw = [System.IO.File]::ReadAllText($path)
    $lines = $raw -split "`r?`n"
    $filtered = foreach($line in $lines) {
        if($line -match 'D7\.5\s*=\s*ACTIVE|NEXT\s*=\s*D7\.5|NEXT:\s*D7\.5|D7\.4\s*PASS\s*/\s*CLOSED') { continue }
        if($line -match 'D7\.5\s+PASS\s*/\s*CLOSED') { continue }
        $line
    }
    $block = @('', $marker, '', '## C11-D D7.5 CLOSED', '', '- D7.0-D7.4 PASS/CLOSED.', '- D7 full acceptance PASS/CLOSED.', '- Canonical authorities: matrix CANONICAL_D7_1; catalog CANONICAL_D7_3; identity/provenance CANONICAL_D7_4.', '- Coverage: 9 challenges × 5 delivery profiles × 2 modes = 90 core cases.', '- D4.8 remains BLOCKED; runtime NONE; production and renderer execution disabled.', '- Next active checkpoint: **D8 - Media QA + Release Pipeline**.', '')
    $new = (($filtered -join [Environment]::NewLine).TrimEnd() + [Environment]::NewLine + [Environment]::NewLine + ($block -join [Environment]::NewLine) + [Environment]::NewLine)
    [System.IO.File]::WriteAllText($path,$new,$enc)
}

Update-Current $masterPath '<!-- C11D_D7_5_HANDOFF -->' ''
Update-Current $startPath '<!-- C11D_D7_5_HANDOFF -->' ''
Write-Host 'D7.5 handover closure applied.'
Write-Host 'D7 = PASS / CLOSED'
Write-Host 'NEXT = D8 - Media QA + Release Pipeline'
