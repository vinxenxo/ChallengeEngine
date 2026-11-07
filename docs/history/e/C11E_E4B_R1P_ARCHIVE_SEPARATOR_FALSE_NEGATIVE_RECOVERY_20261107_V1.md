# C11-E E4B R1P — Archive Separator False-Negative and Recovery Record V1

**Date:** 2026-11-07  
**Run:** `E4B_R1P_20261107_032743_5F75045C`  
**Disposition:** parameter generation PASS; archive assertion defect isolated; recovery-only repack supplied.

## Evidence chain

- R1P install: `PASS_ADD_ONLY_INSTALL`, 11/11 files; package-manifest SHA-256 `8bbf54d645aa6e5e1ade723cfd7948110e6d2eb2dba3e51ec751c3d0a81910de`; frozen C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; static audit SHA-256 `600c22dafe2e377cb02b4a69f8823a44745d705b71cdb0d6bcec38da52df3e92`.
- R1P run report status: `PASS_R1P_PARAMETER_PAYLOADS_27_OF_27`; canonical report SHA-256 `9e09940c7a915d1533a2ba0a97765626f5c5d8533c870cda27012d4d90c97b41`.
- Parent bindings SHA-256 `460165c92f3afaebc023a49ab5e0fdb86f7fe4c8133032bb54f6bef67ef0911a`.
- Source manifest SHA-256 `bb5b101492d18ee6c27a649874ffac75aa5dcb2de44cbdc5718902b4cfc6e441`.
- Receipt hash-set SHA-256 `523add74c2607d6b5c85fb5f9b270fa5fbca800d3dd05d05131482b044e1a42d`.
- Diagnostic evidence ZIP SHA-256 `1907279bc21a6c923f43f2c9a77dc78b8c7d29a70d7a63b6ec2c5918a9bf1789`.
- V84 authority ZIP SHA-256 `57d41563d070011e94bd27dcb1bb384de13e95308157d4a8abba8d68189e1234`.

The diagnostic package contains the failed inner archive, all 27 JSON receipts and all 27 sidecars. The inner archive has 72 files; it is structurally readable and each entry's bytes match the corresponding output-root file in the V84 snapshot. Original inner ZIP SHA-256: `a3bb4ddd6f4933026b0221c7e0eb1b62ffe40d477d72ce0190bbe9587b67b800`.

## Root cause

The runner performs an output-folder count of 27 JSON receipts and 27 sidecars before compressing. Python finalization also reopens all 27 receipts and sidecars and confirms the canonical hashes. `Compress-Archive` then creates the ZIP. The subsequent assertion filters `[System.IO.Compression.ZipArchiveEntry].FullName` with `^receipts/[^/]+\.json$`. In the observed PowerShell/.NET archive, the literal entry is `receipts\01_...json`, not `receipts/01_...json`. The comparison is case-sensitive only as to separators; it never normalizes the entry path. Hence the runner reports zero while all 27 JSON entries and sidecars are present.

This is a deterministic packaging-validation bug, not a parameter recipe-generation, helper invocation, Godot execution, parent-binding or hashing failure. No source patch or recipe regeneration is warranted. The new recovery verifier was tested against an isolated V84 extraction and passed the full retained evidence set (27/27 receipts, 27/27 sidecars, 30/30 source pins, 54 backslash-bearing archive entries). It produced a separately named slash-normalized ZIP with SHA-256 `d1ebbf87cc2a8281577b11c10a6a7fcf85914ad3ee31a56554e5863760eed366` and recovery report SHA-256 `6ee88bfa563cfaabc1ea1ca987ec799e7fa901d0992a8d3efaf8127d07a576e5`. This result is a test against the supplied V84 snapshot; live checkout verification remains a single operator command.

## Corrective action

1. Preserve the V1 runner and original ZIP unchanged.
2. Use `RECOVER_C11E_E4B_R1P_EXISTING_RUN_V1.ps1` to revalidate the saved run against live source pins and rebuild a new ZIP with slash-normalized member names.
3. Require the recovery status `PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27` and retain its report/process receipt and recovered ZIP SHA-256.
4. Use the new V2 runner for any later R1P rerun. Its archive assertion normalizes the `FullName` separators and checks both 27 JSON files and 27 sidecars.

Installer behavior is intentionally simple: one add-only overlay, all destinations preflighted before writes, package payload SHA verification, and no overwrite/delete/move or source edits. Do not add installer self-tests or run R1P again merely to prove the path fix.

## Non-effects

`renderer=OFF`; D4.8 remains `BLOCKED`; D9.10 remains `PREPARE_ONLY`; D9.14/D9.16 remain `BLOCKED`; D9.17 remains `BLOCKED_NO_GO`; D10 remains `BLOCKED_FOR_PROMOTION`; release authority remains `NONE`. No family launcher, frame/pixel extraction, D3/audio, FFmpeg, mux or media ran as part of this recovery.
