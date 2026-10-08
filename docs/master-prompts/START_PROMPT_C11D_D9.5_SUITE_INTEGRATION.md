# START PROMPT — C11-D D9.5 Suite Integration

Continue from the latest local D9.4 checkpoint.

## Source of truth

Use the user's latest C11-D tree as the active workspace.

D9.4 receipt must be:

`artifacts/tests/c11d_d9/d9_4/evidence/d9_4_receipt.json`

with:

`result=PASS`, `status=CLOSED`.

## Mission

Complete D9 as the **integration/evolution layer** of the canonical `c11c-suite`.

Do not open D10 yet.

## Read first

- `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md`
- `docs/current/d/D9.4_ACCEPTANCE_CHECKPOINT.md`
- `docs/current/d/D9.5_ENTRY_BRIEF.md`
- `docs/current/d/D9.5_SUITE_INTEGRATION_FOUNDATION_CONTRACT.md`
- `docs/c11/C11C_STUDIO_MASTER_SPEC_v2.1.4_FULL_CONFIGURATION.md`
- `docs/c11/C11C_STUDIO_SUPER_PROMPT_PRINCIPAL_DEVELOPER_v2.1.4.md`
- `c11c-suite/README.md`
- `c11c-suite/main.py`
- every `c11c-suite/*/main.py`
- canonical D4–D9 contracts and runners.

## Architecture rule

Port the useful Studio architecture into the active `c11c-suite`; do not revive a parallel operator root.

Required concepts include:

`ProjectContext / ToolDiscovery / EnvironmentValidator / CommandBuilder / JobManager / ArtifactRegistry / LogCenter / SeedManager / Dashboard / Review / Production / Catalog / Reproducibility / Validation / Operations`.

They may be introduced incrementally and should remain thin wrappers over canonical backend contracts.

## Frozen boundaries

Do not modify C11-C simulation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts or logical 540×960 geometry.

Do not introduce runtime seed derivation or a second production pipeline.

D4.8 remains governed by its existing BLOCKED policy.
D8 release authority remains NONE.

## Acceptance direction

Before D9 closes, the GUI must execute representative real operations through the GUI and verify their evidence on the real Windows workstation. The final D9 certificate must prove CLI/GUI equivalence, visible state/provenance, production safety, reproducibility, operations safety and no protected-root mutation.
