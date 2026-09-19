# ChallengeEngineV01 — Long-Term Project Guide (C11 Freeze)

## Source of truth

- Code: real repository / freeze ZIP.
- Contracts: `docs/` and the active checkpoint contract.
- Evidence: `artifacts/`.
- Conversation handovers are continuity aids, not code authority.

## Architecture

Capa 0 is declarative definitions. Capa 1 is deterministic simulation and validation. Capa 2 is passive presentation and rendering. Capa 3 is production orchestration.

Presentation may consume `SimulationResult`, `FrameSnapshot`, timeline metadata, assets and content metadata. Presentation must not calculate the winning frame, regenerate mechanics, consume structural RNG, or mutate simulation truth.

The social presentation is structurally `HEADER 0..144 / BODY 144..816 / FOOTER 816..960` on a 540x960 output. Challenge framing may be `STATIC_CANVAS`, `PRIMARY_FOCUS` or future `FIT_ENTITIES`.

## Testing model

The repository uses explicit test groups rather than treating all tests as interchangeable:

- CORE: deterministic RNG, mechanics, DDI.
- PRESENTATION: C6 and visual runtime.
- AUDIO: C7.
- AUTHORING: C9.
- C10/C11: freeze and integration contracts.
- PHYSICAL: Movie Maker + FFmpeg/FFprobe.
- STRESS: deterministic seed corpus.

A PASS requires successful process exit, expected PASS marker and absence of fatal runtime markers.

## Seeds

Canonical C11 qualification uses the six fixed seed labels. Stress testing uses a deterministic 32-seed corpus generated from a fixed corpus seed. Tests never generate fresh randomness at runtime.

## Artifacts

All new generated material goes below `artifacts/`. Existing `output/`, `export/` and checkpoint-specific roots remain historical until a validated migration is committed.

## QA video text

Test-only challenge copies may replace Hook/CTA with diagnostic text such as challenge, seed, RNG and FPS. Visual test exports may use the presentation player's QA overlay. Canonical source definitions remain untouched.

## Freeze rule

After C11 Freeze is certified, C11-C may modify presentation art direction and visual assets, but must not reopen simulation mathematics, RNG, challenge contracts, ContentEnvelope schema, or artifact/test architecture unless a new checkpoint explicitly opens that scope.
