# C11-E E6 Reuse Evidence Hydration — V1 execution review / V2 handoff

**Date:** 2026-11-17  
**Disposition:** `V1_AUDIT_COMPLETED_BLOCKED / V2_PATH_NORMALIZATION_CORRECTION_REQUIRED / TWO_HISTORICAL_SOURCE_PINS_UNRESOLVED`

## Evidence received

- Library archive: `e6_reuse_evidence_hydration.zip`, 136,707 bytes, SHA-256 `3d69da2139bb2cbd80bf723072e8c6ec19ebedd2956fcad3ce72626437f28d9b`; ZIP CRC clean; four entries.
- Embedded report: `E6HYDRATE_20261117T210711Z_C7D200D2_REPORT_V1.json`, 819,729 bytes, SHA-256 `61cbbb657bf98acd297529f416a1c65951843e6c9b798635e7c2d4c0a302fe30`; embedded sidecar matches.
- V1 install: `PASS_ADD_ONLY_E6_REUSE_EVIDENCE_HYDRATION_INSTALL`; 3/3 payloads, 33/33 source pins pre/post; install receipt SHA-256 `73e7c46f8d28b1a6b8036a26ad363b6c583ecb48caf98b875d1fcf1836d12c2e`.
- V1 runtime: Python 3.13.14, PowerShell AST PASS, 18/18 tests PASS. Audit status `BLOCKED_E6_REUSE_EVIDENCE_INCOMPLETE`; 1,748/1,803 PASS; 55 failures.

## Failure adjudication

| Failure class | Count | Finding |
|---|---:|---|
| Project-root absolute paths rejected by V1 | 43 | 42 absolute references in six E4C Drill receipts plus one CH004 base-video reference. They are rooted under the recorded active checkout; V1 rejects all absolute paths before resolving the project-root prefix. |
| External runtime executable paths rejected by V1 | 10 | Five executable paths each in the Loop22 process receipt and run manifest. They are metadata references outside the project tree; V1 applies the artifact-only path policy without distinguishing the specific runtime tool fields. V2 allowlists only those exact fields and hashes the actual binaries. |
| CH004 historical source-pin drift | 2 | Actual byte/hash values differ from E4A.7 receipt's source pins: D9 universal editorial model and E1 production service. This is a real provenance divergence pending read-only adjudication; it must not be waived automatically. |

Total: 43 + 10 + 2 = **55**.

The 53 path-class findings are attributable to V1 path normalization; they are not evidence that the referenced media bytes are wrong because V1 did not read/hash those files. V2 must recalculate every reference. A successful V2 path fix is not itself an E6 acceptance.

### The two real source divergences

| File | Historical E4A.7 pin | Current observed file | Difference |
|---|---|---|---|
| `tools/c11d/d9/universal_editorial_model.py` | 26,574 bytes / `5c575be1942ba0613d66579d14db5cf9d7786e7062dfb001bd7be8a2e9c18ae5` | 27,585 bytes / `dac95fb698b52f96432a517d8ec3196a397e5e6bd3c025300350dd55ddce3afd` | 1,011 bytes |
| `c11c-suite/c11c-producer/c11e_production_service.py` | 32,885 bytes / `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951` | 86,687 bytes / `e5dbf9baa72d4c066ff8ba24006df954700d72a5b0f11f9f88aec653e84dce87` | 53,802 bytes |

The observed E1 file hash is independently present in source capture `C11E_E6_SOURCE_CAPTURE_20261117_204122.zip`, SHA-256 `1b35ade7f83618bc64cf3adadeabc0ed47e1b7173c9a65f85b813ee047e70609`. The D9 editorial current hash is recorded by the V1 audit but that file is not included in the source capture. The historical receipt remains immutable.

## Evidence coverage obtained by V1

- D9 manifest/receipt/install and 33 source pins: PASS.
- R1V operator closeout and five Loop selector A/B rows: 5/5 identified.
- Loop22 human closeout, process receipt and manifest were located by exact SHA; the manifest contained the expected `interference_plane` row.
- Drill qualification receipts: 6/6 located; 1,680 nested path/hash references enumerated. 42 could not be read because of V1's absolute-path rejection; those must be rehashed by V2.
- CH004 E4A.7 receipt located by exact SHA; 34 nested references enumerated. The base video path was rejected by V1; two source pins showed actual SHA mismatches; the remaining nested references passed.
- Governance flags in the report remain read-only / no renderer / no media / no BatchId / no dispatch / release NONE.

## Disposition and no-rerun rule

Do not re-run E4, R1V, Loop22, Drill, or CH004 A/V outputs. Do not edit old receipts, output hashes, source pins, or the user's failed report. V1 remains installed and immutable. Use the new add-only V2 path-normalization auditor to re-read the exact files. Keep CH004 reuse blocked until its two source divergences are adjudicated with historical preimage bytes or a documented exclusion decision.
