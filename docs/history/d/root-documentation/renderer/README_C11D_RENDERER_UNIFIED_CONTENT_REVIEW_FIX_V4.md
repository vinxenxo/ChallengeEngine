# C11-D Unified Content Review Fix V4 — complete runtime source lineage

Minimal overlay for `ChallengeEngineV01_STATELESS`. Fixes the runtime summary lineage emitted by the Challenge visual-payload and coordinate-projection review harnesses. It does not change simulation inputs, simulation output, frame selection, projection math, renderer state, or governance.

## Root cause

The unified coordinator correctly expects each review summary to identify the contract that governs that summary. Both Godot harnesses checked their contracts but omitted their own contract file from the emitted `source_lineage` array. The coordinate harness already reported the Challenge visual-payload contract, but omitted its own coordinate-projection contract as well. Therefore the Python join failed despite the files being correctly pinned and checked on disk.

A contract cannot safely embed its own SHA-256 inside itself. The harnesses now hash their own contract bytes at runtime and append that path/hash to the summary lineage, then sort the lineage canonically. The coordinator compares those values to its independently pinned expected hashes.

## Apply

Run from the repository root:

```powershell
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_RENDERER_UNIFIED_CONTENT_REVIEW_FIX_V4.zip" `
  -DestinationPath "." `
  -Force
```

## Validate

```powershell
python .\tools\c11d\d9\test_d_renderer_unified_content_review.py
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
```

Do not run the documentation appenders until the unified review reports PASS. Expected gate state remains unchanged: `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`. This overlay does not authorize video creation.
