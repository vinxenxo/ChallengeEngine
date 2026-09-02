# CHECKPOINT 0.9.0 — PRODUCTION & PROVENANCE CONTRACT

**Status:** FROZEN / APPROVED / VALIDATED  
**Scope:** Production provenance, manifest schema, artifact publication and mixed-RNG batch compatibility.  
**Code changes in contract phase:** 0  

## 1. Authority hierarchy

The project uses the following authority order:

1. **Real repository / ZIP:** source of truth for code.
2. **`docs/*.md`:** source of truth for documented contracts when a live contract is explicitly stated.
3. **Checkpoint handovers:** source of truth for continuity and frozen evidence.
4. Historical checkpoint documents remain historical records and are not silently rewritten.

## 2. Provenance categories

- **DECLARATIVE:** copied from the Challenge Definition (Capa 0).
- **RUNTIME:** emitted by Godot simulation/runtime telemetry.
- **ARTIFACT:** measured from the physical encoded output with FFprobe/file inspection.
- **DERIVED:** consolidated by the Python production factory.

The factory MUST NOT invent, infer or default missing Capa 0 provenance fields.

## 3. Unit manifest contract — `manifest_version = "1.0"`

A canonical unit manifest is stored at:

```text
output/CHALLENGE_XXX/CHALLENGE_XXX_manifest.json
```

Canonical structure:

```json
{
  "manifest_version": "1.0",
  "factory_version": "0.9.0",
  "challenge_id": "CHALLENGE_XXX",
  "declarative_metadata": {},
  "telemetry": {},
  "artifacts": {
    "raw_video": "CHALLENGE_XXX_raw.avi",
    "final_video": "CHALLENGE_XXX.mp4"
  },
  "validation": {},
  "status": "PASS"
}
```

### Declarative snapshot

`declarative_metadata` is an exact snapshot of the following top-level keys when present in the input JSON:

```text
schema_version
engine_version
mechanic
mechanic_version
video_profile_version
asset_family_version
```

Absent keys remain absent. The factory does not synthesize legacy metadata.

`generation.rng_version` is authoritative in Capa 0 and is echoed into runtime telemetry; it is not re-inferred by Python.

### Runtime provenance

The production telemetry currently records, among other fields:

```text
initial_seed
final_seed
seed_used
attempts
rng_version
godot_version
winning_frame_game
winning_frame
winning_time_game
winning_time
total_frames
hook_frames
game_frames
reveal_frames
cta_frames
minimum_distance
score
close_calls
winning_frame_in_valid_window
validate_only
```

### Artifact validation — C6-D4

The canonical E2E acceptance contract is challenge-specific:

```text
physical duration = configured total_frames / fps
physical frame count = configured total_frames
physical frame rate = configured fps
```

The reference profile `2 + 7 + 2 = 11 s / 660 frames @ 60 FPS` remains valid as a fixture profile, but it is no longer a global production requirement.

## 4. Batch manifest contract — `manifest_version = "1.0"`

The batch certificate is stored at:

```text
output/BATCH_MANIFEST.json
```

Its canonical top-level fields are:

```text
manifest_version
factory_version
status
godot_versions[]
rng_versions[]
summary
tchallenges[]
```

Each challenge entry contains at least:

```text
challenge_id
status
mechanic
rng_version
godot_version
manifest
```

`rng_versions[]` is an informational aggregate only. The authoritative RNG semantic is always the per-challenge `rng_version` recorded in the unit provenance.

Mixed batches are therefore valid, including:

```text
RNG 1.0 + RNG 2.0
```

without collapsing their semantics into one batch-wide version.

## 5. Version taxonomy

| Field | Meaning | Authority |
|---|---|---|
| `factory_version` | version of orchestration/packaging/validation behavior | Python factory |
| `manifest_version` | structural JSON contract of manifest files | Production contract |
| `schema_version` | declarative ChallengeDefinition schema version | Capa 0 |
| `engine_version` | historical declarative field; semantics intentionally pending | Capa 0, preserved as-is |
| `godot_version` | physical Godot runtime version | Godot telemetry |
| `rng_version` | RNG semantic version used by the challenge | Capa 0 → telemetry echo |
| `mechanic` | concrete mechanic identifier | Capa 0 |
| `mechanic_version` | version of that mechanic contract | Capa 0 |
| `video_profile_version` | declarative presentation profile version when supplied | Capa 0 |
| `asset_family_version` | declarative asset family version when supplied | Capa 0 |

`challenge_version` is explicitly not part of the 0.9.0 contract.

## 6. Legacy fixture policy

Existing frozen fixtures may have incomplete declarative metadata. This is historical debt, not permission for the factory to infer values.

Examples:

```text
CHALLENGE_005 → lacks schema/engine/video/asset-family metadata
CHALLENGE_006 → lacks schema/engine/mechanic-version/video/asset-family metadata
```

Those omissions remain omissions in the provenance snapshot until a separate Capa 0 maintenance task explicitly changes the fixtures.

## 7. Canonical artifact layout

```text
output/
├── CHALLENGE_001/
│   ├── CHALLENGE_001_raw.avi
│   ├── CHALLENGE_001.mp4
│   └── CHALLENGE_001_manifest.json
├── ...
├── CHALLENGE_006/
│   ├── CHALLENGE_006_raw.avi
│   ├── CHALLENGE_006.mp4
│   └── CHALLENGE_006_manifest.json
└── BATCH_MANIFEST.json
```

Artifact roles:

- RAW AVI: retained intermediate render product.
- MP4: canonical final distribution artifact.
- Unit manifest: canonical unit provenance certificate.
- Batch manifest: canonical batch provenance certificate.

No challenge artifact may be published directly under the root `output/` directory.

The workspace sanitizer introduced in 0.9.0 removes only legacy challenge artifacts matching the engine's known root-level artifact patterns; it does not recursively delete the output directory.

## 8. 0.9.0 acceptance evidence

Frozen evidence includes:

```text
External Python runner:
HIT_V1_ISOLATION            PASS
CATCH_V1_ISOLATION          PASS
CATCH_PRESENTATION_CONTRACT PASS

Batch:
total  = 6
passed = 6
failed = 0
workers = 2

factory_version  = 0.9.0
manifest_version = 1.0
rng_versions     = ["1.0", "2.0"]
```

The final output tree contains six challenge directories and `BATCH_MANIFEST.json` at the root, with no legacy challenge artifacts floating at root level.

## 9. Explicit non-scope

0.9.0 does not modify:

- HIT mathematics;
- CATCH mathematics;
- CATCH Presentation Contract;
- RNG algorithms;
- renderer technology;
- FFmpeg encoding model;
- global test harness architecture;
- challenge fixture JSON files.
