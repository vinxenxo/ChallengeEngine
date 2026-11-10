# C11-E E4C Visual Drill Execution Plan — V3 (2026-11-10)

## Objective

Complete Drill integration through the existing D9 Dynamic Request Payload Binding V2 and E1 shared service. Preserve four types, five tiers, native phases/END_CTA precedence and `FAMILY_MUSIC_V4`. No parallel binder, producer or generator.

## Accepted scope — do not repeat

- Historical Drill authoring adapter: 20/20 across the 24 accepted source pins; report SHA `fc550cf26161c5428e2b8edf280baf611fb3c06f2e3c00773910e352115eaa6e`.
- E4B Loop22: CLOSED; 44/44 A/V; 22/22 A/B; 25/25 tests; operator visual/audio acceptance.
- E4C source preparation and E1 contract were tested in isolated V109-derived material: E1 32/32; Drill V2 source chain 7/7; V1 dynamic binding 12/12; request-scoped binding 51/51 negative controls; editorial review 28/28 negative controls. These are not active Windows runtime acceptance.

## E4C package installation — current result

Overlay V1.1 installed on the active checkout with `PASS_ADD_ONLY_TRANSACTION`, 7/7 source replacements and 13/13 additive files. Receipt SHA-256: `8fb893ea1f468cb2c0c719bc7f4ea7c469c351df8a70351b37cbe920c1072d48`. Do not rerun that installer.

## Windows runtime acceptance — Godot discovery correction

The first E4C runner version required `$env:C11D_GODOT_EXECUTABLE` without resolving Godot automatically. The first hotfix package then repeated a known malformed frozen-manifest SHA typo and aborted before writes. V2 corrects that installer fault and restores the established D9 runner contract. The V2 runner hotfix restores automatic discovery:

1. A valid explicit `$env:C11D_GODOT_EXECUTABLE` is honoured first.
2. Otherwise search `PATH` for `godot4.exe`, `godot.exe`, `godot4`, and `godot`.
3. Search `Downloads`, `C:\Godot`, and `%LOCALAPPDATA%\Programs\Godot` for `Godot_v4.7.1-stable*_win64_console.exe`.
4. Probe each candidate using captured native-process stdout/stderr and accept only exact `4.7.1.stable.mono.official.a13da4feb`. The chosen path is set in the process environment and passed explicitly to the Python matrix runner.

Use the V2 one-shot entrypoint to install the pinned runner hotfix and, only after a successful install receipt, execute the existing E4C acceptance runner once. Do not manually set the Godot variable unless the executable is in a nonstandard location; in that case an explicit path remains supported.

## Expected runtime matrix

- E1 service tests: 32/32.
- Drill V2 source chain: 7/7.
- Existing dynamic-binding regression: 12/12.
- Request-scoped binding: 51/51 negative controls.
- Editorial review: 28/28 negative controls.
- Real-Godot matrix: 20 selector manifests, 20 independent deterministic repeats, 20/20 lineage closures, 67/67 source pins.

Four families: `tracking`, `pursuit`, `saccade`, `peripheral_scan`; five tiers each. Runtime matrix means 40 Godot invocations. It remains non-rendering/preparation-only.

## Separate blockers and native contracts

A.3 visual field-window policy remains blocked by stale editorial-review lineage. Do not edit the approved proposal/decision in place. Dynamic binding PASS does not imply visual consumer approval.

Preserve PRE_ROLL 3s, GAME actual gameplay frames, END_CTA 3s, DONE. During END_CTA native C11-C CTA owns the header. Preserve `FAMILY_MUSIC_V4`: tracking=`FLOWING_VECTOR`, pursuit=`ORGANIC_BLOOM`, saccade=`CIRCUIT_PULSE`, peripheral_scan=`ORBITAL_RITUAL`. Keep gameplay `request.seed` separate from music `request.music_seed`; future A/V uses silent C11-C capture (`-NoSound`) plus separate native music helper. Do not edit protected C11-C launcher.

## Governance

Frozen C11-C manifest: 796,318 bytes, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. Renderer OFF; production dispatch/media OFF; D4.8 BLOCKED; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION; `release_authority=NONE`.
