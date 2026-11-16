# C11-D/E Blocker Remediation Register — V89 (2026-11-16)

| ID | Boundary / issue | State | Required disposition |
|---|---|---|---|
| E5-PREP-01 | E1 family adapter not connected | OPEN / GOVERNED | PREPARE_ONLY canary only; do not create media or invoke renderer; later adapter connection requires separate authority |
| E5-GUI-01 | GUI-origin service parity vs actual Qt interaction | PARTIALLY COVERED BY DESIGN | Canary checks shared-service GUI origin and static GUI wiring; actual Qt session remains explicitly NOT RUN |
| E5-AV-01 | Full three-family A/V qualification | BLOCKED | Requires governed adapter connection and distinct A/V authorization; not part of this PREPARE_ONLY overlay |
| E7-TIME-01 | CH_008 / CH_009 declared 11s vs phase sum 12s | HELD | Await authoritative timing resolution; 99 provisional runnable cases |
| E8-AUTH-01 | C-to-D+E transition / production promotion | BLOCKED | Complete historical regression, independent acceptance, immutable freeze and separate explicit governance decision |

## Permanent controls

C11-C 2.19.12 remains sole production authority. Frozen C11-C manifest SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. `renderer=OFF`; `production_dispatch=false`; `production_media=false`; `release_authority=NONE`. No Git checks; operator manages commits. Source pins are mandatory. No protected core/mechanics/generator/binder/RNG/audio/canonical-definition changes, parallel Producer or sixth module.
