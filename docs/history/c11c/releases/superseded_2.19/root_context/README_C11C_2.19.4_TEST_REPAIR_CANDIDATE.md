# C11-C 2.19.4 — Test / Repair Candidate Readme

This file is a handoff aid for the consolidated 2.19.4 candidate.

The key regression behind the current candidate was not a visual-loop generator failure. The project-global Movie Maker `override.cfg` was unsafe for concurrent workers, and the 2.19.3-v2 mutex workaround made `Workers=7` effectively one-at-a-time.

The current design uses `C11CReviewWorkerIsolation.ps1` to create a separate temporary Godot project root for each worker. The canonical Art Direction runner then launches each worker-local prototype from that root.

The retired `c11c-studio/` tree is excluded and must not be modified. Active Suite changes are under `c11c-suite/`.

See:

- `docs/current/c11c/C11-C_2.19.4_CONSOLIDATED_STATE.md`
- `docs/current/c11c/C11-C_2.19.4_ACCEPTANCE_GATE.md`
- `docs/master-prompts/MASTER_HANDOVER_C11C_2.19.4_CONSOLIDATED.md`
- `docs/master-prompts/START_PROMPT_C11C_2.19.4_CONSOLIDATED.md`
