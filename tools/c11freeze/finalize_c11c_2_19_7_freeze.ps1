[CmdletBinding()]
param()
$ErrorActionPreference='Stop'; Set-StrictMode -Version Latest
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path; Set-Location $Root
function Need([string]$Path,[string]$Label){if(-not(Test-Path -LiteralPath (Join-Path $Root $Path))){throw "[C11-C-FREEZE] Missing $Label`: $Path"}}
function Json([string]$Path){Get-Content -Raw -LiteralPath (Join-Path $Root $Path)|ConvertFrom-Json}
function Hash([string]$Path){(Get-FileHash -LiteralPath (Join-Path $Root $Path) -Algorithm SHA256).Hash.ToLowerInvariant()}
Need 'artifacts/prototypes/c11c_art_direction_review/C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json' 'Art Direction corpus manifest'
Need 'artifacts/prototypes/c11c_art_direction_review/C11-C_COMPLETE_VIDEO_REVIEW_REPORT.json' 'complete video review report'
Need 'artifacts/tests/reports/C11C_2.19.7_ACCEPTANCE_REPORT.json' 'acceptance report'
Need 'tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1' 'worker helper'
Need 'tools/prototypes/c11c_common/C11CMovieCapture.ps1' 'movie helper'
Need 'tools/qa/c11/verify_c11c_suite_launchers.ps1' 'Suite launcher audit'
Need 'docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md' 'current state'
Need 'docs/master-prompts/MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md' 'master handover'
$a=Json 'artifacts/tests/reports/C11C_2.19.7_ACCEPTANCE_REPORT.json'; if([string]$a.status -ne 'PASS'){throw 'Acceptance report is not PASS'}
foreach($k in @('docs_consolidated','suite_self_test','producer_self_test','producer_gui','launcher_audit','parallel_contract','retro_reference','logical','c11a1','retro','physical_smoke','physical_export','video_review')){if(-not [bool]$a.checks.$k){throw "Acceptance check failed: $k"}}
$m=Json 'artifacts/prototypes/c11c_art_direction_review/C11-C_ART_DIRECTION_REVIEW_CORPUS_MANIFEST.json'; if([string]$m.status -ne 'COMPLETE'){throw 'Art Direction manifest not COMPLETE'}; if([int]$m.workers -ne 7){throw 'Workers != 7'}; if([int]$m.max_observed_worker_concurrency -le 1){throw 'Concurrency not proven'}; if([string]$m.worker_isolation -ne 'per_worker_temporary_godot_project'){throw 'Wrong worker isolation'}; if([string]$m.worker_bootstrap -ne 'per_worker_godot_headless_editor_class_scan'){throw 'Missing worker class-cache bootstrap'}
$v=Json 'artifacts/prototypes/c11c_art_direction_review/C11-C_COMPLETE_VIDEO_REVIEW_REPORT.json'; if([string]$v.status -ne 'PASS'){throw 'Complete video review is not PASS'}; if([int]$v.expected_video_count -ne 52 -or [int]$v.loops -ne 27 -or [int]$v.drills -ne 20 -or [int]$v.longforms -ne 5){throw 'Complete video review count mismatch'}
$movie=Get-Content -Raw -LiteralPath (Join-Path $Root 'tools/prototypes/c11c_common/C11CMovieCapture.ps1'); $worker=Get-Content -Raw -LiteralPath (Join-Path $Root 'tools/prototypes/c11c_bulk/C11CReviewWorkerIsolation.ps1'); if($movie.Contains('Mutex')){throw 'Forbidden mutex in Movie Maker helper'}; if($worker.Contains('$i:')){throw 'Invalid PowerShell $i: interpolation remains'}; if(-not $worker.Contains('${i}')){throw 'Worker helper does not contain ${i}'}
$out=Join-Path $Root 'artifacts/releases/c11-c'; New-Item -ItemType Directory -Force -Path $out|Out-Null
$entries=@(); foreach($p in @('project.godot','AGENTS.md','.continue/rules/CONTINUE.md','core','tests','tools','docs','profiles','definitions','challenges','schemas','c11c-suite','README.md','build_factory.py','release_gate.py','.gitignore')){ $full=Join-Path $Root $p; if(-not(Test-Path -LiteralPath $full)){continue}; if((Get-Item $full).PSIsContainer){Get-ChildItem -LiteralPath $full -Recurse -File|Where-Object{$_.FullName -notmatch '\.git([\\/]|$)' -and $_.FullName -notmatch '\.godot([\\/]|$)' -and $_.FullName -notmatch '\__pycache__([\\/]|$)' -and $_.FullName -notmatch '\.pytest_cache([\\/]|$)'}|ForEach-Object{$rel=$_.FullName.Substring($Root.Length+1).Replace('\\','/');$script:entries+=[pscustomobject]@{path=$rel;bytes=$_.Length;sha256=Hash $rel}}}else{$item=Get-Item $full;$script:entries+=[pscustomobject]@{path=$p;bytes=$item.Length;sha256=Hash $p}}}
$entries=$entries|Sort-Object path
$treeText=($entries|ForEach-Object{'{0}|{1}|{2}' -f $_.path,$_.bytes,$_.sha256}) -join "`n"; $tmp=Join-Path $env:TEMP ('c11c_2197_tree_'+[guid]::NewGuid().ToString('N')+'.txt'); [IO.File]::WriteAllText($tmp,$treeText,(New-Object Text.UTF8Encoding($false)));$treeHash=Hash $tmp;Remove-Item $tmp -Force
$stamp=(Get-Date).ToUniversalTime().ToString('o')
$rm=[ordered]@{freeze_id='C11-C';repository_freeze='2.19.7';status='CLOSED_CERTIFIED_FROZEN';sealed_at_utc=$stamp;engine='Godot 4.7.1 stable Mono';suite='0.1.4';producer='0.9.7';geometry=[ordered]@{logical='540x960';review='720x1280 @ 30 FPS';master='1080x1920'};corpus=[ordered]@{visual_loop_families=5;visual_loop_grammars=27;visual_drill_families=4;visual_drill_videos=20;longforms=5;complete_review_videos=52;longform_duration_seconds=180};worker_isolation=[ordered]@{mode='per_worker_temporary_godot_project';workers=7;max_observed_concurrency=[int]$m.max_observed_worker_concurrency;global_mutex=$false;bootstrap='per_worker_godot_headless_editor_class_scan';global_script_class_cache='required';required_class='PresentationProfile'};acceptance=[ordered]@{status='PASS';report='artifacts/tests/reports/C11C_2.19.7_ACCEPTANCE_REPORT.json';complete_video_review='artifacts/prototypes/c11c_art_direction_review/C11-C_COMPLETE_VIDEO_REVIEW_REPORT.json'};suite_ownership=[ordered]@{canonical_root='c11c-suite';retired_root='c11c-studio';retired_root_operational_dependency=$false};tree_sha256=$treeHash;file_count=$entries.Count;files=@($entries)}
$manifestPath=Join-Path $out 'C11-C_2.19.7_FROZEN_MANIFEST.json'; $rm|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $manifestPath -Encoding UTF8
$receipt=@"
# C11-C 2.19.7 — FREEZE RECEIPT

**Status:** CLOSED / CERTIFIED / FROZEN  
**Engine:** Godot 4.7.1 stable Mono  
**Suite:** 0.1.4  
**Producer:** 0.9.7  
**Sealed:** $stamp  
**Tree SHA-256:** `$treeHash`

## Verified

- Full acceptance report PASS.
- Suite launcher audit PASS; `c11c-suite` is the sole active Suite surface.
- `c11c-studio` is retired and not an operational dependency.
- Focused parallel worker contract PASS.
- Art Direction Workers=7 with genuine concurrency >1.
- Per-worker class-cache bootstrap PASS.
- Complete video review PASS: 52/52 (27 loop grammars + 20 Visual Drills + 5 longforms).
- Review media validated at 720×1280 / 30 FPS with audio.
- No global Movie Maker mutex.

## Frozen boundary

C11-B simulation/RNG/truth, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 audio contracts, C9 semantics and logical 540×960 social geometry remain outside this repair seal.
"@
[IO.File]::WriteAllText((Join-Path $out 'C11-C_2.19.7_FREEZE_RECEIPT.md'),$receipt,(New-Object Text.UTF8Encoding($false)))
$zip=Join-Path $out 'C11-C_2.19.7_FROZEN.zip'; if(Test-Path $zip){Remove-Item $zip -Force}; $stage=Join-Path $env:TEMP ('c11c_2197_frozen_'+[guid]::NewGuid().ToString('N'));New-Item -ItemType Directory -Force -Path $stage|Out-Null; foreach($e in $entries){$src=Join-Path $Root ($e.path.Replace('/','\\'));$dst=Join-Path $stage ($e.path.Replace('/','\\'));New-Item -ItemType Directory -Force -Path (Split-Path -Parent $dst)|Out-Null;Copy-Item $src $dst -Force};Copy-Item $manifestPath $stage -Force;Copy-Item (Join-Path $out 'C11-C_2.19.7_FREEZE_RECEIPT.md') $stage -Force;Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $zip -Force;Remove-Item $stage -Recurse -Force;$zh=(Get-FileHash $zip -Algorithm SHA256).Hash.ToLowerInvariant();Set-Content ($zip+'.sha256') ($zh+'  '+[IO.Path]::GetFileName($zip)) -Encoding ASCII
Write-Host '[C11-C-FREEZE] FINAL SEAL PASS';Write-Host '[C11-C-FREEZE] ZIP:' $zip;Write-Host '[C11-C-FREEZE] ZIP SHA-256:' $zh
