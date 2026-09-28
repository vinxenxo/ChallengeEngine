# C11-C Producer 0.9.1 — Current State

## Hotfix

Producer 0.9.1 is a corrective overlay on the 0.9.0 / 2.18.0 GUI stabilization state.

- Fixed the runtime `NameError: name 'QFrame' is not defined` in `c11c-producer/main.py`.
- Fixed the Producer `self_test.py` ordering defect where `drill_text` was used before assignment.
- Added a consolidated console test guide in `docs/current/producer/C11C_PRODUCER_0.9.1_CONSOLE_TEST_COMMANDS.md`.

## UI state retained

- No visible banner/header.
- No visible help/advice paragraphs.
- Dark cyberpunk cyan/magenta palette.
- Variation parameters use slider + `ALEATORIO` checkbox.
- Selected queue row has strong highlighting.
- Completed rows remain visible and are dimmed.
- Existing matching manual-seed products are marked `YA PRODUCIDO` and skipped unless `FORCE`.

## Production boundary

The GUI remains orchestration only. No Challenge mechanics, RNG ownership, simulation truth, canonical rendering logic or C11-B logical 540×960 geometry is changed.
