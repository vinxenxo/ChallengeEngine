# MASTER HANDOVER — C11-B Organized Repository Baseline

## Authority

The semantic baseline is the committed C11-B freeze supplied as `ChallengeEngineV01.2_C11_B_FREEZE_LATEST.zip`. The current working package is a repository-organization overlay on that frozen behavior.

## Current status

The organization is **PREPARED — PENDING USER VALIDATION**. Do not call it the new baseline until the complete runbook passes from the organized tree and the owner commits the result.

## Objective

Turn the frozen C11-B repository into a maintainable long-term codebase while preserving execution behavior, regression coverage and historical auditability.

## Non-negotiables

- No mechanic mathematics changes.
- No RNG algorithm, stream ownership or version changes.
- No canonical definition changes.
- No `SimulationResult` or winning-frame changes.
- No `RenderedFrameStream` semantic changes.
- No C7 audio-contract weakening.
- No C9 authoring-contract redesign.
- No C11-B Header/Body/Footer geometry changes.
- No test deletion to make the cleanup pass.
- No historical document rewriting into current-state documentation.

## Current canonical roots

```text
core/                  engine/runtime
challenges/            challenge source corpus
definitions/           visual definitions
profiles/              versioned profiles
assets/                source assets + references
schemas/               normative schemas
tests/                 executable test corpus
tools/                 reproducible automation
artifacts/             generated evidence
_docs/                 documentation authority
```

The actual documentation root is `docs/`; `_docs/` above is only a conceptual label and does not exist.

## Required reading

1. `docs/00_PROJECT_OVERVIEW.md`
2. `docs/01_ARCHITECTURE.md`
3. `docs/02_DATA_AND_CONTRACTS.md`
4. `docs/03_PRESENTATION.md`
5. `docs/04_REPOSITORY_STRUCTURE.md`
6. `docs/05_TESTING_AND_REGRESSION.md`
7. `docs/06_PRODUCTION_AND_DISTRIBUTION.md`
8. `docs/07_ROADMAP.md`
9. `docs/contracts/C11_ARCHITECTURE_MANIFESTO.md`
10. `docs/checkpoints/C11_FREEZE.md`
11. `docs/checkpoints/C11_B_REPOSITORY_ORGANIZATION.md`
12. `docs/operations/TEST_RUNBOOK.md`

## Validation before acceptance

```powershell
.\tools\maintenance\verify_repository_layout.ps1
.\tools\c11freeze\verify_freeze_structure.ps1
.\tools\c11freeze\run_core_suite.ps1
.\tools\c11freeze\run_c11_suite.ps1
python .\tests\run_all.py
.\tools\c11freeze\run_retrocompatibility.ps1
python .\tools\c11freeze\run_seed_stress.py --repeat 2 --retries 3
.\tools\c11freeze\run_physical_export_suite.ps1
python .\tools\c11freeze\generate_qa_video_matrix.py --include-canonical --limit 0
.\tools\c11freeze\run_qa_video_matrix.ps1
```

## After acceptance

The owner commits the organization checkpoint separately. The next session may then treat this organized tree, its commit and its generated freeze evidence as the live C11-B baseline.

## Next product scope

After acceptance, the next active scope is **C11-C Art Direction**. Reference images belong under `assets/reference/` and generated comparison renders belong under `artifacts/`.
