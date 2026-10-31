# C11-E — current engineering authority (V11)

## Mission: the finished three-family producer

Deliver one coherent GUI/CLI production workflow that creates final audiovisual MP4s for **Challenges, Visual Loops and Visual Drills**. Every family must use its existing C mechanics, timing, frame stream, presentation binder/profile and physical generator; add the enabled D editorial values in the proper family-specific visual slots; generate music with D3 using the independent `request.music_seed`; mux with FFmpeg; validate with FFprobe; and retain hash-bound provenance. C11-C remains the immutable production baseline until E8 is formally accepted and promotion is explicitly decided.

## Authority and read order

1. This file and `.continue/rules/CONTINUE.md`.
2. `docs/current/e/README.md`.
3. `docs/current/e/C11E_CURRENT_AUTHORITY_20261030_V11.md`.
4. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261030_V11.md`.
5. `docs/current/e/C11E_PRODUCT_SCOPE_PRESENTATION_EDITORIAL_MUSIC_20261030_V1.md`.
6. `docs/current/e/C11E_EXECUTION_HYGIENE_AND_ASSISTANT_ERROR_LOG_20261030_V7.md`.
7. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261030_V1.md`.
8. The relevant C source, family binder, physical runner, D9.8/D9.9 contracts and D3 music contracts.
9. `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261030_V11.md` for a new context.

## Architecture

- Work on the user's selected local `main`; never reset, clean, force-checkout, move refs, create/delete branches, commit or push by automation.
- Keep the five existing `c11c-suite` modules. No sixth module and no `c11d-control`.
- GUI and CLI call one canonical C11-E production service. They must not have separate production implementations.
- Reuse the real C generators, deterministic mechanics, family-specific binders, presentation profiles and Godot Movie Maker capture. E adds request/editorial/audio orchestration, not a second gameplay engine.
- Reuse the canonical D9.8 editorial field semantics; reuse D9.9 where its existing Challenge request schema applies. Do not claim Loops/Drills are already accepted by D9.9: E must explicitly add and test the missing family request adapter/dispatch while preserving universal semantics.
- Reuse D3 Music V5 and FFmpeg mux. `request.seed` and `request.music_seed` are distinct; neither may derive from or replace the other.

## Immutable C and D boundaries

- C11-C freeze manifest remains exactly 796318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Do not alter `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, gameplay/structural RNG, mechanics, source definitions, phase durations or protected C files.
- Never enumerate/serialize arbitrary `FrameSnapshot.custom_data`.
- Keep D governance/history untouched: D9.10 `PREPARE_ONLY`; D4.8, D9.14, D9.16, D9.17 and D10 retain their recorded blocked/no-go states; no D release authority is implied by E tests.
- CHALLENGE_008/009 remain excluded pending explicit resolution of 11-second declared duration vs 12-second phase sum.

## Enabled editorial scope

All three families: `title`, `subtitle`, `call_to_action`, `language`. Challenges additionally: `player_name`, `challenge_label`. Reserved `hook`, preparation/final text, header/footer lines and show/hide flags remain disabled. Never map title into C's hook or CTA. Each field must reach its own approved visual slot via the real family's presentation model/binder.

## Required product acceptance

A family is not accepted by a plan, sidecar, unit test or synthetic image. It needs real family generator + binder execution, a final MP4, editorial pixel proof, music WAV made with `music_seed`, muxed A/V MP4, FFprobe stream/geometry/FPS/duration/audio checks, content review and hash-bound provenance.

## Work method

1. E0 reconciles the actual checkout and receipts without resetting history.
2. E1 establishes/validates the common service.
3. E2 isolates Challenge title-to-pixels.
4. E3 proves D3 music/mux on Challenge.
5. E4A/E4B/E4C prove one complete A/V editorial render per family.
6. E5 determinism and regression; E6 Smoke 18; E7 Matrix 101; E8 independent acceptance and promotion decision.

Make the smallest code change that unlocks a functional test. Before sharing a script, inspect the complete PowerShell 5.1 file; pin current commit ancestry/receipts and exact file hashes; validate every destination before writing; use one self-contained package/command; capture actual native process path/args/cwd/exit code; never claim PASS or evidence ZIP unless the verified receipt/artifact exists. A later `Write-Host PASS` cannot override a failed exit code. When the assistant cannot run Windows PowerShell/Godot, say so.
