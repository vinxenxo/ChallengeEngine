# ============================================================
#  Crear ZIP excluyendo archivos/directorios (estilo .gitignore)
# ============================================================
$source   = (Get-Location).Path
$zipName  = (Split-Path $source -Leaf) + ".zip"
$zipPath  = Join-Path (Split-Path $source -Parent) $zipName

# --- Directorios excluidos por NOMBRE (en cualquier nivel) ---
$excludeDirNames = @(
    '.vscode','.idea',
    '.godot','.mono','.import',
    '__pycache__',
    '.pytest_cache','.mypy_cache','.ruff_cache',
    '.venv','venv','env',
    '.git','.githooks'
)

# --- Directorios excluidos por RUTA relativa ---
$excludeDirPaths = @('artifacts/scratch')

# --- Archivos excluidos por nombre/patrón (en cualquier nivel) ---
$excludeFilePatterns = @(
    '.DS_Store','Thumbs.db','Desktop.ini',
    '*.uid','*.import',
    'export.cfg','export_credentials.cfg',
    'mono_crash.*.json',
    '*.translation',
    '*.pyc','*.pyo','*.pyd','*.py[cod]',
    '.env','*.local',
    '*.tmp','*.temp','*.swp','*.swo','*~','*.bak','*.old','*.orig',
    'crash*.log',
    'ConsoleHost_history.txt',
    '*.zip','*.7z','*.rar'
)

# --- Extensiones excluidas SOLO bajo artifacts/ ---
$artifactExtensions = @('.avi','.mp4','.gif','.pcm','.wav','.png','.jpg','.jpeg','.webp')
$artifactDirNames   = @('frames','avi','mp4','gif','media','videos')

# ------------------------------------------------------------
# 1) Recolectar archivos aplicando filtros
# ------------------------------------------------------------
$files = Get-ChildItem -Path $source -Recurse -File -Force | Where-Object {
    $rel  = $_.FullName.Substring($source.Length + 1).Replace('\','/')
    $parts = $rel.Split('/')
    $name  = $_.Name

    # a) Directorio prohibido por nombre
    foreach ($d in $excludeDirNames) {
        if ($parts -contains $d) { return $false }
    }

    # b) Directorio prohibido por ruta exacta o prefijo
    foreach ($p in $excludeDirPaths) {
        if ($rel -eq $p -or $rel -like "$p/*") { return $false }
    }

    # c) .env.* permitiendo .env.example
    if ($name -eq '.env' -or ($name -like '.env.*' -and $name -ne '.env.example')) {
        return $false
    }

    # d) Patrones de archivo generales
    foreach ($pat in $excludeFilePatterns) {
        if ($name -like $pat) { return $false }
    }

    # e) Reglas específicas de artifacts/
    if ($rel -like 'artifacts/*') {
        foreach ($d in $artifactDirNames) {
            if ($parts -contains $d) { return $false }
        }
        $ext = [System.IO.Path]::GetExtension($name).ToLower()
        if ($artifactExtensions -contains $ext) { return $false }
    }

    return $true
}

# ------------------------------------------------------------
# 2) Crear el ZIP
# ------------------------------------------------------------
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$zip = [System.IO.Compression.ZipFile]::Open($zipPath, 'Create')
try {
    foreach ($f in $files) {
        $entryName = $f.FullName.Substring($source.Length + 1).Replace('\','/')
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
            $zip, $f.FullName, $entryName
        ) | Out-Null
    }
} finally {
    $zip.Dispose()
}

Write-Host ""
Write-Host "ZIP creado: $zipPath"      -ForegroundColor Green
Write-Host "Archivos incluidos: $($files.Count)" -ForegroundColor Green