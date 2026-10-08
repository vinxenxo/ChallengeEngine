Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-D8ProjectRoot {
    $root = (Get-Location).Path
    $root = (Resolve-Path -LiteralPath $root).Path
    if(-not (Test-Path -LiteralPath (Join-Path $root 'tools/c11d/d8') -PathType Container)){
        throw "Current location is not a ChallengeEngineV01_STATELESS project root: $root"
    }
    return $root
}

function Get-D8MediaExtensions {
    return @(
        '.mp4','.mov','.mkv','.webm','.avi','.wmv','.mxf','.gif',
        '.wav','.mp3','.m4a','.aac','.flac','.ogg','.opus','.pcm',
        '.aiff','.alac'
    )
}

function Get-D8MediaScopePath([string]$ProjectRoot) {
    return (Join-Path $ProjectRoot 'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json')
}

function Get-D8MediaScopeDeclaration([string]$ProjectRoot) {
    $path = Get-D8MediaScopePath $ProjectRoot
    if(-not (Test-Path -LiteralPath $path -PathType Leaf)){
        throw "Canonical D8 media scope not found: $path"
    }
    return (Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Resolve-D8MediaScope([string]$ProjectRoot) {
    $scope = Get-D8MediaScopeDeclaration $ProjectRoot
    if($scope.scope_mode -ne 'EXPLICIT_REGISTRY_ONLY'){
        throw "Unsupported D8 media scope mode: $($scope.scope_mode)"
    }
    $extensions = Get-D8MediaExtensions
    $resolved = @()
    foreach($item in @($scope.registry)) {
        $rel = ([string]$item.path).Replace('\','/').TrimStart('./')
        if([string]::IsNullOrWhiteSpace($rel)){ throw 'D8 media registry contains an empty path.' }
        $full = Join-Path $ProjectRoot ($rel -replace '/', '\')
        if(-not (Test-Path -LiteralPath $full -PathType Leaf)){ throw "D8 media registry target missing: $rel" }
        $resolvedPath = (Resolve-Path -LiteralPath $full).Path
        if(-not $resolvedPath.StartsWith($ProjectRoot,[System.StringComparison]::OrdinalIgnoreCase)){ throw "D8 media registry target escapes project root: $rel" }
        $ext=[System.IO.Path]::GetExtension($resolvedPath).ToLowerInvariant()
        if($extensions -notcontains $ext){ throw "D8 media registry target has unsupported extension: $rel" }
        $f=Get-Item -LiteralPath $resolvedPath -Force
        $resolved += [ordered]@{path=$rel;full_path=$resolvedPath;bytes=[int64]$f.Length;last_write_utc_ticks=$f.LastWriteTimeUtc.Ticks;extension=$ext}
    }
    return @($resolved | Sort-Object path)
}
