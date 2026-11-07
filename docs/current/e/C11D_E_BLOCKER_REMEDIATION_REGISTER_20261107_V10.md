# C11-D / C11-E Blocker Remediation Register — V10

| ID | Blocker / risk | Current state | Remediation / acceptance |
|---|---|---|---|
| B-R1V-001 | R1V previously lacked explicit operator authorization | RESOLVED_FOR_BOUNDED_SCOPE | Immutable V2 policy + operator approval record; exactly 5×2 C11-C source launches |
| B-R1V-002 | R1V V1 conflicted with native C11-C `-NoSound` encode | RESOLVED_FOR_BOUNDED_SCOPE | V2 supersedes V1, preserving V1 unchanged; one exact pinned libx264 encode argv only |
| B-R1V-003 | Launcher may delete output-root/temp files | MITIGATED_IN_RUNNER; INSTALLER_AND_RUNNER_READY | Ten output roots absent, ten deterministic temp-silent paths absent, ten AVI prefixes empty; no cleanup/reuse/overwrite |
| B-R1V-004 | Transitive C11-C resource provenance incomplete | MITIGATED_IN_RUNNER | 30 R1P + 28 transitive + 3 Option C = 61 pins, checked before/after each launcher and final |
| B-R1V-005 | C11-C manifest sidecar parser mismatch | RESOLVED_IN_STATIC_TESTS | Validate actual `family_id`, `visual.*`, `audio.*`, `artifact_policy.*` structure; reject audio/GIF/AVI |
| B-R1V-006 | `override.cfg` may not restore after capture | GUARDED_FAIL_CLOSED | Exact preimage; restore only known C11C temporary bytes; unknown external bytes are preserved and fail |
| B-R1V-007 | First five source variants not visually accepted | OPEN | Complete ten captures, technical repeat comparison, operator review |
| B-OPTIONC-001 | Option C D compositor implementation absent | OPEN | Implement one generic D-only post-composition consumer after R1V review |
| B-E4A6-001 | `GeneradorMaestro.gd` intentional D-only postimage conflicts with C baseline policy | KNOWN_E4A6_D_ONLY_POSTIMAGE_POLICY_CONFLICT | Do not restore blindly or soften baseline. Prove D-only consumer independence, then rerun existing candidate evaluation |
| B-D4-8-001 | General D renderer activation | BLOCKED | Production policy remains DISABLED / runtime authority NONE; R1V bounded C source capture does not change it |
| B-D9-10-001 | D9.10 renderer dispatch | PREPARE_ONLY | Requires separate production/dispatch authorization after consumer acceptance |
| B-D9-14-001 | GUI real-media certification | BLOCKED | Requires later governed D media evidence |
| B-D9-16-001 | Full acceptance | BLOCKED | Requires all acceptance gates |
| B-D9-17-001 | Go decision | BLOCKED_NO_GO | Requires independent complete evidence |
| B-D10-001 | Promotion | BLOCKED_FOR_PROMOTION | No release authority |
| B-CH-008-009 | Challenge duration conflict | HELD | 11s declared vs 12s phase sum; do not silently alter |

R1V bounded scope is explicitly operator-approved; installation and physical capture remain pending. This is not a blanket closure of D4.8 general production. Preserve renderer OFF and release authority NONE.
