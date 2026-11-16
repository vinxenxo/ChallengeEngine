# C11E E4C Peripheral Scan Qualification Plan — V6 (2026-11-16)

## Current checkpoint

Peripheral Scan is the sole E4C family pending, 0/5. Tracking, Pursuit and Saccade are accepted 5/5; E4C is 15/20.

## Native family contract

- Family `peripheral_scan`; selectors `peripheral_scan/tier-1..tier-5`; profile `ORBITAL_RITUAL`.
- Canonical SHA `aaf50f9223bad678df15589110dfcd6ff42dda89326a0a84bc5a5f51d133a904`.
- Native gameplay 510 frames/17 seconds/30fps; presentation PRE_ROLL 90 + GAME 510 + END_CTA 90 =690 frames/23 seconds.
- Five independent one-shot tiers. No tier output or receipt is recovered from Tracking, Pursuit or Saccade.
- Runtime source pins 38/38; each tier proves three equal physical 91-file inventories at pre-execution, immediately-before-renderer and post-execution.
- H.264 High 720x1280 yuv420p TV 30fps/690 frames; AAC-LC 48kHz stereo; zero A/V start drift; A/B same-seed music identical; C changed-seed music distinct; A/C video bitstreams identical.

## One-overlay install + execute

Use `C11E_E4C_PERIPHERAL_SCAN_COMBINED_OVERLAY_V2_20261116.zip` in Windows PowerShell 5.1 with `-ExecuteBatch`. The one installer invocation verifies exact ZIP/manifest/payload inventory, PowerShell AST 4/4, atomic helper/JSON writer, 51 Python tests, atomic I/O 7/7, 38 source pins and frozen C11-C manifest; it stages and runs PREPARE_ONLY, commits exactly 21 ADD_ONLY files, verifies postimages/pins, and persists immutable install receipt/journal. It then launches the installed runner exactly once, which generates the BatchId after collision checks. No separate runner command and no caller-supplied BatchId.

Successful launch yields `BATCH_LAUNCH_RECEIPT.json`, BATCH_RESULT and acyclic `COMBINED_EXECUTION_RECEIPT.json` binding package, install receipt, journal, launch receipt and BATCH_RESULT by SHA-256. Batch failure after install commit preserves the installation and one-shot evidence; never auto-retry a reserved ID.

## Operator acceptance

A 5/5 technical result remains pending operator review. Inspect every final_A/final_C video and A/B/C audio, then approve layout, typography, title role, editorial, identity, music identity and A/B/C behavior. Only after explicit approval does Peripheral Scan become 5/5 and E4C reach 20/20. E5 remains blocked until then.
