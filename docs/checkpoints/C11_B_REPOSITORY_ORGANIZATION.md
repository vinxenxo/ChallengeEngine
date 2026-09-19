# C11-B Repository Organization Checkpoint

**Status:** PREPARED — PENDING USER VALIDATION

## Baseline

Input baseline: `ChallengeEngineV01.2_C11_B_FREEZE_LATEST.zip`.

The semantic C11-B freeze was already committed by the project owner before this maintenance operation. Its prior freeze seal was:

```text
bfb570d066ed9d025bb0ba23e125b828ecb5c28e20d4e0e62b5d21273ee530ab
```

That hash remains historical evidence of the pre-organization semantic state. The organized repository will receive a different tree hash only after validation.

## Scope

- move compatibility fixtures into `tests/fixtures/`;
- consolidate generated output into `artifacts/`;
- separate historical evidence from active paths;
- consolidate live documentation into `docs/`;
- harden `.gitignore`;
- update test/tool paths only where required by moves;
- remove disposable caches and reproducible binary render output from the repository package.

## Preserved

The cleanup preserves:

- all executable `*Test.gd` suites;
- all `KNOWN_SUITES` registrations;
- C7 compatibility fixtures;
- C11 seed corpora and qualification evidence;
- retrocompatibility references;
- deterministic stress corpus;
- historical checkpoint documentation;
- release/freeze manifests useful for audit.

Generated AVI/MP4/GIF/PNG/JPG/WAV/PCM media was removed from the package where reproducible from current tooling. Textual manifests, reports and frame digests remain where they provide durable evidence.

## Active layout

See `docs/04_REPOSITORY_STRUCTURE.md` for the authoritative tree.

## Acceptance

The checkpoint becomes CLOSED only after the organized repository passes the complete `docs/operations/TEST_RUNBOOK.md` and the owner commits it as a separate maintenance commit.
