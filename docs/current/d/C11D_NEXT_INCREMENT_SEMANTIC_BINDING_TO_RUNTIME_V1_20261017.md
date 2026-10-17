# C11-D Next Increment — Semantic Binding Review to Challenge Runtime Harness V1 (2026-10-17)

## Goal

Move from the accepted static Challenge visual capability matrix and static semantic-binding proposal to a separate, bounded **runtime source-frame/payload harness** without crossing into renderer admission, media creation or release. The deliverable is evidence-bearing source-frame payload instances/receipts per supported selector, not rendered video.

## Entry criteria (satisfied)

- Capability matrix V1: 15/15 tests; 9/9 selectors; 43/43 pins; 9/9 mechanic routes; 27/27 asset-role references; 15/15 unique assets; 9/9 custom-data inventory. Saved report SHA-256 `36c014734892fee2d7a1beb2662cd610c6856b4ecb48d9e06bf596f826795327`.
- Semantic binding proposal V1: 20/20 tests; base track 6/6; candidate secondary rows 9/9; static-source candidates 3/3; custom-data candidates 6/6; temporal conflicts 2/2; approved bindings 0. Saved report SHA-256 `c8d7cbc14912f514ad34117882b1ad296835b4845d554285b4062f6997f4de53`.
- Challenge planner preflight V2: 27/27 cases, repeat stability and D4 parity 27/27, 54 planner calls, 0 Godot, saved report `1e41001f83cf9b093919f46ee2f327553c93464f8369ecfb0dc3b34b0a0c9d43`.
- V1 Challenge 004 preview remains the fixed regression fixture.

## Mandatory source review before runtime code

Review live source (not just documentation) for all nine definitions, mechanic dispatch, `FrameSnapshot` declaration/producer, timeline/timebase definitions and existing V1 binder/harness. Confirm actual type, coordinate space, sample rate, origin and lifecycle semantics for every candidate field. If the source does not establish semantics, keep the row `UNRESOLVED`/blocked instead of guessing. Confirm precise signatures for the canonical D9.9 planner, D4 adapter and D9.10 bridge before using them.

## Required runtime harness properties

1. Separate versioned CLI/harness and report schema; source pins over every consumed source/definition/asset; fail-closed behavior on drift.
2. Explicitly distinguish request identity, plan identity, source snapshot identity, safe visual projection and payload instance identity. Do not use the full request hash as proof of visual sensitivity.
3. For each in-scope selector, use independent Godot processes and exact runtime version `4.7.1.stable.mono.official.a13da4feb` or verify the actual runtime executable/version from the operator's session.
4. Prove deterministic repeated payload projection for identical inputs; prove gameplay-seed visual sensitivity by an actual projected-state difference for a selector where the mechanics genuinely respond. Do not fabricate seed effects for mechanics that cannot consume seed input.
5. Exclude editorial fields, music seed and nonvisual telemetry from the safe visual projection. Music-seed orthogonality is a separate canonical request/planner boundary test, not something this source-only harness may claim.
6. Write no production payload files by default. If temporary receipts are required, use an isolated OS temp evidence folder and label them audit receipts, not renderer payloads. No renderer input, dispatch or media.
7. Treat unsupported mechanics, absent required fields, non-finite values, coordinate ambiguity, hash drift, inconsistent repeats or unexpected native exit codes as hard failures/blocked rows.

## Selector coverage and semantic constraints

- 001: static lock target proposal; source review required.
- 002: static parking target proposal; coordinate space must be resolved from source before projection.
- 003: `target_x` is scalar in `PILOT_0X100`; do not invent Y or a 2D projection.
- 004: retain current V1 as immutable regression path; compare against it rather than modifying it.
- 005/006/007: candidate `target_position` secondary track; inspect source type and its association with the primary actor before binding.
- 008: `active_selection` proposal; no phase-bound payload until the 11s declared / 12s phase-sum conflict is adjudicated.
- 009: `displayed_count` proposal; no phase-bound payload until the same class of timebase conflict is adjudicated.

All proposals remain unauthorized. Require a separate review artifact to change `binding_authorized` or `renderer_projection_approved`.

## Test phases

A. Static contract/schema/tests and negative cases only.
B. Source-review matrix and decision record (including blocked rows).
C. Minimal Godot runtime receipt harness on a deliberately limited in-scope subset; don't imply all-nine success if any selector remains blocked.
D. Extend coverage only after each mechanic row has an explicit, source-backed projection and the V1 regression stays green.
E. Canonical request-boundary seed orthogonality / broader seed-domain completeness are separate gates.

## Not permitted

No `c11d-control`; no C11-C changes; no edits to canonical seed V1 or Challenge definitions; no default/master seed adoption; no broadening V1 selector guards in place; no coordinate extrapolation; no wholesale `custom_data`; no output/media production; no renderer switch; no candidate-input admission; no freeze, promotion or release.

## Exit conditions for this increment

Only claim harness acceptance when the report records actual selector coverage, each exact source hash, Godot version, independent process count, process exit codes, repeat hashes, safe visual projection differences, all negative cases and unchanged governance. A partial pass is a scoped partial, never a 9/9 claim.
