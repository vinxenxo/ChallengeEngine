# C11-E Execution Hygiene and Assistant Error Log — V20

**Date:** 2026-11-03
**Authority:** V24 current authority and gate matrix.

## Repository and package discipline

- Active Windows checkout is authoritative. Uploaded ZIPs, library snapshots, source indexes and historic receipts are supporting evidence only.
- Current base after E3.2: branch `main`, HEAD `3cc1caa6d740b1525a4ebb30a4ff7f02868ac5a8`, parent `a30b63d31b2d071ebab9c67ec9f8ff7393731488`, tree `de8a1180f04eb0f5e0ea5c8130eedaaccf7e78fa`; last supplied worktree clean and `ahead 4` of origin/main.
- Every next overlay must record exact base branch/HEAD/tree and verify C11-C manifest before the first write. The documentation overlay is add-only and must be committed locally before a code overlay is based on its resulting HEAD.
- Do not reset, clean, checkout, rebase, amend, force-push, push or manipulate Git refs. User commits locally each iteration.
- Add-only files: absent means APPLY; identical postimage means ALREADY_PRESENT; differing content is a hard stop. Replacement files require exact preimage or exact intended postimage only. Preflight all destinations before writing.
- Installer must report actual changed path count from the operation results, not compare the allowlist length with changed-path count.
- Capture native process exit code immediately. On nonzero exit, missing/malformed structured receipt or incomplete evidence, stop. Do not run success assertions after a failed process and never print a manual PASS.
- PowerShell 5.1 compatible. Do not use `&&`, `Read-Host`, PowerShell 7 syntax or fragile shell redirection. Capture stdout/stderr independently and hash them; native FFmpeg/FFprobe diagnostics on stderr are not automatically failures.
- Keep new evidence under fresh per-run roots. Never overwrite prior R4/E3 evidence. Each physical run gets a unique RequestId.
- `git diff --check` does not display untracked file contents. Validate staged content before commit; use `--untracked-files=all` for the full status.

## Render and protected-source rules

- No `core/audio`, C11-C generator/mechanics, protected audio generator, canonical Challenge, timing, RNG, C11-C manifest or D authority mutation.
- Keep exactly five `c11c-suite` modules and one canonical E production service. No `c11d-control`, sixth module or parallel service.
- E1 does not dispatch. D9.10's D adapter remains PREPARE_ONLY. Do not relabel D envelopes renderer-native or bypass D4.8/D locks.
- E3 audio/mux tests may create media only under a fresh `artifacts/tests/c11e/e3/<RUN_ID>` root or system temp as appropriate. No `artifacts/production`, releases or catalog promotion in E3.
- Do not rerender gameplay to test a music seed. Reuse the verified E2 R4 video and produce independent audio/mux derivatives.

## GUI-first operation

- From V24 onward, all manual content selection, request editing, editorial controls, seed entry, job launch, progress review, media preview and result inspection happen through the existing Producer GUI.
- Do not ask the operator to manually use CLI commands as a production workflow. CLI remains a thin compatibility adapter and automated separate-process test target over the same service.
- GUI handlers must not duplicate request resolution, seed policy, dispatch selection, receipt construction or media validation; those belong to the shared service.
- Record a real Windows GUI launch and interaction. Static widget tests are not a substitute. Do not infer E1 GUI acceptance from automated E1 service tests.

## Corrections recorded

1. A previous assistant response described 104 BPM as if it were a general D9.2 contract value. The D9.2 contract does not establish a global tempo default. The historical D9.2 runner uses `--tempo 104` for its fixed CHALLENGE_001 pilot fixture. Keep 104 only as that controlled fixture unless a versioned profile/contract authorizes a general default.
2. D3.1's `duration_seconds` input is required. V5 CLI's four-second fallback is not a production duration policy. E must derive duration from the validated visual artifact's FFprobe stream/frame metadata.
3. D3.3's 30-second window is a loudness measurement/mastering workflow, not a license to make a 9-second video carry 30 seconds of audio. E must create a duration-matched delivery stream after mastering and verify it.
4. D9.2's AAC/48 kHz/192k mux and 0.15-second duration drift are a historical Challenge pilot precedent, not an automatic universal codec contract for every output family/profile.
5. The V13 statement `54+27+18=99` conflicts with the target inventory `54+27+20=101` and two held Challenge cases. Use provisional `52+27+20=99`; re-confirm from the live catalog before Matrix101.
6. The earlier V23 E3 source-discovery runner invocation stopped because the checkout was dirty. It is not a PASS. Reconcile active sources after E3.2 and after this docs commit; do not rely on the stale runner's expected HEAD.

## Current status

E3.2 PASS/committed; E3 physical audio, mastering, mux, FFprobe and E3 GUI operation remain NOT RUN. No production renderer/audio/mux has been authorized by E3.2 alone. Release authority remains NONE.
