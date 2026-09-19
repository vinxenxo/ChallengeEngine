[CmdletBinding()]
param(
    [ValidateSet("DryRun","Copy","Move")]
    [string]$Mode = "DryRun"
)

$ErrorActionPreference = "Stop"

# Only known legacy roots are migrated here. Current C11 QA is NOT treated as legacy.
$map = [ordered]@{
    "output_c7" = "artifacts/legacy/output_c7"
    "output_batch_audit" = "artifacts/legacy/output_batch_audit"
    "export" = "artifacts/legacy/export"
    "catch_v1" = "artifacts/legacy/catch_v1"
    "hit_v1" = "artifacts/legacy/hit_v1"
    "parking_v2" = "artifacts/legacy/parking_v2"
    "c9_c_generated_configs" = "artifacts/legacy/c9_c_generated_configs"
    "c9_g_generated_configs" = "artifacts/legacy/c9_g_generated_configs"
    "output" = "artifacts/legacy/output"
}

# QA relocation is intentionally explicit and outside the legacy map.
$qaMap = [ordered]@{
    "qa/c11a1_challenge_qa" = "artifacts/qa/c11a1_challenge_qa"
    "qa/c11a_visual_qa" = "artifacts/qa/c11a_visual_qa"
    "qa/c11b_visibility_qa" = "artifacts/qa/c11b_visibility_qa"
}

function Move-Tree([string]$src, [string]$dst) {
    if (-not (Test-Path -LiteralPath $src)) { return }
    Write-Host "[$Mode] $src -> $dst"
    if ($Mode -eq "DryRun") { return }
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    if ($Mode -eq "Copy") { Copy-Item -LiteralPath (Join-Path $src '*') -Destination $dst -Recurse -Force }
    else { Move-Item -LiteralPath (Join-Path $src '*') -Destination $dst -Force }
}

foreach ($src in $map.Keys) { Move-Tree $src $map[$src] }
foreach ($src in $qaMap.Keys) { Move-Tree $src $qaMap[$src] }

Write-Host "[C11FREEZE] Migration mode completed: $Mode"
Write-Host "[C11FREEZE] Current QA evidence is preserved; output/export roots are legacy until Move is explicitly approved."
