# C11-D Challenge Visual Payload Semantic Binding Proposal V1 — Add-only overlay

## Scope
This overlay adds a source-derived semantic-binding proposal for the nine Challenge mechanics after the accepted V2-A static capability matrix. It contains a strict contract/schema, a read-only Python auditor, 20 unit tests, and continuity documents. It does **not** implement a Godot materializer or approve visual projections.

## Provenance
- Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`
- V2-A capability contract SHA-256: `3b4375957da12d16a6c7f652c1ba2536ce1a819b781b68b15e5dd3f0ee4bda75`
- Expected V2-A coverage: selectors 9/9, source pins 43/43, asset-role refs 27/27, unique assets 15/15.
- Operator-confirmed prior preflight saved report SHA-256: `1e41001f83cf9b093919f46ee2f327553c93464f8369ecfb0dc3b34b0a0c9d43`.
- Operator-confirmed V2-A audit saved report SHA-256: `36c014734892fee2d7a1beb2662cd610c6856b4ecb48d9e06bf596f826795327`.

## Semantic proposal
- Base `FrameSnapshot` fields: `position`, `rotation`, `scale`, `opacity`, `texture_index`, `variant_id`.
- Static targets from source: CHALLENGE_001, CHALLENGE_002, CHALLENGE_004.
- Custom-data candidate fields (six selector-field proposals): CHALLENGE_003 `target_x`; CHALLENGE_005/006/007 `target_position`; CHALLENGE_008 `active_selection`; CHALLENGE_009 `displayed_count`.
- Every candidate has `binding_authorized=false` and `renderer_projection_approved=false`. Whole `custom_data` maps and telemetry are forbidden.
- CHALLENGE_008 and CHALLENGE_009 remain blocked from runtime materialization until their explicit 11s-vs-12s timebase conflict is decided.
- Existing CHALLENGE_004 V1 harness remains an untouched regression fixture.

## Apply / test
Use a short TEMP staging path and the supplied separate PowerShell 5.1 blocks. The apply is add-only; pre-existing differing paths must stop the operation. Python checks validate the proposal and re-run the accepted V2-A lineage audit. No Godot invocation, payload materialization, renderer input or media output occurs.
