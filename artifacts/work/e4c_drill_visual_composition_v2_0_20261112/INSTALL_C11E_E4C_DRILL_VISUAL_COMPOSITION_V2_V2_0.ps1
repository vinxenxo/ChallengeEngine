#requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ProjectRoot,
    [Parameter(Mandatory=$true)][string]$PythonExe,
    [Parameter(Mandatory=$true)][string]$PackageZip
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version 2.0
$script:Stage='INITIALIZE'
$script:StageRoot=$null
$script:EvidenceRoot=$null
$script:JournalPath=$null
$script:PythonCommandLine=$null
$script:Journal=New-Object System.Collections.ArrayList
$script:Added=New-Object System.Collections.ArrayList
$script:Replaced=New-Object System.Collections.ArrayList
$script:RunId='C11E_E4C_DRILL_V2_V2_0_'+[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ',[Globalization.CultureInfo]::InvariantCulture)+'_'+[guid]::NewGuid().ToString('N').Substring(0,8)

function Get-Sha256([string]$Path){return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()}
function Write-Json([string]$Path,$Value){$Value|ConvertTo-Json -Depth 50|Set-Content -LiteralPath $Path -Encoding UTF8}
function Quote-Win32Argument([string]$Value){
    if($null -eq $Value){$Value=''}
    $b=New-Object System.Text.StringBuilder;[void]$b.Append('"');$slashes=0
    foreach($ch in $Value.ToCharArray()){
        if($ch -eq [char]92){$slashes++;continue}
        if($ch -eq [char]34){if($slashes -gt 0){[void]$b.Append(([string][char]92)*(2*$slashes+1))}else{[void]$b.Append([char]92)};[void]$b.Append([char]34);$slashes=0;continue}
        if($slashes -gt 0){[void]$b.Append(([string][char]92)*$slashes);$slashes=0};[void]$b.Append($ch)
    }
    if($slashes -gt 0){[void]$b.Append(([string][char]92)*(2*$slashes))};[void]$b.Append('"');return $b.ToString()
}
function Save-Journal {
    $doc=[ordered]@{schema='C11E-E4C-V2-V2_0-INSTALL-TRANSACTION-JOURNAL-V1';run_id=$script:RunId;stage=$script:Stage;operations=@($script:Journal);updated_utc=[DateTime]::UtcNow.ToString('o')}
    Write-Json $script:JournalPath $doc
}
function Invoke-Python {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][string]$Exe,
        [Parameter(Mandatory=$true)][ValidateNotNullOrEmpty()][string[]]$PythonArguments,
        [ValidateRange(1,900)][int]$TimeoutSeconds=300,
        [string]$WorkingDirectory=$script:StageRoot,
        [hashtable]$Environment=@{}
    )
    if($null -eq $PythonArguments -or $PythonArguments.Count -lt 1){throw 'PYTHON_ARGUMENT_LIST_EMPTY'}
    $quoted=New-Object System.Collections.Generic.List[string]
    foreach($argument in $PythonArguments){if($null -eq $argument){throw 'PYTHON_ARGUMENT_NULL'};$quoted.Add((Quote-Win32Argument ([string]$argument)))}
    $argumentLine=[string]::Join(' ',$quoted.ToArray())
    if([string]::IsNullOrWhiteSpace($argumentLine)){throw 'PYTHON_ARGUMENT_LINE_EMPTY'}
    $script:PythonCommandLine=$Exe+' '+$argumentLine
    Write-Host ('PYTHON_INVOKE='+$script:PythonCommandLine)
    $psi=New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName=$Exe;$psi.Arguments=$argumentLine;$psi.WorkingDirectory=$WorkingDirectory
    $psi.UseShellExecute=$false;$psi.CreateNoWindow=$true
    $psi.RedirectStandardInput=$true;$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true
    foreach($key in $Environment.Keys){$psi.EnvironmentVariables[[string]$key]=[string]$Environment[$key]}
    $proc=New-Object System.Diagnostics.Process;$proc.StartInfo=$psi
    try{
        if(!$proc.Start()){throw 'PYTHON_START_FAILED'}
        $outTask=$proc.StandardOutput.ReadToEndAsync();$errTask=$proc.StandardError.ReadToEndAsync()
        try{$proc.StandardInput.Close()}catch{}
        if(!$proc.WaitForExit($TimeoutSeconds*1000)){
            try{$proc.Kill()}catch{};$proc.WaitForExit()
            $out=$outTask.GetAwaiter().GetResult();$err=$errTask.GetAwaiter().GetResult()
            throw "PYTHON_TIMEOUT: timeout_seconds=$TimeoutSeconds; command=$script:PythonCommandLine; stdout=$out; stderr=$err"
        }
        $out=$outTask.GetAwaiter().GetResult();$err=$errTask.GetAwaiter().GetResult()
        if($proc.ExitCode -ne 0){throw "PYTHON_EXIT=$($proc.ExitCode); command=$script:PythonCommandLine; stdout=$out; stderr=$err"}
        return [pscustomobject]@{ExitCode=[int]$proc.ExitCode;Stdout=$out;Stderr=$err;Command=$script:PythonCommandLine}
    }finally{$proc.Dispose()}
}
function Assert-NoReparseAncestors([string]$Root,[string]$TargetParent){
    $rootFull=[System.IO.Path]::GetFullPath($Root).TrimEnd('\');$parentFull=[System.IO.Path]::GetFullPath($TargetParent)
    if(!$parentFull.StartsWith($rootFull+'\',[System.StringComparison]::OrdinalIgnoreCase) -and $parentFull -ne $rootFull){throw "DESTINATION_PARENT_ESCAPE: $TargetParent"}
    $relative=$parentFull.Substring($rootFull.Length).TrimStart('\');$walk=$rootFull
    foreach($part in ($relative -split '\\')){if([string]::IsNullOrWhiteSpace($part)){continue};$walk=Join-Path $walk $part
        if(Test-Path -LiteralPath $walk -PathType Container){$item=Get-Item -LiteralPath $walk -Force;if(($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0){throw "REPARSE_POINT_DESTINATION_BLOCKED: $walk"}}
    }
}
function Test-FileReplaceRoundTrip([string]$Directory){
    $id=[guid]::NewGuid().ToString('N');$dest=Join-Path $Directory ($id+'_dest.tmp');$source=Join-Path $Directory ($id+'_source.tmp');$backup=Join-Path $Directory ($id+'_backup.tmp');$restoreBackup=Join-Path $Directory ($id+'_restored_postimage.tmp')
    [IO.File]::WriteAllText($dest,'PREIMAGE-'+$id,[Text.Encoding]::UTF8);[IO.File]::WriteAllText($source,'POSTIMAGE-'+$id,[Text.Encoding]::UTF8)
    try{
        if(Test-Path -LiteralPath $backup){throw 'FILE_REPLACE_BACKUP_PATH_NOT_UNIQUE'}
        [IO.File]::Replace($source,$dest,$backup)
        if([IO.File]::ReadAllText($dest) -notmatch ('POSTIMAGE-'+$id) -or [IO.File]::ReadAllText($backup) -notmatch ('PREIMAGE-'+$id)){throw 'FILE_REPLACE_FORWARD_PREFLIGHT_FAIL'}
        [IO.File]::Replace($backup,$dest,$restoreBackup)
        if([IO.File]::ReadAllText($dest) -notmatch ('PREIMAGE-'+$id) -or [IO.File]::ReadAllText($restoreBackup) -notmatch ('POSTIMAGE-'+$id)){throw 'FILE_REPLACE_ROLLBACK_PREFLIGHT_FAIL'}
        return $true
    }finally{foreach($path in @($dest,$source,$backup,$restoreBackup)){if(Test-Path -LiteralPath $path){[IO.File]::Delete($path)}}}
}
function Rollback-Transaction {
    $errors=New-Object System.Collections.ArrayList
    for($i=$script:Journal.Count-1;$i -ge 0;$i--){$entry=$script:Journal[$i]
        try{
            if([string]$entry.status -like 'SKIP*'){$entry.rollback='PREEXISTING_IDENTICAL_PRESERVED'}
            elseif($entry.operation -eq 'ADD'){
                if(Test-Path -LiteralPath $entry.destination -PathType Leaf){$current=Get-Sha256 $entry.destination;if($current -eq $entry.postimage_sha256){[IO.File]::Delete($entry.destination);$entry.rollback='REMOVED_EXACT_POSTIMAGE'}else{$entry.rollback='PRESERVED_UNKNOWN_POSTIMAGE';[void]$errors.Add($entry.destination)}}else{$entry.rollback='ALREADY_ABSENT'}
            }elseif($entry.operation -eq 'REPLACE'){
                $backup=$entry.backup_path
                if([string]::IsNullOrWhiteSpace([string]$backup) -or !(Test-Path -LiteralPath $backup -PathType Leaf)){
                    if((Test-Path -LiteralPath $entry.destination -PathType Leaf) -and (Get-Sha256 $entry.destination) -eq $entry.preimage_sha256){$entry.rollback='NOT_MUTATED_PREIMAGE_STILL_PRESENT'}
                    else{$entry.rollback='BACKUP_MISSING_OR_UNKNOWN_DESTINATION';[void]$errors.Add($entry.destination)}
                    Save-Journal;continue
                }
                if((Get-Sha256 $backup) -ne $entry.preimage_sha256){$entry.rollback='BACKUP_HASH_MISMATCH_PRESERVED';[void]$errors.Add($backup);Save-Journal;continue}
                if(Test-Path -LiteralPath $entry.destination -PathType Leaf){$current=Get-Sha256 $entry.destination;if($current -ne $entry.postimage_sha256){if($current -eq $entry.preimage_sha256){$entry.rollback='PREIMAGE_STILL_PRESENT_BACKUP_RETAINED'}else{$entry.rollback='PRESERVED_UNKNOWN_POSTIMAGE';[void]$errors.Add($entry.destination)};Save-Journal;continue};$rollbackBackup=$backup+'.displaced_'+[guid]::NewGuid().ToString('N');[IO.File]::Replace($backup,$entry.destination,$rollbackBackup);if((Get-Sha256 $entry.destination) -ne $entry.preimage_sha256){throw 'ROLLBACK_RESTORED_HASH_FAIL'};$entry.rollback='RESTORED_EXACT_PREIMAGE';$entry.rollback_displaced_postimage=$rollbackBackup
                }else{[IO.File]::Move($backup,$entry.destination);if((Get-Sha256 $entry.destination) -ne $entry.preimage_sha256){throw 'ROLLBACK_MOVE_HASH_FAIL'};$entry.rollback='RESTORED_PREIMAGE_TO_MISSING_DESTINATION'}
            }
        }catch{$entry.rollback='ROLLBACK_ERROR';$entry.rollback_error=$_.Exception.Message;[void]$errors.Add(($entry.destination+': '+$_.Exception.Message))}
        Save-Journal
    }
    return ,$errors
}

try{
    $script:Stage='PACKAGE_PREFLIGHT'
    if($PSVersionTable.PSVersion.Major -ne 5 -or $PSVersionTable.PSVersion.Minor -ne 1){throw "WINDOWS_POWERSHELL_5_1_REQUIRED: $($PSVersionTable.PSVersion)"}
    $root=[System.IO.Path]::GetFullPath($ProjectRoot);$python=[System.IO.Path]::GetFullPath($PythonExe);$zip=[System.IO.Path]::GetFullPath($PackageZip);$packageRoot=[System.IO.Path]::GetFullPath($PSScriptRoot)
    if(!(Test-Path -LiteralPath $root -PathType Container)){throw "PROJECT_ROOT_MISSING: $root"};if(!(Test-Path -LiteralPath $python -PathType Leaf)){throw "PYTHON_EXE_MISSING: $python"};if(!(Test-Path -LiteralPath $zip -PathType Leaf)){throw "PACKAGE_ZIP_MISSING: $zip"}
    $sidecar=$zip+'.sha256';if(!(Test-Path -LiteralPath $sidecar -PathType Leaf)){throw "PACKAGE_SIDECAR_MISSING: $sidecar"}
    $sideText=(Get-Content -LiteralPath $sidecar -Raw -Encoding UTF8).Trim();if($sideText -notmatch '^([A-Fa-f0-9]{64})\s+(.+)$'){throw 'PACKAGE_SIDECAR_FORMAT_INVALID'}
    $expectedZip=$Matches[1].ToLowerInvariant();$actualZip=Get-Sha256 $zip;if($actualZip -ne $expectedZip){throw "PACKAGE_ZIP_SHA256_FAIL: expected=$expectedZip actual=$actualZip"};Write-Host "PACKAGE_ZIP_SHA256=PASS/$actualZip"
    $manifestPath=Join-Path $packageRoot 'PACKAGE_MANIFEST.json';if(!(Test-Path -LiteralPath $manifestPath -PathType Leaf)){throw 'PACKAGE_MANIFEST_MISSING'}
    $manifest=Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8|ConvertFrom-Json
    if($manifest.schema -ne 'C11E-E4C-VISUAL-COMPOSITION-V2-OVERLAY-MANIFEST-V2_0' -or $manifest.package_id -ne 'C11E_E4C_DRILL_VISUAL_COMPOSITION_V2_REQUALIFICATION_V2_0_20261112'){throw 'PACKAGE_MANIFEST_ID_SCHEMA_FAIL'}
    if($manifest.source_pins.Count -ne 21 -or $manifest.replacements.Count -ne 1 -or $manifest.additions.Count -ne 24 -or $manifest.replace_count -ne $manifest.replacements.Count -or $manifest.add_count -ne $manifest.additions.Count -or $manifest.payload_count -ne ($manifest.replacements.Count+$manifest.additions.Count)){throw 'PIN_OR_OPERATION_COUNT_FAIL'}
    if($manifest.package_class -ne 'HASH_GUARDED_ONE_FILE_REPLACE_PLUS_ADD_ONLY'){throw 'PACKAGE_CLASS_FAIL'}
    $expectedReplacement='tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py'
    $expectedTestAddition='tests/test_c11e_e4c_drill_visual_composition_consumer.py'
    $expectedRequalAddition='tools/c11d/d9/REQUALIFY_C11E_E4C_DRILL_AV_FROM_EXISTING_EVIDENCE_V2.py'
    if([string]$manifest.replacements[0].destination -ne $expectedReplacement){throw 'REPLACEMENT_OPERATION_MATRIX_FAIL'}
    $testItems=@($manifest.additions|Where-Object{[string]$_.destination -eq $expectedTestAddition})
    $requalItems=@($manifest.additions|Where-Object{[string]$_.destination -eq $expectedRequalAddition})
    if($testItems.Count -ne 1 -or $requalItems.Count -ne 1){throw 'ADD_ONLY_OPERATION_MATRIX_FAIL'}
    if([string]$testItems[0].package_path -ne 'payload/add/tests/test_c11e_e4c_drill_visual_composition_consumer.py'){throw 'TEST_MUST_BE_ADD_ONLY_FAIL'}
    if($manifest.package_files.Count -ne 27){throw 'PACKAGE_FILE_COUNT_FAIL'}
    $packagePathRows=@($manifest.package_files|ForEach-Object{[string]$_.path})
    $uniquePackagePathRows=@($packagePathRows|Sort-Object -Unique)
    if($uniquePackagePathRows.Count -ne $packagePathRows.Count){throw 'DUPLICATE_PACKAGE_FILE_PATH'}
    $allOperationRows=@($manifest.replacements)+@($manifest.additions)
    $seenDestinations=@()
    $seenPackageSources=@()
    $replacementDestinations=@($manifest.replacements|ForEach-Object{[string]$_.destination})
    foreach($operationRow in $allOperationRows){
        $destinationKey=[string]$operationRow.destination
        if($seenDestinations -contains $destinationKey){throw "DUPLICATE_OPERATION_DESTINATION: $destinationKey"}
        $seenDestinations+= $destinationKey
        $packageRelative=[string]$operationRow.package_path
        if([IO.Path]::IsPathRooted($packageRelative) -or $packageRelative.Contains('..') -or $packageRelative.Contains(':')){throw "UNSAFE_PACKAGE_SOURCE_PATH: $packageRelative"}
        if($seenPackageSources -contains $packageRelative){throw "DUPLICATE_OPERATION_PACKAGE_SOURCE: $packageRelative"};$seenPackageSources+= $packageRelative
        $requiredPrefix=if($replacementDestinations -contains $destinationKey){'payload/replace/'}else{'payload/add/'}
        if(!$packageRelative.StartsWith($requiredPrefix,[System.StringComparison]::Ordinal)){throw "OPERATION_PACKAGE_PREFIX_MISMATCH: $destinationKey <- $packageRelative"}
        $derivedDestination=$packageRelative.Substring($requiredPrefix.Length)
        if($derivedDestination -cne $destinationKey){throw "OPERATION_PACKAGE_DESTINATION_MISMATCH: destination=$destinationKey derived=$derivedDestination package=$packageRelative"}
        $packageFileRows=@($manifest.package_files|Where-Object{[string]$_.path -eq $packageRelative})
        if($packageFileRows.Count -ne 1 -or [string]$packageFileRows[0].sha256 -ne [string]$operationRow.sha256 -or [long]$packageFileRows[0].bytes -ne [long]$operationRow.bytes){throw "OPERATION_PACKAGE_FILE_BINDING_FAIL: $destinationKey"}
    }
    if($allOperationRows.Count -ne 25){throw 'OPERATION_ROW_COUNT_FAIL'}
    $payloadPackageRows=@($manifest.package_files|Where-Object{([string]$_.path).StartsWith('payload/add/',[System.StringComparison]::Ordinal) -or ([string]$_.path).StartsWith('payload/replace/',[System.StringComparison]::Ordinal)})
    if($payloadPackageRows.Count -ne $allOperationRows.Count){throw 'PAYLOAD_OPERATION_CLOSURE_COUNT_FAIL'}
    foreach($payloadRow in $payloadPackageRows){$payloadOperationMatches=@($allOperationRows|Where-Object{[string]$_.package_path -ceq [string]$payloadRow.path});if($payloadOperationMatches.Count -ne 1){throw "PAYLOAD_OPERATION_CLOSURE_FAIL: $($payloadRow.path)"}}
    $expectedFiles=@($manifest.package_files|ForEach-Object{[string]$_.path}|Sort-Object)
    $actualFiles=@(Get-ChildItem -LiteralPath $packageRoot -File -Recurse|ForEach-Object{$_.FullName.Substring($packageRoot.Length+1).Replace('\','/')}|Where-Object{$_ -ne 'PACKAGE_MANIFEST.json'}|Sort-Object)
    if(Compare-Object -ReferenceObject $expectedFiles -DifferenceObject $actualFiles){throw 'PACKAGE_FILE_INVENTORY_MISMATCH'}
    foreach($file in $manifest.package_files){$full=Join-Path $packageRoot ($file.path -replace '/','\');if(!(Test-Path -LiteralPath $full -PathType Leaf)){throw "PACKAGE_FILE_MISSING: $($file.path)"};if((Get-Item -LiteralPath $full).Length -ne [long]$file.bytes){throw "PACKAGE_FILE_SIZE_MISMATCH: $($file.path)"};if((Get-Sha256 $full) -ne ([string]$file.sha256).ToLowerInvariant()){throw "PACKAGE_FILE_SHA_MISMATCH: $($file.path)"}}
    Write-Host "PACKAGE_INVENTORY=$($manifest.package_files.Count)/$($manifest.package_files.Count) PASS"

    $script:Stage='SOURCE_PIN_PREFLIGHT'
    foreach($pin in $manifest.source_pins){$source=Join-Path $root ($pin.path -replace '/','\');if(!(Test-Path -LiteralPath $source -PathType Leaf)){throw "SOURCE_PIN_MISSING: $($pin.path)"};if((Get-Sha256 $source) -ne ([string]$pin.sha256).ToLowerInvariant()){throw "SOURCE_PIN_FAIL: $($pin.path)"}}
    $frozen=Join-Path $root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json';if((Get-Item -LiteralPath $frozen).Length -ne 796318 -or (Get-Sha256 $frozen) -ne 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'){throw 'FROZEN_C11C_MANIFEST_FAIL'}
    Write-Host 'SOURCE_PINS=21/21 PASS';Write-Host 'FROZEN_C11C_MANIFEST=PASS'

    $script:Stage='POWERSHELL_AST_PREFLIGHT'
    $runner=Join-Path $packageRoot 'payload\add\tools\c11d\d9\RUN_C11E_E4C_DRILL_AV_EXISTING_MEDIA_V2_REQUALIFICATION.ps1'
    foreach($target in @($PSCommandPath,$runner)){$tokens=$null;$errors=$null;[void][System.Management.Automation.Language.Parser]::ParseFile($target,[ref]$tokens,[ref]$errors);if($errors.Count -gt 0){throw "POWERSHELL_AST_FAIL: $target : $($errors[0].Message)"}}
    Write-Host 'POWERSHELL_AST=2/2 PASS'

    $script:Stage='DESTINATION_PREFLIGHT'
    $ops=New-Object System.Collections.ArrayList
    foreach($item in $manifest.replacements){$relative=[string]$item.destination;if([IO.Path]::IsPathRooted($relative) -or $relative.Contains('..') -or $relative.Contains(':')){throw "UNSAFE_REPLACEMENT_DESTINATION: $relative"};$dest=[IO.Path]::GetFullPath((Join-Path $root ($relative -replace '/','\')));if(!$dest.StartsWith($root.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw "DESTINATION_ESCAPE: $relative"};Assert-NoReparseAncestors $root (Split-Path -Parent $dest)
        if(!(Test-Path -LiteralPath $dest -PathType Leaf)){throw "REPLACEMENT_DESTINATION_MISSING: $relative"};$current=Get-Sha256 $dest;$pre=([string]$item.preimage_sha256).ToLowerInvariant();$post=([string]$item.sha256).ToLowerInvariant();if($current -eq $post){$state='SKIP_IDENTICAL_POSTIMAGE'}elseif($current -eq $pre){$state='REPLACE'}else{throw "REPLACEMENT_UNKNOWN_PREIMAGE: $relative current=$current expected_pre=$pre expected_post=$post"}
        [void]$ops.Add([pscustomobject]@{Operation='REPLACE';Relative=$relative;Source=(Join-Path $packageRoot ($item.package_path -replace '/','\'));Destination=$dest;PreimageSha=$pre;Hash=$post;State=$state;Bytes=[long]$item.bytes})
    }
    foreach($item in $manifest.additions){$relative=[string]$item.destination;if([IO.Path]::IsPathRooted($relative) -or $relative.Contains('..') -or $relative.Contains(':')){throw "UNSAFE_ADD_DESTINATION: $relative"};$dest=[IO.Path]::GetFullPath((Join-Path $root ($relative -replace '/','\')));if(!$dest.StartsWith($root.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw "DESTINATION_ESCAPE: $relative"};Assert-NoReparseAncestors $root (Split-Path -Parent $dest)
        if(Test-Path -LiteralPath $dest -PathType Leaf){if((Get-Sha256 $dest) -ne ([string]$item.sha256).ToLowerInvariant()){throw "ADD_COLLISION_DIFFERENT_BYTES: $relative"};$state='SKIP_IDENTICAL'}elseif(Test-Path -LiteralPath $dest){throw "ADD_DESTINATION_NOT_FILE: $relative"}else{$state='ADD'}
        [void]$ops.Add([pscustomobject]@{Operation='ADD';Relative=$relative;Source=(Join-Path $packageRoot ($item.package_path -replace '/','\'));Destination=$dest;PreimageSha=$null;Hash=([string]$item.sha256).ToLowerInvariant();State=$state;Bytes=[long]$item.bytes})
    }
    Write-Host "REPLACEMENT_OPERATIONS=$($manifest.replacements.Count)";Write-Host "ADD_OPERATIONS=$($manifest.additions.Count)";Write-Host 'DESTINATION_CLASSIFICATION=1_REPLACE+24_ADD_ONLY'

    $script:EvidenceRoot=Join-Path $root ('artifacts\tests\c11e\e4c_v2_installer\'+$script:RunId);New-Item -ItemType Directory -Path $script:EvidenceRoot -Force|Out-Null
    $script:JournalPath=Join-Path $script:EvidenceRoot 'TRANSACTION_JOURNAL.json'
    $script:StageRoot=Join-Path $env:TEMP ('C11E_E4C_V2_STAGE_'+[guid]::NewGuid().ToString('N').Substring(0,8));New-Item -ItemType Directory -Path $script:StageRoot|Out-Null
    $script:Stage='STAGING_AND_PYTHON_TESTS'
    # Stage only the test dependencies; all are read from the active checkout and must match pins.
    $stageMap=@(
      @{Source=(Join-Path $root 'core\presentation\PresentationProfile.gd');Relative='core\presentation\PresentationProfile.gd'},
      @{Source=(Join-Path $root 'definitions\c11d\production\C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_V1.json');Relative='definitions\c11d\production\C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_V1.json'},
      @{Source=(Join-Path $root 'definitions\c11d\production\C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_SCHEMA_V1.json');Relative='definitions\c11d\production\C11E_E4C_DRILL_PRESENTATION_TIMEBASE_PROPOSAL_SCHEMA_V1.json'},
      @{Source=(Join-Path $root 'assets\fonts\Inter-Bold.otf');Relative='assets\fonts\Inter-Bold.otf'},
      @{Source=(Join-Path $root 'assets\fonts\NotoSansMono-Regular.ttf');Relative='assets\fonts\NotoSansMono-Regular.ttf'}
    )
    foreach($x in $stageMap){$target=Join-Path $script:StageRoot $x.Relative;New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force|Out-Null;[IO.File]::Copy($x.Source,$target,$true);if((Get-Sha256 $target) -ne (Get-Sha256 $x.Source)){throw "STAGE_SOURCE_COPY_FAIL: $($x.Relative)"}}
    foreach($item in ($manifest.additions|Where-Object{$_.destination -match '^(definitions/c11d/production/|docs/current/e/C11E_E4C_DRILL_COMPOSITION_OPERATOR_DECISION_RECORD)' })){$target=Join-Path $script:StageRoot ($item.destination -replace '/','\');New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force|Out-Null;[IO.File]::Copy((Join-Path $packageRoot ($item.package_path -replace '/','\')),$target,$true)}
    $consumerStage=Join-Path $script:StageRoot 'tools\c11d\d9\c11e_e4c_drill_visual_composition_consumer.py';$testStage=Join-Path $script:StageRoot 'tests\test_c11e_e4c_drill_visual_composition_consumer.py';$requalStage=Join-Path $script:StageRoot 'tools\c11d\d9\REQUALIFY_C11E_E4C_DRILL_AV_FROM_EXISTING_EVIDENCE_V2.py'
    foreach($path in @($consumerStage,$testStage,$requalStage)){New-Item -ItemType Directory -Path (Split-Path -Parent $path) -Force|Out-Null}
    $consumerItem=$manifest.replacements|Where-Object{[string]$_.destination -eq 'tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py'}
    $testItem=$testItems[0]
    $requalItem=$requalItems[0]
    [IO.File]::Copy((Join-Path $packageRoot ($consumerItem.package_path -replace '/','\')),$consumerStage,$true)
    [IO.File]::Copy((Join-Path $packageRoot ($testItem.package_path -replace '/','\')),$testStage,$true)
    [IO.File]::Copy((Join-Path $packageRoot ($requalItem.package_path -replace '/','\')),$requalStage,$true)
    $probe=Join-Path $script:StageRoot 'runtime_probe.py'
    @'
import json, os, sys
os.environ["QT_QPA_PLATFORM"] = "offscreen"
import PySide6
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QColor
app = QGuiApplication(["C11E-V2-RUNTIME-PROBE"])
image = QImage(4, 4, QImage.Format.Format_RGB888)
image.fill(QColor(5, 7, 11))
painter = QPainter(image)
painter.fillRect(1, 1, 2, 2, QColor(240, 241, 242))
painter.end()
assert image.pixelColor(1, 1).red() == 240
assert sys.version_info[:2] == (3, 13), sys.version
print(json.dumps({"python": sys.version, "pyside6": PySide6.__version__, "qt_offscreen": True, "qimage_qpainter": "PASS"}))
'@|Set-Content -LiteralPath $probe -Encoding UTF8
    $pycompile=Invoke-Python -Exe $python -PythonArguments ([string[]]@('-m','py_compile',$consumerStage,$testStage,$requalStage)) -TimeoutSeconds 300 -WorkingDirectory $script:StageRoot
    $runtime=Invoke-Python -Exe $python -PythonArguments ([string[]]@($probe)) -TimeoutSeconds 180 -WorkingDirectory $script:StageRoot -Environment @{QT_QPA_PLATFORM='offscreen'}
    if($runtime.Stdout -notmatch '"qt_offscreen": true' -or $runtime.Stdout -notmatch '"qimage_qpainter": "PASS"'){throw "PYTHON_QT_RUNTIME_PROBE_FAIL: $($runtime.Stdout) $($runtime.Stderr)"}
    $tests=Invoke-Python -Exe $python -PythonArguments ([string[]]@($testStage)) -TimeoutSeconds 600 -WorkingDirectory $script:StageRoot -Environment @{QT_QPA_PLATFORM='offscreen';C11E_TEST_PROJECT_ROOT=$script:StageRoot}
    $testOutput=[string]$tests.Stdout+"`n"+[string]$tests.Stderr
    if($testOutput -notmatch 'Ran 20 tests' -or $testOutput -notmatch 'OK'){throw "STAGED_TESTS_OUTPUT_INVALID: $testOutput"}
    Write-Host 'PYTHON_RUNTIME=3.13/PySide6/Qt_OFFSCREEN_PASS';Write-Host 'PY_COMPILE=3/3 PASS';Write-Host 'STAGED_TESTS=20/20 PASS'
    [IO.File]::WriteAllText((Join-Path $script:EvidenceRoot 'staged_tests.stdout.log'),$tests.Stdout);[IO.File]::WriteAllText((Join-Path $script:EvidenceRoot 'staged_tests.stderr.log'),$tests.Stderr)

    $script:Stage='FILE_REPLACE_PREFLIGHT'
    $preflightDir=Join-Path $script:EvidenceRoot 'file_replace_preflight';New-Item -ItemType Directory -Path $preflightDir -Force|Out-Null
    if(!(Test-FileReplaceRoundTrip $preflightDir)){throw 'FILE_REPLACE_PREFLIGHT_FAIL'};Write-Host 'FILE_REPLACE_PREFLIGHT=FORWARD_AND_ROLLBACK_PASS'

    $script:Stage='IMMEDIATE_RECHECK'
    foreach($pin in $manifest.source_pins){$source=Join-Path $root ($pin.path -replace '/','\');if((Get-Sha256 $source) -ne ([string]$pin.sha256).ToLowerInvariant()){throw "SOURCE_PIN_CHANGED_BEFORE_WRITE: $($pin.path)"}}
    foreach($op in $ops){if($op.State -eq 'SKIP_IDENTICAL' -or $op.State -eq 'SKIP_IDENTICAL_POSTIMAGE'){if((Get-Sha256 $op.Destination) -ne $op.Hash){throw "DESTINATION_CHANGED_BEFORE_WRITE: $($op.Relative)"}}elseif($op.Operation -eq 'REPLACE'){if((Get-Sha256 $op.Destination) -ne $op.PreimageSha){throw "REPLACEMENT_PREIMAGE_CHANGED_BEFORE_WRITE: $($op.Relative)"}}elseif(Test-Path -LiteralPath $op.Destination){throw "ADD_DESTINATION_APPEARED_BEFORE_WRITE: $($op.Relative)"}}
    Write-Host 'IMMEDIATE_RECHECK=PASS'

    $script:Stage='TRANSACTION_INITIALIZE'
    $backupRoot=Join-Path $script:EvidenceRoot 'backups';New-Item -ItemType Directory -Path $backupRoot -Force|Out-Null
    foreach($op in $ops){$entry=[ordered]@{operation=$op.Operation;relative_path=$op.Relative;destination=$op.Destination;preimage_sha256=$op.PreimageSha;postimage_sha256=$op.Hash;backup_path=$null;status=if($op.State -like 'SKIP*'){$op.State}else{'PLANNED'};rollback='NOT_REQUIRED'};[void]$script:Journal.Add($entry)}
    Save-Journal # Durable complete plan exists before the first destination write.

    $script:Stage='TRANSACTION'
    for($i=0;$i -lt $ops.Count;$i++){
        $op=$ops[$i];$entry=$script:Journal[$i]
        if($op.State -like 'SKIP*'){continue}
        $parent=Split-Path -Parent $op.Destination;if(!(Test-Path -LiteralPath $parent -PathType Container)){New-Item -ItemType Directory -Path $parent -Force|Out-Null}
        if($op.Operation -eq 'REPLACE'){
            $temp=$op.Destination+'.'+$script:RunId+'.tmp';$backup=Join-Path $backupRoot (($op.Relative -replace '/','_')+'.'+$script:RunId+'.preimage.bak')
            if((Test-Path -LiteralPath $temp) -or (Test-Path -LiteralPath $backup)){throw "TEMP_OR_BACKUP_COLLISION: $($op.Relative)"}
            $entry.backup_path=$backup;$entry.status='JOURNALED_BEFORE_REPLACE';Save-Journal
            [IO.File]::Copy($op.Source,$temp,$false);if((Get-Sha256 $temp) -ne $op.Hash){throw "REPLACEMENT_TEMP_SHA_FAIL: $($op.Relative)"}
            [IO.File]::Replace($temp,$op.Destination,$backup)
            if((Get-Sha256 $backup) -ne $op.PreimageSha){throw "DISPLACED_PREIMAGE_BACKUP_SHA_FAIL: $($op.Relative)"}
            if((Get-Sha256 $op.Destination) -ne $op.Hash){throw "REPLACEMENT_POSTIMAGE_SHA_FAIL: $($op.Relative)"}
            $entry.status='REPLACED_POSTIMAGE_VERIFIED';[void]$script:Replaced.Add($entry);Save-Journal
        }else{
            $temp=$op.Destination+'.'+$script:RunId+'.tmp';if(Test-Path -LiteralPath $temp){throw "ADD_TEMP_COLLISION: $($op.Relative)"}
            $entry.status='JOURNALED_BEFORE_ADD';Save-Journal
            [IO.File]::Copy($op.Source,$temp,$false);if((Get-Sha256 $temp) -ne $op.Hash){throw "ADD_TEMP_SHA_FAIL: $($op.Relative)"}
            [IO.File]::Move($temp,$op.Destination);if((Get-Sha256 $op.Destination) -ne $op.Hash){throw "ADD_POSTIMAGE_SHA_FAIL: $($op.Relative)"}
            $entry.status='ADDED_POSTIMAGE_VERIFIED';[void]$script:Added.Add($entry);Save-Journal
        }
    }
    $script:Stage='POSTIMAGE_AND_POSTPIN_AUDIT'
    foreach($op in $ops){if((Get-Sha256 $op.Destination) -ne $op.Hash){throw "POSTIMAGE_AUDIT_FAIL: $($op.Relative)"}}
    foreach($pin in $manifest.source_pins){$source=Join-Path $root ($pin.path -replace '/','\');if((Get-Sha256 $source) -ne ([string]$pin.sha256).ToLowerInvariant()){throw "POST_SOURCE_PIN_FAIL: $($pin.path)"}}
    Save-Journal
    $script:Stage='COMPLETE'
    $receipt=[ordered]@{schema='C11E-E4C-VISUAL-COMPOSITION-V2-INSTALL-RECEIPT-V2_0';status='PASS_REPLACE_AND_ADD_ONLY_INSTALL';run_id=$script:RunId;package_id=$manifest.package_id;package_zip_sha256=$actualZip;source_pins='21/21 PASS';replacement_count=1;replacement_postimages=@($manifest.replacements|ForEach-Object{[pscustomobject]@{path=$_.destination;sha256=$_.sha256}});add_count=$manifest.additions.Count;added=@($script:Added|ForEach-Object{$_.relative_path});skipped_identical=@($ops|Where-Object{$_.State -like 'SKIP*'}|ForEach-Object{$_.Relative});powershell_ast='2/2 PASS';python_runtime='3.13/PySide6/Qt OFFSCREEN PASS';py_compile='3/3 PASS';staged_tests='20/20 PASS';file_replace_preflight='FORWARD_AND_ROLLBACK_PASS';postimages='ALL PASS';source_pins_post='21/21 PASS';journal_path=$script:JournalPath;c11c_source_mutation=$false;e1_service_mutation=$false;gui_cli_entrypoint_mutation=$false;dispatch=$false;git_checks='SKIPPED';commits='OPERATOR_MANAGED';release_authority='NONE'}
    $receiptPath=Join-Path $script:EvidenceRoot 'INSTALL_RECEIPT.json';Write-Json $receiptPath $receipt
    Write-Host 'INSTALL_STATUS=PASS_REPLACE_AND_ADD_ONLY_INSTALL';Write-Host "INSTALL_RECEIPT=$receiptPath";Write-Host "TRANSACTION_JOURNAL=$script:JournalPath";Write-Host 'C11C_SOURCE_MUTATION=FALSE';Write-Host 'E1_SERVICE_MUTATION=FALSE';Write-Host 'PRODUCTION_DISPATCH=FALSE';Write-Host 'RELEASE_AUTHORITY=NONE'
}
catch{
    $failure=$_.Exception.Message;$rollbackErrors=New-Object System.Collections.ArrayList
    if($script:Journal.Count -gt 0){$script:Stage='ROLLBACK';$rollbackErrors=Rollback-Transaction}
    $status=if($script:Journal.Count -eq 0){'FAIL_CLOSED_PRE_TRANSACTION_NO_DESTINATION_WRITES'}elseif($rollbackErrors.Count -eq 0){'FAIL_CLOSED_ROLLBACK_COMPLETE'}else{'FAIL_CLOSED_ROLLBACK_INCOMPLETE_UNKNOWN_STATE_PRESERVED'}
    $diag=[ordered]@{schema='C11E-E4C-VISUAL-COMPOSITION-V2-INSTALL-FAILURE-V2_0';status=$status;run_id=$script:RunId;stage=$script:Stage;error=$failure;python_command=$script:PythonCommandLine;journal_path=$script:JournalPath;journal=@($script:Journal);rollback_errors=@($rollbackErrors);git_checks='SKIPPED';commits='OPERATOR_MANAGED';c11c_source_mutation=$false;production_dispatch=$false;release_authority='NONE'}
    if($script:EvidenceRoot){$diagPath=Join-Path $script:EvidenceRoot 'INSTALL_FAILURE.json';Write-Json $diagPath $diag;Write-Error -Message ($status+' ['+$script:Stage+']: '+$failure+'; diagnostic='+$diagPath)}else{$diagPath=Join-Path $env:TEMP ($script:RunId+'_INSTALL_FAILURE.json');Write-Json $diagPath $diag;Write-Error -Message ($status+' ['+$script:Stage+']: '+$failure+'; diagnostic='+$diagPath)}
}
finally{if($script:StageRoot -and (Test-Path -LiteralPath $script:StageRoot)){Remove-Item -LiteralPath $script:StageRoot -Recurse -Force -ErrorAction SilentlyContinue}}
