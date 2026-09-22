param([switch]$Apply)
$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$targets=@()
$proto=Join-Path $ProjectRoot 'artifacts\prototypes'
if (Test-Path -LiteralPath $proto) {
    $targets += @(Get-ChildItem -LiteralPath $proto -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like 'c11c_*' -or $_.Name -eq 'c11c_review_assets' })
}
$targets += @(Join-Path $ProjectRoot 'artifacts\scratch')
Write-Host '[C11C-RESET] This is the explicit destructive C11-C reset.'
Write-Host "[C11C-RESET] Mode: $(if($Apply){'APPLY'}else{'DRY-RUN'})"
foreach ($target in $targets) {
    if (Test-Path -LiteralPath $target) {
        if ($Apply) { Remove-Item -LiteralPath $target -Recurse -Force; Write-Host "[C11C-RESET] REMOVED $target" }
        else { Write-Host "[C11C-RESET] WOULD REMOVE $target" }
    }
}
if ($Apply) { New-Item -ItemType Directory -Force -Path (Join-Path $ProjectRoot 'artifacts\prototypes'),(Join-Path $ProjectRoot 'artifacts\scratch') | Out-Null }
Write-Host '[C11C-RESET] Protected evidence roots were not targeted.'
return
