# C11-C Producer 0.9.0 — Runtime Acceptance

## Required local checks

```powershell
cd .\c11c-producer
python .\self_test.py
python .\preflight.py
.\run.bat
```

## A LA CARTA acceptance matrix

| Type | Test | Delivery | Expected evidence |
|---|---|---|---|
| Challenge | any of `CHALLENGE_001..009` | `MASTER_1080` | source 540×960 → final 1080×1920 |
| Visual Loop | any family/seed | `MASTER_1080` | proven 720×1280 capture → final 1080×1920 |
| Visual Drill | Tracking/Saccade/Pursuit/Peripheral Scan | `MASTER_1080` | C11-C phase envelope + final 1080×1920 |

## UX acceptance

- No banner/header occupies the working area.
- No helper paragraphs are shown in the working area.
- Variation parameters are controlled by slider + `ALEATORIO`.
- Active queue row is visibly highlighted.
- Completed row remains visible and dimmed.
- Existing manual-seed product is shown as `YA PRODUCIDO` and skipped unless `FORCE`.
- Delivery profile remains visible in the recipe form.

## Known architectural guard

A delivery-profile change must not modify Challenge mechanics, simulation, RNG or C11-B logical social geometry. Delivery remains a post-capture concern.
