# C11-E Continuation Master / Overhand Prompt — V65

Continue only in the active Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. It is the source authority. Never extract snapshots/evidence ZIPs over it. The operator controls Git; never stage, commit, reset, clean, switch branches, rebase, amend or push.

## Read first

Read root `AGENTS.md`, `.continue/rules/CONTINUE.md`, `README.md`, then Authority V67, Matrix V65, Backlog V42, Roadmap V55, Alignment V21, Postmortem V10, Plan V12, Doc Index V27, reserved-band visual requirement V5, PowerShell Runner Style Guide V3, source divergence V1 and SHA erratum V1.

## Current E4A.6 disposition

With the D editorial envelope enabled, HEADER and FOOTER reserved bands remain opaque pure black for every frame. Optional `title`/`subtitle` appear only in HOOK/HEADER; optional CTA only in CTA/FOOTER. Inactive text/rules hide while black backgrounds remain. BODY and no-envelope legacy C rendering remain unchanged. Current body/video background colour is accepted; making it user-selectable is a separate future editorial feature. Never alter the black-band invariant.

V2 Windows run evidence: PowerShell 5.1.26100.9818 AST PASS; Python 22/22 PASS; Godot 4.7.1 editor import PASS; live-root 900 frames/one mount/900 black-band frames; Movie Maker 900-frame AVI completed. The Movie Maker stdout contains CONFIGURED envelope marker, complete 180/420/180/120 phase telemetry, audio export disabled and completion. V2 overall BLOCKED was a runner false-negative: path-based `Test-CaptureLog` received `$movie.Stdout` text. Do not assert that a SUMMARY marker is missing; do not repeat source tests or renders.

Recovery V1 passed AST but blocked immediately because it pinned a previous Git HEAD. That check is invalid: the operator commits each iteration. No per-iteration runner may invoke Git, inspect HEAD/status, require `.git`, compare commit IDs, or record Git state. Recovery V1.1 removed every Git check and passed evidence/source preflight, but stopped twice at DOCUMENTATION_PREFLIGHT because the external manifest and then its referenced docs/prompts tree were missing. Neither attempt reached FFmpeg/media or wrote source/docs. Recovery V1.2 embeds the documentation ZIP and manifest; only the `.ps1` is required in Downloads. The sole outstanding E4A.6 operation is recovery-only `RUN_C11E_E4A6_RESERVED_BANDS_RECOVERY_V1_2.ps1` from Downloads. It self-hydrates the embedded documentation bundle, validates the existing evidence and AVI without consulting Git, drops the AVI's incidental PCM stream, creates/validates the silent H.264 MP4, extracts eight boundary stills, audits inactive black bands and active HOOK/CTA text, and installs versioned docs add-only. No external manifest or docs tree is needed. No source writes, Python rerun, Godot run, or Movie Maker recapture. Once its receipt reports `PASS_TEST_ONLY_RESERVED_BANDS_BLACK_CAPTURED`, do not rerun it; E4A.6 is closed only as a bounded visual test-only gate, not full E4A.

## Immediate next — full Challenge E4A A/V

Use the recovered D-composited silent MP4 unchanged; the accepted E4A.4 test used the earlier uncomposited C11-C video, so reuse only its validated mux/FFprobe method and re-pinned D3.3 predicates, never its visual input. Reconcile exact active D3 V5 engine/spec/profile and D3.3 mastering pins against the live checkout and the accepted E4A.4 mux/FFprobe contract. Generate actual D3 V5 audio and D3.3 mastering. Keep gameplay `request.seed` independent from `request.music_seed`. A/B use same gameplay/music seeds; C changes only `music_seed`. Prove A/B raw/mastered/decoded audio repeatability, C audio difference, and identical H.264 elementary stream/frame identity across A/B/C. Require one H.264 plus one AAC-LC 48 kHz stereo stream, non-silence, exactly 15 seconds, A/V drift <=0.15 seconds, complete logs/FFprobe and immutable receipt. Complete operator visual/listening disposition and E1 GUI/CLI parity before closing E4A.

## Full campaign — ordered gates

After full E4A, perform E4B Loop; E4C Drill; E5 determinism/gameplay-vs-music seed isolation/family-profile non-leakage/GUI-CLI parity; E6 Smoke18 (six A/V cases per family); E7 Matrix101 (54 Challenges + 27 Loop grammars + 20 Drill variants); E8 full C-to-E regression, independent acceptance, freeze and separately authorized promotion. CH_008/009 remain held for declared 11 s vs 12 s phase sum.

## PowerShell launcher discipline

Use Windows PowerShell 5.1 only. Read the current PowerShell Runner Style Guide V3 before authoring or debugging launchers. Never inspect Git state; exact file-level SHA pins are the required integrity control. Validate the exact packaged script with PS 5.1 before delivery. Never use `$variable:` inside expandable strings; use `${variable}` or `-f`. Keep file-path and in-memory-text helper signatures separate. Treat live-root and Movie Maker telemetry as distinct contracts. Resume from the last verified artifact; do not repeat accepted work to hide an orchestration defect.

## Invariants and governance

C11-C 2.19.12 remains frozen production authority. Never alter mechanics, RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, frame stream, family timelines, shared C11-C source, binders or C7. `request.seed` and `request.music_seed` remain independent. No sixth suite module, second Producer or parallel binder. Active `GeneradorMaestro.gd` SHA `d42782e8f5bb94ff0ede653a1c4624dc91541cc8203abf136b09a8fc288a7d82` differs from its frozen manifest entry; do not touch it; preserve this as a separate source-isolation/freeze issue. Production renderer/dispatch/media OFF; `release_authority=NONE`.


## Recovery V1.1 documentation package defect and current runner

The operator ran recovery V1.1 twice. First: `DOCUMENTATION_PREFLIGHT` said `Recovery documentation manifest is missing` because the runner was in Downloads without the companion manifest. Second: after copying only the manifests to Downloads, preflight found the manifest but not its referenced `docs/current/e/C11E_CURRENT_AUTHORITY_20261105_V66.md` payload. Both were preflight-only; no FFmpeg/FFprobe/media/source/docs writes occurred. Do not ask the operator to move manifests or folders individually.

Current recovery is V1.2, a self-contained `.ps1` with the compressed doc ZIP and its manifest embedded Base64. It verifies the embedded archive SHA, extracts and verifies all 15 docs into its run-specific evidence root, then uses those payloads for final add-only installation. Only `RUN_C11E_E4A6_RESERVED_BANDS_RECOVERY_V1_2.ps1` is required in Downloads. No other package files are runtime dependencies. It performs no Git calls/HEAD/status/.git check, no rerender, no Python/Godot/Movie Maker rerun and no runtime source writes. It reuses V2 AVI, discards incidental PCM, creates silent normalized review MP4 and audits eight stills. Wait for Windows FFmpeg 9.0 receipt before closing bounded E4A.6.
