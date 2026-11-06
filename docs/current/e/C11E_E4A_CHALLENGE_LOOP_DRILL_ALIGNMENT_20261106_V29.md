# C11-E Challenge / Loop / Drill Alignment — V29

## Family rollout

- Challenge E4A is closed `PASS_TEST_ONLY`; do not replay accepted visual/A/V/audio gates absent regression.
- Loop E4B uses the existing five C11-C families and 27 grammars; four D9.8 editorial fields; family music remains C11-C-owned.
- Drill E4C follows E4B; retain its four-field contract, binder/variation and family audio ownership.

## Shared invariants

1. C11-C 2.19.12 and the frozen manifest remain immutable production authority.
2. No changes to simulation truth, mechanics, binders, timelines, Matrix, RNG, protected presentation layer or family music generators.
3. All canonical editorial keys remain present; blank values normalize through existing D9.8 semantics (`UNKNOWN` where applicable).
4. Gameplay and music seed domains remain independent; no automatic seed adoption/derivation.
5. GUI and CLI must test the same request semantics from independently captured origins. PowerShell 5.1 scripts must not embed non-ASCII fixtures without BOM; prefer GUI-exported UTF-8 JSON.
6. Plan-only parity cannot be represented as rendered media or production acceptance.

## E4B current condition

The populated GUI evidence is PASS. V1 CLI values were corrupted by PS 5.1 source decoding and are not accepted for populated parity. E4B CLI/GUI Parity V2 reads the existing GUI UTF-8 JSON, replays the same raw request through D9.9 and E1 CLI and checks equality. No new GUI run is required.
