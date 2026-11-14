# C11-E E4C R4 — intent SHA semantic mismatch and R5 repair

## Evidence

`R4_RECOVERY_20261114T092932Z.zip` diagnostic reported `REQUIRED_INPUT_SHA_MISMATCH` for `e1_intent.json`, actual file SHA `dfc861764302d7a6dec71de4532828dfe146708ed33dd2483b9c611bdd2f9a94`. Preserved JSON field `intent_sha256` and E1 receipt field were both `9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e`.

## Root cause

The SHA field is self-excluding canonical JSON digest, not raw file bytes digest. Recovery code and the prior PowerShell wrapper conflated the two. No source mutation or evidence corruption occurred; the diagnostic archived all relevant files and the accepted E1 receipt.

## R5 correction

R5 pins raw file bytes separately (`EXPECTED_INTENT_FILE_SHA256`), recomputes canonical intent hash after removing `intent_sha256`, checks the embedded field and `receipt.e1_validation.intent_sha256`, and emits both values in the technical receipt/audit. The installed wrapper uses raw hash only for file integrity and delegates canonical semantics to Python. Five regression cases cover this distinction; previous 12 recovery regressions remain.

## Guardrails

No edits to `e1_intent.json`, E1 service, C11-C manifest, production generators, media, output MP4, silent intermediate, plan or source pins. R5 is add-only documentation plus two exact replacements. Only the existing R3 output is revalidated and used to extract seven review PNGs.
