# C11-D Shared Editorial/Presentation Inheritance Contract V1

## Scope

This is a **new-files-only** architecture contract and static audit. It formalizes the user-directed future architecture: the GUI selects canonical content type/family/subtype/variant, while editable editorial values and common presentation are resolved through one shared layer. Registered families inherit this layer by default; an exception needs an explicit, versioned, SHA-256-bound declaration and explicit approval.

## Files

- `definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_INHERITANCE_V1.json`
- `definitions/c11d/production/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_INHERITANCE_SCHEMA_V1.json`
- `docs/current/d/D_RENDERER_SHARED_EDITORIAL_PRESENTATION_INHERITANCE_CHECKPOINT_V1.md`
- `tools/c11d/d9/d_renderer_shared_editorial_presentation_inheritance.py`
- `tools/c11d/d9/test_d_renderer_shared_editorial_presentation_inheritance.py`
- `README_C11D_SHARED_EDITORIAL_PRESENTATION_INHERITANCE_OVERLAY_V1.md`

## Current source-of-truth behavior

D9.8 remains authoritative for editorial fields and inheritance order. D9.9 remains authoritative for selector dimensions and canonical request/plan identity. D9.10 remains a planning-only bridge. The currently enabled shared fields are `title`, `subtitle`, `call_to_action`, and `language`; `language` is metadata. `player_name` and `challenge_label` remain Challenges-only. Reserved fields and show/hide controls remain disabled.

## New family policy

An unregistered selector is rejected. A newly registered family inherits the shared editorial and presentation contracts by default. A family may diverge only via a separately identified, versioned, hash-bound, explicitly approved exception. Family adapters provide family-owned visual parameter schemas and must not duplicate or rewrite shared editorial/presentation logic.

## Limits

This contract does not approve presentation geometry, semantic regions, frame timing, editorial windows, renderer input, renderer execution, media creation, or release. The pinned `harmonic_membrane` parameter instance is not an exact selector visual payload; its family authoring envelope gap remains open. C11-C remains immutable. `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, D9.17 NO-GO, D10 BLOCKED.

## Run

From repository root:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_shared_editorial_presentation_inheritance.py
python -B .\tools\c11d\d9\d_renderer_shared_editorial_presentation_inheritance.py
```
