#requires -Version 5.1
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
$repoRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$receiptPath=Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_3\d7_3_catalog_receipt.json'
if(-not(Test-Path -LiteralPath $receiptPath -PathType Leaf)){throw 'D7.3 receipt missing.'}
$receipt=Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED'){throw 'D7.3 receipt is not PASS/CLOSED.'}
$paths=@(
 (Join-Path $repoRoot 'docs\current\d\D7.3_HANDOVER.md'),
 (Join-Path $repoRoot 'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md'),
 (Join-Path $repoRoot 'docs\current\d\START_PROMPT_C11D_CURRENT.md')
)
foreach($path in $paths){
 if(Test-Path -LiteralPath $path -PathType Leaf){
   $raw=[System.IO.File]::ReadAllText($path)
   $raw=$raw -replace 'D7\.3 = ACTIVE / IMPLEMENTATION READY','D7.3 = PASS / CLOSED'
   $raw=$raw -replace 'D7\.3 = ACTIVE','D7.3 = PASS / CLOSED'
   $raw=$raw -replace 'NEXT = D7\.3','NEXT = D7.4 - Catalog Identity / Provenance'
   $raw=$raw -replace 'NEXT: D7\.3','NEXT: D7.4 - Catalog Identity / Provenance'
   $utf8=New-Object System.Text.UTF8Encoding($false)
   [System.IO.File]::WriteAllBytes($path,$utf8.GetBytes($raw))
 }
}
Write-Host 'D7.3 handover closure applied.'
Write-Host 'D7.3 = PASS / CLOSED'
Write-Host 'NEXT = D7.4 - Catalog Identity / Provenance'
