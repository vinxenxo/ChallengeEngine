# MASTER START PROMPT — CHALLENGEENGINEV01_STATELESS — 1.1.0-C6-D4

You are continuing work on `ChallengeEngineV01_STATELESS` from checkpoint `1.1.0-C6-D4`.

## Non-negotiable architectural rules
1. Do not alter deterministic simulation truth to solve presentation problems.
2. Do not change RNG stream semantics, seeds, winning-frame mathematics, or frozen mechanic contracts without explicit audit and approval.
3. Treat `VideoTimeline.gd` + challenge `video` config as the temporal source of truth.
4. `0` duration means a presentation phase is omitted; `GAME` must remain > 0.
5. Factory Python and Godot must agree on frame counts before a release is called certified.

## C6-D4 feature
Effective phase order: `HOOK -> GAME -> REVEAL -> CTA`. Any phase with duration `0` is absent from the effective video.

## First actions in this window
- Verify the ZIP baseline and Git diff/state.
- Run `python tests/phase_duration_contract_test.py`.
- In a Godot 4.7.1 environment, run the complete regression suite.
- Render the full 9-challenge batch and verify manifests + FFprobe.
- Then perform the planned repository-wide documentation/audit pass.

## Product convergence roadmap
After C6-D4 certification, prioritize presentation quality, content authoring/profile capabilities, production-ready assets/templates, scalable batch generation, and export/publishing workflow.

## Required final outcome
A clean, reproducible repository base with a migration note, authoritative checkpoint, current roadmap, and no stale documentation presented as live state.
