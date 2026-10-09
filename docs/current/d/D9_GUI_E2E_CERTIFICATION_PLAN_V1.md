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


## D9.12 Test 0.2.0 operator route matrix

The existing `c11c-test` GUI exposes a preflight route for this matrix. The preflight validates this plan only; it **does not start production, renderer work, media creation, release staging, or maintenance mutations**. Actual GUI production certification remains an operator-controlled future D9.14 gate and requires a separately authorized D renderer baseline.

| Case ID | Required evidence | Current gate |
|---|---|---|
| `D9-GUI-001` | Challenge request with custom editorial payload, audio enabled, fixed independent gameplay/music seeds, canonical plan identity | Plan-only checks available; physical media requires future D authorization |
| `D9-GUI-002` | At least one Visual Loop from each of the five supported families | Future D renderer baseline required |
| `D9-GUI-003` | Representative Visual Drill coverage across all four types and supported tiers | Future D renderer baseline required |
| `D9-GUI-004` | Longform production only if a future canonical D request contract enables it | Explicitly disabled today |
| `D9-GUI-005` | Repeated identical request and seeds preserve request/plan identity | Canonical plan parity available now |
| `D9-GUI-006` | Changing music seed changes audio identity without changing gameplay seed/identity | Contract negative/determinism test now; physical audio compare requires future authorization |
| `D9-GUI-007` | Changing editorial payload changes editorial identity while both seed domains remain unchanged | Canonical plan hash check available now |
| `D9-GUI-008` | Missing seed, invalid profile/editorial field/family is blocked | Negative controls available now |
| `D9-GUI-009` | Protected-root mutation is blocked | Config/Maintenance negative tests available now |
| `D9-GUI-010` | Release mutation without authority is blocked | Governance gate; `release_authority=NONE` |
| `D9-GUI-011` | Cleanup/quarantine outside allowlists is blocked and reversible operations preserve evidence | Maintenance 0.2.0 acceptance available now |

The GUI certification preflight must report all 11 case IDs, `operator_execution=REQUIRED`, `renderer_activation=false`, `media_created=false`, `D4.8=BLOCKED`, and `release_authority=NONE`. A preflight PASS is not real-media acceptance and cannot close D9.


## D9.14 real-media GUI certification gate (2026-10-09)

The existing Producer GUI and Test GUI now expose a fail-closed certification gate. This is not media certification: it confirms the current preconditions and enumerates the required ten cases, while returning `BLOCKED` because the future D renderer baseline and explicit D4.8 authorization do not exist. The gate test must not create media, invoke a renderer, write output artifact paths or grant release authority. Run `python .\tools\c11d\d9\test_gui_real_media_certification.py`. Do not use the frozen C11-C renderer to materialize D9 universal editorial bindings.
