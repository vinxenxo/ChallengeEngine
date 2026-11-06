# C11-E PowerShell Runner Style Guide — V5

**Applies to:** every Windows operator runner and recovery/apply script for C11-D/C11-E. **Target runtime:** Windows PowerShell 5.1. The operator commits each iteration; Git is outside runner scope.

## 1. Authority and checkout discipline

- Active checkout only: `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Snapshot ZIPs are evidence, never checkout overlays.
- Never run Git from a per-iteration runner: no `git status`, `rev-parse`, `HEAD`, branch, diff, staging, commit or ref checks. Do not require `.git`; do not compare commit IDs or print Git status. The operator manages commits.
- Keep SHA-256 pins for the exact files being consumed/protected. Keep the frozen C11-C manifest check. SHA pins validate source identity independently of Git.
- Never touch C11-C frozen mechanics, generators, binders, timelines, RNG, simulation truth, core audio or manifest. Prefer D-owned/test-only paths. No source write unless the task explicitly requires a bounded D-only patch with pre/post hashes and protected-path guards.

## 2. PowerShell 5.1 parse and syntax

- First executable operation: native AST parse of the exact `.ps1` using `[System.Management.Automation.Language.Parser]::ParseFile(...)`; stop on any parse error. Print the PowerShell runtime version.
- Avoid PS7-only syntax and operators: no `&&`, null-coalescing, ternary operator, `ForEach-Object -Parallel`, etc. Do not use `Read-Host` in automation.
- Never write `$variable:` inside an expandable string; PowerShell parses it as a scoped/drive-qualified variable reference. Use `${variable}:`, `-f`, or string concatenation. V1 reserved-band runner failed parse at `$i:` in two error strings; V2 corrected this to `${i}:` and native PS5.1 AST passed.
- Use `Start-Process -Wait -PassThru` where appropriate, or `System.Diagnostics.Process` with concurrent stdout/stderr draining and an explicit timeout. Do not leave subprocesses unbounded.

## 3. Process contract (mandatory)

For each external process record: executable path, full argv/working directory, start/finish, timeout, numeric exit code, stdout path/byte count/SHA-256, stderr path/byte count/SHA-256. Persist stdout and stderr separately. Check file existence, exit code, and semantic output markers. Do not infer a failure from stderr presence or infer success from one console line.

Prefer wrappers returning a typed record (`ExitCode`, `TimedOut`, `StdoutText`, `StderrText`, paths, hashes). Do not pass text to a path helper or paths to a content helper. In V2, `Test-CaptureLog` used `Test-Path` + `ReadAllText` (path contract) but Movie Maker branch passed `$movie.Stdout` (text contract); the runner falsely blocked despite a successful AVI. Use separate names such as `Test-CaptureLogPath` and `Test-CaptureLogText`, or a single explicitly typed/validated parameter contract.

## 4. Distinct telemetry by execution mode

- Godot live-root run may emit the consumer `SUMMARY` marker and frame/mount counters.
- Godot Movie Maker capture has a different completion/configuration/phase telemetry contract; do not require live-root-only summary markers from Movie Maker stdout.
- Validate mode-specific semantic markers (`CONFIGURED`, phase cadence, audio flag, `Done recording movie`, output path, actual file probe) and use the live-root receipt for its own counters. Never collapse these two logs into one pattern.

## 5. Self-contained packaging

- A runner must have one documented extraction/execution path. Prefer embedding its small Python worker and doc payload archive in the `.ps1` (base64 + SHA-pinned) when the operator should need only one file in Downloads.
- Do not require external manifests/docs directories unless the README lists every required artifact and preflights them before any project write. Recovery V1.1 failed once because the manifest was missing and again because only the manifest, not its referenced docs, had been copied. Recovery V1.2 fixed this with an embedded, SHA-verified docs ZIP self-hydrated under the run root.
- Before installation, verify archive CRC, manifest schema, relative safe paths (no absolute paths/`..`), byte counts and SHA-256 for every file. Preflight all destination collisions before writing any. Write add-only; identical existing files may be reused, conflicting content must stop.

## 6. Recovery, resumability and no false PASS

- Use a unique run namespace; never overwrite prior evidence. Reuse an existing artifact only after exact path/size/SHA/metadata verification. If an artifact exists but its provenance is missing/mismatched, stop and preserve it.
- Stop at the first failed precondition. Do not hash nonexistent outputs, run dependent tests, or continue after failure. Preserve failure receipt with exact stage, exception, logs and input hashes.
- Use one bounded runner. Do not repeat Python tests, Godot, Movie Maker, media encoding or already-accepted phases when the captured evidence is intact.
- Print PASS only after all required artifacts, hashes, FFprobe/semantic checks and receipts are verified. Mark technical gates `PASS_TEST_ONLY` when they do not establish production authority or human acceptance.

## 7. Known C11-E launcher incidents (do not repeat)

1. **V1 reserved-band PS parse failure:** unescaped `$i:` in two strings. V2 fixed to `${i}:`; AST passed.
2. **V2 Movie Maker false-negative:** path-based `Test-CaptureLog` received `$movie.Stdout` text. AVI capture succeeded; orchestration falsely BLOCKED. Keep path/text contracts distinct.
3. **Recovery V1 stale Git gate:** pinned previous `HEAD`; invalid because operator commits every iteration. Remove all Git interaction; retain content SHA pins.
4. **Recovery V1.1 docs preflight:** first manifest absent, second manifest existed but referenced docs/prompts were absent. Do not assume copying a manifest copies its payload.
5. **Recovery V1.2 success:** self-hydrated embedded docs package; PowerShell 5.1 AST PASS; V2 evidence/source pins PASS; six FFmpeg/FFprobe calls exit 0/no timeout/zero stderr; 8 stills and pixel audit PASS; silent MP4 generated; no source writes or reruns.

## 8. Current workflow-specific notes

- The V2 Movie Maker AVI carried incidental PCM audio while capture was configured with `audio_enabled=false`. Discard it with explicit video-only mapping; never treat it as D3 music.
- Recovery V1.2 MP4 is intentionally silent. Its SHA is `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f`. The next E4A.7 runner must add audio with `-c:v copy`, not re-encode video.
- E1 music contract still leaves tempo/duration unresolved. Test-only fixture values must be named as such; derive duration from FFprobe, never call a historical tempo a product default.
- Any change to the runner requires a native PS5.1 AST parse on Windows. A Linux/static check is useful but must not be described as that native parse.

- When reusing a helper that writes to a fixed intermediate filename (for example E3 `_master_qa` writes `master_mono_check.wav`), preserve each case-specific artifact immediately under a unique label and verify its hash before the next call can overwrite it.


## 9. Child-worker evidence packaging (E4A.7 lesson)

A successful worker may create a second, detailed evidence ZIP while a PowerShell wrapper creates its own outer ZIP. The outer wrapper is not the child evidence archive unless it explicitly includes it. On completion, the wrapper must:

1. Verify the child ZIP exists at the exact worker-reported path.
2. Verify its file length, SHA-256 sidecar and archive CRC.
3. Include the child ZIP itself in the operator-facing package, or explicitly print that it is a separate required upload and never label the wrapper ZIP as the complete evidence bundle.
4. Preserve and include the child receipt/report, SHA256SUMS, FFprobe JSON, all media artifacts and process logs.
5. Ensure the wrapper receipt records both wrapper and child artefact hashes and byte counts.

A worker exit code 0 and final PASS marker are strong runtime evidence, but if the child evidence archive is absent, mark the artifact audit `PENDING_CHILD_ARCHIVE`. Never invent measured output values from a summary log.

## 10. Manual acceptance boundaries

Machine audio QA (loudness, peaks, non-silence, mono compatibility, deterministic hashes and mux metadata) is not a substitute for operator listening. Record human listening, visual inspection and GUI/CLI interaction as separate acceptance rows. Do not infer human review from generated reports or code paths.

## 11. E1 GUI/CLI parity reuse

Before adding a new parity launcher, inspect the existing Producer D9.9/D9.10 handler. Where its GUI action already calls `prepare_c11e_production_intent(... request_origin="GUI")`, invokes the E1 CLI with `--origin CLI` on the same saved request, and writes `c11e_gui_cli_parity.json`, use that native workflow. Do not duplicate the service or introduce a new UI surface.
