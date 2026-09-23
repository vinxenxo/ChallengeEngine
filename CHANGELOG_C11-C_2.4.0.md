# C11-C 2.4.0 — Visual Drill preparation + Tracking production baseline

- Reused the established Challenge 3/2/1 countdown behavior through a shared presentation logic layer.
- Applied the countdown to all four Visual Drill families.
- Added family-specific instruction text during the 3-second pre-roll; Tracking uses the approved follow-the-object instruction.
- Set C11-C Visual Drill canonical gameplay delivery to 17s / 510 frames, producing 20s / 600 frames including the 3s countdown.
- Kept the generic C10-A authoring adapter and its historical short-duration tests unchanged.
- Tracking remains smooth pursuit with bounded Lissajous 2:3 motion, reduced-speed baseline and growing-history trail.
- Tracking Body now fills the complete 540px logical width; Tron depth and mobile-safe palettes remain presentation-only.
- Updated Visual Drill review tooling to validate 17s gameplay, 3s countdown and 20s total output; shared ambient review audio is generated for 20s.
- Added dedicated countdown and Tracking presentation contract tests plus playback watchdog assertions.
