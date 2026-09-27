# C11-C — Longform PowerShell Parser Repair

## Scope

Overlay-only repair for:

`tools/prototypes/c11c_bulk/run_c11c_visual_loop_longform_production.ps1`

No simulation, renderer, audio engine, C7, C9, C11-B freeze, or production contract is changed.

## Repairs

1. PowerShell variable interpolation at `"$Family: ..."` is now delimited as `${Family}: ...`.
2. The social-copy longform separator is ASCII `-` instead of a raw em dash, avoiding Windows PowerShell source-encoding/parser problems.
3. The `.ps1` is stored as UTF-8 with BOM so Windows PowerShell 5.1 correctly decodes the existing Spanish/Unicode strings.

## Recovery runner

The overlay also contains `resume_c11c_full_art_direction_corpus_after_longform.ps1/.cmd`.
It reads the newest `artifacts\\batch\\full_art_direction\\...\\full_run_manifest.json`, reuses its exact five Longform seeds and five Drill seeds, and resumes at Longform production. It does not rerun the 27 Visual Loop products already completed by the interrupted run.

Use the `.cmd` wrapper on Windows so PowerShell execution-policy settings do not block the script.
