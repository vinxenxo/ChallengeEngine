[CmdletBinding()]
param()
$target=Join-Path $PSScriptRoot '..\c11c-suite\c11c-producer\run_visual_drill_production.ps1'
& $target @args
exit $LASTEXITCODE
