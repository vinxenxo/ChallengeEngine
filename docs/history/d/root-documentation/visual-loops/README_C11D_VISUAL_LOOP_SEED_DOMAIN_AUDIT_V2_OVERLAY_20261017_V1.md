# C11-D Visual Loop Seed Domain Audit V2 — Additive Overlay V1

Date: 2026-10-17
Target checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`
Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`

## Scope

This overlay adds a strict, preparation-only V2 audit for explicit seed-domain behavior across the five accepted geometric Visual Loop selectors: `harmonic_membrane`, `interference_plane`, `parametric_ribbon`, `lattice_wave`, and `orbital_wave`. It reuses the canonical D9.9 request planner, existing V1 source-binding core, accepted request-scoped parameter binder V2, accepted exact-selector visual-payload V2, and the current selector metadata reference carrier. No parent implementation or accepted parent contract is modified.

Matrix: five selectors × three explicit seed variants × two independent full-chain receipts = 30 full-chain receipts. Each receipt runs one parameter-binding Godot probe and one exact-selector payload Godot probe, so the expected count is **60 Godot probe invocations plus a separate version probe**.

Seed variants:

| Variant | `gameplay_seed` | `music_seed` |
|---|---:|---:|
| BASELINE | 12345 | 840001 |
| GAMEPLAY_SEED_ONLY_CHANGED | 54321 | 840001 |
| MUSIC_SEED_ONLY_CHANGED | 12345 | 840002 |

## Contract semantics

A gameplay-seed-only change must change canonical request/plan identity, gameplay-derived style/variation/palette/visual-spec projections and full payload identity. A music-only change must change request/plan and request-bound binding/parameter/full payload identity, while preserving gameplay-derived style, authoring envelope, variation recipe, palette and visual-spec hashes. The whole request-bound payload-instance hash is not used alone as the music-orthogonality test because it carries seed-bearing request identity.

The current timing/review reference carrier remains selector-scoped metadata only. It provides nine references per selector, but those references are not asserted to be request-bound to the changed seed pairs and their policy values are not consumed. Any failure of the carrier checks fails closed.

## Staging verification already performed

- `python -B -m unittest tools.c11d.d9.test_d_renderer_visual_loop_seed_domain_audit_v2 -v`: **17/17 PASS** in the isolated snapshot copy.
- Canonical request/bridge/adapter/source-binding planning matrix: **15/15 PLANNED** in the isolated snapshot copy; no Godot was invoked for this preflight.
- New contract loaded with all 70 exact-selector V2 source-lineage pins verified.
- Python compilation and CLI `--help`: PASS.
- **Active Windows Godot runtime for this new seed audit has NOT been run.** That must be done by the operator after applying this overlay.

The preceding exact-selector payload V2 runtime gate did pass on active Windows with Godot `4.7.1.stable.mono.official.a13da4feb`; its evidence is recorded separately in `C11D_VISUAL_LOOP_EXACT_SELECTOR_PAYLOAD_V2_RUNTIME_ACCEPTANCE_CHECKPOINT_20261017.md`. This new seed audit must not be described as runtime-PASS until the actual command exits 0 and its strict markers/report validate.

## Governance locks

`automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `seed_domains_complete_for_candidate_input=false`; `candidate_input_admissible=false`; `renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED`; `release_authority=NONE`.

This overlay is add-only. It does not alter C11-C, modify existing V1 seed audits, replace the accepted V2 parameter/payload contracts, create renderer input, write payload files, create media, or authorize promotion.

## Distribution integrity note

This corrected distribution is strictly **ADD_ONLY**: it contains 13 new targets plus this README and the internal manifest. It does not replace `AGENTS.md`, `.continue/rules/CONTINUE.md`, or `docs/current/d/MASTER_HANDOVER_C11D_CURRENT.md`. Those existing documents remain untouched by this overlay. Any later continuity-document update must be delivered in its own overlay with current, independently verified before-hashes.
