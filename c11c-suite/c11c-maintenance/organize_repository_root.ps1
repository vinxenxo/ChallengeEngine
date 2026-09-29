[CmdletBinding(SupportsShouldProcess=$true)]
param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $ProjectRoot

# This map intentionally moves only known documentation/evidence clutter.
# Core project entrypoints and canonical production roots remain untouched.
$moves = [ordered]@{}

# Active consolidated documentation / prompts.
$moves['C11-C_2.19_CONSOLIDATION_AND_FAILURE_PREVENTION.md'] = 'docs/current/c11c/C11-C_2.19_CONSOLIDATION_AND_FAILURE_PREVENTION.md'
$moves['C11-D_ROADMAP_V1.0_STATELESS.md'] = 'docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md'
$moves['MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md'] = 'docs/master-prompts/MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md'
$moves['START_PROMPT_C11C_2.19_CONSOLIDATED.md'] = 'docs/master-prompts/START_PROMPT_C11C_2.19_CONSOLIDATED.md'
$moves['MASTER_HANDOVER_C11D_V1.0_STATELESS.md'] = 'docs/master-prompts/MASTER_HANDOVER_C11D_V1.0_STATELESS.md'
$moves['START_PROMPT_C11D_V1.0_STATELESS.md'] = 'docs/master-prompts/START_PROMPT_C11D_V1.0_STATELESS.md'
$moves['NEXT-PROMT.TXT'] = 'docs/history/root/NEXT-PROMT_root_legacy.txt'
$moves['NEXT_PROMPT_C11D_V1.0_STATELESS.txt'] = 'docs/master-prompts/NEXT_PROMPT_C11D_V1.0_STATELESS.txt'
$moves['NEXT_PROMPT_C11C_2.19_CONSOLIDATED.txt'] = 'docs/master-prompts/NEXT_PROMPT_C11C_2.19_CONSOLIDATED.txt'
$moves['FULL_ACEPTANCE_REF.md'] = 'docs/current/c11c/FULL_ACCEPTANCE_REFERENCE.md'

# Historical 2.19 root context / candidate evidence.
foreach ($file in Get-ChildItem -LiteralPath $ProjectRoot -File -Filter 'C11C_2.19.*' | Sort-Object Name) {
    if ($file.Name -like '*CONSOLIDATION_AND_FAILURE_PREVENTION*') { continue }
    $moves[$file.Name] = "docs/history/c11c/releases/superseded_2.19/root_context/$($file.Name)"
}
foreach ($file in Get-ChildItem -LiteralPath $ProjectRoot -File -Filter 'CHANGELOG_C11-C_2.19.*.md' | Sort-Object Name) {
    $moves[$file.Name] = "docs/history/c11c/releases/superseded_2.19/root_changelogs/$($file.Name)"
}
foreach ($file in Get-ChildItem -LiteralPath $ProjectRoot -File -Filter 'README_C11C_2.19*.md' | Sort-Object Name) {
    $moves[$file.Name] = "docs/history/c11c/releases/superseded_2.19/root_context/$($file.Name)"
}
foreach ($file in Get-ChildItem -LiteralPath $ProjectRoot -File -Filter 'FULL_ACCEPTANCE_C11C_2.19.*.ps1' | Sort-Object Name) {
    if ($file.Name -eq 'FULL_ACCEPTANCE_C11C_2.19.12.ps1') { continue }
    $moves[$file.Name] = "docs/history/c11c/releases/superseded_2.19/root_context/$($file.Name)"
}

# Other known release / tool clutter.
$moves['C11C_PRODUCER_0.9.1_CONSOLE_TEST_COMMANDS.md'] = 'docs/history/producer/C11C_PRODUCER_0.9.1_CONSOLE_TEST_COMMANDS.md'
$moves['OVERLAY_MANIFEST.json'] = 'artifacts/legacy/c11c_overlay_metadata/OVERLAY_MANIFEST.json'
$moves['OVERLAY_SHA256.json'] = 'artifacts/legacy/c11c_overlay_metadata/OVERLAY_SHA256.json'
$moves['OVERLAY_README.md'] = 'artifacts/legacy/c11c_overlay_metadata/OVERLAY_README.md'
$moves['MANIFEST.txt'] = 'artifacts/legacy/c11c_overlay_metadata/MANIFEST.txt'
$moves['tree.txt'] = 'artifacts/legacy/repository_inventories/tree.txt'
$moves['CONTINUE.md'] = 'docs/history/root/CONTINUE_root_legacy.md'

# Move duplicate maintenance entrypoints only when destination is identical or absent.
foreach ($name in @('clean-videos.ps1','Make_zip.ps1','prepare_c11c_acceptance_workspace.ps1')) {
    $moves[$name] = "tools/maintenance/$name"
}
$moves['clean-godot.ps1'] = 'docs/history/root/clean-godot_root_legacy.ps1'

$report = [System.Collections.Generic.List[object]]::new()
foreach ($entry in $moves.GetEnumerator()) {
    $src = Join-Path $ProjectRoot $entry.Key
    $dst = Join-Path $ProjectRoot $entry.Value
    if (-not (Test-Path -LiteralPath $src -PathType Leaf)) { continue }

    $item = [ordered]@{source=$entry.Key;destination=$entry.Value;action='SKIP';reason=''}
    if (Test-Path -LiteralPath $dst -PathType Leaf) {
        $srcHash = (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash
        $dstHash = (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash
        if ($srcHash -eq $dstHash) {
            if ($Apply) {
                Remove-Item -LiteralPath $src -Force
                $item.action = 'REMOVED_DUPLICATE'
                $item.reason = 'Destination already contained identical bytes.'
            } else {
                $item.action = 'WOULD_REMOVE_DUPLICATE'
                $item.reason = 'Destination already contains identical bytes.'
            }
        } elseif ($entry.Value -like 'docs/current/*' -or $entry.Value -like 'docs/master-prompts/*') {
            $archive = Join-Path $ProjectRoot ('docs/history/root_conflicts/' + $entry.Key)
            if ($Apply) {
                New-Item -ItemType Directory -Force -Path (Split-Path -Parent $archive) | Out-Null
                if (Test-Path -LiteralPath $archive) {
                    $archive = Join-Path $ProjectRoot ('docs/history/root_conflicts/' + ([System.IO.Path]::GetFileNameWithoutExtension($entry.Key)) + '_root_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + [System.IO.Path]::GetExtension($entry.Key))
                }
                Move-Item -LiteralPath $src -Destination $archive
                $item.action = 'ARCHIVED_ROOT_CONFLICT'
                $item.destination = $archive.Substring($ProjectRoot.Length + 1).Replace('\','/')
                $item.reason = 'Canonical destination differs; root snapshot preserved in history.'
            } else {
                $item.action = 'WOULD_ARCHIVE_ROOT_CONFLICT'
                $item.destination = $archive.Substring($ProjectRoot.Length + 1).Replace('\','/')
                $item.reason = 'Canonical destination differs; root snapshot would be preserved in history.'
            }
        } elseif ($entry.Key -eq 'OVERLAY_MANIFEST.json') {
            $archive = Join-Path $ProjectRoot ('docs/history/root_conflicts/OVERLAY_MANIFEST_root_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.json')
            if ($Apply) {
                New-Item -ItemType Directory -Force -Path (Split-Path -Parent $archive) | Out-Null
                Move-Item -LiteralPath $src -Destination $archive
                $item.action = 'ARCHIVED_ROOT_CONFLICT'
                $item.destination = $archive.Substring($ProjectRoot.Length + 1).Replace('\','/')
                $item.reason = 'Root overlay manifest differs from legacy metadata; preserved as a root snapshot instead of overwriting legacy evidence.'
            } else {
                $item.action = 'WOULD_ARCHIVE_ROOT_CONFLICT'
                $item.destination = $archive.Substring($ProjectRoot.Length + 1).Replace('\','/')
                $item.reason = 'Root overlay manifest differs from legacy metadata; root snapshot would be preserved instead of overwriting legacy evidence.'
            }
        } else {
            $item.action = 'CONFLICT'
            $item.reason = 'Destination exists with different SHA-256; source was not moved.'
        }
    } else {
        if ($Apply) {
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
            Move-Item -LiteralPath $src -Destination $dst
            $item.action = 'MOVED'
        } else {
            $item.action = 'WOULD_MOVE'
        }
    }
    $report.Add([pscustomobject]$item)
}

$conflicts = @($report | Where-Object action -eq 'CONFLICT')
$planned = @($report | Where-Object action -in @('WOULD_MOVE','WOULD_REMOVE_DUPLICATE','WOULD_ARCHIVE_ROOT_CONFLICT'))
$moved = @($report | Where-Object action -in @('MOVED','REMOVED_DUPLICATE','ARCHIVED_ROOT_CONFLICT'))

Write-Host ('[ROOT-ORGANIZER] Project root: ' + $ProjectRoot)
Write-Host ('[ROOT-ORGANIZER] Apply=' + [bool]$Apply)
foreach ($r in $report) {
    Write-Host ('[ROOT-ORGANIZER] ' + $r.action + ' | ' + $r.source + ' -> ' + $r.destination + ($(if($r.reason){' | '+$r.reason}else{''})))
}

$reportRoot = Join-Path $ProjectRoot 'artifacts/tests/reports'
New-Item -ItemType Directory -Force -Path $reportRoot | Out-Null
$reportPath = Join-Path $reportRoot ('repository_root_organization_{0}.json' -f (Get-Date -Format 'yyyyMMdd_HHmmss'))
@{
    schema='C11-C-ROOT-ORGANIZATION-V1'
    apply=[bool]$Apply
    project_root=$ProjectRoot
    planned_changes=$planned.Count
    applied_changes=$moved.Count
    conflicts=$conflicts.Count
    untouched_roots=@('project.godot','GeneradorMaestro.gd','Main.tscn','build_factory.py','release_gate.py','AGENTS.md','README.md','.continue','.githooks','core','assets','challenges','definitions','profiles','schemas','tests','tools','c11c-suite','docs')
    entries=@($report)
} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $reportPath -Encoding UTF8

if ($conflicts.Count -gt 0) {
    Write-Host ('[ROOT-ORGANIZER] CONFLICTS=' + $conflicts.Count) -ForegroundColor Yellow
    exit 2
}
if (-not $Apply) {
    Write-Host ('[ROOT-ORGANIZER] DRY-RUN PASS - planned changes=' + $planned.Count)
} else {
    Write-Host ('[ROOT-ORGANIZER] APPLY PASS - applied changes=' + $moved.Count)
}
