$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=(Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$required=@(
 'core\presentation\C11CVisualEditorialLayer.gd',
 'core\presentation\VisualDrillPresentationBinder.gd',
 'core\presentation\PresentationUI.gd',
 'core\presentation\rendering\VisualContentPlayer.gd',
 'tests\C11CVisualDrillSocialPresentationContractTest.gd',
 'tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1'
)
$missing=@($required | Where-Object { -not (Test-Path -LiteralPath (Join-Path $ProjectRoot $_)) })
if($missing.Count -gt 0){ throw ('Missing C11-C Visual Drill presentation overlay files: ' + ($missing -join ', ')) }
Write-Host '[C11-C-DRILL] Overlay file presence: PASS'
