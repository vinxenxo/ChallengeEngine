# C11-D operator evidence ledger — 2026-10-16

This document records the exact user-pasted results for the seed collision regression and bounded cross-type runtime audit. It is not a signed release record; the cited hashes identify the reported audit/stdout/stderr artifacts.

## Execution 1 — collision rejection regression

- Heading: `=== 1/2: SEED COLLISION REGRESSION ===`
- Result: 7 tests, 0.722 seconds, `OK`.
- Final line: `SEED COLLISION REGRESSION: PASS`.
- The tests covered 23 pinned sources and C11-C preservation, the two-selector scope, equal-number collisions rejected before Godot, strict report shape/non-admissibility, missing/invalid seed rejection, no Godot invocation or artifacts, and fail-closed policy changes.
- This test is intentionally pre-runtime and does not prove a rendered frame.

## Execution 2 — cross-type Godot runtime audit

- Godot executable:
  `C:\Users\vinxe\AppData\Local\Microsoft\WinGet\Packages\GodotEngine.GodotEngine.Mono_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.7.1-stable_mono_win64\godot.exe`
- Godot version: `4.7.1.stable.mono.official.a13da4feb`.
- Summary copied from stdout:
  `C11-D CROSS-TYPE SEED DOMAIN AUDIT PASS | selectors=2 | gameplay_seed_sensitivity=2/2 | music_seed_orthogonality=2/2 | independent_repeats=6/6 | source_pins=18/18 | runtime_invocations=12 | seed_domains_complete_for_candidate_input=false | renderer=OFF | media_created=false | D4.8=BLOCKED | release_authority=NONE`
- Report field `audit_sha256`: `94cef68056e7fd5876e64642746012e3ba9c8e8106b03a3d78dd609d8eea7053`.
- Captured stdout SHA-256: `d2563c122dac6548f0fe1e4ced1d069b071ccd2ee50896a43cdf655b660a1594`.
- Captured stderr SHA-256: `98f4a2c4df3c95b2b4c4472f2e0098b40d7268cdb7b6272e7762cd7511c2620f`.
- Evidence folder: `C:\Users\vinxe\AppData\Local\Temp\C11D_CROSS_TYPE_RECOVERY_20261015_184503`.
- Receipt lines: six entries for `challenges` (baseline/gameplay-only/music-only × run 1/run 2) and six entries for `visual_loops` with the same variant/repeat pattern. Every line says `canonical V1 receipt PASS`.

## Strictly bounded interpretation

Selector A is `content_type=challenges`, `family_id=parking_v2`, `variant_id=CHALLENGE_004`. Selector B is `content_type=visual_loops`, `family_id=c11c_geometric_waves_v1`, `subtype_id=harmonic_membrane`. All other Challenge selectors, all other Visual Loop grammars/families, arbitrary requests and automatic/default seed behavior remain outside this run.

The report's execution boundary says:

- `c11c_source_mutation=false`
- `renderer_activation=false`
- `renderer_dispatch_invoked=false`
- `renderer_input_emitted=false`
- `production_execution=false`
- `media_created=false`
- `request_input_persisted=false`
- `payload_files_written=false`
- `receipt_files_written=false`
- `output_artifact_path=null`
- `release_authority=NONE`

The report status is `PREPARATION_ONLY_CROSS_TYPE_SEED_DOMAIN_AUDIT_NOT_INPUT_ADMISSION`. It explicitly lists seed coverage and selector expansion as unclosed requirements.

## Verification discipline for later contexts

Keep raw stdout/stderr and their hashes distinct from the JSON report's internal `audit_sha256`. Do not hash or cite a missing file. Do not convert a logging/parsing exception into a test failure or pass. A future run needs an actual process exit code of zero plus the expected machine-readable summary, version, pins and receipt count before printing PASS.
