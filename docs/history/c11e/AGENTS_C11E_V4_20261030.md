# AGENTS.md — C11-E current engineering authority (V4)

## Active program and continuation order

The active engineering workstream is C11-E on the user-selected local Git branch `main`. Its objective is one GUI/CLI production path reusing C11-C mechanics and physical runners, D9.9 request/editorial resolution where valid, and D3 audio under separate gates. Do not switch branches or refs.

Read in this order:
1. `AGENTS.md` and `.continue/rules/CONTINUE.md`.
2. `docs/current/e/README.md` and `docs/current/e/C11E_CURRENT_AUTHORITY_20261030_V4.md`.
3. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261030_V4.md`.
4. `docs/current/e/C11E_E0_REVIEW_AND_E1_SOURCE_ARCHITECTURE_20261030_V1.md`.
5. `docs/current/e/C11E_DOCUMENTATION_RECONCILIATION_20261030_V4.md`.
6. `docs/history/c11d/C11D_TO_C11E_ROADMAP_TRANSITION_20261030_V1.md`.
7. Charter, architecture contract and risk register V3; then C11-C frozen contracts.
8. `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261030_V4.md` for a new context window.

## Authority and invariants

C11-C 2.19.12 remains the production baseline until E8 formal acceptance, freeze and promotion. Preserve `release/C11C_FREEZE_PACKAGE_MANIFEST.json` SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes. Never edit the frozen package/manifest or extract a snapshot over the checkout.

D receipts/locks remain immutable and scoped to D. D9.10 and `shared_production_context_service.py` remain preparation-only; do not convert them into an E dispatcher. E owns its service, receipts and gates. E tests do not promote a release.

Keep five existing `c11c-suite` modules; no `c11d-control` or sixth suite module. GUI and CLI call one canonical E production service. Reuse C generators and visual consumers. Do not mutate `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, gameplay RNG, mechanics, challenge definitions or timing to support editorial fields. Do not enumerate/serialize arbitrary `FrameSnapshot.custom_data`.

`request.seed` and `request.music_seed` are separate. First visual proof is `CHALLENGE_001`, with `title` displayed in its own dedicated editorial slot, not mapped to `content.hook`. `CHALLENGE_008/009` remain excluded until the declared 11 s versus phase sum 12 s conflict is resolved.

## Gates and execution

E0 is verified PASS. E1 is active service/API/parity work and has no physical renderer dispatch. E2 permits only two isolated Challenge renders for title A/B; E3 adds D3+FFmpeg mux; E4 separately adds Loop and Drill. E5 regression/determinism, E6 Smoke 18, E7 Matrix 101 and E8 acceptance follow in order. Do not inherit PASS across gates.

Use Windows PowerShell 5.1 and complete pasteable blocks. No `&&`, `Read-Host` or PowerShell 7-only syntax. Prehash every source; stop on mismatch. Capture real exit codes, stdout/stderr, tool versions, hashes and receipts. No reset/clean/forced checkout. No commit/push unless specifically directed.
