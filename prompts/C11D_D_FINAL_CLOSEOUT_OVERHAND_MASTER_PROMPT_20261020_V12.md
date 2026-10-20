# C11-D Final Closeout Overhand Master Prompt — V12 (2026-10-20)

## Authority

Continue engineering C11-D using the live checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` as the only authority for active files. Context snapshots and overlays are references, not proof of checkout identity. Frozen C11-C manifest SHA remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; do not change it.

## Accepted evidence gates

- V2-B design contract tests 90/90, 11/11 files, 81/81 source pins, 9/9 authority pins.
- V2-B runtime implementation tests 198/198; receipt `e64cfd259914c471d03e8578b955140ad487b04694c5f682834517d823fcbfc4`.
- V2-B runtime safe-projection acceptance `PASS_SAFE_PROJECTION_SEED_SENSITIVITY`, planner 45/45, Godot 4.7.1 Mono 45/45, selectors 9/9, evidence logs 45/45, source pins 81/81, authority pins 9/9. Report SHA `f7a1522695cbd6d3f3681d3f266b625e3062d5141c32cddbb4532bcb466e0446`.
- Candidate evidence audit reconciled PASS with 6/6 typed candidates and no raw values; audit SHA `8c4503c128355fa21e670be0aaea25b093a73c325253a2afcec2a066a92e5f00`. Its two implementation fixes were tested 39/39 and 40/40; do not repeat the Godot matrix for auditor-only changes.

## Current increment: explicit candidate semantic review

The next add-only overlay introduces a source-bound semantic review request, a strict request schema, and a separate semantic decision-record schema. The request links the source semantic review (SHA `374472b2d7ab0a70d94ed1f650302869b829252dcf06a7afe29c7c2e18e345dc`), V2-B design, seed matrix, V2-C contract, runtime report, implementation receipt and sanitized audit SHA. It intentionally keeps all decisions pending, binding flags false, and raw values absent.

The six candidates are: `CHALLENGE_003.target_x: float`; `CHALLENGE_005.target_position: Vector2`; `CHALLENGE_006.target_position: Vector2`; `CHALLENGE_007.target_position: Vector2`; `CHALLENGE_008.active_selection: int`; `CHALLENGE_009.displayed_count: int`. Respect field-specific lifecycle and seed semantics. In particular, Pilot's `target_x` is a scalar configured track and is not itself a gameplay-seed sensitivity oracle; Hit's target is a per-run constant; Catch/Find target fields are per-frame tracks; Choose is an option index; Count's displayed count is not `target_count` and is also encoded in primary position.

CHALLENGE_008/009 remain source-frame-only because total duration is 11s while phase durations total 12s. This semantic review does not approve any coordinate projection, field-to-region, visibility/timebase policy or renderer mapping. Static target proposals 001/002/004 remain unapproved and out of this six-candidate runtime audit.

## Procedure

1. Apply the add-only review-request overlay with all hashes and pins verified; stop on any unexpected destination or source drift.
2. Run its test with the exact sanitized audit JSON path and SHA; do not rerun Godot.
3. Review all six candidate questions explicitly and write a separate decision record validated by the new schema. Semantic acceptance is not binding approval.
4. Only after a future independent, explicit approval artifact exists may work proceed toward a separate field-to-region/visibility proposal. Do not implement a payload-side visual consumer under this review request.

## Absolute locks

`renderer=OFF`; no payload/media; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; baseline approval MISSING; freeze ineligible; release authority NONE. `CHALLENGE_004` V1 harness/fixture is immutable. Do not serialize all `FrameSnapshot.custom_data`, print raw candidate values, write media, dispatch production or emit renderer-native inputs.
