$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
$fail = $false

$checks = @(
    @{ Name = "PresentationFramer exists"; Path = "$root\core\presentation\PresentationFramer.gd" },
    @{ Name = "Generador imports PresentationFramer"; Path = "$root\GeneradorMaestro.gd" },
    @{ Name = "Gate accepts framing policy"; Path = "$root\core\presentation\WinningFrameVisibilityGate.gd" },
    @{ Name = "QA framing metadata tool exists"; Path = "$root\tools\qa\c11\apply_c11b02_qa_framing_policy.ps1" }
)
foreach ($c in $checks) {
    if (-not (Test-Path -LiteralPath $c.Path)) {
        Write-Host "FAIL: $($c.Name)" -ForegroundColor Red
        $fail = $true
    } else {
        Write-Host "PASS: $($c.Name)"
    }
}

$text = Get-Content -LiteralPath "$root\GeneradorMaestro.gd" -Raw
foreach ($needle in @('initialize_presentation_framing\(\)', 'framing_policy', 'presentation_frame_offset', 'c11b_visibility_audit_requested = has_user_flag\(')) {
    if ($text -notmatch $needle) {
        Write-Host "FAIL: Generador missing $needle" -ForegroundColor Red
        $fail = $true
    }
}

$initIndex = $text.IndexOf("setup_presentation_bindings()")
$assetIndex = $text.IndexOf("FamilyAssets.configure_presentation(")
$auditIndex = $text.IndexOf("if c11b_visibility_audit_requested:")
if ($assetIndex -ge 0 -and $auditIndex -gt $assetIndex) {
    Write-Host "PASS: C11B audit deferred until presentation state is initialized" -ForegroundColor Green
} else {
    Write-Host "FAIL: C11B audit deferral ordering missing" -ForegroundColor Red
    $fail = $true
}

if ($fail) {
    Write-Host "[C11B02_INSTALLATION] FAIL" -ForegroundColor Red
    exit 1
}
Write-Host "[C11B02_INSTALLATION] PASS" -ForegroundColor Green
