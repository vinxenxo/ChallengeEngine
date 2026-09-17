# C11-A.1 Challenge Seed Qualification — Delivery Package

This package adds only the QA harness. It does not modify the simulation core, RNG, mechanics, authoring contracts or renderers.

## Install

Copy the package contents into the project root, preserving `tools/` and `docs/`.

## Run

From the project root:

```powershell
.\tools\run_c11a1_challenge_bulk_qa.ps1
```

This performs 54 sequential, isolated executions so GPU/Movie Maker processes do not race each other. It writes only under:

```text
qa/c11a1_challenge_qa/
```

Never under the historical root `output/`.

## Resume behavior

The runner refuses to overwrite an existing run directory. `-Resume` skips runs already marked `COMPLETE` and retries runs marked `RUNNING` or `FAILED`, removing only that incomplete run directory before starting it again.

## Finalize

After all 54 runs:

```powershell
.\tools\finalize_c11a1_challenge_bulk_qa.ps1
```

The finalizer never invokes Godot or FFmpeg to re-render. It only audits existing evidence, verifies the technical gate and compares A/B pairs.

Expected success marker:

```text
[C11A1] Manifest finalized: technical=54/54, determinism_ab_pass=True
```

## Output

```text
qa/c11a1_challenge_qa/
├── C11A1_CHALLENGE_BULK_PLAN.json
├── C11A1_CHALLENGE_BULK_MANIFEST.json
└── runs/
    ├── challenge_001_seed_12345_A/
    ├── ...
    └── challenge_009_seed_12345_B/
```

Every run contains the QA definition copy, factory stdout/stderr, factory manifest, telemetry, simulation summary, AVI/MP4, frame digest, review frames and contact sheet.
