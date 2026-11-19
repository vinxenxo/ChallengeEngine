# C11-E E6 — Master handover: Option C Native Qt Probe V2 — 2026-11-19

## Mandate

Replace the C11-C 2.19.12 audiovisual factory with a complete D+E factory for Challenge, Visual Loop and Visual Drill: shared E1 service, family-specific generation contracts, D editorial/layout, correct family music, delivery encoding/mux, FFprobe/audio QA, reproducible manifests, review artifacts and immutable receipts. This is not merely a post-compositor substitution. The historical C chain is documented in `C11E_C11C_FACTORY_TO_DE_REPLACEMENT_ARCHITECTURE_V1.md` and its code inventory JSON.

## Current E6 technical checkpoint

- Option C remains the approved D-only postcomposition architecture; geometry V3 approved for Loop only: 720x1280 canvas, 504x896 content at (108,192), black 192px header/footer and 108px side gutters. Resampler quality is not approved.
- Python V4 compositor is disqualified as 30fps hot path: target P95 2050.1467ms / about 0.488fps.
- QImage V1 stopped before test execution because the runner compared full-manifest hashes to pointer-value hashes. Windows receipt `E6OPTCQT_20261119T204307Z_9BFC7875` is preserved; 0/37 tests and no benchmark ran.
- V2 changes the test adjudicator/runner and adds a pinned add-only installer plus versioned docs; it leaves the QImage compositor implementation unchanged. It structurally verifies the historical/current manifests differ at exactly `/source_lineage/6/sha256`, checks whole-file hashes separately from pointer-value hashes, and classifies the approved A3 specialized PASS. It does not alter any historic receipt, active source file, C11-C file or D4.8 V2.
- V2 retains the existing QImage module and 37 synthetic Qt tests. Windows runtime/PowerShell AST have not yet been executed for this package.

## C-to-D+E factory migration constraints

- Challenge retains its Challenge-specific effective-definition/timeline/capture route; Challenge music is D3 Music V5 when independently authorized.
- Loop retains its family grammar/binder/timeline and accepted family music until a separate music migration is qualified.
- Drill retains its family review envelope, phase/countdown/END_CTA precedence, binder/timeline and accepted family music until separately qualified.
- `request.seed` and `request.music_seed` remain independent. GUI is a thin dispatcher over the one E1 service; CLI stays as compatibility/test automation.
- Preserve family capture/timebase/identity. Do not flatten every family into one renderer or create a second Producer/binder/family adapter.
- Replace the whole production loop: request and family stage → D9.8/D9.9/D9.10 plan/bridge → D visual artifact → family audio → authorized FFmpeg mux → FFprobe/audio QA → manifest/sidecar/receipt/review.

## Next action

Install V2 add-only, confirm its PowerShell 5.1 self-AST and immutable pins, then execute `RUN_C11E_E6_OPTION_C_NATIVE_QT_PROBE_V2.py` under Python 3.13.14/PySide6 6.11.2 with exactly seven iterations. The only acceptable successful result is `PASS_QIMAGE_STAGE_BENCHMARKED_NOT_END_TO_END`; inspect its three synthetic previews and benchmark. A passing synthetic probe is not E6 acceptance and is not authority for a real frame, renderer, Godot, FFmpeg/FFprobe, audio or mux.

After V2 PASS, perform source-closure of the real Loop input/metadata, then a scoped one-selector copied-frame proof and visual/negative-control review. Widen to six Loop Smoke18 selectors only under a successor D4.8 policy and separate exact TEST_ONLY execution manifest.

## Immutable and blocked authority

C11-C 2.19.12 manifest remains 796,318 bytes / SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. D4.8 V2 remains 12,996 bytes / SHA `0866b53ad4fcdebe74d01f66864b2dfb00eb644ca28dcd59301c8f3208239c07` and BLOCKED. E1 PREPARE_ONLY; D9.10 PREPARE_ONLY; D9.14/D9.16 BLOCKED; D9.17 BLOCKED_NO_GO; D10 BLOCKED_FOR_PROMOTION. Renderer OFF; dispatch/media OFF; E6 accepted 0; no BatchId; `release_authority=NONE`. No C11-C protected mechanics, generators, core audio or frozen manifest changes. No Git checks; commits operator-managed; active-checkout SHA pins enforced.
