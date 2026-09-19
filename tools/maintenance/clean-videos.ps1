<#
.SYNOPSIS
Elimina archivos .mp4 y .avi (incluye raw.avi) de la carpeta actual y subcarpetas.

.DESCRIPTION
Usa la carpeta donde se ejecuta el script como punto de partida.
No requiere parámetros. Por seguridad, admite -WhatIf para simular.

.EXAMPLE
.\EliminarVideos.ps1 -WhatIf
.\EliminarVideos.ps1
#>
param(
    [switch]$WhatIf
)

# Carpeta donde se ejecuta el script (no donde está guardado el .ps1)
$Ruta = (Get-Location).Path

Write-Host "Carpeta de trabajo: $Ruta" -ForegroundColor Cyan

if (-not (Test-Path -LiteralPath $Ruta -PathType Container)) {
    Write-Error "La ruta no existe o no es una carpeta: $Ruta"
    exit 1
}

# Buscar .mp4 y .avi en la carpeta actual y subcarpetas
$archivos = Get-ChildItem -LiteralPath $Ruta -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Extension -in '.mp4', '.avi' -or $_.Name -eq 'raw.avi'
    }

if (-not $archivos -or $archivos.Count -eq 0) {
    Write-Host "No se encontraron archivos .mp4, .avi o raw.avi en: $Ruta"
    exit 0
}

Write-Host "Se encontraron $($archivos.Count) archivo(s) para eliminar.`n"

foreach ($archivo in $archivos) {
    if ($WhatIf) {
        Write-Host "[WhatIf] Se eliminaría: $($archivo.FullName)" -ForegroundColor Yellow
    } else {
        try {
            Remove-Item -LiteralPath $archivo.FullName -Force -ErrorAction Stop
            Write-Host "Eliminado: $($archivo.FullName)" -ForegroundColor Green
        } catch {
            Write-Warning "Error al eliminar $($archivo.FullName): $($_.Exception.Message)"
        }
    }
}

if ($WhatIf) {
    Write-Host "`nModo WhatIf: no se eliminó ningún archivo. Ejecuta sin -WhatIf para borrar de verdad." -ForegroundColor Cyan
}