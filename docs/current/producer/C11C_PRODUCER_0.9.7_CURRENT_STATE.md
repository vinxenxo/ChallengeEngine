# C11-C Producer 0.9.7 — Current State / C11-C 2.19.6 Candidate

## Authority

The live Producer is `c11c-suite/c11c-producer/`.

The current repository is **C11-C 2.19.6 final repair candidate — NOT FROZEN**. Producer version remains **0.9.7**.

## Runtime / capture

- orchestration-only;
- temporary AVI Movie Maker capture;
- project-local `--path .`;
- no explicit `--resolution` on the proven single-Drill route;
- stable-file waiting;
- FFmpeg video-only source conversion;
- family music generated/muxed separately;
- AVI removed with scratch stage.

## Editorial hook

Canonical source: `profiles/presentation/c11c_visual_hooks.json`.

The Producer does not read `authoring.json.content.hook`.

The shared Movie Maker helper is intentionally lock-free. Parallel Art Direction uses separate temporary worker project roots, so no project-global mutex is required or permitted.

## Suite ownership

Producer GUI/launcher sources live under `c11c-suite/c11c-producer/`. Canonical BAT launchers set `C11C_PROJECT_ROOT`, change directory to the repository root, and preserve the child exit code. No operational path requires `c11c-studio`.

## Visual review relationship

The Producer can invoke the canonical Art Direction review runner. Its 2.19.6 concurrency implementation is owned by `tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1`, which isolates each concurrent Movie Maker process in a private temporary Godot project root.

## Validation provenance

Previously recorded Windows/Godot 4.7.1 single-Tracking Producer smoke: seed `452878546`, T1, constant, S140, `MASTER_1080` → **FINAL PRODUCT PASS**. That evidence remains valid as historical runtime evidence; it does not by itself freeze the 2.19.6 candidate.

## Boundary

Do not add presentation-side or Producer-side gameplay calculations. Any requirement crossing the frozen C11-B/C boundary requires an explicit checkpoint.
