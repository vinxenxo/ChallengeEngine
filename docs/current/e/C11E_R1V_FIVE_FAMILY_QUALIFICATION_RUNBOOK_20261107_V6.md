# R1V Five-Family Qualification Runbook — V6

## Stop conditions and failed attempts

Do not rerun V2 wrapper or V3 installer. V3 installer failed 0/15 because it passed `-3.13` to the actual `Python313\python.exe`; it did not install files. Previous wrapper attempt failed preflight with null exit codes. No launchers or media were created by either attempt.

## V4 install — one PowerShell-only operation

Extract the V4 ZIP to a new Downloads folder, not over the checkout. Run `INSTALL_C11E_R1V_PYTHON_EXE_RESOLUTION_RECOVERY_V4.ps1` with active ProjectRoot. Installer performs only PowerShell manifest/frozen/governance/R1P/payload/path/AST validation and add-only copy. It does not discover Python, run the Python suite or spawn another process. Identical pre-existing bytes are verified/skipped; differing collisions are rejected. Require `PASS_ADD_ONLY_INSTALL` and `VERIFIED_PAYLOAD_FILES=15/15`.

## Capture — one Python preflight only

Run only `tools/c11d/d9/RUN_C11E_E4B_R1V_FIVE_FAMILY_QUALIFICATION_V3.ps1`. It resolves a direct `python.exe`, confirms version 3.13 via `-c`, runs the 32-test active-checkout suite exactly once with stdout/stderr file redirection and numeric exit code; only a 32/32 PASS permits the ten approved launcher processes. Do not run the test suite separately or manually invoke launchers.

It must stop on any source pin, policy, path, output-root, temporary-file, sidecar, frame or pixel discrepancy. Preserve all raw receipts and logs; do not clean output directories.

Scope remains five first-family selectors A/B, native silent MP4 only, FFprobe read-only, FFmpeg decode-to-memory. No audio, music, filters, D consumer, D9.10, D3, mux, GIF, delivery or release. Technical PASS awaits operator visual review.
