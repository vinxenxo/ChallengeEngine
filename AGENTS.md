# C11-E — current engineering authority (V16)

## Mission: the complete three-family producer

Deliver final audiovisual MP4s for **Challenges, Visual Loops and Visual Drills**. Retain C11-C generators, mechanics, deterministic domains, timeline, frame stream and family presentation binders. Add enabled D9.8 editorial values in proper family-specific slots, D3 Music V5 driven by independent `request.music_seed`, FFmpeg mux, FFprobe checks and provenance. GUI and CLI must use one shared C11-E production service. CHALLENGE_001 A/B is only the first technical gate, not the product.

## Authority and read order

1. This file and `.continue/rules/CONTINUE.md`.
2. `docs/current/e/README.md`.
3. `docs/current/e/C11E_CURRENT_AUTHORITY_20261031_V16.md`.
4. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261031_V16.md`.
5. `docs/current/e/C11E_E2_V8_JSON_FLOAT_SEED_REMEDIATION_20261031_V1.md`.
6. `docs/current/e/C11E_PRODUCT_SCOPE_PRESENTATION_EDITORIAL_MUSIC_20261030_V1.md`.
7. `docs/current/e/C11E_EXECUTION_HYGIENE_AND_ASSISTANT_ERROR_LOG_20261031_V12.md`.
8. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261031_V6.md`.
9. Relevant C sources, family binders, D9.8/D9.9 contracts and D3 music contracts.
10. `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261031_V16.md` for a new window; master prompt for broad continuity.

## Architecture and immutable boundaries

- Work on the user's selected local `main`; never reset, clean, switch branch, move refs, rebase, amend or push. The user commits locally every iteration; bind each installer to exact package-time HEAD/parent. Runtime runners verify E0/E1 ancestry and exact source hashes.
- Keep the five existing `c11c-suite` modules. No sixth module and no `c11d-control`.
- GUI and CLI call one canonical C11-E production service.
- C11-C frozen manifest remains exactly 796318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. No edits to protected mechanics, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, RNG, C source definitions or timing.
- D governance/release locks remain unchanged; E gate passes do not confer D release authority or replace C11-C before E8.

## Editorial and audio contracts

Common enabled fields: `title`, `subtitle`, `call_to_action`, `language`; Challenge-only `player_name`, `challenge_label`. Reserved hook/preparation/final/header/footer fields and show flags remain disabled. Do not map title to hook/CTA. Loop/Drill need explicitly tested E family adapters; do not assume Challenge-specific D9.9 is universal. `request.seed` and `request.music_seed` are independent. D3 V5 creates music; FFmpeg muxes; FFprobe validates.

## Current gate state

E0 applied; E1 automated Windows tests 2/2 pass, manual GUI observation pending. E2 V7 failed at `C11EChallenge001E2.gd:62`: JSON parser float Variant vs validator TYPE_INT assumption; failure archive documents one partial-frame renderer invocation, no accepted media. E2 V8 package adds integral numeric predicate and a Godot-native preflight; installation/execution pending. E3 remains blocked until E2 has complete A/B evidence and human review.

Do not modify C baseline/governance. Do not create media in an installer. Capture process path/args/cwd/exit code. No success check after failure; no manually printed PASS. When Windows/Godot cannot be run by the assistant, say so and supply verifiable operator commands.
