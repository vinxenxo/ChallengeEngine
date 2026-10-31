# C11-E — current program index (V13)

**Product target:** final audiovisual MP4 production for Challenges, Visual Loops and Visual Drills. Preserve the C11-C engine and presentation, consume the enabled D9.8 editorial fields in each family’s actual visual binder, generate music through D3 from the independent `request.music_seed`, mux with FFmpeg and validate with FFprobe. GUI and CLI share one C11-E production service.

Authority: `C11E_CURRENT_AUTHORITY_20261031_V13.md`.
Gate matrix: `C11E_GATES_ACCEPTANCE_MATRIX_20261031_V13.md`.
E2 V6 physical retry authority: `C11E_E2_V6_REMEDIATION_AND_RETRY_AUTHORITY_20261031_V2.md`.
Scope and family-specific visual/audio contract: `C11E_PRODUCT_SCOPE_PRESENTATION_EDITORIAL_MUSIC_20261030_V1.md`.
Execution hygiene and error prevention: `C11E_EXECUTION_HYGIENE_AND_ASSISTANT_ERROR_LOG_20261031_V9.md`.
D→E roadmap: `docs/history/c11d/C11D_TO_C11E_FULL_FAMILY_ROADMAP_20261031_V3.md`.

E0 V2 is applied and its three V9 instruction archives are hash-verified. E1 Windows automated tests remain 2/2 PASS; manual GUI observation is pending. E2 V5 passed its 9 contract tests and pair preparation but failed before Godot: the runner incorrectly queried `request_id` on the CLI summary instead of the hash-verified `E2_PAIR_PREPARED.json` receipt. The V6 runner patch fixes that schema read. The first V6 package installer then failed before any payload write because it called `.NET File.Replace` with a null backup path. Its receipt records 0/9 files applied; the runner remains V5. V6 remediation package V2 now uses a verified, non-null backup path on the same volume, pins the failed V1 receipt, and safely archives the one verified orphan temp file before applying. Physical E2 retry remains pending.
