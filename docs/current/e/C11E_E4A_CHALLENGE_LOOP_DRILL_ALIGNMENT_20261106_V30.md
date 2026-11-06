# C11-E Challenge / Loop / Drill Alignment — V30

## Family rollout

- Challenge E4A is closed `PASS_TEST_ONLY`; do not replay accepted visual, A/V or listening gates absent regression.
- Loop E4B has accepted populated GUI/CLI parity. The next matrix covers all five existing C11-C families and 27 concrete grammar selectors through the current D9.9/D9.10/E1 plan-only boundary.
- Drill E4C follows E4B; preserve its four-field editorial contract, binder/variation and family audio ownership.

## E4B matrix definition

- Five families, 27 concrete grammars (5/5/5/5/7), excluding `auto`.
- Three seed scenarios per grammar: baseline, gameplay-only change, music-only change; 81 cases total.
- Reuse canonical D9.9 resolver, D9.10 bridge, existing D-only prepare adapter and E1 service. No new binder/Producer.
- The same helper is invoked by a diagnostic button inside the current D9.9 GUI tab and by the CLI runner. CLI replays the GUI-exported request template; editorial hashes and exact four values must match over all 81 rows.
- Four keys remain complete: `title`, `subtitle`, `call_to_action`, `language`; blanks remain `UNKNOWN`. No per-field omission.

## Shared invariants

1. C11-C 2.19.12 and frozen manifest remain immutable production authority.
2. No changes to simulation truth, mechanics, binders, timelines, Matrix, RNG, protected presentation layer or family music generators.
3. Gameplay and music seed domains remain independent; no automatic seed adoption/derivation.
4. GUI and CLI use the same canonical backend and request template semantics. PowerShell 5.1 scripts are ASCII-only for literals; Unicode comes from UTF-8 JSON.
5. Plan-only parity is not rendered media or production acceptance. The family matrix emits no renderer input.
