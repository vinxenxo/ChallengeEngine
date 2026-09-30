[CmdletBinding()]
param([switch]$DryRun)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$HistoryRoot=Join-Path $ProjectRoot 'docs\history\c11c\releases\superseded_2.19'
if(-not $DryRun){ New-Item -ItemType Directory -Path $HistoryRoot -Force | Out-Null }

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


# Explicit non-numeric repair notes/snapshots that are no longer current authority.
foreach($fileName in @(
    'C11-C_2.19.12_PREFREEZE_REPAIR_V24.md',
    'C11-C_2.19.12_PREFREEZE_REPAIR_V25.md',
    'C11-C_2.19_C11A1_CANONICAL_PRODUCER_CLOSURE_V16.md',
    'C11-C_2.19_C11A1_CANONICAL_PRODUCER_CLOSURE_V17.md',
    'C11-C_2.19_C11A1_CANONICAL_PRODUCER_CLOSURE_V18.md',
    'C11-C_2.19_C11A1_MANIFEST_PATH_CLOSURE.md',
    'C11-C_2.19_CURRENT_STATE.md',
    'C11-C_2.19_V9_CLOSURE_NOTES.md',
    'C11C_2.19.12_PRE_FREEZE_STATUS.md',
    'C11C_2.19.12_A1_CLOSURE_CHANGELOG_V16.md',
    'C11C_2.19.12_A1_CLOSURE_CHANGELOG_V17.md',
    'C11C_2.19.12_A1_CLOSURE_CHANGELOG_V18.md',
    'C11C_2.19.12_A1_CLOSURE_CHANGELOG_V19.md',
    'C11-C_2.19.12_PREFREEZE_MAINTENANCE_FIX_V36.md'
)) {
    Archive-One (Join-Path $ProjectRoot ('docs\current\c11c\' + $fileName)) (Join-Path 'current_repair_history' $fileName)
}
Archive-One (Join-Path $ProjectRoot 'docs\current\suite\C11C_SUITE_0.1.5_RULES.md') (Join-Path 'suite_history' 'C11C_SUITE_0.1.5_RULES.md')
Archive-One (Join-Path $ProjectRoot 'docs\current\c11c\FULL_ACCEPTANCE_REFERENCE.md') (Join-Path 'current_repair_history' 'FULL_ACCEPTANCE_REFERENCE.md')
Archive-One (Join-Path $ProjectRoot 'docs\current\c11c\C11-C_2.19_REPAIR_MANIFEST.json') (Join-Path 'current_repair_history' 'C11-C_2.19_REPAIR_MANIFEST.json')
Archive-One (Join-Path $ProjectRoot 'docs\master-prompts\MASTER_HANDOVER_C11_B_FREEZE.md') (Join-Path 'master_prompts_history' 'MASTER_HANDOVER_C11_B_FREEZE.md')
Archive-One (Join-Path $ProjectRoot 'docs\master-prompts\MASTER_HANDOVER_C11_B_REPOSITORY_ORGANIZATION.md') (Join-Path 'master_prompts_history' 'MASTER_HANDOVER_C11_B_REPOSITORY_ORGANIZATION.md')
Archive-One (Join-Path $ProjectRoot 'docs\master-prompts\NEXT_PROMPT_C11C_2.19_CONSOLIDATED.txt') (Join-Path 'master_prompts_history' 'NEXT_PROMPT_C11C_2.19_CONSOLIDATED.txt')
Archive-One (Join-Path $ProjectRoot 'docs\master-prompts\C11C_2.19.12_V33_PREFREEZE_CONTEXT_PACK.md') (Join-Path 'master_prompts_history' 'C11C_2.19.12_V33_PREFREEZE_CONTEXT_PACK.md')

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

# Superseded Producer 0.8 current documents are historical now that 0.9.7 is active.
foreach($fileName in @('C11C_PRODUCER_0.8.0_AUDIT.md','C11C_PRODUCER_0.8.0_CURRENT_STATE.md','C11C_PRODUCER_0.8.0_RUNTIME_ACCEPTANCE.md')) {
    Archive-One (Join-Path $ProjectRoot ('docs\current\producer\' + $fileName)) (Join-Path 'producer_legacy_prompts' $fileName)
}

# Legacy dated Producer prompts stay historical; the active pair is updated separately in c11c-suite/c11c-producer.
$producerRoot=Join-Path $ProjectRoot 'c11c-suite\c11c-producer'
if(Test-Path -LiteralPath $producerRoot){
    foreach($file in @(Get-ChildItem -LiteralPath $producerRoot -File -Filter 'C11C_PRODUCER_MASTER_HANDOVER_2026-09-*.md' -ErrorAction SilentlyContinue)){
        Archive-One $file.FullName (Join-Path 'producer_legacy_prompts' $file.Name)
    }
    foreach($file in @(Get-ChildItem -LiteralPath $producerRoot -File -Filter 'C11C_PRODUCER_START_PROMPT_2026-09-*.md' -ErrorAction SilentlyContinue)){
        Archive-One $file.FullName (Join-Path 'producer_legacy_prompts' $file.Name)
    }
}
Write-Host '[C11C-DOCS] 2.19 documentation consolidation complete; prior numeric 2.19.x material is historical and the unversioned consolidated 2.19 set remains active.'
if($DryRun){Write-Host '[C11C-DOCS] DRY RUN - no files moved.'}
