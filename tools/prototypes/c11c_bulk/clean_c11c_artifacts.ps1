param(
    [switch]$Apply
)
$ErrorActionPreference='Stop'
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$protected=@('legacy','qa','regression','releases','production','tests')
$mediaExtensions=@('.mp4','.gif','.avi','.wav','.png','.jpg','.jpeg','.webp','.bmp','.mov','.mkv','.webm')
$roots=@()
foreach ($name in @('c11c_geometric_waves_v1','c11c_fractal_bloom_v1','c11c_sacred_symmetry_v1','c11c_living_particles_v1','c11c_invisible_forces_v1','c11c_bulk_multiseed')) {
    $p=Join-Path $ProjectRoot ("artifacts\prototypes\$name")
    if (Test-Path -LiteralPath $p) { $roots += $p }
}
Write-Host '[C11C-CLEAN] Manual C11-C prototype media cleanup only.'
Write-Host "[C11C-CLEAN] Mode: $(if($Apply){'APPLY'}else{'DRY-RUN'})"
$count=0;$bytes=[int64]0
foreach ($root in $roots) {
    Get-ChildItem -LiteralPath $root -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
        if ($mediaExtensions -contains $_.Extension.ToLowerInvariant()) {
            $count++;$bytes+=$_.Length
            if ($Apply) { Remove-Item -LiteralPath $_.FullName -Force; Write-Host "[C11C-CLEAN] REMOVED $($_.FullName)" }
            else { Write-Host "[C11C-CLEAN] WOULD REMOVE $($_.FullName)" }
        }
    }
}
Write-Host "[C11C-CLEAN] Media files: $count"
Write-Host ("[C11C-CLEAN] Reclaimable: {0:N2} MB" -f ($bytes/1MB))
Write-Host '[C11C-CLEAN] Protected roots: legacy / qa / regression / releases / production / tests'
Write-Host '[C11C-CLEAN] Review assets and metadata are retained.'
return
