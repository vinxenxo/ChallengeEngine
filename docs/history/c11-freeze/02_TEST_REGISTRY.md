# C11 Freeze — Test Registry

The repository contains a large accumulated corpus. Tests are grouped by responsibility so that a full freeze can be reproduced without confusing logical validation with physical export.

## CORE

Deterministic RNG, mechanic isolation, DDI and canonical mechanic contracts. These suites protect simulation truth.

## PRESENTATION / C6

Presentation components, profiles, visual runtime, renderers, ContentEnvelope and binding contracts. Visual playback tests may instantiate `VisualContentPlayer` directly; C11-B.1 therefore keeps that usage backward-compatible.

## AUDIO / C7

Audio generators, PCM hashes, timeline, manifest, mux and FFprobe contracts.

## AUTHORING / C9

Authoring adapters, canonical generation, productive generation and runtime projections. Productive tests now use the authoritative current adapter metadata rather than historical placeholder expectations.

## C10 / C11

C10 authoring/runtime/physical smoke infrastructure and the C11 Unified Social Frame, Presentation Framing, Social UI Integration and repository-freeze contracts.

## PHYSICAL

`C6F06VisualLoopPhysicalExportTest.gd` and `C6F06VisualDrillPhysicalExportTest.gd` are artifact consumers. They do not create their input artifacts. `tools/c11freeze/run_physical_export_suite.ps1` first runs the physical Movie Maker smoke generation and then runs these assertions.

## STRESS

`tools/c11freeze/run_seed_stress.py` uses the fixed `qa/seed_corpus/stress_v1.json` corpus. Runtime tests never invent random seeds; the corpus itself is deterministic and hashable.

## Runner semantics

`python tests/run_all.py` is the logical corpus runner and skips physical-export consumers unless `--include-physical` is explicitly supplied. `tools/c11freeze/run_all.ps1` is the full freeze runner and includes physical generation/validation.

A suite is PASS only when its process exits successfully, its expected PASS marker appears, and no fatal parse/runtime marker is observed.
