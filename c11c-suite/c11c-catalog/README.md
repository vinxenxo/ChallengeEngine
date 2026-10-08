# C11-C Catalog 0.2.0 — C11-D integration

The existing `c11c-catalog` application remains the only Catalog surface. Version 0.2.0 preserves the generic artifacts browser and adds **C11-D Products / Provenance**.

## Governed sources

- D7.3 canonical intent catalog, only with successful D7.3 validation and PASS/CLOSED D7.3/D7.4 receipts.
- D9.4 acceptance manifest's exact five media rows, each path constrained to the project root and SHA-256/size verified against disk.
- D9.5.1 Producer GUI saved plan records, only with the known receipt schema, complete companion evidence, identity/hash/parity consistency and all execution guards false.

D9.4 media rows require a valid D8.7 PASS_NO_MEDIA/CLOSED receipt and the canonical empty explicit media scope. The Catalog never infers a D product from a filename or arbitrary folder, never promotes historical media, never renders media and never grants release authority. D9.1–D9.3 physical pilot media are shown as `VALIDATED_PILOT` only and remain `NOT_REGISTERED_FOR_D8_RELEASE`. D7 rows are `PLAN_ONLY`; Producer request rows are `PLAN_ONLY` and carry a canonical D4.5 CLI plan-reproduction command.

## Tests

```powershell
python .\c11c-suite\c11c-catalog\self_test.py
python .\c11c-suite\c11c-catalog\test_catalog_gui_contract.py
python .\c11c-suite\self_test.py
```

The Python data projector is standard-library-only so receipt/provenance checks are testable without launching Qt. The actual window still requires the existing PySide6 runtime and must be smoke-tested on Windows.

`renderer_execution=false`; `production_execution=false`; `release_authority=NONE`; `media_rendered_by_catalog=false`.
