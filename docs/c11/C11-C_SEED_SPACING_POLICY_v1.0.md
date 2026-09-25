# C11-C Seed Spacing Policy v1.0

## Objective
Production batches must avoid both repeated seeds and clustered numeric seed values.

## Strategy
`stratified_spread_random_v1` partitions the configured integer range into separated bins, chooses one random value from each bin, shuffles the result, and validates the minimum pairwise gap. The minimum gap is 40% of the nominal bin spacing.

## Scope
The policy applies to weekly 27-product production, monthly production across the complete month, one-family production bulk, 5x5 production and long-form segment seeds. Historical explicit review fixtures remain allowed so old visual references stay reproducible.

## Audit
Batch manifests expose `seed_strategy`, `minimum_seed_gap`, the full seed list and unique video key count.

## Frozen boundary
This is production allocation logic only. It does not alter gameplay RNG or authoring truth.
