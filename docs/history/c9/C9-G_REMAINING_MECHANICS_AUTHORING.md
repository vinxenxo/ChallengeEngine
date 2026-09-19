# C9-G — Remaining Mechanics Authoring Productization

Cierra la productización de authoring para las cinco mecánicas restantes del corpus C7:

- key
- pilot
- find_v1
- choose_v1
- count_v1

Cada mecánica obtiene un adapter productivo, una familia visual dedicada y un binding de vídeo/audio coherente con su fixture C7.

## Pipeline

```text
authoring_remaining_c9_batch.json
        -> ChallengeGenerator
        -> Canonical V2
        -> ChallengeMigrationAdapter
        -> Runtime V1
        -> build_factory.py
        -> 5 manifests PASS
```

La excepción `C7_A2_MIXED_BATCH_REQUIRED` puede aparecer porque este lote es audio-on únicamente. Se considera política de lote no bloqueante; cualquier otro error invalida C9-G.

### FIX4 — count_v1 nested structural parameters
`count_v1` fija `min_value=3` y `max_value=10` dentro del bloque estructural `simulation.parameters.count`. El batch deja `overrides` vacío para evitar validación errónea contra parámetros raíz.
