# D Renderer Request-Scoped Editorial Value Carrier — Checkpoint V1

**Date:** 2026-10-12  
**State:** `PREPARATION_ONLY_HASH_BOUND_EDITORIAL_SIDECAR_NOT_VISUAL_CONSUMPTION`  
**Scope:** C11-D; the three existing fixed D9.9 review fixtures only.  
**Approval:** not approved; not renderer input; no production, baseline, freeze or release approval.

## Why this increment is bounded

The operator confirmed the preceding request-scoped materialization runner and regressions completed successfully under Godot `4.7.1.stable.mono.official.a13da4feb`. That gate establishes the two existing in-memory Godot harnesses execute. It does not establish editorial text is part of their visual payloads.

The field audit and routing reconciliation still distinguish **14/14 canonical-to-review-chain values** from **0/14 values consumed by the current visual payloads**. That distinction remains unchanged here.

## Decision

A **D-owned editorial value sidecar** can be contracted without selecting layout, timing, coordinate or audio policy. The sidecar contains the canonical D9.9-resolved strings and per-value SHA-256 digests; each supported content type also binds the canonical request hash separately from the fixed base-materialization request hash and actual in-memory payload hash.

The optional input only overrides enabled editorial string values. It cannot change a fixture's content selection, gameplay seed, music seed, variation index, delivery profile or presentation profile. Every override is re-resolved by the existing canonical D9.9 producer chain. Unsupported/disabled fields (including `hook`, `reveal`, `cta`, `show_title` and longform fields) are rejected. Challenge phase fields are not aliases for D9.9 `title`, `subtitle` or `call_to_action`.

When editorial values differ from the base fixture, the receipt intentionally records two different request hashes and the unchanged base visual payload hash. This is a sidecar linkage, **not** a claim that the materializer regenerated a request-specific payload or that the visual payload contains or displays the text.

## Measured contract output

| Measure | V1 result |
|---|---:|
| Supported content types | 3/3 |
| Enabled D9.9 field instances carried in sidecar | 14/14 |
| Visual-text values in sidecar | 11/11 |
| `language` metadata values | 3/3 |
| Editorial values injected into visual payload | 0/14 |
| Visual text consumed/rendered by payload | 0/14 |
| Renderer-native input / dispatch / media | none |

`semantic_region_id`, `layout_geometry` and `visibility_window` stay null in every field record. No proposed field route or window is silently promoted.

## Files

- Contract: `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_CARRIER_V1.json`
- Output schema: `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_CARRIER_SCHEMA_V1.json`
- Optional input schema: `definitions/c11d/production/D_RENDERER_REQUEST_SCOPED_EDITORIAL_VALUE_INPUT_SCHEMA_V1.json`
- Console-only implementation: `tools/c11d/d9/d_renderer_request_scoped_editorial_value_carrier.py`
- Focused tests: `tools/c11d/d9/test_d_renderer_request_scoped_editorial_value_carrier.py`

The runner invokes only the existing bounded, headless Godot payload materialization review and then creates a hash-bound in-memory sidecar receipt. Neither payloads nor receipts are written to disk. The optional JSON input is read-only and supports values for the enabled D9.9 field allowlist only.

## Windows verification

From the repository root:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_request_scoped_editorial_value_carrier.py
python -B .\tools\c11d\d9\d_renderer_request_scoped_editorial_value_carrier.py --godot "C:\PATH\TO\Godot_v4.7.1-stable_win64_console.exe"
```

The first command validates contract logic with mocked Godot summaries; it does not execute Godot. The second command executes the actual bounded Godot harnesses and validates the sidecar against their materialization receipt. Its expected summary is `sidecar_fields=14/14`, `visual_payload_consumed=0/14`, `payload_member_injection=false`, `renderer_input=NOT_EMITTED`, `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`.

To exercise changed text values, pass a JSON file matching the input schema using `--editorial-values-file <path>`. Example:

```json
{
  "schema": "C11-D-D9-REQUEST-SCOPED-EDITORIAL-VALUE-OVERRIDES-V1",
  "schema_version": "1.0",
  "values_by_content_type": {
    "visual_loops": {
      "title": "Alternate Loop Title",
      "language": "EN"
    },
    "challenges": {
      "player_name": "MARTA"
    }
  }
}
```

The canonical D9.9 resolver normalizes these values (for example, `language` to lowercase) and the sidecar hashes them. The actual base payload hash remains unchanged and the output explicitly marks visual consumption false. Do not interpret this as end-to-end visual editorial acceptance.

## Gates retained

- Frozen C11-C manifest remains pinned to `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; no C11-C or simulation mutation.
- `renderer=OFF`; `renderer_native_input_emitted=false`; `renderer_dispatch_invoked=false`; `media_created=false`.
- `candidate_input_admissible=false`; `video_render_ready=false`; `D4.8=BLOCKED`; `release_authority=NONE`.
- D9.14/D9.16 remain blocked, D9.17 remains `BLOCKED_NO_GO`, and D10 remains blocked.
- Renderer implementation/baseline approval is absent. Visual text layout, semantic-region geometry, all editorial visibility windows, delivery timebase, Challenge temporal/sample alignment, coordinate composition/projection, audio/mux/QA remain unresolved or unapproved.

## Next engineering gate

After Windows validation, the next safe increment is to design a **separate D-owned visual consumer** only after the relevant presentation-region and per-field visibility-window policies are formally approved. It must consume the sidecar without changing simulation truth or confusing sidecar presence with rendered consumption. Arbitrary selector/seed/profile transport remains a separate future contract; this V1 intentionally supports only the fixed review identities.
