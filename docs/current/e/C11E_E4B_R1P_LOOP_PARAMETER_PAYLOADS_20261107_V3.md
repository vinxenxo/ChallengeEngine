# E4B R1P — Loop Family Parameter Payloads V3

**Date:** 2026-11-07  
**State:** `PASS_R1P_PARAMETER_PAYLOADS_27_OF_27`; original ZIP assertion false-negative; archive recovery pending active-checkout receipt.

## Execution result

Run ID: `E4B_R1P_20261107_032743_5F75045C`.

The preserved aggregate report has status `PASS_R1P_PARAMETER_PAYLOADS_27_OF_27` and canonical SHA-256 `9e09940c7a915d1533a2ba0a97765626f5c5d8533c870cda27012d4d90c97b41`. It records 27 cases, 27 grammars, five families and 27 receipts. The SHA-256 of the canonical ordered receipt-hash set is `523add74c2607d6b5c85fb5f9b270fa5fbca800d3dd05d05131482b044e1a42d`; parent bindings SHA-256 is `460165c92f3afaebc023a49ab5e0fdb86f7fe4c8133032bb54f6bef67ef0911a`; source manifest SHA-256 is `bb5b101492d18ee6c27a649874ffac75aa5dcb2de44cbdc5718902b4cfc6e441`.

The diagnostic evidence and V84 authority snapshot preserve 27 JSON receipts and 27 `.json.sha256` sidecars. Independent validation confirms each receipt's canonical SHA, sidecar, unique selector, request identity, D9.9/D9.10 parent identity, family-stage/prototype/launcher pins, visual payload/repeat hash equality, visual-parameter canonical text hash, separated gameplay/music seeds, timing descriptor, governance locks and in-memory-only materialization boundary. All 30 global source pins match the V84 snapshot; the recovery verifier repeats all 30 checks against the live checkout.

## Exact packaging defect

The original ZIP was created successfully. The retained original archive has 72 entries and contains all run files. Its receipt entry names use literal Windows path separators, e.g. `receipts\01_E4B_R1P_20261107_032743_5F75045C_01.json`. The V1 PowerShell runner counts only `^receipts/[^/]+\.json$`, so it reports zero. The 27 receipt files exist on disk and inside the archive; this is a separator-normalization false negative after successful generation and finalization.

The Python finalizer output itself records:

- `status=PASS_R1P_PARAMETER_PAYLOADS_27_OF_27`
- `receipt_count=27`
- `receipt_hash_verification=PASS_27_OF_27`
- `report_sha256=9e09940c7a915d1533a2ba0a97765626f5c5d8533c870cda27012d4d90c97b41`

The process receipt records PowerShell 5.1, Python 3.13.14 and Godot 4.7.1, successful subprocess exit codes, stdout/stderr hashes, no checkout source-file writes and no renderer/media dispatch.

## Recovery path — no rerun

Install this overlay add-only, then run from the active checkout root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\c11d\d9\RECOVER_C11E_E4B_R1P_EXISTING_RUN_V1.ps1" -RunId "E4B_R1P_20261107_032743_5F75045C"
```

The utility verifies the existing output directory, report and sidecars, all 27 receipts, parent bindings, source pins, process receipt, all captured stdout/stderr hashes, runtime executable SHA-256 pins and the original ZIP contents. It normalizes entry paths and writes a new `E4B_R1P_20261107_032743_5F75045C_RECOVERED.zip`, without overwriting the original or regenerating recipes. It also emits a separate recovery report and PowerShell process receipt. The exact recovery acceptance status is `PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27`.

The recovery verifier was executed successfully against an isolated extraction of V84 using Python 3.13.5: status `PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27`, source pins 30/30, receipts 27/27, backslash entries 54, recovered ZIP SHA-256 `d1ebbf87cc2a8281577b11c10a6a7fcf85914ad3ee31a56554e5863760eed366`, recovery report SHA-256 `6ee88bfa563cfaabc1ea1ca987ec799e7fa901d0992a8d3efaf8127d07a576e5`. This is a reproducibility/tool test on the supplied V84 snapshot; the operator must run it once on the active Windows checkout to pin that checkout and produce the local PowerShell process receipt. The recovery run is deliberately limited to evidence validation and ZIP repackaging. It does not invoke Python preparation/finalization, Godot, family launchers, prototypes, renderers, D3, FFmpeg, frame extraction or media generation.

## Corrected runner for future use

`RUN_C11E_E4B_R1P_LOOP_PARAMETER_PAYLOADS_V2.ps1` is a separate add-only path. It normalizes each archive entry `FullName` by replacing `\` with `/`, trims a leading slash, counts exactly 27 JSON receipts and 27 `.json.sha256` sidecars, and leaves the V1 runner untouched. A new R1P run is not required to close the retained run.

## Acceptance boundary

R1P closes only request-bound, deterministic, in-memory Loop family parameter payloads and timing descriptors. It does not materialize C11-C frames/pixels or establish visual quality, consumer readiness, D9.10 renderability, audio behavior or release readiness. Maintain `renderer=OFF`, `D4.8=BLOCKED`, `D9.10=PREPARE_ONLY`, `D9.14/D9.16=BLOCKED`, `D9.17=BLOCKED_NO_GO`, `D10=BLOCKED_FOR_PROMOTION` and `release_authority=NONE`.
