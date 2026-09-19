param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

$OutputRoot = Join-Path $ProjectRoot 'output'

# Frozen evidence / canonical paths that this cleanup NEVER touches.
$ProtectedPaths = @(
    (Join-Path $ProjectRoot 'output/c10c_e2e'),
    (Join-Path $ProjectRoot 'output_batch_audit'),
    (Join-Path $ProjectRoot 'output_c7'),
    (Join-Path $ProjectRoot 'export')
)

# Known generated/stale C10-era output only.
$Candidates = New-Object System.Collections.Generic.List[string]

if (Test-Path -LiteralPath $OutputRoot) {
    foreach ($item in @(Get-ChildItem -LiteralPath $OutputRoot -Force)) {
        $name = $item.Name
        $isCandidate = $false

        if ($name -eq 'BATCH_MANIFEST.json') { $isCandidate = $true }
        elseif ($name -match '^CHALLENGE_(?:00[1-9]|VIDEO_OFF_001)$') { $isCandidate = $true }
        elseif ($name -match '^[a-z_]+_demo\.avi$') { $isCandidate = $true }
        elseif ($name -eq 'c11a_visual_qa') { $isCandidate = $true }

        if ($isCandidate) {
            [void]$Candidates.Add($item.FullName)
        }
    }
}

Write-Host '==================================================='
Write-Host '[CLEAN-C10] Generated-output cleanup'
Write-Host '==================================================='
Write-Host "Project: $ProjectRoot"
Write-Host "Targets found: $($Candidates.Count)"
Write-Host ''

if ($Candidates.Count -eq 0) {
    Write-Host '[CLEAN-C10] Nothing to remove.'
    exit 0
}

foreach ($path in $Candidates) {
    Write-Host "  REMOVE: $path"
}

Write-Host ''
Write-Host 'PRESERVED:'
foreach ($path in $ProtectedPaths) {
    if (Test-Path -LiteralPath $path) {
        Write-Host "  KEEP:   $path"
    }
}

if (-not $Apply) {
    Write-Host ''
    Write-Host '[CLEAN-C10] DRY RUN only. No files were deleted.' -ForegroundColor Yellow
    Write-Host '[CLEAN-C10] To apply: .\tools\clean_c10_generated_outputs.ps1 -Apply'
    exit 0
}

Write-Host ''
Write-Host '[CLEAN-C10] Applying cleanup...' -ForegroundColor Yellow
foreach ($path in $Candidates) {
    if (Test-Path -LiteralPath $path) {
        Remove-Item -LiteralPath $path -Recurse -Force
    }
}

Write-Host '[CLEAN-C10] PASS - obsolete generated output removed.' -ForegroundColor Green
exit 0
