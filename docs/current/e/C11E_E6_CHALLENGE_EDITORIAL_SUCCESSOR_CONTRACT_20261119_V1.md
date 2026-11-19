# C11-E E6 Challenge — Editorial Window and Consumer Successor Contract V1

**Status:** `D_OWNED_SUCCESSOR_CONTRACT_PREPARE_AND_STATIC_TEST_SCOPE`  
**Date:** 2026-11-19  
**Predecessor:** accepted E4A Challenge policy/adapter/consumer V1, immutable.

## 1. Purpose

Enable the approved synthetic Challenge editorial fixture to be consumed in Smoke18 for six selected Challenge scenarios without changing canonical timelines or the E4A predecessor contract. This contract covers D-owned successor behavior and static proof; it does not itself authorize Godot, renderer input, media or audio execution.

## 2. Fixed Smoke18 Challenge scope

Selectors: `CHALLENGE_001`, `002`, `004`, `005`, `006`, `007`.

| Selector | Native duration | Source fps | Source frames | HOOK | GAME | CTA | Editorial windows |
|---|---:|---:|---:|---:|---:|---:|---|
| 001 | 9 s | 60 | 540 | 0 | 420 | 120 | title/subtitle GAME; CTA CTA |
| 002 | 10 s | 60 | 600 | 180 | 420 | 0 | title/subtitle HOOK; CTA GAME |
| 004 | 15 s | 60 | 900 | 180 | 420 | 120 | title/subtitle HOOK; CTA CTA |
| 005 | 7 s | 60 | 420 | 0 | 420 | 0 | title/subtitle GAME; CTA GAME |
| 006 | 9 s | 60 | 540 | 0 | 420 | 120 | title/subtitle GAME; CTA CTA |
| 007 | 10 s | 60 | 600 | 180 | 420 | 0 | title/subtitle HOOK; CTA GAME |

The windows above describe the E6 successor proposal: retain the primary window when it contains frames; use GAME only when HOOK/CTA primary has zero frames. Frame ranges remain canonical-FPS, half-open intervals. No phase duration/order/FPS/mechanic/seed changes.

## 3. D1.5 regions and ownership

Use the existing logical 540×960 presentation layout:

- HEADER `Rect2(0, 0, 540, 144)` — title and subtitle.
- BODY `Rect2(0, 144, 540, 672)` — Challenge source visual.
- FOOTER `Rect2(0, 816, 540, 144)` — CTA.

Do not alter the geometry, safe area, typography contract or native phase timeline. Zero-frame source windows do not justify moving fields to another region.

## 4. Native hook migration guard

The current adapter seam must not migrate a native hook merely because header editorial is active and `show_hook_countdown` is true. The successor must use the native render model's actual visibility signal (`native_render_model.show_hook` or an equally explicit current-phase signal):

1. If native HOOK is visible, title/subtitle may share HEADER; migrate native hook text exactly once and suppress its original rendering to avoid duplicate hook text.
2. If native HOOK is not visible (including GAME fallback), draw D title/subtitle in HEADER only. Do not migrate native hook text and do not suppress an already-hidden native hook.
3. With no active D header editorial, preserve existing native hook/countdown behavior.
4. CTA ownership remains singular. During native CTA window D Footer owns the CTA. During GAME fallback the native CTA is not visible by canonical timeline; D Footer may own the E6 test CTA.

## 5. Editorial fixture and identity invariants

- Keep the already prepared synthetic Spanish family editorial fixture as a run-scoped E6 test input, never a product default.
- Preserve exact strings and canonical four-field schema as pinned by the existing Challenge editorial binding PREPARE_ONLY receipt.
- Preserve 18 A/B/C probes nested under six scenario rows. A/B gameplay and music seeds repeat; C changes only the approved music seed.
- The current approved Challenge music fixture is `challenge_8bit_v1`, A/B seed 840001, C seed 840002, variation 0, 104 BPM, with duration derived from canonical phase timebase and verified against actual media metadata. This is test-only and is not written to product defaults.
- E1 `tempo_bpm` and `duration_seconds` remain null. `player_name` and `challenge_label` remain UNKNOWN/BLOCKED; personalization remains false.
- No E4A V1, C11-C definition, binder, timeline, winning-frame detector, RNG or family audio source changes.

## 6. Required static tests

1. Six selector timelines and phase sums match canonical definitions and the existing 18 PREPARE_ONLY envelopes.
2. A/B/C identity, hashes, seed separation and sidecars exact.
3. All 54 field/probe slots have positive half-open windows; 27 primary windows remain primary; 27 zero-frame primary windows use the approved GAME fallback.
4. HOOK frames: native hook migration exactly once; native hook suppressed only after migration.
5. GAME fallback frames: D Header text visible; native hook not migrated and not spuriously suppressed.
6. CTA frames and GAME fallback: exactly one CTA owner.
7. D1.5 geometry and safe-area containment exact; no region movement.
8. Unicode NFC, font availability, shaping and wrapping preflight; actual raster legibility/contrast/overflow remains part of visual review.
9. Old E4A V1 envelopes remain accepted by the predecessor path without changing its pins.
10. Source pins, C11-C manifest and governance flags remain unchanged; no media tools/processes invoked.

## 7. Render gate

After the static suite passes, prepare the selector-specific visual render manifest with exact canonical definition hashes and output expectations. Runtime rendering remains gated by the scoped Smoke18 D4.8 successor, exact process allowlist and E6 TEST_ONLY authorization. A successful runtime readback is not human visual acceptance or E6 row acceptance.
