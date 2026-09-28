# C11-C Studio — First Build Audit and Corrective Baseline

## Audit target

Original user-provided `bootstrap_studio.py` from Library, which generated a PySide6 GUI under `c11c-studio`.

## Result

The original build had a strong UI skeleton and several correct architectural instincts, but it did **not** yet satisfy the complete C11-C Studio master contract.

### Correct foundations found

- PySide6 desktop architecture.
- Project-root discovery.
- Environment/tool discovery.
- Direct subprocess command construction.
- QProcess-based asynchronous execution.
- Dashboard, Review, Production, Families, Seeds, Artifacts, Logs, Validation and Settings concepts.
- 5-family concept.
- 5×5 review/production concepts.
- protected production/artifact classification intent.

### Material gaps corrected in v0.2.1

1. Production 5×5 used the wrong family-bulk operation instead of the dedicated current `run_c11c_production_25.ps1` when available.
2. Manual seed mode was incomplete.
3. Footer/Force options were not consistently transported.
4. Grammar controls were presented without capability validation.
5. `JobManager` merged stderr into stdout and finalized process state too early on `errorOccurred`.
6. Cancellation could become FAILED instead of CANCELLED.
7. Job persistence was incomplete.
8. Canonical validation scripts were not directly executable from Validation Center.
9. Cleanup UI only previewed scratch instead of using the canonical manual cleaner.
10. Settings missed player/behavior/tool-path options from the master spec.
11. Production Catalog lacked manifest/log/social inspection.
12. Art Direction, Products, Jobs, Games/Drills and Reproduction surfaces were missing or incomplete.
13. Family/grammar/parameter discovery was too hard-coded.
14. Backend version was hard-coded rather than discovered with fallback.
15. Effective parameters were not consistently exposed with provenance/state.
16. The GUI had no snapshot service.
17. No centralized capability-aware command adapter existed.
18. Versioned-tool proliferation was not normalized at the GUI level.

## v0.2.1 policy

- Canonical tools are discovered at runtime.
- GUI commands use structured argument arrays.
- No GUI renderer/math reimplementation.
- Review never cleans Production.
- Production is protected and overwrite is explicit.
- Dynamic family/parameter discovery is used where backend metadata allows it.
- Unknown backend parameters are retained as inspectable information rather than dropped.
- Logical 540×960 and physical 720×1280 are shown separately.
- 18s is a current baseline, not a permanent law.

## Remaining intentionally gated work

The current v2.1.4 backend does not expose every artistic parameter as a command-line override. Therefore the GUI shows non-editable/effective/derived parameters rather than pretending unsupported CLI controls are editable.

The Art Direction Lab is the future home for experimental overlays once the backend explicitly supports them.

## Validation boundary

The build can be statically parsed and internally self-tested in this environment. Physical Windows/PySide6/Godot execution remains the user-side acceptance test.
