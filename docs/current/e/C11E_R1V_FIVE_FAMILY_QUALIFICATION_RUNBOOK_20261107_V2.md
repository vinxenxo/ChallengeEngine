# C11-E R1V Five-Family Qualification Runbook — V2

## Preconditions

1. Active Windows checkout remains `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`; never extract a snapshot over it.
2. Prior closeouts remain accepted: R1P recovered archive, Option C installer/contract receipts, frozen C11-C manifest and static family audit.
3. Python 3.13, Windows PowerShell 5.1, Godot 4.7.1, FFmpeg with libx264 and paired FFprobe are available on PATH. The helper additionally checks that `python.exe` resolves to the same Python 3.13 interpreter selected by `py -3.13`.
4. The installer preflight completes 28/28 Python tests and active-checkout integration: R1P archive/27 receipts, 61 live source pins, Option C report/process/install receipts, preserved V1 proposal, approved V2 approval record, unchanged D4.8 production policy.
5. The ten output roots, ten temp-silent file paths and ten temporary AVI prefixes are absent. `override.cfg` preimage is captured exactly.

## Install

Extract the overlay to a separate folder under Downloads. Do not extract into the checkout. Run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\Downloads\C11E_D4_8_R1V_FIVE_FAMILY_QUALIFICATION_V2_20261107\INSTALL_C11E_D4_8_R1V_FIVE_FAMILY_QUALIFICATION_V2.ps1" -ProjectRoot "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"
```

Expected add-only result: `INSTALL_STATUS=PASS_ADD_ONLY_INSTALL`, `INSTALLED_FILES=17/17`. The installer parses itself and the runner with the Windows PowerShell 5.1 AST parser, verifies all 17 payload hashes and runs the 28-test active-checkout integration suite before copying any file. If a destination exists, stop; do not delete or replace it. Installer's preflight/receipt identifies the colliding path.

## Run

From the checkout root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\c11d\d9\RUN_C11E_E4B_R1V_FIVE_FAMILY_QUALIFICATION_V1.ps1" -ProjectRoot "C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS"
```

The runner first repeats the static+active evidence suite and captures its stdout/stderr. It then performs exactly ten pinned C11-C `-NoSound` launches (A then B for each family), immediately validates output and all 61 source pins, inspects source MP4s with read-only FFprobe, decodes frames to memory with FFmpeg and compares the five pairs. Before each launcher it verifies the unique output root, deterministic temp-silent MP4 path and run-tagged temporary AVI prefix are absent; it never cleans or reuses them. It captures a wrapper process receipt with exit codes and stdout/stderr SHA-256. It stops at the first error and preserves partial evidence. No manual relaunch into an existing output root.

## Expected technical result

`PASS_R1V_FIVE_FAMILY_TECHNICAL_CAPTURE_10_OF_10_PENDING_OPERATOR_VISUAL_REVIEW` with 10/10 launchers, five deterministic repeat pairs, five family inventories × A/B, 61/61 pins throughout, and an evidence ZIP.

This result still requires the operator/independent reviewer to inspect the ten silent MP4s visually. A technical PASS alone does not qualify the five families for full production. Do not qualify the remaining 22 variants until this review is accepted. D compositor, D9.10 render dispatch, D3/audio and mux remain off.
