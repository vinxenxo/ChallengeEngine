# C11-E Gates Acceptance Matrix — V97
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

## Latest Windows R1V execution — FFmpeg 9 decode compatibility (2026-11-08)

- Path-budget correction V2 installed PASS: 13/13 payloads; install receipt SHA `f57999151f94f378d08290b15bd30586a2180f855e280ef96b2ff4056b1decc5`.
- Active Windows integrated wrapper `R1V_AV_WRAPPER_V1_20261108_012250_5CC5EFEF` passed 52/52, zero skips/errors/failures; wrapper receipt SHA `f8149461d80029bacbf8aa3ddb59ad33ee75246e5225c176a3190063594380b0`.
- A/V preflight passed with the compact run ID and 257-character max path. It reused the accepted Fractal Bloom A MP4; FFprobe found 660 frames at 720x1280/30 and 22 seconds.
- Run `Q5_022257_316922` failed closed in the in-memory pixel decoder because the host is FFmpeg 9.0 and the code still supplied removed `-vsync 0`. Decoder stderr: `Unrecognized option 'vsync'. Error splitting the argument list: Option not found`.
- No new launcher, music generation, mux or A/V output was started/completed (0/0/0/0). The source MP4 remains pinned/unchanged. Full incident record: `C11E_R1V_FFMPEG9_PIXEL_DECODE_COMPATIBILITY_CORRECTION_20261108_V1.md`.
- Corrective code V1 replaces only `-vsync 0` with `-fps_mode passthrough`, retains rawvideo pipe-to-memory and exact frame hashing, and extends the existing test_04 without changing the combined 52-test count. Error diagnostics now include FFmpeg stderr and decoded/expected frame counts.
- Next step: install the FFmpeg9 pixel-decode fix V1 after exact receipt/evidence/predecessor preflight, then run the same integrated wrapper once. Do not repeat accepted 52-test work manually, R1P, Option C, or Fractal A. No separate silent-only stage.



## R1V latest active status — 2026-11-08

| Gate | State | Evidence / disposition |
|---|---|---|
| V1.1 A/V overlay install | PASS | 21/21; receipt SHA `256b774a5e45763e56d22c6583c637e53515813678e7dbab53b124b71e6b00` |
| Lineage fix V2 install | PASS | 12/12; receipt SHA `b635b3dbcc9ddc6f1bae0c3362ddbe2aea5723ff79ddcc3f06ff2d0367479bd5` |
| Path-budget fix V2 install | PASS | 13/13; receipt SHA `f57999151f94f378d08290b15bd30586a2180f855e280ef96b2ff4056b1decc5` |
| Active Windows combined tests | PASS | 52/52; 0 errors, 0 failures, 0 skips |
| Compact path budget | PASS | 140 paths preflighted; maximum 257 chars |
| Accepted Fractal A reuse | PASS | Existing MP4 SHA pinned; no rerender |
| FFmpeg 9 in-memory pixel decode | BLOCKED | Legacy `-vsync 0` rejected by FFmpeg 9.0; no new launcher/audio/mux |
| FFmpeg9 decode fix V1 | PREPARED | `-fps_mode passthrough`; existing test_04 assertion; Windows install/re-run pending |
| R1V ten integrated A/V outputs | PENDING | Not started; no output completion |
| Human visual/layer/audio review | PENDING | Starts only after technical 10/10 |

## Latest operator execution checkpoint — 2026-11-08 (authoritative; supersedes prior next-step text)

- Active checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. V1.1 A/V overlay PASS 21/21; lineage correction V2 PASS 12/12; path-budget correction V2 PASS 13/13. Latest path-budget install receipt SHA-256: `f57999151f94f378d08290b15bd30586a2180f855e280ef96b2ff4056b1decc5`. Frozen C11-C manifest remains `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Active Windows wrapper `R1V_AV_WRAPPER_V1_20261108_012250_5CC5EFEF` passed the combined gate: 52/52, zero skips, errors or failures. Receipt SHA-256: `f8149461d80029bacbf8aa3ddb59ad33ee75246e5225c176a3190063594380b0`.
- A/V run `Q5_022257_316922` passed preflight, reused the accepted Fractal Bloom A, then failed closed during in-memory pixel decoding. Report SHA-256 `67759765d0c4d55737b3480d1d54f56e9b878dde75f2e462225bbc57f5412a70`; process receipt SHA-256 `f904e08edac76d07f5324b88937c71b0104ea1db18201d12154e6ec7df4ec74b`.
- Exact FFmpeg 9.0 stderr: `Unrecognized option 'vsync'. Error splitting the argument list: Option not found`. No new C11-C launcher, WAV generation, AAC mux or completed A/V output occurred. The existing Fractal A source and its MP4 hash remain unchanged.
- Root cause: FFmpeg 9 removed legacy `-vsync`; the compatible per-output video sync option is `-fps_mode passthrough`. The correction preserves in-memory rawvideo pipe decoding, 660-frame identity accounting, and the no-frame-files policy. A local FFmpeg 7.1.5 reproduction returned all 660 frames / 912,384,000 bytes; Windows FFmpeg 9 confirmation remains pending.
- **Current next action:** install `C11E_R1V_FFMPEG9_PIXEL_DECODE_FIX_V1_20261108.zip` from a fresh Downloads folder, then run the existing integrated wrapper once. Do not reinstall V1.1, lineage V2 or path-budget V2; do not rerun R1P, Option C or Fractal A.
- No silent-only intermediate stage. Renderer OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.

