# Generated Artifacts

`artifacts/` is the only canonical root for generated outputs and evidence.

- `production/` — generated production exports.
- `qa/` — repeatable QA evidence and manifests.
- `regression/` — reference comparisons and freeze reports.
- `tests/` — test logs, inventories and test-generated JSON.
- `releases/` — retained package/checkpoint evidence.
- `legacy/` — historical generated evidence migrated out of the live path.
- `scratch/` — disposable local workspace and ignored by Git.

Binary media is deliberately ignored by Git and can be regenerated from the corresponding definitions/manifests.
