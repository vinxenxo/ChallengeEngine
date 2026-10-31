# C11-D → C11-E — full-family delivery roadmap (V3)

## Product objective

Deliver final A/V MP4s for Challenges, Visual Loops and Visual Drills. Preserve the C11-C mechanics, physical generators and C presentation/binders. Route enabled D9.8 editorial fields to the correct family-specific visual slots. Generate D3 Music V5 from independent `request.music_seed`, mux with FFmpeg, validate with FFprobe. GUI and CLI use one canonical C11-E service.

## Current checkpoint and gates

- **E0:** applied; 13/13 overlay postimages and 3/3 archived V9 instruction copies verified.
- **E1:** shared GUI/CLI service installed; Windows automated tests 2/2 PASS; manual GUI observation pending.
- **E2:** Challenge-only title A/B, audio disabled. V5 passed 9 contract tests and pair preparation but failed before Godot due to `request_id` being read from the summary rather than the verified receipt. V6 runner patch fixes the schema read. V6 installer V1 failed at first replacement because File.Replace received a null backup path (0/9 applied); V6 installer V2 is prepared with a real backup path and exact failure/temp evidence pins. No physical E2 render exists yet.
- **E3:** D3 Music V5 generation, separate music-seed proof, FFmpeg mux and FFprobe A/V validation.
- **E4A:** full Challenge path using real Challenge generator/binder, presentation, allowed editorial and audio.
- **E4B:** full Visual Loop path using existing Loop grammar/generator/binder and presentation consumer.
- **E4C:** full Visual Drill path using existing Drill variant/generator/binder and presentation consumer.
- **E5:** determinism, replay, seed isolation, editorial pixel isolation, three-family regression and GUI/CLI parity.
- **E6:** Smoke18, six reviewed A/V executions per family.
- **E7:** Matrix101 (54 Challenges + 27 Loop grammars + 20 Drill variants). CH_008/009 held pending explicit resolution of the declared 11s versus summed 12s timing; current runnable scope 99 is not a complete Matrix101.
- **E8:** independent formal acceptance and explicit baseline freeze/promotion decision.

## Architecture and protected boundaries

GUI/CLI → one C11-E service → canonical request/editorial resolution → E family adapter → existing C mechanics/generator/binder/frame stream → Godot Movie Maker → D3 WAV with independent music seed → FFmpeg mux → FFprobe and human A/V review. D9.9 remains only where its Challenge request schema applies; Loop/Drill need E-owned family adapters.

Do not alter `SimulationResult`, `winning_frame`, `close_calls`, protected gameplay RNG, frame-stream semantics, Challenge definitions or C11-C manifest. Do not serialize arbitrary `FrameSnapshot.custom_data`. Enabled editorial: common `title`, `subtitle`, `call_to_action`, `language`; Challenge-only `player_name`, `challenge_label`. Reserved hook/preparation/final/header/footer fields and show flags remain disabled. Title is not hook or CTA. D governance/release locks remain unchanged.

**V3 update:** records the failed V6 V1 installer as a separate incident and the V2 installer design. This does not reduce the full three-family product target or authorize skipping E3/E4B/E4C.
