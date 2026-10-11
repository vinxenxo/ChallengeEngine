# D9 Unified Presentation Region Policy Integration — 2026-10-11

## Change summary

Added a strict, proposal-only contract and preview builder that reconcile the current logical composition contract with the renderer-neutral frame-program contract. Integrated the preview and its digest into the three-content-type unified review report.

The semantic mapping is `title`/`subtitle` to `HEADER`, `call_to_action` to `FOOTER`, and Challenge-only `player_name`/`challenge_label` to `CHALLENGE_OVERLAY`; `language` stays metadata-only. The mapping does not define geometry, font choices, visual styling, transitions, z-order behavior at runtime, or field visibility timing.

The unified review contract/schema now pin the two existing contracts and the new policy, add the `unified_presentation_region_policy_parity` cross-check and approval locks, increase lineage to 22 sources, and retain a separate unresolved gate for policy approval. The Challenge timing summary exposes delivery `duration_seconds` from the proposed temporal alignment so the audio/video duration check can compare explicit values.

## Validation caveat

The proposal-specific suite and integrated unified-review suite reached pass markers during an earlier preparation pass (15/15 policy tests; 17/17 cross-artifact checks; 30/30 negative checks). A subsequent tightening ensures the policy validator rejects a frozen-manifest digest mismatch. The staging copy available for this build does not contain the canonical frozen manifest bytes, so final source-pinned validation and Godot orchestration must be rerun in the canonical full checkout after applying the overlay. No exception is made for a mismatched frozen manifest.

## Non-effects

No C11-C source, simulation truth, RNG, temporal anchor or metrics are changed. No output media is written. No renderer is activated and no policy is approved. `D4.8=BLOCKED`, `release_authority=NONE`.
