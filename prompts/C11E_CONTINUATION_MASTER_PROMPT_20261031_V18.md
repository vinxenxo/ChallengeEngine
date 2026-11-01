# C11-E continuation master prompt — V18

Work in `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. Continue from the live Windows checkout, not from assumptions. Full product target: finished MP4 generation for Challenge, Visual Loop and Visual Drill, existing C11-C mechanics retained, approved D presentation/editorial fields, D3 Music V5 with independent `request.music_seed`, FFmpeg mux, FFprobe validation and one shared CLI/GUI service. CHALLENGE_001 A/B is only the initial technical gate.

## Governing sources

Read `AGENTS.md`, `.continue/rules/CONTINUE.md`, `docs/current/e/README.md`, authority V18, gate matrix V18, V9 remediation V2 note, execution hygiene V14 and roadmap V8. Active checkout is authoritative. Use the uploaded snapshot `C11E_WORKING_CONTEXT_20261031_191534.zip` as filtered historic context only; use V7 physical failure ZIP separately. Do not regenerate the snapshot or repeat E0/E1.

## First reconciliation

Record live branch, HEAD, parent, tree, `git status --short --branch`; keep user commits. Never reset/clean/checkout/rebase/amend/push. Verify E0/E1 ancestry, E0 and E1 receipts, V7 V2 install receipt, V7 failure evidence ZIP (SHA-256 `27fa769c35165e8171120bc0fce16fc3739505198157a874360c2de432c6bbe7`), exactly one APPLIED V8 receipt, and C11-C frozen manifest (796,318 bytes / `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`). Reconcile each V9 V2 destination hash; do not infer applied state from the previous installer failure.

## V9 installer V1 incident and V2 correction

V9 V1 incorrectly required the V8 GDScript preimage `af142fc5...77911493` before considering already-applied state. Operator-reported actual was `4787b445...755dae5`, exactly V9 payload postimage. V1 stopped before writes. Do not rerun V1.

Use only `C11E_E2_V9_TEST_HARNESS_REMEDIATION_20261031_V2.zip` plus SHA sidecar. V2 has strict idempotent classification: for each replacement, expected V8 preimage means apply; exact V9 postimage means record `ALREADY_PRESENT`; unknown means abort. For each add-only path, absent means add, exact postimage means `ALREADY_PRESENT`, other existing content means abort. It validates all payloads and paths before writes and rechecks each target immediately before mutation. Check receipt schema `C11E-E2-V9-FIX-V2-RECEIPT-V1`, status `APPLIED`, all 16 destinations and backups/postimages. Renderer/media false. Then user commits locally.

## Runtime sequence

Run isolated Godot 4.7.1 Mono test `res://tools/c11e/e2/test_c11e_e2_godot_json_numeric_contract.gd`, passing a unique absolute `--result-json` path through Godot's `--` user-argument separator. Capture stdout/stderr and native exit code. Require exit 0 and structured JSON schema `C11E-E2-GODOT-JSON-NUMERIC-TEST-RESULT-V1`, status `PASS`, gameplay and music parsed JSON types both `float`, `full_sidecar_validation=true`, numeric_cases_passed=30 and expected=30. Missing/malformed result or failed condition stops; never synthesize result JSON.

Only after preflight PASS run V9 physical E2 runner with fresh RequestId `C11E-E2-CH001-AB-20261031-V9`, exactly two isolated CHALLENGE_001 A/B renders, no audio. Verify receipt/checksum, AVI/MP4 file hashes, dimensions, fps, frames, nonuniform source samples, gameplay body pixel identity, title slot pixel difference, header invariance, FFprobe stream count and provenance. Failure evidence must be retained. Automated PASS remains human review pending until independent visual inspection; no E3 before E2 acceptance.

## Complete roadmap

After E2: E3 Challenge Music V5, independent seed, FFmpeg and FFprobe; E4A full Challenge; E4B Loop binder/adapter/editorial/music; E4C Drill binder/adapter/editorial/music; E5 determinism + seed isolation + GUI/CLI parity; E6 Smoke18; E7 Matrix101 (54 Challenge +27 Loop +20 Drill, but CH008/009 held until 11-second/12-second timing conflict is authority-corrected); E8 independent acceptance/freeze/promotion. Common enabled editorial fields title/subtitle/call_to_action/language; Challenge-specific player_name/challenge_label. Reserved hook/preparation/final/header/footer remain disabled.

C11-C 2.19.12 remains immutable authoritative production baseline until E8. Release authority NONE. PowerShell 5.1 safe; no false PASS; no bypass of pins or gate locks.
