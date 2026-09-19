C11-B.0.1 NEXT DIAGNOSTIC

No engine or mapper change is introduced by this revision.
The audit now prints body_rect, logical, expected and actual positions for failed runs.

Purpose: determine whether the runtime is actually mapping the CHALLENGE_001 Sprite2D,
or whether the observed gate rectangle comes from a stale/different presentation path.

Run:
  .\tools\run_c11b_body_visibility_audit.ps1

Do not rerender C11-A.1.
