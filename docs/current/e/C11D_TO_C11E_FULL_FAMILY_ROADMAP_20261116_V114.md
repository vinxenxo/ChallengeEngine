# C11-D to C11-E Full-Family Roadmap — V114 (2026-11-16)

## Current checkpoint

E4A Challenge and E4B Visual Loop remain accepted within their declared scopes. E4C Visual Drill is CLOSED 20/20 (Tracking, Pursuit, Saccade and Peripheral Scan each 5/5 with technical PASS and operator A/V approval). Do not rerun any accepted E4 family batch.

## Ordered execution sequence

| Order | Phase | Entry | Exit |
|---:|---|---|---|
| 1 | E4A / E4B / E4C | Historical family contracts | Closed in accepted scopes; preserve all evidence |
| 2 | E5 Cross-Family | E4A/B/C accepted; three representative contracts and pins reconciled | Determinism, seed isolation, family adapter/profile/binder/timeline non-leakage, GUI/CLI parity, governed A/V qualification and receipts across Challenge/Loop/Drill |
| 3 | E6 Smoke18 | Full E5 acceptance | 18 A/V smoke scenarios: six per family |
| 4 | E7 Matrix101 | E6 accepted | 54 Challenge + 27 Loop + 20 Drill; CH_008/CH_009 held on 11s/12s mismatch; 99 provisional runnable |
| 5 | E8 | E7 disposition accepted | Complete historical regression map, independent acceptance, immutable freeze and separately governed transition decision |

## E5 opening canary

The operator-authorized opening canary is a bounded PREPARE_ONLY integration test, not E6 and not full E5 closure. The selected contracts are Challenge `parking_v2/CHALLENGE_004`, Visual Loop `c11c_fractal_bloom_v1/radial_bloom`, and Visual Drill `tracking/tier-2`. The exact canonical hashes, native timebase references, family music routes/profiles and seed pairs are fixed in `C11E_E5_CROSS_FAMILY_QUALIFICATION_PLAN_20261116_V3.md` and the E5 canary JSON contract.

A/B repeats baseline semantics; C changes only `request.music_seed`; D changes only `request.seed`. Each probe executes through GUI-origin and CLI-origin preparation in the same E1 service, yielding 12 pairs / 24 rows. Validate distinct family music profiles, family-native boundaries and seed non-leakage, static/dynamic source-pin stability and immutable receipts.

The current E1 adapter remains `NOT_CONNECTED_E1`; therefore the opening canary must create zero media and may not launch renderer, Godot, D3 V5 audio, FFmpeg or FFprobe. GUI-origin service preparation plus static GUI wiring is not represented as a real Qt UI session. Full E5 A/V and observed GUI runtime are still required according to governed authorization.

## Remaining phases

- **E6 Smoke18:** six audiovisual scenarios per family.
- **E7 Matrix101:** 54 Challenge + 27 Loop + 20 Drill. CH_008/CH_009 remain held until the 11-second declared duration versus 12-second phase sum is authoritatively reconciled; 99 provisional runnable rows.
- **E8:** reconcile all historical C11-C review categories row-by-row, independent acceptance, immutable freeze and explicit C-to-D+E transition authority.

## Architecture and governance

C11-C 2.19.12 remains immutable production authority. Preserve family-specific mechanics, binders, grammars, timelines and music. Shared E1 orchestration does not authorize flattening family semantics or introducing a parallel Producer/binder/renderer. `renderer=OFF`, `production_dispatch=false`, `production_media=false`, `release_authority=NONE` until E8 and separate governance approval.
