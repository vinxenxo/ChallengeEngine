# D9 — Challenge Temporal Alignment Policy Proposal V1 (2026-10-11)

A proposal-only contract was added to reconcile the already reviewed Challenge timeline and the separately proposed editorial and sampling policies. The supported fixture is `CHALLENGE_004`, 900 source frames at 60 FPS to 450 delivery frames at 30 FPS. Cumulative source boundaries `[0,180,600,780,900]` map to `[0,90,300,390,450]` exactly. The timeline phases remain zero-based half-open ranges.

The known winning anchor maps from source frame 574 / GAME-local 394 to delivery frame 287 / GAME-local 197 because the selected GAME-local cadence is even-indexed. This is a parity assertion only; selection does not use the winning frame as an input, and `close_calls` does not contribute to timing.

The policy remains `PROPOSED_NOT_APPROVED`. The contract only reconciles existing declarations and performs static checks; it does not materialize snapshots, renderer input, persistent evidence or media. C11-C stays immutable, renderer OFF, D4.8 BLOCKED, release authority NONE. Full D9.14/D9.16 acceptance, D9.17 closure and D10 remain blocked as required.
