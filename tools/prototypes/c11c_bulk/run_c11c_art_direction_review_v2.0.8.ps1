param(
    [int[]]$Seeds = @(),
    [int]$VariationsPerFamily = 5,
    [switch]$ResetReviewAssets
)
$ErrorActionPreference = 'Stop'
$canonical = Join-Path $PSScriptRoot 'run_c11c_art_direction_review_v2.1.0.ps1'
$args = @{ VariationsPerFamily = $VariationsPerFamily }
if ($PSBoundParameters.ContainsKey('Seeds')) { $args['Seeds'] = $Seeds }
if ($ResetReviewAssets) { $args['ResetReviewAssets'] = $true }
& $canonical @args
if (-not $?) { throw 'C11-C art-direction review failed.' }
return
