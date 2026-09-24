# MASTER HANDOVER — ChallengeEngineV01_STATELESS / C11-C 2.9.1

## 0. Mission
Continue the deterministic Godot 4.7.1 project `ChallengeEngineV01_STATELESS` from the C11-C Visual Drills phase without regressing frozen contracts.

This handover is authoritative for the transition to the next context window.

## 1. Current baseline
- Target branch: **C11-C 2.9.1**.
- 2.9.0 introduced the complete four-family Visual Drill presentation layer and usability refinements.
- 2.9.1 is a narrow runtime hotfix for `PeripheralScanRenderer.gd` only.
- The user has already confirmed that the videos render after the 2.9.1 family implementation.
- Current known 2.9.0 aggregate failures were caused by one undeclared `_environment` identifier in `PeripheralScanRenderer.gd`.

## 2. Frozen architecture
Never modify:
- C11-B simulation truth;
- Challenge mechanics;
- structural RNG ownership;
- `SimulationResult`;
- `winning_frame`;
- `close_calls`;
- `WinningFrameDetector`;
- `RenderedFrameStream` semantics;
- C7 audio ownership/contracts;
- C9 authoring contracts;
- logical 540x960 social geometry;
- physical 720x1280 / 30 FPS delivery contract.

Presentation may render authored/runtime outputs but must not calculate gameplay truth.

## 3. Visual Drill family status
### Tracking — CLOSED
- Seed changes authored trajectory characteristics, not only cosmetics.
- History-only trail / time fade.
- Target is presentation hero.
- Tron 3D background removed by artistic decision.
- No unexplained grey circular background object.

### Saccade — CLOSED
- No spatial interpolation.
- 180–300 px authored jump constraint.
- APPEAR 200 ms nominal / IDLE difficulty tier / VANISH 50 ms nominal.
- Jump counter is rendered from mechanic `jump_index`.
- Seed changes authored polar distribution.

### Pursuit — IMPLEMENTED / VALIDATE
- Cubic uniform B-spline.
- Arc-length LUT.
- Constant-speed-by-arc traversal in authored output.
- Sizygia answer sheet.
- Camouflage zones.
- Monolith / Euler-gyro inspired target presentation.

### Peripheral Scan — IMPLEMENTED / VALIDATE
- Fixed central anchor.
- Three orbital rings.
- Deterministic polar event schedule.
- Threat vs distractor answer sheet.
- Eclipse / flare presentation.
- 2.9.1 fixes the undeclared `_environment` presentation dependency.

## 4. Common usability layer
The Visual Drill host now has:
1. 3-second countdown borrowed from the Challenge presentation contract.
2. Gameplay from the canonical `RenderedFrameStream`/Visual Drill runtime.
3. 3-second terminal self-evaluation CTA in **Header**.

Terminal copy:
`¿LO CONSEGUISTE?`
`¿HASTA DÓNDE LLEGASTE?`

The CTA must reuse `CTAComponent`; do not create a second CTA framework.

## 5. Typography
The Visual Drill editorial text must not use Comic Sans. Typography is governed by the common presentation layer and has its dedicated regression suite.

## 6. Social delivery
Every generated Visual Drill must produce its social metadata text sidecar containing at least:
- title;
- description;
- family;
- seed;
- resolution;
- FPS;
- duration;
- frames;
- audio state;
- matrix state / presentation metadata when applicable;
- hashtags.

Do not silently omit the sidecar for newly added families.

## 7. Palette direction
Use a semantic palette bank. Primary is reserved for target/anchor. Secondary and tertiary accents drive trail, orbital, flare and editorial detail. Seeded variation must affect a meaningful set of visual parameters; do not return to the earlier state where only the trail changed between seeds.

## 8. Audio direction
Current state: one shared global Visual Drill ambient master, deterministic and mobile-safe.

Future refinement should be additive, not a replacement of C7 ownership:
- subtle harmonic bed;
- low transient density;
- movement-aware accompaniment;
- no harsh high-frequency energy;
- no strobing-like audio modulation;
- same global audio master architecture across drill families.

## 9. Gameplay-depth roadmap from the Drill Design Bible
### Tracking
- Predictive occlusion tunnel.
- Target morph-state counting.

### Saccade
- N-back spatial memory.
- Flash recognition / symbol discrimination.

### Pursuit
- Simulated depth / scale modulation.
- Flanker distractors.

### Peripheral Scan
- Quadrant accounting.
- Rhythmic asynchrony / anti-entrainment.

Any new mechanic must place truth in authoring/runtime and expose the answer sheet deterministically; presentation only consumes the result.

## 10. Required validation order
Run focused suites first, then the complete corpus:

```powershell
godot --headless --path . --script .\tests\C11CVisualDrillEndCTAContractTest.gd
godot --headless --path . --script .\tests\C11CVisualDrillTypographyContractTest.gd
godot --headless --path . --script .\tests\C11CVisualDrillSocialDeliveryContractTest.gd
godot --headless --path . --script .\tests\C11CDrillPaletteBankContractTest.gd

godot --headless --path . --script .\tests\C6F08TrackingPlaybackValidationTest.gd
godot --headless --path . --script .\tests\C6F08SaccadePlaybackValidationTest.gd
godot --headless --path . --script .\tests\C6F08PursuitPlaybackValidationTest.gd
godot --headless --path . --script .\tests\C6F08PeripheralScanPilotTest.gd

python -m py_compile .\tests\run_all.py
python .\tests\run_all.py
```

Expected closure condition:
- zero `SCRIPT ERROR`;
- zero parse errors;
- zero false PASS states;
- complete corpus PASS.

## 11. Review command
For one-seed smoke across all four families:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_visual_drill_review.ps1 `
    -Seeds 314159 `
    -Families tracking,saccade,pursuit,peripheral_scan `
    -Smoke `
    -ResetReviewAssets
```

For the full aesthetic variance review, use exactly five unique seeds and omit `-Smoke`.

## 12. Immediate next objective
After 2.9.1 is completely green, do not reopen the already closed mechanics. The next context should choose between:
- Visual Drill audio v2 / motion-synchronized ambient refinement;
- deeper gameplay layers from the Drill Design Bible;
- final palette/art polish;
- packaging/documentation freeze for the four-family Visual Drill set.

## 13. Continuity rule
Never claim a phase is closed from a single focused test. Closure requires focused tests + aggregate runner + physical review when the change is visual or delivery-related.
