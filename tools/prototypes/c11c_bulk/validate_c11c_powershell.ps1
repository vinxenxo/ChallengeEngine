param()
$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$roots=@(
    (Join-Path $ProjectRoot 'tools\prototypes\c11c_bulk'),
    (Join-Path $ProjectRoot 'tools\prototypes\c11c_fractal_bloom_v1'),
    (Join-Path $ProjectRoot 'tools\prototypes\c11c_geometric_waves_v1'),
    (Join-Path $ProjectRoot 'tools\prototypes\c11c_invisible_forces_v1'),
    (Join-Path $ProjectRoot 'tools\prototypes\c11c_living_particles_v1'),
    (Join-Path $ProjectRoot 'tools\prototypes\c11c_sacred_symmetry_v1')
)
$files=@()
foreach ($r in $roots) { if (Test-Path -LiteralPath $r) { $files += @(Get-ChildItem -LiteralPath $r -File -Filter '*.ps1' -Force) } }
$parser=[System.Management.Automation.Language.Parser]
$failed=$false
foreach ($file in ($files | Sort-Object FullName -Unique)) {
    $tokens=$null; $errors=$null; $null=$parser::ParseFile($file.FullName,[ref]$tokens,[ref]$errors)
    if ($errors.Count -gt 0) { $failed=$true; Write-Host "[C11C-PS-PARSE] FAIL $($file.FullName)"; foreach ($e in $errors) { Write-Host ("  line="+$e.Extent.StartLineNumber+" col="+$e.Extent.StartColumnNumber+" "+$e.Message) } }
    else { Write-Host "[C11C-PS-PARSE] PASS $($file.FullName)" }
}
if ($failed) { exit 1 }
Write-Host "[C11C-PS-PARSE] COMPLETE - $($files.Count) PowerShell files parsed successfully."
exit 0
