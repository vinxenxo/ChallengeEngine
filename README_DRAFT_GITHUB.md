# ChallengeEngineV01

Motor determinista para producir vídeos de retos de precisión.

## Current status

> **This file is a GitHub README draft, not the authoritative live-status document.**
> The authoritative state for this repository is `MASTER_HANDOVER_CHECKPOINT_1.1.0-C6-D4.md` plus `docs/ROADMAP_PHASES.md`.

```text
Checkpoint 1.1.0-C6-D4
<<<<<<< HEAD
C6-D4 code complete / static contract PASS / Godot E2E pending in this environment
=======
C6-D4 CERTIFIED / Windows Godot 4.7.1 E2E PASS / 9 of 9 factory PASS
>>>>>>> fdd1006 (CHECKPOINT 1.1.0  C6-E E.1)
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

## Current direction

FIND is already integrated and frozen from 1.0.0. The next work is presentation/product convergence: visual fidelity, content authoring, asset/template systems, scalable batch generation, and export/publishing workflow.

See:

- `MASTER_HANDOVER_CHECKPOINT_1.1.0-C6-D4.md`
- `docs/ROADMAP_PHASES.md`
- `docs/DOCUMENTATION_STATUS_1.1.0-C6-D4.md`
