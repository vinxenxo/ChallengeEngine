[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$readme = Join-Path (Get-Location) 'README.md'
$marker = '<!-- C11_FREEZE_STATUS_START -->'
$endMarker = '<!-- C11_FREEZE_STATUS_END -->'
$section = @"
$marker

## C11 FREEZE — Current Status

**C11 is CLOSED / CERTIFIED / FROZEN.**

The C11 cycle unified challenge and visual presentation around a common 540x960 social structure:

- Header: 0..144
- Body: 144..816
- Footer: 816..960

The deterministic simulation boundary is unchanged. Presentation maps and renders existing truth; it does not calculate mechanics, winning frames or RNG outcomes.

Freeze evidence includes the 103/103 logical corpus, 54/54 retrocompatibility, 576 stress executions, 2/2 physical smoke exports and 54/54 QA video renders. The C7-A2 mixed-audio rule remains authoritative and is intentionally outside the video-only QA matrix.

The next active scope is **C11-C Art Direction**, restricted to presentation and visual assets.

$endMarker
"@

$current = if (Test-Path -LiteralPath $readme) { Get-Content -Raw -LiteralPath $readme } else { '# ChallengeEngineV01_STATELESS`n' }
$pattern = [regex]::Escape($marker) + '(?s:.*?)' + [regex]::Escape($endMarker)
if ($current -match $pattern) {
    $current = [regex]::Replace($current,$pattern,$section.Trim())
} else {
    $current = $section.Trim() + "`n`n" + $current.TrimStart()
}
Set-Content -LiteralPath $readme -Value $current -Encoding UTF8
Write-Host '[C11FREEZE] README updated'
