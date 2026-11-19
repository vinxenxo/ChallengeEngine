# C11-E Installer Incident Register — V54 (2026-11-19)

## E6 Render Gate Preflight V1–V2.1 incident closure

All incidents below are retained as failed evidence; none is to be retried as an installer chain.

| Package | Failure | Stage | Checkout mutation |
|---|---|---|---|
| Render Gate V1 | Six Python tests used `Path.read_text()` with Windows cp1252 against UTF-8 JSON; six `UnicodeDecodeError` failures | Unit tests | None |
| V1.1 | Operator's `$PackageRoot` remained the V1 extraction, so the V1.1 installer path did not exist; subsequent V1.1 `File.Replace` call also passed a null backup path | Invocation / installer | None |
| V1.2 | Interpolated string `"PREIMAGE_PIN_MISMATCH:$rel:$destSha"` failed PowerShell 5.1 parsing at `:$rel` | AST parse | None |
| V1.3 | Versioned roadmap/master handover destinations conflicted with existing LATEST snapshot documents; package included stale document revisions | Package preflight | None; `source_write_attempted=false` |
| Render Gate Apply V2 | `START_PROCESS_CAPTURE_CONTRACT_INVALID: APPLY`; static capture check rejected a valid `-RedirectStandardError $path` argument form | Staged read-only audit | None; no transaction started |
| Render Gate Apply V2.1 | Staged project mirror lacked the family-editorial audit receipt sidecar at the referenced path | Staged read-only audit | None; no transaction started |

The V2.1 run passed PS 5.1 AST, 21/21 source pins, 8/8 predecessor receipts in active checkout, Python 3.13.14, 44/44 unit tests and 7/7 atomic-I/O tests before staged audit failure. The failure receipt was `6d0dce8ede2552985abed09b5623abe82f55a0c494f6c8d5f595997979e1dd31` (failure run `cd40066b6ca743769f31abd34a335fdd`). The failure was caused by staging incompleteness, not evidence absence in the active checkout.

The parent PowerShell console later displayed `E6_RENDER_GATE_PREFLIGHT_V2_APPLY=PASS` after the nonzero child exit and terminating throw. That later line is not a valid success state; the authoritative result is `APPLY_EXIT=1` and `NO_PASS_EMITTED=TRUE` in the child failure receipt/log.

## Process discipline lessons

- Never ask the operator to retry V1/V1.1/V1.2/V1.3/V2/V2.1.
- Do not stage a partial project mirror if an audit expects predecessor sidecars. Either audit the active root directly or materialize the complete exact input set and validate every copied hash before invoking the auditor.
- A parent directory's existence is not a file destination collision. Compare the exact destination file only.
- `Start-Process` capture contract must be tested against the real PowerShell command shape; do not use brittle end-of-line regexes that reject a valid parameter value.
- Use `Parser.ParseFile` in Windows PowerShell 5.1 before invocation. Do not report AST PASS from a different runtime.
- Native child exit code must be captured immediately. Nonempty stderr alone is not failure. Do not print any PASS after a failed child.
- Use real non-null backup paths for any `File.Replace`; add-only transaction must use CreateNew/Move to absent destinations, not replace.
- All document destination names must be selected from the exact latest snapshot version inventory before writing the package; do not synthesize versions from older chat state.

## Current incident status

`RENDER_GATE_PREFLIGHT_V2` and `V2.1` are CLOSED `FAILED_CLOSED` before transaction. No rollback is required and no preflight installer is to be invoked again. Subsequent E6 work proceeds as a separate functional PREPARE_ONLY increment, not another preflight patch.
