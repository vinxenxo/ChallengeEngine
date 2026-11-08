# C11-E Gates Acceptance Matrix — V94

| Gate | State | Evidence / boundary |
|---|---|---|
| E4A GUI/CLI parity | PASS_TEST_ONLY | D99 GUI fixture; do not repeat |
| E4B static family mapping | PASS | 5/5 families, 27/27 selectors |
| E4B R1P parameter payloads | CLOSED PASS | 27/27 receipts, 30/30 source pins |
| Option C handoff | PASS PREPARE_ONLY | 27/27 handoffs, 33/33 pins; D compositor not implemented |
| R1V Fractal Bloom A source | Source capture PASS; human visual PASS | launcher exit 0, H.264 720x1280/30, 660 frames, silent source SHA `7971...f659`; operator confirms visual/layers |
| R1V prior V3 wrapper | FAIL_CLOSED false-negative | Godot UTF-16 `×` log parser and `yuvj420p/pc` check mismatch; only one successful capture; no inventory in old run |
| R1V A/V scope amendment | APPROVED bounded | Five selectors × A/B; native C11-C FAMILY_MUSIC_V4; 10 A/V outputs; 9 new launchers + 1 reused source |
| Integrated R1V A/V installer | PASS_ADD_ONLY_INSTALL (V1.1 Windows) | PowerShell-only preflight/add-only; new policy is read from package payload; no Python/tests/process invocation; semantic parent-receipt schema checks |
| Integrated R1V A/V wrapper | FAIL_CLOSED before launch | One direct Python 3.13 resolution; combined 52-test suite once; requires zero skips/failures/errors; then integrated runner |
| Integrated A/V tests | WINDOWS: 52 run, 1 error, 0 failures, 0 skips | Isolated V84 reconstruction, 0 failures/errors; Windows wrapper must report 52 tests and 0 skips |
| Five-family A/V capture | NOT STARTED | wrapper receipt proves capture_exit_code=null and zero launchers |
| Remaining 22 Loop variants | PENDING | Separate expansion only after 5-family A/V and human visual/audio review |
| Option C D compositor | NOT IMPLEMENTED | Static handoff only |
| General D4.8 production activation | BLOCKED | Production policy remains DISABLED; runtime authority NONE |
| D9.10 | PREPARE_ONLY | No dispatch |
| D9.14 / D9.16 | BLOCKED | Not accepted |
| D9.17 | BLOCKED_NO_GO | Not accepted |
| D10 / release | BLOCKED_FOR_PROMOTION / NONE | No production authority |

C11-C 2.19.12 and frozen manifest remain unchanged. R1V A/V qualification is bounded test authority only.


## Windows execution evidence — V1.1

| Gate | State | Evidence / boundary |
|---|---|---|
| V1.1 add-only installer | PASS_ADD_ONLY_INSTALL | 21/21; install receipt SHA `256b774a5e45763e56d22c6583c637e53515813678b5e7dbab53b124b71e6b00`; frozen manifest unchanged |
| V1.1 integrated 52-test wrapper | FAIL_CLOSED before launch | 52 run; 1 error; 0 failures; 0 skips; `test_20` queried an absent prior-report JSON field |
| R1V A/V launchers | NOT STARTED | wrapper receipt explicitly says no launcher started; capture exit code null |
| Prior Fractal A | REUSE SOURCE ACCEPTED; lineage validator correction pending | Existing MP4/report/process hashes verified; correct field mapping is documented in V17/V96 |
| Lineage schema correction | PREPARED | Source-pinned module replacement only for behavior; docs/prompts refreshed; rerun same wrapper once |

V1.0 located in Library is not installed in the local checkout and is not part of this execution chain. No capture/audio/mux scope change is introduced by the correction.


## Lineage-fix installer recovery

| Gate | State | Evidence / boundary |
|---|---|---|
| Lineage-fix installer V1 | FAIL_PREFLIGHT_NO_CHANGES | First missing successor doc V17 was incorrectly classified PINNED_REPLACE; no payload applied |
| Lineage-fix installer V2 | PREPARED | Versioned docs are ADD; ten V1.1 predecessor paths/hashes pinned; sole code file is same-path PINNED_REPLACE; full staging before apply |
| Corrected integrated wrapper | NOT RERUN | Run once only after V2 installer PASS; requires 52/52 and zero skips/errors/failures |

The V1.0 Library package is not installed locally and is not a dependency. No A/V capture has started.
