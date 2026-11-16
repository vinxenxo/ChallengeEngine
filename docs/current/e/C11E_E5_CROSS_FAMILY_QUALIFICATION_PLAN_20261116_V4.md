# C11-E E5 Cross-Family Qualification Plan — V4

**Date:** 2026-11-16  
**Status:** `A_V_OPERATOR_ACCEPTED`; `E5_OPEN_QT_GUI_RUNTIME_REQUIRED`.

## Purpose and declared scope

E5 proves cross-family deterministic behavior, gameplay/music seed isolation, family adapter/profile/binder/timeline non-leakage, GUI/CLI parity, and governed representative A/V qualification across Challenge, Visual Loop and Visual Drill. It is distinct from E6 Smoke18 and does not repeat E4 matrices.

The three accepted representatives remain:

| Family | Selector | Native profile/route | Baseline gameplay/music seeds |
|---|---|---|---:|
| Challenge | `parking_v2 / CHALLENGE_004` | `challenge_8bit_v1` / D3 V5 planning binding | 314159 / 840001 |
| Visual Loop | `c11c_fractal_bloom_v1 / radial_bloom` | `ORGANIC_BLOOM` / preserve native Loop route | 100006 / 500006 |
| Visual Drill | `tracking / tier-2` | `FLOWING_VECTOR` / preserve native Drill route | 12345 / 840001 |

Canonical source identities, timebases and the original 31 static pins remain defined in V3 and the canary JSON contract. The active run's dynamic/static/historical evidence union was rechecked as 134/134.

## 1. PREPARE_ONLY cross-family canary — PASS

Batch `E5-XF-PREP-20261116T142423Z-D455AA63` passed:

- 12/12 GUI-origin/CLI-origin semantic preparation pairs.
- 24/24 service-origin rows.
- A/B replay; C changed only music seed; D changed only gameplay seed across all three families.
- Distinct family music profiles and family-native binder/grammar/timebase boundaries preserved.
- Source pin union stable pre/post; combined receipts are immutable and SHA-linked.
- Combined receipt SHA-256 `8fb5dde145046f167e13109b8f8168e91ed0982e6baf2894b13dc9df28d39393`.
- Batch result SHA-256 `efd6679860c9ead92516da3eb2c39e6eb41ae0dc77396c0f082c29b4a81a8c3d`.

The canary itself remains PREPARE_ONLY. It did not run the visible Qt window or generate media.

## 2. Representative A/V qualification — PASS / operator accepted

The separate authorized TEST_ONLY media path reused accepted family-owned outputs and generated only the missing Loop C changed-music result. No E4 matrix was repeated.

- Challenge `parking_v2/CHALLENGE_004`: accepted E4A.7 A/B/C D-composited A/V evidence; prior operator acceptance remains valid.
- Visual Loop `radial_bloom`: accepted A/B and newly recovered C with gameplay seed 100006 and music seed 500007. Loop C H.264 exactly matches accepted A; AAC differs; native C music is deterministic. MP4 SHA-256 `2c14f825a1e00a19a9d27cffdffa854947dfb22da0c7fae089e3a0344a643c83`; recovery receipt SHA-256 `86105f8cba04cf7ad5ed2516049c6b16845e95fe21d7940019b8046bb7c75f21`.
- Visual Drill `tracking/tier-2`: accepted E4C A/B/C technical evidence; receipt SHA-256 `f95e9b4e787f1b4f7db79b92428324f6de662ade55b260c7692d4440e2967ee7`.

The operator explicitly approved video, audio, editorial line, music and layout for all three representatives, including Loop C. This closes the representative operator A/V review gate. See `C11E_E5_CROSS_FAMILY_AV_CLOSEOUT_20261116_V1.md` for evidence references and the immutable recovery receipt details.

## 3. Remaining E5 gate — visible Qt Producer runtime

The recovery receipt correctly records `actual_qt_gui_runtime=NOT_RUN_OPERATOR_UI_SESSION_REQUIRED`. GUI-origin/CLI-origin service preparation and static GUI wiring are not proof that the actual visible Producer window ran.

The sole remaining E5 acceptance action is a visible Windows Qt session using the existing Producer, selecting and resolving the three same E5 representative requests. The exact procedure, request fields, safe action, expected receipts and compact evidence packaging are in `C11E_E5_QT_GUI_RUNTIME_ACCEPTANCE_20261116_V1.md`.

Expected evidence root:

`artifacts/tests/c11d_d9/producer_universal/D99-GUI-<ID>/`

Require three distinct new GUI run directories: Challenge, Loop and Drill. For each require E1 service PASS, D9 GUI/CLI parity PASS, lifecycle PASS, family stage evidence where applicable, and unchanged fail-closed execution boundaries.

## 4. Clarification: `NOT_CONNECTED_E1` is an intentional boundary

The E1 shared service currently sets `family_adapter.status=NOT_CONNECTED_E1`; its target gate is E2 for Challenge and E4 for Loop/Drill. Editorial fields remain `NOT_CONSUMED_E1`; renderer input, renderer dispatch, production execution and media creation remain false. This is the intended PREPARE_ONLY architecture.

E5 validates that these family-specific preparation contracts, profiles, binders, grammars, timelines and seed domains remain correctly isolated. It does not require the E1 family adapters to become connected, and it does not authorize a dispatch path. The separate TEST_ONLY A/V qualifications above do not change the E1 adapter status. Do not implement a new E1 adapter connection as an E5 closeout shortcut.

## 5. Exit and downstream phases

When all three visible Qt runtime rows pass and their evidence is verified, publish the E5 full-phase closeout in its declared TEST_ONLY scope. Then:

1. E6 Smoke18 — 18 audiovisual smoke scenarios, six per family; start only after E5 full acceptance.
2. E7 Matrix101 — 54 Challenge + 27 Loop + 20 Drill. CH_008/CH_009 remain held pending authoritative reconciliation of declared 11 s against 12 s phase sum; 99 provisional runnable rows.
3. E8 — row-by-row historical C-to-E regression reconciliation, independent acceptance, immutable freeze and separately governed C-to-D+E transition decision.

## Governance

C11-C 2.19.12 remains immutable production authority; frozen manifest 796,318 bytes / SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. E1 remains PREPARE_ONLY; renderer OFF; production dispatch/media false; release authority NONE. No Git checks; commits operator-managed; source SHA-256 pins enforced. No protected C11-C changes, parallel Producer/binder/renderer/mechanic, sixth suite module or promotion.
