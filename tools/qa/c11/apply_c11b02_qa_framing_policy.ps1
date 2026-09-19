[CmdletBinding()]
param(
    [string]$InputRoot = "artifacts/qa/c11a1_challenge",
    [string]$ChallengeId = "CHALLENGE_001",
    [string]$Policy = "PRIMARY_FOCUS"
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
if (-not [IO.Path]::IsPathRooted($InputRoot)) { $InputRoot = Join-Path $root $InputRoot }
$InputRoot = [IO.Path]::GetFullPath($InputRoot)
$runsRoot = Join-Path $InputRoot 'runs'
if (-not (Test-Path -LiteralPath $runsRoot -PathType Container)) { throw "C11B0: falta $runsRoot" }

$count = 0
foreach ($file in Get-ChildItem -LiteralPath $runsRoot -Recurse -Filter 'challenge_definition.json' -File) {
    $json = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
    if ([string]$json.challenge_id -ne $ChallengeId) { continue }

    if ($null -eq $json.presentation) {
        $json | Add-Member -MemberType NoteProperty -Name presentation -Value ([pscustomobject]@{})
    }
    $existing = @($json.presentation.PSObject.Properties.Name)
    if ($existing -contains 'framing_policy') {
        $json.presentation.framing_policy = $Policy
    } else {
        $json.presentation | Add-Member -MemberType NoteProperty -Name framing_policy -Value $Policy
    }

    $json | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $file.FullName -Encoding UTF8
    $count++
}

if ($count -ne 6) { throw "C11B0: se actualizaron $count configs para $ChallengeId; se esperaban 6." }
Write-Host "[C11B0.2] QA framing metadata applied: $count run configs -> $Policy" -ForegroundColor Green
