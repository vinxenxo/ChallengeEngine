# C11-C Studio — Build Notes v0.2.4

## Fixes

- Fixed `MainWindow` ownership collision between the `JobManager` service and the `JobsPage` widget.
- `JobManager` is retained as `self.job_manager`; `self.jobs` remains the Jobs UI page.
- `LogsPage` now receives the actual `JobManager`, so log streaming and job lifecycle signals are connected to the service.
- Cancellation and running-state checks use the `JobManager` service directly.
- No C11-B/C backend simulation, RNG, rendering or canonical toolchain code was changed.
