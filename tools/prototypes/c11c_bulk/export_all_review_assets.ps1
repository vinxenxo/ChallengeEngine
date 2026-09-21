param(
    [string]$InputRoot = ".\artifacts\prototypes",
    [string]$OutputRoot = ".\artifacts\prototypes\c11c_review_assets"
)

$ErrorActionPreference = "Stop"

& "$PSScriptRoot\export_review_gifs.ps1" -InputRoot $InputRoot -OutputRoot $OutputRoot
if ($LASTEXITCODE -ne 0) { throw "Review GIF export failed" }

& "$PSScriptRoot\export_review_keyframes.ps1" -InputRoot $InputRoot -OutputRoot $OutputRoot
if ($LASTEXITCODE -ne 0) { throw "Review keyframe export failed" }

Write-Host "[C11-C-REVIEW] ALL REVIEW ASSETS COMPLETE"
