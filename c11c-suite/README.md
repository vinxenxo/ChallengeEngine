# C11-C Suite — 0.1.4 / Active Operator Surface

`c11c-suite` is the canonical GUI/CLI operator shell for `ChallengeEngineV01_STATELESS`.

## Surfaces

- `c11c-test` — logical regression, QA and focused acceptance.
- `c11c-catalog` — artifact browsing and metadata inspection; version 0.2.0 adds receipt-driven C11-D product/provenance/replay records.
- `c11c-maintenance` — documentation consolidation, repository organization, cleanup and freeze packaging.
- `c11c-config` — declarative configuration inspection/editing; 0.2.0 adds read-only D2–D9 contract governance and explicit C11-D operator profiles with validation, hash/diff and backup/restore.
- `c11c-producer` — audiovisual orchestration for Challenges, Visual Loops and Visual Drills.

## Producer 0.10.0

The existing Producer retains all C11-C Challenges/Loops/Drills workflows and adds a C11-D Production Request + Personalization tab using canonical D4.6/D4.5 planning adapters. It validates GUI/CLI parity and records plan evidence; D4.8 remains BLOCKED, so this tab does not render or create release products. No sixth suite is introduced.

## Operator parity

The Suite does not own an alternative backend. GUI actions launch the same canonical scripts used directly from the repository. During D, GUI and CLI remain co-equal orchestration surfaces.

## Current versions

- Suite application: **0.1.4**
- Producer: **0.10.0**
- Catalog: **0.2.0** (D9.6 Windows GUI confirmed by operator)
- Config: **0.2.0** (D9.7 overlay prepared; Windows GUI acceptance pending)
- C11-C baseline: **2.19.12 FROZEN**
- C11-D: **D0–D8 CLOSED · D9 ACTIVE · D9.4 CHECKPOINT PASS · D9.5.1 Producer plan GUI PASS · D9.6 Catalog GUI PASS · D9.7 Config 0.2.0 pending Windows GUI · D10 BLOCKED**
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


## Config 0.2.0 — D9.7

The existing Config GUI now exposes read-only D2–D9 canonical registry/policy inspection and a dedicated, validated C11-D Operator Profiles workflow. Generic Repository Config cannot write under challenges, definitions, schemas, assets, core, tools, tests, c11c-suite or any profiles path. Only the dedicated tab writes `profiles/c11d/operator/*.json`, with explicit confirmation, schema validation, hash/diff, `.bak` and validated restore. Profiles are not yet auto-fed into Producer; execution/release remain disabled. Windows Qt/filesystem acceptance is still pending.
