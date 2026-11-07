# E4B D9.8 / D9.9 Semantic Reconciliation — V4

D9.8 has separate dimensions that must not be collapsed:

- **D9.9 plan compatibility:** the canonical universal request/editorial intent can be normalized and represented in plan-only form for Challenge, Loop and Drill.
- **D4 executable compatibility:** a request is admitted to a real renderer only when its family-specific payload consumer, input schema, source binding, gate and authority are all accepted.

For Loop and Drill, V2 sets plan compatibility true while preserving D4 executable compatibility false. This is intentional. `PLAN_ONLY` is not renderer admission.

The E4B shared-service boundary now resolves the Loop preparation for its canonical 27 grammars through the E1 service used by GUI and CLI. It does not mean a family adapter consumes pixels. The accepted policy selections define composition constraints and editorial intent; they do not enable render dispatch or add request fields.

V2 installer receipt construction has a Windows PowerShell 5.1 generic-list conversion defect. V3 performs an exact postimage/add-only/backup reconciliation and provides the stable runner. See Authority V82 and blocker register V3.

Hard invariants: C11-C mechanics and family binders unchanged; visual launcher `-NoSound` with `request.seed`; music independently uses `request.music_seed`; no D3 V5 for Loop/Drill; D9.10 `PREPARE_ONLY`; D4.8 `BLOCKED`.
