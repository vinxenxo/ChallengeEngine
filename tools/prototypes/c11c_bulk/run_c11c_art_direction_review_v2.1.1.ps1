param(
    [int[]]$Seeds = @(),
    [ValidateRange(1,50)][int]$VariationsPerFamily = 5,
    [switch]$ResetReviewAssets
)
$target = Join-Path $PSScriptRoot 'run_c11c_art_direction_review.ps1'
$args = @{}
if ($PSBoundParameters.ContainsKey('Seeds')) { $args.Seeds = $Seeds }
$args.VariationsPerFamily = $VariationsPerFamily
if ($ResetReviewAssets) { $args.ResetReviewAssets = $true }
& $target @args
if (-not $?) { throw 'Canonical art-direction review launcher failed.' }
return
