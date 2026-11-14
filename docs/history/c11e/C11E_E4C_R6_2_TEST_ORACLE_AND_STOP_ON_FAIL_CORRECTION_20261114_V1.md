# C11-E E4C R6.2 — test-oracle correction and fail-closed orchestration

Date: 2026-11-14

## R6.1 outcome (truthful disposition)

R6.1 passed package ZIP, package-file, source-pin and preimage-lineage preflight, but it did **not** pass the staged consumer suite. The installer failed closed before transaction at `test_10_family_title_subtitle_and_cta_use_distinct_approved_regions`; no R6.1 destination writes, install receipt, or R6.1 transaction journal were produced. The subsequent user-side commands were manually continued despite the non-zero installer exit. They read a prior R5 `RUN_ID`/audit receipt, attempted a runner path that had not been installed, and then printed unconditional PASS text. Those audit/runner PASS lines are not R6.1 evidence and are expressly invalidated.

## Root cause

The approved family-title style is Inter-Bold 22px, centered, warm gold RGB `(235, 215, 161)`. The R6.1 test predicate counted a pixel only when the minimum of all three channels was greater than 180. Because the approved blue channel is 161, no fully rendered approved-gold title pixel could ever satisfy that predicate. The assertion therefore rejected the correct approved title color; it was a test-oracle defect, not evidence that the compositor failed to render the title.

## R6.2 correction

R6.2 changes only the test predicate: the title region is checked against a chromatic gold floor `(180,160,110)`, while subtitle and CTA remain checked against their near-white floor `(180,180,180)`. The test also pins the expected approved family-title RGB value. Compositor source, visual geometry, typography, title color, native frame content, phase timebase, source evidence and audio artifacts are unchanged.

R6.2 retains the five replacement preimages proven by the accepted R2/R4/R5 transaction journals. R6.1 did not start its transaction, so the active checkout remains at the R6.1 preflight state. The first replacement preimage is the R2 accepted postimage `42e4cb8097ea9536dca63627e82c240ce0bb5b73baf03152269a35ac219a68eb`; the other four preimages retain their already documented accepted journal lineage. Installer and independent auditor validate all five links.

## Execution safety correction

R6.2 includes one package-root orchestration script. It verifies the ZIP/sidecar, extracts to a newly generated unique temporary directory (never overlays an existing Downloads folder), verifies all 24 package files, then executes install, audit and the R6 runner sequentially. A non-zero process exit or missing/wrong run-specific receipt terminates the sequence immediately. The audit receipt must match the exact R6.2 run ID, package ID and ZIP SHA. The runner is not started until both installation and independent audit pass. It also verifies the newly generated output ID, technical receipt, seven review frames and review-bundle SHA. No stale R5 or earlier receipt can satisfy those checks.

## Governance and next gate

R6.2 is a test-only/package correction. No C11-C frozen source or manifest is modified; no native capture, GUI/CLI smoke, Godot, family music generation, production dispatch or release action is introduced. E1 remains PREPARE_ONLY, dispatch OFF, release_authority NONE. Successful R6.2 technical requalification remains pending human visual/audio review. `tracking/tier-1` remains 0/20 until operator acceptance; this does not close E4C.
