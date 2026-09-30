# MASTER HANDOVER — ChallengeEngineV01_STATELESS / C11-C 2.19.12

**State: FINAL C11-C freeze candidate.**

## Authority

The C11-C 2.19.12 source tree is the final consolidated candidate. Formal immutability begins only after the final acceptance report and freeze-package receipt are sealed.

## Read first

1. `AGENTS.md`
2. `.continue/rules/CONTINUE.md`
3. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_STATE.md`
4. `docs/current/c11c/C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md`
5. `docs/current/c11c/C11-C_2.19_COMPLETE_VIDEO_REVIEW_RUNBOOK.md`
6. `docs/current/c11c/C11-C_2.19_COMMAND_SHEET.md`
7. `docs/current/c11c/C11-C_2.19_DOCUMENTATION_INDEX.md`
8. `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md`

## Provenance

- Godot 4.7.1 stable Mono.
- Producer 0.9.7.
- 5 Visual Loop families / 27 grammars.
- 4 Visual Drill families.
- 5 Longforms.
- 52-video complete review.
- Historical C11-A.1 compatibility preserved over the canonical Challenge producer.

## Frozen boundaries

Do not change simulation truth, RNG ownership/algorithm, SimulationResult, winning-frame semantics, close-call semantics, WinningFrameDetector, RenderedFrameStream, C7, C9 or logical 540x960 geometry without an explicit D checkpoint.

## Suite rule

`c11c-suite` is both GUI and command-line operator shell. GUI actions must remain thin wrappers around the exact canonical commands used from console. No duplicate backend.

## Freeze procedure

Run final acceptance, restore the verified historical `build_factory.py`, then use Maintenance -> `GENERAR ZIP FROZEN C11-C 2.19.12`. The packager excludes artifacts, caches, editor/source-control clutter and retired studio tooling, and records SHA-256 provenance.

## Transition to D

After the frozen archive is sealed, D begins from that exact archive. Do not continue changing C11-C while starting D.
