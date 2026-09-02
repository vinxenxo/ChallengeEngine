# ChallengeEngineV01

Motor determinista para producir vídeos de retos de precisión.

## Current status

```text
Checkpoint 0.9.0 — Production Contract Consolidation
FROZEN / VALIDATED
```

## Core principles

- Stateless deterministic RNG.
- Semantic stream capabilities for RNG 2.0.
- Pure deterministic simulation separated from presentation.
- Godot calculates and renders RAW.
- Python orchestrates production and provenance.
- FFmpeg packages the final MP4.
- FFprobe validates physical artifacts.
- External Python runner is the final suite-level PASS/FAIL arbiter.

## Production contract

```text
factory_version  = 0.10.0
manifest_version = 1.0
FPS              = 60
PHASES           = HOOK / GAME / REVEAL / CTA
RULE             = 0 frames => phase omitted
GAME             = > 0 frames
TOTAL            = suma de fases activas
```

Canonical output:

```text
output/CHALLENGE_XXX/
output/BATCH_MANIFEST.json
```

## Fixtures

```text
001 key         RNG 1.0
002 parking     RNG 1.0
003 pilot       RNG 2.0
004 parking_v2  RNG 2.0
005 hit_v1      RNG 2.0
006 catch_v1    RNG 2.0
```

## 1.0.0 direction

FIND is the selected candidate for the next mathematical family. Its contract is still in draft. MATCH is not being introduced in 1.0.0.

See:

- `docs/PRODUCTION_PROVENANCE_CONTRACT_V1.0.md`
- `docs/CHECKPOINT_1.0.0_B_FIND_CONTRACT_DRAFT.md`
- `MASTER_HANDOVER_CHECKPOINT_0.9.0.md`
