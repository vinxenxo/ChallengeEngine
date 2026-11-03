# C11-E Execution Backlog — V5

**Date:** 2026-11-03  
**Immediate step:** rerun the corrected read-only E4A source discovery V2 through the self-extracting PowerShell launcher. E3 is closed test-only on the supplemental recovery receipt.

## 1. E3 V1.5 closure

Windows run completed all source/preflight pins, Python 3.13, FFmpeg/FFprobe, `py_compile=0`, and the full C11-E discovery suite. The V1.5 runner asserted exactly 50 tests, zero skips and `OK`, then failed while hashing `runner_transcript.log` under the active `Start-Transcript` file lock. The original `BLOCKED` status remains immutable. The read-only recovery completed with PASS and receipt SHA `8e01946da3de35c05430335259a88e14f5bae1b660c6896de5d8f13c37c3fafe`; no rerun occurred. E3 negative controls and formal E3 test-only closure are PASS.

## 2. V1 overlay defects

- V1 installer expected a truncated V26 doc hash ending `...fed1`; active file hash includes the final `a` (`...fed1a`). It stopped during protected-pin validation before any documentation writes.
- V1 discovery ended `Los tipos de argumentos no coinciden`. V2 replaces generic typed collections with simple arrays, executes one text-search pattern per call and records detailed exception diagnostics. No production source is modified.

## 3. E4A.0 corrected discovery

Run `START_C11E_E3_RECOVERY_E4A_DISCOVERY_V2.ps1` alongside its V2 ZIP. The launcher verifies the ZIP SHA, extracts into a fresh folder, applies versioned docs add-only, validates/skips an already-recovered E3 receipt (or invokes recovery if absent), and runs the read-only discovery. It stops on every nonzero exit and retains stdout/stderr logs.

E4A.0 must provide exact paths, line references, SHA pins, binder/consumer symbols, layout sources/slots, authorized editorial field routing, E1 service call, CLI argument contract and current GUI dispatch callback. No source patch or renderer/media run occurs.

## 4. E4A implementation gate

After E4A.0 review, refresh live pins immediately before patching. Implement the smallest CLI-first change in the proven existing Challenge consumer, then expose the same service/worker through the current Producer GUI. Prove title/subtitle/CTA and Challenge-specific fields only where D authority explicitly enables them; language stays metadata-only. Prove layout geometry, visibility, clipping and pixel effects; use D3 V5 Challenge audio via E3 mux/QC. No parallel binder/renderer/producer.

Run static/preflight and focused tests before any gameplay render. A physical Challenge audiovisual A/B/C test follows only when the source contract is established.

## 5. Remaining gates and coverage

E4B Loop, E4C Drill, E5 cross-family determinism/seed isolation/adapter non-leakage and CLI/GUI parity, E6 Smoke18, E7 Matrix101, E8 independent acceptance. Reconcile all historic C11-C test/review categories row-by-row before E8, including 27 reviews and 9 Challenges. Keep CH_008/009 held (99 provisional Matrix101 cases) pending authoritative timing resolution.

## 6. Do not repeat or modify

Do not rerun E0/E1/E2/E3.2, V1.3/V1.4, E3 physical audio pilot or V1.5 50-test suite without a relevant source/test pin change. Do not rerender R4. Do not alter C11-C generators/mechanics, `core/audio`, D3 V5 engine, E1 service, D governance or C11-C manifest. No sixth suite module or `c11d-control`.

C11-C 2.19.12 remains sole production authority; `release_authority=NONE`, no freeze or promotion.
