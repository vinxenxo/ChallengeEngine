[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$script = Join-Path $PSScriptRoot 'artifact_lifecycle_quarantine_rules.py'

function Get-InputFingerprint([string]$FullPath) {
    if (-not (Test-Path -LiteralPath $FullPath)) { return @('__MISSING__') }
    if ((Get-Item -LiteralPath $FullPath).PSIsContainer) {
        $files = @(Get-ChildItem -LiteralPath $FullPath -Recurse -File | Sort-Object -Property FullName)
        return @($files | ForEach-Object {
            $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            $_.FullName + '|' + $hash
        })
    }
    $hash = (Get-FileHash -LiteralPath $FullPath -Algorithm SHA256).Hash.ToLowerInvariant()
    return @($FullPath + '|' + $hash)
}

if (-not (Test-Path -LiteralPath $script -PathType Leaf)) {
    throw "D5.4 validator not found: $script"
}

$before = @{}
foreach ($path in @(
    'definitions/c11d/artifacts/C11D_ARTIFACT_LIFECYCLE_POLICY_V1.json',
    'artifacts/tests/c11d_d5/d5_0',
    'artifacts/tests/c11d_d5/d5_1',
    'artifacts/tests/c11d_d5/d5_2',
    'artifacts/tests/c11d_d5/d5_3'
)) {
    $full = Join-Path $root $path
    if (Test-Path -LiteralPath $full) {
        $before[$path] = @(Get-InputFingerprint $full)
    }
}

Push-Location $root
try {
    $output = & python.exe $script 2>&1
    $exitCode = $LASTEXITCODE
    $output | ForEach-Object { Write-Host $_ }
}
finally {
    Pop-Location
}

if ($exitCode -ne 0) {
    throw "D5.4 validator failed with exit code $exitCode"
}

# Verify D5.4 itself did not mutate any input tree.
$mutated = $false
foreach ($key in $before.Keys) {
    $full = Join-Path $root $key
    $after = @(Get-InputFingerprint $full)
    if ([string]::Join("`n", [string[]]$before[$key]) -ne [string]::Join("`n", [string[]]$after)) {
        $mutated = $true
        Write-Error "Input tree changed during D5.4: $key"
    }
}

if ($mutated) {
    throw 'D5.4 filesystem mutation guard FAILED.'
}

Write-Host 'D5.4 runner mutation guard: PASS'
