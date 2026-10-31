# Transición C11-D → C11-E — roadmap funcional de las tres familias (V1)

## Intención original preservada

C11-D definió una capa editorial universal, perfiles de presentación y D3 Music sobre el motor/generadores físicos C11-C. D9.8 fijó el modelo editorial; D9.9 introdujo la resolución universal; D9.10 quedó en preparación, no en render. D9.1/D9.2 y D9.14 demostraron que los generadores C, D3 y FFmpeg pueden producir medios físicos, pero no demostraron que los valores del formulario universal llegasen a los píxeles. C11-E debe cerrar esa brecha para Challenge, Loop y Drill.

## Programa E

- **E0 — Rebaseline:** checkout actual, branch/HEAD/parent, C manifest, E1/E2 receipts, live source pins, toolchain, current worktree and error register. No rollback.
- **E1 — Shared service:** one request/intent/production service for GUI and CLI; normalized selection, profile, delivery, editorial inheritance, independent seeds and provenance. Add family-specific producers without forking GUI/CLI semantics.
- **E2 — Challenge visual proof:** title in an independent editorial presentation slot; A/B MP4, same gameplay/config/seed, title-only pixel difference; no audio in this isolating gate.
- **E3 — Challenge A/V:** D3 Music V5 plus FFmpeg mux; prove independent `music_seed`, valid streams and gameplay pixels unchanged when music seed changes.
- **E4A — Challenge family production:** full presentation/editorial/music path with canonical Challenge generator and runner.
- **E4B — Visual Loop family production:** full path through Loop binder, family+grammar identity and C render consumer; D3 audio/mux.
- **E4C — Visual Drill family production:** full path through Drill binder, type+tier identity and C render consumer; D3 audio/mux.
- **E5 — Determinism/regression:** same request/seeds reproduce expected hashes/frames; music-seed-only change alters audio but not gameplay; editorials affect only approved regions; three-family GUI/CLI parity.
- **E6 — Smoke 18:** six representative executions per family, including A/V media QA and provenance.
- **E7 — Matrix 101:** 54 Challenges + 27 Loop grammars + 20 Drill variants. CH_008/009 are held; until 11 s vs 12 s timing discrepancy is resolved, runnable scope is 99 and Matrix 101 remains open.
- **E8 — Formal acceptance:** independent review, release/freeze eligibility, explicit approval and promotion decision. No earlier gate authorizes baseline replacement.

## Architecture constraints

GUI/CLI → one C11-E service → canonical request/editorial resolution → family-specific E presentation adapter → existing C mechanics/frame stream/binder/generator → Godot Movie Maker capture → D3 WAV generation with independent music seed → FFmpeg mux → FFprobe/visual/audio review. D9.9 is reused where its request schema applies; the D9.8 model's Loop/Drill selection data is not misrepresented as an already accepted D9.9 plan. E must add the missing universal family request/dispatch integration under E contracts.

Do not alter protected C mechanics, `SimulationResult`, `winning_frame`, `close_calls`, RNG or frame-stream semantics. Do not serialize arbitrary `custom_data`. Keep C11-C manifest immutable. Preserve D's old preparation/authority records unchanged.
