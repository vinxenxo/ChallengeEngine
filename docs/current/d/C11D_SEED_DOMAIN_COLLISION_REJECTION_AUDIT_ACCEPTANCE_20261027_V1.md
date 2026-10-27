# C11-D — Aceptación de auditoría de colisión de semillas V1 en Windows

Fecha: 27-10-2026  
Estado: `WINDOWS_PASS_PRECHECK_REJECTIONS_ONLY; CATALOG_WIDE_COMPLETENESS_NOT_ESTABLISHED`.

## Aplicación documental

El overlay previo se aplicó en el checkout Windows activo con `GUARDED_REPLACEMENTS=2/2_HASH_VERIFIED`, `ADD_ONLY_FILES=3/3_HASH_VERIFIED` y `FROZEN_C11C_MANIFEST=UNCHANGED`. Backup: `C:\Users\vinxe\AppData\Local\Temp\C11D_POST_V2_2_AUDIT_BACKUP_448f6df1a04945fb975b17797c307f80`.

## Evidencia real de Windows

```text
C11D_SEED_DOMAIN_COLLISION_REJECTION_AUDIT=PASS
AUDIT_EXIT_CODE=0
SELECTORS=2
EXPLICIT_SEED_NEGATIVE_CASES=20/20
NUMERIC_SEED_COLLISION_REJECTIONS=4/4
COLLISION_VALUES=12345,840001
ALL_REJECTIONS_PRECEDE_GODOT=true
SOURCE_PINS=23/23
RUNTIME_INVOCATIONS=0
AUDIT_SHA256=2eb512f38740052ab2a3f06bda35eae3374c6a28d241734dafa7567a99f6fcd0
REPORT_FILE_SHA256=aa386c6f61a993c52353814b03dc581bef27f45de805b1278e212cb78a3cf642
STDOUT_SHA256=8e093a5c9f1ceab56aa825795c8290f3abe282119a3f471f4aa7beba898dab0d
STDERR_SHA256=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

- Log directory: `%TEMP%\C11D_SEED_DOMAIN_COLLISION_AUDIT_20261027_1bc24be1ec5c406ea02434e9b3514cb5`.
- Report: `%TEMP%\C11D_SEED_DOMAIN_COLLISION_AUDIT_20261027_1bc24be1ec5c406ea02434e9b3514cb5\seed_domain_collision_report.json`.
- Completion marker: `%TEMP%\C11D_SEED_DOMAIN_COLLISION_REJECTION_AUDIT_20261027.completed.json`.

Resultado aceptado exclusivamente para los dos selectores del contrato V1: `parking_v2/CHALLENGE_004` y `c11c_geometric_waves_v1/harmonic_membrane`. El guard rechazó las dos colisiones numéricas para cada uno antes de Godot; no se invocó Godot.

## Límite

El PASS no demuestra que los dominios de semillas estén completos para todo el catálogo, ni sensibilidad visual de los nueve Challenges, ni soporte dinámico de payload para otros selectores. Se conserva `seed_domains_complete_for_candidate_input=false` y todas las puertas de admisión siguen cerradas.
