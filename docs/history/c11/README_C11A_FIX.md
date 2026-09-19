# C11-A implementation fix

This package contains:

- `tests/C11ABulkEnvelopeGenerator.gd`: 9x6 envelope generation, now isolated under `qa/c11a_visual_qa`.
- `tools/run_c11a_visual_bulk_qa.ps1`: corrected C11-A runner. Godot invocations use `Start-Process -Wait` so Phase 2 cannot race Phase 1; Movie Maker remains graphical/no `--headless`.
- `tools/clean_c10_generated_outputs.ps1`: safe cleanup of known stale generated artifacts from the C10 freeze. Default mode is dry-run; use `-Apply` to delete.

The cleanup script preserves `output/c10c_e2e`, `output_batch_audit`, `output_c7`, and `export`.
