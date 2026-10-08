[CmdletBinding()]
param(
    [string]$ProjectRoot = '',
    [string]$BaselineZip = '',
    [switch]$VerifyBaselineZip
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Resolve the repository root only after parameter binding.
# Using $PSScriptRoot in a parameter default is unsafe here because it may be empty
# during nested PowerShell invocation. The script path itself is stable in the body.
if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $ProjectRoot = (Get-Location).Path
}
$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
if(-not (Test-Path -LiteralPath (Join-Path $ProjectRoot 'tools/c11d/d8') -PathType Container)){
    throw "ProjectRoot does not look like ChallengeEngineV01_STATELESS: $ProjectRoot"
}
$EvidenceRoot = Join-Path $ProjectRoot 'artifacts/tests/c11d_d8/d8_0'
$EvidenceRel = 'artifacts/tests/c11d_d8/d8_0'
. (Join-Path $PSScriptRoot 'd8_media_scope.ps1')


function Write-Utf8NoBom([string]$Path, [string]$Text) {
    $enc = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Text, $enc)
}

function CanonicalJson($Value) {
    return ($Value | ConvertTo-Json -Depth 40 -Compress)
}

function Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Rel([string]$FullPath) {
    $resolved = (Resolve-Path -LiteralPath $FullPath).Path
    if($resolved.StartsWith($ProjectRoot, [System.StringComparison]::OrdinalIgnoreCase)){
        return $resolved.Substring($ProjectRoot.Length).TrimStart('\','/').Replace('\','/')
    }
    throw "Path escapes ProjectRoot: $resolved"
}

function IsUnderEvidence([string]$RelativePath) {
    $p = $RelativePath.Replace('\','/').TrimStart('./')
    return ($p -eq $EvidenceRel -or $p.StartsWith($EvidenceRel + '/'))
}

function Get-FileSnapshot {
    param([string]$Root)
    $items = @()
    foreach ($f in Get-ChildItem -LiteralPath $Root -File -Recurse -Force) {
        $r = Rel $f.FullName
        if (IsUnderEvidence $r) { continue }
        $parts = @($r.Split('/'))
        $isArtifact = ($parts.Count -gt 0 -and $parts[0] -eq 'artifacts')
        $isMedia = (MediaExtensions -contains $f.Extension.ToLowerInvariant())
        $record = [ordered]@{
            path = $r
            bytes = [int64]$f.Length
            last_write_utc_ticks = $f.LastWriteTimeUtc.Ticks
        }
        if((-not $isArtifact) -or (-not $isMedia)){
            $record['sha256'] = Sha256 $f.FullName
        } else {
            $record['sha256'] = $null
            $record['fingerprint_mode'] = 'metadata-only-media'
        }
        $items += $record
    }
    return @($items | Sort-Object path)
}

function Compare-Snapshot($Before, $After) {
    $b = @{}; foreach($x in $Before){$b[$x.path] = $x}
    $a = @{}; foreach($x in $After){$a[$x.path] = $x}
    $added = @(); $removed = @(); $changed = @()
    foreach($k in $a.Keys){
        if(-not $b.ContainsKey($k)){ $added += $a[$k] }
        elseif($a[$k].bytes -ne $b[$k].bytes -or $a[$k].last_write_utc_ticks -ne $b[$k].last_write_utc_ticks -or $a[$k].sha256 -ne $b[$k].sha256){
            $changed += [ordered]@{path=$k; before=$b[$k]; after=$a[$k]}
        }
    }
    foreach($k in $b.Keys){ if(-not $a.ContainsKey($k)){ $removed += $b[$k] } }
    return [ordered]@{pass=($added.Count -eq 0 -and $removed.Count -eq 0 -and $changed.Count -eq 0); added=@($added|Sort-Object path); removed=@($removed|Sort-Object path); changed=@($changed|Sort-Object path)}
}

function Discover-Command([string]$Name) {
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue | Select-Object -First 1
    if($null -eq $cmd){ return [ordered]@{name=$Name; available=$false} }
    $version = @()
    try { $version = & $cmd.Source -version 2>&1 | ForEach-Object { $_.ToString() } } catch { $version = @("ERROR: $($_.Exception.Message)") }
    return [ordered]@{name=$Name; available=$true; source=$cmd.Source; command_type=$cmd.CommandType.ToString(); version=@($version)}
}

function Get-TotalBytes($Files) {
    $total = [int64]0
    foreach($file in @($Files)){
        if($null -ne $file){ $total += [int64]$file.Length }
    }
    return $total
}

function MediaExtensions {
    return @(Get-D8MediaExtensions)
}

function Inventory-Media {
    $exts = MediaExtensions
    $roots = @('artifacts','release')
    $byRoot = @()
    $all = @()
    foreach($rootRel in $roots){
        $root = Join-Path $ProjectRoot $rootRel
        if(-not (Test-Path -LiteralPath $root -PathType Container)){
            $byRoot += [ordered]@{root=$rootRel; present=$false; media_count=0; media_bytes=0; media_by_extension=@()}
            continue
        }
        $files = @(Get-ChildItem -LiteralPath $root -File -Recurse -Force)
        $media = @($files | Where-Object { $exts -contains $_.Extension.ToLowerInvariant() })
        $all += $media
        $groups = @($media | Group-Object { $_.Extension.ToLowerInvariant() } | Sort-Object Name | ForEach-Object { [ordered]@{extension=$_.Name; count=$_.Count; bytes=(Get-TotalBytes $_.Group)} })
        $byRoot += [ordered]@{root=$rootRel; present=$true; file_count=$files.Count; media_count=$media.Count; media_bytes=(Get-TotalBytes $media); media_by_extension=$groups}
    }
    $workspaceMedia = @(
        Get-ChildItem -LiteralPath $ProjectRoot -File -Recurse -Force |
          Where-Object { -not (IsUnderEvidence (Rel $_.FullName)) -and ($exts -contains $_.Extension.ToLowerInvariant()) }
    )
    $samples = @($workspaceMedia | Sort-Object FullName | Select-Object -First 200 | ForEach-Object { [ordered]@{path=(Rel $_.FullName); bytes=[int64]$_.Length; extension=$_.Extension.ToLowerInvariant()} })
    return [ordered]@{media_extensions=$exts; roots=$byRoot; workspace_media_count=$workspaceMedia.Count; workspace_media_bytes=(Get-TotalBytes $workspaceMedia); sample_limit=200; sample=$samples}
}

function Inventory-RelevantFiles {
    $roots = @('artifacts','release','definitions','tools','tests','docs/current/d','docs/master-prompts')
    $patterns = @('*manifest*.json','*receipt*.json','*.framemd5','*.md5','*.sha256','*.sha','*provenance*.json','*sidecar*','*probe*.json','*release*','*qa*.json')
    $items = @()
    foreach($rr in $roots){
        $root = Join-Path $ProjectRoot $rr
        if(-not (Test-Path -LiteralPath $root -PathType Container)){ continue }
        foreach($f in Get-ChildItem -LiteralPath $root -File -Recurse -Force){
            $match = $false
            foreach($p in $patterns){ if($f.Name -like $p){$match=$true;break} }
            if($match -and -not (IsUnderEvidence (Rel $f.FullName))){
                $items += [ordered]@{path=(Rel $f.FullName); bytes=[int64]$f.Length; sha256=(Sha256 $f.FullName); extension=$f.Extension.ToLowerInvariant()}
            }
        }
    }
    return @($items|Sort-Object path)
}

function Inventory-FFmpegCallers {
    $roots = @('tools','tests','release_gate.py','docs/current/d')
    $callers = @()
    $needle = '(?i)ffmpeg(?:\.exe)?|ffprobe(?:\.exe)?'
    foreach($rr in $roots){
        $root=Join-Path $ProjectRoot $rr
        if(-not (Test-Path -LiteralPath $root)){continue}
        $files = if((Get-Item -LiteralPath $root).PSIsContainer){ Get-ChildItem -LiteralPath $root -File -Recurse -Force | Where-Object {$_.Extension -in @('.ps1','.py','.gd','.bat','.cmd','.sh','.txt','.md')} } else { Get-Item -LiteralPath $root }
        foreach($f in $files){
            $lines = @(Get-Content -LiteralPath $f.FullName -ErrorAction Stop)
            $hits=@()
            for($i=0;$i -lt $lines.Count;$i++){ if($lines[$i] -match $needle){ $hits += [ordered]@{line=($i+1); text=$lines[$i].Trim()} } }
            if($hits.Count -gt 0){
                $mutationHints=@()
                foreach($h in $hits){
                    if($h.text -match '(?i)\-y\b|OutFile|Set-Content|WriteAllBytes|Copy-Item|Move-Item|Remove-Item|Delete|mux|transcod|encode|extract'){ $mutationHints += $h }
                }
                $callers += [ordered]@{path=(Rel $f.FullName); sha256=(Sha256 $f.FullName); ffmpeg_reference_lines=$hits; media_mutation_hints=$mutationHints}
            }
        }
    }
    return @($callers|Sort-Object path)
}

function Read-JsonIfPresent([string]$RelativePath){
    $p=Join-Path $ProjectRoot $RelativePath
    if(-not (Test-Path -LiteralPath $p -PathType Leaf)){ return $null }
    try { return (Get-Content -LiteralPath $p -Raw -Encoding UTF8 | ConvertFrom-Json) } catch { return [ordered]@{parse_error=$_.Exception.Message} }
}

function Find-GovernanceEvidence {
    $candidates=@(
        'definitions/c11d/production/C11D_PRODUCTION_ACTIVATION_POLICY_V1.json',
        'artifacts/tests/c11d_d4/d4_8/d4_8_authorization_evidence.json',
        'artifacts/tests/c11d_d4/d4_8/d4_8_validation_receipt.json'
    )
    $found=@()
    foreach($r in $candidates){
        $j=Read-JsonIfPresent $r
        if($null -ne $j){$found += [ordered]@{path=$r; sha256=(Sha256 (Join-Path $ProjectRoot $r)); json=$j}}
    }
    $d7Candidates=@()
    $d7Root=Join-Path $ProjectRoot 'artifacts/tests/c11d_d7'
    if(Test-Path -LiteralPath $d7Root -PathType Container){
        $d7Candidates = @(Get-ChildItem -LiteralPath $d7Root -File -Recurse -Force | Where-Object {$_.Name -match '(?i)(matrix|catalog|identity|provenance|acceptance|receipt|freeze).*\.json$'} | ForEach-Object {[ordered]@{path=(Rel $_.FullName); bytes=[int64]$_.Length; sha256=(Sha256 $_.FullName)}} | Sort-Object path)
    }
    return [ordered]@{governance_documents=$found; d7_evidence_candidates=$d7Candidates}
}

$baselinePath = $null
$baselineHash = $null
if(-not [string]::IsNullOrWhiteSpace($BaselineZip)){
    $baselinePath = (Resolve-Path -LiteralPath $BaselineZip).Path
    $baselineHash = Sha256 $baselinePath
    if($VerifyBaselineZip -and $baselineHash -ne '396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d'){
        throw "Baseline SHA-256 mismatch: $baselineHash"
    }
}

if(-not (Test-Path -LiteralPath $EvidenceRoot -PathType Container)){ New-Item -ItemType Directory -Path $EvidenceRoot -Force | Out-Null }
$before = Get-FileSnapshot -Root $ProjectRoot

$inventory = [ordered]@{
    contract='C11-D-D8.0-BOUNDARY-INVENTORY-V1'
    phase='D8.0'
    status='INVENTORY_ONLY'
    project_root='.'
    evidence_root=$EvidenceRel
    baseline_zip_path=if($null -ne $baselinePath){(Rel $baselinePath)}else{$null}
    baseline_zip_sha256=$baselineHash
    governance=(Find-GovernanceEvidence)
    binaries=@(Discover-Command 'ffmpeg'; Discover-Command 'ffprobe')
    media=(Inventory-Media)
    d8_media_scope=[ordered]@{declaration_path='definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json';scope_mode='EXPLICIT_REGISTRY_ONLY';candidate_count=@(Resolve-D8MediaScope $ProjectRoot).Count}
    relevant_files=(Inventory-RelevantFiles)
    ffmpeg_ffprobe_callers=(Inventory-FFmpegCallers)
    forbidden_execution_flags=[ordered]@{d4_8='BLOCKED'; runtime_authority='NONE'; production_execution=$false; renderer_execution=$false; master_seed='NOT_ADOPTED'; runtime_derivation_enabled=$false; automatic_seed_generation=$false; cross_domain_seed_sharing='FORBIDDEN'}
    legacy_release_gate=[ordered]@{path='release_gate.py'; present=(Test-Path -LiteralPath (Join-Path $ProjectRoot 'release_gate.py') -PathType Leaf); classification='UNTRUSTED'; authority='NONE'; reason='Pre-existing gate is historical/legacy and is not a D8 authority unless explicitly re-adopted by a later D8 contract.'}
}

$inventoryPath=Join-Path $EvidenceRoot 'd8_0_inventory.json'
Write-Utf8NoBom $inventoryPath (CanonicalJson $inventory)

$classification=@{
  contract='C11-D-D8.0-TOOLING-CLASSIFICATION-V1'
  classification=@(
    [ordered]@{item='release_gate.py'; category='UNTRUSTED'; authority='NONE'; mutation='writes release/RELEASE_MANIFEST.json under its legacy flow'; disposition='do not invoke in D8.0'},
    [ordered]@{item='tools/qa/c11/*'; category='REUSABLE_LEGACY_TOOLING'; authority='NONE'; mutation='some runners invoke ffmpeg with output-producing flags'; disposition='inventory/reference only in D8.0'},
    [ordered]@{item='tests/C7A503AudioVisualFFmpegMuxTest.gd'; category='REUSABLE_LEGACY_TOOLING'; authority='NONE'; mutation='mux test executes ffmpeg'; disposition='do not execute in D8.0'},
    [ordered]@{item='tests/C7A504AudioVisualFFprobeValidationTest.gd'; category='REUSABLE_LEGACY_TOOLING'; authority='NONE'; mutation='ffprobe invocation is read-only but consumes media'; disposition='defer physical media probing to D8.1'},
    [ordered]@{item='release/evidence/*'; category='HISTORICAL_EVIDENCE'; authority='NONE'; mutation='none by inventory'; disposition='do not treat as active C11-D release'},
    [ordered]@{item='tests/reference/c11a1/**/*.framemd5'; category='HISTORICAL_EVIDENCE'; authority='NONE'; mutation='none by inventory'; disposition='regression references, not release eligibility proof'}
  )
}
$classificationPath=Join-Path $EvidenceRoot 'd8_0_tool_classification.json'
Write-Utf8NoBom $classificationPath (CanonicalJson $classification)

$after = Get-FileSnapshot -Root $ProjectRoot
$mutation = Compare-Snapshot $before $after
$mutationPath=Join-Path $EvidenceRoot 'd8_0_mutation_guard.json'
Write-Utf8NoBom $mutationPath (CanonicalJson ([ordered]@{contract='C11-D-D8.0-MUTATION-GUARD-V1'; scope='all files outside artifacts/tests/c11d_d8/d8_0/'; result=$mutation}))

$invHash=Sha256 $inventoryPath
$classHash=Sha256 $classificationPath
$mutHash=Sha256 $mutationPath
$receiptStatus = if($mutation.pass){'PASS'}else{'FAIL'}
$receipt=[ordered]@{
  contract='C11-D-D8.0-CLOSURE-RECEIPT-V1'
  phase='D8.0'
  status=$receiptStatus
  next=if($mutation.pass){'D8.1'}else{'D8.0_REPAIR'}
  authority='CANONICAL_D8_0_INVENTORY'
  governance=[ordered]@{d4_8='BLOCKED'; runtime_authority='NONE'; production_execution=$false; renderer_execution=$false; media_execution='FORBIDDEN'}
  evidence=[ordered]@{inventory_sha256=$invHash; tool_classification_sha256=$classHash; mutation_guard_sha256=$mutHash}
  write_boundary=$EvidenceRel
  mutation_guard=$mutation.pass
}
$receiptPath=Join-Path $EvidenceRoot 'd8_0_receipt.json'
Write-Utf8NoBom $receiptPath (CanonicalJson $receipt)

if(-not $mutation.pass){ throw 'D8.0 mutation guard FAILED. Repository changed outside the D8.0 evidence boundary.' }
Write-Output ('D8.0 INVENTORY PASS | evidence=' + $EvidenceRel + ' | inventory_sha256=' + $invHash)
