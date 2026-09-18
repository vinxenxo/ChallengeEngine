$ErrorActionPreference = 'Stop'

$source = Join-Path $PSScriptRoot 'challenges\CHALLENGE_001.json'
$target = Join-Path $PSScriptRoot 'tests\fixtures\C7_VIDEO_ONLY_CHALLENGE_001.json'

if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
    throw "No existe el challenge fuente: $source"
}

$targetDir = Split-Path -Parent $target
if (-not (Test-Path -LiteralPath $targetDir -PathType Container)) {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
}

$data = Get-Content -LiteralPath $source -Raw -Encoding UTF8 | ConvertFrom-Json

# Preserve the complete validated C6 challenge structure.
# Only change identity/seed and explicitly remove any audio authoring block.
$data.challenge_id = 'CHALLENGE_VIDEO_OFF_001'

if ($null -eq $data.generation) {
    throw 'El challenge fuente no contiene generation.'
}
$data.generation.seed = 998877

# C7 video-only authority: no canonical_v2.audio.
if ($null -ne $data.canonical_v2) {
    $audioProperty = $data.canonical_v2.PSObject.Properties['audio']
    if ($null -ne $audioProperty) {
        $data.canonical_v2.PSObject.Properties.Remove('audio')
    }
}

# Defensive cleanup in case an older experimental fixture had a root audio block.
$rootAudioProperty = $data.PSObject.Properties['audio']
if ($null -ne $rootAudioProperty) {
    $data.PSObject.Properties.Remove('audio')
}

$json = $data | ConvertTo-Json -Depth 100
[System.IO.File]::WriteAllText($target, $json, [System.Text.UTF8Encoding]::new($false))

Write-Host "Fixture creado: $target"
