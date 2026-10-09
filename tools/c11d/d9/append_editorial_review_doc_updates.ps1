$ErrorActionPreference = 'Stop'
$repoRoot = (Get-Location).Path

$updates = @(
    [pscustomobject]@{
        Path = 'docs/current/d/D_RENDERER_BASELINE_PREPARATION_PLAN_V1.md'
        Marker = '<!-- C11D_EDITORIAL_REVIEW_MANIFEST_V1_PLAN -->'
        Section = @'
<!-- C11D_EDITORIAL_REVIEW_MANIFEST_V1_PLAN -->

## D9.9→D9.10 editorial review manifest — preparation update (2026-10-10)

`tools/c11d/d9/d_renderer_editorial_review_manifest.py` joins the canonical request/plan, D9.10 bridge, PREPARE_ONLY adapter envelope, binding preview, logical composition, frame program and temporal reference into a deterministic in-memory review manifest. The focused test covers challenges, Visual Loops and Visual Drills with strict schema and negative validation.

Open integration findings are explicit: CHALLENGE_004 timing is 60 FPS while REVIEW_720 is 30 FPS and requires a separate normalization policy; Visual Loop timing is family-level, Visual Drill timing is type/tier-level, and per-field text visibility frame windows are not defined. Do not infer missing bindings or enable renderer execution to hide these gaps.

This contract is review-only: `video_render_ready=false`, renderer OFF, media not created, D4.8 BLOCKED and release authority NONE. Baseline freeze remains blocked until all D acceptance and governance gates are met.
'@
    },
    [pscustomobject]@{
        Path = 'docs/current/d/D9_SUITE_INTEGRATION_CHANGELOG.md'
        Marker = '<!-- C11D_EDITORIAL_REVIEW_MANIFEST_V1_CHANGELOG -->'
        Section = @'
<!-- C11D_EDITORIAL_REVIEW_MANIFEST_V1_CHANGELOG -->

## 2026-10-10 — D9.9→D9.10 editorial review manifest V1

Added a non-renderable cross-contract audit manifest and focused test. It pins 25 upstream sources, checks exact editorial text/hash continuity, identifies challenge source/delivery FPS mismatch, and retains explicit gaps for Visual Loop grammar payload, Visual Drill request payload and per-field frame windows. No production, dispatch, media output, D4.8 authorization or release authority is enabled.
'@
    },
    [pscustomobject]@{
        Path = 'docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md'
        Marker = '<!-- C11D_EDITORIAL_REVIEW_MANIFEST_V1_HANDOVER -->'
        Section = @'
<!-- C11D_EDITORIAL_REVIEW_MANIFEST_V1_HANDOVER -->

## Latest D9 editorial-review increment (2026-10-10)

The editorial review manifest now audits the canonical D9.9→D9.10 chain against the temporal reference. Current focused test expected result: 3/3 content types, 3/3 determinism, 3/3 editorial chain, 3/3 temporal reference, 28/28 negative cases, 3/3 structural schema checks and 3/3 Draft 2020-12 schema checks when `jsonschema` is installed.

Known unresolved issues that must remain visible: CHALLENGE_004 source FPS 60 vs REVIEW_720 target FPS 30; Visual Loop family-level and Drill type/tier-level timing references do not yet bind the generated visual payload; editorial-field frame windows remain undefined. This manifest permits copy review only. It does not make a video render-ready.

Governance remains unchanged: C11-C frozen and immutable; renderer OFF; media_created=false; D4.8 BLOCKED; release authority NONE; D baseline approval/freeze and full acceptance still pending.
'@
    },
    [pscustomobject]@{
        Path = 'docs/current/d/START_PROMPT_C11D_CURRENT.md'
        Marker = '<!-- C11D_EDITORIAL_REVIEW_MANIFEST_V1_START_PROMPT -->'
        Section = @'
<!-- C11D_EDITORIAL_REVIEW_MANIFEST_V1_START_PROMPT -->

## Current context addendum — editorial review manifest V1 (2026-10-10)

Before advancing temporal/render integration, run `python .\tools\c11d\d9\test_d_renderer_editorial_review_manifest.py`. It verifies exact canonical copy and temporal-source lineage, while preserving `video_render_ready=false`. Review the reported source/delivery FPS mismatch for challenges and the unbound Visual Loop/Drill instances and text-field frame windows; do not silently normalize, invent timing, or activate rendering. Repeat the candidate preflight and aggregate regression on the operator checkout after each overlay.
'@
    }
)

# Validate every destination and marker before making any changes.
foreach ($item in $updates) {
    $full = Join-Path $repoRoot $item.Path
    if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
        throw "Required handover document is missing; no files modified: $($item.Path)"
    }
    $content = [System.IO.File]::ReadAllText($full, [System.Text.Encoding]::UTF8)
    $count = ([regex]::Matches($content, [regex]::Escape($item.Marker))).Count
    if ($count -gt 1) {
        throw "Duplicate update marker; no files modified: $($item.Path)"
    }
}

$encoding = [System.Text.UTF8Encoding]::new($false)
$added = 0
$skipped = 0
foreach ($item in $updates) {
    $full = Join-Path $repoRoot $item.Path
    $content = [System.IO.File]::ReadAllText($full, [System.Text.Encoding]::UTF8)
    if ($content.Contains($item.Marker)) {
        $skipped++
        continue
    }
    [System.IO.File]::AppendAllText($full, [Environment]::NewLine + [Environment]::NewLine + $item.Section.Trim() + [Environment]::NewLine, $encoding)
    $added++
}
Write-Output "C11-D editorial review docs update PASS | added=$added | already_present=$skipped | targets=$($updates.Count) | overwrite=FALSE"
