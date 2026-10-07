# MASTER HANDOVER â€” Challenge Engine V1.0 STATELESS â€” D

**Entry baseline:** sealed C11-C 2.19.12 archive + verified archive/tree SHA-256.

D is an additive productization branch around immutable C11-C engine truth.

## Current checkpoint

D6.4 = PASS / CLOSED

**NEXT = D7 - Production Matrix + Catalog

Read `docs/current/d/D6.4_REQUEST_PLAN_PROVENANCE_INTEGRATION_CONTRACT.md` and the current D handover before implementing or validating D6.4. Do not start D6.5 until D6.4 has a PASS/CLOSED receipt.

## First reads

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md`
4. `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md`
5. `docs/current/d/C11-D_MILESTONES_APPROVED.md`
6. `docs/current/d/D6.4_REQUEST_PLAN_PROVENANCE_INTEGRATION_CONTRACT.md`
7. `docs/current/d/README_D6.4.md`

## Frozen boundary

Do not change C11-B/C simulation truth, RNG algorithm/ownership, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7, C9 or logical 540x960 geometry without an explicit checkpoint.

## D6.4 integration ownership

- D4.2 owns canonical request identity.
- D6.2 owns seed resolution identity.
- D6.1 owns seed registry and governance policy identity.
- D4.4 owns canonical Production Plan and its SHA-256.
- D6.4 owns only integration/provenance evidence.

## Seed invariants

- `request.seed -> gameplay.seed -> GAMEPLAY`.
- `request.music_seed -> music.seed -> MUSIC`.
- Numeric equality across independent authorities is valid.
- Cross-domain consumption is forbidden.
- Derivation capability remains available but runtime activation is disabled.
- `master_seed = NOT_ADOPTED`.
- Personalization and `variation_index` are not seed authorities.
- Shared/global RNG and Producer automatic selection are not canonical authorities.

## D4/D5 boundaries

D4.4 remains the only Production Plan constructor and plan-hash owner. D5 lineage remains read-only. D4.8 remains BLOCKED and cannot be converted into an authorization grant by downstream evidence.

## Runtime fence

`runtime_authority = NONE`.

`production_execution = false`.

Renderer, Godot production and FFmpeg production execution remain false.

## Approved sequence

D0 â†’ D1 â†’ D2 â†’ D3 â†’ D4 â†’ D5 â†’ D6 â†’ D7 â†’ D8 â†’ D9 â†’ D10.

Do not start D10 mechanics while D1-D6 foundations are unstable.

D6.5 = PASS / CLOSED
