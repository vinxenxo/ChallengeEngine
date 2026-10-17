# V2-B narrow start prompt — semantic binding review

Work only on reviewing the Challenge visual payload semantic binding proposals. First verify the live matrix contract (`3b4375957da12d16a6c7f652c1ba2536ce1a819b781b68b15e5dd3f0ee4bda75`), proposal contract (expected `d37cb74f360e19e664b94673bbf4b95462cad6e681a08215a95f4565c6e810aa`), and frozen C11-C manifest (`e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`). Stop and reconcile if any differs.

For each of the nine secondary bindings and six `custom_data` candidates, record the real source, mechanic, type, units/coordinate frame, temporal semantics, missing-value behavior, allowed visual effect, invariants, seed expectations, tests and review rationale. Current approved count is 0. Do not accept mappings by implication, do not bulk-convert `custom_data`, and do not modify the materializer yet.

Handle `CHALLENGE_008` and `CHALLENGE_009` timebase mismatches as a separate decision record; do not fix them unilaterally. After review, propose the minimal V2-B runtime acceptance design; test final visual payload hashes rather than inferring visual correctness from request/plan hashes. Maintain renderer OFF, no media, no payload materialization, candidate input inadmissible and release authority NONE.
