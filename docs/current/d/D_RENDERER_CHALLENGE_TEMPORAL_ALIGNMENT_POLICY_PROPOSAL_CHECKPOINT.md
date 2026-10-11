# C11-D Challenge Temporal Alignment Policy Proposal — V1

**Status:** `PROPOSED_NOT_APPROVED` — static policy review only.

## Purpose

Declare a single, testable reference for aligning the frozen 60 FPS Challenge timeline, the 30 FPS `REVIEW_720` delivery timeline, the explicit editorial field-window proposal, and the independent GAME sample-selection proposal. This proposal aligns their existing declarations; it does not approve them or materialize renderer input.

## Pinned reference case

- Challenge: `CHALLENGE_004`, mechanic `parking_v2`.
- Source timeline: 900 frames at 60 FPS, 15 seconds.
- Delivery timeline: 450 frames at 30 FPS, 15 seconds.
- Source phase boundaries: `0, 180, 600, 780, 900`.
- Delivery phase boundaries: `0, 90, 300, 390, 450`.
- Phase frame counts: source `180, 420, 180, 120`; delivery `90, 210, 90, 60`.
- Source and delivery ranges use zero-based half-open intervals `[start, end)`.
- Runtime winning anchor reference: absolute source frame `574`, source GAME-local index `394`, delivery GAME-local index `197`, absolute delivery frame `287`.
- Editorial field-window reference remains a separate proposal: Hook `[0,90)`, empty Reveal suppressed, CTA `[390,450)`. Phase names do not imply text visibility by themselves.
- GAME sample selection remains a separate proposal: even zero-based GAME-local indices `0,2,...,418`, no interpolation.

## Proposed boundary rule

For this one supported source/delivery ratio, project each cumulative source boundary using nearest delivery tick, ties half-up:

`floor((2 * source_boundary * delivery_fps + source_fps) / (2 * source_fps))`

All boundaries in this pinned case land exactly on the 2:1 cadence, so there is no boundary drift. Other timebases fail closed and require a separate proposal.

## Guardrails

- The contract does not sample snapshots or construct the 210-record delivery candidate.
- It does not rewrite `winning_frame`, `close_calls`, `SimulationResult`, RNG, or metrics.
- `close_calls` remains episode count only.
- It does not infer visibility from phase labels, define audio behavior, invoke renderer/FFmpeg, write payloads or persistent reports, or create media.
- C11-C 2.19.12 and its freeze manifest stay immutable.
- Renderer OFF; `D4.8=BLOCKED`; `release_authority=NONE`; D9.14/D9.16 acceptance remain blocked as required; D9.17 remains NO-GO; D10 remains blocked.

## Verification

Run `python .\tools\c11d\d9\test_d_renderer_challenge_temporal_alignment_policy.py` from the repository root. This validates the contract, exact cumulative phase boundaries, half-open coverage, 15-second duration parity, winning-anchor alignment, editorial/sample proposal parity, source lineage, and fail-closed governance. A PASS is not approval.
