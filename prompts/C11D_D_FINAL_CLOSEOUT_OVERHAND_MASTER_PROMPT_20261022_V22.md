# MASTER OVERHAND PROMPT — C11-D Runtime Fix V2 — 2026-10-22

## Authority and continuity

C11-C 2.19.12 remains immutable and authoritative. Do not edit its freeze manifest. Current V2-B consumer runtime V1 failed the Godot run despite printed denominator lines; actual stderr reported invalid comparisons of float/Vector2 to Object in the missing-key sentinel test. The V2 fix creates new files and leaves failed V1 artifacts untouched.

## Gate sequence

1. Validate the fix ZIP SHA and manifest SHA.
2. Verify prior receipts, source/authority pins, design pins, and V1 runtime module/harness input hashes.
3. ADD_ONLY apply new V2 filenames; refuse all non-identical collisions.
4. Run V2 static suite with 114/114 expected checks.
5. Run V2 Godot Mono `4.7.1.stable.mono.official` harness: 241 negative, 36 positive, 277 total; require process exit 0 and stdout marker PASS. Record both output hashes and create a receipt only after post-test integrity checks pass.
6. Review results before any next gate. Do not wire into production, change core simulation or snapshots, enumerate/copy/serialize all `custom_data`, enable renderer, bind renderer projection, create media, materialize payload, or run a render test.

## Fixed governance locks

`renderer=OFF`, `release_authority=NONE`, `baseline_approval=MISSING`, `freeze_eligible=false`, `candidate_input_admissible=false`, `runtime_implementation_authorized_for_production=false`, `render_test_authorized=false`, approved bindings zero.
