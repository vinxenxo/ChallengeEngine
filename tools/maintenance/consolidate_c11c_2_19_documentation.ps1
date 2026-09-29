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

$CurrentMinor=12
function Test-Prior219([string]$Name){
    $m=[regex]::Match($Name,'2\.19\.(\d+)')
    if(-not $m.Success){ return $false }
    return ([int]$m.Groups[1].Value -lt $CurrentMinor)
}

foreach($rootName in @('docs\current\c11c','docs\master-prompts')){
    $root=Join-Path $ProjectRoot $rootName
    if(-not(Test-Path -LiteralPath $root)){continue}
    foreach($file in @(Get-ChildItem -LiteralPath $root -File -Recurse -ErrorAction SilentlyContinue)){
        if($file.Name -in @('C11-C_2.19_CONSOLIDATED_STATE.md','C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md','C11-C_2.19_COMPLETE_VIDEO_REVIEW_RUNBOOK.md','C11-C_2.19_COMMAND_SHEET.md','C11-C_2.19_DOCUMENTATION_INDEX.md')){ continue }
        if((Test-Prior219 $file.Name)){
            $relative=$file.FullName.Substring($root.Length+1)
            Archive-One $file.FullName (Join-Path ('current_snapshots\' + $rootName.Replace('\','_')) $relative)
        }
        elseif($rootName -eq 'docs\master-prompts' -and $file.Name -match 'C11C_PRODUCER_.*2026-09-2[5-7]'){
            Archive-One $file.FullName (Join-Path 'producer_legacy_prompts' $file.Name)
        }
    }
}

foreach($file in @(Get-ChildItem -LiteralPath $ProjectRoot -File -Filter '*2.19.*' -ErrorAction SilentlyContinue)){
    if((Test-Prior219 $file.Name)){Archive-One $file.FullName (Join-Path 'root_context' $file.Name)}
}
foreach($file in @(Get-ChildItem -LiteralPath $ProjectRoot -File -Filter 'NEXT_PROMPT_C11C_2.19.*' -ErrorAction SilentlyContinue)){
    if($file.Name -notmatch 'CONSOLIDATED' -and (Test-Prior219 $file.Name)){Archive-One $file.FullName (Join-Path 'root_context' $file.Name)}
}

# Legacy dated Producer prompts stay historical; the active pair is updated separately in c11c-suite/c11c-producer.
$producerRoot=Join-Path $ProjectRoot 'c11c-suite\c11c-producer'
if(Test-Path -LiteralPath $producerRoot){
    foreach($file in @(Get-ChildItem -LiteralPath $producerRoot -File -Filter 'C11C_PRODUCER_MASTER_HANDOVER_2026-09-*.md' -ErrorAction SilentlyContinue)){
        if($file.Name -ne 'C11C_PRODUCER_MASTER_HANDOVER_2026-09-28.md'){Archive-One $file.FullName (Join-Path 'producer_legacy_prompts' $file.Name)}
    }
    foreach($file in @(Get-ChildItem -LiteralPath $producerRoot -File -Filter 'C11C_PRODUCER_START_PROMPT_2026-09-*.md' -ErrorAction SilentlyContinue)){
        if($file.Name -ne 'C11C_PRODUCER_START_PROMPT_2026-09-28.md'){Archive-One $file.FullName (Join-Path 'producer_legacy_prompts' $file.Name)}
    }
}
Write-Host '[C11C-DOCS] 2.19 documentation consolidation complete; prior numeric 2.19.x material is historical and the unversioned consolidated 2.19 set remains active.'
if($DryRun){Write-Host '[C11C-DOCS] DRY RUN - no files moved.'}
