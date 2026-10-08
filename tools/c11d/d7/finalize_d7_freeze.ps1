#requires -Version 5.1
[CmdletBinding()]
param([string]$LibraryBaselineNote = 'D7.5 PASS frozen baseline is stored in the project Library; exact Library display name is the external canonical artifact identity.')
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$closeScript = Join-Path $PSScriptRoot 'close_d7_5_handover.ps1'
$masterCurrent = Join-Path $repoRoot 'docs\current\d\MASTER_HANDOVER_C11D_CURRENT.md'
$startCurrent = Join-Path $repoRoot 'docs\current\d\START_PROMPT_C11D_CURRENT.md'
$D7FreezeMarker = '<!-- C11D_D7_FREEZE_HANDOFF -->'
$artifactDir = Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_freeze'
$receiptPath = Join-Path $repoRoot 'artifacts\tests\c11d_d7\d7_5\d7_5_acceptance_receipt.json'
if(-not(Test-Path -LiteralPath $receiptPath)){throw 'D7.5 receipt not found.'}
$receipt=Get-Content -LiteralPath $receiptPath -Raw|ConvertFrom-Json
if($receipt.result -ne 'PASS' -or $receipt.status -ne 'CLOSED'){throw 'D7.5 must be PASS/CLOSED before D7 freeze.'}
foreach($predecessor in @('d7_0/d7_0_audit_receipt.json','d7_1/d7_1_matrix_receipt.json','d7_2/d7_2_validation_receipt.json','d7_3/d7_3_catalog_receipt.json','d7_4/d7_4_identity_receipt.json')){
    $prePath=Join-Path $repoRoot ('artifacts\tests\c11d_d7\'+$predecessor)
    if(-not(Test-Path -LiteralPath $prePath)){throw ('Missing D7 predecessor receipt: {0}' -f $predecessor)}
    $pre=Get-Content -LiteralPath $prePath -Raw|ConvertFrom-Json
    if($pre.result -ne 'PASS' -or $pre.status -ne 'CLOSED'){throw ('D7 predecessor not PASS/CLOSED: {0}' -f $predecessor)}
}
if(Test-Path -LiteralPath $closeScript){
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $closeScript
    if($LASTEXITCODE -ne 0){throw 'D7.5 handover closure failed.'}
}
$buildPath=Join-Path $repoRoot 'build_factory.py'
if(-not(Test-Path -LiteralPath $buildPath)){throw 'Root build_factory.py missing during D7 freeze.'}
$buildHash=(Get-FileHash -LiteralPath $buildPath -Algorithm SHA256).Hash.ToLowerInvariant()
$expectedBuild='3db8fbc21cf0c78430018424f83a9eed5b42df34a3908ba152f6771f0679d2a3'
if($buildHash -ne $expectedBuild){throw 'C11-C build_factory.py SHA-256 mismatch during D7 freeze.'}
New-Item -ItemType Directory -Force -Path $artifactDir|Out-Null
$included=@('build_factory.py','core','challenges','definitions','schemas','profiles','tests','c11c-suite','tools/c11d','docs/current/d','docs/master-prompts','artifacts/tests/c11d_d0','artifacts/tests/c11d_d1','artifacts/tests/c11d_d2','artifacts/tests/c11d_d3','artifacts/tests/c11d_d4','artifacts/tests/c11d_d5','artifacts/tests/c11d_d6','artifacts/tests/c11d_d7')
$records=@()
foreach($item in $included){$p=Join-Path $repoRoot ($item -replace '/', '\');if(Test-Path -LiteralPath $p -PathType Leaf){$f=Get-Item -LiteralPath $p;$records+=[pscustomobject]@{path=$item;size=[int64]$f.Length;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()};continue};if(Test-Path -LiteralPath $p -PathType Container){foreach($f in Get-ChildItem -LiteralPath $p -Recurse -File -ErrorAction SilentlyContinue){$rel=$f.FullName.Substring($repoRoot.Length).TrimStart('\','/') -replace '\\','/';$records+=[pscustomobject]@{path=$rel;size=[int64]$f.Length;sha256=(Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}}}}
$records=@($records|Sort-Object path)
$sha256=New-Object System.Security.Cryptography.SHA256Managed
$sb=New-Object System.Text.StringBuilder
foreach($r in $records){[void]$sb.Append($r.path);[void]$sb.Append("`0");[void]$sb.Append($r.size);[void]$sb.Append("`0");[void]$sb.Append($r.sha256);[void]$sb.Append("`n")}
$treeHash=($sha256.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($sb.ToString()))|ForEach-Object{$_.ToString('x2')})-join ''
$manifest=[ordered]@{checkpoint='C11-D D7.5';phase='D7';status='FROZEN';library_baseline_note=$LibraryBaselineNote;frozen_c11c_baseline='ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip';frozen_c11c_zip_sha256='d85425cf18c5211c8497574f4fc66202d613eacc0ec14cd4e2fef0b24f634a32';build_factory_path='build_factory.py';build_factory_sha256=$buildHash;d7_authorities=[ordered]@{matrix='CANONICAL_D7_1';catalog='CANONICAL_D7_3';identity_provenance='CANONICAL_D7_4';full_acceptance='CANONICAL_D7_5'};coverage=[ordered]@{challenges=9;delivery_profiles=5;modes=2;matrix_rows=90;catalog_items=90;core_cases=90};governance=[ordered]@{master_seed='NOT_ADOPTED';derivation_runtime_activation=$false;cross_domain_seed_sharing='FORBIDDEN';automatic_seed_generation=$false;d4_8='BLOCKED';runtime_authority='NONE';production_execution=$false;renderer_execution=$false;release_directory_forbidden=$true};included_record_count=$records.Count;governed_tree_sha256=$treeHash;created_at_utc=[DateTime]::UtcNow.ToString('o')}
[System.IO.File]::WriteAllText((Join-Path $artifactDir 'd7_freeze_manifest.json'),($manifest|ConvertTo-Json -Depth 20),(New-Object System.Text.UTF8Encoding($false)))
$fr=[ordered]@{checkpoint='C11-D D7 FREEZE';result='PASS';status='FROZEN';d7_5_receipt_sha256=(Get-FileHash -LiteralPath $receiptPath -Algorithm SHA256).Hash.ToLowerInvariant();c11c_build_factory_sha256=$buildHash;governed_tree_sha256=$treeHash;governed_tree_records=$records.Count;library_baseline_note=$LibraryBaselineNote;next='D8.0 - Media QA + Release Pipeline'}
[System.IO.File]::WriteAllText((Join-Path $artifactDir 'd7_freeze_receipt.json'),($fr|ConvertTo-Json -Depth 20),(New-Object System.Text.UTF8Encoding($false)))
$currentBlock=@(
    '','<!-- C11D_D7_FREEZE_HANDOFF -->','','## C11-D D7 FROZEN / D8 READY','',
    '- D7.0-D7.5 PASS/CLOSED.',
    '- D7 phase FROZEN.',
    '- Canonical authorities: matrix CANONICAL_D7_1; catalog CANONICAL_D7_3; identity/provenance CANONICAL_D7_4; full acceptance CANONICAL_D7_5.',
    '- Coverage: 9 challenges x 5 delivery profiles x 2 modes = 90 core cases.',
    '- Governance remains locked; D4.8 BLOCKED; runtime NONE; production/renderer false.',
    '- Next active checkpoint: D8.0 - Media QA + Release Pipeline.',''
) -join [Environment]::NewLine
$enc=New-Object System.Text.UTF8Encoding($false)
foreach($currentPath in @($masterCurrent,$startCurrent)){
    if(Test-Path -LiteralPath $currentPath){
        $raw=[System.IO.File]::ReadAllText($currentPath)
        if(-not $raw.Contains($D7FreezeMarker)){
            [System.IO.File]::WriteAllText($currentPath,$raw.TrimEnd()+[Environment]::NewLine+[Environment]::NewLine+$currentBlock+[Environment]::NewLine,$enc)
        }
    }
}


$docsCurrentDir = Join-Path $repoRoot 'docs\current\d'
$docsMasterDir = Join-Path $repoRoot 'docs\master-prompts'
New-Item -ItemType Directory -Force -Path $docsCurrentDir,$docsMasterDir | Out-Null
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$closureDoc = @'
# C11-D D7 — FINAL PHASE FREEZE

## Status

D7 = FROZEN / CLOSED.

D7.0 through D7.5 are PASS/CLOSED. The canonical matrix contains 90 core cases (9 challenges × 5 delivery profiles × 2 modes), the catalog contains 90 items, and catalog identity/provenance is 1:1 with the matrix.

## Authorities

- Matrix: CANONICAL_D7_1.
- Catalog: CANONICAL_D7_3.
- Identity/Provenance: CANONICAL_D7_4.
- Full Acceptance: CANONICAL_D7_5.

## Governance

`master_seed=NOT_ADOPTED`; runtime derivation disabled; automatic seed generation disabled; cross-domain seed sharing `FORBIDDEN`; D4.8 `BLOCKED`; runtime authority `NONE`; production and renderer execution disabled; `release/` is not created by D7.

## C11-C boundary

Frozen C11-C baseline: `ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip`.
SHA-256: `D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32`.

Active C11-C `build_factory.py` remains at repository root with SHA-256 `3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3`.

## Evidence

- `artifacts/tests/c11d_d7/d7_5/d7_5_acceptance_receipt.json`
- `artifacts/tests/c11d_d7/d7_freeze/d7_freeze_receipt.json`
- `artifacts/tests/c11d_d7/d7_freeze/d7_freeze_manifest.json`

## Next

D8.0 — Media QA + Release Pipeline.
'@
[System.IO.File]::WriteAllText((Join-Path $docsCurrentDir 'D7_FINAL_FREEZE_CLOSURE.md'),$closureDoc,$utf8NoBom)

$masterDoc = @'
# C11-D — MASTER HANDOVER — D7 FROZEN / D8 READY

D7 = FROZEN / CLOSED.
Next active checkpoint: **D8.0 — Media QA + Release Pipeline**.

Completed: D0 PASS/CLOSED; D1 PASS/CLOSED; D2 PASS/CLOSED; D3 PASS/CLOSED; D4 PASS/CLOSED (D4.8 remains BLOCKED); D5 PASS/CLOSED; D6 PASS/CLOSED; D7 PASS/CLOSED + FROZEN.

D7 authorities: matrix `CANONICAL_D7_1`; catalog `CANONICAL_D7_3`; identity/provenance `CANONICAL_D7_4`; full acceptance `CANONICAL_D7_5`.
Coverage: 9 challenges × 5 delivery profiles × 2 modes = 90 core cases.

Governance locks: `master_seed=NOT_ADOPTED`; runtime derivation disabled; automatic seed generation disabled; cross-domain seed sharing `FORBIDDEN`; D4.8 `BLOCKED`; runtime `NONE`; production false; renderer false.

Protect C11-C simulation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts, logical 540x960 geometry, and proven C11-C presentation/production behavior.

C11-C frozen ZIP: `ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip`.
C11-C ZIP SHA-256: `D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32`.
Root `build_factory.py` SHA-256: `3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3`.

The latest D7.5 PASS frozen baseline is stored in the project Library and is the D8 source of truth. Do not resume from earlier D7 candidate overlays.

Read this handover, then `START_PROMPT_C11D_D8.0.md`, then the D7 freeze receipt/manifest before changing anything.
'@
[System.IO.File]::WriteAllText((Join-Path $docsMasterDir 'MASTER_HANDOVER_C11D_D7_FROZEN.md'),$masterDoc,$utf8NoBom)

$startDoc = @'
# C11-D D8.0 — START PROMPT

Continue `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` from the **FROZEN D7.5 baseline** stored in the project Library.

C11-C is immutable at `ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip` with SHA-256 `D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32`.
Root `build_factory.py` SHA-256: `3DB8FBC21CF0C78430018424F83A9EED5B42DF34A3908BA152F6771F0679D2A3`.

D7.0-D7.5 are PASS/CLOSED and D7 is FROZEN. Authorities: matrix `CANONICAL_D7_1`; catalog `CANONICAL_D7_3`; identity/provenance `CANONICAL_D7_4`; full acceptance `CANONICAL_D7_5`. Coverage = 9 challenges × 5 profiles × 2 modes = 90 core cases.

Governance remains locked: `master_seed=NOT_ADOPTED`; runtime derivation disabled; automatic seed generation disabled; cross-domain seed sharing `FORBIDDEN`; D4.8 `BLOCKED`; runtime `NONE`; production false; renderer false.

Protect C11-C simulation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts, logical 540x960 geometry, and proven C11-C presentation/production behavior.

D8 roadmap: D8.0 Media QA/boundary; D8.1 ffprobe/media integrity; D8.2 visual QA; D8.3 audio QA integration; D8.4 artifact eligibility/provenance-to-media; D8.5 deterministic release manifest/staging policy; D8.6 release dry-run + negatives; D8.7 full D8 acceptance + freeze.

First action: inventory existing media QA/release tooling and evidence. Establish the canonical D8.0 contract before implementing release execution. Do not infer authorization from D7; D4.8 remains BLOCKED until a future explicit authorization checkpoint.
'@
[System.IO.File]::WriteAllText((Join-Path $docsMasterDir 'START_PROMPT_C11D_D8.0.md'),$startDoc,$utf8NoBom)

$currentBlock = @(
    '', '<!-- C11D_D7_FREEZE_HANDOFF -->', '',
    '## C11-D D7 FROZEN / D8 READY', '',
    '- D7.0-D7.5 PASS/CLOSED.',
    '- D7 phase FROZEN.',
    '- Canonical authorities: matrix CANONICAL_D7_1; catalog CANONICAL_D7_3; identity/provenance CANONICAL_D7_4; full acceptance CANONICAL_D7_5.',
    '- Coverage: 9 challenges x 5 delivery profiles x 2 modes = 90 core cases.',
    '- Governance remains locked; D4.8 BLOCKED; runtime NONE; production/renderer false.',
    '- Next active checkpoint: D8.0 - Media QA + Release Pipeline.', ''
) -join [Environment]::NewLine
foreach($currentPath in @($masterCurrent,$startCurrent)){
    if(Test-Path -LiteralPath $currentPath){
        $raw=[System.IO.File]::ReadAllText($currentPath)
        if(-not $raw.Contains('<!-- C11D_D7_FREEZE_HANDOFF -->')){
            [System.IO.File]::WriteAllText($currentPath,$raw.TrimEnd()+[Environment]::NewLine+[Environment]::NewLine+$currentBlock+[Environment]::NewLine,$utf8NoBom)
        }
    }
}
Write-Host 'D7 FREEZE = PASS / FROZEN'
Write-Host ('Governed tree records = {0}; SHA-256 = {1}' -f $records.Count,$treeHash)
Write-Host 'NEXT = D8.0 - Media QA + Release Pipeline'
