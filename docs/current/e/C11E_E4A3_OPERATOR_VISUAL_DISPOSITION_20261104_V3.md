# C11-E E4A.3 operator visual disposition — V3

**Date:** 2026-11-04  
**Disposition:** `PASS_USER_CONFIRMED_INTENTIONAL_SELECTED_CONFIGURATION`

The operator confirms that the countdown hook and editorial layer appearing together in the reviewed runner output is an intentional configuration. The output demonstrates that the editorial consumer renders its fields in that selected composition. The coincidence is not, by itself, a compositor defect or failed layout test.

The presentation system is configuration-dependent. It is incorrect to require every field to print on every Challenge. Future Producer GUI must expose the relevant visibility choices as request values and pass them through the existing E1 service to the D-owned consumer. At minimum, countdown-hook visibility must support on/off. Other editorial options must be grounded in approved policy and recovered historical Challenge configurations, rather than guessed.

The next coverage plan must:
- inspect D1.1 Challenge mapping, D1.5 region topology, D1.7 declarative mappings, historical Challenge binders/profiles and per-Challenge definitions/tests/receipts;
- enumerate only evidenced configurations;
- exercise countdown on/off and policy-authorized title/subtitle/CTA presence or omission;
- capture expected phase/region, PNG/frame evidence, body identity and no-change controls for each configuration;
- retain UNKNOWN geometry/typography as UNKNOWN.

`player_name` and `challenge_label` remain blocked pending their geometry authority; `language` remains metadata-only. This disposition does not approve every untested combination or establish a generic safe-area rule.
