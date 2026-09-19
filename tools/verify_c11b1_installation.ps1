$ErrorActionPreference = "Stop"
$checks = @(
    @{ Name = "UnifiedSocialFrame exposes UI mount points"; Pass = (Test-Path ".\core\presentation\UnifiedSocialFrame.tscn" -PathType Leaf) -and ((Get-Content ".\core\presentation\UnifiedSocialFrame.tscn" -Raw) -match "HeaderContent") -and ((Get-Content ".\core\presentation\UnifiedSocialFrame.tscn" -Raw) -match "BodyContentRoot") -and ((Get-Content ".\core\presentation\UnifiedSocialFrame.tscn" -Raw) -match "FooterContent") },
    @{ Name = "PresentationUI supports UnifiedSocialFrame"; Pass = ((Get-Content ".\core\presentation\PresentationUI.gd" -Raw) -match "_build_unified_frame_ui") },
    @{ Name = "SocialUIBinder exists"; Pass = (Test-Path ".\core\presentation\SocialUIBinder.gd" -PathType Leaf) },
    @{ Name = "Main.tscn integrates UnifiedSocialFrame"; Pass = ((Get-Content ".\Main.tscn" -Raw) -match "UnifiedSocialFrame") },
    @{ Name = "VisualContentPlayer.tscn integrates UnifiedSocialFrame"; Pass = ((Get-Content ".\core\presentation\rendering\VisualContentPlayer.tscn" -Raw) -match "UnifiedSocialFrame") },
    @{ Name = "B1 contract test exists"; Pass = (Test-Path ".\tests\C11B1SocialUIIntegrationContractTest.gd" -PathType Leaf) }
)
$failed = 0
foreach ($check in $checks) { if ($check.Pass) { Write-Host "PASS: $($check.Name)" } else { Write-Host "FAIL: $($check.Name)" -ForegroundColor Red; $failed++ } }
if ($failed -gt 0) { Write-Host "[C11B1_INSTALLATION] FAIL failures=$failed" -ForegroundColor Red; exit 1 }
Write-Host "[C11B1_INSTALLATION] PASS"
