# C11-E E4C V2.3 R5 — instalación y recuperación

## Causa corregida

El campo `intent_sha256` del intent E1 no es el SHA-256 de los bytes JSON en disco. Es el digest canónico obtenido con JSON UTF-8, claves ordenadas, separadores compactos `(',', ':')` y sin el campo `intent_sha256`. Para esta evidencia: digest canónico `9dfe5c1c4568ed7fbc4bb4260d47da4e518b1a163811fb88f2a9f1bff55c304e`; digest de fichero crudo `dfc861764302d7a6dec71de4532828dfe146708ed33dd2483b9c611bdd2f9a94`. La suite y el wrapper validan ambos valores por separado y el recibo E1 debe enlazar al digest canónico.

## Instalar

Extraer el ZIP a un directorio nuevo y ejecutar `INSTALL_C11E_E4C_V2_3_R5_INTENT_HASH_RECOVERY.ps1` con `-ProjectRoot`, `-PythonExe` y `-PackageZip`. El instalador valida Windows PowerShell 5.1, ZIP/manifest/package file hashes, 21 source pins, frozen C11-C, PowerShell AST, Python 3.13, py_compile, 17 pruebas focalizadas, File.Replace forward/rollback, paths e immediate recheck. Aplica 2 REPLACE +15 ADD_ONLY, transacción con journal y backup de las dos preimágenes.

Toda la documentación y los prompts Master/Start/First van como ADD_ONLY dentro del mismo instalador. No instalar documentos por separado ni extraer documentación manualmente al checkout.

## Auditar

Ejecutar `VERIFY_C11E_E4C_V2_3_R5_INSTALL_V1.ps1` con el RunId que emite el instalador. Debe verificar 17 operaciones, 2 backups, 21 pins, freeze C11-C y decision-record inmutable.

## Recuperar el output existente

Ejecutar desde el checkout: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\c11d\d9\RUN_C11E_E4C_V2_3_R5_EXISTING_OUTPUT_RECOVERY.ps1`. El wrapper valida el SHA crudo del `e1_intent.json`, el helper verifica también el SHA canónico y el binding del recibo; después comprueba el plan, silent intermediate, tres MP4 y source pins, FFprobe y elementary stream hashes. Solo extrae 7 PNG con `-fps_mode passthrough` y crea `E4C_DRILL_V2_REQUALIFICATION_RECEIPT.json`, auditoría y `E4C_V2_OPERATOR_REVIEW_BUNDLE.zip`.

La recuperación no recompone frames, no vuelve a muxar, no genera música, no ejecuta CLI/GUI/Godot/native capture. Ante error crea ZIP diagnóstico con logs, snapshot de output y source evidence. No reintentar a ciegas; revisar el ZIP generado.

## Aceptación / roadmap

El status técnico es `PASS_V2_TECHNICAL_REQUALIFICATION_PENDING_OPERATOR_VISUAL_AUDIO_ACCEPTANCE`. La revisión humana de siete frames y tres MP4 A/B/C es obligatoria. Selector actual `tracking/tier-1` sigue 0/20 hasta aceptación. Después 19 selectores restantes, E4C 20/20, E5, E6 Smoke18, E7 Matrix101 y E8. `E1=PREPARE_ONLY`, `family_adapter=NOT_CONNECTED_E1`, `production_dispatch=FALSE`, `release_authority=NONE`.
