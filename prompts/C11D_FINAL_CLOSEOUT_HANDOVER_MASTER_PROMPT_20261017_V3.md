# C11-D final closeout — master handover prompt V3 (2026-10-17)

You are continuing the ChallengeEngine V01 STATELESS C11-D branch. Read `docs/current/d/C11D_FULL_CONTEXT_CONTINUITY_CHECKPOINT_20261017_V7.md`, `docs/current/d/C11D_CHALLENGE_VISUAL_PAYLOAD_SEMANTIC_BINDING_CLOSEOUT_CHECKPOINT_20261017_V1.md`, and `docs/current/d/C11D_V2B_SEMANTIC_BINDING_REVIEW_AND_RUNTIME_GATE_PLAN_20261017_V1.md` before proposing changes. Treat the active Windows working tree as source of truth and verify current file hashes; snapshots and chat excerpts can be stale.

## Mission

Finish C11-D through evidence-based gates, eventually replacing C11-C only after explicit baseline approval, freeze and promotion. C11-C is frozen and must not be changed or regenerated.

Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Current facts

- Challenge seed-domain planner preflight V2 passed: 9 selectors, 27 variants, 54 planner invocations, deterministic repeats, D4 parity, 0 Godot, no payload.
- Challenge visual payload capability matrix V1 passed in the active checkout: 15/15 tests; 9 selectors; 43/43 source pins; 9/9 mechanic routes; 27/27 asset references; 15 unique assets; 9/9 custom-data inventories; existing preview runtime coverage 1/9.
- Challenge visual payload semantic binding proposal V1 passed in the active checkout: 20/20 tests; 9/9 selectors; 43/43 pins; 9/9 secondary proposals; 3/3 static bindings; 6/6 candidate custom-data fields; 27/27 references; 15 unique assets; 2/2 temporal conflicts. **Approved bindings = 0.** These runs did not invoke Godot or materialize payloads.
- `CHALLENGE_008` and `CHALLENGE_009` retain declared-total vs phase-sum timing conflicts.

## Non-negotiable governance state

`renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; `baseline_approval=MISSING`; `freeze_eligible=false`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed_adopted=false`.

## What to do next

1. Inspect and verify the live semantic binding proposal contract and report schema; confirm they match the current capability matrix. No source edits before understanding the actual contents.
2. Conduct a field-by-field review of each proposed secondary binding and each of the six `custom_data` candidates. Determine source semantics, type, units/coordinate frame, timing, missing values, visual role, seed expectations and test coverage. Do not approve automatically.
3. Keep the 008/009 timebase conflict review independent and unresolved until a documented decision exists.
4. Only after semantic review, design a separate V2-B runtime harness that proves *visual payload* seed sensitivity—not merely request/plan hash sensitivity—plus deterministic repeats, music-seed orthogonality, editorial invariance, negative fail-closed cases and source lineage.
5. Run Python contract tests first. Runtime testing, if authorized by the reviewed plan, must use the valid Godot 4.7.1 Mono executable from the current session/configuration and must not render, create media, write candidate payloads or emit renderer inputs.
6. Capture actual commands, exit codes, stdout/stderr, receipts, report hashes and scope. Update checkpoint/start prompt after evidence is observed.
7. Never print or claim PASS after a failed command, missing output, or a preflight conflict. Preflight every overlay destination before the first copy. Existing add-only targets must be identical by hash or the overlay must abort without writes; do not overwrite historical files merely to keep a filename.

## Architecture and invariants

Extend only the approved `c11c-suite` surfaces. Do not invent `c11d-control`. CLI and future GUI should share the canonical service layer. Shared editorial/presentation inheritance is the default. `winning_frame` is the only Challenge temporal anchor; `close_calls` is episode count only. Presentation must not alter simulation, calculation, input, pause or result. Logical composition remains 540×960 with Header 0–144, Body 144–816, Footer 816–960. A delivery profile of 720×1280/30 FPS does not permit resampling the source preview.

Keep the response concise, exact and evidence-based. If a task is large, make safe progress without asking repeated questions, but never invent an approval or runtime result. Use paste-ready PowerShell 5.1, separate apply and test blocks, short staging paths, explicit directory creation, reliable process exit codes, backup/rollback where replacements are truly approved, and no downloaded `.ps1` requirement.
