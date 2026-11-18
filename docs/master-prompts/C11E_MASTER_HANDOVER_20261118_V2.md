# C11-E Master Handover — V2 (2026-11-18)

## Sole authority and workflow

Active Windows checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Never extract snapshots over it. Operator manages commits. Do not invoke Git or inspect HEAD/status/branch. SHA-256 source pins and the frozen C11-C manifest are authoritative.

## Accepted work — do not repeat

- E4A Challenge, E4B Loop, E4C Drill 20/20 and E5 Cross-Family accepted in their declared scopes.
- E5 visible Qt Producer runtime 3/3 PASS; the blank `language=es` value was an operator omission, not a product defect.
- R1V human A/V 10/10 and Loop22 A/V 44/44 accepted; preserve batches and approvals.
- E6 hydration V2 focused suite 34/34 PASS; hydration report 1,801/1,803 with exactly two historical CH004 source-pin divergences and zero other failures.
- D9 multi-selector plan: six Challenge groups, 18 E1 intents and 18 D envelopes, PREPARE_ONLY.
- V1 D9 dependency reconciliation active-checkout runner: report PASS, 13/13 fixed evidence pins/sidecars, 33/33 source pins, 9/9 route dependencies, 2/2 observed-current CH004 hashes, 0 blockers. Exact report SHA `fa54b47826f58acc823d45a8771a2dc12827d34d46d9586a34b8f6813a9e0603`.

## Incident disposition and V2 gate

The V1 installer actually completed 6/6 add-only copies and postimage hashes. The subsequent `INSTALL_FAILED` was a caller-side false failure because `$LASTEXITCODE` was checked after a PowerShell script instead of after a native process. Do not repeat that check.

V1 focused tests were 12/13 PASS on the operator's Windows environment. The single error was `WinError 1314` while attempting to create an OS symlink in `test_rejects_symlink_escape`; it occurred before the path-safety assertion. V2 provides an equivalent deterministic path-resolution escape test using a mocked `Path.resolve()`, without requiring Windows symlink privilege.

Next action: extract `C11E_E6_D9_PIN_RECONCILIATION_V2_20261118.zip` outside the checkout and run `APPLY_AND_RUN_C11E_E6_D9_PIN_RECONCILIATION_V2.ps1`. It add-only installs a new V2 test and documents, preflights destinations, rejects reparse-point ancestors, verifies hashes, runs V2 tests, then reruns the V1 read-only audit. It does not modify the V1 audit module or replace any installed file.

## E6 continuation

Once V2 returns `PASS_APPLY_AND_RECONCILE`, continue the family-owned D9 Challenge executor in PREPARE_ONLY and adjudicate CH004 historical source lineage from original E4A.7 evidence. Do not assume CH004 reuse is accepted merely because current service pins pass. Do not regenerate accepted E4A/Loop/Drill artifacts.

CH008/009 retain their declared 11 s and current phase sum 12 s. The operator's early-design explanation is historical context; duration authority remains pending a formal decision. Do not alter definitions, frames or timing during this reconciliation.

## Authorization and invariants

D4.8 R1V V2 remains immutable and blocks Smoke18, Godot capture, D3/audio/PCM and FFmpeg filters/mux. Engineering approval is not media authorization. A separate E6 TEST_ONLY authorization and explicit governance resolution are required before render/media. C11-C 2.19.12 remains sole production authority; frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. E1 PREPARE_ONLY; renderer OFF; dispatch/media false; release authority NONE. No protected C11-C changes, no parallel Producer/binder/renderer or sixth module. Git checks skipped; commits operator-managed; pins enforced.

## Roadmap

E6 Smoke18 → E7 Matrix101 (54+27+20; CH008/009 held pending explicit duration decision; 99 provisional) → E8 historic C-to-E regression, independent acceptance, immutable freeze and separate transition decision.
