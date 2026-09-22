# C11-C — Consolidated Changelog v2.0.1 → v2.1.4

## v2.0.1 — Editorial/audio/social baseline
- Seed-driven editorial header/footer text and real variation terms.
- Deterministic Matrix/airport-board transition on header hook.
- Expanded cyberpunk/geek/steampunk vocabulary tied to active parameters.
- Default deterministic ambient audio with `-NoSound` / `-Silent` opt-out.
- Social sidecar generated per video with exact reproduction command.
- 18 s / 30 FPS / 540-frame review baseline.

## v2.0.2–v2.0.5 — Stability/editorial hotfixes
- Editorial animator reference corrected.
- Fractal and Invisible Forces shader symbol failures corrected.
- BOM-safe social manifest reading.
- Palette-derived editorial colors restored and intensified.
- Header/footer decorative rules restored.
- Repeated `VISUAL LOOP // FAMILY` footer line removed.
- Exactly one canonical final MP4 per run; silent intermediates moved to OS temp.
- Artifact cleanup/reset separated from rendering.

## v2.0.6 — Social delivery feedback
- Social output prepared for 720x1280 delivery.
- Mobile palette treatment increased saturation/luminance.
- Mobile-safe ambient audio introduced to reduce perceived speaker resonance/coupling.

## v2.1.0–v2.1.3 — Toolchain separation/consolidation
- Prototype/review/production workspaces separated.
- Final products protected under `artifacts\production\audiovisual`.
- PowerShell parser and delivery validators added.
- Superseded versioned launchers retired.
- Temporary `override.cfg` used so frozen `project.godot` remains unchanged.

## v2.1.4 — Physical-validation correction
- Corrected Godot Movie Maker CLI syntax to `--resolution 720x1280` as one argument. The prior split `720`,`1280` representation was invalid.
- All five family launchers now use the same resolution contract.
- Multiseed/review/production child-script calls use typed hashtable splatting to avoid Windows PowerShell array/switch binding errors.
- Canonical preflight validates parser, delivery contract, and absence of obsolete versioned launchers.
- Review generation remains non-destructive except for explicit `-ResetReviewAssets` targeting only its own review-assets directory.
- No C11-B/C7 boundaries reopened.

## Deferred
- Seed/geometry-dependent variable loop duration (short/medium/long) is intentionally deferred to an independent future contract.
- Art Direction 2.0 starts from the new 25-video corpus after this toolchain validation pass.
