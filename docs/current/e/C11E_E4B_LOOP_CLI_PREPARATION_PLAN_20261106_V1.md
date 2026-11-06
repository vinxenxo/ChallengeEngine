# E4B Loop Active-Checkout CLI Preparation Plan — V1

## Purpose

Prove populated editorial preservation through the active Windows checkout's actual D9.9 CLI and shared E1 CLI, plus the static D-owned proposal validator. This is not a render or media test.

## Install and run

Install the add-only E4B Loop Step V1 overlay. Then run from the project root:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\tools\c11d\d9\RUN_C11E_E4B_LOOP_CLI_PREPARATION_V1.ps1"
```

Requires PowerShell 5.1 and Python 3.13. Optional `-ProjectRoot` and `-PythonExe` are supported; pins are never bypassed.

## Fixture

`visual_loops / c11c_geometric_waves_v1 / harmonic_membrane`; REVIEW; gameplay seed 314159; music seed 840001; REVIEW_720; social_default_v1; variation 0; audio ON as metadata; personalization ON. Four canonical fields:

- title: `Título editorial Loop — composición armónica en movimiento`
- subtitle: `Explora el patrón geométrico, observa sus ciclos y descubre cómo evoluciona la forma`
- call_to_action: `Guarda este loop y comparte tu patrón favorito`
- language: `es`

## Important CLI boundary

The D9.9 CLI receives the raw universal request JSON. The E1 CLI independently receives that same raw request with `--origin CLI`. Do not pass D9 result/canonical request to E1 CLI; that is not its CLI input contract.

## Runner checks

27 SHA-256 pins, including D99 V2 `main.py` postimage and C11-C family/visual/music source pins; frozen C11-C manifest; 17 static composition proposal tests; D9.9 request/editorial/plan/bridge/adapter checks; E1 request/editorial/plan identity parity; exact preservation of four values; E1 reports each field `NOT_CONSUMED_E1` (required gate E4); existing family music route remains protected and D3 V5/FFmpeg are not invoked. Receipt and output JSON/logs are written to `artifacts/tests/c11e/e4b_loop_cli/<run-id>/`.

Expected status: `PASS_CLI_PREPARATION_ONLY`; renderer/dispatch/production/media false; D4.8 BLOCKED; release NONE.
