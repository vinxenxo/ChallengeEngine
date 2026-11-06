# C11-E Current Documentation Index — V27

**Authority:** Current Authority V67; Gates Matrix V65; Execution Backlog V42; Family Roadmap V55; Family Alignment V21.

## Read first

1. `AGENTS.md` (legacy V18-era navigation; note its documented SHA-256 typo).
2. `.continue/rules/CONTINUE.md` (legacy V18-era navigation; do not treat its malformed SHA as canonical).
3. `README.md` (legacy V18-era navigation).
4. `docs/current/e/C11E_CURRENT_AUTHORITY_20261105_V67.md`.
5. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261105_V65.md`.
6. `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261105_V42.md`.
7. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261105_V55.md`.
8. `docs/current/e/C11E_E4A_CHALLENGE_LOOP_DRILL_ALIGNMENT_20261105_V21.md`.
9. `docs/history/c11e/C11E_E4A6_LIVE_PIXEL_CAPTURE_POSTMORTEM_20261105_V10.md`.
10. `docs/history/c11e/C11E_E4A6_LIVE_PIXEL_POSTPROCESS_PLAN_20261105_V12.md`.
11. `docs/history/c11e/C11E_E4A6_RESERVED_BANDS_VISUAL_REQUIREMENT_20261105_V5.md`.
12. `docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_V3.md`.
13. `docs/history/c11e/C11E_C11C_GENERADORMAESTRO_MANIFEST_DIVERGENCE_20261105_V1.md`.
14. `docs/history/c11e/C11E_ROOT_DOCS_MANIFEST_SHA_ERRATUM_20261105_V1.md`.

## Prompts for context handover

- `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261105_V65.md` (Master / Overhand).
- `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261105_V65.md`.
- `prompts/C11E_FIRST_PROMPT_20261105_V9.md`.

## Current E4A.6 evidence boundary

V2's Windows command passed AST, 22 focused tests, Godot import, live-root and Movie Maker capture, but its orchestration returned BLOCKED because a path-based helper received in-memory stdout text. Recovery V1 then passed AST but stopped before evidence processing because it compared Git HEAD with a stale pre-commit pin; no Git checks are permitted in per-iteration runners because the operator commits each iteration. Recovery V1.1 removed Git checks but blocked twice at documentation preflight because its external manifest/payload paths were not co-located. Neither run processed media or wrote source/docs. Recovery V1.2 embeds the compressed manifest and all 15 versioned document payloads in the runner, self-extracts and SHA-verifies them under the unique evidence run root, and works with only the `.ps1` in Downloads. It reuses the AVI and does not rerender or repeat tests. V2, V1 and both V1.1 failure receipts remain immutable.

## Current recovery handoff

Only `RUN_C11E_E4A6_RESERVED_BANDS_RECOVERY_V1_2.ps1` is current. Copy only this `.ps1` to Downloads; it has no external manifest or docs-tree dependency. Do not copy manifests separately. Expected receipt is `C11E_E4A6_RESERVED_BANDS_BLACK_RECOVERY_V1_2_RECEIPT.json`; its PASS remains test-only.

## Next gate

Full Challenge E4A A/V: corrected D-composited MP4 unchanged + actual D3 V5/D3.3 audio + A/B same music seed / C changed music seed + identical H.264 video + AAC-LC/48 kHz/stereo/non-silence + 15 s + <=0.15 s A/V drift + operator listening review + E1 GUI/CLI parity. E4B/E4C/E5/Smoke18/Matrix101/E8 remain ordered after full E4A.

## Governance

C11-C 2.19.12 remains immutable production baseline; renderer/dispatch/production media OFF; `release_authority=NONE`. The original-vs-active `GeneradorMaestro.gd` source divergence remains unresolved and is not superseded by E4A.6.
