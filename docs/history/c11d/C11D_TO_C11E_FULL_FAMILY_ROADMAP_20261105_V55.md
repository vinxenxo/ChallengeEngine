# C11-D to C11-E Full-Family Roadmap — V55

**Product outcome:** one canonical C11-E GUI/CLI service for Challenge, Visual Loop and Visual Drill. C11-C mechanics/generators/binders remain authoritative and unchanged. D supplies presentation/editorial and family-aware music integration; E coordinates service, FFmpeg mastering/mux, FFprobe QA, provenance and receipts.

## Current position

- E0–E3 accepted in their recorded scopes.
- E4A.2, E4A.3D.1, E4A.4 and E4A.5B accepted in their recorded test-only/read-only scopes.
- E4A.6 live-root: 900 frames, one mount; the reserved-band correction is D-only.
- V2 Windows run: PowerShell 5.1 AST PASS; 22/22 focused tests; Godot 4.7.1 editor import PASS; live-root 900/900 with 900 black-band frames; Movie Maker completed 900/900 frames and wrote its AVI.
- V2 wrapper blocked after capture because a path-based log validator was given an in-memory stdout string. This is a false-negative in the orchestration helper, not a capture/consumer failure.
- Recovery-only V1 stopped on the obsolete Git HEAD. V1.1 removed Git checks and passed its evidence/source preflight, but then stopped twice at documentation preflight: the first run lacked the external manifest beside the script; the second had the manifest but not its referenced docs/prompts tree. Neither V1.1 attempt reached media processing or wrote source/docs. V1.2 embeds the compressed documentation package and self-extracts it under its unique evidence run root; only the `.ps1` in Downloads is needed. No Git checks, test reruns, Godot or Movie Maker recapture.

## Ordered gates

1. **E4A.6 black reserved bands:** recovery-only V1.2 validates exact V2 evidence/source pins and self-hydrates its embedded docs; discards AVI audio; produces a 720x1280/30 FPS/450-frame H.264 silent MP4; creates eight boundary stills; audits inactive black bands and active HOOK/CTA; installs versioned docs add-only. The bounded visual gate is `PASS_TEST_ONLY_RESERVED_BANDS_BLACK_CAPTURED` only with its recovery receipt. Operator has confirmed the visual result is correct. This is not full E4A.
2. **Full E4A Challenge A/V:** corrected D-composited MP4 unchanged (never the earlier uncomposited E4A.4 C11-C input) + re-pinned active D3 V5 engine + D3.3 mastering + accepted E4A.4 mux/FFprobe method/predicates; A/B same music seed, C changed music seed; audio A/B repeatability/C difference; identical H.264 elementary stream/frame identity; AAC-LC 48 kHz stereo; non-silence; 15 s; <=0.15 s A/V drift; human visual/listening disposition and E1 GUI/CLI parity.
3. **E4B Visual Loop:** integrate presentation/editorial/music while preserving existing binder, grammar and variant timeline.
4. **E4C Visual Drill:** integrate presentation/editorial/music while preserving existing binder, phase timeline and END_CTA precedence.
5. **E5:** cross-family repeatability, gameplay/music seed separation, profile/adapter non-leakage and GUI/CLI parity.
6. **E6 Smoke18:** six audiovisual cases per family.
7. **E7 Matrix101:** 54 Challenge + 27 Loop + 20 Drill. CH_008/009 remain held pending explicit resolution of declared 11 s versus 12 s phase sum.
8. **E8:** complete historical C-to-E regression reconciliation, independent acceptance, immutable freeze and separately authorized promotion.

## Invariants and governance

Never modify C11-C simulation truth, RNG, mechanics, protected binders, frame stream, shared C11-C editorial layer or family timelines. `request.seed` and `request.music_seed` remain independent. No sixth suite surface, second Producer or parallel binder. The HEADER/FOOTER reserved bands remain black while the optional D envelope is enabled; the body/video background colour can become user-configurable as a separate future feature. Per-iteration runners do not inspect Git; the operator commits each iteration. Production renderer/dispatch/media OFF; `release_authority=NONE`. Active `GeneradorMaestro.gd` still differs from the frozen C11-C manifest entry; do not rewrite it as part of E4A.6.
