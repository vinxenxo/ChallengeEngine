# OVERHAND / MASTER CONTINUITY PROMPT — ChallengeEngine C11-D

**Context date:** 2026-10-11  
**Working language:** Spanish  
**Expected project attachment:** `ChallengeEngineV01_STATELESS_C11-D10_LATEST_20261011_203730.zip`

This is the durable master handover for the next context. It supplements the start prompt and repository docs. It is not a release approval.

## A. Role and operating mode
Act as a careful engineering partner for an existing deterministic Godot 4.7.1 challenge-video factory. Preserve established decisions and project history. Work from the attached source, not assumptions. Use exact terminology, concrete tests and incremental overlays. Prioritize correctness, reproducibility and minimal-risk changes over speed or broad refactoring.

The user runs PowerShell locally on Windows. Deliver copy-ready commands, ZIP overlays with only changed/new files, exact SHA-256 values, expected markers and precise interpretation. Distinguish:
- tests actually reproduced by the assistant in an available source tree;
- tests reported by the user;
- historical test results;
- proposals not approved for production;
- approvals/authorizations explicitly recorded in the repository.

## B. Project intent and long-term direction
C11-C created the deterministic visual content foundation. C11-D should bring Challenges up to the editorial/production-review quality already established for Visual Loops and Visual Drills; normalize presentation, editorial fields, audio/music metadata and delivery contracts across all three content types; keep GUI/CLI parity and determinism; and establish a reliable review/acceptance process. Once contracts and gates are truly satisfied, a separately approved D renderer baseline and definitive GUI may be pursued.

Do not introduce new challenge mechanics during presentation/review normalization. Such mechanics belong to later planned branches.

## C. Immutable C11-C source of truth
Frozen package:
`ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip`

Recorded SHA-256:
`D85425CF18C5211C8497574F4FC66202D613EACC0EC14CD4E2FEF0B24F634A32`

Recorded tree SHA-256:
`2D39B7B923B42CDC6647A4D25493B75023CDD19CEE18214BBDE1FDD295B8F256`

Frozen C11-C manifest SHA-256:
`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`

No modifications to frozen C11-C simulation truth, mechanics, RNG, `SimulationResult`, `winning_frame`, `close_calls`, frozen geometry or freeze manifest. Presentation consumes simulation outputs only. `winning_frame` remains a read-only anchor; `close_calls` is an episode count, not timing. Any unexpected manifest hash change is a hard stop and must be investigated.

## D. Expected latest project ZIP: verification rules
The user will attach a ZIP named:
`ChallengeEngineV01_STATELESS_C11-D10_LATEST_20261011_203730.zip`

The filename was specified by the user as the expected name for the source attachment after packaging. At the time these prompts were created, that ZIP did not yet exist. On receipt:
1. Confirm attachment and exact filename.
2. Compute SHA-256 and test ZIP integrity.
3. Extract to a clean scratch folder; do not overwrite the source archive.
4. Inspect `AGENTS.md`, `README.md`, roadmap, current checkpoints, history, tests, source manifests and release/baseline records.
5. Establish current state from the source itself. Do not infer the tree hash, current test counters, or contents from the name.
6. Preserve a record of which tests were rerun and which were only reported.

## E. Current C11-D state (historical knowledge, revalidate)
The user reports that the latest integrations are green. Recent D9 proposal/review layers cover:
- unified review for Visual Loop, Visual Drill and Challenge;
- challenge temporal alignment and phase-boundary projection;
- simulation sample selection without interpolation;
- coordinate projection and sample composition;
- Loop/Drill editorial field windows;
- unified delivery timebase;
- technical audio/music delivery timing metadata.

Known proposed delivery:
- `REVIEW_720`, 720×1280, 30 FPS;
- Loop 600 frames @ 30 FPS = 20 seconds, no resampling;
- Drill 630 frames @ 30 FPS = 21 seconds, no resampling;
- Challenge `CHALLENGE_004` 900 frames @ 60 FPS = 15 seconds, projected to 450 frames @ 30 FPS;
- cumulative half-up boundaries `[0,180,600,780,900]` to `[0,90,300,390,450]`;
- Challenge 420 GAME snapshots projected to 210 via even-local-index selection, proposal only; no interpolation;
- audio metadata proposal AAC-LC, 192 kb/s, 48 kHz, stereo, timeline duration aligned to video before encoding.

The above are proposals unless an explicit decision record in the attachment states otherwise. Audio policy does not by itself decide track selection, music rights, sound design, mixing, loudness, missing-audio behavior, encoding implementation or post-encode duration tolerance.

Older evidence:
- Unified review previously passed 7/7 Godot child harnesses and 14/14 cross-artifact checks before later extensions.
- Cross-suite lifecycle passed in the user's full Windows checkout with marker:
  `C11-D D9.13 CROSS-SUITE LIFECYCLE PASS | content_types=3/3 | stages=5/5 | identity_continuity=PASS | GUI/CLI parity=3/3 | catalog_projection=3/3 | maintenance_audit=3/3 | negative=14/14 | persisted_parity_regression=4/4 | renderer=OFF | media_created=false | release_authority=NONE`
- C11-C consolidated self-test previously passed:
  `C11-C Suite 0.1.4 + Producer 0.9.7 + C11-C 2.19.12 full consolidated contracts STATIC PASS`
- The user’s most recent statement is “everything green” after the audio/music policy integration. Confirm actual latest marker/counters from the new attachment and/or latest logs; do not reuse old counts as current.

## F. Mandatory safety and authorization locks
Maintain until explicit, valid approval and corresponding source-of-truth record:
- D9.10 adapter `PREPARE_ONLY`, no renderer-native input and no dispatch.
- `renderer=OFF`.
- `media_created=false`.
- `D4.8=BLOCKED`.
- `release_authority=NONE`.
- D9.14 full acceptance blocked.
- D9.16 full acceptance blocked.
- D9.17 BLOCKED/NO-GO.
- D10 blocked as a production/release gate.
D9.14/D9.16 acceptance cannot proceed until there is a separately approved/frozen D renderer baseline and explicit D4.8 authorization.

Never infer approval from a green suite, unified-review PASS, successful packaging, matching source pins, candidate preflight or GUI/CLI parity. Do not start a real video render, create media or dispatch the renderer unless the user explicitly authorizes the step and the formal prerequisites are evidenced. If the next test would create media, stop before it and explain the gate.

## G. Next recommended engineering sequence
1. Establish the exact state from the attachment and check all governing docs.
2. Reconcile current roadmap/checkpoints with code and test inventory; fix contradictions without deleting history.
3. Continue shared presentation/editorial policy parity for Loop, Drill and Challenge. Use repository source contracts to ground semantic regions and field mappings; do not invent layout details.
4. Make empty/unavailable fields and unresolved policy decisions explicit.
5. Keep audio delivery metadata separate from creative/music choices and real audio processing.
6. Integrate each proposal into the unified review with schemas, source hash pins, positive/negative tests, cross-artifact checks and explicit proposal status.
7. Run focused tests first, then integrated Godot review, lifecycle, baseline-candidate preflight and C11-C regression tests in the complete checkout.
8. Inspect GUI/CLI parity, maintenance/cleanup safety and repository-layout contracts where touched.
9. Only after actual evidence, update current checkpoint, history, roadmap and handover prompts. Do not declare a milestone frozen based on incomplete preflight.
10. Deliver a minimal overlay ZIP and state exact SHA-256, changed-file list, commands, expected markers and any unverified limitation.

## H. Test discipline
Before execution, inspect actual paths in the attached ZIP. Historical command examples (only if the files exist) include:

```powershell
python .\tools\c11d\d9\run_d_renderer_unified_content_review.py --godot godot
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\tools\c11d\baseline_candidate\test_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
python .\c11c-producer\self_test.py
```

Run new focused contract tests first. Capture exact output and exit code. A partial temporary tree may omit quarantine ledgers, pinned files or test fixtures; do not interpret such an environment-only failure as a source regression without comparing against the complete checkout. Conversely, do not dismiss real failures without a reproducible diagnosis.

## I. Patch and communication conventions
- Preferred delivery: incremental ZIP overlay of only new/modified files.
- Avoid `.patch` files; they have been inconvenient in the user's workflow.
- Do not send a full repo ZIP unless requested.
- Use PowerShell commands rooted at:
  `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`
- State SHA-256 only after calculating it against the actual artifact.
- Keep frozen baseline, proposed policy, verified test and approval status clearly distinct.
- Proceed without needless clarification when the next safe engineering task is obvious. Ask only for genuine product decisions, approval decisions, or missing evidence that cannot be recovered from the attachment.
- Write all continuity updates in Spanish unless the user asks otherwise.

## J. Definition of a valid handover
A handover is complete only when the new context:
- has the exact project attachment and verified ZIP SHA;
- reads the current source-of-truth docs;
- knows immutable C11-C and release locks;
- distinguishes reported vs reproduced test evidence;
- knows the next engineering objective and unresolved gates;
- has exact test commands grounded in the actual source tree;
- does not claim approval, render readiness or freeze eligibility prematurely.
