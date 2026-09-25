# C11-C CHANGELOG — 2.11.0

## 2.11.0 — Hooks, canonical naming, social copy and music refinement

### Visual Drill hooks
- Added canonical hook bank with exactly 10 hooks per Visual Drill family.
- Deterministic selection uses `posmod(seed + family_offset, hook_count)`.
- The selected hook is rendered in Header and reused verbatim as the first line of the social sidecar.

### Social delivery
- Fixed hashtags on every current C11-C video: `#GenerativeArt #GodotEngine #LoopArt #OddlySatisfying`.
- Family/subfamily-specific hashtags are appended deterministically.
- Public `.txt` output is now publication-friendly copy; internal QA metadata remains in the render manifest rather than polluting the social post.

### Visual Loop nomenclature
- Canonical crosswalk is technical_id → artistic_name → runtime_id → production_id.
- The five historical families remain exactly five families.

### Music
- `FAMILY_MUSIC_V3` compatibility mode retained; generator revision raised to 3.3.0.
- A-minor pentatonic frequency bank.
- Full soft ADSR pad envelope with long attack/release.
- Deterministic low-frequency value noise, including cyclic loop-safe noise.
- Richer harmonic presence for mobile audibility.
- Slow deterministic stereo motion limited to ±0.16.
- Loop-safe frequency/phrase treatment and stabilized periodic low-pass stage.
- Visual Drills use family + seed; Visual Loops use visual grammar + seed. The editorial hook never drives audio.

### Packaging
- This release is delivered as a file overlay only; no full-project ZIP is required.

### Scope protection
No changes to C11-B simulation truth, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, structural RNG, C9 authoring semantics or C7 ownership/contracts.
