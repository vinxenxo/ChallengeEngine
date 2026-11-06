# C11-E Current Documentation Index — V28

**Authority:** Current Authority V68; Gates Matrix V66; Execution Backlog V43; Family Roadmap V56; Family Alignment V22; PowerShell Runner Style Guide V4.

## Read first

1. `AGENTS.md`, `.continue/rules/CONTINUE.md`, `README.md` (legacy V18-era navigation; their malformed frozen-manifest SHA references are documented in the history erratum; do not use those values as authority).
2. `docs/current/e/C11E_CURRENT_AUTHORITY_20261106_V68.md`.
3. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261106_V66.md`.
4. `docs/current/e/C11E_E3_EXECUTION_BACKLOG_20261106_V43.md`.
5. `docs/current/e/C11E_E4A_CHALLENGE_LOOP_DRILL_ALIGNMENT_20261106_V22.md`.
6. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261106_V56.md`.
7. `docs/current/e/C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_PLAN_20261106_V1.md`.
8. `docs/current/e/C11E_POWERSHELL_RUNNER_STYLE_GUIDE_V4.md`.
9. `docs/history/c11e/C11E_E4A6_RESERVED_BANDS_BLACK_RECOVERY_POSTMORTEM_20261106_V1.md`.
10. `docs/history/c11e/C11E_E4A7_AUDIO_MUX_SOURCE_PIN_RECONCILIATION_20261106_V1.md`.
11. Existing lineage: E4A6 capture postmortem V10, postprocess plan V12, reserved-band requirement V5, GeneratorMaestro manifest divergence V1, and root-doc SHA erratum V1.

## Prompts for context handover

- `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261106_V66.md` (Master / Overhand).
- `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261106_V66.md`.
- `prompts/C11E_FIRST_PROMPT_20261106_V10.md`.

## Latest accepted E4A.6 boundary

Recovery V1.2 is complete and user visual review is PASS. Receipt SHA: `3279011fa16479d4901c5b271463707a437ce7458d306c1667ab222cb1603980`. Silent D-composited MP4 SHA: `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`. Eight boundary stills; 12/12 inactive reserved-band checks PASS with RGB<=3 tolerance; 4/4 active HOOK/CTA checks PASS. 22/22 Python tests, Godot 900-frame runtime and Movie Maker 900-frame capture are reused from V2, not rerun.

Do not rerun V2, recovery V1/V1.1/V1.2 or any accepted source/render tests absent concrete drift/new defect. No Git/HEAD/status checks in per-iteration tools.

## Current next gate

`RUN_C11E_E4A7_D_COMPOSITED_CHALLENGE_AV_V1.ps1` (ready for execution; final outcome is governed by the runtime receipt). It self-hydrates the Python worker and docs package, validates the Recovery V1.2 receipt and the exact MP4 SHA in the active checkout, verifies source-file pins (including current E1 service SHA `348997...`), then generates D3 V5 A/B/C music, applies D3.3 mastering, and stream-copy muxes audio onto the already D-composited video. It must not render or re-encode video. A/B same `music_seed`; C changed seed; gameplay seed constant. Output predicates are detailed in the E4A.7 plan.

The E4A.4 test remains a valid bounded audio/mux precedent, but its video input SHA `edbd446d67142d20e138e55563f16cbae8d9a4c39469fd2bebcb3c9d5723fb9e` did **not** contain the full-frame D compositor. Reuse its method/predicates only, never its MP4 input.

## Ordered campaign

E4A.7 audio/mux → operator audio review and E1 GUI/CLI parity → full E4A acceptance → E4B Loop → E4C Drill → E5 cross-family determinism/seed isolation/profile separation/parity → E6 Smoke18 → E7 Matrix101 → E8 full historical C-to-E regression, independent acceptance/freeze and separate promotion. CH_008/009 remain held for the 11 s / 12 s mismatch.

## Governance

C11-C 2.19.12 remains production authority; renderer/dispatch/production media OFF; `release_authority=NONE`. Never modify protected C source or use a snapshot ZIP as checkout authority.
