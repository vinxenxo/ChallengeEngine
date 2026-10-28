# Playbook de ejecución y tests — C11-D en Windows PowerShell 5.1

Este documento recoge los patrones que ya han funcionado en el checkout y los fallos que se deben evitar. Usar bloques completos, por separado: preflight, tests y runtime. No mezclar apply y test.

## 1. Reglas no negociables

- Usar Windows PowerShell 5.1, no depender de funciones exclusivas de PowerShell 7.
- Envolver bloques críticos en `& { ... }`, establecer `$ErrorActionPreference = 'Stop'` y usar rutas explícitas.
- No usar `&&`, `Read-Host`, `ForEach-Object -Parallel`, ni sintaxis PS7.
- No confiar en el valor histórico de `$?` después de otras líneas; para procesos externos usar `Start-Process -Wait -PassThru` y comprobar `$Process.ExitCode`.
- Separar stdout y stderr en ficheros distintos, imprimir hashes y conservar los logs si algo falla.
- No ejecutar otra vez una matriz/runtime tras un error sin diagnosticar la primera causa. No borrar logs ni carpetas temporales con evidencia.
- Al terminar un `Start-Process`, validar tanto el exit code como los marcadores requeridos y el contenido reportado. Un exit code cero por sí solo no es aceptación.
- No convertir una prueba estática en una afirmación de runtime PASS.

## 2. Identidad del checkout y del manifiesto C11-C

Antes de tocar fuentes de autoridad, validar la copia activa del manifiesto congelado. No copiar el manifiesto extraído de un ZIP al checkout. El ZIP de contexto generado por `c11c-suite` tiene su propia identidad/fingerprint; esa huella no es el hash del manifiesto canónico del árbol vivo.

```powershell
& {
    $ErrorActionPreference = 'Stop'
    Set-Location 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'

    $Manifest = Join-Path (Get-Location).Path 'release\C11C_FREEZE_PACKAGE_MANIFEST.json'
    if (-not (Test-Path -LiteralPath $Manifest -PathType Leaf)) {
        throw ('No existe el manifiesto C11-C: ' + $Manifest)
    }

    $Hash = (Get-FileHash -LiteralPath $Manifest -Algorithm SHA256).Hash.ToLowerInvariant()
    $Size = (Get-Item -LiteralPath $Manifest).Length
    Write-Host ('FROZEN_C11C_MANIFEST_SHA256=' + $Hash)
    Write-Host ('FROZEN_C11C_MANIFEST_SIZE=' + $Size)

    if ($Hash -ne 'e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953') {
        throw 'El manifiesto canónico del checkout no coincide. STOP; no restaurarlo desde el ZIP.'
    }
    if ($Size -ne 796318) {
        throw 'El tamaño del manifiesto canónico no coincide. STOP; no restaurarlo desde el ZIP.'
    }
    Write-Host 'FROZEN_C11C_MANIFEST=PASS'
}
```

## 3. Probe de versión Python para PowerShell 5.1

No recrear el probe inline con `py.exe -3.13 -c '...'`: ya falló en este entorno con `File "<string>", line 1` durante el paso de argumentos. Para preflight usar `py.exe -3.13 --version` y comprobar el exit code inmediatamente. El texto válido puede llegar como `3.13.14` o `Python 3.13.14`; hay que retirar el prefijo no numérico y validar `major.minor`, no comparar la cadena original literalmente. La corrección Phase P ya incorporó una normalización y pasó 5/5 casos.

Bloque de diagnóstico independiente:

```powershell
& {
    $ErrorActionPreference = 'Stop'
    $PythonLauncher = (Get-Command 'py.exe' -ErrorAction Stop).Source
    $VersionOutput = (& $PythonLauncher -3.13 --version 2>&1 | Out-String).Trim()
    $VersionExit = $LASTEXITCODE
    Write-Host ('PYTHON_313_VERSION_TEXT=' + $VersionOutput)
    Write-Host ('PYTHON_313_VERSION_EXIT=' + $VersionExit)
    if ($VersionExit -ne 0) {
        throw ('PYTHON_313_PREFLIGHT=FAIL | ' + $VersionOutput)
    }

    $NormalizedVersion = ($VersionOutput -replace '^[^\d]*', '').Trim()
    $Parts = $NormalizedVersion.Split('.')
    if ($Parts.Length -lt 2 -or $Parts[0] -ne '3' -or $Parts[1] -ne '13') {
        throw ('PYTHON_313_PREFLIGHT=FAIL | version=' + $VersionOutput)
    }
    Write-Host ('PYTHON_313_PREFLIGHT=PASS | ' + $VersionOutput)
}
```

## 4. Suite estática Phase P (ya pasó 30/30; volver a ejecutar solo si fuente/input cambió o el gate lo exige)

```powershell
& {
    $ErrorActionPreference = 'Stop'
    Set-Location 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'

    $PythonLauncher = (Get-Command 'py.exe' -ErrorAction Stop).Source
    $TestPath = Join-Path (Get-Location).Path 'tools\c11d\d9\test_d_renderer_phase_p_source_value_frame_value_provenance_20261028.py'
    if (-not (Test-Path -LiteralPath $TestPath -PathType Leaf)) {
        throw ('No existe el test Phase P: ' + $TestPath)
    }

    $LogRoot = Join-Path $env:TEMP ('C11D_PHASE_P_STATIC_TESTS_20261028_' + [Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $LogRoot | Out-Null
    $Stdout = Join-Path $LogRoot 'tests.stdout.txt'
    $Stderr = Join-Path $LogRoot 'tests.stderr.txt'
    $Arguments = '-3.13 "' + $TestPath + '"'

    $Process = Start-Process -FilePath $PythonLauncher -ArgumentList $Arguments -WorkingDirectory (Get-Location).Path -RedirectStandardOutput $Stdout -RedirectStandardError $Stderr -Wait -PassThru -NoNewWindow
    $OutText = [System.IO.File]::ReadAllText($Stdout)
    $ErrText = [System.IO.File]::ReadAllText($Stderr)
    Write-Host $OutText
    Write-Host $ErrText
    Write-Host ('TEST_EXIT_CODE=' + $Process.ExitCode)
    Write-Host ('TEST_STDOUT_SHA256=' + (Get-FileHash -LiteralPath $Stdout -Algorithm SHA256).Hash.ToLowerInvariant())
    Write-Host ('TEST_STDERR_SHA256=' + (Get-FileHash -LiteralPath $Stderr -Algorithm SHA256).Hash.ToLowerInvariant())
    Write-Host ('TEST_LOG_DIR=' + $LogRoot)

    if ($Process.ExitCode -ne 0 -or $OutText -notmatch 'Ran 30 tests' -or $OutText -notmatch '(?m)^OK\s*$') {
        throw 'PHASE_P_STATIC_TESTS=FAIL. No ejecutar runtime.'
    }
    if ($ErrText.Trim().Length -gt 0) {
        throw 'PHASE_P_STATIC_TESTS=FAIL: stderr no vacío. Conservar logs e investigar.'
    }
    Write-Host 'PHASE_P_STATIC_TESTS=PASS | 30/30'
}
```

## 5. Phase P runtime — siguiente ejecución, no aceptada todavía

Ejecutar el runner actual solo después de confirmar que la identidad del checkout, el preflight Python y los tests estáticos son correctos. El runner ya tiene SHA-256 esperado `77644d982ed0f552d58561ba05eb4969a76c90703bbb8745dbf73d1bafa3e327` tras la normalización.

```powershell
& {
    $ErrorActionPreference = 'Stop'
    Set-Location 'C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS'

    $Runner = Join-Path (Get-Location).Path 'tools\c11d\d9\run_d_renderer_phase_p_source_value_frame_value_provenance_20261028.ps1'
    if (-not (Test-Path -LiteralPath $Runner -PathType Leaf)) { throw ('No existe runner: ' + $Runner) }
    $RunnerHash = (Get-FileHash -LiteralPath $Runner -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Host ('PHASE_P_RUNNER_SHA256=' + $RunnerHash)
    if ($RunnerHash -ne '77644d982ed0f552d58561ba05eb4969a76c90703bbb8745dbf73d1bafa3e327') {
        throw 'El runner ha cambiado desde la normalización aceptada. No ejecutar: inspeccionar diferencia y actualizar pins por un gate separado.'
    }

    # Única invocación. No envuelvas en un segundo retry automático.
    & $Runner
    if (-not $?) {
        throw 'Phase P runtime runner no terminó satisfactoriamente; conservar toda la evidencia y diagnosticar antes de reintentar.'
    }
}
```

Si `$Runner` lanza excepción antes de volver, el bloque termina por `$ErrorActionPreference='Stop'`; no hace falta que la línea `$?` actúe como mecanismo de control de excepciones. La salida de la consola y las carpetas `%TEMP%` creadas por el runner deben conservarse. En caso de fallo, no volver a ejecutar antes de identificar si el fallo provino del preflight, pin check, planner, proceso Godot, comparación de hashes o validador final.

Después de la primera ejecución del runner, capturar y documentar el marcador final exacto producido por la versión actual, `ExitCode`, report/receipt SHA-256, hashes de stdout/stderr y conteo de procesos y ficheros de evidencia. No inventar el marcador antes de observarlo.

## 6. Patrones que causaron fallos históricos

- Un `apply` que espera una expresión anterior exacta puede fallar tras corregirse el texto del preflight. No forzar el parche: inspeccionar el preflight actual y preparar una reparación que pinte la versión real.
- Un proceso puede mostrar errores PowerShell incluso cuando el texto contiene una salida parcial. Comprobar el ExitCode y el resultado del runner, no el último `$?` después de `Write-Host`/`Get-Content`.
- `stdout` y `stderr` vacíos no demuestran éxito por sí solos; revisar el proceso, el estado de reporte y el marcador.
- Aceptadores deben verificar la evidencia ya producida, no repetir una matriz completa. Si el problema es de postcondición/write-back con evidencia PASS, reparar el aceptador para leer la estructura real; no volver a ejecutar Godot sin necesidad.
- No actualizar checkpoints/ledgers a PASS si el runner se detuvo antes del marcador final o si los hashes no corresponden.
