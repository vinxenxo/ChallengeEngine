# C11-C Suite — 0.1.4

`c11c-suite` is the canonical GUI/CLI operator shell for `ChallengeEngineV01_STATELESS`.

## Surfaces

- `c11c-test` — logical regression, QA and focused acceptance operations.
- `c11c-catalog` — artifact browsing and metadata inspection.
- `c11c-maintenance` — documentation consolidation, repository organization, safe cleanup, checks and freeze packaging.
- `c11c-config` — declarative configuration inspection/editing.
- `c11c-producer` — audiovisual orchestration for Challenges, Visual Loops and Visual Drills.

## Operator parity

The Suite does not own an alternative backend. GUI actions launch the same canonical scripts used directly from the repository root. During D, GUI and CLI may be used concurrently for authoring and verification without creating a second logic path.

## Current versions

- Suite application: **0.1.4**.
- Producer: **0.9.7**.
- C11-C baseline: **2.19.12**.
- Godot: **4.7.1 stable Mono**.

The `C11C_SUITE_CURRENT_RULES.md` document is the current rules authority; the former version-labelled rules file is historical evidence.

## Important routing

`REVIEW_CHALLENGES` uses `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`.

Historical C11-A.1 qualification remains available only as explicit compatibility/regression tooling.

## Freeze

The sole C11-C freeze authority is `tools/maintenance/create_c11c_freeze_zip.ps1`, exposed by:

`c11c-suite/c11c-maintenance/run_freeze_package.bat`
