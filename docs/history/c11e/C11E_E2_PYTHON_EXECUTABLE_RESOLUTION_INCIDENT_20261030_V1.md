# C11-E E2 V4 — Python executable resolution and missing failure ZIP (V1)

**Observed:** 2026-10-30, physical runner attempted `Process.Start()` for `python --version` and failed with `The system cannot find the file specified`.

**Confirmed root cause:** `Get-Command python -CommandType Application` returned two results: Python 3.13.14 at `C:\Users\vinxe\AppData\Local\Programs\Python\Python313\python.exe` and the Microsoft Store alias at `C:\Users\vinxe\AppData\Local\Microsoft\WindowsApps\python.exe`. The runner stored the collection in `$PythonCommand` and then cast `$PythonCommand.Source` to string; this concatenated both paths into one invalid `FileName`.

**Independent probes:** Godot `4.7.1.stable.mono.official.a13da4feb`, FFmpeg 9.0 and FFprobe 9.0 each started with exit code 0. Python failed only in the runner's ambiguous path construction; the real Python executable exists.

**Evidence behavior defect:** stage directory existed but was empty; `FailureZip` path reported by V4 did not exist. The failure occurred before any logs were written. This is a runner evidence defect, not absence of the operator's diagnostic transcript.

**Impact:** no Python test, pair builder, Godot render, AVI, MP4, audio or mux was executed by E2 V4. E2 remains not accepted. V4 overlay installation itself remains PASS 21/21.

**Corrective action:** resolve a single non-WindowsApps executable path (or explicit `-PythonExecutable`), write a process-start diagnostic before every `Process.Start()`, record the full exception, and only report a failure evidence ZIP after verifying file existence, nonzero bytes and archive entries. Retry with a new RequestId.
