# C11-D Final Closeout / Handover Master Prompt — V6 (2026-10-17)
 
## Mission

Continue the D9/D10 C11-D renderer-baseline preparation from the exact active Windows checkout. C11-D is a deterministic, renderer-agnostic production system. The eventual objective remains for D to supersede frozen C11-C only after all gates, formal approval, freeze and promotion. That authority has not been granted. Do not treat a passing subgate as promotion eligibility.

## Current highest-priority state

Three Challenge-specific gates now exist and have operator-confirmed static PASS results:

1. Canonical planner preflight V2: 9/9 selectors, 27/27 seed cases, repeats and D4 parity, request/plan identity sensitivity 9/9, editorial invariance 9/9, 5/5 negatives, 54 planner calls, zero Godot/materialization. Saved report `1e41001f83cf9b093919f46ee2f327553c93464f8369ecfb0dc3b34b0a0c9d43`.
2. Visual payload capability matrix V1: 15/15 tests; 9/9 selectors; 43/43 source pins; 9/9 mechanic routes; 27/27 asset refs; 15/15 unique assets; 9/9 `custom_data` inventories; 2 temporal conflicts; existing Challenge 004 preview only 1/9. Saved report `36c014734892fee2d7a1beb2662cd610c6856b4ecb48d9e06bf596f826795327`.
3. Semantic binding proposal V1: **20/20** tests; base track 6/6; proposal rows 9/9; static source bindings 3/3; candidate `custom_data` fields 6/6; assets 27/27 and 15 unique; temporal conflicts 2/2; approved bindings 0. Saved report `c8d7cbc14912f514ad34117882b1ad296835b4845d554285b4062f6997f4de53`.

Challenge visual materialization and gameplay-seed visual sensitivity remain untested by these Challenge static steps. The immediate engineering objective is to inspect live source semantics, then design a separate Challenge runtime-harness V1. Do not expand an accepted V1 binder in place.

## Architecture / scope

- Extend only existing suite surfaces (`c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`); do not create `c11d-control`.
- Reuse D9.9 canonical selector/planner and existing D4/D9.10 adapter signatures only when verified against the source.
- Keep Challenge 004 V1 binder/harness and its pins/asset roles/source frame semantics immutable as regression.
- Treat 001/002/004 static target candidates and 003/005/006/007/008/009 custom-data proposals as unauthorized until reviewed. No blanket `custom_data` serialization.
- `PILOT_0X100.target_x` is scalar, not a 2D target; no fabricated Y or delivery-resolution projection.
- Music seed orthogonality requires canonical request/planner boundary evidence, not a source-only Challenge harness.
- Challenge 008/009 have 11s declared total and 12s segment sum; do not accept their phase-bound runtime payload until shared timebase authority makes a decision.

## Evidence discipline

Use reports, exit codes, source pins and hashable receipts. Distinguish request hash, plan hash, source snapshot hash, safe visual projection hash and payload instance hash. A request-envelope hash difference is not proof the visible state changed. Use independent Godot processes for repeat checks. Do not report selector coverage beyond the selector rows actually tested. If a source mechanic does not respond to a gameplay seed, report blocked/failing rather than synthetic visual mutations.

## No-go boundaries

Frozen C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` must remain unchanged. Keep renderer OFF; media false; candidate input inadmissible; seed domains incomplete; automatic seed false; master seed not adopted; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; baseline approval missing; freeze ineligible; release authority NONE. No renderer-native inputs, renderer dispatch, media creation, release, freeze, promotion or C11-C cutover.

## Tooling / PowerShell 5.1 conduct

Use short temp roots; ZIP entries/directories and actual hashes must be verified before application. Apply only add-only destinations or replacements with exact prior-hash preconditions and a backup. Keep application and tests separate. Use a single complete block, fail closed, capture native exit code plus stdout/stderr separately. Do not let a success banner print after a command failure. Do not use `$PSScriptRoot`, `&&`, PS7 syntax, stale variables after exceptions or path assumptions inferred from a ZIP's display name. Before every new overlay, perform a local source/contract read and write tests before runtime integration.
