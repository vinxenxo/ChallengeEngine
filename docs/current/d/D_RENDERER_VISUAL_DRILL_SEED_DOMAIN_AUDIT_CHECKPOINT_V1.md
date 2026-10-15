# Visual Drill V2 seed-domain sensitivity and orthogonality audit — Checkpoint V1

**Date:** 2026-10-15  
**State:** `PREPARATION_ONLY_RUNTIME_PASS_OPERATOR_REPORTED`  
**Scope:** Four Visual Drill families × five tiers only; no catalog-wide claim.  
**Authority:** review-only, source-pinned; not renderer input, baseline approval, freeze, or render authorization.

## Why this gate exists

The accepted Visual Drill V2 runtime matrix has 20/20 type/tier selectors, 20/20 request-manifest closures, 20/20 independent repeats, and 67/67 V2 lineage pins. That proves selector-bound repeatability for the admitted matrix but does not, by itself, prove that changing `gameplay_seed` changes each selected visual payload or that changing only `music_seed` stays out of visual payload/generator state.

This checkpoint adds a read-only audit on top of the canonical V2 binder. It does not introduce a second binder and does not change simulation logic, the `winning_frame` temporal anchor, the frozen C11-C source, or any renderer interface.

## Experiment definition

Three 20-case matrices use the same canonical request IDs, selector families, tiers, profiles, variation index, and all non-seed request fields:

1. **Baseline:** `gameplay_seed=12345`, `music_seed=840001`.
2. **Gameplay-only mutation:** `gameplay_seed=54321`, `music_seed=840001`.
3. **Music-only mutation:** `gameplay_seed=12345`, `music_seed=840002`.

Each case is run through the V2 binder's mandatory independent runtime repeat. Expected total is 3 × 20 × 2 = **120 Godot runtime invocations**. For each selector, gameplay-only variation must change request-binding identity, payload hash and visual-state hash. Music-only variation must change request-binding identity while preserving the payload hash, visual-state hash, and Visual Drill authoring evidence. Exact selector coverage, repeat evidence, seeds and non-seed identity fields are fail-closed checks.

## Files introduced or integrated

- `definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SEED_DOMAIN_AUDIT_V1.json` — 70 source pins, fixed matrix and governance limits.
- `definitions/c11d/production/D_RENDERER_VISUAL_DRILL_SEED_DOMAIN_AUDIT_SCHEMA_V1.json` — strict Draft 2020-12 report schema.
- `tools/c11d/d9/d_renderer_visual_drill_seed_domain_audit.py` — stdout-only Godot runtime audit using the existing V2 binder.
- `tools/c11d/d9/test_d_renderer_visual_drill_seed_domain_audit.py` — fail-closed logic, contract and governance regressions.

The focused Python test passed 12/12 in the isolated preparation tree. This is not the runtime gate. The following command is retained for reproducibility; the operator reports that this gate has since passed on the active Windows checkout.

## Active Windows runtime acceptance — operator-confirmed 2026-10-15

The operator subsequently confirmed that the complete focused/runtime gate returned green on the active Windows checkout. This is recorded as operator-reported acceptance for the Visual Drill seed-domain experiment, scoped to the 20 canonical selectors and three seed variants defined above. The latest chat confirmation did not restate the runtime log SHA-256, so this checkpoint deliberately does not invent one or reuse the different V2 payload-binding log digest. Preserve the original console capture and record its digest when available. This accepted gate remains scoped to Visual Drills; the Challenge/Visual Loop cross-type seed audit is a separate pending gate.

Reported acceptance criteria: `cases=20`, `gameplay_seed_sensitivity=20/20`, `music_seed_orthogonality=20/20`, `source_pins=70/70`, `runtime_invocations=120`; the governed boundary remains renderer OFF and no media.

## Preparation-copy verification — 2026-10-15 (not Windows runtime acceptance)

The focused/static regression chain in the reconstructed preparation tree completed successfully:

- Seed-domain audit contract/logic: **14/14 tests**.
- Candidate I/O gap: **9/9 tests**, `source_pins=45/45`, `groups=10/10`, `complete=0`, `partial=6`, `blocked=4`.
- Candidate identity inventory: **10/10 tests**, `source_files=156`, source fingerprint `b5599c3d3a498e0f0e0d969d5d9b9ac8bbd9a1af1fba621db632a7b9558c016f`.
- Existing Visual Drill V2 source-chain regression: **7/7 tests**.
- Request-scoped payload-binding regression: **negative=51/51**.
- Unified content review: **38/38 tests**, `source_lineage=23/23`, `source_files=22/22`, `harness_contracts=7/7`, `cross_checks=18/18`, `negative=32/32`.

These static results are isolated preparation-copy checks, not a substitute for the operator-confirmed Windows runtime execution. The live 120-invocation gate is reported PASS by the operator; a separately identified SHA-256 for that specific seed-domain log was not restated in the conversation.

## Windows runtime acceptance

From the repository root, set `C11D_GODOT_EXECUTABLE` to the actual Godot 4.7.1 console executable, then execute:

```powershell
python -B .\tools\c11d\d9\test_d_renderer_visual_drill_seed_domain_audit.py
python -B .\tools\c11d\d9\d_renderer_visual_drill_seed_domain_audit.py --godot $env:C11D_GODOT_EXECUTABLE --timeout 120 --full-report
```

Expected positive summary only if runtime actually proves the experiment:
`cases=20 | gameplay_seed_sensitivity=20/20 | music_seed_orthogonality=20/20 | source_pins=70/70 | runtime_invocations=120`.

The runner writes no report or media to disk and emits no renderer-native input. Save the full stdout/stderr as operator evidence and record its SHA-256 in the next accepted checkpoint only after inspection. If a later rerun fails, keep the whole seed-domain gate open and diagnose that exact selector; do not relax the expected relationship.

## Explicit scope limits and next progression

Even after this runtime gate passes, full seed-domain readiness remains **incomplete**. Open requirements include automatic-seed behavior, collisions and cross-domain rules for arbitrary requests, and wider Challenge / Visual Loop request matrices. The next work after the operator-reported Visual Drill gate is to extend the existing canonical binder and tests to bounded Challenge/Visual Loop scopes; then adjudicate the remaining policy proposals (editorial field windows and visibility, presentation/coordinate regions, delivery timebase, and audio/music delivery) before implementing a separately approved payload-side editorial consumer.

## Governance and immutable references

- Frozen manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`.
- `baseline_approval=MISSING`; `freeze_eligible=false`; D9.10=`PREPARE_ONLY`.
- D9.14/D9.16 remain blocked; D9.17 remains `BLOCKED_NO_GO`; D10 remains blocked.
- The I/O gap remains 0/10 complete, 6 partial and 4 blocked. Passing the bounded seed audit cannot make `seed_domains` complete for arbitrary candidate input.
