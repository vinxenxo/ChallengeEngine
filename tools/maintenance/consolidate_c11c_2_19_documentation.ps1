[CmdletBinding()]
param([switch]$DryRun)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$HistoryRoot=Join-Path $ProjectRoot 'docs\history\c11c\releases\superseded_2.19'
New-Item -ItemType Directory -Path $HistoryRoot -Force | Out-Null

function Same-File([string]$A,[string]$B){
    if(-not(Test-Path -LiteralPath $A) -or -not(Test-Path -LiteralPath $B)){return $false}
    return (Get-FileHash -LiteralPath $A -Algorithm SHA256).Hash -eq (Get-FileHash -LiteralPath $B -Algorithm SHA256).Hash
}
function Archive-One([string]$Source,[string]$RelativeDestination){
    if(-not(Test-Path -LiteralPath $Source -PathType Leaf)){return}
    $destination=Join-Path $HistoryRoot $RelativeDestination
    if(Test-Path -LiteralPath $destination){
        if(Same-File $Source $destination){
            Write-Host "[C11C-DOCS] already archived: $RelativeDestination"
            if(-not $DryRun){Remove-Item -LiteralPath $Source -Force}
            return
        }
        $destination=Join-Path (Split-Path -Parent $destination) (([IO.Path]::GetFileNameWithoutExtension($destination)) + '_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + ([IO.Path]::GetExtension($destination)))
    }
    Write-Host "[C11C-DOCS] ARCHIVE: $Source -> $destination"
    if($DryRun){return}
    New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
    Move-Item -LiteralPath $Source -Destination $destination -Force
}

# Current documentation must contain only the single active 2.19.6 authority.
foreach($rootName in @('docs\current\c11c','docs\master-prompts')){
    $root=Join-Path $ProjectRoot $rootName
    if(-not(Test-Path -LiteralPath $root)){continue}
    foreach($file in @(Get-ChildItem -LiteralPath $root -File -Recurse -ErrorAction SilentlyContinue)){
        $name=$file.Name
        if($name -match '2\.19\.[0-5]' -or $name -match '2\.19\.x'){
            $relative=$file.FullName.Substring($root.Length+1)
            Archive-One $file.FullName (Join-Path ('current_snapshots\' + $rootName.Replace('\\','_')) $relative)
        }
        elseif($rootName -eq 'docs\master-prompts' -and $name -match 'C11C_PRODUCER_.*2026-09-2[5-7]'){
            $relative=$file.Name
            Archive-One $file.FullName (Join-Path 'producer_legacy_prompts' $relative)
        }
    }
}

# Root continuity files: preserve the newest 2.19.6 set, archive older 2.19.x.
foreach($file in @(Get-ChildItem -LiteralPath $ProjectRoot -File -Filter '*2.19.*' -ErrorAction SilentlyContinue)){
    if($file.Name -match '2\.19\.[0-5]'){ Archive-One $file.FullName (Join-Path 'root_context' $file.Name) }
}
foreach($file in @(Get-ChildItem -LiteralPath $ProjectRoot -File -Filter 'NEXT_PROMPT_C11C_2.19.*' -ErrorAction SilentlyContinue)){
    if($file.Name -ne 'NEXT_PROMPT_C11C_2.19.6.txt'){ Archive-One $file.FullName (Join-Path 'root_context' $file.Name) }
}

# Producer context prompts live under the canonical Suite surface. Keep exactly one current dated pair.
$producerRoot=Join-Path $ProjectRoot 'c11c-suite\c11c-producer'
if(Test-Path -LiteralPath $producerRoot){
    foreach($file in @(Get-ChildItem -LiteralPath $producerRoot -File -Filter 'C11C_PRODUCER_MASTER_HANDOVER_2026-09-*.md' -ErrorAction SilentlyContinue)){
        if($file.Name -ne 'C11C_PRODUCER_MASTER_HANDOVER_2026-09-28.md'){ Archive-One $file.FullName (Join-Path 'producer_legacy_prompts' $file.Name) }
    }
    foreach($file in @(Get-ChildItem -LiteralPath $producerRoot -File -Filter 'C11C_PRODUCER_START_PROMPT_2026-09-*.md' -ErrorAction SilentlyContinue)){
        if($file.Name -ne 'C11C_PRODUCER_START_PROMPT_2026-09-28.md'){ Archive-One $file.FullName (Join-Path 'producer_legacy_prompts' $file.Name) }
    }
}

# Historical standalone 2.19 release notes and manifests already archived elsewhere are retained.
Write-Host '[C11C-DOCS] 2.19 consolidation complete: one active 2.19.6 authority, older snapshots historical.'
Write-Host "[C11C-DOCS] Historical archive: $HistoryRoot"
if($DryRun){Write-Host '[C11C-DOCS] DRY RUN — no files moved.'}
