# C11-E — current authority (V16)

**Cut-off:** 2026-10-31. **Snapshot identity:** `main` / HEAD `b92434d6a8b50cef7e49ba6b75a4813777927fe7`, parent `a3c7c5d284a96ce115ca52208b4039002502753b`, commit tree `91aa803c2d675ec9fc7afff120b2bc7d3de479ef`. The supplied filtered snapshot was captured at `2026-10-31T18:17:27Z` (19:17:27 Europe/Madrid), size 9,618,925 bytes, SHA-256 `250c154ddb74813a7478d9aeb03ddaac7ccd15595c82bbfad607552f048408b5`; its sidecar and report agree. It is context, not an authority to overwrite the active checkout.

## Product objective — unchanged and complete

Deliver final audiovisual MP4 production for **Challenges, Visual Loops and Visual Drills**. Retain the existing C11-C generators, simulation mechanics, frame streams, deterministic gameplay and presentation binders. Add the D presentation/editorial layer using the correct family-specific adapters; consume enabled D9.8 fields in their own visual slots; generate D3 Music V5 from independent `request.music_seed`; mux with FFmpeg; verify with FFprobe; and keep GUI/CLI on one shared C11-E production service. CHALLENGE_001 A/B is only the first technical integration control, not the product or an acceptable endpoint.

## Authority and immutable boundaries

- C11-C 2.19.12 remains the production baseline until E8 is independently accepted, frozen and explicitly promoted. Its manifest remains exactly 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- Do not change protected C generators, C mechanics, `SimulationResult`, `winning_frame`, `close_calls`, frame stream, RNG domains, source definitions, timing, or D governance/release records.
- D locks remain as previously recorded: D9.10 `PREPARE_ONLY`; D4.8, D9.14, D9.16, D9.17 and D10 are not promotion authority; release authority `NONE`.
- Keep only the five existing `c11c-suite` modules. No `c11d-control` or sixth module. Do not reset, clean, switch branch, rebase, amend or push to satisfy a gate.

## Verified E0/E1 baseline

E0 re-entry commit `b92434d` remains a direct child of E1 foundation commit `a3c7c5d`. E0 V2 receipt SHA-256 `869a099c6d73e9b9230db954e68707e3b079db82c368dd151806f8e10a9c8315`. E1 automated Windows tests 2/2 pass, with manual GUI operator observation still pending. Do not repeat accepted E0/E1 work.

## E2 V7 physical result — FAILED, not accepted

- Run: `C11E-E2-CH001-AB-20261031-V7`; branch `main`; runtime HEAD `b92434d6a8b50cef7e49ba6b75a4813777927fe7`; parent `a3c7c5d284a96ce115ca52208b4039002502753b`.
- Failure ZIP: `C11E_E2_CH001_AB_FAILURE_EVIDENCE_20261031_191440_13012eef.zip`; 29,568 bytes; 47 entries; SHA-256 `27fa769c35165e8171120bc0fce16fc3739505198157a874360c2de432c6bbe7`.
- Python pair contract tests passed 9/9; pair preparation, Python 3.13.14, Godot 4.7.1 Mono, FFmpeg and FFprobe were resolved/launched successfully. No conversion/mux or B render followed.
- Godot started the A renderer and produced a 12,374-byte AVI fragment with only one recorded frame, then stderr reported `[C11E_E2] Editorial sidecar contract validation failed.` at `C11EChallenge001E2.gd:62`; Godot exited 40. Failure diagnostic proves renderer invocation count 1, media path recorded, `media_accepted=false`, release authority `NONE`.
- The sidecar values and all other validator predicates match the expected contract. Root cause: Godot's `JSON.parse_string()` represents JSON numeric values as `TYPE_FLOAT`; the E2 validator required both seed values to be `TYPE_INT`. Thus otherwise-valid JSON seeds `193847` and `840001` failed type checks. This is a GDScript validation defect, not a malformed request, GPU failure, or operator error.
- There is no E2 success receipt, no final MP4 pair, no A/B pixel proof and no human review. The later interactive-console checks after the runner's nonzero exit attempted to read a nonexistent success receipt and ended with an unconditional `Write-Host ... PASS`; those commands are invalid and must not be used as evidence.

## V8 JSON-number remediation — prepared, installation pending

The V8 overlay changes only the E-owned E2 validator/runner and E documentation/instructions. GDScript accepts `TYPE_INT` or `TYPE_FLOAT` only when finite, positive, mathematically integral and within 1..2,147,483,646. A new Godot-native headless test JSON-round-trips a complete valid E2 sidecar, asserts Godot returns floats, calls the actual sidecar validator, and rejects decimal, zero, negative, string, boolean, non-finite and out-of-range seeds in both domains. The V8 runner pins both E2 scripts and invokes that test before Python preparation or physical render. The retry uses fresh RequestId `C11E-E2-CH001-AB-20261031-V8`; V7 output remains immutable.

After installing V8 and committing the iteration locally, the next gate is one controlled E2 V8 execution only. No E3 until a valid two-render A/B output, FFprobe and frame-difference controls, provenance, and independent visual review are accepted. Failure remains failure; never follow an error branch with success verification or a manual PASS.

## Full product roadmap

After E2 acceptance: E3 Challenge D3 Music V5, independent music seed, FFmpeg mux and FFprobe; E4A Challenge presentation/editorial/music; E4B Visual Loop adapter/binder/editorial/music; E4C Visual Drill adapter/binder/editorial/music; E5 determinism, seed isolation and GUI/CLI parity; E6 Smoke18 (six reviewed A/V outputs per family); E7 Matrix101 (54 Challenges + 27 Loop grammars + 20 Drill variants; runnable set 99 while CH_008/009 remain held pending explicit resolution of declared 11 s vs summed 12 s); E8 independent acceptance, freeze and explicit promotion decision.

Enabled D9.8 fields: common `title`, `subtitle`, `call_to_action`, `language`; Challenge-only `player_name`, `challenge_label`. Reserved hook/preparation/final/header/footer fields and show flags remain disabled. Do not map title to hook or CTA. Loop/Drill need tested E-owned family adapters; do not pretend Challenge-only D9.9 request coverage is universal.
