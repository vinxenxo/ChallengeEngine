# C11-E E4A Challenge presentation-configuration coverage plan — V1

**Date:** 2026-11-04  
**Status:** planning contract; no new renderer behavior or production authority.

## Purpose

E4A must validate a configurable presentation system rather than a single composition in which every possible editorial value is always visible. The countdown-on composition reviewed by the operator is an intentional valid state. Tests must cover the supported configuration space grounded in the historical repository and approved D policy.

## Repository evidence to inspect before fixing the matrix

1. `docs/current/d/D1.1_CHALLENGE_VISUAL_EDITORIAL_MAPPING_V1.0.md`: maps CHALLENGE_001..009; timing/geometry are UNKNOWN where not recovered.
2. `docs/current/d/D1.5_PLATFORM_LAYOUT_TEMPLATE_CONTRACT.md`: logical canvas 540x960; Header 0..144, Body 144..816, Footer 816..960. Generic safe-area, CTA geometry, typography and asset-fit rules remain UNKNOWN.
3. `docs/current/d/D1.7_CHALLENGE_VISUAL_EDITORIAL_DECLARATIVE_MAPPING.md`: nine unique Challenge mappings inherit the common layout; no Challenge layout overrides.
4. Historical `ChallengePresentationBinder.gd`, `C11CVisualEditorialLayer.gd`, Challenge definitions, family profiles, tests and review receipts: use these to recover state/phase visibility and actual historical variants. They are protected historical evidence, not patch targets.
5. Approved C11E Challenge editorial policy V1: title/subtitle → HEADER/HOOK; call_to_action → FOOTER/CTA; empty values omitted; language metadata-only; player_name/challenge_label geometry-blocked.

## Initial test dimensions

| Dimension | Candidate states | Authority/qualification |
|---|---|---|
| Countdown hook | enabled / disabled | Operator-confirmed behavior; future GUI option via E1 |
| Title | populated / empty | Policy V1; empty omitted |
| Subtitle | populated / empty | Policy V1; empty omitted |
| Call to action | populated / empty | Policy V1; empty omitted |
| Challenge-only player fields | blocked | Do not exercise as visible output until geometry authority exists |
| Language | metadata only | No visual pixel expectation |

This table is a dimension inventory, not a command to execute every mathematical combination. Build a compact representative matrix from actual Challenge variants and historical tests. Each selected row must record challenge ID, source definition SHA, presentation profile, hook/countdown state, supplied/omitted editorial values, expected phase and region, frame sample, visual result and receipt. Do not synthesize unknown timing or geometry.

## Minimum representative cases

- countdown ON with the operator-selected editorial composition (known valid case);
- countdown OFF with otherwise identical request/editorial values, proving the hook disappears while other approved output behaves as expected;
- header editorial populated with CTA omitted;
- CTA populated with header editorial omitted;
- title and subtitle both present, with CTA present or omitted only where a historical/approved profile supports the arrangement;
- one historical challenge variant with a distinct recovered presentation arrangement, if source evidence confirms it.

The exact number of rows and per-Challenge assignments must be set after the historical source inventory. No arbitrary all-2^N sweep. Reuse shared E1 service; no GUI-only logic, parallel binder, second renderer or sixth surface.

## Exit evidence

Focused contract tests, request/receipt proof of the selected configuration, pixel/frame evidence at the appropriate phases, source/body identity checks, configuration-specific expected visibility checks, GUI/CLI same-service parity, and user visual review. All visual runs stay test-only under current governance locks.
