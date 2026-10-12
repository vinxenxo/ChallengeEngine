# D9 Shared Editorial/Presentation Context Binding Checkpoint V1

Status: `PREPARE_ONLY_SHARED_CONTEXT_BINDING_NOT_RENDERER_INPUT`.

## Decision

This increment creates one request-scoped, in-memory binding record joining the canonical D9.9 request/plan, resolved D9.8 editorial values, D9.10 bridge identity, and a D-owned presentation-profile reference registry. It does not modify the canonical Producer or bridge implementations.

## Profile reference registry

`social_default_v1` is registered as an identity reference because the existing `PresentationProfile.gd` declares it as `DEFAULT_ID`. The registry carries identity only: geometry and physical presentation are not embedded, resolved, or approved. Unknown profile IDs reject until an explicit versioned and hash-bound registry change is added. This is not a claim that all future profiles are render-ready.

## Binding rules

- Source values come from `evaluate_universal_request`, `plan.editorial`, and the D9.10 bridge record.
- The same request hash and plan hash tie editorial values and presentation-profile identity to the same context.
- The current D9.8 allowlist decides shared fields versus Challenge-only fields. `language` remains metadata.
- Gameplay and music seeds stay separate domains. Editorial and presentation identity changes cannot write or derive seeds.
- Unknown profile references, altered hashes, unexpected editorial fields, and cross-content Challenge-only fields reject.
- Output is stdout-only/in-memory; no receipt file is written.

## Evidence boundary

This proves identity/context binding, not a physical renderer binder, profile geometry, semantic regions, editorial visibility windows, or exact visual payload. `renderer=OFF`, `media_created=false`, `D4.8=BLOCKED`, `release_authority=NONE`, D9.17 NO-GO, D10 BLOCKED. Frozen C11-C source is not modified.

## Windows CLI encoding hardening

The separate-process CLI emits JSON with ASCII escapes so protocol bytes are independent of the active Windows console code page. The contract test captures subprocess output as bytes, validates successful exit and ASCII-safe JSON before parsing, and reports process/JSON failures directly instead of surfacing a secondary decoding or `json.loads(None)` exception.
