# C11-E E4C V1.7 installer destination classification incident — V1

**Date:** 2026-11-12  
**Disposition:** FAIL_CLOSED_PRE_TRANSACTION / NO_CHECKOUT_MUTATION  
**Superseding installer:** V1.8 only

## Observed operator diagnostic

`PACKAGE_ZIP_SHA256=PASS/65e95d286d6aca15b2dd1bf05f27f64b3519182a3fbe2c13206e30d3421cc31e`; inventory 24/24; 21/21 source pins; frozen C11-C manifest PASS; PowerShell AST 2/2. Installer then failed with `REPLACEMENT_DESTINATION_MISSING: tests/test_c11e_e4c_drill_visual_composition_consumer.py`.

## Root cause

The V1.7 manifest declared two replacement operations. The existing D-owned consumer path is a genuine replacement. The test module destination under repository `tests/` is newly introduced by V1.7. V1.7 carried preimage SHA `aedeb5754d94fdbaad134a653f57ca07466c845dcef081c8774668245455a7a0`, but independent archive inspection proves this is the SHA of the earlier test file at `tools/c11d/d9/test_c11e_e4c_drill_visual_composition_consumer.py` inside the historical V9 package. The file content hash was valid for that old path; its use as a preimage for the new `tests/` destination was invalid. Therefore the new test destination must be `ADD_ONLY` and must not retain that preimage guard.

## Transaction disposition

The V1.7 script raises this failure at its destination-preflight loop, before `EvidenceRoot`, `TRANSACTION_JOURNAL.json`, backups or mutation staging are initialized. The catch path has an empty in-memory journal and therefore performs no rollback operations. `FAIL_CLOSED_ROLLBACK_COMPLETE` is the script's generic zero-entry rollback status. No repository destination write occurred; no consumer postimage was installed by this attempt.

## Consolidated V1.8 correction

- One replacement: `tools/c11d/d9/c11e_e4c_drill_visual_composition_consumer.py`, guarded by its exact preimage/postimage.
- Twenty-one add-only destinations, including `tests/test_c11e_e4c_drill_visual_composition_consumer.py`. If absent, add; if exact postimage, skip; if different bytes or a non-file collision, abort before transaction.
- Installer operation matrix is asserted from the manifest, destination paths are unique, and staged consumer/test/requalifier inputs are resolved from manifest entries rather than assuming a payload directory.
- All 21 source pins, frozen manifest, PowerShell AST, Python/PySide6/Qt runtime, py_compile, 18 focused tests, File.Replace round-trip, immediate rechecks, journal-before-write, backups, postimages and rollback guards remain mandatory.
- No changes to V2 consumer logic, tests' assertions, requalifier, runner, C11-C, E1 service, GUI/CLI facade, shared executor or dependencies.

V1.8 is a rebuilt, single consolidated correction; no repeated V1.7 execution is permitted. Its Windows install and existing-media requalification remain pending operator-run evidence.
