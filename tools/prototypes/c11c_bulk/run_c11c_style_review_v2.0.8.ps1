param(
    [Parameter(Mandatory=$true)]
    [int[]]$Seeds,
    [switch]$KeepExistingReviewAssets,
    [switch]$ResetReviewAssets
)
$ErrorActionPreference='Stop'
$canonical=Join-Path $PSScriptRoot 'run_c11c_style_review_v2.1.0.ps1'
$args=@{ Seeds=$Seeds }
if ($KeepExistingReviewAssets) { $args['KeepExistingReviewAssets']=$true }
if ($ResetReviewAssets) { $args['ResetReviewAssets']=$true }
& $canonical @args
if (-not $?) { throw 'C11-C style review failed.' }
return
