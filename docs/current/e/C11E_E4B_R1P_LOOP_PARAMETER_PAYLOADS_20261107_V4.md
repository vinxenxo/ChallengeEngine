# C11-E E4B R1P — Loop Parameter Payloads V4 / Final Closeout

**Date:** 2026-11-07  
**Phase state:** `CLOSED_PASS_27_OF_27`  
**Run:** `E4B_R1P_20261107_032743_5F75045C`

## 1. Final result

The operator ran the add-only archive-recovery installer (12/12) and recovery-only process in the active Windows checkout. Recovery exited 0 and returned:

`PASS_R1P_ARCHIVE_RECOVERED_AND_PAYLOADS_REVALIDATED_27_OF_27`

The recovery verifier checked the existing run only. It did not rerun Godot, rematerialize recipes, invoke prototypes/launchers or modify source files.

## 2. Hash-pinned evidence

| Evidence | SHA-256 |
|---|---|
| Original R1P ZIP | `a3bb4ddd6f4933026b0221c7e0eb1b62ffe40d477d72ce0190bbe9587b67b800` |
| Recovered R1P ZIP | `d49f54ffdee6026426c2bb87fcb72b5c8a68f09cb64fb91f71e25dc10fd26b52` |
| R1P canonical report | `9e09940c7a915d1533a2ba0a97765626f5c5d8533c870cda27012d4d90c97b41` |
| Receipt hash-set digest | `523add74c2607d6b5c85fb5f9b270fa5fbca800d3dd05d05131482b044e1a42d` |
| Parent bindings | `460165c92f3afaebc023a49ab5e0fdb86f7fe4c8133032bb54f6bef67ef0911a` |
| Source manifest | `bb5b101492d18ee6c27a649874ffac75aa5dcb2de44cbdc5718902b4cfc6e441` |
| Recovery report | `6bd16983a01919c7c41f785b281988139ae2a569a23daa81db6a20694f21c640` |
| Recovery process receipt | `b4299cca349b646cc05fffaf83765f5108ad55b70d177d27ce0745031a4c07a0` |
| Recovery stdout | `b004a48b98e34b9eb4cf1ca14e3d9ea8b9f223c998b4c0eabd6ab7faac7f77ce` |
| Recovery stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## 3. Independent archive cross-check

The uploaded original and recovered ZIPs were reviewed read-only:

- 72 members in each archive;
- identical normalized member-name sets;
- all 72 member byte streams exactly equal after replacing backslash path separators with `/`;
- recovered ZIP CRC passes and has no backslash-bearing paths;
- 27 JSON receipts and 27 `.json.sha256` sidecars;
- all 27 canonical receipt hashes and sidecars pass using the verifier's canonicalization rule (remove `receipt_sha256`, recursively key-sort JSON, compact UTF-8 serialization);
- 27/27 `payload_sha256 == repeat_payload_sha256`;
- 27 unique selectors across five families: Geometric Waves 5, Fractal Bloom 5, Sacred Symmetry 5, Living Particles 5, Invisible Forces 7;
- 30/30 source manifest pins match V84 snapshot; operator's active Windows recovery output independently states 30/30 live source pins;
- captured R1P process log hashes match the embedded process receipt; all recorded process exits are zero and error streams are empty.

R1P timing descriptors: 8 selectors at 20 seconds/600 frames, 7 at 22 seconds/660 frames, and 12 at 23 seconds/690 frames, all 30 FPS. These are expected descriptors only. They are not measured media-frame inventory.

## 4. Root-cause closure

The V1 runner's final archive predicate searched for `receipts/...`, while Windows ZIP entry names used `receipts\...`. The original ZIP contained all expected 72 files and all 27 receipts; the exception was a separator-normalization false negative after finalization. Recovery normalized member names without changing member bytes.

## 5. Acceptance boundary

R1P proves request-bound deterministic visual parameter recipes/timing only. It does not prove actual family output frames/pixels, D9.10 pixel consumption, renderer input, visual pilot, audio, mux or production. R1P is complete and must not be repeated.

Next: R1V actual frame inventory/pixel hashes, only after architecture/policy disposition and bounded D4.8 qualification authorization. See R1V design V2 and the D baseline-isolation decision docket.
