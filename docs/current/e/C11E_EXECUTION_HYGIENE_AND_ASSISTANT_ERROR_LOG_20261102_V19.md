# C11-E Execution Hygiene and Assistant Error Log — V19

**Date:** 2026-11-02
**Authority:** `C11E_CURRENT_AUTHORITY_20261102_V23.md`

## Current execution rules

- Active Windows checkout is authoritative; local Git commits belong to the operator.
- Never reapply V22/V22 V2 after commit `02f5fac`; its 12 actual path changes are already committed and reconciled.
- Do not compare actual staged path count with the size of an allowlist. Allowlist defines permitted paths, not a mandatory number of changed files. Verify staged paths are a subset of allowlist and reject unexpected paths.
- Add-only applicators must be idempotent: identical existing destination = `ALREADY_PRESENT_IDENTICAL`; differing content = hard stop. Never overwrite.
- `git diff --cached --check` remains mandatory. No native PowerShell stderr redirection under EAP Stop where it can turn successful test stderr into a false failure; prefer `System.Diagnostics.ProcessStartInfo` with asynchronous stdout/stderr capture.
- Every physical attempt uses a fresh RequestId; do not create duplicate renders for read-only reconciliations.
- Preserve R4 receipt, evidence ZIP, hashes, source media, and original `human_visual_review=PENDING` field unchanged.
- E3 begins with source discovery; do not guess D3 Music V5 settings, edit implementation, render audio or mux before reviewing the active contract and pins.
- Maintain C11-C 2.19.12 frozen manifest and protected mechanics; release authority stays NONE until E8.

## Incidents and resolutions

1. V22 original overlay: installer expected `overlay\` while package layout differed. Package V2 corrected the folder structure.
2. V22 V2 staging count: installer incorrectly required a fixed 18 staged paths. Only 12 paths contained actual changes, and `git diff --cached --check` passed. Operator committed the 12 valid changed paths as `02f5fac7698fe6d73076d3da1e3dfa852bd06725`. The 18 count assertion was a bug, not a missing-file defect.
3. Re-running V2 after the commit correctly encountered `Add-only destination already exists`. This was the add-only guard working; the script should not have been run again. No reset, clean or rollback is needed.
4. Read-only reconciliation at `02f5fac` passed: 9/9 documentary/contact-sheet pins, V21 whitespace fixes 3/3, frozen C11-C/E2 source pins, receipt/sidecar, ZIP entries/hash, media hashes 2/2, FFprobe 2/2, clean worktree.

## Assistant error handling

Do not generate another installer iteration when the existing commit has already applied and passed reconciliation. Prefer a read-only verification script. Never require an allowlist path count to equal staged changes. Never repeat user-confirmed questions or accepted preflights.
5. V23 Markdown whitespace and preflight sequencing: seven newly added Markdown documents contained trailing spaces, so the mandatory staged whitespace check correctly stopped the installer after staging. The read-only E3 preflight was then launched before the V23 changes were committed and correctly rejected the non-clean checkout. Repair is limited to these seven documents; the E3 preflight's two content pins are refreshed below. Correct order: repair, staged diff check, commit V23, then run the read-only E3 preflight. No audio, renderer, production media or FFmpeg mux was invoked.