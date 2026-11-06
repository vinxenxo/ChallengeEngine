# C11-E E4A.7 D-Composited Challenge A/V — Post-Run Review V1

**Date:** 2026-11-06

## Wrapper evidence inspected

Library artifact `C11E_E4A7_D_COMPOSITED_CHALLENGE_AV.zip`, 47,068 bytes, SHA-256 `2a2c7be634e0d74d12b91f1ab74f850910f4d5dc77f545bda981903f06bd38ee`. ZIP CRC passed. It contains the embedded Python worker (43,974 bytes; SHA `52c20df87dcca747295a2c513cded1e43bdf06740b24a115c9ce71f5aedbc238`), embedded docs archive (31,777 bytes; SHA `25d9b66c1ac31291e9454f766cd5042ea55ba87e1c41c9499096543e10399f03`), wrapper JSON receipt, stdout, empty stderr and worker exit-code `0`. Wrapper receipt says `exit_code=0`, `timed_out=false`, stdout 872 bytes, stderr 0. The stdout contains all expected stages and final `PASS_TEST_ONLY_D3V5_D33_MUX` marker.

The worker code was inspected. It checks Recovery V1.2 receipt/MP4/stills/pixel audit, source pins, three sealed E1 TEST intents, D3 V5 raw-repeatability/music-seed difference, D3.3 30-second mastering/mono QA, 15-second PCM masters, three AAC muxes, FFprobe cardinality/codec/rate/layout/frame/duration/start/end drift, source H.264 bitstream identity and decoded AAC A/B equality/C difference. The final PASS marker occurs only after it writes the report/receipt and child ZIP.

## Missing child archive

The wrapper archive does **not** include the detailed worker-created ZIP. Stdout reports:

- `RUN_20261106T070808Z-62F31F9C.zip`
- Expected SHA-256 `ad4024cc6caa3b9140a284390b852c76f3dcd5d50d88cf03813d6bb4e374d293`
- Worker receipt SHA-256 `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`

The missing ZIP should be at `artifacts/tests/c11e/e4a_d_composited_av_review/RUN_20261106T070808Z-62F31F9C.zip`. Request it for independent verification. Until supplied, do not copy numeric QA measurements into the authority record.

## E4A.7 status

- Runtime worker: PASS reported by wrapper (exit 0 + final PASS marker).
- Child archive / exact receipts / media audit: pending upload.
- Operator listening A/B/C: pending.
- E1 GUI/CLI parity: pending.
- Full E4A: remains IN_PROGRESS.

## Packaging incident / prevention

The operator-facing wrapper package was created without the child ZIP despite printing its path/hash. This is not an audio/render failure. Future wrapper packaging must include and re-hash the child archive or explicitly ask for it as a separate upload. See PowerShell Runner Style Guide V5.
