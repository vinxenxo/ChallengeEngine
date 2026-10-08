# C11-D D9.4 — Acceptance Closure V1

Purpose: formally close D9 after successful real-media pilot execution in D9.1, audio-enabled A/V pilot in D9.2, and deterministic repeatability/negative control in D9.3.

This is a control-plane acceptance runner. It does not activate Godot, does not invoke the renderer, does not run bulk production, and does not create release products.

## Preconditions
- D8.7 receipt: PASS_NO_MEDIA / CLOSED / release_authority NONE.
- D9.0: PASS / PREFLIGHT_ONLY with pilot authorization false.
- D9.1: PASS / PILOT_COMPLETE and mutation guard PASS.
- D9.2: PASS / PILOT_COMPLETE with AAC 48 kHz stereo and release authority NONE.
- D9.3: PASS / PILOT_REPEAT_COMPLETE with exact WAV/MP4 repeatability and a changed negative control.

## Allowed write root
`artifacts/tests/c11d_d9/d9_4`

## Protected domains
C11-C, D0-D7 tooling/contracts, production/seeds definitions, release roots, and unrelated test/challenge roots are snapshotted and must remain byte-identical.

## Execution
Run from repository root:

```powershell
Expand-Archive `
  -LiteralPath "$env:USERPROFILE\Downloads\C11D_D9.4_ACCEPTANCE_CLOSURE_OVERLAY_V1.zip" `
  -DestinationPath "." `
  -Force
```

Then parse the runner with the standard PowerShell 5.1 parser audit, followed by:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File ".\tools\c11d\d9\run_d9_4_acceptance_closure.ps1" `
  -AuthorizeAcceptance
```

Expected terminal result:

`D9.4 PASS | D9=CLOSED | d9_1=PASS | d9_2=PASS | d9_3=PASS | repeatability=EXACT | negative_control=PASS | release_authority=NONE`

Expected canonical receipt:
`artifacts/tests/c11d_d9/d9_4/evidence/d9_4_receipt.json`
