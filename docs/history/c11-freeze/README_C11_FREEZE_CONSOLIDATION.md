# C11 Freeze Consolidation — Repository Order & Regression Hardening

## Objective

This package is the consolidation layer before C11-C Art Direction.
It does not change simulation mathematics, RNG, SimulationResult, winning_frame, frozen challenge definitions or visual-family maths.

It establishes:

- one canonical artifact root: `artifacts/`;
- a documented split between canonical production, QA evidence, regression reports and legacy evidence;
- deterministic seed corpora for repeatable random-seed stress tests;
- a retrocompatibility runner for CHALLENGE_001..009;
- a QA-video config generator that replaces generic CTA/link text with run-specific diagnostics;
- a repository inventory and output migration tool with dry-run/apply modes;
- a long-term documentation index and freeze checklist.

## Safety model

Migration is non-destructive by default. `migrate_artifacts.ps1` starts in dry-run mode and can copy historical evidence into `artifacts/legacy/` before any deletion is considered.

Do not delete `output/`, `export/`, `output_c7/`, `output_batch_audit/` or historical production folders until retrocompatibility and artifact indexing have passed.

## Target artifact layout

```text
artifacts/
├── production/
│   ├── challenges/
│   └── audiovisual/
├── qa/
│   ├── c11a_visual/
│   ├── c11a1_challenge/
│   ├── c11b_visibility/
│   ├── seed_stress/
│   └── video_matrix/
├── regression/
│   ├── baselines/
│   ├── runs/
│   └── reports/
├── tests/
│   ├── logs/
│   └── reports/
├── scratch/
└── legacy/
    └── <original-root-folder>/...
```

## Recommended execution order

1. `tools/c11freeze/inventory_repository.ps1`
2. `tools/c11freeze/generate_seed_corpus.py`
3. `tools/c11freeze/migrate_artifacts.ps1` (dry-run)
4. `tools/c11freeze/run_test_suite.ps1`
5. `tools/c11freeze/run_retrocompatibility.ps1`
6. `tools/c11freeze/generate_qa_video_configs.py`
7. `tools/c11freeze/run_qa_video_matrix.ps1`
8. review reports
9. only then perform the physical repository migration/freeze

## Current known baseline debt

The current `tests/run_all.py` evidence contains seven known failures unrelated to C11-B presentation success:

- C6F06 visual physical-export tests expect obsolete root `output/*.avi` artifacts;
- C6F2AdapterMetadataBindingTest has a test-side `%` formatting failure;
- C6F2ProductiveGeneratorTest has contract drift around productive metadata/pilot/hit paths;
- C6F3PresentationBindingTest has presentation-family metadata drift;
- C9E/C9F productive authoring tests require output-config wiring.

These must be classified and repaired before the final C11 freeze, but they are not reasons to alter frozen simulation families.
