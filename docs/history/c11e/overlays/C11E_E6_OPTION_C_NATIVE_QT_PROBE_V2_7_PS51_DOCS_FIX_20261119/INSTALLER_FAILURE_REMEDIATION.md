# V2.6 installer incident and V2.7 remediation

## Operator-observed V2.6 failure

The V2.6 installer reached the add-only write transaction, then attempted to verify repository documentation using:

```powershell
Where-Object { Test-Path -LiteralPath $_.destination -PathType Leaf -and (Get-Sha256 $_.destination) -eq $_.sha256 }
```

Windows PowerShell 5.1 parsed `-and` as an argument to `Test-Path`, producing `ParameterBindingException: No se encuentra ningún parámetro que coincida con el nombre del parámetro 'and'`.

The V2.6 catch path reported `ROLLBACK_STATUS=PASS; REMOVED_OWNED_ADDS=16`. This is the authoritative transaction outcome: all 16 files added by that invocation were removed after their SHA-256 postimages were rechecked. No V2.6 install receipt was retained because the transaction did not complete. The later `REPOSITORY_DOCS=9/9` line came from a separate interactive command after the preceding `throw`; it is not evidence of successful document installation. The first explicit `REPO_DOC_MISSING` confirms the absence.

The subsequent `Ran 0 tests ... NO TESTS RAN` / exit 5 and missing V2.6 runner were downstream consequences of the transaction rollback. No QImage test was executed in that attempt.

## V2.7 correction

- Replaces the problematic `Where-Object` expression with an explicit `foreach` loop. Each document is checked for leaf existence, exact byte count and exact SHA-256; the loop fails immediately on the first mismatch.
- Performs document postimage verification before creating a PASS install receipt/sidecar.
- Corrects count/path reporting so `DOCS_FILES=x/y` and `DOCS_ROOT=<actual path>` are independently emitted.
- Preserves transaction rollback of only current-invocation additions whose content still matches the expected SHA-256.
- Installs 7 versioned tool/test files and 11 documents, including current doc index V175, under the repository's observed `docs/current/e/` and `docs/history/c11e/overlays/` layout.
- Adds explicit QImage compositor and target-test file SHA/byte pins to the runner, based on the latest uploaded checkout snapshot.

No V2.6 files or receipts are treated as installed. No prior V2.1–V2.5 receipt is changed.
