# C11-D/E Blocker Remediation Register — V29 (2026-11-09)

| Blocker / gate | Current state | Resolution path |
|---|---|---|
| Loop22 AV authorization | Approved in bounded operator conversation | New independent 22×2 TEST_ONLY amendment; not borrowed from the 5-selector R1V permission |
| Audio delivery frequency | Resolved | Preserve native PCM16 44.1 kHz; create separate exact-sample PCM16 48 kHz delivery copy; AAC-LC 192 kb/s/48 kHz stereo |
| FFmpeg 9 decode flag | Resolved in package | Use `-fps_mode passthrough`, not legacy `-vsync 0` |
| Windows MAX_PATH | Guarded | Compact run ID, path-budget preflight across all 44 slots |
| D renderer | OFF | Remains disabled |
| D4.8 production | BLOCKED | No general activation |
| D9.10 | PREPARE_ONLY | No dispatch |
| D10 / release | BLOCKED_FOR_PROMOTION / NONE | No promotion/release |
