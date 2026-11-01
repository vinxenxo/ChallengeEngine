# C11-E Continuation Master Prompt — V22 (2026-11-02)

## Mission

Complete C11-E as a production-ready, governed integration for the entire product: Challenge, Visual Loop and Visual Drill. Preserve the C11-C 2.19.12 generators/mechanics and add the C11-D universal presentation layer, editable universal editorial fields and D3 Music V5. CLI and GUI must call the same shared production service. Final outputs must be MP4 with validated audio/video mux and synchronization. CHALLENGE_001 A/B is only the first presentation/editorial control, not the final scope.

## Authority order

1. Active Windows checkout: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`.
2. `AGENTS.md` and `.continue/rules/CONTINUE.md` (read both; V21/V22 E rules may be more restrictive than the historical C baseline).
3. `docs/current/e/C11E_CURRENT_AUTHORITY_20261102_V22.md`.
4. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261102_V22.md`.
5. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261102_V12.md`.
6. V22 E2 R4 receipt/visual review and the exact source pins recorded within.
7. Earlier immutable contracts, receipts, pins and gate artifacts.

If any document conflicts with the active checkout or a more authoritative immutable artifact, stop and reconcile it with a separately recorded decision. Do not guess.

## Immutable C11-C baseline

`release/C11C_FREEZE_PACKAGE_MANIFEST.json` must remain exactly 796,318 bytes with SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. C11-C 2.19.12 stays the production authority until E8 independent acceptance, formal freeze and promotion. Never copy a snapshot ZIP over the checkout. Never change protected C11-C mechanics/generators to make an E test pass.

## Current checkpoint

E2 R4 automated physical run passed with the following immutable references:

- RequestId `C11E-E2-CH001-AB-20261101-V9-R4`.
- Receipt SHA-256 `2f8c355453d8558c6af42aa5da35f603b767726d64ba04f842dc799a2cadef7f`.
- Evidence ZIP SHA-256 `f33431bb131697baf9dc3df6ed1ed8e4ca14ecb40d7b9ef07c812a5bca67a3de`.
- R4 checkout branch/head `main` / `7fbdf8529d2af6ba7089eacd8fd9b38682466d84`.
- Runner SHA-256 `158325324626085ebf319f68906ca8778f9a08eb39c6e8441da146c12ee4f953`.
- Python E2 test SHA-256 `ab4ed3fd421ef0cac86d4ef25167f0161a186ef5bd90373414abed7bea17d2a9`.
- Godot numeric test SHA-256 `73fc4421f6ebfec8e3f458123600663cc772838731f57e240ef22abbebf2ef3b`.
- Godot JSON numeric 30/30; Python contract 9/9; both runners/render rows successful.
- Exactly two CHALLENGE_001 A/B renders with same gameplay seed 193847 and music seed 840001; title is the only request difference.
- Gameplay crop identical 540/540 source frames; title slot different 540/540; surrounding header areas identical; final MP4s differ 270/270 frames.
- Both delivery MP4s are H.264 High, 720×1280, 30 fps, 270 frames, 9 seconds, `yuv420p`, `color_range=tv`, no audio. E2 intentionally has no soundtrack.

Independent sampled visual review found no obvious issue across 18 decoded frames plus six receipt PNGs. The operator's full playback sign-off is still PENDING and must be separately recorded. This prompt does not authorize marking the receipt field as complete or starting E3 execution early.

## Next permitted work

After operator approval of both complete MP4s, inspect the actual D3 Music V5 source, contract, schemas, sidecars, validators, tests and current hashes. Produce a read-only preflight and acceptance matrix. Only then implement or run the smallest separately governed E3 gate. Do not invent contract fields or technical settings.

E3 proves independent music seed, deterministic audio selection/render, music-only seed variation with gameplay invariance, FFmpeg mux through the shared service, FFprobe validation of both streams and A/V timing, and the required negative/reproducibility cases. Every physical attempt uses a new RequestId. Preserve failed evidence.

## Downstream full-family gates

- E4A Challenge adapter
- E4B Visual Loop adapter
- E4C Visual Drill adapter
- E5 cross-family determinism, seed isolation and CLI/GUI parity
- E6 Smoke18 (six per family)
- E7 Matrix101 (54 Challenge, 27 Loop, 20 Drill)
- E8 independent acceptance, freeze and formal promotion

CH_008/CH_009 remain held because declared duration 11 seconds conflicts with summed phases 12 seconds (`3+7+0+2`). Current valid set remains 99 unless explicit authority resolves this.

## Permanent locks and engineering constraints

- `release_authority=NONE`; no baseline promotion or freeze eligibility before E8.
- Do not alter the C11-C frozen manifest or protected C11-C mechanics/generators.
- Work in the governed `c11c-suite`; no `c11d-control`.
- GUI/CLI use the same service adapter, never parallel production implementations.
- `winning_frame` is only a temporal anchor; `close_calls` is only an episode count.
- No automatic seed generation; gameplay and music RNG domains stay independent with no cross-consumption.
- No stale PASS, no inferred approvals, no evidence overwrite, no reused RequestIds.
- PowerShell 5.1 safe: no `&&`, no `Read-Host`; use robust process capture when native stderr could trip `$ErrorActionPreference='Stop'`.
- Prefer one meaningful, source-pinned overlay per real engineering change. Do not repeat installers/documentation without material evidence change.
