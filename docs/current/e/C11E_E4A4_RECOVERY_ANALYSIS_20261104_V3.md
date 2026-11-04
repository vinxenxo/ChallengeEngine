# C11-E E4A.4 recovery analysis — V3

**Date:** 2026-11-04  
**Status:** worker PASS recorded; recovery utility V3 prepared. Archive inspection/operator review pending.

## Worker evidence

Windows run folder: `RUN_20261104T013653Z-8469583E`  
JSON `run_id`: `20261104T013653Z-8469583E`  
Worker ZIP SHA-256: `ccdef6038be84bb4216f6777592a7adf6ba0ec084887f536088df6bbe952d01f`  
Inner receipt SHA-256: `8d351c513b6972d4f583dfe6678ab46e0441ab0466315a03abf1ce1179c115ca`  
Worker native exit code: 0; marker: `C11E_E4A4_CHALLENGE_AUDIO_MUX=PASS_ISOLATED_TEST_ONLY`; focused tests 42/42.

## Root cause of recovery V2 false BLOCKED

The worker creates `run_id = <UTC timestamp>-<8 hex>` and stores it without a prefix in both receipt and report. For filesystem readability, it names the run folder and ZIP `RUN_<run_id>`. ZIP members are rooted at `RUN_<run_id>/`. Recovery V2 incorrectly asserted `$Receipt.run_id -eq $RunName`; this compares different representations. Correct checks are:

- `RunName` starts with `RUN_`;
- `$ExpectedRunId = $RunName.Substring(4)`;
- receipt `run_id` equals `$ExpectedRunId`;
- report `run_id` equals `$ExpectedRunId`;
- ZIP basename equals `$RunName + '.zip'` and archive members begin `$RunName + '/'`.

This is a recovery validator bug. It does not invalidate the worker's exit code, PASS marker, output receipt hash or ZIP hash. Do not regenerate media.

## Packaging improvement

Recovery V3 is one self-contained PowerShell file with the add-only documentation payload embedded and pinned. It does not require extracting an additional overlay ZIP. This removes ambiguity caused by extracting a kit under an extra directory and then assuming the script is directly in Downloads. Invoke the actual `.ps1` path shown after saving it.

## Verification performed by V3

Worker log exit codes and 42-test transcript; exact PASS marker; reported run directory and ZIP restricted to the E4A4 test root; worker ZIP SHA and sidecar; archive path uniqueness; inner receipt and sidecar hashes; report hash/status/run identity; seed tuple; test-only flags; H.264 identity and A/B/C audio seed invariants; expected three MP4s and three raw WAVs; every `SHA256SUMS.txt` entry against archive bytes and full archive coverage; C11-C frozen manifest before/after; embedded documentation manifest and all add-only payload hashes.

V3 does not invoke D3 V5, D3.3, FFmpeg, FFprobe, Godot, the C11-C generator or a production dispatch. It applies only versioned documentation and writes a recovery receipt. Operator audio and A/V synchronization review remain separate.
