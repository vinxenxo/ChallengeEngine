# C11-D Start Prompt — Current State (2026-10-17 V4)

Continue from the **active Windows checkout**, not from a stale ZIP. Read these current documents first:

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`
4. `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261017_V4.md`
5. `docs/current/d/C11D_VISUAL_LOOP_SEED_DOMAIN_AUDIT_V2_RUNTIME_CHECKPOINT_20261017.md`
6. `docs/current/d/C11D_CHALLENGE_SELECTOR_PLAN_MATRIX_PREFLIGHT_CHECKPOINT_20261017.md`
7. `docs/current/d/C11D_SEED_DOMAIN_NEXT_INCREMENT_PLAN_20261017_V3.md`
8. `docs/current/d/C11D_WORKSTREAM_NON_DUPLICATION_REGISTER_20261017_V4.md`

## Verified latest gate

Visual Loop exact-selector payload V2 runtime PASS and Visual Loop seed-domain V2 runtime PASS on Godot `4.7.1.stable.mono.official.a13da4feb`. The latter reported `selectors=5/5`, `seed_variant_chains=15/15`, independent repeat pairs `15/15`, gameplay visual sensitivity `5/5`, music orthogonality `5/5`, 60 Godot invocations, source pins as defined by the accepted audit, and `seed_domains_complete_for_candidate_input=false`.

## Next required action

Apply the **additive-only** Challenge seed-domain planner preflight V2 overlay, run its 20 focused tests, then run `d_renderer_challenge_seed_domain_preflight_v2.py --root . --full-report`. This stage must have zero Godot invocations and zero payload materialization.

The universal planner has a catalog for all nine Challenge variants, but the existing V1 request-to-payload binder and Godot harness still admit only `parking_v2 / CHALLENGE_004`. Do not broaden claims based on planner support alone. CHALLENGE_008/009 also contain a timeline mismatch (explicit total duration 11 seconds vs component sum 12 seconds); leave them unapproved for timeline/payload until the shared temporal-policy workstream resolves it.

After the planner preflight passes, plan an additive Challenge V2 payload path that reuses the universal planner and D9.10 bridge/adapter, with exact source identity, mechanics/asset whitelist/timebase evidence, seed sensitivity, repeat checks and fail-closed negatives. Do not mutate accepted V1 binder contracts in-place or duplicate the universal planner.

## Locked boundaries

Never edit the frozen C11-C manifest, simulation truth, RNG ownership, `winning_frame`, or `close_calls`. Do not create media or renderer inputs. Keep `candidate_input_admissible=false`, `renderer=OFF`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED`, `release_authority=NONE`, `master_seed=NOT_ADOPTED`, and automatic seed generation disabled. No baseline approval/freeze/cutover without explicit formal authorization.
