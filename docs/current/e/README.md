# C11-E — current program index (V16)

**Product target:** final audiovisual MP4 production for Challenges, Visual Loops and Visual Drills. Preserve the C11-C engine, generators and presentation; consume enabled D9.8 editorial fields in each family's real binder; generate D3 Music V5 from independent `request.music_seed`; mux with FFmpeg and validate with FFprobe. GUI and CLI share one C11-E production service. CHALLENGE_001 A/B is only the first technical control.

Authority: `C11E_CURRENT_AUTHORITY_20261031_V16.md`.
Gate matrix: `C11E_GATES_ACCEPTANCE_MATRIX_20261031_V16.md`.
E2 V8 JSON-number remediation: `C11E_E2_V8_JSON_FLOAT_SEED_REMEDIATION_20261031_V1.md`.
Execution hygiene: `C11E_EXECUTION_HYGIENE_AND_ASSISTANT_ERROR_LOG_20261031_V12.md`.
Product scope: `C11E_PRODUCT_SCOPE_PRESENTATION_EDITORIAL_MUSIC_20261030_V1.md`.
Commit policy: `C11E_LOCAL_COMMIT_EACH_ITERATION_POLICY_20261031_V1.md`.
D→E roadmap: `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261031_V6.md`.
New-window prompts: `prompts/C11E_NEXT_WINDOW_START_PROMPT_20261031_V16.md` and `prompts/C11E_CONTINUATION_MASTER_PROMPT_20261031_V16.md`.

## Latest E2 state

E2 V7 **FAILED**. The 9/9 Python pair tests and request preparation succeeded; Godot A exited 40 at the GDScript sidecar validator because Godot parses JSON numbers as float Variants while V7 required integer Variant types for the gameplay and music seeds. The failure archive proves one renderer invocation and one partial-frame AVI; it proves no accepted media. There is no B output, final MP4, success receipt or human review. Ignore the invalid console PASS text printed after the runner had already failed.

V8 adds a strict finite positive integral seed predicate and a Godot-native headless JSON numeric regression before any pair preparation or render. Package installation and E2 V8 physical retry are still pending. E3 remains blocked.

The user's supplied filtered snapshot records `main` / HEAD `b92434d6a8b50cef7e49ba6b75a4813777927fe7`, parent `a3c7c5d284a96ce115ca52208b4039002502753b`. The user commits locally every iteration; each installer must pin its package-time HEAD/parent. Runtime runners may accept descendants only with E0/E1 ancestry and exact source pins. Snapshots exclude artifacts/media: upload physical E2 evidence separately.
