# C11-E — gates and acceptance matrix (V15)

| Gate | Deliverable | Acceptance evidence | State at 2026-10-31 cut-off |
|---|---|---|---|
| E0 | Reconcile checkout, C manifest, receipts, source pins and instructions | E0 receipt, 13/13 payloads, 3/3 archives | APPLIED and locally committed at b92434d |
| E1 | Shared GUI/CLI production service | Windows tests + separate GUI operator observation | Automated 2/2 PASS; GUI observation pending |
| E2 | CH001 title changes only its visual slot, not gameplay | Two nonblank AVIs/MP4s, FFprobe, A/B frame comparison, source provenance and human review | V5 fails at summary/receipt lookup; V6 passes 9/9 pair tests but Godot script parse failure + uniform grey AVI; V7 V1 installer refused stale checkout pins with zero writes; V7 V2 package prepared, install pending |
| E3 | D3 Music V5 and final audio mux | Independent `music_seed`, WAV, FFmpeg mux, FFprobe | Not started; blocked by E2 |
| E4A | Challenge presentation + enabled editorial + music | Existing Challenge generator/binder and D3/mux | Not started |
| E4B | Loop presentation + enabled editorial + music | Existing Loop grammar/generator/binder and D3/mux | Not started |
| E4C | Drill presentation + enabled editorial + music | Existing Drill type/tier/generator/binder and D3/mux | Not started |
| E5 | Determinism, seed isolation and GUI/CLI parity | Source-bound hashes, frame comparisons and repeatability | Not started |
| E6 | Smoke18: six audiovisual cases per family | 18 physical reviewed A/V outputs and receipts | Not started |
| E7 | Matrix101: 54 Challenges + 27 Loop grammars + 20 Drill variants | Complete 101-case evidence set | Not started; runnable scope 99 while CH_008/009 held |
| E8 | Independent acceptance and explicit freeze/promotion | Independent reviewer decision + immutable evidence | Not started |

## E2 safety and acceptance

V6 created a uniform grey AVI after Godot reported a GDScript parse/load error; exit 0 and “Done recording movie” are not acceptance. V7 explicitly fixes Variant typing, rejects parse/load errors, probes source frames 60/270/480 for nonuniform pixels and records actual Godot/media activity. E2 remains exactly two CHALLENGE_001 A/B runs, no audio. The next runner invocation must use the current `main` HEAD with E1/E0 ancestor commits and all exact source pins. A runner exit 0 still requires separate human visual review.

## Per-iteration commit identity

Operator commits every iteration. Installer packages pin the exact HEAD/parent current at package-build time; each next package refreshes these pins. The runtime runner captures actual HEAD/parent and accepts descendant local commits only if E1/E0 ancestry and exact source pins are intact. No reset, clean, branch switch, rebase, amend, ref movement or push is used to satisfy a gate.

All C11-C freeze and D governance/release locks remain unchanged. E2/E3/E4 success does not itself grant release authority or promote E over C11-C.
