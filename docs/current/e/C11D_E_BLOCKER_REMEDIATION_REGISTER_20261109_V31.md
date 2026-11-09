# C11-D/E Blocker Remediation Register — V31 (2026-11-09)

| Blocker / gate | Current state | Resolution path |
|---|---|---|
| Loop22 AV authorization | Approved bounded TEST_ONLY scope | Retain 22 selectors × A/B; never infer renderer authority |
| Loop22 V1 PowerShell stderr integration | RESOLVED by V2 .NET process bridge | V2 bridge PASS; do not rerun V1 wrapper |
| Loop22 V1 runner directory bootstrap | ROOT CAUSE CONFIRMED: duplicate creation of shared family/repeat output paths | Install shared-directory fix overlay; V3 wrapper + runner V2; 25/25 focused tests before media |
| Loop22 failed V2 runner attempt | FAILED before first media launcher; 0 launches/outputs | Preserve evidence; no capture recovery required; rerun only after V3 all-green preflight |
| Audio delivery frequency | Resolved | Native PCM16 stereo 44.1 kHz retained; separate exact-sample PCM16 stereo 48 kHz delivery WAV; AAC-LC 192 kb/s / 48 kHz stereo |
| FFmpeg 9 decode flag | Resolved | Use `-fps_mode passthrough`; preserve H.264 via stream copy |
| Windows MAX_PATH | Guarded | Compact run ID and <=259-character path preflight across all 44 slots |
| D renderer | OFF | Remains disabled |
| D4.8 production | BLOCKED | No general activation |
| D9.10 | PREPARE_ONLY | No dispatch |
| D9.14 / D9.16 | BLOCKED | No activation |
| D9.17 | BLOCKED_NO_GO | No activation |
| D10 / release | BLOCKED_FOR_PROMOTION / NONE | No promotion or release |

## Standing execution rules

C11-C 2.19.12 and the frozen manifest are immutable. Do not repeat accepted R1P 27/27 or R1V pilot evidence. No Git checks; operator manages commits. Enforce SHA-256 pins and fail closed on any unknown preimage.
