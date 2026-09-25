# CHANGELOG C11-C 2.11.1

## Copy / encoding
- Removed emoji from all active Visual Drill hooks and Visual Loop social fallback copy.
- Social sidecars are UTF-8 without BOM and preserve Spanish accented characters.
- Fixed hashtags are always present: `#GenerativeArt #GodotEngine #LoopArt #OddlySatisfying`.

## Music
- Promoted the procedural music generator to `4.0.1` while retaining the `FAMILY_MUSIC_V4` contract.
- Visual Loop grammar is now a real deterministic input to audio arrangement.
- Five loop launchers use the V4 generator.
- Drill profiles retain distinct family arrangements and gain enough presence for mobile playback without exceeding the 0.36 peak ceiling.

## Coverage
- Added exhaustive Visual Loop subtype + music coverage: 26 videos, one for every authored grammar.
- Corrected the historical Fractal coverage gap: seed 4 exercises `nested_worlds`.
- Coverage rejects duplicate audio hashes within the same family.

## Architecture
No changes to frozen C11-B truth, C9 authoring truth, `SimulationResult`, `RenderedFrameStream`, `winning_frame`, `close_calls`, `WinningFrameDetector`, or C7 ownership.
