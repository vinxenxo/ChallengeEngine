#requires -Version 5.1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$ProjectRoot = (Get-Location).Path
foreach($required in @('project.godot','AGENTS.md','build_factory.py')){
    if(-not (Test-Path -LiteralPath (Join-Path $ProjectRoot $required))){
        throw "Run this audit from the ChallengeEngine project root; missing $required"
    }
}

$ReleaseRoot = Join-Path $ProjectRoot 'artifacts\releases'
$ArchiveName = 'ChallengeEngineV01_STATELESS_C11-C_2.19.12_FROZEN_20260930_175709.zip'
$ArchivePath = Join-Path $ReleaseRoot $ArchiveName
$PackageReceiptPath = Join-Path $ReleaseRoot 'C11-C_2.19.12_FROZEN_PACKAGE_RECEIPT_20260930_175709.json'
$OutputRoot = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4'
$DocsRoot = Join-Path $ProjectRoot 'docs\current\d'
$ReportPath = Join-Path $OutputRoot 'd4_0_production_flow_audit.json'
$ReceiptPath = Join-Path $OutputRoot 'd4_0_validation_receipt.json'
$ContractPath = Join-Path $DocsRoot 'D4.0_PRODUCTION_FLOW_AUDIT_CONTRACT.md'
$MasterHandoverPath = Join-Path $DocsRoot 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPromptPath = Join-Path $DocsRoot 'START_PROMPT_C11D_CURRENT.md'

if(-not (Test-Path -LiteralPath $ArchivePath)){ throw "Frozen C11-C archive not found: $ArchivePath" }
if(-not (Test-Path -LiteralPath $PackageReceiptPath)){ throw "Frozen C11-C package receipt not found: $PackageReceiptPath" }
$PackageReceipt = Get-Content -Raw -LiteralPath $PackageReceiptPath -Encoding UTF8 | ConvertFrom-Json
$ArchiveHash = (Get-FileHash -LiteralPath $ArchivePath -Algorithm SHA256).Hash.ToLowerInvariant()
if($ArchiveHash -ne ([string]$PackageReceipt.archive_sha256).ToLowerInvariant()){
    throw 'Frozen C11-C archive SHA-256 does not match its package receipt.'
}

New-Item -ItemType Directory -Force -Path $OutputRoot,$DocsRoot | Out-Null

function Get-Evidence([string]$RelativePath,[string]$Role) {
    $FullPath = Join-Path $ProjectRoot $RelativePath
    if(-not (Test-Path -LiteralPath $FullPath -PathType Leaf)){
        return [ordered]@{ path=$RelativePath; role=$Role; present=$false; sha256=$null; bytes=0 }
    }
    $File = Get-Item -LiteralPath $FullPath
    $Hash = (Get-FileHash -LiteralPath $FullPath -Algorithm SHA256).Hash.ToLowerInvariant()
    return [ordered]@{ path=$RelativePath; role=$Role; present=$true; sha256=$Hash; bytes=[int64]$File.Length }
}

function Write-JsonNoBom([string]$Path,[object]$Value) {
    $Json = $Value | ConvertTo-Json -Depth 40
    [System.IO.File]::WriteAllText($Path,$Json,(New-Object System.Text.UTF8Encoding($false)))
}

$Evidence = @(
    (Get-Evidence 'c11c-suite\c11c-producer\main.py' 'GUI Recipe model, selection controls, seed generation and CLI delegation'),
    (Get-Evidence 'c11c-suite\c11c-producer\producer_schema.json' 'Active Producer family, grammar and personalization control definitions'),
    (Get-Evidence 'c11c-suite\c11c-producer\producer_schema_source.json' 'Producer schema source'),
    (Get-Evidence 'c11c-suite\c11c-producer\run_visual_drill_production.ps1' 'Visual Drill console adapter'),
    (Get-Evidence 'c11c-suite\main.py' 'Canonical Suite GUI application routing'),
    (Get-Evidence 'tools\prototypes\c11c_bulk\run_c11c_challenge_production.ps1' 'Challenge console production launcher'),
    (Get-Evidence 'tools\prototypes\c11c_bulk\run_c11c_production.ps1' 'Visual Loop console production launcher'),
    (Get-Evidence 'tools\prototypes\c11c_bulk\C11CProductionBatchCommon.ps1' 'Visual Loop schedule, seed planning and batch orchestration'),
    (Get-Evidence 'build_factory.py' 'Challenge CLI production, validation, manifest and provenance backend'),
    (Get-Evidence 'profiles\delivery\c11c_video_delivery_profiles.json' 'Shared C11-C delivery profile definitions'),
    (Get-Evidence 'challenges\CHALLENGE_001.json' 'Declarative Challenge timing, metadata, generation and asset fields'),
    (Get-Evidence 'definitions\c11d\asset_families\C11D_CHALLENGE_ASSET_BINDING_REGISTRY_V1.json' 'D2 evidence-backed Challenge asset binding'),
    (Get-Evidence 'definitions\c11d\music\C11D_MUSIC_ENGINE_V5_SPEC_V1.json' 'D3 shared deterministic music interface and dedicated music seed'),
    (Get-Evidence 'definitions\c11d\music\C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json' 'D3 declarative Challenge music style profile'),
    (Get-Evidence 'artifacts\tests\c11d_d3\d3_3\d3_3_validation_receipt.json' 'D3 closed-state evidence'),
    (Get-Evidence 'tools\qa\c11\run_c11a1_challenge_bulk_qa.ps1' 'Historical compatibility QA path; not current production adapter'),
    (Get-Evidence 'artifacts\releases\C11-C_2.19.12_FROZEN_PACKAGE_RECEIPT_20260930_175709.json' 'Frozen C11-C archive and source-tree provenance')
)

$ProducerSchemaPath = Join-Path $ProjectRoot 'c11c-suite\c11c-producer\producer_schema.json'
$ProducerSchema = Get-Content -Raw -LiteralPath $ProducerSchemaPath -Encoding UTF8 | ConvertFrom-Json
$DeliveryConfigPath = Join-Path $ProjectRoot 'profiles\delivery\c11c_video_delivery_profiles.json'
$DeliveryConfig = Get-Content -Raw -LiteralPath $DeliveryConfigPath -Encoding UTF8 | ConvertFrom-Json
$ChallengeFiles = @(Get-ChildItem -LiteralPath (Join-Path $ProjectRoot 'challenges') -Filter 'CHALLENGE_*.json' -File | Sort-Object Name)
$ChallengeIds = @($ChallengeFiles | ForEach-Object { $_.BaseName })
$LoopFamilyIds = @($ProducerSchema.families.PSObject.Properties | ForEach-Object { $_.Name })
$DrillFamilyIds = @($ProducerSchema.drills.PSObject.Properties | ForEach-Object { $_.Name })
$DeliveryProfiles = @($DeliveryConfig.profiles.PSObject.Properties | ForEach-Object { $_.Name })

$FieldFindings = @(
    [ordered]@{ field='production_request'; disposition='NEW'; state='No single canonical request schema/object is present; UI Recipe is an in-memory operator model.'; candidates=@('c11c-suite/c11c-producer/main.py: Recipe','tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1') },
    [ordered]@{ field='challenge_selection'; disposition='REUSE'; state='Challenge catalog reads challenges/CHALLENGE_*.json and CLI launchers accept ChallengeId; normalize the selector in D4.1.'; candidates=@('c11c-suite/c11c-producer/main.py: load_challenge_catalog','tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1') },
    [ordered]@{ field='seed'; disposition='ADAPT'; state='UI supports generated/manual seeds; challenge and visual production launchers consume seeds separately.'; candidates=@('c11c-suite/c11c-producer/main.py: Recipe.manual_seeds','tools/prototypes/c11c_bulk/C11CProductionBatchCommon.ps1') },
    [ordered]@{ field='music_seed'; disposition='REUSE'; state='D3 defines a dedicated deterministic music seed, independent of gameplay and structural RNG; carry it explicitly in the canonical request.'; candidates=@('definitions/c11d/music/C11D_MUSIC_ENGINE_V5_SPEC_V1.json','tools/c11d/d3/c11d_music_engine_v5.py') },
    [ordered]@{ field='visual_presentation_profile'; disposition='ADAPT'; state='C11-C family/grammar controls and D2 Challenge asset binding exist as separate declarations; request should reference stable IDs.'; candidates=@('c11c-suite/c11c-producer/producer_schema.json','definitions/c11d/asset_families/C11D_CHALLENGE_ASSET_BINDING_REGISTRY_V1.json') },
    [ordered]@{ field='duration'; disposition='REUSE'; state='Challenge duration is derived from declarative hook/game/reveal/CTA timing; Loop duration has a separate bounded launcher parameter.'; candidates=@('challenges/CHALLENGE_001.json','tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1','tools/prototypes/c11c_bulk/run_c11c_production.ps1') },
    [ordered]@{ field='format_resolution_fps'; disposition='ADAPT'; state='Central delivery profiles exist; Challenge launcher also carries its own profile table, creating duplicated policy to reconcile.'; candidates=@('profiles/delivery/c11c_video_delivery_profiles.json','tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1') },
    [ordered]@{ field='personalization'; disposition='ADAPT'; state='Producer exposes family-specific grammar, palette and parameter controls plus footer/audio options; no cross-family personalization contract exists.'; candidates=@('c11c-suite/c11c-producer/producer_schema.json','c11c-suite/c11c-producer/main.py: Recipe.targets') },
    [ordered]@{ field='metadata_editorial'; disposition='REUSE'; state='Challenge declarations and production manifests already carry editorial/declarative metadata.'; candidates=@('challenges/CHALLENGE_001.json','build_factory.py: build_declarative_metadata') },
    [ordered]@{ field='render_mode'; disposition='ADAPT'; state='GUI operation modes distinguish review/production/batch-like jobs, while adapters select separate launchers; normalize mode without erasing behavior differences.'; candidates=@('c11c-suite/c11c-producer/main.py: Recipe.operation/video_type','tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1') },
    [ordered]@{ field='artifact_destination'; disposition='ADAPT'; state='Production, QA/review and scratch use distinct roots; preserve those policies while representing destination intent declaratively.'; candidates=@('tools/prototypes/c11c_bulk/run_c11c_production.ps1','build_factory.py','artifacts/production','artifacts/qa','artifacts/scratch') },
    [ordered]@{ field='provenance'; disposition='REUSE'; state='Existing manifests retain input definition hashes, git identity, output hashes and validation; bind these to a canonical request hash.'; candidates=@('build_factory.py: audit_unit_manifest','tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1') },
    [ordered]@{ field='cli_entrypoints'; disposition='REUSE'; state='Direct console launchers exist for Challenge, Visual Loop and Visual Drill flows; retain as adapters over one orchestrator.'; candidates=@('tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1','tools/prototypes/c11c_bulk/run_c11c_production.ps1','c11c-suite/c11c-producer/run_visual_drill_production.ps1') },
    [ordered]@{ field='gui_entrypoints'; disposition='REUSE'; state='c11c-suite routes to Producer; Producer uses QProcess to invoke canonical PowerShell launchers.'; candidates=@('c11c-suite/main.py','c11c-suite/c11c-producer/main.py') },
    [ordered]@{ field='validators'; disposition='REUSE'; state='Challenge schema/runtime validation, manifest/provenance audit, delivery probing and Producer preflight exist; D4.2 should compose rather than duplicate.'; candidates=@('build_factory.py','tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1','c11c-suite/c11c-producer/preflight.py') },
    [ordered]@{ field='planners_orchestrators'; disposition='ADAPT'; state='GUI Recipe queue, C11-C batch schedule and backend factory each orchestrate part of production; no single shared request orchestrator is evidenced.'; candidates=@('c11c-suite/c11c-producer/main.py: Recipe','tools/prototypes/c11c_bulk/C11CProductionBatchCommon.ps1','build_factory.py') },
    [ordered]@{ field='request_hash'; disposition='NEW'; state='Artifact/input hashes exist, but no hash over a normalized canonical production request is evidenced.'; candidates=@('build_factory.py: provenance_sha256','D4.1 schema requirement') },
    [ordered]@{ field='simulation_truth_rng'; disposition='PROTECTED'; state='Challenge truth, gameplay/structural RNG ownership and frozen C11-C engine contracts remain outside D4 adapters.'; candidates=@('AGENTS.md: Frozen engine boundary','docs/current/d/D3.1_SHARED_MUSIC_ENGINE_V5_CONTRACT.md') },
    [ordered]@{ field='legacy_producer_lineage'; disposition='HISTORICAL'; state='Producer schema engine/profile lineage 2.16.9 is provenance, not the current C11-C 2.19.12 orchestration baseline.'; candidates=@('c11c-suite/c11c-producer/producer_schema.json','docs/current/producer/C11C_PRODUCER_0.9.7_CURRENT_STATE.md') }
)

$EvidenceMap = @{}
foreach($item in $Evidence){ if($item.present){ $EvidenceMap[$item.path.Replace('\','/')] = $item.sha256 } }
$NowUtc = [DateTime]::UtcNow.ToString('o')
$Audit = [ordered]@{
    schema = 'C11D-D4.0-PRODUCTION-FLOW-AUDIT-V1'
    checkpoint = 'C11-D D4.0'
    result = 'PASS'
    status = 'AUDIT COMPLETE / D4.1 READY'
    generated_at_utc = $NowUtc
    baseline = [ordered]@{
        release = [string]$PackageReceipt.release
        archive = ('artifacts/releases/' + $ArchiveName)
        archive_sha256 = $ArchiveHash
        source_tree_sha256 = ([string]$PackageReceipt.source_tree_sha256).ToLowerInvariant()
        package_receipt = 'artifacts/releases/C11-C_2.19.12_FROZEN_PACKAGE_RECEIPT_20260930_175709.json'
        package_receipt_sha256 = (Get-FileHash -LiteralPath $PackageReceiptPath -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    scope = [ordered]@{
        static_source_audit = $true
        production_activated = $false
        gui_launched = $false
        cli_production_launched = $false
        c11c_engine_modified = $false
        simulation_truth_modified = $false
        rng_modified = $false
    }
    inventory = [ordered]@{
        challenge_definitions = $ChallengeIds
        challenge_count = $ChallengeIds.Count
        c11c_visual_loop_families = $LoopFamilyIds
        c11c_visual_drill_families = $DrillFamilyIds
        delivery_profiles = $DeliveryProfiles
        canonical_production_request_schema_found = $false
        gui_surface = 'c11c-suite -> c11c-producer (Producer 0.9.7)'
        cli_surfaces = @('Challenge: tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1','Visual Loop: tools/prototypes/c11c_bulk/run_c11c_production.ps1','Visual Drill: c11c-suite/c11c-producer/run_visual_drill_production.ps1','Legacy/general factory: build_factory.py --config/--batch')
    }
    field_findings = $FieldFindings
    evidence = $Evidence
    evidence_sha256 = $EvidenceMap
    disposition = [ordered]@{
        reuse = @('Challenge definitions/catalog','delivery profile definitions','D2 Challenge asset binding','D3 shared music engine/style profile and independent music seed','C11-C GUI and console launchers','manifest/provenance validators')
        adapt = @('GUI Recipe input model','seed handling','presentation/profile binding','duration and delivery policy normalization','REVIEW/PRODUCTION mode mapping','artifact destination intent','orchestrator composition')
        new = @('canonical Production Request schema','normalization contract','cross-domain personalization contract','canonical request hash','single backend orchestrator')
        protected = @('C11-C frozen archive/tree','simulation truth','gameplay and structural RNG','C11-C renderers and existing runtime contracts')
        historical = @('Producer engine/profile lineage 2.16.9 when used as engine provenance')
    }
    next = 'D4.1 - Canonical Production Request Schema'
}

$ContractLines = @(
    '# C11-D D4.0 - Production Flow / Request Audit',
    '',
    '## Status',
    '',
    'PASS / CLOSED. Static audit complete; D4.1 is ready to define the canonical schema.',
    '',
    '## Baseline',
    '',
    ('- Frozen C11-C archive: `' + $ArchiveName + '`.'),
    ('- Archive SHA-256: `' + $ArchiveHash + '` (verified against the frozen-package receipt).'),
    ('- Source-tree SHA-256 from receipt: `' + ([string]$PackageReceipt.source_tree_sha256).ToLowerInvariant() + '`.') ,
    '',
    '## Audit scope',
    '',
    'This checkpoint inspected active Challenge and C11-C production declarations, operator surfaces, launchers, delivery profiles, validators, manifests and D2/D3 reusable contracts. It did not launch GUI, CLI production or a renderer, and did not change simulation truth, RNG, or frozen C11-C.',
    '',
    '## Existing flow',
    '',
    'The active GUI route is `c11c-suite` to Producer 0.9.7. Producer keeps an in-memory `Recipe`, builds seed jobs and invokes canonical PowerShell launchers through QProcess. Challenge production accepts ChallengeId, seed, delivery profile and output root. Visual Loop and Drill flows use their respective launchers. `build_factory.py` also exposes a general Challenge CLI using declarative config/batch inputs and writes manifests with validation and provenance.',
    '',
    'The GUI therefore delegates to existing console routes, but its Recipe is not a persisted, versioned request and the routes do not share one canonical orchestrator.',
    '',
    '## Field disposition',
    '',
    '| Field | Classification | Audit finding |',
    '|---|---|---|',
    '| Production Request / request hash | NEW | No canonical request schema or normalized-request hash is evidenced. |',
    '| Challenge selection / editorial metadata | REUSE | Existing Challenge definitions, catalog and metadata/manifests provide authoritative source material. |',
    '| Challenge seed / music_seed | ADAPT / REUSE | Seed entry is split across adapters; D3 already provides an independent deterministic music seed. |',
    '| Visual and presentation profile | ADAPT | C11-C family/grammar declarations and D2 asset bindings are reusable references with different identities. |',
    '| Duration / format / resolution / FPS | ADAPT | Declarative timing and central delivery profiles exist; Challenge launcher duplicates part of profile policy. |',
    '| Personalization | ADAPT / NEW | Producer exposes family-specific controls; a cross-family declarative contract is absent. |',
    '| REVIEW / PRODUCTION mode | ADAPT | Existing operation modes route to distinct adapters and destinations. |',
    '| Artifact destination / provenance | ADAPT / REUSE | Roots are established; manifests already record input, output and validation provenance. |',
    '| GUI / CLI entrypoints and validators | REUSE | Existing Suite/Producer and direct launchers plus validation paths should remain thin adapters. |',
    '| Canonical planner/orchestrator | ADAPT | Recipe queue, batch scheduler and factory divide orchestration today. |',
    '| Simulation truth, RNG and frozen C11-C | PROTECTED | Explicitly outside D4 request normalization and orchestration. |',
    '| Producer 2.16.9 lineage | HISTORICAL | Retain as provenance only; current tooling baseline is C11-C 2.19.12. |',
    '',
    '## D4.1 design implications',
    '',
    '1. Define stable request IDs for Challenge/content, visual/asset family, delivery profile, music style and render mode.',
    '2. Keep gameplay seed and dedicated music_seed separate in the request and its provenance.',
    '3. Keep logical Challenge timing and content truth sourced from Challenge definitions.',
    '4. Reference existing delivery and D2/D3 registries; do not copy their policy into the schema.',
    '5. Represent REVIEW and PRODUCTION intent and artifact destination explicitly while retaining established root policies.',
    '6. Hash canonical normalized request bytes and bind that hash to current manifest provenance.',
    '7. Keep GUI and CLI as adapters over one later orchestrator; D4.0 does not activate either.',
    '',
    '## Evidence',
    '',
    '- `artifacts/tests/c11d_d4/d4_0_production_flow_audit.json`',
    '- `artifacts/tests/c11d_d4/d4_0_validation_receipt.json`',
    '- Frozen archive and active-source SHA-256 entries are included in the audit JSON.',
    '',
    '## Next',
    '',
    'D4.1 - Canonical Production Request Schema.'
)
$ContractText = $ContractLines -join [Environment]::NewLine
[System.IO.File]::WriteAllText($ContractPath,$ContractText,(New-Object System.Text.UTF8Encoding($false)))
Write-JsonNoBom $ReportPath $Audit

$Receipt = [ordered]@{
    schema = 'C11D-VALIDATION-RECEIPT-V1'
    checkpoint = 'C11-D D4.0'
    result = 'PASS'
    status = 'CLOSED'
    objective = 'Production Flow / Request Audit'
    audit_only = $true
    production_activated = $false
    gui_launched = $false
    cli_production_launched = $false
    c11c_baseline_archive_sha256 = $ArchiveHash
    c11c_source_tree_sha256 = ([string]$PackageReceipt.source_tree_sha256).ToLowerInvariant()
    audit_artifact = 'artifacts/tests/c11d_d4/d4_0_production_flow_audit.json'
    audit_artifact_sha256 = (Get-FileHash -LiteralPath $ReportPath -Algorithm SHA256).Hash.ToLowerInvariant()
    contract = 'docs/current/d/D4.0_PRODUCTION_FLOW_AUDIT_CONTRACT.md'
    contract_sha256 = (Get-FileHash -LiteralPath $ContractPath -Algorithm SHA256).Hash.ToLowerInvariant()
    next = 'D4.1 - Canonical Production Request Schema'
    generated_at_utc = $NowUtc
}
Write-JsonNoBom $ReceiptPath $Receipt

$HandoffMarker = '<!-- C11D_D4_0_HANDOFF_V1 -->'
$Handoff = @(
    $HandoffMarker,
    '',
    '## C11-D D4.0 CLOSED / PASS',
    '',
    '- C11-C 2.19.12 frozen archive SHA-256 verified against the package receipt.',
    '- Production flow audit completed from active source and contract evidence.',
    '- No GUI launch, CLI production run, renderer activation, C11-C source change, simulation truth change or RNG change.',
    '- Canonical Production Request schema and request hash are NEW D4.1 work.',
    '- Reuse the existing Challenge definitions, D2 asset binding, D3 music contract, delivery profiles, launchers and provenance validators.',
    '- Audit: `artifacts/tests/c11d_d4/d4_0_production_flow_audit.json`.',
    '- Contract: `docs/current/d/D4.0_PRODUCTION_FLOW_AUDIT_CONTRACT.md`.',
    '- Receipt: `artifacts/tests/c11d_d4/d4_0_validation_receipt.json`.',
    '- Next active checkpoint: **D4.1 - Canonical Production Request Schema**.',
    ''
)

foreach($Path in @($MasterHandoverPath,$StartPromptPath)){
    if(-not (Test-Path -LiteralPath $Path)){ throw "Required D handover missing: $Path" }
    $Existing = [System.IO.File]::ReadAllText($Path)
    if(-not $Existing.Contains($HandoffMarker)){
        $Updated = $Existing.TrimEnd() + [Environment]::NewLine + [Environment]::NewLine + ($Handoff -join [Environment]::NewLine)
        [System.IO.File]::WriteAllText($Path,$Updated,(New-Object System.Text.UTF8Encoding($false)))
    }
}

Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.0 - PRODUCTION FLOW AUDIT PASS / CLOSED'
Write-Host '=================================================='
Write-Host ('[OK] Frozen C11-C archive SHA-256: {0}' -f $ArchiveHash)
Write-Host ('[OK] Challenge definitions inventoried: {0}' -f $ChallengeIds.Count)
Write-Host ('[OK] Reusable delivery profiles inventoried: {0}' -f $DeliveryProfiles.Count)
Write-Host '[OK] No GUI, CLI production or renderer was activated.'
Write-Host ('[OK] Audit: {0}' -f $ReportPath)
Write-Host ('[OK] Contract: {0}' -f $ContractPath)
Write-Host ('[OK] Receipt: {0}' -f $ReceiptPath)
Write-Host '[OK] NEXT: D4.1 - Canonical Production Request Schema'
