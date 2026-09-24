# C11-C 2.8.0 — Visual Drill CTA Header + Pursuit + Peripheral Scan

- Moved the shared Visual Drill terminal CTA from Footer to Header without duplicating CTAComponent.
- Added authored deterministic Pursuit: cyclic uniform cubic B-spline, arc-length LUT, per-frame path samples, bounded speed modulation, sizygia answer sheet and camouflage zones.
- Added authored deterministic Peripheral Scan: fixed center anchor, three orbital rings, logistic-map angles, exact threat/distractor schedule and answer sheet.
- Added presentation art for Pursuit (Monolith in Void, Euler-like target, radial screen-texture DOF) and Peripheral Scan (Eclipse, orbital radar rings, solar flares).
- Added semantic palette banks for Pursuit and Peripheral Scan.
- Added mechanic/presentation contract tests and updated legacy playback tests.
- Added Visual Drill audio direction handoff; no C7 audio generator ownership changed in this phase.
- Review `authoring.json` now records the deterministic authored answer sheet (study artifact) without moving the seed into the authoring request schema.
- Pursuit arc traversal now incorporates the authored difficulty speed multiplier while retaining subtle deterministic modulation.
