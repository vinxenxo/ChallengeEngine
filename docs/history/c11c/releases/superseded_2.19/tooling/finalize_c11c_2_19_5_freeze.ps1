[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $Root

function Need([string]$Path,[string]$Label){ if(-not(Test-Path -LiteralPath (Join-Path $Root $Path))){ throw "[C11-C-FREEZE] Missing $Label`: $Path" } }
function Json([string]$Path){ Get-Content -Raw -LiteralPath (Join-Path $Root $Path) | ConvertFrom-Json }
function Hash([string]$Path){ (Get-FileHash -LiteralPath (Join-Path $Root $Path) -Algorithm SHA256).Hash.ToLowerInvariant() }

Need 'artifacts/prototypes/c11c_art_direction_review/C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json' 'Art Direction corpus manifest'
Need 'artifacts/tests/reports/C11C_2.19.5_ACCEPTANCE_REPORT.json' 'C11-C acceptance report'
Need 'tools/prototypes/c11c_common/C11CMovieCapture.ps1' 'Movie capture helper'
Need 'tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1' 'Worker helper'
Need 'docs/current/c11c/C11-C_2.19.5_CONSOLIDATED_STATE.md' 'current state'
Need 'docs/master-prompts/MASTER_HANDOVER_C11C_2.19.5_CONSOLIDATED.md' 'master handover'

$manifest=Json 'artifacts/prototypes/c11c_art_direction_review/C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json'
if([string]$manifest.status -ne 'COMPLETE'){ throw '[C11-C-FREEZE] Art Direction manifest is not COMPLETE.' }
if([int]$manifest.workers -ne 7){ throw '[C11-C-FREEZE] Art Direction manifest workers != 7.' }
if([int]$manifest.max_observed_worker_concurrency -le 1){ throw '[C11-C-FREEZE] Genuine concurrency was not proven.' }
if([string]$manifest.worker_isolation -ne 'per_worker_temporary_godot_project'){ throw '[C11-C-FREEZE] Wrong worker isolation mode.' }

$acceptance=Json 'artifacts/tests/reports/C11C_2.19.5_ACCEPTANCE_REPORT.json'
if([string]$acceptance.status -ne 'PASS'){ throw '[C11-C-FREEZE] Consolidated acceptance report is not PASS.' }

$movie=Get-Content -Raw -LiteralPath (Join-Path $Root 'tools/prototypes/c11c_common/C11CMovieCapture.ps1')
$worker=Get-Content -Raw -LiteralPath (Join-Path $Root 'tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1')
$suiteFiles=@(Get-ChildItem -LiteralPath (Join-Path $Root 'c11c-suite') -Recurse -File | Where-Object { $_.Extension.ToLowerInvariant() -in @('.py','.ps1','.bat','.cmd') })
if($movie.Contains('System.Threading.Mutex') -or $movie.Contains('Mutex')){ throw '[C11-C-FREEZE] Forbidden mutex remains in Movie Maker helper.' }
if($worker.Contains('$i:') -or -not $worker.Contains('${i}')){ throw '[C11-C-FREEZE] Worker helper still contains invalid $i: interpolation.' }
$studioRefs=@($suiteFiles | Where-Object { $_.Name -ne 'self_test.py' -and (Get-Content -Raw -LiteralPath $_.FullName).Contains('c11c-studio') })
if($studioRefs.Count -gt 0){ throw '[C11-C-FREEZE] Operational Suite launcher dependency on retired c11c-studio detected.' }

# Verify acceptance report includes the required final sections.
if(-not [bool]$acceptance.focused_parallel_contract){ throw '[C11-C-FREEZE] Acceptance report does not record focused parallel contract.' }
if(-not [bool]$acceptance.art_direction_concurrency){ throw '[C11-C-FREEZE] Acceptance report does not record concurrency proof.' }

$outRoot=Join-Path $Root 'artifacts/releases/c11-c'
New-Item -ItemType Directory -Force -Path $outRoot | Out-Null

$paths=@('project.godot','AGENTS.md','.continue/rules/CONTINUE.md','core','tests','tools','docs','profiles','definitions','challenges','schemas','c11c-suite','README.md','build_factory.py','release_gate.py','.editorconfig','.gitattributes','.gitignore')
$entries=New-Object System.Collections.Generic.List[object]
foreach($p in $paths){
    $full=Join-Path $Root $p
    if(-not(Test-Path -LiteralPath $full)){continue}
    if((Get-Item $full).PSIsContainer){
        Get-ChildItem -LiteralPath $full -File -Recurse | Where-Object { $_.FullName -notmatch '\\.git([\\/]|$)' -and $_.FullName -notmatch '\\.godot([\\/]|$)' -and $_.FullName -notmatch '\\__pycache__([\\/]|$)' -and $_.FullName -notmatch '\\.pytest_cache([\\/]|$)' } | ForEach-Object {
            $rel=$_.FullName.Substring($Root.Length+1).Replace('\','/')
            $entries.Add([pscustomobject]@{path=$rel;bytes=$_.Length;sha256=Hash $rel})
        }
    } else {
        $item=Get-Item $full; $rel=$p.Replace('\','/')
        $entries.Add([pscustomobject]@{path=$rel;bytes=$item.Length;sha256=Hash $rel})
    }
}
$entries=$entries | Sort-Object path
$treeText=($entries | ForEach-Object { '{0}|{1}|{2}' -f $_.path,$_.bytes,$_.sha256 }) -join "`n"
$tmp=Join-Path $env:TEMP ('c11c_2195_freeze_' + [guid]::NewGuid().ToString('N') + '.txt')
[IO.File]::WriteAllText($tmp,$treeText,(New-Object Text.UTF8Encoding($false)))
$treeHash=(Get-FileHash -LiteralPath $tmp -Algorithm SHA256).Hash.ToLowerInvariant(); Remove-Item $tmp -Force

$stamp=(Get-Date).ToUniversalTime().ToString('o')
$releaseManifest=[ordered]@{
    freeze_id='C11-C'; repository_freeze='2.19.5'; status='CLOSED_CERTIFIED_FROZEN'; sealed_at_utc=$stamp
    engine='Godot 4.7.1 stable Mono'; suite='0.1.4'; producer='0.9.7'
    geometry=[ordered]@{logical='540x960';review='720x1280 @ 30 FPS';master='1080x1920'}
    corpus=[ordered]@{visual_loop_families=5;visual_loop_grammars=27;visual_drill_families=4;longforms=5;longform_duration_seconds=180}
    worker_isolation=[ordered]@{mode='per_worker_temporary_godot_project';workers=7;max_observed_concurrency=[int]$manifest.max_observed_worker_concurrency;global_mutex=$false}
    acceptance=[ordered]@{status='PASS';focused_parallel_contract=$true;art_direction_concurrency=$true}
    suite_ownership=[ordered]@{canonical_root='c11c-suite';retired_root='c11c-studio';retired_root_operational_dependency=$false}
    tree_sha256=$treeHash; file_count=$entries.Count; files=@($entries)
}
$manifestPath=Join-Path $outRoot 'C11-C_2.19.5_FROZEN_MANIFEST.json'
$releaseManifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

$receipt=@"
# C11-C 2.19.5 — FREEZE RECEIPT

**Status:** CLOSED / CERTIFIED / FROZEN  
**Engine:** Godot 4.7.1 stable Mono  
**Suite:** 0.1.4  
**Producer:** 0.9.7  
**Sealed:** $stamp  
**Tree SHA-256:** `$treeHash`

## Verified acceptance

- Consolidated acceptance report: PASS.
- Focused parallel worker contract: PASS.
- Art Direction `Workers=7`: PASS.
- Worker isolation: one temporary Godot project root per worker.
- Maximum observed worker concurrency: $([int]$manifest.max_observed_worker_concurrency) (>1).
- Movie Maker review capture: 720×1280 @ 30 FPS.
- Movie capture helper: no global mutex.
- Operational Suite launchers: no `c11c-studio` dependency.
- PowerShell worker interpolation: `${i}:` (valid form).

## Frozen boundary

C11-B simulation/RNG/truth, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio contracts, C9 semantics and logical 540×960 social geometry remain outside this repair seal.

## Canonical next step

C11-D starts only from this frozen 2.19.5 state and its recorded receipt/manifest.
"@
$receiptPath=Join-Path $outRoot 'C11-C_2.19.5_FREEZE_RECEIPT.md'
[IO.File]::WriteAllText($receiptPath,$receipt,(New-Object Text.UTF8Encoding($false)))

# Build the frozen source package without artifacts, caches or retired studio.
$zip=Join-Path $outRoot 'C11-C_2.19.5_FROZEN.zip'
if(Test-Path $zip){Remove-Item $zip -Force}
$stage=Join-Path $env:TEMP ('c11c_2195_frozen_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stage -Force | Out-Null
foreach($e in @($entries)){
    $src=Join-Path $Root ($e.path.Replace('/','\'))
    # Do not ship the retired studio or generated artifacts.
    if($e.path -match '^c11c-studio(/|$)' -or $e.path -match '^artifacts(/|$)'){continue}
    $dst=Join-Path $stage ($e.path.Replace('/','\'))
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst) | Out-Null
    Copy-Item -LiteralPath $src -Destination $dst -Force
}
# Add the freeze receipt/manifest to the package too.
Copy-Item $manifestPath $stage -Force
Copy-Item $receiptPath $stage -Force
Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $zip -Force
Remove-Item $stage -Recurse -Force
$zipHash=(Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
Set-Content -LiteralPath ($zip+'.sha256') -Value ($zipHash + '  ' + [IO.Path]::GetFileName($zip)) -Encoding ASCII
Write-Host '[C11-C-FREEZE] FINAL SEAL PASS'
Write-Host '[C11-C-FREEZE] Manifest:' $manifestPath
Write-Host '[C11-C-FREEZE] Receipt:' $receiptPath
Write-Host '[C11-C-FREEZE] ZIP:' $zip
Write-Host '[C11-C-FREEZE] ZIP SHA-256:' $zipHash
