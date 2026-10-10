# D Renderer Editorial Field Window Proposal V1 — Checkpoint

**State:** proposed, not approved; in-memory review only.  
**Renderer:** OFF · **Media created:** false · **D4.8:** BLOCKED · **Release authority:** NONE.

## Purpose

Propose explicit display windows for canonical editorial text in `CHALLENGE_004` using the already-reviewed `REVIEW_720` phase ranges. This closes the gap between a phase schedule and a field-specific schedule without silently treating phase names as universal visibility instructions.

## Proposed mapping (delivery-frame, zero-based, half-open)

| Editorial field | Phase | Delivery range | Count | State |
|---|---|---:|---:|---|
| `hook` | `HOOK` | `[0,90)` | 90 | `PROPOSED_VISIBLE_WINDOW` |
| `reveal` | `REVEAL` | none | 0 | `SUPPRESSED_EMPTY_EDITORIAL_FIELD` |
| `cta` | `CTA` | `[390,450)` | 60 | `PROPOSED_VISIBLE_WINDOW` |

The policy ID is `C11D_SAME_NAME_EDITORIAL_FIELD_TO_PHASE_FULL_WINDOW_V1`. It assigns a full phase range only because this explicit policy maps a specific source field to a specific phase. It is not a generic rule that all phase ranges are text visibility windows. Source strings remain byte-for-byte unchanged; the preview records their UTF-8 SHA-256 digests.

## Deliberately unresolved

- The mapping policy is **`PROPOSED_NOT_APPROVED`** and does not itself authorize renderer input.
- No editorial field-window mapping is declared for Visual Loops or Visual Drills yet; this contract must not invent titles/CTAs for them.
- This contract does not define font, region geometry, animation, entry/exit transitions, layering, outlines, or safe-area rules.
- It does not map `winning_frame` / `close_calls` to presentation time, select simulation samples, define interpolation/audio, or emit a render program.
- Empty `reveal` remains suppressed; no placeholder copy is synthesized.

## Runtime evidence

`review_editorial_field_windows_in_memory.gd` invokes the effective frozen Challenge runtime twice, checks deterministic runtime evidence and simulation invariance, rebinds the presentation profile only on a deep copy, and builds a digest-backed proposal in memory. It writes no report or payload file.

## Verification

1. Run `python -m py_compile` and `test_d_renderer_editorial_field_window_proposal.py`.
2. Run `godot --headless --path . --script res://tools/c11d/d9/review_editorial_field_windows_in_memory.gd`.
3. Only after Godot reports PASS, run `append_editorial_field_window_proposal_doc_updates.ps1` and the focused regression suite.

A Python contract PASS is not the same as the Godot runtime PASS. Neither result approves the policy, enables the renderer, authorizes D4.8, or freezes the D baseline.
