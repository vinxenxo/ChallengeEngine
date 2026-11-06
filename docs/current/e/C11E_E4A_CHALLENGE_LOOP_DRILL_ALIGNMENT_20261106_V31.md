# C11-E Challenge / Loop / Drill Alignment — V31

## Accepted family progress

- Challenge E4A is closed `PASS_TEST_ONLY`; don't repeat accepted visual/A/V/listening or D99 GUI evidence absent a regression.
- Loop E4B has populated GUI/CLI parity accepted and a Windows full-family matrix accepted plan-only: 5 existing families, 27 concrete grammars, 81 scenarios, 81 deterministic repeats, 27 seed relations, 81/81 GUI/CLI selector parity.
- Drill E4C follows Loop; preserve Drill's four-field editorial contract, existing binder/variation/timebase and family audio ownership.

## Canonical editorial contracts

- Challenge: six canonical keys remain present (`title`, `subtitle`, `call_to_action`, `language`, `player_name`, `challenge_label`); blank optional strings normalize to `UNKNOWN`; no key omission.
- Loop/Drill: four keys remain present (`title`, `subtitle`, `call_to_action`, `language`); blank optional strings normalize to `UNKNOWN`; no per-field optionality.
- GUI and CLI feed the same canonical D9.9/E1 preparation semantics. PowerShell 5.1 scripts must be ASCII-only; non-ASCII strings flow through UTF-8 JSON/Python and are verified NFC.

## E4B matrix scope and meaning

- Family distribution: 5/5/5/5/7 = 27 concrete grammars; `auto` selector entries excluded.
- Three scenarios per grammar: baseline, gameplay-only seed mutation, music-only seed mutation; 81 cases, 81 deterministic repeats and 27 seed relations.
- All nine canonical identity fields match across GUI/CLI in all 81 rows; request-origin IDs are provenance-bound and are not treated as editorial semantic identity.
- D9.9 returns `UNIVERSAL_EDITORIAL_INTENT_PLAN_ONLY`; it is not a D4 executable plan or renderer-native payload. D9.8 compatibility metadata stays pending until separately reconciled and tested.
- E1 Loop editorial remains `NOT_CONSUMED_E1`; family adapter `NOT_CONNECTED_E1`; existing C11-C family music route preserved and not invoked.

## Non-negotiable C11-C invariants

No mutation of simulation truth, C mechanics/generators, family scenes, binders, timelines, Matrix, RNG, `C11CVisualEditorialLayer`, common presentation contracts, core audio or family music generators. Gameplay and music seeds remain independent. No new Producer, sixth module or parallel binder.

## Sequence

E4B: current-hash policy decisions → family-specific D binding review → D-only consumer outside the source frame → 27-selector GUI/CLI test coverage → B.1/D.1 audio/timebase decisions → visual/A/V/human acceptance. Then E4C Drill → E5 → Smoke18 → Matrix101 → E8. Renderer/dispatch/media stay OFF; release authority NONE.
