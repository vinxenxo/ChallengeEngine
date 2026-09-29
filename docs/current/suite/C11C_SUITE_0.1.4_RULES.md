# C11-C Suite 0.1.4 — Operational Rules

## Ownership

`c11c-suite/` is the canonical active Suite surface. `c11c-studio/` is retired and must not be updated or required for operation.

## Launcher parity

Every operational test/QA capability must have a canonical implementation, direct console route, Suite/GUI route when appropriate, and current documentation.

## Worker concurrency

Art Direction `Workers=7` is genuine concurrency. Each worker owns a private temporary Godot project root, private `.godot` state and worker-local class-cache bootstrap. A global mutex or serial fallback is prohibited.

## Contract-test lifecycle

Command-line `SceneTree`/`MainLoop` tests must enter through the appropriate `_initialize()` lifecycle and explicitly terminate with `quit()` or an intentional MainLoop termination.

## Logical runner transient policy

`tests/run_all.py` may retry only exact Windows `0xC06D007F` process exits. Explicit FAIL markers, fatal patterns, timeouts, missing PASS markers after exit 0, and other non-zero statuses remain failures.

## GUI / backend boundary

The Suite and Producer are orchestration surfaces. They do not implement mechanics, RNG, timing truth or gameplay calculations.
