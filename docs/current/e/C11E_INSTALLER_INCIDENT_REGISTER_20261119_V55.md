# C11-E Installer & Runner Incident Register — V55

**Date:** 2026-11-19

## Closed failed preflight attempts
- V1: test suite exposed six UTF-8 default-codepage errors.
- V1.1: installer failed on invalid null backup path to `File.Replace`; no replacement.
- V1.2: PowerShell 5.1 parser rejected `$rel:$destSha`; no replacement.
- V1.3: ADD_ONLY collision on stale V118 roadmap destination; failed before source write.
- V2: capture-contract regex falsely rejected compliant `Start-Process` arguments; failed before transaction.
- V2.1: staging audit attempted to construct absent copied predecessor sidecar; failed closed before transaction.
These incidents are retained as evidence. Do not rerun these scripts or patch them incrementally.

## Successful current increment
`C11E_E6_CHALLENGE_EDITORIAL_BINDING_PREPARE_ONLY_V1`: installed 19/19 ADD_ONLY; 24/24 tests; emitted 18 bound envelopes; receipt SHA `0fb637e97dcdd18f32e769d22f15a540481034641b7116fb1693eaf2c1e139aa`; binding manifest SHA `1e0cf76c7664d3224678f887b9915afad21ce27eef71e4e73e16a4e6a54e8ff3`; binding receipt SHA `ef0e2b7b6c3efdbb6a715730b783da79c0c13f5ca9df34e00e2ce6cbfcbc6b83`.

## Prevention rules
- Use exact current document version sequence from active snapshot; add-only collision is a hard stop, never overwrite.
- Read sidecar existence from actual source; do not assume or synthesize source sidecars.
- Verify the staged files that the runner actually reads.
- Capture native process stdout/stderr separately, capture ExitCode immediately, and never print PASS after nonzero child exit.
- PowerShell 5.1 AST must pass before invoking any child script.
- GIT checks skipped; operator-managed commits; SHA-256 source pins enforced.
