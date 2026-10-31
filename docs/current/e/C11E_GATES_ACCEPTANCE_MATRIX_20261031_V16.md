# C11-E — gates and acceptance matrix (V16)

| Gate | Deliverable | Acceptance evidence | State at 2026-10-31 cut-off |
|---|---|---|---|
| E0 | Checkout, C manifest, receipts and instructions | E0 receipt and source pins | Applied; E0 re-entry commit `b92434d` is child of E1 `a3c7c5d` |
| E1 | Shared GUI/CLI production service | Windows automated tests + separate GUI observation | Automated 2/2 PASS; manual GUI observation pending |
| E2 | CH001 editorial title reaches only its visual slot; gameplay invariant | Two real nonblank A/B AVIs and MP4s, FFprobe, full pixel comparisons, hashes and human review | **V7 FAILED**: Python 9/9 PASS, but Godot A exited 40 because JSON-decoded seeds are `TYPE_FLOAT` while validator required `TYPE_INT`; one-frame AVI fragment only; no success receipt. V8 correction package prepared, not yet installed or run. |
| E3 | D3 Music V5 and final audio mux | Independent `music_seed`, WAV, FFmpeg mux, FFprobe A/V | Not started; blocked by E2 |
| E4A | Challenge presentation + enabled editorial + music | Real Challenge generator/binder, final A/V MP4 and reviewed receipt | Not started |
| E4B | Visual Loop presentation + enabled editorial + music | Real Loop grammar/generator/binder, final A/V MP4 and reviewed receipt | Not started |
| E4C | Visual Drill presentation + enabled editorial + music | Real Drill type/tier/generator/binder, final A/V MP4 and reviewed receipt | Not started |
| E5 | Determinism, seed isolation, regression and GUI/CLI parity | Repeatable source/frame/music hashes and regression evidence | Not started |
| E6 | Smoke18 | 18 physical reviewed A/V outputs (six per family) | Not started |
| E7 | Matrix101 | 54 Challenges + 27 Loop grammars + 20 Drill variants | Not started; currently 99 runnable while CH_008/009 are held |
| E8 | Independent acceptance, freeze and promotion decision | Independent reviewer artifact and hash-bound immutable evidence | Not started |

## E2 V7 forensic diagnosis

Failure evidence: `C11E_E2_CH001_AB_FAILURE_EVIDENCE_20261031_191440_13012eef.zip`, 29,568 bytes / 47 entries / SHA-256 `27fa769c35165e8171120bc0fce16fc3739505198157a874360c2de432c6bbe7`. Python pair tests 9/9 pass; pair preparation and toolchain version probes pass. Godot 4.7.1 Mono enters the A renderer and then logs `Editorial sidecar contract validation failed` at GDScript line 62, exit code 40. The failure diagnostic says one renderer invocation, AVI path created, media not accepted and release authority NONE. There is no valid final output or success receipt.

Godot JSON parsing converts numeric JSON tokens to `TYPE_FLOAT`. The old validator required `TYPE_INT` for both seed values; this made the validator reject valid `193847` / `840001` values after JSON parsing. The source-code fix is to accept integer or float Variant types only when finite, positive, integral and <=2,147,483,646. A pinned Godot-native headless regression must PASS before the physical A/B render.

## V8 retry conditions

- Install the V8 add-only/remediation overlay only after its exact checkout identity, C11-C manifest, V7 V2 APPLIED receipt, V7 failure ZIP, source preimages and every package payload hash validate.
- V8's Godot JSON numeric test must print `C11E_E2_GODOT_JSON_NUMERIC_CONTRACT=PASS`; if that test fails, the renderer must not be invoked.
- Then run exactly two isolated `CHALLENGE_001` A/B renders with no audio and fresh RequestId `C11E-E2-CH001-AB-20261031-V8`. No E3 audio or family-wide claim is part of E2.
- A zero process exit is necessary but insufficient. Require two nonuniform 540-frame source AVIs (540x960/60fps), two final 720x1280/30fps MP4s without audio, FFprobe, 540/540 body pixel identity, title slot different on every frame, header outside the slot identical, provenance and independent human review.
- Do not reuse the V7 RequestId, partial output, failure ZIP, or stale variables. If V8 fails, inspect the new diagnostic archive and retain the failure without a manual PASS.

## Per-iteration commit identity

The operator commits locally every iteration. The V8 installer is pinned to the latest uploaded snapshot checkout `main` / `b92434d6a8b50cef7e49ba6b75a4813777927fe7`, parent `a3c7c5d284a96ce115ca52208b4039002502753b`. It also requires the expected current V7 source postimages and V7 receipts/evidence. After installation, the operator may commit. V8 runtime runner permits verified descendants only when E0/E1 ancestry and every source hash match, recording actual runtime HEAD/parent. Do not silently retarget a stale installer.

C11-C remains immutable and D governance/release locks remain unchanged. CH_008/009 remain held pending explicit resolution of 11-second declared duration vs 12-second summed phase durations. E2 or E3 success does not grant release authority or promote E over C11-C.
