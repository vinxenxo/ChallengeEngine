# C11-C 2.19.12 — Full Context Pack

Open a new context with this pack when the 2.19 consolidated candidate is the active state.

Authoritative status: **CANDIDATE — NOT FROZEN**.

The operational implementation lives in `c11c-suite/`. `c11c-studio/` is retired and must not be modified or used.

Read `MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md` first, then `START_PROMPT_C11C_2.19_CONSOLIDATED.md` and the files listed in `C11C_2.19.12_CONTEXT_INDEX.md`.

The required parallel review semantics are non-negotiable: `Workers=7` is genuine concurrent capture; each worker gets a private temporary Godot project root; `WorkerRoot` is canonical; no global mutex and no serial fallback.
