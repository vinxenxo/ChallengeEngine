# Repository Organization Policy

## Objective

Keep the active repository small, obvious, reproducible and auditable without deleting regression coverage or useful history.

## Canonical ownership

| Content | Canonical location |
|---|---|
| Engine/runtime | `core/` |
| Challenge inputs | `challenges/` |
| Visual definitions | `definitions/` |
| Profiles | `profiles/` |
| Source/reference assets | `assets/` |
| Schemas | `schemas/` |
| Tests | `tests/` |
| Automation | `tools/` |
| Generated evidence | `artifacts/` |
| Current documentation | `docs/` |
| Historical documentation | `docs/history/` |

Every new generated output must have exactly one canonical owner and one documented cleanup/recovery strategy.

## Reorganization rules

1. Never move a file without checking executable references.
2. Never remove a test or fixture because its name appears old.
3. Update paths together with the owning test/tool.
4. Keep compatibility fixtures in `tests/fixtures/`.
5. Keep generated output below `artifacts/`.
6. Keep historical material explicitly outside active execution paths.
7. Do not reintroduce retired roots.
8. Do not change deterministic simulation semantics as part of a path cleanup.

## Retired roots

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

Historical copies may exist below `artifacts/legacy/` or `docs/history/` but are not active paths.

## Applying this organization to an existing Git checkout

The recommended procedure is to create a dedicated branch from the committed C11-B freeze and replace the working tree contents while preserving `.git/`.

```powershell
git status --short
git switch -c chore/c11b-repository-organization
```

The organization package should be extracted outside the repository first. Then, from the repository root, close Godot and replace all working-tree content except `.git/`. This is intentionally destructive to obsolete local generated folders, so the committed C11-B freeze is the rollback point.

After replacement, run `tools/maintenance/verify_repository_layout.ps1` before any commit.

## Acceptance

This checkpoint is accepted only when:

- the repository layout verifier passes;
- the C11 freeze repository contract passes;
- the complete logical and checkpoint runbook passes;
- no retired active root remains;
- `git diff` contains only intended path/documentation/test-helper changes;
- the owner commits the organization separately from the C11 semantic freeze.
