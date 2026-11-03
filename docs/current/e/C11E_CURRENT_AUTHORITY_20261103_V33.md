# C11-E Current Authority — V33

**Date:** 2026-11-03  
**Authority:** active Windows checkout. This revision records operator approval of Challenge editorial policy V1 and authorization for isolated E4A render tests. It grants no production renderer/release authority.

## 1. Product objective

One C11-E audiovisual production system for Challenge, Visual Loop and Visual Drill. Keep C11-C simulation/generators and existing family audio implementations immutable. Add approved D presentation/editorial, family-correct audio orchestration, FFmpeg mux, FFprobe/A-V QA and immutable run receipts. Existing five suite surfaces only; one canonical shared service for Producer GUI and CLI compatibility path. No parallel binder/producer/renderer and no sixth suite module.

## 2. Accepted state retained

- E0/E1, bounded E2 R4 title-to-pixels control, E3.2, E3 Challenge audio/mux pilot and 50/50 negative controls remain accepted within scope. Do not repeat them absent relevant source changes.
- E4A Challenge source discovery/read-only audit and GUI contract successor are closed within their scope. GUI successor receipt SHA-256: `3ca7c173481247bf8b1273aada92b7266e3d385214ffd8770858492f894f5679`.
- Gate A direct readiness assessment is closed with blockers, not a PASS: I/O 0/10 complete, 6 partial, 4 blocked; identity 164 sources; editorial sidecar 14/14, visual consumption 0/14; fixed-fixture binding reports 3/3 deterministic joins. Five Python test exit codes remain unverified due to the native stderr capture defect in the PowerShell wrapper. Do not repeat the reports/previews or those tests as a bundle.

## 3. Approved Challenge editorial policy

The operator explicitly approved Policy V1 on 2026-11-03 (`APROBAR POLICY V1`). Decision JSON: `definitions/c11d/production/C11E_E4A_CHALLENGE_EDITORIAL_PRESENTATION_POLICY_APPROVAL_V1.json`. The approval is scoped to the Challenge semantic mapping only:
- `title` → `HEADER` / `HOOK`;
- `subtitle` → `HEADER` / `HOOK`;
- `player_name` → `CHALLENGE_OVERLAY` / `HOOK + GAME`;
- `challenge_label` → `CHALLENGE_OVERLAY` / `HOOK + GAME`;
- `call_to_action` → `FOOTER` / `CTA`;
- `language` → metadata only, no visual drawing.

Use canonical D9.8 inheritance only. Omit empty values. Resolve named phase boundaries from each selected canonical Challenge in its native source timebase. D9.9 names remain distinct from phase-field keys `hook`, `reveal`, `cta`. `call_to_action`→`CTA` is a policy relationship, not a name alias. Unresolved region/window fails closed. No guessed geometry or hard-coded CHALLENGE_004 numeric frame boundaries.

## 4. Historical D/C implementation reuse

D1.1 Challenge mapping passed as non-rendering mapping evidence. D1.7 declarative mapping passed 9/9 with canonical inherited layout and no Challenge layout override. D1.5 supplies the 540×960 logical frame: HEADER 0–144, BODY 144–816, FOOTER 816–960. C11-C `ChallengePresentationBinder.gd`, `C11CVisualEditorialLayer.gd` and `VisualContentPlayer.gd` are frozen references, not edit targets.

Reuse the existing D-only Challenge source-timebase materializer, safe projection and V2B allowlisted coordinate consumer/source-composition route. The prior V2B consumer passed 277 review-only cases; the source-composition chain passed its 402-check evidence validator and four-Challenge 1680/1680 source/marker runtime. These are logical composition evidence, not pixel renders; do not rerun absent pin drift.

## 5. Immediate work — E4A visual closure

1. Obtain the exact current source files once through `SOURCE_HANDOFF_COMMAND.txt`; this is a copy/ZIP operation only, no test, runner or installer.
2. Implement the minimal D-only extension on the existing Challenge source composition/allowlisted consumer path. Carry exact effective text, per-field value hash, request/payload/source identity, policy hash, semantic region and named phase window. Do not read or serialize all `FrameSnapshot.custom_data`.
3. Add a dedicated isolated off-screen Godot test surface which consumes that same D composition result. It must not be callable through Producer, D9.10 dispatch or production pipeline.
4. Render A/B frame/PNG test artifacts using the same Challenge/source/gameplay frames. Assert approved region/window pixel changes, no drawing for language/empty values, unchanged gameplay/source pixels, deterministic repeats, fail-closed missing/ambiguous region/window and all policy/source/hash negatives.
5. Resolve `CHALLENGE_OVERLAY` only through the existing D1.5/profile/family composition authority. If the exact profile has no approved geometry, those two fields remain blocked while HEADER/FOOTER field tests proceed. Never infer a rectangle.
6. After visual pixel proof, use the accepted E3 audio/mux/QC pipeline for isolated test-only A/V acceptance; do not rerender gameplay merely to vary the music seed.

User authorization: isolated E4A test renders are approved. Production renderer activation, production dispatch and real-media D9.14 qualification are not.

## 6. Remaining roadmap

E4A Challenge pixel and test-only A/V closure → E4B Loop → E4C Drill → E5 determinism/independent seed domains/family-profile non-leakage/GUI-CLI parity → E6 Smoke18 (six per family) → E7 Matrix101 (99 currently runnable; CH_008/009 held until 11s vs 12s authority correction) → E8 full historic C11-C case reconciliation (including 27 review and 9 Challenge cases), independent acceptance, freeze and separate promotion.

## 7. Governance

C11-C 2.19.12 remains sole production authority. Frozen manifest 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` is immutable. `renderer=OFF` for production; `D9.10=PREPARE_ONLY`; `D4.8=BLOCKED`; `D9.14/D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `release_authority=NONE`; `baseline_promotion=false`; `freeze_eligible=false`.
