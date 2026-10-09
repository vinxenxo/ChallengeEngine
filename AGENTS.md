# AGENTS.md — ChallengeEngineV01_STATELESS / C11-D D7 FROZEN

## Current authority

**C11-D D7.5 = PASS / CLOSED; D7 = FROZEN. Next = D8.0 Media QA + Release Pipeline.**

Immutable D7.5 baseline:
`ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip`

ZIP SHA-256: `396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`

Do not resume from earlier D7 candidate overlays.

## Mandatory first reads for D8

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `docs/master-prompts/MASTER_HANDOVER_C11D_D7_FROZEN.md`
4. `docs/master-prompts/START_PROMPT_C11D_D8.0.md`
5. `docs/current/d/D7_DOCUMENTATION_CLOSURE.md`
6. `docs/current/d/D8.0_ENTRY_BRIEF.md`
7. `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md`

## Frozen C11-C boundary

Do not modify without an explicit checkpoint, contract update, focused regression and rollback evidence:

- simulation mathematics and mechanic truth;
- RNG algorithm, streams and ownership;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream`;
- C7 audio contracts/ownership;
- C9 authoring semantics;
- logical 540×960 C11-B social geometry;
- proven C11-C presentation/production behavior.

## D7 frozen boundary

D7 created metadata/governance only. It established a deterministic 90-case production matrix and catalog chain but did **not** authorize media production or release execution.

- Matrix authority: `CANONICAL_D7_1`.
- Catalog authority: `CANONICAL_D7_3`.
- Identity/provenance authority: `CANONICAL_D7_4`.
- Full acceptance authority: `CANONICAL_D7_5`.
- `master_seed=NOT_ADOPTED`.
- Cross-domain seed sharing: `FORBIDDEN`.
- D4.8: `BLOCKED`.
- Runtime: `NONE`.
- Production: `false`.
- Renderer: `false`.

## Operator parity

`c11c-suite` remains the canonical GUI operator shell. GUI actions must continue to delegate to the same canonical PowerShell/Python/Godot paths used directly from the command line.

For D, GUI and CLI may be used simultaneously during authoring/testing; no GUI-only backend or state may be introduced.

## Test discipline

Focused checks come before expensive aggregate execution. PowerShell 5.1 compatibility is mandatory. Python validation should use `-B` or `PYTHONDONTWRITEBYTECODE=1` when repository mutation guards are active.
