# C11-C 2.19.10 — Consolidated Repair Candidate

**NOT FROZEN.** This is the consolidated 2.19 repair candidate after the workstation complete-review regression reported `20/20` Visual Drill envelopes generated but 15 expected envelope paths missing.

## Root fix

The PowerShell reviewer supplies an absolute `ReviewRootOverride`. The envelope generator must not reinterpret that absolute path through `ProjectSettings.globalize_path()`. It now preserves absolute roots and globalizes only relative roots.

The generator also restores the established 17s non-Tracking Drill gameplay value.

## Worker contract

`Workers=7` remains genuine concurrency. Do not replace worker-local roots with a global mutex or serial fallback.

## Suite ownership

`c11c-suite/` is the only active Suite surface. `c11c-studio/` is retired and untouched.

## Apply

Extract this ZIP at the repository root with overwrite enabled. Then run the focused contract sequence in `START_PROMPT_C11C_2.19_CONSOLIDATED.md`.

## Freeze

Do not freeze from this package. Freeze remains blocked until fresh workstation acceptance and the complete 52-video review are fully green, including observed concurrency greater than 1.
