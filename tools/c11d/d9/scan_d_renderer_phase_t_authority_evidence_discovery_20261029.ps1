[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Root,
    [switch]$RecordResults,
    [string]$ReportJsonPath,
    [string]$ReportMarkdownPath,
    [string]$TestStdoutPath,
    [string]$TestStderrPath
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0
$Root = [System.IO.Path]::GetFullPath($Root).TrimEnd('\')
$ExpectedRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'
if(-not [string]::Equals($Root,$ExpectedRoot,[System.StringComparison]::OrdinalIgnoreCase)){throw 'CHECKOUT_ROOT_MISMATCH'}
function Get-Sha([string]$P){(Get-FileHash -LiteralPath $P -Algorithm SHA256).Hash.ToLowerInvariant()}
function Get-TextSha([string]$Text){$b=[System.Text.Encoding]::UTF8.GetBytes($Text);$h=[System.Security.Cryptography.SHA256]::Create();try{([BitConverter]::ToString($h.ComputeHash($b))).Replace('-','').ToLowerInvariant()}finally{$h.Dispose()}}
function Test-Hash([string]$S){return ($S -match '^[0-9a-f]{64}$')}

if($RecordResults){
    foreach($P in @($ReportJsonPath,$ReportMarkdownPath,$TestStdoutPath,$TestStderrPath)){if([string]::IsNullOrWhiteSpace($P) -or -not(Test-Path -LiteralPath $P -PathType Leaf)){throw ('PHASE_T_RECORD_INPUT_MISSING='+$P)}}
    $Report = Get-Content -LiteralPath $ReportJsonPath -Raw | ConvertFrom-Json
    if($Report.phase -ne 'T' -or $Report.no_global_absence_claim -ne $true){throw 'PHASE_T_RECORD_REPORT_SCOPE_INVALID'}
    if(-not [string]::Equals([System.IO.Path]::GetFullPath([string]$Report.scan_root).TrimEnd('\'),$Root,[System.StringComparison]::OrdinalIgnoreCase)){throw 'PHASE_T_RECORD_ROOT_MISMATCH'}
    if($Report.status -ne 'CANDIDATE_INVENTORY_READY_FOR_HUMAN_REVIEW'){throw 'PHASE_T_RECORD_SCAN_NOT_CLEAN'}
    if($Report.scan_errors.Count -ne 0){throw 'PHASE_T_RECORD_SCAN_ERRORS_PRESENT'}
    if($Report.source_pins_verified.Count -ne 11){throw ('PHASE_T_RECORD_SOURCE_PIN_COUNT='+$Report.source_pins_verified.Count)}
    foreach($Pin in $Report.source_pins_verified){$Current=Join-Path $Root ($Pin.path -replace '/','\');if(-not(Test-Path -LiteralPath $Current -PathType Leaf)){throw ('PHASE_T_RECORD_PIN_MISSING='+$Pin.path)};if((Get-Sha $Current) -ne $Pin.sha256){throw ('PHASE_T_RECORD_PIN_CHANGED='+$Pin.path)}}
    if($Report.governance.renderer -ne 'OFF' -or $Report.governance.approved_bindings -ne 0 -or $Report.governance.approved_custom_data_bindings -ne 0 -or $Report.governance.approved_renderer_projection_bindings -ne 0 -or $Report.governance.release_authority -ne 'NONE'){throw 'PHASE_T_RECORD_GOVERNANCE_MISMATCH'}
    if($Report.timing_conflicts.Count -ne 2){throw 'PHASE_T_RECORD_TIMING_COUNT_MISMATCH'}
    foreach($C in $Report.timing_conflicts){if($C.declared_total_duration_seconds -ne 11 -or $C.phase_duration_sum_seconds -ne 12 -or $C.status -ne 'BLOCKER_NO_CORRECTION_INFERRED'){throw ('PHASE_T_RECORD_TIMING_CONFLICT='+$C.challenge)}}
    $OutText=[System.IO.File]::ReadAllText($TestStdoutPath);$ErrText=[System.IO.File]::ReadAllText($TestStderrPath)
    if(-not $OutText.Contains('PHASE_T_AUTHORITY_DISCOVERY_TESTS=40/40')){throw 'PHASE_T_RECORD_TEST_MARKER_MISSING'}
    if(-not($ErrText.Contains('Ran 40 tests') -and $ErrText.Contains('OK'))){throw 'PHASE_T_RECORD_TEST_STDERR_INCOMPLETE'}
    $DestJson=Join-Path $Root 'docs\current\d\C11D_PHASE_T_AUTHORITY_EVIDENCE_DISCOVERY_RESULT_20261029_V1.json'
    $DestMd=Join-Path $Root 'docs\current\d\C11D_PHASE_T_AUTHORITY_EVIDENCE_DISCOVERY_RESULT_20261029_V1.md'
    $ReceiptPath=Join-Path $Root 'docs\current\d\C11D_PHASE_T_AUTHORITY_EVIDENCE_DISCOVERY_RESULT_RECEIPT_20261029_V1.md'
    $JsonBytes=[System.IO.File]::ReadAllBytes($ReportJsonPath);$MdBytes=[System.IO.File]::ReadAllBytes($ReportMarkdownPath)
    $Receipt=@"
# Phase T — Authority Evidence Discovery Result Receipt

- Recorded UTC: $([DateTime]::UtcNow.ToString('o'))
- Report status: $($Report.status)
- Files seen: $($Report.counts.files_seen); eligible text files scanned: $($Report.counts.text_files_scanned).
- Candidate files: $($Report.counts.candidate_files); unsearched binary documents/archives: $($Report.counts.unsearched_documents); scan errors: $($Report.counts.scan_errors).
- Scan index SHA-256: $($Report.scan_index_sha256)
- Result JSON SHA-256: $(Get-Sha $ReportJsonPath)
- Result Markdown SHA-256: $(Get-Sha $ReportMarkdownPath)
- Test stdout SHA-256: $(Get-Sha $TestStdoutPath)
- Test stderr SHA-256: $(Get-Sha $TestStderrPath)
- Test marker: `PHASE_T_AUTHORITY_DISCOVERY_TESTS=40/40`; exit code was checked by operator script.

This receipt records a candidate inventory only. No finding is authority by keyword, and no global absence claim is made. Candidate files and every unsearched binary document/archive require human review as appropriate.

Governance remains `renderer=OFF`, all approved binding counts zero, `release_authority=NONE`; CHALLENGE_008/009 remain 11 seconds declared versus 12 seconds of phase duration. No runtime or Godot was invoked.
"@
    $ReceiptBytes=[System.Text.Encoding]::UTF8.GetBytes($Receipt)
    $Destinations=@(@{Path=$DestJson;Bytes=$JsonBytes;Kind='Exact';Already=$false},@{Path=$DestMd;Bytes=$MdBytes;Kind='Exact';Already=$false},@{Path=$ReceiptPath;Bytes=$ReceiptBytes;Kind='Receipt';Already=$false})
    $ExpectedReceiptLines=@('- Result JSON SHA-256: '+(Get-Sha $ReportJsonPath),'- Result Markdown SHA-256: '+(Get-Sha $ReportMarkdownPath),'- Test stdout SHA-256: '+(Get-Sha $TestStdoutPath),'- Test stderr SHA-256: '+(Get-Sha $TestStderrPath),'- Test marker: `PHASE_T_AUTHORITY_DISCOVERY_TESTS=40/40`')
    foreach($D in $Destinations){
        if(Test-Path -LiteralPath $D.Path -PathType Leaf){
            if($D.Kind -eq 'Receipt'){$ExistingText=[System.IO.File]::ReadAllText($D.Path);foreach($Needle in $ExpectedReceiptLines){if(-not $ExistingText.Contains($Needle)){throw ('PHASE_T_ADD_ONLY_RECEIPT_CONFLICT='+$D.Path+'; missing='+$Needle)}};$D.Already=$true}
            else{$Existing=Get-Sha $D.Path;$Tmp=Join-Path $env:TEMP ('TCHK'+[guid]::NewGuid().ToString('N'));[System.IO.File]::WriteAllBytes($Tmp,$D.Bytes);$Incoming=Get-Sha $Tmp;Remove-Item -LiteralPath $Tmp -Force;if($Existing -ne $Incoming){throw ('PHASE_T_ADD_ONLY_CONFLICT='+$D.Path+'; actual='+$Existing)};$D.Already=$true}
        } elseif(Test-Path -LiteralPath $D.Path){throw ('PHASE_T_DESTINATION_NOT_FILE='+$D.Path)} else {$D.Already=$false}
    }
    foreach($D in $Destinations){if(-not $D.Already){$Tmp=$D.Path+'.tmp.'+[guid]::NewGuid().ToString('N');[System.IO.File]::WriteAllBytes($Tmp,$D.Bytes);[System.IO.File]::Move($Tmp,$D.Path)};$RelativeOut=$D.Path.Substring($Root.Length);if($RelativeOut.StartsWith('\')){$RelativeOut=$RelativeOut.Substring(1)};$RelativeOut=$RelativeOut.Replace('\','/');Write-Output ('ADDED_OR_VERIFIED_SHA256='+$RelativeOut+'='+ (Get-Sha $D.Path))}
    Write-Output 'PHASE_T_RESULT=RECORDED_ADD_ONLY'
    Write-Output 'AUTHORITY_DECISION_ADJUDICATION=NOT_PERFORMED; CANDIDATES_REQUIRE_HUMAN_REVIEW'
    Write-Output 'RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; RELEASE_AUTHORITY=NONE'
    return
}

# Scan mode: no repository writes. RecordResults is the only mode that adds the report.
$TextExtensions=@('.md','.markdown','.txt','.rst','.json','.yaml','.yml','.toml','.csv','.ps1','.py','.gd','.tscn','.tres','.xml','.ini','.cfg','.log','.shader','.gdshader')
$UnsearchedExtensions=@('.pdf','.doc','.docx','.odt','.rtf','.xlsx','.xls','.pptx','.ppt','.zip','.7z','.rar')
$ExcludedDirs=@('.git','.godot','node_modules','.venv','venv','__pycache__','bin','obj','dist','build','.pytest_cache','.mypy_cache','cache','tmp','temp')
$SelfExcludedPrefixes=@('docs/current/d/C11D_PHASE_T_','definitions/c11d/review/D_RENDERER_PHASE_T_','tools/c11d/d9/test_d_renderer_phase_t_authority_evidence_discovery_','tools/c11d/d9/scan_d_renderer_phase_t_authority_evidence_discovery_')
$MaxTextBytes=4194304
$MaxHashBytes=52428800
$StrongLinePattern='(?i)\b(approved\s+by|approved_by|authorized\s+by|authorized_by|authorised\s+by|authorised_by|decision\s+authority|decision_authority|approval\s+authority|approval_authority|authority\s+granted|authority_granted|formal(?:ly)?\s+approved|formally_approved|signed\s+off\s+by|signed_off_by|hereby\s+approve|policy\s+adopted|policy_adoption|adoption\s+authorized|adoption_authorized|adoption_authorised|approval_status|decision_status|signatory|approver|authorization\s+record|authorization_record)\b'
$NamePattern='(?i)(authority|authori[sz]ation|approval|policy.*decision|decision.*record|sign.?off|adjudicat|governance|baseline.*approval|release.*authority)'
$Stack=New-Object 'System.Collections.Generic.Stack[string]';$Stack.Push($Root)
$ScanRows=New-Object 'System.Collections.Generic.List[string]'
$Candidates=New-Object 'System.Collections.Generic.List[object]'
$Unsearched=New-Object 'System.Collections.Generic.List[object]'
$Large=New-Object 'System.Collections.Generic.List[object]'
$Errors=New-Object 'System.Collections.Generic.List[object]'
$SourcePins=New-Object 'System.Collections.Generic.List[object]'
$DirectoriesSeen=0;$FilesSeen=0;$TextScanned=0;$CandidateLines=0;$SelfExcluded=0
$CandidatePaths=@{}
$Utf8=[System.Text.Encoding]::UTF8
$ShaAlg=[System.Security.Cryptography.SHA256]::Create()
try {
    while($Stack.Count -gt 0){
        $Dir=$Stack.Pop();$DirectoriesSeen++
        try{$Children=[System.IO.Directory]::GetFileSystemEntries($Dir)}catch{$Errors.Add([pscustomobject]@{path=$Dir;error=$_.Exception.Message});continue}
        foreach($Path in $Children){
            try{$Attr=[System.IO.File]::GetAttributes($Path)}catch{$Errors.Add([pscustomobject]@{path=$Path;error=$_.Exception.Message});continue}
            $Leaf=[System.IO.Path]::GetFileName($Path)
            if(($Attr -band [System.IO.FileAttributes]::Directory) -ne 0){
                if($ExcludedDirs -contains $Leaf.ToLowerInvariant()){continue}
                if(($Attr -band [System.IO.FileAttributes]::ReparsePoint) -ne 0){continue}
                $Stack.Push($Path);continue
            }
            $FilesSeen++
            $Rel=$Path.Substring($Root.Length);if($Rel.StartsWith('\')){$Rel=$Rel.Substring(1)};$Rel=$Rel.Replace('\','/')
            $SelfSkip=$false;foreach($Pref in $SelfExcludedPrefixes){if($Rel.StartsWith($Pref,[System.StringComparison]::OrdinalIgnoreCase)){$SelfSkip=$true;break}}
            if($SelfSkip){$SelfExcluded++;continue}
            $Ext=[System.IO.Path]::GetExtension($Path).ToLowerInvariant()
            try{$Len=([System.IO.FileInfo]$Path).Length}catch{$Errors.Add([pscustomobject]@{path=$Rel;error=$_.Exception.Message});continue}
            if($UnsearchedExtensions -contains $Ext){
                $UH=$null
                if($Len -le $MaxHashBytes){try{$UH=Get-Sha $Path}catch{$Errors.Add([pscustomobject]@{path=$Rel;error=$_.Exception.Message})}}
                $Unsearched.Add([pscustomobject]@{path=$Rel;extension=$Ext;bytes=$Len;sha256=$UH;reason='Binary/document/archive content not searched by this gate; manual or format-aware inspection required.'})
                continue
            }
            if($TextExtensions -notcontains $Ext){continue}
            if($Len -gt $MaxTextBytes){$Large.Add([pscustomobject]@{path=$Rel;bytes=$Len;reason='Exceeds the 4 MiB text-content scan cap; not content-searched.'});continue}
            try{$Bytes=[System.IO.File]::ReadAllBytes($Path);$FHash=([BitConverter]::ToString($ShaAlg.ComputeHash($Bytes))).Replace('-','').ToLowerInvariant();$Text=$Utf8.GetString($Bytes)}catch{$Errors.Add([pscustomobject]@{path=$Rel;error=$_.Exception.Message});continue}
            $TextScanned++;$ScanRows.Add($Rel+'|'+$Bytes.Length+'|'+$FHash)
            $NameHit=($Leaf -match $NamePattern)
            $CandidateMatchList=New-Object 'System.Collections.Generic.List[object]';$LineNo=0
            foreach($Line in ($Text -split "`r?`n")){
                $LineNo++
                if($Line -match $StrongLinePattern){
                    $Snippet=$Line.Trim();if($Snippet.Length -gt 260){$Snippet=$Snippet.Substring(0,257)+'...'};$CandidateMatchList.Add([pscustomobject]@{line=$LineNo;rule='AUTHORITY_APPROVAL_OR_DECISION_FIELD_CANDIDATE';snippet=$Snippet})
                }
                if($CandidateMatchList.Count -ge 10){break}
            }
            if($NameHit -or $CandidateMatchList.Count -gt 0){
                $CandidateLines += $CandidateMatchList.Count
                $Candidates.Add([pscustomobject]@{path=$Rel;sha256=$FHash;bytes=$Bytes.Length;classification='UNREVIEWED_CANDIDATE_NOT_AUTHORITY';filename_match=[bool]$NameHit;matches=@($CandidateMatchList.ToArray())})
            }
        }
    }
} finally {$ShaAlg.Dispose()}
$ScanRowsArray=@($ScanRows.ToArray() | Sort-Object -CaseSensitive)
$IndexText= if($ScanRowsArray.Count -gt 0){([string]::Join("`n",$ScanRowsArray)+"`n")}else{''}
$IndexSha=Get-TextSha $IndexText
# Reconfirm pinned source set for discovery report; no writes performed in scan mode.
$Pins=@(
@{Path='release/C11C_FREEZE_PACKAGE_MANIFEST.json';Hash='e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'},
@{Path='AGENTS.md';Hash='0d4565e57b9fe9bba88a88f10babd175f3bb5e3fb437014866ed1e67d3016b37'},
@{Path='.continue/rules/CONTINUE.md';Hash='52776e55023a36e1ead71cf39a93337ca96f6097bd2c88018c3353484145ac86'},
@{Path='docs/current/d/C11D_ENGINEERING_PHASE_LEDGER_20261029_V5.md';Hash='18a509e5f9345efd5575ef87392a58df7aed8bfcf1c0c9e2dde2396925f938bb'},
@{Path='docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261029_V28.md';Hash='6025f8a79312b551fb12aa375ba2e4a392de55998d6ae98c8ef4aa42555bdb48'},
@{Path='docs/current/d/C11D_PHASE_S_AUTHORITY_EVIDENCE_PREFLIGHT_ACCEPTANCE_REVIEW_20261029_V1.md';Hash='9998e9f0e47db9f3b21265bb65a1266a0dc9d60274de9a82e8a01e4a5e9208de'},
@{Path='docs/current/d/C11D_PHASE_S_AUTHORITY_EVIDENCE_PREFLIGHT_CLOSEOUT_20261029_V1.md';Hash='1986edf289ac4cee6c0738c1cd99b915508bf66c382d123c846380251e281770'},
@{Path='docs/current/d/C11D_PHASE_S_AUTHORITY_EVIDENCE_PREFLIGHT_20261029_V1.json';Hash='6df0e9b3d5d76cc14313c518786b765a86e779f1e110311a0593ee9939675d0d'},
@{Path='docs/current/d/C11D_PHASE_R_OPERATOR_POLICY_DECISION_PACKET_20261029_V1.json';Hash='6b6cd0881e207b0b3ce55de7db87b7aa325f2ea65ecaa94d7efc1afd2a9b386a'},
@{Path='docs/current/d/C11D_PHASE_Q_SEMANTIC_POLICY_DEPENDENCY_MATRIX_20261029_V1.json';Hash='de2d5e548e00442ee8f15ca7514744b402c6400b4a8497b2b6f6671d29b00390'},
@{Path='docs/current/d/C11D_PHASE_P_SOURCE_FRAME_PROVENANCE_ACCEPTANCE_REVIEW_20261029_V1.md';Hash='d75b13453fac89b01eb806aaff162771d33d7ff15d88d6f81c2825cf8bcc9132'}
)
foreach($Pin in $Pins){$P=Join-Path $Root ($Pin.Path -replace '/','\');if(-not(Test-Path -LiteralPath $P -PathType Leaf)){$Errors.Add([pscustomobject]@{path=$Pin.Path;error='SOURCE_PIN_MISSING'});continue};$H=Get-Sha $P;if($H -ne $Pin.Hash){$Errors.Add([pscustomobject]@{path=$Pin.Path;error=('SOURCE_PIN_MISMATCH='+$H)});continue};$SourcePins.Add([pscustomobject]@{path=$Pin.Path;sha256=$H;status='PASS'})}
$Status=if($Errors.Count -eq 0){'CANDIDATE_INVENTORY_READY_FOR_HUMAN_REVIEW'}else{'INCOMPLETE_SCAN_REQUIRES_REMEDIATION'}
$Report=[ordered]@{
 schema_version='1.0.0';phase='T';status=$Status;created_utc=[DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ');scan_root=$Root;
 scope=[ordered]@{working_tree_only=$true;git_history_searched=$false;external_files_searched=$false;text_extensions=$TextExtensions;excluded_directory_names=$ExcludedDirs;self_excluded_prefixes=$SelfExcludedPrefixes;maximum_text_file_bytes=$MaxTextBytes;binary_contents_searched=$false;archive_contents_searched=$false};
 counts=[ordered]@{directories_seen=$DirectoriesSeen;files_seen=$FilesSeen;text_files_scanned=$TextScanned;files_skipped_large=$Large.Count;candidate_files=$Candidates.Count;candidate_match_lines=$CandidateLines;unsearched_documents=$Unsearched.Count;scan_errors=$Errors.Count;self_excluded_files=$SelfExcluded};
 scan_index_sha256=$IndexSha;source_pins_verified=@($SourcePins.ToArray());candidates=@($Candidates.ToArray() | Sort-Object -Property path);unsearched_documents=@($Unsearched.ToArray() | Sort-Object -Property path);skipped_large_files=@($Large.ToArray() | Sort-Object -Property path);scan_errors=@($Errors.ToArray() | Sort-Object -Property path);
 governance=[ordered]@{renderer='OFF';approved_bindings=0;approved_custom_data_bindings=0;approved_renderer_projection_bindings=0;release_authority='NONE'};
 timing_conflicts=@(@{challenge='CHALLENGE_008';declared_total_duration_seconds=11;phase_duration_sum_seconds=12;status='BLOCKER_NO_CORRECTION_INFERRED'},@{challenge='CHALLENGE_009';declared_total_duration_seconds=11;phase_duration_sum_seconds=12;status='BLOCKER_NO_CORRECTION_INFERRED'});
 no_global_absence_claim=$true;candidate_review_disclaimer='Candidates are unreviewed leads only; keyword/filename matches are not proof of authority.';
 coverage_limitations=@('Git history and external files were not searched.','PDF/Office document and archive contents were not searched; inventory is provided for review.','Text files larger than 4 MiB were listed but not content-searched.','Excluded generated/cache/vendor directories are enumerated in scope.');
 aggregate_hash_algorithm='SHA256(path|bytes|sha256 rows sorted by relative path, UTF-8 LF terminated)'
}
if($RecordResults){throw 'INTERNAL_MODE_BRANCH_ERROR'}
$OutDir=Join-Path $env:TEMP ('T'+[guid]::NewGuid().ToString('N').Substring(0,8));New-Item -ItemType Directory -Path $OutDir | Out-Null
$JsonPath=Join-Path $OutDir 'authority_discovery.json';$MdPath=Join-Path $OutDir 'authority_discovery.md'
$JsonText=ConvertTo-Json -InputObject $Report -Depth 12
[System.IO.File]::WriteAllText($JsonPath,$JsonText,[System.Text.UTF8Encoding]::new($false))
$Md=@"
# Phase T — Authority Evidence Discovery Result

- Created UTC: $($Report.created_utc)
- Status: **$Status**
- Checkout: `$Root`
- Files seen: $FilesSeen; text files scanned: $TextScanned; candidates: $($Candidates.Count); unsearched documents/archives: $($Unsearched.Count); large skipped text files: $($Large.Count); scan errors: $($Errors.Count).
- Scan index SHA-256: `$IndexSha`

## Interpretation

This is a read-only candidate inventory. It does not adjudicate authority and does not establish global absence. Every candidate and every unsearched binary document/archive must be reviewed before relying on an absence claim. The eleven-second versus twelve-second conflicts for CHALLENGE_008/009 remain blocked.

## Candidate paths

$(if($Candidates.Count -eq 0){'- No candidate matched the configured filename/content rules. This is not proof of global absence.'}else{($Candidates | ForEach-Object { '- `' + $_.path + '` — `UNREVIEWED_CANDIDATE_NOT_AUTHORITY`; sha256 `' + $_.sha256 + '`; filename match=' + $_.filename_match + '; content matches=' + $_.matches.Count }) -join "`n"})

## Unsearched document/archive paths

$(if($Unsearched.Count -eq 0){'- None found by extension inventory.'}else{($Unsearched | ForEach-Object { '- `' + $_.path + '` — ' + $_.reason }) -join "`n"})

## Scan errors

$(if($Errors.Count -eq 0){'- None.'}else{($Errors | ForEach-Object { '- `' + $_.path + '` — ' + $_.error }) -join "`n"})

## Governance

`renderer=OFF`; all approved binding counters remain zero; `release_authority=NONE`. No runtime, Godot, renderer, payload materialization, or media generation was performed.
"@
[System.IO.File]::WriteAllText($MdPath,$Md,[System.Text.UTF8Encoding]::new($false))
Write-Output ('PHASE_T_SCAN_RESULT_JSON='+$JsonPath)
Write-Output ('PHASE_T_SCAN_RESULT_JSON_SHA256='+(Get-Sha $JsonPath))
Write-Output ('PHASE_T_SCAN_RESULT_MD='+$MdPath)
Write-Output ('PHASE_T_SCAN_RESULT_MD_SHA256='+(Get-Sha $MdPath))
Write-Output ('PHASE_T_SCAN_FILES_SEEN='+$FilesSeen)
Write-Output ('PHASE_T_SCAN_TEXT_FILES='+$TextScanned)
Write-Output ('PHASE_T_SCAN_CANDIDATES='+$Candidates.Count)
Write-Output ('PHASE_T_SCAN_UNSEARCHED_DOCUMENTS='+$Unsearched.Count)
Write-Output ('PHASE_T_SCAN_ERRORS='+$Errors.Count)
Write-Output ('PHASE_T_SCAN_INDEX_SHA256='+$IndexSha)
Write-Output ('PHASE_T_DISCOVERY_STATUS='+$Status)
Write-Output 'PHASE_T_DISCOVERY=PASS_READ_ONLY_INVENTORY_PENDING_HUMAN_REVIEW'
Write-Output 'RUNTIME_REEXECUTED=false; GODOT_INVOKED=false; RENDERER=OFF; RELEASE_AUTHORITY=NONE'
