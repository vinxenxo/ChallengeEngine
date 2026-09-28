# C11-C Suite 0.1.3 — Operational Rules

## Test/script parity

Every new automated test or operational script must have:

1. a canonical implementation in the repository;
2. a direct console launcher;
3. a launcher in the relevant `c11c-suite` GUI;
4. documentation describing its command, inputs and evidence.

`c11c-test` discovers the Godot logical corpus through `tests/run_all.py` and also exposes Python/PowerShell operational checks.

## Current additional Producer checks

- `PRODUCER SELF-TEST`
- `PRODUCER GUI CONTRACT`
- `RETRO REFERENCE CONTRACT`
- `SEED STRESS`

## Producer review catalogue

The Producer now exposes `REVIEW_CHALLENGES`: historical C11-A.1 qualification/review, 9 Challenges × 6 seed cases.

## Frozen status

The Suite remains a proof of concept during C freeze. Interface evolution is permitted in D, but the C manufacturing backend contracts are not changed from the Suite.
