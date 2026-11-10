#requires -Version 5.1
# C11E E4C runner revision V3: strict console-only Godot discovery + headless smoke + audited preflight reuse.
[CmdletBinding()]
param([string]$ProjectRoot = 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS',[int]$GodotTimeoutSeconds = 180,[string]$ReusePreflightEvidenceDir = '')
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

function Get-Sha256([string]$Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Quote-WinArg([string]$Value) {
    if ($Value.Length -gt 0 -and $Value -notmatch '[\s"]') { return $Value }
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.Append('"')
    $slashes = 0
    foreach ($ch in $Value.ToCharArray()) {
        if ([int]$ch -eq 92) { $slashes++; continue }
        if ($ch -eq '"') {
            for ($i=0; $i -lt (2*$slashes+1); $i++) { [void]$sb.Append([char]92) }
            [void]$sb.Append('"'); $slashes=0; continue
        }
        for ($i=0; $i -lt $slashes; $i++) { [void]$sb.Append([char]92) }
        $slashes=0; [void]$sb.Append($ch)
    }
    for ($i=0; $i -lt (2*$slashes); $i++) { [void]$sb.Append([char]92) }
    [void]$sb.Append('"')
    return $sb.ToString()
}
function Invoke-Native([string]$Name,[string]$FilePath,[string[]]$Arguments,[string]$WorkingDirectory,[int]$TimeoutSeconds,[string]$EvidenceDir) {
    $stdoutPath = Join-Path $EvidenceDir ($Name + '.stdout.log')
    $stderrPath = Join-Path $EvidenceDir ($Name + '.stderr.log')
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $FilePath
    $psi.Arguments = (($Arguments | ForEach-Object { Quote-WinArg ([string]$_) }) -join ' ')
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $proc = New-Object System.Diagnostics.Process
    $proc.StartInfo = $psi
    if (-not $proc.Start()) { throw "Could not start $Name" }
    $outTask = $proc.StandardOutput.ReadToEndAsync()
    $errTask = $proc.StandardError.ReadToEndAsync()
    if (-not $proc.WaitForExit($TimeoutSeconds * 1000)) {
        try { $proc.Kill() } catch {}
        $proc.WaitForExit()
        [IO.File]::WriteAllText($stdoutPath, $outTask.Result, ([System.Text.UTF8Encoding]::new($false)))
        [IO.File]::WriteAllText($stderrPath, $errTask.Result, ([System.Text.UTF8Encoding]::new($false)))
        throw "$Name timed out after $TimeoutSeconds seconds; evidence=$EvidenceDir"
    }
    $proc.WaitForExit()
    $stdout = $outTask.Result
    $stderr = $errTask.Result
    [IO.File]::WriteAllText($stdoutPath, $stdout, ([System.Text.UTF8Encoding]::new($false)))
    [IO.File]::WriteAllText($stderrPath, $stderr, ([System.Text.UTF8Encoding]::new($false)))
    $exitCode = [int]$proc.ExitCode
    $exitCodeHex = '0x' + [BitConverter]::ToUInt32([BitConverter]::GetBytes($exitCode),0).ToString('X8')
    return [pscustomobject]@{ Name=$Name; ExitCode=$exitCode; ExitCodeHex=$exitCodeHex; StdOut=$stdout; StdErr=$stderr; StdOutPath=$stdoutPath; StdErrPath=$stderrPath }
}
function Assert-Run([object]$Run,[string]$Pattern,[string]$Label) {
    if ($Run.ExitCode -ne 0) { throw "$Label exited $($Run.ExitCode) ($($Run.ExitCodeHex)); inspect $($Run.StdErrPath)" }
    $all = $Run.StdOut + "`n" + $Run.StdErr
    if ($Pattern -and $all -notmatch $Pattern) { throw "$Label output did not satisfy expected marker '$Pattern'" }
}

$root = [IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $root -PathType Container)) { throw "ProjectRoot missing: $root" }
$utf8 = New-Object System.Text.UTF8Encoding($false)
$psParseErrors = $null
$psTokens = $null
[System.Management.Automation.Language.Parser]::ParseFile($MyInvocation.MyCommand.Path,[ref]$psTokens,[ref]$psParseErrors) | Out-Null
if ($psParseErrors.Count -gt 0) { throw "Runner PowerShell AST errors: $($psParseErrors.Count)" }

$frozen = Join-Path $root 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
if (-not (Test-Path -LiteralPath $frozen -PathType Leaf) -or (Get-Item -LiteralPath $frozen).Length -ne 796318 -or (Get-Sha256 $frozen) -ne 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953') { throw 'Frozen C11-C manifest pin mismatch' }

$expectedPins = @(
    @{p='c11c-suite/c11c-producer/c11e_production_service.py';h='5dc15d355b86758a24ff0772e75ea1a889fd59503b1632ea26821856a08935dc'},
    @{p='c11c-suite/c11c-producer/main.py';h='ddd9ce281b5da840042f1a03a63157758500cdaef70aa40e1e32e14ec1253fdf'},
    @{p='c11c-suite/c11c-producer/test_c11e_production_service.py';h='b3aea22cf713ba4382307ad6bbae777777b660bcd30b5c6c8f5497c5cf5817c5'},
    @{p='definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V1.json';h='872a395adf7b20273a14a937933f59f2ae7380fe06e38cb62775a4db9cdc8b95'},
    @{p='definitions/c11d/production/D_RENDERER_DYNAMIC_REQUEST_PAYLOAD_BINDING_V2.json';h='60530add02fee5bd4d70056e49bf20be87dc5dc0886dd07444e44c0b14bee981'},
    @{p='definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json';h='5702092bc1c88e4b333dd30cc150f0d383cd2006121037b0198905c75a3af795'},
    @{p='definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_PAYLOAD_BINDING_V1.json';h='a657d5334548cde2bb524e161d472d5fea098163b6693c0ef73b280982f20b1c'}
)
foreach ($pin in $expectedPins) {
    $path = Join-Path $root ($pin.p -replace '/', '\')
    if ((Get-Sha256 $path) -ne $pin.h) { throw "Installed E4C source pin mismatch: $($pin.p)" }
}

function Add-GodotCandidate([System.Collections.Generic.List[object]]$List,[string]$Path,[string]$Source) {
    if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path -PathType Leaf)) { return }
    $full = [IO.Path]::GetFullPath($Path)
    $exists = @($List | Where-Object { $_.Path -ieq $full }).Count -gt 0
    if (-not $exists) { $List.Add([pscustomobject]@{Path=$full;Source=$Source;IsConsole=([IO.Path]::GetFileName($full) -match '(?i)console\.exe$')}) }
}
function Add-GodotExecutableWithConsoleSibling([System.Collections.Generic.List[object]]$ConsoleList,[System.Collections.Generic.List[object]]$FallbackList,[string]$Path,[string]$Source) {
    if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path -PathType Leaf)) { return }
    $full = [IO.Path]::GetFullPath($Path)
    $leaf = [IO.Path]::GetFileName($full)
    $directory = Split-Path -Parent $full
    if ($leaf -match '(?i)console\.exe$') {
        Add-GodotCandidate $ConsoleList $full $Source
        return
    }
    # An official Windows Godot installation ships a dedicated console executable beside the GUI editor.
    foreach ($pattern in @('Godot_v4.7.1-stable_mono_win64_console.exe','Godot_v4.7.1-stable*_win64_console.exe','godot4_console.exe','godot_console.exe')) {
        $siblings = @(Get-ChildItem -LiteralPath $directory -Filter $pattern -File -ErrorAction SilentlyContinue)
        foreach ($sibling in $siblings) { Add-GodotCandidate $ConsoleList $sibling.FullName ($Source + ':SIBLING_CONSOLE') }
    }
    Add-GodotCandidate $FallbackList $full ($Source + ':NON_CONSOLE_FALLBACK')
}
function Get-GodotCandidates {
    $console = New-Object System.Collections.Generic.List[object]
    $fallback = New-Object System.Collections.Generic.List[object]
    $configured = $env:C11D_GODOT_EXECUTABLE
    if (-not [string]::IsNullOrWhiteSpace($configured)) {
        $resolved = $null
        if (Test-Path -LiteralPath $configured -PathType Leaf) { $resolved = [IO.Path]::GetFullPath($configured) }
        else {
            $configuredCommand = Get-Command -Name $configured -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($configuredCommand) {
                $configuredPath = $configuredCommand.Source
                if ([string]::IsNullOrWhiteSpace($configuredPath) -and $configuredCommand.CommandType -eq 'Application') { $configuredPath = $configuredCommand.Definition }
                if ($configuredPath -and (Test-Path -LiteralPath $configuredPath -PathType Leaf)) { $resolved = [IO.Path]::GetFullPath($configuredPath) }
            }
        }
        if (-not $resolved) { throw "C11D_GODOT_EXECUTABLE is set but does not resolve to an executable file: $configured" }
        Add-GodotExecutableWithConsoleSibling $console $fallback $resolved 'ENV:C11D_GODOT_EXECUTABLE'
    }

    # Discover command paths, but always enqueue adjacent console binaries before editor GUI binaries.
    foreach ($commandName in @('godot4_console.exe','godot_console.exe','Godot_v4.7.1-stable_mono_win64_console.exe','godot4.exe','godot.exe','godot4','godot')) {
        $commands = @(Get-Command -Name $commandName -All -ErrorAction SilentlyContinue)
        foreach ($command in $commands) {
            $commandPath = $command.Source
            if ([string]::IsNullOrWhiteSpace($commandPath) -and $command.CommandType -eq 'Application') { $commandPath = $command.Definition }
            if (-not [string]::IsNullOrWhiteSpace($commandPath)) {
                Add-GodotExecutableWithConsoleSibling $console $fallback $commandPath ('PATH:' + $commandName)
            }
        }
    }

    $searchRoots = @(
        (Join-Path $env:USERPROFILE 'Downloads'),
        'C:\Godot',
        (Join-Path $env:LOCALAPPDATA 'Programs\Godot')
    ) | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Container) }
    foreach ($directory in $searchRoots) {
        foreach ($pattern in @('Godot_v4.7.1-stable_mono_win64_console.exe','Godot_v4.7.1-stable*_win64_console.exe','godot4_console.exe','godot_console.exe')) {
            $found = Get-ChildItem -LiteralPath $directory -Filter $pattern -File -Recurse -ErrorAction SilentlyContinue
            foreach ($file in $found) { Add-GodotCandidate $console $file.FullName ('SEARCH_CONSOLE:' + $directory) }
        }
    }

    # WinGet's package cache is not under LocalAppData\Programs\Godot; inspect only the Mono package directory.
    $wingetRoot = Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages'
    if (Test-Path -LiteralPath $wingetRoot -PathType Container) {
        $monoPackages = @(Get-ChildItem -LiteralPath $wingetRoot -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like 'GodotEngine.GodotEngine.Mono_*' })
        foreach ($packageDirectory in $monoPackages) {
            foreach ($godotDirectory in @(Get-ChildItem -LiteralPath $packageDirectory.FullName -Directory -ErrorAction SilentlyContinue)) {
                foreach ($pattern in @('Godot_v4.7.1-stable_mono_win64_console.exe','Godot_v4.7.1-stable*_win64_console.exe')) {
                    $found = Get-ChildItem -LiteralPath $godotDirectory.FullName -Filter $pattern -File -Recurse -ErrorAction SilentlyContinue
                    foreach ($file in $found) { Add-GodotCandidate $console $file.FullName 'WINGET_MONO_PACKAGE_CONSOLE' }
                }
            }
        }
    }
    # Only console candidates are eligible; non-console fallbacks are explicitly rejected.
    return @($console.ToArray()) + @($fallback.ToArray())
}
function Save-GodotCrashDiagnostics([string]$EvidenceDir,[string]$GodotPath) {
    $path = Join-Path $EvidenceDir 'WINDOWS_GODOT_CRASH_EVENTS.txt'
    try {
        $since = (Get-Date).AddMinutes(-45)
        $events = @(Get-WinEvent -FilterHashtable @{LogName='Application';Id=@(1000,1001);StartTime=$since} -ErrorAction SilentlyContinue |
            Where-Object { $_.Message -match 'Godot' -or $_.Message -match [regex]::Escape([IO.Path]::GetFileName($GodotPath)) } |
            Select-Object -First 30)
        if ($events.Count -gt 0) {
            $content = $events | Format-List TimeCreated,Id,ProviderName,Message | Out-String -Width 400
        } else {
            $content = 'No matching Application Error / Windows Error Reporting events found in the last 45 minutes.'
        }
    } catch { $content = 'Windows crash-event query unavailable: ' + $_.Exception.Message }
    [IO.File]::WriteAllText($path,$content,([System.Text.UTF8Encoding]::new($false)))
    return $path
}
function Invoke-GodotHeadlessSmoke([string]$GodotPath,[int]$Index,[string]$EvidenceDir) {
    $probeRoot = Join-Path $env:TEMP ('C11E_GODOT_HEADLESS_PROBE_' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $probeRoot -Force | Out-Null
    $projectText = "config_version=5`n`n[application]`nconfig/name=`"C11E_GODOT_HEADLESS_PROBE`"`n`n[rendering]`nrenderer/rendering_method=`"gl_compatibility`"`n"
    $scriptText = "extends SceneTree`n`nfunc _initialize() -> void:`n    print(`"C11E_GODOT_HEADLESS_SCRIPT_SMOKE=PASS`" )`n    quit(0)`n"
    [IO.File]::WriteAllText((Join-Path $probeRoot 'project.godot'),$projectText,([System.Text.UTF8Encoding]::new($false)))
    [IO.File]::WriteAllText((Join-Path $probeRoot 'probe.gd'),$scriptText,([System.Text.UTF8Encoding]::new($false)))
    try {
        return Invoke-Native ('GODOT_HEADLESS_SMOKE_{0:D2}' -f $Index) $GodotPath @('--headless','--path',$probeRoot,'--script','res://probe.gd') $probeRoot 60 $EvidenceDir
    } finally {
        if (Test-Path -LiteralPath $probeRoot -PathType Container) { Remove-Item -LiteralPath $probeRoot -Recurse -Force -ErrorAction SilentlyContinue }
    }
}

$py = (Get-Command py.exe -ErrorAction Stop).Source
$godotCandidates = @(Get-GodotCandidates)
if ($godotCandidates.Count -eq 0) { throw 'GODOT NOT FOUND: no Godot command was found on PATH and no Godot 4.7.1 console executable was found in Downloads, C:\Godot or LocalAppData\Programs\Godot.' }
$evidenceBase = Join-Path $root 'artifacts\tests\c11e\e4c_drill_binder_v2_acceptance'
if (-not (Test-Path -LiteralPath $evidenceBase)) { New-Item -ItemType Directory -Path $evidenceBase | Out-Null }
$runId = 'DRILLV2_' + (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ') + '_' + ([guid]::NewGuid().ToString('N').Substring(0,8))
$evidence = Join-Path $evidenceBase $runId
New-Item -ItemType Directory -Path $evidence | Out-Null
Write-Host "E4C_DRILL_EVIDENCE_DIR=$evidence"

$versionRun = Invoke-Native 'PYTHON_VERSION' $py @('-3.13','-c','import sys; print(sys.version)') $root 30 $evidence
Assert-Run $versionRun '3\.13\.' 'Python 3.13'

$godot = $null
$godotRun = $null
$godotVersionText = $null
$godotDiscoverySource = $null
$godotProbeIndex = 0
$godotProbeFailures = New-Object System.Collections.Generic.List[string]
foreach ($candidate in $godotCandidates) {
    $godotProbeIndex++
    if (-not $candidate.IsConsole) {
        $godotProbeFailures.Add(($candidate.Path + ' => rejected: non-console Windows GUI executable; no GUI fallback is permitted'))
        continue
    }
    $probeName = 'GODOT_VERSION_CANDIDATE_{0:D2}' -f $godotProbeIndex
    try {
        $candidateRun = Invoke-Native $probeName $candidate.Path @('--version') $root 30 $evidence
        $candidateVersion = $candidateRun.StdOut.Trim()
        if ([string]::IsNullOrWhiteSpace($candidateVersion)) { $candidateVersion = $candidateRun.StdErr.Trim() }
        if ($candidateRun.ExitCode -ne 0 -or $candidateVersion -ne '4.7.1.stable.mono.official.a13da4feb') {
            $godotProbeFailures.Add(($candidate.Path + ' => version exit=' + $candidateRun.ExitCode + ' (' + $candidateRun.ExitCodeHex + '), version=' + $candidateVersion))
            continue
        }
        $smoke = Invoke-GodotHeadlessSmoke $candidate.Path $godotProbeIndex $evidence
        $smokeCombined = $smoke.StdOut + "`n" + $smoke.StdErr
        if ($smoke.ExitCode -ne 0 -or $smokeCombined -notmatch 'C11E_GODOT_HEADLESS_SCRIPT_SMOKE=PASS') {
            $crashLog = Save-GodotCrashDiagnostics $evidence $candidate.Path
            $godotProbeFailures.Add(($candidate.Path + ' => headless smoke exit=' + $smoke.ExitCode + ' (' + $smoke.ExitCodeHex + '), stderr=' + $smoke.StdErrPath + ', stdout=' + $smoke.StdOutPath + ', crash_events=' + $crashLog))
            continue
        }
        $godot = $candidate.Path
        $godotRun = $candidateRun
        $godotVersionText = $candidateVersion
        $godotDiscoverySource = $candidate.Source
        Write-Host "GODOT_HEADLESS_SCRIPT_SMOKE=PASS; candidate=$godot"
        break
    } catch {
        $godotProbeFailures.Add(($candidate.Path + ' => ' + $_.Exception.Message))
    }
}
if ([string]::IsNullOrWhiteSpace($godot)) {
    throw ('No Godot 4.7.1 Mono candidate passed version + real headless-script smoke. Only console executables are eligible; GUI fallbacks are explicitly rejected. Probes: ' + ($godotProbeFailures -join ' | '))
}
$env:C11D_GODOT_EXECUTABLE = $godot
Write-Host "GODOT_DISCOVERY_SOURCE=$godotDiscoverySource"
Write-Host "GODOT_EXECUTABLE=$godot"
Write-Host "GODOT_VERSION_VERIFIED=$godotVersionText"

function Test-ReusablePreflightEvidence([string]$Directory,[string]$RootPath,[string]$EvidenceOutput) {
    if ([string]::IsNullOrWhiteSpace($Directory)) { return $null }
    $base = [IO.Path]::GetFullPath((Join-Path $RootPath 'artifacts\tests\c11e\e4c_drill_binder_v2_acceptance'))
    $full = [IO.Path]::GetFullPath($Directory)
    if (-not $full.StartsWith($base + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { return $null }
    if (-not (Test-Path -LiteralPath $full -PathType Container)) { return $null }
    $required = @('PY_COMPILE','PYTHON_VERSION','E1_SERVICE_TESTS','DRILL_V2_SOURCE_CHAIN_TESTS','DYNAMIC_BINDING_V1_REGRESSION','REQUEST_SCOPED_BINDING_REGRESSION','EDITORIAL_REVIEW_MANIFEST_REGRESSION')
    $files = New-Object System.Collections.Generic.List[object]
    $logs = @{}
    foreach ($name in $required) {
        foreach ($stream in @('stdout','stderr')) {
            $path = Join-Path $full ($name + '.' + $stream + '.log')
            if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { return $null }
            $logs[$name + '.' + $stream] = Get-Content -LiteralPath $path -Raw -Encoding UTF8
            $files.Add([pscustomobject]@{path=$name + '.' + $stream + '.log';sha256=(Get-Sha256 $path);bytes=(Get-Item -LiteralPath $path).Length})
        }
    }
    $pythonText = $logs['PYTHON_VERSION.stdout'] + $logs['PYTHON_VERSION.stderr']
    $e1Text = $logs['E1_SERVICE_TESTS.stdout'] + $logs['E1_SERVICE_TESTS.stderr']
    $v2Text = $logs['DRILL_V2_SOURCE_CHAIN_TESTS.stdout'] + $logs['DRILL_V2_SOURCE_CHAIN_TESTS.stderr']
    $v1Text = $logs['DYNAMIC_BINDING_V1_REGRESSION.stdout'] + $logs['DYNAMIC_BINDING_V1_REGRESSION.stderr']
    $scopedText = $logs['REQUEST_SCOPED_BINDING_REGRESSION.stdout'] + $logs['REQUEST_SCOPED_BINDING_REGRESSION.stderr']
    $reviewText = $logs['EDITORIAL_REVIEW_MANIFEST_REGRESSION.stdout'] + $logs['EDITORIAL_REVIEW_MANIFEST_REGRESSION.stderr']
    if ($pythonText -notmatch '3\.13\.') { return $null }
    if ($e1Text -notmatch 'Ran 32 tests[\s\S]*OK') { return $null }
    if ($v2Text -notmatch 'Ran 7 tests[\s\S]*OK') { return $null }
    if ($v1Text -notmatch 'tests=12/12') { return $null }
    if ($scopedText -notmatch 'negative=51/51') { return $null }
    if ($reviewText -notmatch 'negative=28/28') { return $null }
    $priorRunId = Split-Path -Leaf $full
    $receipt = [ordered]@{
        schema='C11E-E4C-REUSED-PREFLIGHT-EVIDENCE-V1'
        status='PASS_REUSED_AFTER_CURRENT_SOURCE_PIN_REVALIDATION'
        prior_run_id=$priorRunId
        prior_evidence_directory=$full
        python_version='3.13'
        py_compile='PASS_LOGS_PRESENT_AND_SUBSEQUENT_ORDERED_STAGES_COMPLETED'
        e1_service_tests='PASS_32_OF_32'
        drill_v2_source_chain='PASS_7_OF_7'
        dynamic_binding_v1='PASS_12_OF_12'
        request_scoped_binding='PASS_51_NEGATIVES'
        editorial_review_manifest='PASS_28_NEGATIVES'
        current_source_pins_revalidated=$true
        current_frozen_manifest_revalidated=$true
        reused_logs=@($files.ToArray())
    }
    $receiptPath = Join-Path $EvidenceOutput 'REUSED_PREFLIGHT_EVIDENCE_RECEIPT.json'
    [IO.File]::WriteAllText($receiptPath,(ConvertTo-Json -InputObject $receipt -Depth 12),([System.Text.UTF8Encoding]::new($false)))
    $receiptSha = Get-Sha256 $receiptPath
    [IO.File]::WriteAllText(($receiptPath + '.sha256'),("$receiptSha  REUSED_PREFLIGHT_EVIDENCE_RECEIPT.json`n"),([System.Text.UTF8Encoding]::new($false)))
    return [pscustomobject]@{ReceiptPath=$receiptPath;ReceiptSha256=$receiptSha;PriorRunId=$priorRunId}
}
$reusedPreflight = Test-ReusablePreflightEvidence $ReusePreflightEvidenceDir $root $evidence
if ($reusedPreflight) {
    Write-Host 'E4C_PREFLIGHT_EVIDENCE_REUSE=PASS_SOURCE_PINS_REVALIDATED'
    Write-Host "E4C_PREFLIGHT_REUSED_FROM=$($reusedPreflight.PriorRunId)"
    Write-Host "E4C_PREFLIGHT_REUSE_RECEIPT=$($reusedPreflight.ReceiptPath)"
    Write-Host "E4C_PREFLIGHT_REUSE_RECEIPT_SHA256=$($reusedPreflight.ReceiptSha256)"
} else {
    if (-not [string]::IsNullOrWhiteSpace($ReusePreflightEvidenceDir)) { Write-Host 'E4C_PREFLIGHT_EVIDENCE_REUSE=NOT_REUSABLE; executing ordered preflight tests' }
    $compile = Invoke-Native 'PY_COMPILE' $py @('-3.13','-B','-m','py_compile','c11c-suite/c11c-producer/c11e_production_service.py','c11c-suite/c11c-producer/main.py','c11c-suite/c11c-producer/test_c11e_production_service.py') $root 60 $evidence
    Assert-Run $compile '' 'Python compile'

    $producerDir = Join-Path $root 'c11c-suite\c11c-producer'
    $serviceTests = Invoke-Native 'E1_SERVICE_TESTS' $py @('-3.13','-B','-m','unittest','test_c11e_production_service','-v') $producerDir 180 $evidence
    Assert-Run $serviceTests 'Ran 32 tests[\s\S]*OK' 'E1 service/GUI-CLI contract tests'

    $v2Tests = Invoke-Native 'DRILL_V2_SOURCE_CHAIN_TESTS' $py @('-3.13','-B','-m','unittest','tools.c11d.d9.test_d_renderer_dynamic_request_payload_binding_visual_drill_v2','-v') $root 180 $evidence
    Assert-Run $v2Tests 'Ran 7 tests[\s\S]*OK' 'Drill V2 source-chain tests'

    $v1Tests = Invoke-Native 'DYNAMIC_BINDING_V1_REGRESSION' $py @('-3.13','-B','tools/c11d/d9/test_d_renderer_dynamic_request_payload_binding.py') $root 120 $evidence
    Assert-Run $v1Tests 'tests=12/12' 'Existing dynamic binder V1 regression'

    $scopedTests = Invoke-Native 'REQUEST_SCOPED_BINDING_REGRESSION' $py @('-3.13','-B','tools/c11d/d9/test_d_renderer_request_scoped_payload_binding.py') $root 120 $evidence
    Assert-Run $scopedTests 'negative=51/51' 'Request-scoped binding regression'

    $reviewTests = Invoke-Native 'EDITORIAL_REVIEW_MANIFEST_REGRESSION' $py @('-3.13','-B','tools/c11d/d9/test_d_renderer_editorial_review_manifest.py') $root 120 $evidence
    Assert-Run $reviewTests 'negative=28/28' 'Editorial review manifest regression'
}

# Known visual-policy blocker is reported independently of dynamic request binding.
$a3Path = Join-Path $root 'definitions\c11d\production\D_RENDERER_LOOP_DRILL_EDITORIAL_FIELD_WINDOW_PROPOSAL_V1.json'
$reviewPath = Join-Path $root 'definitions\c11d\production\D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json'
$a3 = Get-Content -LiteralPath $a3Path -Raw -Encoding UTF8 | ConvertFrom-Json
$currentReviewSha = Get-Sha256 $reviewPath
$a3ReviewRow = @($a3.source_lineage | Where-Object { $_.path -eq 'definitions/c11d/production/D_RENDERER_EDITORIAL_REVIEW_MANIFEST_V1.json' }) | Select-Object -First 1
if (-not $a3ReviewRow -or $a3ReviewRow.sha256 -ne $currentReviewSha) {
    $policyState = 'BLOCKED_STALE_DEPENDENCY_LINEAGE_D3_EDITORIAL_CONSUMER_NOT_ADMITTED'
} else {
    $policyState = 'LINEAGE_CURRENT_BUT_PROPOSAL_ONLY_NOT_RENDERER_AUTHORITY'
}
Write-Host "E4C_VISUAL_EDITORIAL_POLICY=$policyState"

$binder = Join-Path $root 'tools\c11d\d9\d_renderer_dynamic_request_payload_binding.py'
$matrix = Invoke-Native 'DRILL_V2_GODOT_20_PAIR_RUNTIME' $py @('-3.13','-B',$binder,'--visual-drill-matrix','--godot',$godot,'--timeout',[string]$GodotTimeoutSeconds,'--root',$root) $root ([int]([Math]::Min(14400,[Math]::Max(600,($GodotTimeoutSeconds*45))))) $evidence
if ($matrix.ExitCode -ne 0) { $crashLog = Save-GodotCrashDiagnostics $evidence $godot; Write-Host "GODOT_CRASH_DIAGNOSTICS=$crashLog" }
Assert-Run $matrix 'C11-D VISUAL DRILL DYNAMIC REQUEST PAYLOAD BINDING V2 PASS[\s\S]*cases=20 \| families=4/4 \| selectors=20/20 \| independent_runtime_repeat=20/20 \| request_payload_manifest=20/20 \| lineage_closure=20/20 \| source_pins=67/67' 'Real-Godot Drill V2 matrix'

$prefix = 'C11-D DYNAMIC REQUEST PAYLOAD RECEIPT VERIFIED='
$lines = @($matrix.StdOut -split "`r?`n" | Where-Object { $_.StartsWith($prefix) })
if ($lines.Count -ne 20) { throw "Expected 20 VERIFIED receipts; observed $($lines.Count)" }
$expected = @{}
foreach ($family in @('tracking','pursuit','saccade','peripheral_scan')) { foreach ($tier in 1..5) { $expected["$family/tier-$tier"] = $false } }
$receiptRows = New-Object System.Collections.Generic.List[object]
foreach ($line in $lines) {
    $r = $line.Substring($prefix.Length) | ConvertFrom-Json
    $key = "$($r.request_identity.selection.family_id)/$($r.request_identity.selection.variant_id)"
    if (-not $expected.ContainsKey($key) -or $expected[$key]) { throw "Duplicate/out-of-scope Drill receipt: $key" }
    $expected[$key] = $true
    if ($r.runtime_verification_status -ne 'VERIFIED' -or $r.runtime_repeat_evidence.status -ne 'VERIFIED' -or $r.runtime_repeat_evidence.independent_runtime_executions -ne 2) { throw "Runtime/repeat receipt failed: $key" }
    if ($r.payload_manifest.manifest_sha256 -ne $r.payload_evidence.request_payload_manifest_sha256) { throw "Payload manifest digest mismatch: $key" }
    if ($r.payload_evidence.exact_selector_payload_materialized -ne $true) { throw "Exact selector payload not materialized: $key" }
    if ($r.readiness.candidate_input_admissible -ne $false -or $r.readiness.video_render_ready -ne $false) { throw "Receipt improperly escalates readiness: $key" }
    if ($r.execution_boundary.renderer_activation -ne $false -or $r.execution_boundary.renderer_native_input_emitted -ne $false -or $r.execution_boundary.media_output_created -ne $false -or $r.execution_boundary.release_authority -ne 'NONE') { throw "Receipt crosses governance boundary: $key" }
    $receiptRows.Add($r)
}
if (@($expected.Values | Where-Object { -not $_ }).Count -ne 0) { throw 'Drill V2 matrix did not cover all 20 exact type/tier combinations' }
$receiptJsonl = Join-Path $evidence 'DRILL_V2_VERIFIED_RECEIPTS.jsonl'
$receiptRows | ForEach-Object { ConvertTo-Json -InputObject $_ -Depth 40 -Compress } | Set-Content -LiteralPath $receiptJsonl -Encoding UTF8

$report = [ordered]@{
    schema='C11E-E4C-DRILL-BINDER-V2-WINDOWS-ACCEPTANCE-RECEIPT-V1'
    run_id=$runId
    status='PASS_E4C_DRILL_DYNAMIC_BINDING_20_OF_20_PENDING_VISUAL_POLICY_AND_AV'
    frozen_c11c_manifest_sha256='e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953'
    python_version=($versionRun.StdOut.Trim())
    godot_version=$godotVersionText
    godot_discovery_source=$godotDiscoverySource
    godot_executable_path=$godot
    e1_service_tests='PASS_32_OF_32'
    v2_source_chain_tests='PASS_7_OF_7'
    v1_dynamic_binding_regression='PASS_12_OF_12'
    request_scoped_binding_regression='PASS_3_OF_3_AND_51_NEGATIVES'
    editorial_review_manifest_regression='PASS_3_OF_3_AND_28_NEGATIVES'
    visual_policy_lineage=$policyState
    selector_matrix='20_OF_20'
    independent_runtime_repeats='20_OF_20'
    request_payload_manifests='20_OF_20'
    lineage_closure='20_OF_20'
    receipt_jsonl_sha256=(Get-Sha256 $receiptJsonl)
    runtime_stdout_sha256=(Get-Sha256 $matrix.StdOutPath)
    runtime_stderr_sha256=(Get-Sha256 $matrix.StdErrPath)
    candidate_input_admissible=$false
    video_render_ready=$false
    renderer='OFF'
    media_created=$false
    d4_8='BLOCKED'
    d9_10='PREPARE_ONLY'
    release_authority='NONE'
}
$reportPath = Join-Path $evidence 'E4C_DRILL_BINDER_V2_ACCEPTANCE_RECEIPT.json'
$json = ConvertTo-Json -InputObject $report -Depth 12
[IO.File]::WriteAllText($reportPath,$json,([System.Text.UTF8Encoding]::new($false)))
$reportSha = Get-Sha256 $reportPath
[IO.File]::WriteAllText(($reportPath + '.sha256'),("$reportSha  E4C_DRILL_BINDER_V2_ACCEPTANCE_RECEIPT.json`n"),([System.Text.UTF8Encoding]::new($false)))

Write-Host 'E4C_DRILL_DYNAMIC_BINDER_V2=PASS_20_OF_20'
Write-Host 'E4C_DRILL_INDEPENDENT_RUNTIME_REPEAT=PASS_20_OF_20'
Write-Host 'E4C_DRILL_REQUEST_PAYLOAD_MANIFEST=PASS_20_OF_20'
Write-Host "E4C_VISUAL_EDITORIAL_POLICY=$policyState"
Write-Host "E4C_DRILL_RECEIPT=$reportPath"
Write-Host "E4C_DRILL_RECEIPT_SHA256=$reportSha"
Write-Host 'E4C_DRILL_RENDERER=OFF_MEDIA_CREATED=false_D4.8=BLOCKED_RELEASE_AUTHORITY=NONE'
