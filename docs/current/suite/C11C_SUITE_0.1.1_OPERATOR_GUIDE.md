# C11-C Suite 0.1.1 — Operator Guide

## Purpose

`c11c-suite` is the operator layer of `ChallengeEngineV01_STATELESS`. It does not replace the canonical test runners, production wrappers, definitions, simulation, mechanics, RNG, presentation truth or renderer mathematics.

## Launch

From the repository root:

```powershell
cd C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS
.\c11c-suite\run.bat
```

Individual suite members can also be launched directly:

```powershell
.\c11c-suite\c11c-test\run.bat
.\c11c-suite\c11c-catalog\run.bat
.\c11c-suite\c11c-maintenance\run.bat
.\c11c-suite\c11c-config\run.bat
.\c11c-suite\c11c-producer\run.bat
```

The historical misspelling remains available as a compatibility launcher:

```powershell
.\c11c-suite\c11c-maintenace\run.bat
```


## Preflight / static checks

```powershell
python .\c11c-suite\self_test.py
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\preflight.py
```

## Canonical logical test registry

Run every registered logical suite:

```powershell
python .\tests\run_all.py
```

The Suite reads `KNOWN_SUITES` from that file; it does not maintain a second list of engine tests.

Run one registered Godot suite directly:

```powershell
godot --headless --path . --script .\tests\PATH\TO\SomeTest.gd
```

## Full freeze / regression gate

The canonical project gate is:

```powershell
.\tools\c11freeze\run_all.ps1
```

Individual gates exposed by the Suite include:

```powershell
.\tools\c11freeze\run_core_suite.ps1
.\tools\c11freeze\run_c11_suite.ps1
.\tools\c11freeze\run_retrocompatibility.ps1
.\tools\c11freeze\run_physical_export_suite.ps1
.\tools\maintenance\verify_repository_layout.ps1
.\tools\prototypes\c11c_bulk\validate_c11c_delivery_configuration.ps1
```

## Historical QA

Historical Challenge qualification (9 × 6 seeds):

```powershell
.\tools\qa\c11\run_c11a1_challenge_bulk_qa.ps1
```

Historical visual QA:

```powershell
.\tools\qa\c11\run_c11a_visual_bulk_qa.ps1
```

## C11-C art-direction review

All review contents:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 -Workers 7 -All
```

Longforms only:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 -Workers 7 -Longforms
```

The longform path is currently protected by a focused regression for the `REVIEW_720` same-path copy condition in `run_c11c_production.ps1`.

## Deterministic stress

```powershell
python .\tools\c11freeze\run_seed_stress.py --repeat 2 --retries 3
```

## Producer

The live Producer is now:

```text
c11c-suite/c11c-producer/
```

It remains an orchestration UI. Challenge production still goes through the canonical Challenge wrapper; Loop and Drill production still goes through their canonical C11-C wrappers.

Example direct Challenge production:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_challenge_production.ps1 -ChallengeId CHALLENGE_005 -Seed 1247290191 -DeliveryProfile MASTER_1080 -OutputRoot .\artifacts\production\audiovisual\challenges\CHALLENGE_005\seed_1247290191
```

Example direct Longform batch:

```powershell
.\tools\prototypes\c11c_bulk\run_c11c_art_direction_batch_v4.ps1 -Workers 7 -Longforms
```

## Catalog

`c11c-catalog` scans `artifacts/` recursively. It can show:

- image previews;
- video/GIF thumbnails;
- FFprobe stream/container metadata when FFprobe is installed;
- JSON and textual evidence;
- file size, timestamp and repository-relative path.

It does not mutate artifacts.

## Maintenance

The maintenance GUI exposes safe operational actions. Automatic cleanup targets only:

```text
artifacts/scratch
artifacts/tests/logs/verbose
```

Repository layout and delivery checks call the canonical project scripts. Project ZIP creation excludes transient developer folders such as `.git`, `.godot`, Python caches and, by default, `artifacts/`.

## Config

`c11c-config` exposes declared configuration surfaces including:

```text
challenges/
definitions/
profiles/
schemas/
docs/contracts/
docs/checkpoints/
tools/prototypes/c11c_common/
project.godot
```

JSON is validated before save. Editable configuration receives a `.bak` backup before being written. Code/runtime files remain read-only in the GUI.

## Boundary rule

The Suite must never become an alternate implementation of project truth. A GUI may inspect, invoke, validate, edit declared configuration or package evidence; it must not reimplement mechanics, RNG, simulation semantics, `SimulationResult`, `winning_frame`, `RenderedFrameStream`, audiovisual ownership or renderer mathematics.
