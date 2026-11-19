# C11-E Option C installer incident ledger — V4

Date: 2026-11-19. Active checkout remains the sole authority. This ledger records observed outputs; it does not rewrite prior receipts.

| Package | Failure | Pre-transaction result | Disposition |
|---|---|---|---|
| Frame compositor V1 | Non-identical destination `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261119_V186.md` | Installer source inspection showed collision at line 153 before write block at line 224 | Closed; no rerun |
| Frame compositor V2 | Three non-identical Handover V16 / Prompt V187 destinations | Operator output: `TRANSACTION_STARTED=FALSE`, `PROJECT_PAYLOAD_MUTATION=FALSE` | Closed; no rerun |
| Frame compositor V3 | Python 3.13.14 exists but `PIL` import failed with `ModuleNotFoundError` | Operator output: `TRANSACTION_STARTED=FALSE`, `PROJECT_PAYLOAD_MUTATION=FALSE` | Closed; no rerun |

V4 removes the dependency entirely. The area filter is implemented with standard-library bytes/memoryview/integer arithmetic. V4 does not require pip and does not install dependencies. Its documentation uses one package-specific history directory to avoid replacing canonical current prompt/authority files. The installer must list all destination collisions and fail before writing if any exist.

Do not delete or overwrite any prior prompt, authority, receipt, failed package or staging directory as a collision workaround. No previous installer is to be repeated.
