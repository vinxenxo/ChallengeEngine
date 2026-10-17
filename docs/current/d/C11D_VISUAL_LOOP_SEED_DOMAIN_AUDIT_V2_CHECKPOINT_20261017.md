# C11-D Visual Loop Seed Domain Audit V2 — Checkpoint

Date: 2026-10-17  
State: `CONTRACT_AND_UNIT_TESTS_PASS; WINDOWS_RUNTIME_PENDING; CANDIDATE_INPUT_INADMISSIBLE`

## Purpose

Prove explicit `gameplay_seed` sensitivity and `music_seed` orthogonality across the five already accepted geometric Visual Loop V2 selectors, without claiming general seed-domain completeness or renderer eligibility.

## Preconditions and lineage

- Frozen C11-C manifest: `release/C11C_FREEZE_PACKAGE_MANIFEST.json`, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; not modified.
- Exact-selector V2 parent contract SHA-256: `50379db3cd15dcae2ca8a39b6ddfc0d2e73835bea7d98983f81ed5c6ebcdd325`.
- Request-scoped grammar parameter binder V2 contract SHA-256: `f7c35fd5afbb593734aa340e838ef3081f86d9d971ef2bdcffe341a413494947`.
- Exact-selector V2 lineage closure remains the authority for 70 source pins. This audit must not fork or reduce it.
- The newly added audit contract pins its implementation and both strict schemas by SHA-256.

## Bounded matrix

Selectors: `harmonic_membrane`, `interference_plane`, `parametric_ribbon`, `lattice_wave`, `orbital_wave`.

Each selector is exercised with:

1. BASELINE: `gameplay_seed=12345`, `music_seed=840001`.
2. GAMEPLAY_SEED_ONLY_CHANGED: `gameplay_seed=54321`, `music_seed=840001`.
3. MUSIC_SEED_ONLY_CHANGED: `gameplay_seed=12345`, `music_seed=840002`.

There are 15 selector/variant combinations with two separately planned and executed receipts each: 30 full-chain receipts. Each receipt invokes the existing parameter binder V2 and exact-selector payload V2 in Godot: 30 + 30 = 60 Godot probe invocations, plus one version probe.

## Acceptance predicates

- All 15 selector/variant chains planned by canonical D9.9 request/bridge/adapter, with source-binding lineage rebuilt for each seed variant.
- Two independent full-chain receipts per variant pair equal on all recorded identity and payload digests.
- `gameplay_seed` mutation changes request/plan identity and style/variation/palette/visual-spec/full payload hashes for each grammar.
- `music_seed` mutation changes request/plan, binding/parameter-instance and full payload identity for each grammar, but preserves `style_parameters_sha256`, `authoring_envelope_sha256`, `family_variation_recipe_sha256`, `resolved_palette_sha256` and `visual_spec_sha256`.
- 135 selector/seed-variant policy references are metadata-only: `policy_values_consumed=false`.
- Strict input/receipt schemas, exact seed values, 70 parent source pins, output/report self-hash and all governance locks validate.

## Staging evidence (not active-Windows runtime evidence)

The added focused test suite has 17/17 passing unit/contract/negative cases on the isolated snapshot copy. Canonical request-chain planning succeeds for 15/15 selector/variant combinations in that copy. No Godot execution was performed for this new audit during staging. Active Windows Godot acceptance remains **PENDING**.

## Operator runtime command

From the active repository root, first run the focused suite and proceed only if it passes:

```powershell
python -B -m unittest tools.c11d.d9.test_d_renderer_visual_loop_seed_domain_audit_v2 -v
```

Then run the audit with the actual Godot 4.7.1 console executable. The audit prints `C11-D VISUAL LOOP SEED DOMAIN AUDIT V2 PASS` only after runtime evidence, deterministic repeats, semantic seed comparisons and strict report schema all pass. Preserve stdout, stderr, report SHA-256 and evidence folder in the operator checkpoint before marking runtime accepted.

## Open gates and explicit non-claims

This bounded gate does not establish automatic/default seed behavior, `master_seed`, arbitrary numeric collisions or arbitrary cross-domain requests, other Visual Loop families, Visual Drills, Challenge selectors, candidate-I/O completeness, editorial/presentation policy approval, renderer admission, media production, baseline approval or cutover.

Locks remain: automatic seeds disabled; `master_seed=NOT_ADOPTED`; `seed_domains_complete_for_candidate_input=false`; candidate input inadmissible; renderer OFF; media not created; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.17 BLOCKED_NO_GO; D10 BLOCKED; release authority NONE.
