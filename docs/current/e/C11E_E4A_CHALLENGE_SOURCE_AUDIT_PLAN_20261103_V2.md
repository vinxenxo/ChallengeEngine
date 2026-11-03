# C11-E E4A Challenge — Source Audit Plan V2

## Purpose

Run a fail-closed, read-only source inventory against the active Windows checkout. V2 replaces the incompatible PowerShell V1 collection/pattern handling. It must not patch the repository's production source or invoke rendering.

## Required output

- Exact source path, byte count and SHA-256 for all key service/CLI/GUI/D9/D3/E3/freeze files.
- Candidate binder/consumer and layout/presentation files, with line-numbered symbol/field references.
- Trace of E1 request/editorial model → D9 bridge/adapter → existing Challenge visual consumer → composited slots.
- Current approved field subset and destinations, with `language` metadata-only; reserved fields remain disabled.
- Existing CLI call and argument contract plus current GUI dispatch callback. Both routes will invoke the same service/worker.
- Exact current C11-C manifest identity.

## Compatibility implementation

The V2 PowerShell runner uses ordinary arrays and PSCustomObject records, one `Select-String` pattern per invocation and bounded output. It records exception type, invocation line and script stack trace. It is compatible with Windows PowerShell 5.1; no PowerShell 7 syntax is required.

## Gate

`E4A.0=PASS_READ_ONLY` only after the full JSON/Markdown reports are written and all required source-root scans finish. If the audit blocks, retain its diagnostics and do not begin E4A code changes. No GUI, CLI production task, renderer, Godot, FFmpeg or media is invoked.
