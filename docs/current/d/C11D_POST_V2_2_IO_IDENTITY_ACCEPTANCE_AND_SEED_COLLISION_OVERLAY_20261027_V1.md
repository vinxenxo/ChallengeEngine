# Overlay — aceptación del refresh I/O/identidad y gate de colisión de semillas

**Overlay ID:** `C11D_POST_V2_2_IO_IDENTITY_ACCEPTANCE_AND_SEED_COLLISION_AUDIT_20261027_V1`  
**Modo:** `GUARDED_REPLACE_AND_ADD_ONLY`  
**Propósito:** registrar solo los resultados Windows recibidos del refresh post-V2.2 y añadir un ejecutor de solo lectura para la siguiente auditoría fail-closed de semillas. No cambia los contratos de producción ni autoriza renderer/media.

## Aplicación y precondiciones

El lanzador verifica SHA-256 del ZIP, lista exacta de entradas y hashes/tamaños de staging; verifica que el manifiesto C11-C conserve SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953` y `796318` bytes; verifica todos los `before_sha256`; crea un backup comprobable de los dos destinos reemplazados; exige que los destinos add-only no existan; y vuelve a verificar todos los hashes finales. Si una guarda falla, se detiene.

## Resultados Windows aceptados

- I/O: exit `0`; groups `10`, complete `0`, partial `6`, blocked `4`, source pins `54/54`; audit `b8c5d5994d349c1ce9fef518d7633f72565f3c927cd7bc51cdd89fe5d2df2fe2`.
- Identity: exit `0`; sources `164`; fingerprint `0b4168bddac991ac03ea45d424f5af4fa2316c275dc31c1866c5cf8baf532d25`; report `74e518b620d297c5e09cf6e9495864dbe96e9394b6520e9a5e492775642b92bf`.
- Efecto permitido: actualizar checkpoint/ledger y añadir el registro de aceptación y helper read-only.

## Gate que sigue

El helper nuevo ejecuta el audit Python existente sin Godot ni persistencia al repositorio. Guardará las salidas completas y el informe en `%TEMP%`, separará stdout/stderr, validará el marker, los valores exactos y el estado bloqueado; un marcador de intento creado antes de ejecutar impide repetir el gate accidentalmente, incluso tras un fallo parcial; el marcador de finalización solo se crea cuando todas las guardas pasan. Espera `20/20` negativos y `4/4` colisiones, `23/23` pins y cero invocaciones Godot. Ningún valor esperado se registra como PASS Windows hasta que el operador entregue esa ejecución.

## No autorizaciones

No se toca C11-C ni el manifiesto; no se modifica el binder, las políticas, los seeds de producción o el renderer. No se crea input de renderer, payload materializado ni media. `candidate_input_admissible=false`, `D4.8=BLOCKED`, `release_authority=NONE` siguen vigentes.
