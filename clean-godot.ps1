<#
.SYNOPSIS
    Limpia la cache de Godot y regenera automaticamente.

.DESCRIPTION
    Por defecto:
      - Borra TODA la cache: .godot, .uid, .import, .mono
      - Regenera la cache ejecutando Godot en modo headless
      - NO hace backup (usa -Backup para activarlo)

.PARAMETER Backup
    Activa el backup (ZIP) antes de borrar. Desactivado por defecto.

.PARAMETER ExcludeImport
    NO borra los archivos .import ni la carpeta .import.

.PARAMETER ExcludeMono
    NO borra la carpeta .mono.

.PARAMETER NoRegenerate
    NO regenera la cache con Godot al terminar.

.PARAMETER GodotPath
    Ruta al ejecutable de Godot. Por defecto: 'godot' (debe estar en PATH).

.PARAMETER DryRun
    Muestra que se eliminaria sin borrar nada.

.PARAMETER NoConfirm
    No pide confirmacion antes de borrar.

.EXAMPLE
    .\clean-godot.ps1
    Borra todo y regenera automaticamente. Sin backup, con confirmacion.

.EXAMPLE
    .\clean-godot.ps1 -Backup
    Igual que arriba pero con backup previo.

.EXAMPLE
    .\clean-godot.ps1 -ExcludeImport -ExcludeMono
    Borra solo .godot y .uid, conserva .import y .mono, y regenera.

.EXAMPLE
    .\clean-godot.ps1 -DryRun
    Simula sin borrar nada.
#>

param(
    [switch]$Backup,
    [switch]$ExcludeImport,
    [switch]$ExcludeMono,
    [switch]$NoRegenerate,
    [string]$GodotPath = "godot",
    [switch]$DryRun,
    [switch]$NoConfirm
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "====================================================" -ForegroundColor Magenta
Write-Host "        LIMPIADOR DE CACHE GODOT" -ForegroundColor Magenta
Write-Host "====================================================" -ForegroundColor Magenta
Write-Host ""

# Verificar que estamos en un proyecto de Godot
if (-not (Test-Path "project.godot")) {
    Write-Host "ADVERTENCIA: No se encontro 'project.godot' en esta carpeta." -ForegroundColor Yellow
    Write-Host "   Asegurate de ejecutar el script desde la raiz del proyecto." -ForegroundColor Yellow
    Write-Host ""
    if (-not $NoConfirm) {
        $resp = Read-Host "Continuar de todos modos? (s/n)"
        if ($resp -ne "s") { exit }
    }
}

if ($DryRun) {
    Write-Host "MODO SIMULACION (no se borrara nada)" -ForegroundColor Yellow
    Write-Host ""
}

# Mostrar configuracion
Write-Host "Configuracion:" -ForegroundColor Cyan
Write-Host "   Backup:          $(if ($Backup) { 'SI' } else { 'NO (usa -Backup para activar)' })" -ForegroundColor Gray
Write-Host "   Borrar .godot:   SI" -ForegroundColor Gray
Write-Host "   Borrar .uid:     SI" -ForegroundColor Gray
Write-Host "   Borrar .import:  $(if ($ExcludeImport) { 'NO (excluido)' } else { 'SI' })" -ForegroundColor Gray
Write-Host "   Borrar .mono:    $(if ($ExcludeMono) { 'NO (excluido)' } else { 'SI' })" -ForegroundColor Gray
Write-Host "   Regenerar:       $(if ($NoRegenerate) { 'NO' } else { 'SI (automatico)' })" -ForegroundColor Gray
Write-Host ""

# Confirmar
if (-not $NoConfirm -and -not $DryRun) {
    $resp = Read-Host "Continuar? (s/n)"
    if ($resp -ne "s") {
        Write-Host "Cancelado." -ForegroundColor Yellow
        exit
    }
    Write-Host ""
}

# ============================================
# 1. BACKUP (OPCIONAL)
# ============================================
if ($Backup -and -not $DryRun) {
    Write-Host "[1/5] Creando backup..." -ForegroundColor Cyan

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupDir = ".godot_backups"
    $backupFile = Join-Path $backupDir "backup_$timestamp.zip"

    if (-not (Test-Path $backupDir)) {
        New-Item -ItemType Directory -Path $backupDir | Out-Null
    }

    # Recopilar items a respaldar
    $itemsToBackup = @()
    if (Test-Path ".godot") { $itemsToBackup += ".godot" }
    if (-not $ExcludeImport -and (Test-Path ".import")) { $itemsToBackup += ".import" }
    if (-not $ExcludeMono -and (Test-Path ".mono")) { $itemsToBackup += ".mono" }

    $uidFiles = Get-ChildItem -Recurse -Filter "*.uid" -File -ErrorAction SilentlyContinue
    $importFiles = @()
    if (-not $ExcludeImport) {
        $importFiles = Get-ChildItem -Recurse -Filter "*.import" -File -ErrorAction SilentlyContinue
    }

    if ($itemsToBackup.Count -eq 0 -and $uidFiles.Count -eq 0 -and $importFiles.Count -eq 0) {
        Write-Host "   No hay nada para respaldar (nada que borrar)." -ForegroundColor Gray
    } else {
        $tempDir = Join-Path $env:TEMP "godot_backup_$timestamp"
        New-Item -ItemType Directory -Path $tempDir -Force | Out-Null

        foreach ($item in $itemsToBackup) {
            Copy-Item -Path $item -Destination $tempDir -Recurse -Force -ErrorAction SilentlyContinue
        }

        foreach ($f in $uidFiles) {
            $relPath = $f.FullName.Substring((Get-Location).Path.Length + 1)
            $destPath = Join-Path $tempDir $relPath
            $destDir = Split-Path $destPath -Parent
            if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
            Copy-Item -Path $f.FullName -Destination $destPath -Force
        }

        foreach ($f in $importFiles) {
            $relPath = $f.FullName.Substring((Get-Location).Path.Length + 1)
            $destPath = Join-Path $tempDir $relPath
            $destDir = Split-Path $destPath -Parent
            if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
            Copy-Item -Path $f.FullName -Destination $destPath -Force
        }

        try {
            Compress-Archive -Path "$tempDir\*" -DestinationPath $backupFile -Force
            Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue

            $backupSizeMB = [math]::Round((Get-Item $backupFile).Length / 1MB, 2)
            Write-Host "   OK - Backup creado: $backupFile ($backupSizeMB MB)" -ForegroundColor Green
        } catch {
            Write-Host "   ERROR al crear backup: $_" -ForegroundColor Red
            Write-Host "   Abortando por seguridad." -ForegroundColor Red
            exit 1
        }
    }
} else {
    if ($Backup) {
        Write-Host "[1/5] Backup: OMITIDO (modo simulacion)" -ForegroundColor DarkGray
    } else {
        Write-Host "[1/5] Backup: NO solicitado (usa -Backup para activar)" -ForegroundColor DarkGray
    }
}
Write-Host ""

# ============================================
# Funcion auxiliar para eliminar
# ============================================
function Remove-SafePath {
    param([string]$Path, [string]$Label)
    if (Test-Path $Path) {
        if ($DryRun) {
            Write-Host "   [SIMULACION] Se eliminaria: $Path" -ForegroundColor DarkYellow
        } else {
            Remove-Item -Path $Path -Recurse -Force -ErrorAction SilentlyContinue
            Write-Host "   OK - $Label eliminado: $Path" -ForegroundColor Green
        }
    } else {
        Write-Host "   No existe: $Path" -ForegroundColor Gray
    }
}

# ============================================
# 2. Carpeta .godot
# ============================================
Write-Host "[2/5] Carpeta .godot" -ForegroundColor Cyan
Remove-SafePath -Path ".godot" -Label "Carpeta .godot"
Write-Host ""

# ============================================
# 3. Archivos .uid
# ============================================
Write-Host "[3/5] Archivos .uid" -ForegroundColor Cyan
$uidFiles = Get-ChildItem -Recurse -Filter "*.uid" -File -ErrorAction SilentlyContinue
if ($uidFiles.Count -gt 0) {
    Write-Host "   Encontrados: $($uidFiles.Count) archivos" -ForegroundColor Yellow
    if ($DryRun) {
        $uidFiles | ForEach-Object { Write-Host "   [SIMULACION] $($_.FullName)" -ForegroundColor DarkYellow }
    } else {
        $uidFiles | Remove-Item -Force
        Write-Host "   OK - Eliminados: $($uidFiles.Count) archivos .uid" -ForegroundColor Green
    }
} else {
    Write-Host "   No se encontraron archivos .uid" -ForegroundColor Gray
}
Write-Host ""

# ============================================
# 4. Archivos .import y carpeta .mono
# ============================================
if (-not $ExcludeImport) {
    Write-Host "[4/5] Archivos .import" -ForegroundColor Cyan
    $importFiles = Get-ChildItem -Recurse -Filter "*.import" -File -ErrorAction SilentlyContinue
    if ($importFiles.Count -gt 0) {
        Write-Host "   Encontrados: $($importFiles.Count) archivos" -ForegroundColor Yellow
        if ($DryRun) {
            $importFiles | ForEach-Object { Write-Host "   [SIMULACION] $($_.FullName)" -ForegroundColor DarkYellow }
        } else {
            $importFiles | Remove-Item -Force
            Write-Host "   OK - Eliminados: $($importFiles.Count) archivos .import" -ForegroundColor Green
        }
    } else {
        Write-Host "   No se encontraron archivos .import" -ForegroundColor Gray
    }

    if (Test-Path ".import") {
        Remove-SafePath -Path ".import" -Label "Carpeta .import"
    }
} else {
    Write-Host "[4/5] Archivos .import: OMITIDO (-ExcludeImport)" -ForegroundColor DarkGray
}

if (-not $ExcludeMono) {
    Write-Host ""
    Write-Host "   Carpeta .mono:" -ForegroundColor Cyan
    Remove-SafePath -Path ".mono" -Label "Carpeta .mono"
} else {
    Write-Host "   Carpeta .mono: OMITIDO (-ExcludeMono)" -ForegroundColor DarkGray
}
Write-Host ""

# ============================================
# 5. REGENERAR CON GODOT (AUTOMATICO POR DEFECTO)
# ============================================
if (-not $NoRegenerate) {
    if ($DryRun) {
        Write-Host "[5/5] Regenerar: OMITIDO (modo simulacion)" -ForegroundColor DarkGray
        Write-Host "   [SIMULACION] Se ejecutaria: $GodotPath --headless --path . --editor --quit" -ForegroundColor DarkYellow
    } else {
        Write-Host "[5/5] Regenerando cache con Godot..." -ForegroundColor Cyan

        $godotCmd = Get-Command $GodotPath -ErrorAction SilentlyContinue
        if (-not $godotCmd) {
            Write-Host "   ERROR: No se encontro el ejecutable de Godot: '$GodotPath'" -ForegroundColor Red
            Write-Host "   Asegurate de que 'godot' este en PATH o usa -GodotPath 'C:\ruta\a\godot.exe'" -ForegroundColor Yellow
            Write-Host "   Saltando regeneracion." -ForegroundColor Yellow
        } else {
            Write-Host "   Ejecutando: $GodotPath --headless --path . --editor --quit" -ForegroundColor Gray
            Write-Host ""
            $startTime = Get-Date

            & $GodotPath --headless --path . --editor --quit

            $exitCode = $LASTEXITCODE
            $elapsed = [math]::Round(((Get-Date) - $startTime).TotalSeconds, 1)

            Write-Host ""
            if ($exitCode -eq 0) {
                Write-Host "   OK - Godot termino correctamente (${elapsed}s)" -ForegroundColor Green
            } else {
                Write-Host "   ADVERTENCIA: Godot salio con codigo $exitCode (${elapsed}s)" -ForegroundColor Yellow
            }
        }
    }
} else {
    Write-Host "[5/5] Regenerar: OMITIDO (-NoRegenerate)" -ForegroundColor DarkGray
}
Write-Host ""

# ============================================
# RESUMEN
# ============================================
Write-Host "====================================================" -ForegroundColor Green
if ($DryRun) {
    Write-Host "      SIMULACION COMPLETADA (nada borrado)" -ForegroundColor Yellow
} else {
    Write-Host "         LIMPIEZA COMPLETADA" -ForegroundColor Green
}
Write-Host "====================================================" -ForegroundColor Green
Write-Host ""

if (-not $NoRegenerate -and -not $DryRun) {
    Write-Host "Cache regenerada. Ya puedes abrir Godot normalmente." -ForegroundColor Cyan
} else {
    Write-Host "Abre Godot para regenerar la cache automaticamente." -ForegroundColor Cyan
    Write-Host "O ejecuta: godot --headless --path . --editor --quit" -ForegroundColor Gray
}
Write-Host ""