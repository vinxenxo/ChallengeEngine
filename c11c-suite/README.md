# C11-C Suite — 0.1.4 / Active Operator Surface

`c11c-suite` is the canonical GUI/CLI operator shell for `ChallengeEngineV01_STATELESS`.

## Surfaces

- `c11c-test` — logical regression, QA and focused acceptance.
- `c11c-catalog` — artifact browsing and metadata inspection.
- `c11c-maintenance` — documentation consolidation, repository organization, cleanup and freeze packaging.
- `c11c-config` — declarative configuration inspection/editing.
- `c11c-producer` — audiovisual orchestration for Challenges, Visual Loops and Visual Drills.

## Operator parity

The Suite does not own an alternative backend. GUI actions launch the same canonical scripts used directly from the repository. During D, GUI and CLI remain co-equal orchestration surfaces.

## Current versions

- Suite application: **0.1.4**
- Producer: **0.9.7**
- C11-C baseline: **2.19.12 FROZEN**
- C11-D: **D7 FROZEN / D8.0 NEXT**
- Godot: **4.7.1 stable Mono**

## Important routing

`REVIEW_CHALLENGES` uses `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`.

Historical C11-A.1 qualification remains compatibility/regression tooling only.

## Freeze state

C11-C is immutable; D7 is frozen. D8 must add QA/release governance without changing the frozen engine boundary.

## Directory contents

### Subdirectories
- `c11c-catalog/`
- `c11c-config/`
- `c11c-maintenance/`
- `c11c-producer/`
- `c11c-test/`

### Representative files
- `common.py`
- `main.py`
- `requirements.txt`
- `run.bat`
- `self_test.py`
- `test_retro_reference_contract.bat`
- `test_retro_reference_contract.py`
