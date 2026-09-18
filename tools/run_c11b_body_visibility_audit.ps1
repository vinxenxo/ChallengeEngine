[CmdletBinding()]
param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$InputRoot = "qa/c11a1_challenge_qa",
    [string]$OutputRoot = "qa/c11b_visibility_qa"
)

$ErrorActionPreference = 'Stop'
$ProjectRoot = [IO.Path]::GetFullPath($ProjectRoot)
if (-not [IO.Path]::IsPathRooted($InputRoot))  { $InputRoot = Join-Path $ProjectRoot $InputRoot }
if (-not [IO.Path]::IsPathRooted($OutputRoot)) { $OutputRoot = Join-Path $ProjectRoot $OutputRoot }
$InputRoot = [IO.Path]::GetFullPath($InputRoot)
$OutputRoot = [IO.Path]::GetFullPath($OutputRoot)

$manifest = Join-Path $InputRoot 'C11A1_CHALLENGE_BULK_MANIFEST.json'
$runsRoot = Join-Path $InputRoot 'runs'
if (-not (Test-Path -LiteralPath $manifest -PathType Leaf)) { throw "C11B.0: falta $manifest" }
if (-not (Test-Path -LiteralPath $runsRoot -PathType Container)) { throw "C11B.0: falta $runsRoot" }
if ($null -eq (Get-Command godot -ErrorAction SilentlyContinue)) { throw 'C11B.0: godot no está en PATH.' }

New-Item -ItemType Directory -Force -Path (Join-Path $OutputRoot 'runs') | Out-Null

$sourceManifest = Get-Content -LiteralPath $manifest -Raw -Encoding UTF8 | ConvertFrom-Json
# C11-A.1 canonical manifest stores executions[]. Keep items[] as a compatibility fallback.
$items = if ($null -ne $sourceManifest.executions) { @($sourceManifest.executions) } elseif ($null -ne $sourceManifest.items) { @($sourceManifest.items) } else { @() }
if ($items.Count -ne 54) { throw "C11B.0: manifest C11A1 contiene $($items.Count) ejecuciones; se esperaban 54." }

function Invoke-CapturedProcess {
    param([string]$ConfigPath, [string]$StdoutPath, [string]$StderrPath)
    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = 'godot'
    $psi.WorkingDirectory = $ProjectRoot
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $arguments = @('--headless','--path',$ProjectRoot,'--',"--config=$ConfigPath",'--validate-only','--c11b-visibility-audit')
    if ($null -ne $psi.ArgumentList) {
        foreach ($arg in $arguments) {
            [void]$psi.ArgumentList.Add($arg)
        }
    } else {
        $psi.Arguments = ($arguments | ForEach-Object { '"' + ($_ -replace '"', '\"') + '"' }) -join ' '
    }
    $p = [Diagnostics.Process]::new()
    $p.StartInfo = $psi
    [void]$p.Start()
    $outTask = $p.StandardOutput.ReadToEndAsync()
    $errTask = $p.StandardError.ReadToEndAsync()
    $p.WaitForExit()
    $stdout = $outTask.Result
    $stderr = $errTask.Result
    [IO.File]::WriteAllText($StdoutPath,$stdout,[Text.UTF8Encoding]::new($false))
    [IO.File]::WriteAllText($StderrPath,$stderr,[Text.UTF8Encoding]::new($false))
    return [pscustomobject]@{ ExitCode=$p.ExitCode; Stdout=$stdout; Stderr=$stderr }
}

Write-Host '[C11B0] Unified Social Frame — winning-frame visibility audit' -ForegroundColor Cyan
Write-Host "[C11B0] Input:  $InputRoot"
Write-Host "[C11B0] Output: $OutputRoot"
Write-Host '[C11B0] No rendering and no simulation modification; uses existing challenge runtime.'

$results = @()
$index = 0
foreach ($item in ($items | Sort-Object run_id)) {
    $index++
    $runDir = Join-Path $runsRoot $item.run_id
    $config = Join-Path $runDir 'challenge_definition.json'
    if (-not (Test-Path -LiteralPath $config -PathType Leaf)) { throw "C11B0: falta config $config" }
    $outDir = Join-Path (Join-Path $OutputRoot 'runs') $item.run_id
    New-Item -ItemType Directory -Force -Path $outDir | Out-Null
    $stdoutPath = Join-Path $outDir 'stdout.txt'
    $stderrPath = Join-Path $outDir 'stderr.txt'

    Write-Host ("[{0}/54] AUDIT {1}" -f $index,$item.run_id)
    $proc = Invoke-CapturedProcess -ConfigPath $config -StdoutPath $stdoutPath -StderrPath $stderrPath
    $matches = [regex]::Matches($proc.Stdout,'(?m)^\[C11B_VISIBILITY_JSON\](.+)$')
    if ($matches.Count -eq 0) {
        $results += [pscustomobject]@{ run_id=$item.run_id; pass=$false; exit_code=$proc.ExitCode; error='missing C11B_VISIBILITY_JSON' }
        continue
    }
    $payload = $matches[$matches.Count-1].Groups[1].Value | ConvertFrom-Json
    $results += [pscustomobject]@{
        run_id = $item.run_id
        challenge_id = $payload.challenge_id
        pass = [bool]$payload.pass
        exit_code = $proc.ExitCode
        winning_frame_game = [int]$payload.winning_frame_game
        winning_frame = [int]$payload.winning_frame
        body_rect = $payload.body_rect
        errors = $payload.errors
        entities = $payload.entities
    }
}

$failures = @($results | Where-Object { -not $_.pass })
$manifestOut = [pscustomobject]@{
    schema_version = '1.0'
    checkpoint = 'C11-B.0'
    purpose = 'Unified Social Frame winning-frame visibility gate'
    source_manifest = 'qa/c11a1_challenge_qa/C11A1_CHALLENGE_BULK_MANIFEST.json'
    body_region = [pscustomobject]@{ x=0; y=144; width=540; height=672 }
    technical_runs = $results.Count
    visibility_pass_count = @($results | Where-Object { $_.pass }).Count
    visibility_fail_count = $failures.Count
    overall_pass = ($results.Count -eq 54 -and $failures.Count -eq 0)
    runs = $results
}

$outManifest = Join-Path $OutputRoot 'C11B0_BODY_VISIBILITY_MANIFEST.json'
$manifestOut | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $outManifest -Encoding UTF8

if ($failures.Count -gt 0) {
    Write-Host "[C11B0] VISIBILITY NO-GO — $($failures.Count) run(s) failed." -ForegroundColor Red
    $failures | ForEach-Object { Write-Host (" - {0}: {1}" -f $_.run_id, ($_.errors -join '; ')) -ForegroundColor Red }
    exit 1
}

Write-Host '[C11B0] VISIBILITY PASS — 54/54 winning frames enclosed by BodyRegion.' -ForegroundColor Green
Write-Host "[C11B0] Manifest: $outManifest"
exit 0
