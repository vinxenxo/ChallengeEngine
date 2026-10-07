# C11-D D6.4 Runner Repair V2

## Root-relative overlay

Apply this overlay at:

`C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`

## Fixes

1. The PowerShell runner now invokes the Python snapshot mode with the required `--root` argument:

   `python seed_request_plan_integrator.py --root <repo> --snapshot-only`

2. The runner creates `artifacts/tests/c11d_d6/d6_4/` before execution when absent.

3. The runner still enforces that only the D6.4 evidence directory may change and that this directory contains exactly the four declared evidence JSON files.

## Release policy

D6.4 evidence is written only under:

`artifacts/tests/c11d_d6/d6_4/`

The D6.4 runner does **not** write to `release/` and must not do so because the mutation guard is intentionally limited to the D6.4 evidence tree.

Release packaging is a separate lifecycle step and is not part of D6.4 validation.
