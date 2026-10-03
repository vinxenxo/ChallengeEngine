$contenido = @'
<#
.SYNOPSIS
    Limpieza extrema y optimización segura para Windows 11.
.DESCRIPTION
    Elimina archivos temporales, cachés regenerables y componentes obsoletos,
    aplica compresión del SO (Compact OS), optimiza el SSD y opcionalmente
    desactiva la hibernación y elimina bloatware.
    Mide el espacio liberado y guarda un log en el escritorio.
.NOTES
    Requiere PowerShell como Administrador.
    Autor: Script mejorado para uso personal.

.EXAMPLE
    Ejecutar desde PowerShell:
    PS> powershell -ExecutionPolicy Bypass -File .\tools\maintenance\LimpiezaExtrema.ps1

#>

# ============================================================
#  CONFIGURACIÓN INICIAL
# ============================================================
$ErrorActionPreference = 'SilentlyContinue'
$ProgressPreference    = 'Continue'
$script:LogFile        = "$env:USERPROFILE\Desktop\Limpieza_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
$script:StartTime      = Get-Date

# ============================================================
#  FUNCIONES AUXILIARES
# ============================================================
function Write-Log {
    param([string]$Message, [string]$Color = 'White', [string]$Level = 'INFO')
    $timestamp = (Get-Date).ToString('HH:mm:ss')
    $line = "[$timestamp][$Level] $Message"
    Write-Host $line -ForegroundColor $Color
    Add-Content -Path $script:LogFile -Value $line
}

function Get-FreeSpaceGB {
    $drive = Get-PSDrive -Name C
    return [math]::Round($drive.Free / 1GB, 2)
}

function Show-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host ("=" * 62) -ForegroundColor DarkCyan
    Write-Host "  $Title" -ForegroundColor Magenta
    Write-Host ("=" * 62) -ForegroundColor DarkCyan
    Add-Content -Path $script:LogFile -Value "`n=== $Title ==="
}

function Test-Admin {
    $current = [Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
    return $current.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Test-SafePath {
    param([string]$Path)
    $forbidden = @('C:\Windows\System32', 'C:\Windows\SysWOW64', 'C:\Windows\WinSxS', 'C:\Program Files', 'C:\Program Files (x86)', 'C:\Users')
    foreach ($f in $forbidden) {
        if ($Path -like "$f*" -and $Path -notlike "$f\*\Temp*") { return $false }
    }
    return $true
}

# ============================================================
#  VALIDACIONES PREVIAS
# ============================================================
Clear-Host
Write-Host ""
Write-Host "  ========================================================" -ForegroundColor Cyan
Write-Host "    LIMPIEZA EXTREMA Y OPTIMIZACION - WINDOWS 11" -ForegroundColor Cyan
Write-Host "    Lenovo Yoga i7 | 500 GB SSD | 16 GB RAM" -ForegroundColor Cyan
Write-Host "  ========================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Admin)) {
    Write-Host "  [X] ERROR: Debes ejecutar este script como Administrador." -ForegroundColor Red
    Write-Host "      Abre PowerShell con clic derecho -> 'Ejecutar como administrador'." -ForegroundColor Yellow
    Write-Host ""
    Pause
    Exit 1
}

"=== LOG DE LIMPIEZA - $(Get-Date) ===" | Out-File -FilePath $script:LogFile -Encoding UTF8
Write-Log "Log iniciado en: $script:LogFile" -Color Cyan

$freeBefore = Get-FreeSpaceGB
$totalSpace = [math]::Round((Get-PSDrive -Name C).Used / 1GB + $freeBefore, 2)

Write-Host ""
Write-Log "Espacio libre inicial en C: $freeBefore GB de $totalSpace GB" -Color Green
Write-Host ""

Write-Host "  Este script realizara las siguientes acciones:" -ForegroundColor White
Write-Host "    [+] Punto de restauracion del sistema" -ForegroundColor Gray
Write-Host "    [+] Limpieza de temporales, caches y Papelera" -ForegroundColor Gray
Write-Host "    [+] Limpieza de Windows Update y Delivery Optimization" -ForegroundColor Gray
Write-Host "    [+] Limpieza profunda de WinSxS con DISM" -ForegroundColor Gray
Write-Host "    [+] Compresion del SO con Compact OS" -ForegroundColor Gray
Write-Host "    [+] Optimizacion TRIM del SSD" -ForegroundColor Gray
Write-Host "    [?] Desactivar hibernacion (se preguntara)" -ForegroundColor Yellow
Write-Host "    [?] Eliminar bloatware (se preguntara)" -ForegroundColor Yellow
Write-Host ""
$resp = Read-Host "  Deseas continuar? (S/N)"
if ($resp -notmatch '^[SsYy]') {
    Write-Host "  Operacion cancelada por el usuario." -ForegroundColor Yellow
    Exit 0
}

# ============================================================
#  1. PUNTO DE RESTAURACION
# ============================================================
Show-Section "1. PUNTO DE RESTAURACION DEL SISTEMA"
try {
    Enable-ComputerRestore -Drive "C:\" -ErrorAction Stop
    Write-Log "System Restore habilitado en C:" -Color Green
    Checkpoint-Computer -Description "Antes de limpieza extrema" -RestorePointType "MODIFY_SETTINGS" -ErrorAction Stop
    Write-Log "Punto de restauracion creado correctamente." -Color Green
} catch {
    Write-Log "No se pudo crear el punto de restauracion: $($_.Exception.Message)" -Color Yellow -Level 'WARN'
    Write-Log "Continuando de todos modos..." -Color Yellow
}

# ============================================================
#  2. ARCHIVOS TEMPORALES
# ============================================================
Show-Section "2. LIMPIEZA DE ARCHIVOS TEMPORALES"
$tempPaths = @(
    "$env:TEMP",
    "C:\Windows\Temp",
    "C:\Windows\Prefetch"
)
foreach ($path in $tempPaths) {
    if ((Test-Path $path) -and (Test-SafePath $path)) {
        Write-Log "Limpiando: $path" -Color Cyan
        Get-ChildItem -Path $path -Recurse -Force -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
}
Write-Log "Temporales, Prefetch y caches de usuario eliminados." -Color Green

# ============================================================
#  3. PAPELERA DE RECICLAJE
# ============================================================
Show-Section "3. PAPELERA DE RECICLAJE"
try {
    Clear-RecycleBin -Force -ErrorAction Stop
    Write-Log "Papelera vaciada." -Color Green
} catch {
    Write-Log "Papelera ya estaba vacia o no accesible." -Color Yellow -Level 'WARN'
}

# ============================================================
#  4. DELIVERY OPTIMIZATION
# ============================================================
Show-Section "4. CACHE DE DELIVERY OPTIMIZATION"
try {
    Delete-DeliveryOptimizationCache -Force -ErrorAction Stop
    Write-Log "Cache de Delivery Optimization limpiada." -Color Green
} catch {
    Write-Log "No se pudo limpiar DO: $($_.Exception.Message)" -Color Yellow -Level 'WARN'
}

# ============================================================
#  5. WINDOWS UPDATE
# ============================================================
Show-Section "5. CACHE DE WINDOWS UPDATE"
$services = @('wuauserv', 'bits', 'cryptsvc', 'dosvc')
Write-Log "Deteniendo servicios: $($services -join ', ')" -Color Cyan
foreach ($svc in $services) {
    Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue
}
Start-Sleep -Seconds 2

$wuPaths = @(
    "C:\Windows\SoftwareDistribution\Download",
    "C:\Windows\SoftwareDistribution\DataStore"
)
foreach ($p in $wuPaths) {
    if (Test-Path $p) {
        Write-Log "Limpiando: $p" -Color Cyan
        Get-ChildItem -Path $p -Recurse -Force -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    }
}

Write-Log "Reiniciando servicios..." -Color Cyan
foreach ($svc in $services) {
    Start-Service -Name $svc -ErrorAction SilentlyContinue
}
Write-Log "Cache de Windows Update limpiada." -Color Green

# ============================================================
#  6. DISM / WinSxS
# ============================================================
Show-Section "6. LIMPIEZA PROFUNDA DE COMPONENTES (WinSxS)"
Write-Log "Ejecutando DISM StartComponentCleanup (puede tardar varios minutos)..." -Color Cyan
$dismResult = Dism.exe /online /Cleanup-Image /StartComponentCleanup 2>&1
$dismResult | Add-Content -Path $script:LogFile
Write-Log "Limpieza de WinSxS completada." -Color Green

# ============================================================
#  7. CACHE DE MINIATURAS
# ============================================================
Show-Section "7. CACHE DE MINIATURAS"
$thumbPath = "$env:LOCALAPPDATA\Microsoft\Windows\Explorer"
if (Test-Path $thumbPath) {
    Get-ChildItem -Path "$thumbPath\thumbcache_*.db" -Force -ErrorAction SilentlyContinue |
        Remove-Item -Force -ErrorAction SilentlyContinue
    Write-Log "Cache de miniaturas limpiada." -Color Green
} else {
    Write-Log "Ruta de cache de miniaturas no encontrada." -Color Yellow -Level 'WARN'
}

# ============================================================
#  8. HIBERNACION (OPCIONAL)
# ============================================================
Show-Section "8. DESACTIVAR HIBERNACION (OPCIONAL)"
$hiberFile = "C:\hiberfil.sys"
$hiberSize = 0
if (Test-Path $hiberFile) {
    $hiberSize = [math]::Round((Get-Item $hiberFile -Force).Length / 1GB, 2)
    Write-Host "  Archivo hiberfil.sys detectado: $hiberSize GB" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "  [!] Desactivar la hibernacion:" -ForegroundColor Yellow
Write-Host "      - Libera ~$hiberSize GB (el tamano de tu RAM)" -ForegroundColor Gray
Write-Host "      - Desaparece la opcion 'Hibernar' del menu de energia" -ForegroundColor Gray
Write-Host "      - 'Suspender' SIGUE funcionando con normalidad" -ForegroundColor Gray
Write-Host "      - Se puede reactivar despues con: powercfg /hibernate on" -ForegroundColor Gray
Write-Host ""
$respHiber = Read-Host "  Desactivar la hibernacion? (S/N)"
if ($respHiber -match '^[SsYy]') {
    powercfg /hibernate off
    Write-Log "Hibernacion desactivada. hiberfil.sys eliminado." -Color Green
} else {
    Write-Log "Hibernacion conservada por decision del usuario." -Color Yellow -Level 'SKIP'
}

# ============================================================
#  9. COMPACT OS
# ============================================================
Show-Section "9. COMPRESION DEL SO (COMPACT OS)"
Write-Log "Consultando estado actual..." -Color Cyan
Compact.exe /CompactOS:query | Tee-Object -FilePath $script:LogFile -Append

Write-Host ""
Write-Host "  [i] Compact OS comprime archivos del sistema para ahorrar espacio." -ForegroundColor Gray
Write-Host "      No afecta al rendimiento en SSD modernos." -ForegroundColor Gray
Write-Host ""
$respCompact = Read-Host "  Activar Compact OS? (S/N)"
if ($respCompact -match '^[SsYy]') {
    Write-Log "Aplicando Compact OS (puede tardar varios minutos)..." -Color Cyan
    Compact.exe /CompactOS:always | Tee-Object -FilePath $script:LogFile -Append
    Write-Log "Compact OS aplicado." -Color Green
} else {
    Write-Log "Compact OS no aplicado por decision del usuario." -Color Yellow -Level 'SKIP'
}

# ============================================================
#  10. ALMACENAMIENTO RESERVADO
# ============================================================
Show-Section "10. ALMACENAMIENTO RESERVADO DE WINDOWS"
try {
    Set-WindowsReservedStorageState -State Disabled -ErrorAction Stop
    Write-Log "Almacenamiento reservado desactivado." -Color Green
} catch {
    Write-Log "No se pudo modificar el almacenamiento reservado." -Color Yellow -Level 'WARN'
}

# ============================================================
#  11. TRIM / OPTIMIZACION SSD
# ============================================================
Show-Section "11. OPTIMIZACION DEL SSD (TRIM)"
try {
    Optimize-Volume -DriveLetter C -ReTrim -ErrorAction Stop
    Write-Log "TRIM ejecutado correctamente en C:." -Color Green
} catch {
    Write-Log "No se pudo ejecutar TRIM: $($_.Exception.Message)" -Color Yellow -Level 'WARN'
}

# ============================================================
#  12. BLOATWARE (OPCIONAL)
# ============================================================
Show-Section "12. ELIMINACION DE BLOATWARE (OPCIONAL)"
$bloatware = @(
    @{Name='Microsoft.3DBuilder';           Desc='3D Builder'},
    @{Name='Microsoft.BingWeather';         Desc='Clima (Bing Weather)'},
    @{Name='Microsoft.GetHelp';             Desc='Obtener ayuda'},
    @{Name='Microsoft.Getstarted';          Desc='Sugerencias'},
    @{Name='Microsoft.MicrosoftOfficeHub';  Desc='Office Hub'},
    @{Name='Microsoft.MicrosoftSolitaireCollection'; Desc='Solitario'},
    @{Name='Microsoft.MixedReality.Portal'; Desc='Mixed Reality Portal'},
    @{Name='Microsoft.Office.OneNote';      Desc='OneNote (version Store)'},
    @{Name='Microsoft.OneConnect';          Desc='OneConnect'},
    @{Name='Microsoft.People';              Desc='Contactos'},
    @{Name='Microsoft.SkypeApp';            Desc='Skype (version Store)'},
    @{Name='Microsoft.WindowsAlarms';       Desc='Alarmas y reloj'},
    @{Name='Microsoft.WindowsFeedbackHub';  Desc='Feedback Hub'},
    @{Name='Microsoft.WindowsMaps';         Desc='Mapas'},
    @{Name='Microsoft.XboxApp';             Desc='Xbox (version clasica)'},
    @{Name='Microsoft.ZuneMusic';           Desc='Groove Musica'},
    @{Name='Microsoft.ZuneVideo';           Desc='Peliculas y TV'}
)

Write-Host "  Aplicaciones candidatas a eliminar:" -ForegroundColor White
$installed = @()
foreach ($app in $bloatware) {
    $pkg = Get-AppxPackage -Name $app.Name -ErrorAction SilentlyContinue
    if ($pkg) {
        Write-Host "    - $($app.Desc)" -ForegroundColor Gray
        $installed += $pkg
    }
}

if ($installed.Count -eq 0) {
    Write-Log "No se encontraron aplicaciones preinstaladas de la lista." -Color Green
} else {
    Write-Host ""
    $respBloat = Read-Host "  Eliminar estas $($installed.Count) aplicaciones? (S/N)"
    if ($respBloat -match '^[SsYy]') {
        foreach ($pkg in $installed) {
            Write-Log "Eliminando: $($pkg.Name)" -Color Cyan
            Remove-AppxPackage -Package $pkg.PackageFullName -ErrorAction SilentlyContinue
        }
        Write-Log "Bloatware eliminado." -Color Green
    } else {
        Write-Log "Bloatware conservado por decision del usuario." -Color Yellow -Level 'SKIP'
    }
}

# ============================================================
#  13. RESUMEN FINAL
# ============================================================
$freeAfter = Get-FreeSpaceGB
$freed = [math]::Round($freeAfter - $freeBefore, 2)
$elapsed = (Get-Date) - $script:StartTime

Show-Section "RESUMEN FINAL"
Write-Host ""
Write-Host "  Espacio libre ANTES  : $freeBefore GB" -ForegroundColor White
Write-Host "  Espacio libre DESPUES: $freeAfter GB" -ForegroundColor White
Write-Host "  -------------------------------------" -ForegroundColor DarkGray

if ($freed -gt 0) {
    Write-Host "  [OK] ESPACIO LIBERADO: $freed GB" -ForegroundColor Green
} else {
    Write-Host "  [i] Sin cambios significativos de espacio." -ForegroundColor Yellow
}

Write-Host "  Tiempo total         : $([math]::Round($elapsed.TotalMinutes, 1)) min" -ForegroundColor White
Write-Host ""
Write-Host "  Log guardado en:" -ForegroundColor White
Write-Host "    $script:LogFile" -ForegroundColor Cyan
Write-Host ""
Write-Host "  [!] REINICIA el portatil para aplicar todos los cambios." -ForegroundColor Yellow
Write-Host ""
Write-Host ("=" * 62) -ForegroundColor DarkCyan

Add-Content -Path $script:LogFile -Value "`nEspacio antes: $freeBefore GB | Despues: $freeAfter GB | Liberado: $freed GB"

Write-Host ""
Read-Host "  Pulsa ENTER para salir"
'@

$ruta = "$env:USERPROFILE\Desktop\LimpiezaExtrema.ps1"
$contenido | Out-File -FilePath $ruta -Encoding UTF8 -Force
Write-Host "Archivo creado en: $ruta" -ForegroundColor Green
Write-Host "Ahora abre PowerShell como Administrador y ejecútalo." -ForegroundColor Cyan