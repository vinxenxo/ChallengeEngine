# C11-C 2.9.0 — Visual Drill Polish + Gameplay Expansion

## Status

ACTIVE / CANDIDATE — pending final Windows/Godot 4.7.1 runtime and physical review gate.

C11-B remains CLOSED / CERTIFIED / FROZEN.

## Scope

2.9.0 consolidates the Visual Drill presentation and production layer without modifying frozen Challenge simulation contracts.

### Shared presentation
- PRE_ROLL 3 s / GAME / END_CTA 3 s for all four Visual Drill families.
- Terminal CTA reuses the historical Challenge `CTAComponent`.
- Visual Drill CTA is mounted in Header.
- FooterRegion is hidden during END_CTA so the former gray footer surface cannot remain behind the CTA.
- Legacy Challenge CTA placement remains untouched.

### Typography
- New C11-C text uses Courier Regular through `C11CVisualTypography.gd`.
- C6/Challenge legacy Comic Sans configuration is preserved outside the C11-C path.
- Editorial sizing measures the active C11-C font instead of the legacy theme font.

### Visual system
- 18 semantic palettes are available per Visual Drill family.
- Seeded presentation variants can affect target/accent/editorial treatment.
- Shared procedural family-specific environments keep the stimulus dominant.
- Tracking remains free of the previously rejected Tron road while retaining its history trail.
- Pursuit uses a deep-space field plus target-anchored radial depth treatment.
- Peripheral Scan uses orbital/radar atmosphere and angular flares.

### Audio
- Shared deterministic `drill_motion_ambient_v2` master for Visual Drill production.
- No event-locked audio timing is introduced; the master is independent of family and seed.
- Mobile-safe dynamic range and restrained low/mid harmonic content are part of the profile.

### Social delivery
- Every physical review render writes `VisualDrill_<family>_seed_<seed>_social.txt`.
- The runner fails closed if the sidecar is missing.
- Sidecar records CTA placement, typography, audio state, family, seed, resolution, FPS and durations.

### Pursuit
- Authored uniform cubic B-spline.
- Arc-length LUT and normalized per-frame samples.
- Seeded control points and controlled speed modulation.
- Authored sizygia count/event frames and camouflage zones.

### Peripheral Scan
- Authored polar/logistic schedule.
- Deterministic threat/distractor events with exact frame starts.
- Answer sheet includes counts and event frame lists.

## QA additions

- Typography contract.
- Social sidecar contract.
- Expanded palette-bank contract.
- Runtime regression hardening for all four Visual Drill generator routes.

## Future cognitive-load mechanics

Tracked as authored roadmap, not renderer-only effects:

- Tracking: predictive occlusion / target morphing.
- Saccade: N-back / flash recognition.
- Pursuit: depth-scale modulation / flanker interference.
- Peripheral Scan: quadrant binning / asynchronous polyrhythm.

Each future mechanic requires explicit authored answer data and a focused contract suite.

## Version continuity

2.6.0 → seeded Tracking/Saccade.
2.7.0 → shared terminal CTA.
2.7.1 → CTA compile hotfix.
2.7.2 → CTA lifecycle test hotfix.
2.8.0 → Pursuit/Peripheral initial implementation + Header CTA.
2.8.1 → Pursuit/Peripheral runtime hotfixes.
2.9.0 → current Visual Drill polish, production delivery and documentation consolidation.
