# C11-E — higiene de ejecución y registro preventivo de errores (V5)

Este registro es obligatorio antes de preparar paquetes, instaladores, runners o instrucciones Windows. Cada incidente requiere una prevención técnica verificable.

## Controles obligatorios

1. Entregar un único ZIP autocontenido con overlay, installer, runner, README, manifest y hashes. No asumir que archivos creados aquí aparecen en Downloads.
2. Proporcionar nombre/ruta exactos y una única secuencia pegable.
3. Target Windows PowerShell 5.1. Evitar `$Name:`; usar `-f`/`${Name}`. Mantener `if/elseif/else` en el mismo bloque. Si el runtime no está disponible aquí, declarar el límite y hacer revisión estática explícita.
4. Capturar `$LASTEXITCODE` inmediatamente después de cada proceso; abortar ante fallo. No ejecutar verificación/render tras instalación fallida y no imprimir PASS fuera de la rama de éxito.
5. Distinguir preimages de instalador y postimages de verificador. Validar todos los destinos y sources antes del primer write.
6. Verificar hash y CRC del ZIP, miembros, dependencias y rutas internas. Usar nombres de artefacto exactos.
7. Preservar `main`, refs, commits y C11-C manifest. Verificar HEAD/padre y árbol limpio esperados; ningún reset/checkout/commit/push automático.
8. Separar gobernanza D histórica y E. No revertir AGENTS/CONTINUE E para satisfacer el evaluador D.
9. Separar pruebas aisladas, Windows tests, contrato GUI, observación GUI, parse GDScript, Godot runtime, MP4, pixel comparisons y revisión humana.
10. No sobrescribir outputs. Reintentos usan RequestId nuevo; conservar la evidencia de cualquier fallo tras crear output root.
11. Pin de todas las fuentes que ejecuta el runner físico; recalcular hashes después de cualquier edición.
12. No afirmar render/media/pixel PASS sin logs Windows, exit code real, receipt, archivos y hashes.
13. `override.cfg`: cuarentena y restauración verificadas; nunca borrar/sobrescribir contenido diferente.
14. Calcular SHA de receipts sobre bytes reales y normalizar las rutas absolutas antes de compararlas.
15. Antes de sustituir instrucciones raíz, archivar exactamente sus preimages activos y verificarlos.
16. Resolver commits legítimos antes de construir paquetes; verificar exact HEAD, parent, diff, receipts y pins. Nunca aceptar cualquier descendiente automáticamente.
17. Texto manual en consola no es stdout del runner ni evidencia de PASS.
18. En guard de contención Windows, usar `GetFullPath`, `DirectorySeparatorChar` y un único separador al formar el prefijo raíz. No concatenar el literal PowerShell `'\'` para representar un carácter; en single quotes son dos backslashes.
19. Probar con casos positivos (ruta relativa normal) y negativos (`..`, rooted, UNC, symlink/reparse point) antes de publicar un installer.

## Incidentes

- E0 capture: `else` se pegó fuera del bloque `if`; siempre un bloque entero.
- E1 package V1: se asumió Downloads para artefactos que no se habían descargado; paquete autocontenido.
- E1 installer V1: interpolación PowerShell `$Relative:` inválida; usar `-f`.
- E1 verify V1: se ejecutó tras instalación fallida; fail-fast wrapper y pins de etapa correctos.
- Captura de pines: se compararon archivos de integración `c11c-suite` contra hashes brutos C sin aplicar la clasificación D; usar el evaluador/contrato adecuado, nunca inferir drift protegido de esa comparación aislada.
- E2 V2: HEAD `bc8330e` obsoleto después del commit legítimo `a3c7c5d`; reconciliar exact commit/parent/receipts antes del paquete.
- E2 V3: `TrimEnd('\') + '\'` construyó un prefijo de dos separadores y rechazó `c11c-suite/c11c-producer/main.py`; V4 usa `DirectorySeparatorChar` exactamente una vez y normaliza con `GetFullPath`.
- E2 consola: el usuario escribió manualmente un texto PASS tras exit code 1; no tratarlo como salida del runner.
- E2 runtime no disponible en entorno de preparación: no declarar PowerShell/Godot parse o render PASS sin evidencia del Windows activo.

## Checklist de publicación

Confirmar el commit activo y sus receipts; escanear strings PowerShell y llamadas `if/else`; comprobar el guard de ruta con positivos/negativos; enumerar miembros; ejecutar CRC; hash del paquete; validar todos los preimages; entregar solo un runner; capturar exit code y nunca imprimir PASS en fallo.
