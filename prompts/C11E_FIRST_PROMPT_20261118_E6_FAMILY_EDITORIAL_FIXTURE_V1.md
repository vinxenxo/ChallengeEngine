# FIRST PROMPT — C11-E E6 Smoke18 Family Editorial Fixture V1 (2026-11-18)

Continue in `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS` (active checkout is sole source authority). ZIP snapshots are evidence only. Do not extract over the checkout. `GIT_CHECKS=SKIPPED; COMMITS=OPERATOR_MANAGED; SOURCE_FILE_PINS=ENFORCED`. Use Windows PowerShell 5.1 and Python 3.13.14.

## Latest evidence

V2 readiness audit: `E6COMPREADINESSV2_20261118T214318Z_D41DD6C6`, SHA-256 `5470ee637b559977f266f1ed8131dbb1729bc9ef2225cddd58414efe3187035f`; status `PASS_AUDIT_ONLY_GAPS_IDENTIFIED_EXECUTION_HELD`, 17/17 pins, 36/36 Challenge written evidence, E6 accepted 0. Existing Challenge PREPARE_ONLY receipt SHA `b54a884f1574d22fa65ea198d279d9ba84bb3967adc87885213f7659a1b1c944` remains immutable. Reuse requalification receipt SHA `4d63b8caec7a975cc0362ee9d7a5924f5ab8371e8e8e1457e1d60956bf65ce33` remains a candidate inventory, not acceptance.

## Operator editorial requirement

Use separate non-default synthetic Spanish copy for all three families and pass it through every Smoke18 family test:

- Challenge (6 rows): `E6 · DESAFÍO EN PRUEBA` / `RITMO Y PRECISIÓN EN PRUEBA` / `PROBAR DESAFÍO`.
- Visual Loop (6 rows): `E6 · BUCLE EN PRUEBA` / `SECUENCIA VISUAL EN PRUEBA` / `REPETIR BUCLE`.
- Visual Drill (6 rows): `E6 · DRILL EN PRUEBA` / `CONTROL DE SERIES EN PRUEBA` / `INICIAR SERIE`.

One triplet is assigned to all rows in its family. Challenge receives it on A/B_REPEAT/C_CHANGED_MUSIC_SEED for each of six selectors (18 nested targets). Combined with six Loop and six Drill rows, this is 18 top-level scenarios / 30 editorial targets. Do not inflate the Smoke18 denominator.

## Install and run

Follow `README_C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1.md`. The installer is at the ZIP root. Verify the ZIP sidecar first, extract to a fresh temp folder, run the ADD_ONLY installer, and only after PASS run `tools\c11d\d9\RUN_C11E_E6_SMOKE18_FAMILY_EDITORIAL_FIXTURE_V1.ps1`. Do not re-extract to or overwrite the active checkout.

## Interpretation

PASS proves fixture pinning and PREPARE_ONLY assignment coverage only. It does not prove visual readback. Challenge and Drill need consumer readback; Loop D postcompositor remains blocked/not admitted. Compare actual consumed text against family defaults before claiming non-default consumption. Keep player name and challenge label UNKNOWN/BLOCKED.

## Invariants

C11-C frozen manifest SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`; D4.8 V2 SHA `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`, unchanged/BLOCKED. E1 PREPARE_ONLY; renderer OFF; dispatch/media false; release authority NONE; E6 accepted 0; Matrix not frozen. No Godot, FFmpeg, FFprobe, D3/audio, PCM, mux, renderer, dispatch, BatchId or media creation. Do not rerun accepted A/V.
