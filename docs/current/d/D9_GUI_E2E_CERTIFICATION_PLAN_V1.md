# C11-D D9 — GUI E2E Certification Plan V1

## Acceptance principle

A GUI feature is complete only when the complete job lifecycle can be executed and observed from the GUI using the same canonical backend as CLI.

## Required lifecycle

```text
CONFIG
  ↓
PRODUCER REQUEST
  ↓
PERSONALIZATION
  ↓
CANONICAL PLAN
  ↓
PRODUCTION / REVIEW
  ↓
MEDIA QA
  ↓
CATALOG + PROVENANCE
  ↓
REPRODUCTION
  ↓
MAINTENANCE / ARCHIVE
```

## GUI/CLI equivalence

For each supported operation:

1. build the request in GUI;
2. build the equivalent request in CLI;
3. compare normalized request identity;
4. compare Production Plan identity;
5. execute only through canonical backend commands;
6. compare outputs and provenance.

## Certification corpus

### Challenge

At least one real Challenge with custom editorial values, audio ON and fixed gameplay/music seeds.

### Visual Loop

At least one real Visual Loop from each of the five current families once the D renderer bridge is available.

### Visual Drill

At least one representative case from each supported drill family/type once the D renderer bridge is available.

### Longform

At least one supported Longform production case once the D renderer bridge is available.

## Deterministic tests

- same request + same seeds + same editorial payload → same plan identity and deterministic product identity;
- same seeds + different editorial payload → different editorial/personalization identity;
- same request + changed music seed → changed audio identity without gameplay change;
- repeated GUI run → same backend inputs and reproducible output.

## Negative tests

- missing required seed;
- invalid profile;
- invalid editorial field;
- invalid family/subfamily;
- release execution without authority;
- protected-root write;
- destructive maintenance action outside allowlist;
- overwrite of a protected or immutable evidence root.

## Operator observability

The GUI must surface:

- current effective request;
- plan hash;
- seed identity;
- personalization identity;
- job status;
- output path;
- media QA result;
- catalog identity;
- reproduction command/reference;
- maintenance/quarantine outcome;
- logs/error evidence.

## Final gate

D9 cannot close while the GUI merely constructs a plan. It must prove the real operational path for the D content model and its editorial configuration, with physical media evidence where the current D renderer baseline supports it.
