# C11-E — execution hygiene and assistant error log (V7)

## Mandatory controls

1. One self-contained package with exact ZIP name/hash and one pasteable Windows PowerShell 5.1 command. Never assume files are already in Downloads.
2. Verify branch, exact HEAD/parent, receipts, C manifest, payload hashes, every destination preimage and every add-only destination before the first write.
3. Archive exact pre-E instructions before replacing them. Preflight archive targets as absent or exact hash-matching; record archive postimages in the receipt.
4. Capture each native executable as one absolute existing path. `Get-Command -All` can return multiple Python applications; filter WindowsApps and select one element, never cast the collection to string.
5. Record `FileName`, arguments, working directory, `file_exists`, full `Process.Start()` exception and inner exception before claiming a process was started.
6. Capture `$LASTEXITCODE` immediately. Failed installation prevents verification/render. Failed runner prevents PASS. A later `Write-Host` is not evidence.
7. Failure/evidence ZIP: first write nonempty diagnostic evidence; compress existing paths only; then assert the archive exists, is nonzero, opens, contains entries and has a computed SHA-256. Never print a path/hash before those checks.
8. No output overwrites. Every retry uses a new RequestId. Partial AVIs/MP4s and quarantine copies remain preserved.
9. Distinguish static tests, Python tests, PowerShell parse/runtime, GDScript parse, Godot runtime, physical AVI, delivery MP4, mux, pixel comparison, human visual/audio review and overall family acceptance.
10. No global inventories unless a source pin changed or an explicit baseline decision requires one. Prefer focused source/call-graph work.
11. C11-C mechanics, manifest, frame stream, RNG and protected sources remain untouched. Never enumerate arbitrary `custom_data`.
12. D governance and receipts remain unchanged; E receipts are a separate ledger.

## Assistant incidents and prevention

- E0 upload/capture: `else` pasted in a separate PowerShell submission. Prevention: entire script or single contiguous block.
- E1 package: assumed generated files existed in Downloads. Prevention: one autocontained ZIP and exact extraction path.
- E1 installer: `$Relative:` PowerShell interpolation parser failure. Prevention: `-f`/`${Relative}`, complete-script syntax scan.
- E1 verify: launched despite failed installer. Prevention: immediate exit-code branch.
- Source-pin audit: compared permitted D integration roots to raw C hashes. Prevention: apply the baseline's protected-vs-D-root policy.
- E2 V2: pinned obsolete HEAD `bc8330e` after legitimate E1 consolidation `a3c7c5d`. Prevention: exact current commit, parent and receipts are part of package generation.
- E2 V3: bad separator prefix in path guard. Prevention: `GetFullPath`, `DirectorySeparatorChar` and positive/negative tests.
- E2 V4: `Get-Command python` returned Python313 and WindowsApps; collection `.Source` concatenated. Prevention: one resolved absolute executable; explicit path supported.
- E2 V4 failure report: announced a ZIP that did not exist because stage was empty. Prevention: create diagnostics and verify archive existence, length, entry count and SHA before output.
- E2 manual console: text `C11-E E2 V4 COMPLETED` was printed after exit 1. Prevention: only runner exit code plus receipt/media evidence may establish status.
- E0 re-entry package V1 review: it declared pre-E archive destinations but only validated them; it did not copy the V9 preimages before replacement. Prevention: V2 installer builds an archive plan, preflights every archive path, copies and verifies exact V9 bytes before replacing active files; archive copies appear in receipt.

## Publication standard

Before delivery, inspect the entire script and package manifest; validate hashes/CRC and path guards; test the fail-fast sequence; inspect success and error branches; explicitly disclose that PowerShell/Godot runtime was not executed in this environment. A clean ZIP is not proof of successful installation or rendering.
