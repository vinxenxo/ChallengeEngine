# C11-C Studio — Build Notes v0.2.3

Patch release for a Qt runtime defect discovered during first Windows launch.

## Fixed
- `LogView` no longer calls the nonexistent `QPlainTextEdit.setFontFamily()` API.
- Consolas is applied through the widget font object (`QFont`), preserving behavior without backend/toolchain changes.

## Validation
- Embedded source extraction: PASS
- Python compileall: PASS
- Pure self-test: expected PASS

This release does not modify the frozen C11-B core or canonical C11-C toolchain.
