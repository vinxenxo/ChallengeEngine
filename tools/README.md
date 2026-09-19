# Tools Map

## Freeze and certification

`tools/c11freeze/` contains the canonical checkpoint/release gates: core suite, C11 suite, retrocompatibility, seed stress, physical export and video matrix.

## QA helpers

- `tools/qa/c7/` — C7-specific fixtures and policies.
- `tools/qa/c10/` — C10 physical export smoke.
- `tools/qa/c11/` — C11 qualification, framing and visibility utilities.

## Maintenance

`tools/maintenance/` contains routine repository maintenance. `tools/maintenance/legacy/` contains one-off historical scripts and is not part of the normal execution path.

New production or QA automation should have one canonical location and one documented artifact output root.
