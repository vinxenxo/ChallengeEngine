# C11-E — gates and acceptance matrix (V13)

| Gate | Functional deliverable | Acceptance evidence | State at 2026-10-31 cut-off |
|---|---|---|---|
| E0 | Reconcile checkout, C manifest, receipts, source pins and instructions | E0 receipt, 13/13 payloads, 3/3 archives | **APPLIED** |
| E1 | One shared GUI/CLI service with request/editorial/seed/provenance parity | Windows tests and separate GUI observation | Automated 2/2 PASS; GUI observation pending |
| E2 | Challenge `title` affects only its own visual slot, not gameplay | Two MP4s, FFprobe, frame-level A/B compare, receipt and human review | V5 tests 9/9 and pair prep PASS; V5 runner failed pre-Godot. V6 V1 installer failed before writes (0/9); V6 V2 package prepared, Windows installation pending |
| E3 | D3 Music V5 generation and final mux | Independent music seed, WAV, FFmpeg mux, FFprobe A/V | Not started; E2 dependency |
| E4A | Full Challenge presentation/editorial/music | Existing Challenge generator/binder + enabled editorial + D3/mux | Not started |
| E4B | Full Visual Loop presentation/editorial/music | Existing Loop grammar/generator/binder + enabled editorial + D3/mux | Not started |
| E4C | Full Visual Drill presentation/editorial/music | Existing Drill type/tier/generator/binder + enabled editorial + D3/mux | Not started |
| E5 | Determinism, replay, independent seeds, pixel isolation and GUI/CLI parity | Hash/frame/stream comparisons and source-bound receipts | Not started |
| E6 | Smoke18, six reviewed A/V renders per family | 18 physical reviewed A/V outputs and receipts | Not started |
| E7 | Matrix101: 54 Challenges + 27 Loop grammars + 20 Drill variants | Full 101-case result; no silent omissions | Not started; runnable scope 99 while CH_008/009 held |
| E8 | Formal independent acceptance and freeze/promotion decision | Separate reviewer/operator decision and immutable evidence | Not started |

## V6 V2 installer boundary

The installer itself does not invoke the renderer or create media. It requires the exact main/HEAD/parent, C11-C manifest, E0 receipt, V6 V1 failed receipt, current V5 runner/README preimages, E2 source pins, exact payload hashes and add-only destinations. It archives only one verified orphan temp whose hash equals the intended V6 runner postimage. Replacements use a non-null unique backup path; the preimage backup is hash-verified and retained in the receipt directory. Any installer nonzero exit blocks the runner.

## E2 physical acceptance

After verified installation, a fresh V6 run must produce exactly two Challenge 001 MP4s. Both must pass FFprobe. Gameplay/body source and output frames must remain identical; the designated title region must show the expected A/B delta. Retain provenance, pair receipt, source/render/media hashes and human visual review. Preparation receipts, unit tests and process exit alone are insufficient.

## Family acceptance and invariants

E4A/E4B/E4C must use actual family-specific C generators and binders; route enabled D9.8 fields into family-correct distinct visual slots; render physical source media; generate D3 audio from `request.music_seed`; mux via FFmpeg; validate final MP4 via FFprobe; preserve provenance. GUI/CLI share one service. Gameplay `request.seed` remains isolated from `request.music_seed`.

Do not modify C11-C manifest, protected C mechanics/RNG/frame-stream semantics or D governance. Do not serialize arbitrary `FrameSnapshot.custom_data`. Reserved editorial fields stay disabled. E2/E3/E4 PASS never grants release authority or promotes C11-E over C11-C.
