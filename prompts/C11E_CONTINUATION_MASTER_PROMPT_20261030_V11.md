# C11-E — continuation master prompt V11 (E0 full-family restart)

Continue on the real Windows checkout `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`, branch `main`. Do not reset, clean, switch branches, move refs, commit or push. C11-C 2.19.12 remains immutable; manifest 796318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Product mission

Produce final audiovisual MP4s for all three families: Challenges, Visual Loops and Visual Drills. Each must retain the actual C mechanics, timing, family-specific binder and C presentation; visibly consume the enabled D9.8 editorial fields in correct visual slots; use D3 Music V5 with independent `request.music_seed`; mux using FFmpeg; validate using FFprobe; and preserve complete provenance. GUI and CLI call one canonical E production service.

## Current state at E0 restart

- E1 service is committed in `a3c7c5d284a96ce115ca52208b4039002502753b` (parent `bc8330e794fe37efe0c4f9c2bb0c0bd389f28f2c`). Existing E1 install 8/8 and Windows tests 2/2 PASS; manual GUI observation pending.
- E2 V4 overlay is installed 21/21 and path guard 4/4 PASS. Its physical run failed before Python. No sidecars, AVI, MP4, pixel comparison or valid failure ZIP exist.
- Root cause was multi-result `Get-Command python` (`Python313` + WindowsApps) converted to one invalid ProcessStartInfo FileName. Python 3.13.14, Godot 4.7.1 Mono and FFmpeg 9/FFprobe individually launch.
- E0 re-entry V2 package repairs only process resolution/diagnostics and corrects the archive copy step. Do not apply V1; do not re-run V4; after E0 V2 install use a NEW RequestId for E2.

## Enabled D9.8 fields

All families: `title`, `subtitle`, `call_to_action`, `language`; Challenge only: `player_name`, `challenge_label`. Reserved hook/preparation/final/header/footer/show flags remain disabled. Title never replaces hook or CTA. Reuse D9.9 for its existing Challenge request schema. E must explicitly adapt Loop grammar/family and Drill type/tier requests; do not label those accepted by D9.9 already.

## Full-family roadmap

E0 rebaseline; E1 common service; E2 Challenge editorial pixel A/B; E3 Challenge D3 music/mux; E4A Challenge full A/V; E4B Loop full A/V; E4C Drill full A/V; E5 deterministic/regression; E6 Smoke18 (six per family); E7 Matrix101 (54 Challenge +27 Loop +20 Drill; CH_008/009 remain held due 11 s/12 s mismatch); E8 separate independent formal acceptance/freeze/promotion.

## Non-negotiables

Keep five existing `c11c-suite` modules. No `c11d-control` or sixth module. Do not mutate `SimulationResult`, `winning_frame`, `close_calls`, mechanics, gameplay/structural RNG, frame stream or protected C. Never enumerate arbitrary `FrameSnapshot.custom_data`. `request.seed` and `request.music_seed` are independent. D records remain unchanged (D9.10 PREPARE_ONLY, D4.8/D9.14/D9.16/D9.17/D10 blocked as already recorded; release authority none). Longform disabled.

## Execution quality

Windows PowerShell 5.1 only. Each package must be self-contained and hash-pinned, each installer must archive preimages actually before replacement, preflight all destinations before first write, and each runner must resolve one native executable and log the full Process.Start context. Capture real exit codes immediately; no verification/render after failed install; no manually printed PASS. Evidence ZIPs require existence, nonzero size, readable entries and hash before reporting. Do not claim PowerShell/Godot execution by the assistant.
