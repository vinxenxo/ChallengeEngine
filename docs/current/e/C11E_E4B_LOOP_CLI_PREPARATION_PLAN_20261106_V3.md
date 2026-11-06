# E4B Loop CLI Preparation Plan — V3

## Input

Use the existing local GUI evidence directory `artifacts/tests/c11d_d9/producer_universal/D99-GUI-439FD530F839`. If its location differs, pass `-GuiEvidenceRoot`. Do not rerun GUI and do not use the ZIP itself as the directory.

## Install

Install `C11E_E4B_LOOP_CLI_PARITY_V2.zip` with its included add-only installer. Extract the archive directly to Downloads; the script is at the root of the extracted folder. The installer preflights 30 source pins (including D99 main.py postimage), the frozen C11-C manifest, 18 file hashes/byte counts and all destinations before writing. It installs 15 versioned documents plus the V2 runner/helper/test. No existing source file is overwritten.

## Execute

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\c11d\d9\RUN_C11E_E4B_LOOP_CLI_GUI_PARITY_V2.ps1"
```

Optional explicit evidence path:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\c11d\d9\RUN_C11E_E4B_LOOP_CLI_GUI_PARITY_V2.ps1" -GuiEvidenceRoot ".\artifacts\tests\c11d_d9\producer_universal\D99-GUI-439FD530F839"
```

The runner uses Python 3.13 and Windows PowerShell 5.1. It verifies 32 source pins after installation, static proposal tests 17/17 and Unicode helper tests 5/5, derives CLI JSON from GUI UTF-8, runs D9.9 CLI and E1 CLI with the same raw request and verifies parity/governance. The `.ps1` is ASCII-only.

## Acceptance

Require `C11E_E4B_LOOP_CLI_GUI_PARITY=PASS_GUI_CLI_EDITORIAL_PARITY_ONLY`; equal GUI/CLI editorial hash; exact title/subtitle/CTA/language and NFC; D9/E1 request and plan hashes equal within CLI; correct music and independent seed domains; `NOT_CONSUMED_E1`/gate E4 and family adapter disconnected; renderer/input/dispatch/production/media false; D4.8 BLOCKED; release NONE.

## Output

`artifacts/tests/c11e/e4b_loop_cli_parity/<ID>/` contains raw CLI request, prep receipt, D9 result, E1 result, parity receipt, runner receipt and process stdout/stderr with hashes. Zip the complete folder and upload. V2 is plan/preparation-only; no Godot, D3 V5, family music engine, FFmpeg, render or media.
