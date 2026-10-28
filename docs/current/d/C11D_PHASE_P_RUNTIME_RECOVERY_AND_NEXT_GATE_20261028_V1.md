# Phase P — recuperación del probe y puerta runtime siguiente

**Estado:** `STATIC_PASS_30_OF_30; RUNTIME_PENDING`. Este registro captura la secuencia de recuperación y define una sola próxima acción; no es un registro de aceptación de runtime.

## Secuencia registrada

1. El primer runner de Phase P no alcanzó la auditoría runtime: `py.exe : File "<string>", line 1`. No consta un runtime PASS ni debe interpretarse el error del preflight como fallo de semántica de los seis candidatos.
2. Un overlay intermedio de aislamiento V3 fue rechazado por la comprobación de precondición: “El preflight Python 3.13 esperado no está presente”. La aplicación fue cerrada sin ejecutar tests runtime. No volver a aplicar ese V3 contra una fuente diferente.
3. Se aplicó el overlay `C11D_PHASE_P_PYTHON_VERSION_NORMALIZATION_FIX_20261028_V1.zip`. El runner cambió desde SHA `e9a6bb83b5de353c30288c6d5215419f6a2488340c08c5289798d2c3c9cc2a97` a `77644d982ed0f552d58561ba05eb4969a76c90703bbb8745dbf73d1bafa3e327`. El postcheck informó `PHASE_P_PYTHON_VERSION_NORMALIZATION_POSTCHECK=PASS`.
4. La prueba de normalización comprobó cinco entradas: `3.13.14`, `Python 3.13.14`, BOM + `3.13.14`, `Python 3.12.9` rechazado y `3.14.0` rechazado. Resultado 5/5 y normalización inmediatamente anterior a la validación.
5. El preflight real informó `PYTHON_313_PREFLIGHT=PASS | Python 3.13.14`.
6. La suite estática Phase P informó 30/30, exit code 0, stdout SHA `a32c904fad96c2068f689d39208029f50946ff73843e4d4055ac6dcc311e73e3`, stderr vacío SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Log directory `%TEMP%\C11D_PHASE_P_STATIC_TESTS_20261028_6c3212888d134707a4300d1354cbc009`.

## No más parches en cadena

El siguiente paso no es modificar más el script ni crear otro overlay de normalización. El siguiente paso es una sola ejecución real del runner ya fijado. La suite estática prueba la estructura/código, pero no reemplaza las ejecuciones Godot exigidas por el propio runner, sus pins antes/después ni las comparaciones independientes.

Si la ejecución falla, conservar la salida que generó. No repetirla sin identificar la primera condición fallida y comprobar si se trata de entorno, argumentos de proceso, pin drift, planner, runtime, hash de repetición o validación de evidencia. Nunca relajar un test para conseguir PASS.

## Requisitos mínimos de aceptación a verificar en el reporte real

- Exit code real del runner `0` y marcador de aceptación final único definido por el runner actual.
- Python 3.13.x detectado mediante probe compatible con PowerShell 5.1; no depender de inline `-c` con quoting frágil.
- Pins de entradas y fuentes antes y después intactos.
- Planner canónico seleccionado, seis selectores exactos y dos procesos independientes por selector como establece el contrato actual.
- Comparaciones de hash independientes: estabilidad de dos procesos no equivale a igualdad source-value/frame-value.
- Valores temporales acotados en memoria y solo hashes/tipo/presencia/resultado relacional en las evidencias; no volcar el diccionario completo.
- No renderer, media, payload materializado, proyecto fuente cambiado ni binding aprobado.
- Conservar stdout, stderr, informe, hashes de artefactos y ficheros de evidencia de proceso.

Después del runtime PASS, revisar contra el contrato V1/schema V1 y generar un artefacto de aceptación independiente con todos los hashes. No cambiar retrospectivamente el estado de pre-run del contrato; no aprobar bindings como subproducto de esta fase.
