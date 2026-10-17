# C11-D Workstream Non-Duplication Register — V4

| Workstream | Canonical owner | Status / rule |
|---|---|---|
| Universal Challenge selection and request planning | `tools/c11d/d9/universal_producer.py` + `universal_editorial_model.py` | Supports canonical nine Challenge variants; use this shared planner, do not create a second planner |
| Existing dynamic request-to-payload V1 | `d_renderer_dynamic_request_payload_binding.py` + `materialize_dynamic_request_payload_in_memory.gd` | Intentionally pinned to CHALLENGE_004 for Challenge; do not claim multi-Challenge support or edit its V1 gate in place |
| Visual Loop grammar parameter binding V2 | Existing request-scoped grammar parameter binder V2 | Accepted for five geometric selectors; do not duplicate |
| Visual Loop exact-selector payload V2 | Existing exact-selector materializer/audit V2 | Runtime PASS for five geometric selectors; do not duplicate |
| Visual Loop seed domain V2 | `d_renderer_visual_loop_seed_domain_audit_v2.py` | Runtime PASS, five selectors; keep auto/default/collision/arbitrary seed domains blocked |
| Challenge planner seed preflight V2 | `d_renderer_challenge_seed_domain_preflight_v2.py` | New, Python-only; proves D9.9 request/plan sensitivity only, not payload behavior |
| Future Challenge V2 materialization | Not yet implemented | Additive extension that reuses D9.9 planner and D9.10 bridge/adapter; must cover per-mechanic payload/timebase/assets and not fork universal selection logic |
| Shared temporal policy | Existing Challenge temporal alignment / unified content review workstream | CHALLENGE_008/009 11-vs-12s contradiction is visible; resolve there, not via a parallel timing policy |
| Shared editorial/presentation/audio and candidate I/O | Existing unified review and candidate I/O workstreams | No duplicate consumers/policies; all proposals remain unapproved until explicitly adjudicated |

## Governance remains unchanged

Renderer OFF; no media; candidate input inadmissible; C11-C immutable; D4.8 BLOCKED; release authority NONE.
