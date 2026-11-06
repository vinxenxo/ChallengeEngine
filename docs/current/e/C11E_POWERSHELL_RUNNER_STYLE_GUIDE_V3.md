# C11-E PowerShell Runner Style Guide — V3

**Purpose:** prevent repeatable Windows PowerShell 5.1 launcher defects in C11-E evidence runners. This guide is normative for future runner authoring and packaging. Target runtime is Windows PowerShell 5.1.

## 1. Parse and language compatibility

1. Parse the complete packaged `.ps1` with Windows PowerShell 5.1 before delivery. An in-runner parser check cannot rescue a syntax error that prevents startup. Validate the exact packaged bytes after final packaging.
2. Do not use PowerShell 7-only syntax: `&&`, `||`, `??`, ternary `?:`, null-conditional operators, pipeline-chain operators, or newer APIs absent from Windows PowerShell 5.1.
3. Never write an expandable string containing `$name:`. PowerShell can parse the colon as a scope/drive separator. Use `${name}` or, preferably for diagnostics, `('message {0}: {1}' -f $name,$value)`.
4. Quote strings and paths explicitly. Use `-LiteralPath` for filesystem operations. Use descriptive variable names and invariant culture for serialized numbers.

## 2. Path, text and process contracts

1. A path helper must declare a path parameter, verify `Test-Path -LiteralPath ... -PathType Leaf`, then read the file.
2. A text helper must accept in-memory text and must not pass that text to `Test-Path` or `ReadAllText`. Keep `...Text` and `...File` helpers separate.
3. Never pass `$process.Stdout` to a path-based helper. E4A.6 V2 did exactly that; it returned a false BLOCKED after Movie Maker completed. The defect was a path-vs-content contract mismatch, not relaxed acceptance criteria.
4. For ordinary bounded Windows tools, use `Start-Process -Wait -PassThru` with separate stdout/stderr files. Inspect the process `.ExitCode`; preserve byte counts and SHA-256 for both logs.
5. When hard timeouts and concurrent draining are required, `System.Diagnostics.Process` is an explicit exception: set `UseShellExecute=false`, redirect both streams, start both `ReadToEndAsync()` tasks before waiting, enforce timeout, capture actual exit code, then persist and hash both files.
6. Do not require empty stderr unless the tool contract defines any stderr byte as failure. Never merge stderr into stdout as a substitute for evidence provenance.
7. Record exact executable/arguments/working directory, exit code, timeout flag, stdout/stderr paths, byte counts and hashes.

## 3. Godot process-mode telemetry

1. Treat live-root runtime (`--quit-after`) and Movie Maker (`--write-movie`) as distinct process contracts. Never require one mode's marker from the other.
2. E4A.6 live-root emits `C11E_E4A6_LIVE_CONSUMER_SUMMARY`; Movie Maker emits `C11E_E4A6_LIVE_CONSUMER_CONFIGURED`, `TELEMETRY_JSON`, `AUDIO_EXPORT_JSON`, and `Done recording movie at path`, plus frame/FPS telemetry.
3. Movie Maker semantic validation includes matching envelope SHA, success/enabled true, source_frames=900, phase counts 180/420/180/120, audio export disabled, successful completion and a real AVI. FFprobe independently validates dimensions, frame rate, frame count and duration.
4. `audio_enabled=false` does not guarantee no AVI audio stream. The E4A.6 AVI contains PCM S16LE 48 kHz stereo; a video-only derivative must explicitly map `0:v:0` and use `-an`.

## 4. Validation and evidence design

1. Separate tool success, semantic log success, artifact existence, technical media contract, and pixel/content audit.
2. Parse JSON only after its marker is verified; catch parse errors; cast numeric values; compare identity/hash fields exactly.
3. Tie every artifact to its source/envelope SHA and tool contract. Record file hashes, byte sizes, FFprobe JSON, logs, exit codes, durations and frame counts.
4. Recovery must resume from the last verified artifact, not repeat accepted renders/tests. Preserve mismatched files; never silently overwrite evidence. Reuse only when hash and provenance match.
5. Add-only documentation must preflight every collision before the first write, verify each packaged SHA, write via a temporary sibling, and verify postimage SHA. Never replace a versioned record in place.
6. A failure receipt must name the exact failed predicate and last successful stage; do not label orchestration failure as an application/render defect.

## 5. Visual sampling and media handling

1. Distinguish logical from delivery dimensions and state scale factor. E4A.6 logical 540x960 to delivery 720x1280; each 144 logical-pixel reserved band becomes 192 delivery pixels.
2. Sample defined frame indices and interior pixel coordinates; record thresholds, sample counts, non-black ratio and active-text counts.
3. Map only intended streams (`-map 0:v:0 -an`) when source capture contains unwanted audio. Validate final output using FFprobe and ensure no unintended streams remain.
4. File metadata and stream inspection are authoritative; a console marker alone does not prove encoder/audio properties.

## 6. Git and iteration ownership — mandatory

1. **Do not invoke Git from per-iteration engineering/evidence runners.** Do not run `git status`, `git rev-parse`, read `HEAD`, compare commit IDs, require a `.git` directory, or serialize Git state into receipts.
2. The operator creates a commit at each iteration. A changing `HEAD` is expected and must never block source tests, evidence recovery, or postprocessing.
3. Protect the actual engineering boundary with exact file-level SHA-256 pins, frozen manifest hash/byte count, path allowlists and pre/post source hashes. Those checks remain mandatory; they are independent of Git metadata.
4. Runners must not stage, commit, reset, clean, switch branches, rebase, amend or push. This is a no-Git-interaction policy, not merely a no-mutation policy.

## 7. Packaging and rollout

1. Package one runner at ZIP root with README, SHA sidecar and manifest of all embedded docs/payloads. Verify CRC, sidecar, runner SHA, all doc hashes and archive paths after final build.
2. Keep runner, evidence and output namespaces versioned. Never recycle an output directory when semantics change.
3. Active Windows checkout is source authority. Never overlay snapshots/evidence ZIPs. Recovery-only runners remain source-read-only.
4. Keep the runner's scope narrow; do not create extra launcher layers to compensate for evidence already captured.

## 8. Incident index

| Incident | Root cause | Prevention |
|---|---|---|
| Reserved-band V1 parser failure | `$i:` in expandable strings parsed as scoped variable syntax. | PS 5.1 parse the exact packaged file; use `${i}` or `-f`. |
| Reserved-band V2 false BLOCKED | Path-based helper received in-memory stdout text. | Separate text/file helpers and test the exact call-site parameter contract. |
| Movie Maker SUMMARY mismatch risk | Live-root and Movie Maker emit different telemetry. | Validate the exact marker set for each invocation mode. |
| Recovery V1 false BLOCKED | Runner pinned `git rev-parse HEAD` to an earlier commit and required `.git`; operator had legitimately committed the iteration, so preflight stopped before evidence validation. | Never read Git state in per-iteration runners. Retain exact source and manifest SHA pins only. |

**Current rule:** do not rerender, rerun accepted tests, or create another launcher layer to fix an orchestration-only failure. Reuse the last verified artifact and apply the smallest correction.


## 7. Self-contained packaging and documentation payloads

1. A runner advertised as “run from Downloads” must not require the user to manually copy a manifest, documentation folder, sidecar payload or nested relative tree next to it. A manifest only describes files; it does not supply them.
2. Prefer a self-contained runner with its small, versioned documentation bundle compressed and embedded as Base64. Pin the exact compressed bytes with SHA-256; at runtime decode, hash-check, write to a unique run-scoped temporary/evidence folder, safely extract, then validate the embedded manifest and every document SHA before use.
3. Do not extract embedded package data into the checkout before all media/pixel gates pass. Keep it under that run's evidence directory. Copy versioned docs into the project only in the final add-only stage, with collision preflight before the first write and per-file post-write SHA verification.
4. The runner must operate when it is the only downloaded file. Any optional external package/README may aid human inspection but cannot be a runtime dependency. Do not make the operator move manifests to Downloads.
5. Failure receipts must identify `DOCUMENTATION_PREFLIGHT` separately from media processing. Missing manifest/payload is a packaging error, not an evidence or renderer failure. V1.1 demonstrated that copying only the manifest leaves all referenced relative document paths unresolved.
6. Before delivery, test ZIP entries and the extracted staging algorithm, verify archive SHA and every embedded manifest path/hash/byte count, scan the packaged PowerShell for forbidden Git calls and PS7-only syntax, and run a native Windows PowerShell 5.1 AST parse when available. Do not claim that native parsing was performed in a Linux-only build environment.
