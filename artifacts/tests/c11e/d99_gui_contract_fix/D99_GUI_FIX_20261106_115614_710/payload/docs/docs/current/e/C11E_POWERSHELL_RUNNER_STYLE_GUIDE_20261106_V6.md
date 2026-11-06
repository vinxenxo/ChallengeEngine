# C11-E PowerShell Runner Style Guide — V6

**Applies to:** Windows operator runners/recovery scripts for C11-D/C11-E. Target Windows PowerShell 5.1. Operator manages commits; runner Git access is forbidden.

## 1. Authority / checkout

- Active checkout only: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`; snapshots are evidence, never checkout overlays.
- No Git invocation or inspection: no status, HEAD, branch, diff, staging, commit, `rev-parse`, `.git` requirement or commit-ID gate. The operator commits each iteration.
- Pin exact consumed/protected files with SHA-256 and validate the frozen C11-C manifest. These are content identity checks, not Git state checks.
- Keep C11-C generators/mechanics, RNG, binders/timelines, simulation truth, shared presentation/core audio and manifest immutable.

## 2. PowerShell 5.1 syntax/parse

- Report runtime and run native AST parse using `[System.Management.Automation.Language.Parser]::ParseFile(...)` at runner start.
- Do not use PS7-only syntax/operators (`&&`, null-coalescing, ternary, parallel foreach, etc.). Avoid `Read-Host` in automated flows.
- Never interpolate `$name:` in an expandable string; use `${name}:`, `-f` or concatenation. Recovery V1 reserved-band failed at `$i:`; V2 fixed it.
- Keep dynamic command invocation unambiguous; prefer argument arrays with `ProcessStartInfo` or safely quoted `Start-Process` arguments. Drain stdout/stderr concurrently and bound every process with timeout.

## 3. External process evidence

For each process record executable, argv, working directory, start/finish, timeout, numeric exit code, stdout/stderr path, byte count and SHA-256. stdout/stderr are separate files. Non-empty stderr is not automatically failure: FFmpeg's loudnorm, ebur128 and volumedetect commonly write normal diagnostics/measurements to stderr. Determine success from exit code plus semantic output, probe and artifact predicates.

Never pass text to a path helper or a path to a text helper. Use clearly typed `Test-LogPath` and `Test-LogText` helpers or validate parameter contracts. Keep mode-specific telemetry separate (live-root vs Movie Maker).

## 4. Self-contained delivery / add-only docs

- If one `.ps1` is the operator-facing artifact, embed its worker and doc payload ZIP in the script with SHA pin; do not require loose docs/manifests unless every dependency is explicit and preflighted.
- Validate archive CRC, manifest schema, safe relative paths (no absolute paths/`..`), file count, byte sizes and per-file SHA before writes.
- Preflight all destination collisions before the first write. Add-only install; identical existing files may be reused; differing content stops before any write.
- Ensure documentation index references only files present in the package or already confirmed in the checkout.

## 5. Output/evidence packaging

- Distinguish wrapper log/package from worker-produced evidence ZIP. A wrapper PASS is not an auditable media result until the nested worker ZIP exists, is included or separately uploaded, its expected SHA matches, and all internal checksums are verified. E4A.7 outer wrapper omitted the worker ZIP; the worker had succeeded, but independent output audit needed the separately uploaded `RUN_...zip`.
- Verify every nested SHA manifest entry and receipt/report sidecar. Preserve exact worker outputs, process logs, FFprobe JSON, raw/mastered/decoded WAV, elementary streams, mux MP4s, intents and receipts.
- Record which evidence was user-inspected and which requires human listening. Never infer audio quality or visual approval solely from automated metrics.

## 6. Rerun/recovery discipline

- Unique namespace per attempt; never overwrite prior evidence. Reuse outputs only after source SHA, metadata, size and hash all match.
- Stop on first failed precondition; retain failure receipt and logs. Do not rerun upstream accepted phases to recover a downstream wrapper/package failure.
- One bounded runner per concrete task. No repeated generic launcher/installers or redundant accepted tests.
- Print PASS only after all required artifacts and hashes are independently verified. Mark test-only clearly; no production authorization follows from a test pass.

## 7. Recorded C11-E incidents

1. Reserved-band V1: unescaped `$i:` caused PS5.1 AST parse failure; corrected with `${i}:`.
2. Reserved-band V2: path helper received stdout text; false-negative despite successful Movie Maker capture.
3. Recovery V1: stale Git HEAD gate; removed permanently because commits are operator-managed.
4. Recovery V1.1: external docs manifest and its payload were missing; V1.2 embedded and self-hydrated the doc ZIP.
5. Recovery V1.2: success; no rerun of tests/Godot/Movie Maker; six FFmpeg/FFprobe checks passed, eight stills/pixel audit passed.
6. E4A.7 wrapper: Python worker exited 0 and created its 268-entry evidence ZIP, but wrapper ZIP did not include that generated ZIP. Require explicit nested output packaging/upload plus SHA/checksum audit; wrapper console PASS alone is not a final evidence review.
7. D3.3 fixed intermediate mono-check WAV: preserve case-labeled mono artefact immediately to avoid a shared filename overwriting prior cases.

## 8. Current E4A notes

- Recovery V1.2 visual MP4 SHA `841b035...` is silent intentionally; discard incidental AVI PCM.
- E4A.7 uses `-c:v copy`; source H.264 SHA must remain unchanged in A/B/C.
- E1 music contract leaves tempo/duration unresolved. 104 BPM is a labeled historical test fixture; 15 s comes from FFprobe. Never call these product defaults.
- E4A.7 technical pass does not satisfy GUI/CLI runtime parity. Operator A/B/C listening is separately confirmed PASS.


## 9. Minimal GUI contract patches

- Treat an error as an observed symptom, then reconcile it against the uploaded run artifacts before attributing the cause. In D99-GUI-D22A8281E993 the GUI request includes `presentation_options`, but the D9 request omits it and both parity receipts report PASS. Record this discrepancy; do not label the uploaded run as a failed receipt.
- D9.9 is strict: never add an E1-only field to the D9.9 universal request schema. If an option is not yet part of the GUI contract, omit it at the GUI request constructor; preserve any accepted E1 internal default.
- Before source edits, pin the exact active file bytes, dependent E1/D9 files and frozen manifest. No Git/HEAD/status/branch checks. Stop safely on source drift.
- Use exact, counted source anchors; reject zero or multiple matches. Keep the patch to the smallest D-owned GUI file set. Never change the D9.9 schema, resolver, E1 service, C11-C files or renderer for a UI-only request mistake.
- Add a focused regression test that asserts the GUI request contains no unsupported field and D9.8 canonical editorial keys remain present. Empty strings normalize to the established `UNKNOWN` sentinel; don't conflate empty-value normalization with field deletion.
- Run the narrow E1 unit suite and D9 request matrix only; do not rerun media or rendering. Preserve pre/post SHA, backup, test stdout/stderr, exit code and hashes.


## 10. Source-patch overlay discipline

- A hash-gated source patch must preflight every source pin, test destination and documentation destination before the first write. A collision anywhere stops the entire operation before source changes.
- Create/verify an add-only backup of the exact preimage before replacing a source file. Re-hash the source immediately before the write and again after it.
- Never put a previously published document path into a new overlay with different bytes. Advance the versioned filename; do not overwrite, repair in place, or weaken add-only collision checks. An older V2 documentation installer that collides with an occupied V69 path is rejected by design; publish a new non-colliding version set instead.
- Keep the patch on the named D-owned source file. Do not modify schema/resolver/service layers when the confirmed seam is GUI payload construction.
- Verify every canonical editorial key family-by-family in tests. A blank value may normalize to the existing sentinel `UNKNOWN`; that must never delete its key. Do not implement future per-field selection controls before the user authorizes that stage.
- A successful evidence ZIP that differs from a separately reported error is not the error trace. Preserve both facts and make the minimal boundary hardening without mislabeling the successful receipt.
