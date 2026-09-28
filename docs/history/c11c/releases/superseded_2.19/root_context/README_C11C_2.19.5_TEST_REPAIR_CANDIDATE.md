# C11-C 2.19.5 — Final Repair Candidate Pointer

This file is retained as a root-level continuity pointer. The single current authority for the 2.19 branch is the consolidated 2.19.5 documentation set.

Read first:

- `C11C_2.19.5_CONTEXT_INDEX.md`
- `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.5_CONSOLIDATED.md`
- `docs/master-prompts/START_PROMPT_C11C_2.19.5_CONSOLIDATED.md`
- `docs/current/c11c/C11-C_2.19.5_CONSOLIDATED_STATE.md`

The final repair preserves genuine `Workers=7` concurrency using one temporary Godot project root per worker. `C11CMovieCapture.ps1` is lock-free; the rejected global mutex experiment must not return. The worker helper uses `${i}:`, never `$i:`.

The active Suite surface is `c11c-suite/`. `c11c-studio/` is retired and must not be updated or used.

Runtime acceptance and the final freeze seal are defined in `docs/current/c11c/C11-C_2.19.5_FREEZE_COMMANDS.md`.
