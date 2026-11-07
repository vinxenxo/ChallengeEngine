# C11-E E4B D9.8 / D9.9 Semantic Reconciliation — V2

**Date:** 2026-11-07. Supersedes V1 wording only for current compatibility semantics; V1 and all evidence remain unchanged.

## Problem

D9.8 metadata stated `PENDING_D9_9_UNIVERSAL_REQUEST_ADAPTER` for Loop/Drill even though D9.9 now resolves universal editorial-intent requests for those types in plan-only mode. This made the blocker ambiguous: a plan request could succeed while the D9.8 catalog still claimed the adapter was pending.

## V2 semantics

For Loop and Drill:

- `model_state=ACTIVE_MODEL_ONLY` — editorial allowlist and resolver are active.
- `d9_9_plan_compatible=true` — universal D9.9 canonical request/plan compatibility exists.
- `d4_executable_compatible=false` — no D4 execution compatibility is admitted.
- legacy `request_plan_compatible=false` is retained to avoid conflating the old D4 executable gate with D9.9 planning.
- `request_plan_state=D9_9_UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY`.
- `renderer_activation=false`, `production_execution=false`, `runtime_authority=NONE`, `release_authority=NONE`.

Challenge remains `CURRENT_D4_CHALLENGE_PATH` for its already accepted D4 request path. Longform remains disabled.

## Implementation and evidence

V80 updates the D9.8 JSON model, resolver catalog/selection/result and focused tests. Local snapshot test: 9 Challenges, 5 Loop families/27 grammars, 4 Drill types/20 variants, negative 25/25, Longform disabled. Service expected pin updated to the exact new resolver SHA. Windows runner validates postimage pins and reruns focused model/service tests.

## Consequences

This resolves only the stale plan compatibility label. It does not grant D4 execution compatibility, materialize payload, emit renderer input, dispatch a launcher, generate media, close D9.14/D9.16/D9.17 or authorize D10 promotion. D4.8 remains BLOCKED.
