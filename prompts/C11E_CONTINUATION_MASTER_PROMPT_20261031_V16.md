# C11-E continuation master prompt (V16)

Act as the engineering lead for `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Do not claim direct access to the operator's Windows checkout. Use supplied snapshots/evidence as read-only context, and require live Windows evidence for active-checkout claims. The operator commits locally at each iteration; this is expected. Every installer must pin the exact checkout identity for its iteration; runtime runners may accept descendants only after verifying E0/E1 ancestry and every exact source pin.

## Mission — complete product, not a single test

Deliver production-ready final audiovisual MP4s for all three families: Challenge, Visual Loop and Visual Drill. Preserve C11-C generators, mechanics, timing, frame streams and deterministic domains. Add the C/D presentation layer, enabled D9.8 editorial values in the proper family-specific binder/slot, D3 Music V5 via independent `request.music_seed`, FFmpeg mux and FFprobe validation. GUI and CLI must use one shared C11-E production service. CHALLENGE_001 A/B is only the first technical control. C11-C 2.19.12 remains immutable production baseline until E8 independent acceptance, freeze and explicit promotion.

## Read authority in this order

1. `AGENTS.md` and `.continue/rules/CONTINUE.md`.
2. `docs/current/e/README.md`.
3. `docs/current/e/C11E_CURRENT_AUTHORITY_20261031_V16.md`.
4. `docs/current/e/C11E_GATES_ACCEPTANCE_MATRIX_20261031_V16.md`.
5. `docs/current/e/C11E_E2_V8_JSON_FLOAT_SEED_REMEDIATION_20261031_V1.md`.
6. `docs/current/e/C11E_PRODUCT_SCOPE_PRESENTATION_EDITORIAL_MUSIC_20261030_V1.md`.
7. `docs/current/e/C11E_EXECUTION_HYGIENE_AND_ASSISTANT_ERROR_LOG_20261031_V12.md`.
8. `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261031_V6.md`.
9. Current sources, E2 receipts and failure evidence as relevant.

## Verified latest handover evidence

The supplied snapshot `C11E_WORKING_CONTEXT_20261031_191534.zip` SHA-256 `250c154ddb74813a7478d9aeb03ddaac7ccd15595c82bbfad607552f048408b5` / 9,618,925 bytes matches its SHA sidecar/report. It captured branch `main`, HEAD `b92434d6a8b50cef7e49ba6b75a4813777927fe7`, parent `a3c7c5d284a96ce115ca52208b4039002502753b`, commit tree `91aa803c2d675ec9fc7afff120b2bc7d3de479ef`. Snapshot ZIP excludes `artifacts/` and media by design; the failure ZIP must be uploaded separately.

E2 V7 physical failure: `C11E_E2_CH001_AB_FAILURE_EVIDENCE_20261031_191440_13012eef.zip`, 29,568 bytes / 47 entries / SHA-256 `27fa769c35165e8171120bc0fce16fc3739505198157a874360c2de432c6bbe7`. Python pair tests 9/9 pass, but Godot A exits 40 with `Editorial sidecar contract validation failed` at GDScript line 62, after one renderer invocation and one-frame AVI fragment. Root cause is confirmed: Godot `JSON.parse_string()` parses JSON number values into `TYPE_FLOAT`; V7 E2 validator incorrectly required `TYPE_INT` for gameplay/music seeds. No B render, final MP4s or success receipt; E2 failed and E3 remains blocked. Ignore the spurious console `Write-Host PASS` after the nonzero runner exit; it has no evidentiary value.

## Immediate next gate

V8 remediation package: `C11E_E2_V8_JSON_FLOAT_SEED_REMEDIATION_20261031_V1.zip`. It is prepared against the snapshot's exact `main`/`b92434d`/`a3c7c5d` checkout. Do not install blindly: verify ZIP SHA from supplied package sidecar, installer preconditions, V7 APPLIED receipt and V7 failure ZIP first. If the exact install identity has changed, stop and rebuild the installer for the actual current checkout; never reuse stale pins.

The GDScript fix accepts only finite positive integral JSON numeric values (TYPE_INT or TYPE_FLOAT) within 1..2147483646. A Godot-native headless test JSON-round-trips a complete valid E2 sidecar, confirms the parser returns floats, invokes the actual sidecar validator and rejects invalid seeds in both domains. The V8 runner must emit `C11E_E2_GODOT_JSON_NUMERIC_CONTRACT=PASS` before any Python pair preparation or physical render; if absent, no renderer is allowed. After install receipt APPLIED and postimage verification, the operator may commit locally. Run one fresh E2 V8 two-render A/B with `C11E-E2-CH001-AB-20261031-V8`; no audio. Do not execute success-only receipt commands after a nonzero exit. Do not re-run V7.

E2 acceptance still requires two nonuniform source AVIs, two final MP4s, FFprobe, full gameplay/body pixel identity, distinct title slot each frame, header outside-slot identity, hashes/provenance and separate human review. Until accepted, do not start E3.

## Next gates after E2

E3 Challenge D3 Music V5 + independent music seed + FFmpeg mux + FFprobe; E4A Challenge, E4B Visual Loop and E4C Visual Drill each with real family-specific adapter/binder/editorial/presentation/music; E5 determinism/seed isolation/GUI-CLI parity; E6 Smoke18 (six per family); E7 Matrix101 (54 Challenge +27 Loop +20 Drill; currently 99 runnable while CH_008/009 remain held for 11s/12s conflict); E8 independent acceptance/freeze/promotion.

Common D9.8 enabled fields: title, subtitle, call_to_action, language. Challenge-only: player_name, challenge_label. Hook/preparation/final/header/footer fields and show flags remain disabled. Do not map title to hook or CTA. Loop/Drill need explicit tested E adapters. Do not alter C generator/mechanics, C11-C manifest, D locks, Git refs, or branch. No resets, clean, branch switching, rebase, amend or push. Do not fabricate hashes, receipts, media, test outcomes or human review.
