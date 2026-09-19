[CmdletBinding()]
param(
    [string]$Output = "artifacts/tests/reports/repository_inventory.json"
)

$ErrorActionPreference = "Stop"
$roots = @(
    "output", "output_c7", "output_batch_audit", "export", "qa",
    "catch_v1", "hit_v1", "parking_v2", "c9_c_generated_configs", "c9_g_generated_configs"
)

$result = [ordered]@{
    generated_at = (Get-Date).ToString("o")
    repo = (Get-Location).Path
    legacy_roots = @()
    active_artifact_root_exists = Test-Path "artifacts"
}

foreach ($root in $roots) {
    $full = Join-Path (Get-Location) $root
    if (Test-Path $full) {
        $files = @(Get-ChildItem -LiteralPath $full -Recurse -File -ErrorAction SilentlyContinue)
        $bytes = ($files | Measure-Object Length -Sum).Sum
        $result.legacy_roots += [ordered]@{
            path = $root
            files = $files.Count
            bytes = [int64]$bytes
        }
    }
}

$out = Join-Path (Get-Location) $Output
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $out) | Out-Null
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $out -Encoding UTF8
Write-Host "[C11FREEZE] Inventory written: $out"
