# MASTER HANDOVER CHECKPOINT 0.9.0

## Project

ChallengeEngineV01 / ChallengeEngineV01_STATELESS

## Current checkpoint

**0.9.0 — PRODUCTION CONTRACT CONSOLIDATION**  
**FROZEN / VALIDATED**

## Frozen history

```text
0.5.x  Batch / Parallel Production                  FROZEN
0.6.0  HIT v1                                      FROZEN
0.7.0  Production Contract Hardening               FROZEN
0.8.0  CATCH v1                                    FROZEN
0.8.1  CATCH Presentation Contract                 FROZEN / VALIDATED
0.9.0  Production Contract Consolidation            FROZEN / VALIDATED
```

## 0.9.0 production contract

- `factory_version = "0.9.0"`.
- `manifest_version = "1.0"`.
- Unit manifests are self-describing provenance certificates.
- Capa 0 metadata is copied exactly when present; the factory never invents missing fields.
- `generation.rng_version` is checked against runtime telemetry.
- Mixed RNG 1.0/2.0 batches are valid; the per-challenge value is authoritative.
- Challenge artifacts are isolated under `output/CHALLENGE_XXX/`.
- `BATCH_MANIFEST.json` is the only canonical challenge-batch artifact at `output/` root.
- Root-level legacy challenge artifacts are selectively sanitized.
- Failed E2E production does not publish partial canonical artifacts.

## 0.9.0 validation evidence

External runner:

```text
HIT_V1_ISOLATION            PASS
CATCH_V1_ISOLATION          PASS
CATCH_PRESENTATION_CONTRACT PASS
```

Production batch:

```text
workers = 2
total   = 6
passed  = 6
failed  = 0
status  = PASSED
```

Metadata:

```text
factory_version  = 0.9.0
manifest_version = 1.0
rng_versions     = ["1.0", "2.0"]
godot_versions   = ["4.7.1-stable (official)"]
```

The CATCH Presentation Contract remains frozen:

```text
FrameSnapshot.position
    → primary catcher

FrameSnapshot.custom_data["target_position"]
    → secondary target
```

No 0.9.0 change redefines this contract.

## Known legacy debt intentionally preserved

Existing fixtures may omit declarative metadata fields. The provenance layer records only what the source actually declares.

In particular:

```text
CHALLENGE_005 → no schema_version / engine_version / video_profile_version / asset_family_version
CHALLENGE_006 → no schema_version / engine_version / mechanic_version / video_profile_version / asset_family_version
```

This is historical debt, not inferred metadata.

## Next checkpoint

# CHECKPOINT 1.0.0 — FIND V1

Current phase:

```text
1.0.0-A  Candidate Audit             PASS
1.0.0-B  FIND Mathematical Contract  DRAFT / REVISION REQUIRED
```

MATCH is rejected for 1.0.0 because its multi-entity state transport would force unnecessary presentation architecture expansion.

FIND is selected as the candidate family.

## 1.0.0 working doctrine

Do NOT yet:

- assign RNG streams;
- modify `SimulationResult`;
- modify `FrameSnapshot` globally;
- modify `WinningFrameDetector` globally;
- modify `GeneradorMaestro.gd`;
- modify CATCH/HIT;
- modify the production factory;
- modify frozen fixtures.

First finish the FIND mathematical contract, then isolate it, then integrate it.

## Mandatory FIND decisions still open

1. event-based close-call semantics;
2. target static vs. micro-motion;
3. distractor topology constraints;
4. exact presentation transport for static distractors without structural RNG access;
5. final capture/score semantics;
6. eventual semantic-stream allocation.
