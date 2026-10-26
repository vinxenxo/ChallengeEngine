# C11-D Universal Editorial Field Visibility Policy Proposal — Checkpoint V1 (2026-10-26)

**Status:** `PROPOSAL_ONLY_NOT_RENDERER_INPUT` · **Decision:** pending separate operator review · **Renderer:** OFF.

## Purpose

Join the existing D9.9 universal editorial field inventory to one explicit *candidate* visibility rule for Challenges, Visual Loops and Visual Drills. The proposal is add-only and renderer-neutral. It does not approve the proposed mapping, turn fixture intervals into evaluated runtime windows, or authorize implementation of the editorial payload consumer.

## Candidate rule

For each enabled D9.9 visual-text field with a non-empty canonical string, propose the full zero-based, half-open delivery interval `[0, delivery_frame_count)`. An empty string is suppressed and receives no interval. Preserve exact source text; do not trim, translate, normalize or rewrite it. `language` stays metadata-only with no visual interval.

| Content type | Universal field instances | Candidate delivery fixture | Visual fields | Metadata only |
|---|---:|---|---:|---:|
| Challenges | 6 | REVIEW_720, 450 frames @ 30 FPS | 5 | 1 |
| Visual Loops | 4 | REVIEW_720, 600 frames @ 30 FPS | 3 | 1 |
| Visual Drills | 4 | REVIEW_720, 630 frames @ 30 FPS | 3 | 1 |
| **Total** | **14** | Candidate fixtures only | **11** | **3** |

The candidate timelines are pinned review fixtures taken from the existing still-unapproved timebase proposals, not approved delivery output. The current reconciliation reports zero evaluated intervals because the raw field values and materialized request-scoped delivery-frame counts are not exposed by its runtime summary.

## Region and namespace rules

- `title` / `subtitle` → semantic `HEADER`; `call_to_action` → semantic `FOOTER`.
- Challenge-only D9.9 fields `player_name` / `challenge_label` → semantic `CHALLENGE_OVERLAY`.
- `language` is metadata only; no implied translation, instruction, or visible text.
- Challenge phase fields `hook`, `reveal`, `cta` remain a separate namespace and are not aliases for D9.9 `title`, `subtitle`, or `call_to_action`.
- Region geometry, coordinates, typography, wrapping, safe areas, layering details and pixel placement remain unresolved and out of scope.

## Source and safety boundaries

The contract pins the current canonical producer/model, review manifest, region proposal, both existing window proposals, delivery-timebase/Challenge temporal proposals, and reconciliation/audit contracts by SHA-256. The Windows apply script must abort if any prerequisite hash diverges. Do not overwrite existing files.

`evaluated_visibility_windows=0`; `visual_payload_consumed=0/14` remains the current evidence. This increment does not consume editorial text in a payload, create payload or receipt files, emit renderer-native input, dispatch the renderer, create media, or alter C11-C. `candidate_input_admissible=false`; approved bindings remain zero; D4.8, D9.14, D9.16, D9.17 and D10 retain their existing locks; release authority remains NONE.

## Required next gate

Run the focused tests and proposal validator on the active Windows checkout. Then review this proposal in a *separate* immutable decision record. A proposal test PASS is not an operator decision. Only after explicit field-window and presentation-region decisions—and their independent dependency gates—may a later separately authorized increment implement a D-owned editorial payload consumer. Do not infer approval, rendering authority, or readiness from this checkpoint.
