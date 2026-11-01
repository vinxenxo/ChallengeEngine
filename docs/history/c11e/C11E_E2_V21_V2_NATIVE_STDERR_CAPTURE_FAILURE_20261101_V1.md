# C11-E V21 V2 â€” PowerShell 5.1 native stderr capture failure

**Date:** 2026-11-01
**Status:** V21 V2 aborted; runner rollback attempted; do not interpret this as a Python test failure.

V21 V2 redirected the Python 3.13 unittest process using PowerShell native-command `1>` and `2>` while `$ErrorActionPreference = Stop`. Python's unittest runner writes test progress and the final summary to stderr on successful execution. Windows PowerShell 5.1 surfaced that native stderr as a terminating `RemoteException`, so the applicator stopped after displaying the first test line and entered its rollback path.

The Python suite itself had already passed 9/9 in the active checkout under the separate V19/V20 repairs. This V21 V2 failure is a process-capture defect in the overlay script; it does not invalidate the earlier 9/9 receipt and does not establish that test 01 failed.

V21 V3 uses `System.Diagnostics.ProcessStartInfo` with `UseShellExecute=false`, both streams redirected and consumed asynchronously using `ReadToEndAsync()`. It writes stdout/stderr to distinct stage logs, checks the actual process exit code and validates `Ran 9 tests` plus `OK` in the combined captured text. FFmpeg, FFprobe and Godot are also invoked using the same helper to avoid native stderr handling ambiguity.

V21 V3 performs FFmpeg media QA and both pre-render contracts before modifying the runner. It then applies the deterministic three-literal patch, verifies runner SHA `158325324626085ebf319f68906ca8778f9a08eb39c6e8441da146c12ee4f953`, writes the V21 documents and receipt, and leaves all rendering to fresh R4.

No renderer or production media is invoked by either V21 applicator. C11-C baseline, generator mechanics and Git refs remain untouched.