#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$receiptPath = Join-Path $repoRoot 'artifacts\tests\c11d_d6\d6_5\d6_5_acceptance_receipt.json'
if (-not (Test-Path -LiteralPath $receiptPath -PathType Leaf)) { throw 'D6.5 acceptance receipt is missing.' }
$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if ($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED') { throw 'D6.5 receipt is not PASS/CLOSED.' }

$files = @(
    @{ Path='docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'; Marker='D6.5 = PASS / CLOSED'; Next='D7 - Production Matrix + Catalog' },
    @{ Path='docs/current/d/START_PROMPT_C11D_CURRENT.md'; Marker='D6.5 = PASS / CLOSED'; Next='D7 - Production Matrix + Catalog' },
    @{ Path='docs/master-prompts/MASTER_HANDOVER_C11D_V1.0_STATELESS.md'; Marker='D6.5 = PASS / CLOSED'; Next='D7 - Production Matrix + Catalog' }
)

foreach ($item in $files) {
    $path = Join-Path $repoRoot $item.Path.Replace('/', '\')
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { continue }
    $text = Get-Content -LiteralPath $path -Raw
    $text = [regex]::Replace($text, 'D6\.0\s*=.*?(?=\r?\n)', 'D6.0 = PASS / CLOSED')
    $text = [regex]::Replace($text, 'D6\.1\s*=.*?(?=\r?\n)', 'D6.1 = PASS / CLOSED')
    $text = [regex]::Replace($text, 'D6\.2\s*=.*?(?=\r?\n)', 'D6.2 = PASS / CLOSED')
    $text = [regex]::Replace($text, 'D6\.3\s*=.*?(?=\r?\n)', 'D6.3 = PASS / CLOSED')
    $text = [regex]::Replace($text, 'D6\.4\s*=.*?(?=\r?\n)', 'D6.4 = PASS / CLOSED')
    if ($text -match 'D6\.5\s*=') {
        $text = [regex]::Replace($text, 'D6\.5\s*=.*?(?=\r?\n)', 'D6.5 = PASS / CLOSED')
    } else {
        $text += "`r`nD6.5 = PASS / CLOSED`r`n"
    }
    $text = [regex]::Replace($text, 'NEXT\s*=.*?(?=\r?\n)', 'NEXT = D7 - Production Matrix + Catalog')
    $bytes = [System.Text.UTF8Encoding]::new($false).GetBytes($text)
    [System.IO.File]::WriteAllBytes($path, $bytes)
}

Write-Host 'D6.5 handover closure applied.'
Write-Host 'D6.5 = PASS / CLOSED'
Write-Host 'NEXT = D7 - Production Matrix + Catalog'
