# C11-E E6 Smoke18 Read-only Audit Recovery — V2 (2026-11-17)

## Incident closure: V2 PowerShell 5.1 argument-marshalling defect

The V2 installer completed successfully in the operator checkout:

- `PASS_ADD_ONLY_IDEMPOTENT_INSTALL`
- 29/29 final postimages verified; 4 files added and 25 identical files skipped
- frozen C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`
- D4.8 R1V policy SHA-256 `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07`

The V2 runner stopped before focused tests and before the V2 audit module. The cause was the Python version probe:

`print("{}.{}.{}".format(...))`

Windows PowerShell 5.1 removed the embedded double quotes while marshalling the native `python.exe -c` argument. Python therefore received invalid syntax (`print({}.{}.{}.format(...))`). This was not an evidence-pin failure and did not execute the V2 audit.

The earlier V1 read-only audit remains a valid, separately recorded PASS: 50/50 source pins, 11/11 baseline-document pins, R1V human closeout 10/10, Loop22 human closeout 44/44 and six Drill evidence receipts. V1 receipt SHA-256: `e108334945b11ab86321e8fb4cf19f38d159a13eae1ebbf32fc88eca208d797c`.

## V3 runner correction

`RUN_C11E_E6_SMOKE18_READONLY_AUDIT_V3.ps1` is a new ADD_ONLY entrypoint. It leaves V1 and V2 runners and Python modules unchanged. It reuses the already-installed and pinned V2 test/audit modules.

The version probe now uses quote-free Python source:

`import sys; print(chr(46).join(map(str, sys.version_info[:3])))`

This avoids embedded quote characters in the PowerShell 5.1 native argument string. The V3 runner verifies the V2 Python module pins, the PowerShell AST, Python 3.13, runs 15 focused tests and then invokes the V2 read-only audit module once.

## Operator execution result (2026-11-17)

- V2 installer: PASS, 29/29 postimages; 4 added, 25 identical skipped.
- V2 runner: failed at Python version probe before tests or audit; no V2 audit receipt was created.
- No renderer, Godot, FFmpeg, FFprobe, music/audio generation, mux, dispatch or BatchId reservation occurred.
- Preserve the V1 audit receipt and V2 install receipt/journal. Do not rerun or replace V1/V2 files.

## V3 scope and boundaries

The V3 installer adds only the new V3 PowerShell runner and versioned continuity records. The runner reads the existing V2 Python tests/audit module. It does not run any media tool and does not create a BatchId. A successful V2-module audit still reports Challenge unresolved and Smoke18 execution held.

C11-C 2.19.12 remains frozen; D4.8 R1V V2 remains unchanged; E1 PREPARE_ONLY; family adapter NOT_CONNECTED_E1; renderer OFF; production dispatch/media false; release authority NONE. Git checks remain skipped and commits operator-managed.
