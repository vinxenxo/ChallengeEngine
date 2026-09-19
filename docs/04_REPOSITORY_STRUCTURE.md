# Repository Structure

This document defines the **live filesystem contract**. A path is considered live when current tests, production tools, or current documentation may depend on it.

## Top-level map

```text
ChallengeEngineV01_STATELESS/
├── project.godot                 # Godot project definition
├── README.md                     # public/current entry point
├── AGENTS.md                     # engineering operating rules
├── .gitignore                    # generated/local-state policy
├── .gitattributes
├── .editorconfig
├── GeneradorMaestro.gd           # current composition root / main generator
├── Main.tscn                     # main Godot scene
├── build_factory.py              # canonical production/batch CLI
├── release_gate.py               # release validation helper
│
├── .continue/                    # continuity rules for development tooling
├── .githooks/                    # repository hooks
├── core/                         # engine and runtime source
├── challenges/                   # canonical challenge definitions/source inputs
├── definitions/                  # canonical visual definitions
├── profiles/                     # video/audio/difficulty/runtime profiles
├── assets/                       # source-controlled assets, fonts and references
├── schemas/                      # normative data schemas
│
├── tests/                        # executable test corpus
│   ├── fixtures/                 # stable test inputs/corpora
│   ├── helpers/                  # shared path/runtime helpers
│   ├── mechanics/                # mechanic isolation tests
│   └── c11freeze/                # repository/freeze contracts
│
├── tools/
│   ├── c11freeze/                # canonical freeze/reproducibility gates
│   ├── qa/                       # checkpoint-specific QA utilities
│   └── maintenance/              # cleanup and repository maintenance
│       └── legacy/               # historical one-off maintenance scripts
│
├── artifacts/                   # generated evidence and production outputs
│   ├── production/
│   │   ├── challenges/
│   │   └── audiovisual/
│   ├── qa/
│   ├── regression/
│   ├── tests/
│   ├── releases/
│   ├── legacy/
│   └── scratch/
│
└── docs/
    ├── 00_PROJECT_OVERVIEW.md
    ├── 01_ARCHITECTURE.md
    ├── 02_DATA_AND_CONTRACTS.md
    ├── 03_PRESENTATION.md
    ├── 04_REPOSITORY_STRUCTURE.md
    ├── 05_TESTING_AND_REGRESSION.md
    ├── 06_PRODUCTION_AND_DISTRIBUTION.md
    ├── 07_ROADMAP.md
    ├── contracts/
    ├── mechanics/
    ├── operations/
    ├── checkpoints/
    ├── master-prompts/
    └── history/
```

## What belongs where

| Area | Role | Git policy |
|---|---|---|
| `core/` | runtime/engine implementation | Track |
| `challenges/` | canonical challenge inputs | Track |
| `definitions/` | canonical visual definitions | Track |
| `profiles/` | versioned runtime/production profiles | Track |
| `assets/` | source assets, fonts, owner references | Track |
| `schemas/` | normative schemas | Track |
| `tests/` | executable compatibility/regression corpus | Track |
| `tools/` | reproducible automation | Track |
| `artifacts/` | generated evidence/outputs | Mostly ignore binary media; retain manifests/reports |
| `docs/` | current contracts/process + history | Track |

## Artifact layout

Current generated evidence has one canonical root: `artifacts/`.

- `artifacts/production/` — current production outputs and audiovisual evidence.
- `artifacts/qa/` — current checkpoint evidence, seed matrices, physical smoke and video QA.
- `artifacts/regression/` — reference, comparison and retrocompatibility reports.
- `artifacts/tests/` — test logs, inventories and reports.
- `artifacts/releases/` — retained release/freeze evidence.
- `artifacts/legacy/` — superseded generated evidence retained for audit.
- `artifacts/scratch/` — disposable workspace; never a source of truth.

Binary video/image/audio artifacts are reproducible and are normally ignored by Git. Their manifests, textual reports and deterministic hashes remain the durable evidence.

## Documentation layout

`docs/00..07_*` is the authoritative current narrative. `docs/operations/` contains executable operating procedures. `docs/checkpoints/` records checkpoint status. `docs/master-prompts/` contains current continuity prompts. `docs/history/` contains superseded documents and one-off historical material.

Do not update historical documents to make them describe the current system; update the current numbered documentation instead.

## References and source assets

`assets/reference/` is reserved for owner-supplied art-direction references and other intentionally version-controlled source material. Generated comparisons, contact sheets and rendered candidates belong under `artifacts/`, not beside the references.

## Retired roots

The following roots are prohibited in the live repository:

```text
output/
output_c7/
output_batch_audit/
qa/
export/
c9_c_generated_configs/
c9_g_generated_configs/
scripts/
```

A historical copy may exist only below an explicitly named historical area such as `artifacts/legacy/` or `docs/history/`.

## Safety rule for reorganization

A move is acceptable only when all executable references are updated and the full test runbook still passes. Never infer that an old file is disposable solely from its age or name.
