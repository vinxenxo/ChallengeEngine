# C11-C 2.18.6 — Final Test Contract Hotfix

Applies to the current C11-C 2.18.x freeze candidate.

## Repairs

- Fixes the stale Visual Drill review default: non-Tracking families use 17s gameplay; Tracking remains 21s.
- Makes the Longform source-artifact contract test self-contained by defining `_assert()`.
- Adds the D1.5 platform layout template concept for versioned Header / Body / Footer / CTA / safe-area profiles.

## Apply

```powershell
Expand-Archive -LiteralPath "$env:USERPROFILE\\Downloads\\C11C_2.18.6_TEST_HOTFIX_OVERLAY.zip" -DestinationPath "." -Force
```

## Focused tests

```powershell
.\\c11c-suite\\c11c-test\\run_suite.bat C11CVisualDurationPolicyContractTest.gd
.\\c11c-suite\\c11c-test\\run_suite.bat C11CVisualLoopLongformSourceArtifactContractTest.gd
```

## Full logical corpus

```powershell
python .\\tests\\run_all.py
```

No simulation, mechanics, RNG or authored gameplay truth is changed by this overlay.
