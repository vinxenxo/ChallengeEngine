$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$gm = Join-Path $root 'GeneradorMaestro.gd'
$cm = Join-Path $root 'core\presentation\CoordinateMapper.gd'
if (-not (Test-Path $gm)) { throw 'Missing GeneradorMaestro.gd' }
if (-not (Test-Path $cm)) { throw 'Missing CoordinateMapper.gd' }
$g = Get-Content -LiteralPath $gm -Raw -Encoding UTF8
$c = Get-Content -LiteralPath $cm -Raw -Encoding UTF8
$checks = [ordered]@{
  'Generador uses social_body_rect' = ($g -match 'social_body_rect')
  'Audit uses local Sprite2D transform' = ($g -match 'parent_rect\s*=\s*sprite\.transform\s*\*\s*local_rect')
  'Audit has expected position telemetry' = ($g -match 'object_expected_position')
  'Mapper accepts target_rect' = ($c -match 'target_rect:\s*Rect2')
  'Mapper defines social body' = ($c -match 'DEFAULT_SOCIAL_BODY_RECT')
}
$checks.GetEnumerator() | ForEach-Object { '[C11B0.1] {0}: {1}' -f $_.Key, $(if ($_.Value) {'PASS'} else {'FAIL'}) }
if (($checks.Values | Where-Object { -not $_ }).Count -gt 0) { exit 1 }
Write-Host '[C11B0.1] Installation verification PASS' -ForegroundColor Green
