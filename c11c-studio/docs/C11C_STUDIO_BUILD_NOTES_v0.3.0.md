# C11-C Studio — Build Notes v0.3.0

## UX/UI pass

- Reworked the global application shell without changing backend/services/contracts.
- Added grouped navigation: Workflow, Creative, Output, System.
- Added a stronger top bar with backend/C11-B state, delivery metadata, environment status and project identity.
- Added explicit Ready/Running status treatment in the status bar.
- Reworked Dashboard into a daily-operation surface with quick actions, status cards and recent jobs.
- Reworked Review Lab and Production into clearer protected panels with consistent hierarchy and spacing.
- Improved tables, controls, focus states, tabs, scrollbars, tooltips and log typography.
- Preserved all existing signals, CommandBuilder calls, JobManager ownership and canonical execution paths.

## Explicit non-scope

No simulation, RNG, SimulationResult, winning_frame, close_calls, rendering mathematics, audio contracts, authoring contracts, seed algorithms, command construction or canonical PowerShell tool behavior were changed by this UX/UI pass.
