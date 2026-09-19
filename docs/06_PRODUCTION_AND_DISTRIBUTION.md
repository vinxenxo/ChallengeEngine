# Production and Distribution

## Canonical production pipeline

```text
canonical definition
    ↓
authoring / contract validation
    ↓
deterministic runtime
    ↓
passive presentation
    ↓
Godot Movie Maker
    ↓
AVI
    ↓
FFmpeg
    ↓
MP4
    ↓
FFprobe + manifest
    ↓
release gate
```

`build_factory.py` is the canonical production CLI. Its normal output root is `artifacts/production/challenges`.

## Artifact policy

- `artifacts/production/challenges/`: challenge production outputs.
- `artifacts/production/audiovisual/`: C7 audiovisual/audio evidence.
- `artifacts/qa/`: C10/C11 QA runs, manifests and regression inputs.
- `artifacts/regression/`: baselines, comparisons and freeze reports.
- `artifacts/tests/`: test logs/reports.
- `artifacts/releases/`: retained release/freeze packages and certificates.
- `artifacts/legacy/`: historical outputs preserved for audit only.
- `artifacts/scratch/`: disposable local work.

## Physical rendering

The physical contract uses Godot 4.7.1 with the graphical Compatibility renderer and Movie Maker. Headless Godot is appropriate for logical validation, fixture preparation and contract suites; it is not a replacement for the physical export path.

## Release readiness

Before a production release, the repository must have:

1. a known source/configuration snapshot;
2. green logical and deterministic regression;
3. required physical export evidence;
4. valid manifests/provenance;
5. reproducible production commands;
6. documented recovery/rollback behavior;
7. no unresolved contract drift.

## Roadmap to production

C11-C defines and validates the visual language. C11-D locks final export profiles, production media QA and release-candidate outputs. C11-E establishes distribution metadata, packaging and final operational procedures.
