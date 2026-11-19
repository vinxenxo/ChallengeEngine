# C11-E E6 Option C V2 — Installer and recovery contract

## Installation model

Add-only, transactional, PowerShell 5.1 installer. It installs a single versioned probe folder and versioned historical documentation. It does not replace `tools/c11d/d9/c11e_e6_loop_option_c_frame_compositor_v3.py`, D9/E1 services, C11-C, definitions, manifests, Producer GUI or governance files.

## Required safeguards

1. Parse the installer itself with `System.Management.Automation.Language.Parser.ParseFile` before performing I/O; stop on any parse error.
2. Require PowerShell 5.1 and a non-empty explicit project root containing the exact C11-C manifest and D4.8 V2 path.
3. Require `-ExpectedPackageZipSha256`; compare the ZIP with the out-of-band value printed with the package.
4. Open the ZIP with .NET `ZipArchive`; reject absolute paths, drive prefixes, `..`, backslashes, empty/invalid/reserved Windows path segments, duplicate/case-colliding names, duplicate destinations, excessive member count/size, unmanifested members and destinations outside the two explicit install roots.
5. Validate the embedded package manifest and SHA/byte identity of every member other than the manifest itself before extraction. Check ZIP entry lengths against manifest lengths and use bounded 1 MiB streaming into a new unique temp folder; abort if any expanded member exceeds its declared size, then verify stage postimages.
6. Verify frozen C11-C manifest (796,318 bytes / exact SHA) and D4.8 V2 (12,996 bytes / exact SHA) immediately before preflight.
7. Preflight every destination in full before writing any file. Existing byte-identical postimage = `SKIP_IDENTICAL`; existing differing file = hard collision. No force/overwrite route.
8. Write to a unique sibling `.partial` using `CreateNew`, flush/close, re-hash, then `File.Move` to a destination that must still be absent. This prevents replacement.
9. On exception, remove only receipt/sidecar partials in this run's unique receipt folder, then rollback only payload paths created by this transaction and only when their current hash still equals the transaction's payload hash. Never delete existing or changed files.
10. Re-hash all installed postimages. Write the JSON receipt and SHA sidecar as unique sibling temporaries and move them atomically only after flush; the success marker is printed last under `artifacts/tests/c11e/e6_option_c_native_qt_probe_v2_install/<INSTALL_ID>/`.
11. Do not call Python, Godot, FFmpeg, FFprobe, audio, mux, launchers, Git, or production dispatch from installer.

## Idempotency and recovery

- Re-running against all identical postimages performs no replacements and records identical skips.
- Any pre-existing differing destination blocks before the first file is written. No manual deletion or overwrite is recommended; preserve the conflicting file and reconcile through a separately reviewed package.
- A failed partial installation rolls back only this run's verified additions and prints remaining paths if cleanup cannot be completed.
- An install receipt is written only after every file postimage passes. `PASS_ADD_ONLY` is never printed before receipt and sidecar are complete.
- The installer never reads or checks Git state. Operator owns commits. Source pins, not Git identity, are the integrity authority.
