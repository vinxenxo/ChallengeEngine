# C11-E Gates Acceptance Matrix — V96

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
| Integrated R1V A/V wrapper test gate | PASS 52/52 | Active Windows run `R1V_AV_WRAPPER_V1_20261108_003543_5D7E5320`; 0 errors/failures/skips; lineage test now passes |
| Integrated A/V tests | WINDOWS PASS 52/52 | Isolated V84 reconstruction: 52 tests, 0 errors/failures, 1 expected Linux-only skip; active Windows: 52/52, zero skips/errors/failures |
| Five-family A/V capture | FAIL_CLOSED before new launch | Prior Fractal A reused; FFprobe audit sidecar path exceeded MAX_PATH; 0 new launchers, 0 WAV generations, 0 muxes, 0 completed A/V outputs |
| Remaining 22 Loop variants | PENDING | Separate expansion only after 5-family A/V and human visual/audio review |
| Option C D compositor | NOT IMPLEMENTED | Static handoff only |
| General D4.8 production activation | BLOCKED | Production policy remains DISABLED; runtime authority NONE |
| D9.10 | PREPARE_ONLY | No dispatch |
| D9.14 / D9.16 | BLOCKED | Not accepted |
| D9.17 | BLOCKED_NO_GO | Not accepted |
| D10 / release | BLOCKED_FOR_PROMOTION / NONE | No production authority |

C11-C 2.19.12 and frozen manifest remain unchanged. R1V A/V qualification is bounded test authority only.


## Historical Windows execution evidence — V1.1

| Gate | State | Evidence / boundary |
|---|---|---|
| V1.1 add-only installer | PASS_ADD_ONLY_INSTALL | 21/21; install receipt SHA `256b774a5e45763e56d22c6583c637e53515813678b5e7dbab53b124b71e6b00`; frozen manifest unchanged |
| V1.1 integrated 52-test wrapper | HISTORICAL FAIL_CLOSED | 52 run; 1 error; 0 failures; 0 skips; resolved by V2 lineage correction |
| R1V A/V launchers | NOT STARTED | wrapper receipt explicitly says no launcher started; capture exit code null |
| Prior Fractal A | REUSE SOURCE ACCEPTED; lineage validator correction pending | Existing MP4/report/process hashes verified; correct field mapping is documented in V17/V96 |
| Lineage schema correction V2 | PASS_INSTALLED | 12/12; active Windows test_20 passes; receipt SHA `b635b3dbcc9ddc6f1bae0c3362ddbe2aea5723ff79ddcc3f06ff2d0367479bd5` |

V1.0 located in Library is not installed in the local checkout and is not part of this execution chain. No capture/audio/mux scope change is introduced by the correction.


## Lineage-fix installer recovery

| Gate | State | Evidence / boundary |
|---|---|---|
| Lineage-fix installer V1 | FAIL_PREFLIGHT_NO_CHANGES | First missing successor doc V17 was incorrectly classified PINNED_REPLACE; no payload applied |
| Lineage-fix installer V2 | PASS_INSTALLED | 12/12; receipt SHA `b635b3dbcc9ddc6f1bae0c3362ddbe2aea5723ff79ddcc3f06ff2d0367479bd5` |
| Corrected integrated wrapper tests | PASS 52/52 | Active Windows wrapper `R1V_AV_WRAPPER_V1_20261108_003543_5D7E5320`; 0 skips/errors/failures |

The V1.0 Library package is not installed locally and is not a dependency. No A/V capture has started.


## Current active correction

| Gate | State | Evidence / boundary |
|---|---|---|
| Windows path-budget implementation V1 with corrected installer package V2 | PREPARED | Compact 16-character run ID; preflight all 140 planned artifact paths; exact max 257 chars; reject >259 before creating outputs or launching processes |
| R1V A/V integrated outputs | PENDING | Rerun wrapper only after path-budget fix installer PASS; do not rerun R1P, Option C or prior Fractal A |


| Windows path-budget installer package V1 | FAIL_CLOSED_PRE_FLIGHT | Malformed 65-character expected receipt SHA; no staging/apply |
| Windows path-budget installer package V2 | PREPARED | Corrected receipt pin + manifest-wide 64-hex SHA validation; await active install |
