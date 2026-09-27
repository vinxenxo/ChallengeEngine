param(
    [switch]$Apply,
    [switch]$MoveLegacy,
    [switch]$ArchiveRedundantRootDocs,
    [switch]$CreateCompatibilityStubs
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Docs=Join-Path $ProjectRoot 'docs'
$Current=Join-Path $Docs 'current'
$History=Join-Path $Docs 'history'
$Archive=Join-Path $History 'reorganization_2.16.9'
$dirs=@($Current,(Join-Path $Current 'c11c'),(Join-Path $Current 'challenges'),(Join-Path $Current 'producer'),$History,$Archive)
Write-Host '[DOCS-REORG] Plan for C11-C 2.16.9 documentation consolidation.'
Write-Host '[DOCS-REORG] Default mode is dry-run. Use -Apply to mutate files.'
foreach($d in $dirs){ Write-Host "[DOCS-REORG] ensure $d"; if($Apply){New-Item -ItemType Directory -Force -Path $d | Out-Null} }
if($MoveLegacy){
    $legacyFiles=@(Get-ChildItem -LiteralPath (Join-Path $Docs 'c11') -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '(?i)(CHANGELOG|MASTER_HANDOVER|START_PROMPT|PATCH|OVERLAY|INSTALL|README|2\.\d)' })
    foreach($f in $legacyFiles){ $target=Join-Path $Archive $f.Name; Write-Host "[DOCS-REORG] archive $($f.FullName) -> $target"; if($Apply){Move-Item -LiteralPath $f.FullName -Destination $target -Force} }
}
if($ArchiveRedundantRootDocs){
    foreach($name in '00_PROJECT_OVERVIEW.md','01_ARCHITECTURE.md','02_DATA_AND_CONTRACTS.md','03_PRESENTATION.md','04_REPOSITORY_STRUCTURE.md','05_TESTING_AND_REGRESSION.md','06_PRODUCTION_AND_DISTRIBUTION.md','07_ROADMAP.md'){
        $src=Join-Path $Docs $name
        if(Test-Path -LiteralPath $src){ $target=Join-Path $Archive $name; Write-Host "[DOCS-REORG] archive root doc $src -> $target"; if($Apply){Move-Item -LiteralPath $src -Destination $target -Force} }
    }
}
if($CreateCompatibilityStubs){
    foreach($name in '00_PROJECT_OVERVIEW.md','01_ARCHITECTURE.md','02_DATA_AND_CONTRACTS.md','03_PRESENTATION.md','04_REPOSITORY_STRUCTURE.md','05_TESTING_AND_REGRESSION.md','06_PRODUCTION_AND_DISTRIBUTION.md','07_ROADMAP.md'){
        $target=Join-Path $Docs $name
        $content="# Compatibility entry point — $name`r`n`r`nAuthoritative current version:`r`n`r`ndocs/current/$name`r`n"
        Write-Host "[DOCS-REORG] compatibility stub $target"
        if($Apply){[IO.File]::WriteAllText($target,$content,(New-Object Text.UTF8Encoding($false)))}
    }
}
if($Apply){ Write-Host '[DOCS-REORG] APPLY complete. Run python .\tests\run_all.py.' } else { Write-Host '[DOCS-REORG] DRY-RUN complete. No files changed.' }
