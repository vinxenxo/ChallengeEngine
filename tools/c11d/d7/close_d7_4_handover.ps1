#requires -Version 5.1
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$receiptPath = Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_4\d7_4_identity_receipt.json'
if (-not (Test-Path -LiteralPath $receiptPath -PathType Leaf)) { throw 'D7.4 receipt missing.' }
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D7.4 receipt must be PASS/CLOSED before handover closure.' }

function Write-Utf8NoBom {
    param([string]$Path, [string]$Text)
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Text, $enc)
}

$targets = @(
    (Join-Path $repoRoot 'docs\current\d\D7.4_HANDOVER.md'),
    (Join-Path $repoRoot 'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md'),
    (Join-Path $repoRoot 'docs\current\d\START_PROMPT_C11D_CURRENT.md')
)
foreach ($path in $targets) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Handover target missing: $path" }
    $text = [System.IO.File]::ReadAllText($path)
    $updated = $text
    $updated = [regex]::Replace($updated, 'D7\.3\s*-\s*PASS\s*/\s*CLOSED', 'D7.4 - PASS / CLOSED')
    $updated = [regex]::Replace($updated, 'NEXT\s*:\s*D7\.4[^\r\n]*', 'NEXT: D7.5 - Full D7 Acceptance')
    if ($updated -eq $text) {
        $updated = [regex]::Replace($updated, 'D7\.3\s+PASS/CLOSED', 'D7.4 PASS/CLOSED')
        $updated = [regex]::Replace($updated, 'NEXT\s+D7\.4[^\r\n]*', 'NEXT D7.5 - Full D7 Acceptance')
    }
    Write-Utf8NoBom -Path $path -Text $updated
}
Write-Host '[OK] D7.4 handover closed and current C11-D handover advanced to D7.5.'
