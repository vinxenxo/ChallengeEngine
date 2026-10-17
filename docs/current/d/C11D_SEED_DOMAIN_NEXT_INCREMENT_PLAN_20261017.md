# C11-D — Next seed-domain increment after five-selector payload V2 runtime PASS

**Date:** 2026-10-17  
**State:** `PLANNED_NOT_IMPLEMENTED`  
**Prerequisite accepted:** `C11D_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2_RUNTIME_ACCEPTANCE_CHECKPOINT_20261017.md`  
**Authority:** Implementation plan, not authorization to admit renderer input.

## Objective

Move seed-domain coverage from a single Visual Loop representative to all five geometric grammars now admitted by the V2 in-memory request-to-payload chain, without duplicating that chain or editing the frozen V1 seed audit.

## Scope V2

`visual_loops / c11c_geometric_waves_v1`, exact selectors in contract order:

`harmonic_membrane`, `interference_plane`, `parametric_ribbon`, `lattice_wave`, `orbital_wave`.

Seed variants (hold all other request dimensions constant):

| Variant | `gameplay_seed` | `music_seed` |
|---|---:|---:|
| `BASELINE` | 12345 | 840001 |
| `GAMEPLAY_SEED_ONLY_CHANGED` | 54321 | 840001 |
| `MUSIC_SEED_ONLY_CHANGED` | 12345 | 840002 |

Execute each variant twice in independent Godot 4.7.1 headless processes: **30 planned calls**. A receipt failure, source drift, request-chain mismatch, repeat mismatch or seed-domain leak fails the entire audit closed.

## Design constraints before coding

1. Keep `D_RENDERER_CANDIDATE_SEED_DOMAIN_AUDIT_V1` and the V1 collision audit untouched. Their pins and scope are historical/canonical V1 contracts, and the cross-type matrix only covers `CHALLENGE_004` plus `harmonic_membrane`.
2. Add a distinct V2 contract/schema/runner/test/checkpoint for the geometric-loop seed matrix. Parent every receipt to the exact five-selector payload V2 contract and its parameter-binding V2 contract using SHA-256 pins.
3. For every mutation, call canonical D9.9 planning with the changed explicit seed values, then regenerate bridge and adapter identities, source binding, timing/reference joins and parameter-instance identity. Never patch request or report hashes in a returned receipt.
4. If the current metadata/reference carrier only supports the baseline seed tuple, add a versioned request-scoped reference-carrier extension or expose its canonical build function; do not fake a join by copying baseline request identity onto a changed request.
5. Invoke the established exact-selector in-memory payload path through a seed-parameterized internal API or new versioned runner. Keep the current accepted V2 contract unchanged. The new path must reproduce its strict schema, exact five-selector checks, source lineage, 20-parameter projection check, payload self-hash checks, and the 19 assertion/zero approval boundary.
6. Add unit tests for the seed variants, repeat equality, cross-domain independence, source-pinned parents, report self-hash/schema, malformed/missing selector/seed values, equal numeric seeds, automatic/default seeds disabled, `master_seed` rejected, Godot absence/version mismatch and fail-closed source drift.
7. Run contract tests first, then the actual active-Windows Godot matrix. Capture stdout/stderr separately, require actual exit code `0`, verify 30 complete receipts, and record the internal audit hash plus external stdout/stderr hashes and evidence directory.

## Seed semantics to encode correctly

- Gameplay-only change must change request/plan/binding identity and demonstrably change the gameplay-derived parameter/style/visual-content projection for every selector.
- Music-only change must change request/binding identity and keep the gameplay-derived style parameters, family variation recipe, resolved palette and visual-spec projection identical for the same gameplay seed.
- The full exact-selector payload envelope carries `request_identity`, including `music_seed`, and embeds the request hash in its parameter instance. As a result, overall envelope and parameter-instance digests can change after a music-seed-only request mutation even while the visual subprojection remains identical. Do not assert whole-envelope hash invariance; assert projection-level orthogonality and document digest layer semantics.
- Each same-variant independent repeat must reproduce request/plan/binding identity and each relevant projection digest.
- `music_seed` never contributes to gameplay profile generation. Numeric equality across the separate gameplay/music domains remains rejected per the existing policy.
- `master_seed` remains `NOT_ADOPTED`; automatic/default seed derivation remains disabled. This audit does not authorize default behavior merely by testing rejection of omitted seeds.

## Required fail-closed negatives

Before starting Godot: missing/null/wrong-type/boolean/zero/out-of-range gameplay seed; missing/null/wrong-type/zero/out-of-range music seed where the schema/domain requires it; automatic/default seed mode; `master_seed` alias; equal numeric gameplay/music value; mismatched grammar selector and parameter instance; stale parent contract/report hashes; request identity not joined to the regenerated plan/reference; missing or duplicate receipt; changed source pin; non-deterministic repeat; visual leakage on music-only mutation.

The expected negative count must be specified by the V2 contract and tested exactly; it must not be copied from an older V1 audit count without a case-by-case matrix.

## Outputs

- Strict Draft 2020-12 contract/report schemas.
- Versioned V2 contract naming all five grammar selectors and seed variants.
- Source-pinned Python runner + contract/negative tests.
- Existing Godot harness reuse if its input/receipt contract is sufficient; otherwise a separate V2 request-bound harness, not a change that breaks the accepted V2 harness.
- Evidence-grade Windows checkpoint and concise README/overlay manifest.

## Exit criteria

All 30 runtime calls return valid source-pinned receipts, gameplay seed sensitivity is 5/5, music visual-projection orthogonality is 5/5, repeats pass 15/15 variants (the three variants for each selector), all declared fail-closed negatives pass, report schema/self-hash pass, and governance remains unchanged. Afterward refresh the candidate I/O and identity source pins. This closes only the geometric Visual Loop seed sub-scope, not all candidate seed domains.

## Deferred / separate gates

Challenge variants; four non-geometric Visual Loop families; the remaining 27-grammar inventory outside this exact five-grammar set; Visual Drill seed-matrix retest unless sources change; explicit approval of automatic/default seeds; master seed adoption; editorial consumption; presentation/coordinates; timebase/timeline; audio/music delivery; candidate I/O admission; D4.8; renderer; media; D9.14/D9.16/D9.17/D10; baseline approval/freeze/promotion/cutover.

## Governance

`renderer=OFF`; `candidate_input_admissible=false`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; D10 blocked. Keep C11-C immutable.
