# C11-E gate acceptance matrix — V18

| Gate | Required evidence | Current state | Authorization |
|---|---|---|---|
| E0 | restart authority and receipt | APPLIED | retained |
| E1 | shared service implementation + automated test 2/2 | automated PASS; GUI visual observation pending | no new E1 rerun needed unless source changes |
| E2 V7 | physical CH001 A/B | FAILED, Godot A exit 40; failure ZIP retained | not accepted |
| E2 V8 | JSON float seed preflight | did not emit required markers / no structured PASS | not accepted |
| E2 V9 V1 install | install harness | rejected preflight: current GDScript hash was exact V9 postimage, V1 installer lacked idempotent state | not applied by this invocation |
| E2 V9 V2 install | three-state idempotent installer | prepared; installation pending | renderer OFF |
| E2 V9 native preflight | Godot 4.7.1 Mono JSON roundtrip + shared sidecar validator; structured result 30/30 | pending | no render before PASS |
| E2 physical A/B | two isolated CHALLENGE_001 renders, no audio; machine checks + human review | pending | only after native preflight PASS |
| E3 | D3 Music V5 / independent music_seed / FFmpeg mux / FFprobe | BLOCKED | E2 must be accepted first |
| E4A | Challenge family integration | BLOCKED | E3 / design gates |
| E4B | Visual Loop integration | BLOCKED | adapter/binder needed |
| E4C | Visual Drill integration | BLOCKED | adapter/binder needed |
| E5 | determinism, seed separation, GUI/CLI parity | BLOCKED | previous gates |
| E6 | Smoke18 | BLOCKED | all three families integrated |
| E7 | Matrix101 / runnable population | BLOCKED | 54+27+20 design, CH008/009 timing hold |
| E8 | independent acceptance, freeze, explicit promotion | BLOCKED | release authority NONE |

## E2 V9 V2 installation decision rule

For each of 6 replacements: exact V8 preimage = `APPLY`; exact V9 intended postimage = `ALREADY_PRESENT`; any other hash = abort before writes. For each of 10 add-only destinations: missing = `APPLY`; exact V9 postimage = `ALREADY_PRESENT`; any other existing content = abort. Validate all 16 payloads and destinations before first write. Receipt records every path, disposition, preimage/backup/postimage and current HEAD identity.

A native preflight PASS requires process exit 0 and structured result schema `C11E-E2-GODOT-JSON-NUMERIC-TEST-RESULT-V1`, status `PASS`, parsed gameplay/music Variant type `float`, full sidecar validation true and exactly 30/30 cases. No output-marker-only acceptance.

E2 physical acceptance requires both runs, receipt/checksum, AVI/MP4 hashes, correct metadata, nonuniform frames, body identity, title-slot A/B difference and independent human review. No audio in E2. E3 must not run before that acceptance.

C11-C is authoritative and immutable through E8. End product remains Challenge + Visual Loop + Visual Drill with presentation/editorial/music, final MP4 validation and the shared GUI/CLI service.
