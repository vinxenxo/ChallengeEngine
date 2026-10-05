#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

# ============================================================
# C11-D D4.4
# Canonical Production Orchestrator
#
# Scope:
#   - define ONE canonical orchestration layer;
#   - accept a canonical Production Request produced by D4.2;
#   - resolve reusable delivery/personalization contracts;
#   - build a deterministic Production Plan;
#   - prove GUI/CLI inputs converge to the same plan/hash;
#   - keep renderers, GUI, production CLI and simulation inactive.
#
# D4.4 does NOT:
#   - render media;
#   - activate Godot;
#   - mutate simulation truth;
#   - consume gameplay/structural RNG;
#   - alter winning_frame/close_calls;
#   - replace D4.2 normalization or D4.3 personalization logic.
# ============================================================

$ProjectRoot = (Get-Location).Path

$SchemaPath = Join-Path $ProjectRoot 'definitions\c11d\production\C11D_PRODUCTION_REQUEST_SCHEMA_V1.json'
$PersonalizationRegistryPath = Join-Path $ProjectRoot 'definitions\c11d\personalization\C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json'
$D42ReceiptPath = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_2\d4_2_validation_receipt.json'
$D43ReceiptPath = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_3\d4_3_validation_receipt.json'

$ToolDir = Join-Path $ProjectRoot 'tools\c11d\d4'
$ArtifactDir = Join-Path $ProjectRoot 'artifacts\tests\c11d_d4\d4_4'
$DocsDir = Join-Path $ProjectRoot 'docs\current\d'
$HistoryDir = Join-Path $ProjectRoot 'docs\history\master-prompts\c11d'

$OrchestratorPath = Join-Path $ToolDir 'canonical_production_orchestrator.py'
$RunnerPath = Join-Path $ToolDir 'run_d4_4_canonical_orchestrator.ps1'

$EvidencePath = Join-Path $ArtifactDir 'd4_4_orchestration_evidence.json'
$ParityPath = Join-Path $ArtifactDir 'd4_4_gui_cli_plan_parity.json'
$ReceiptPath = Join-Path $ArtifactDir 'd4_4_validation_receipt.json'
$PlanPath = Join-Path $ArtifactDir 'd4_4_example_production_plan.json'
$ContractPath = Join-Path $DocsDir 'D4.4_CANONICAL_PRODUCTION_ORCHESTRATOR_CONTRACT.md'

$MasterPath = Join-Path $DocsDir 'MASTER_HANDOVER_C11D_CURRENT.md'
$StartPath = Join-Path $DocsDir 'START_PROMPT_C11D_CURRENT.md'

if(-not (Test-Path -LiteralPath $SchemaPath)){
    throw "D4.1 schema not found: $SchemaPath"
}

if(-not (Test-Path -LiteralPath $PersonalizationRegistryPath)){
    throw "D4.3 personalization registry not found: $PersonalizationRegistryPath"
}

if(-not (Test-Path -LiteralPath $D42ReceiptPath)){
    throw "D4.2 receipt not found: $D42ReceiptPath"
}

if(-not (Test-Path -LiteralPath $D43ReceiptPath)){
    throw "D4.3 receipt not found: $D43ReceiptPath"
}

$PythonCommand = Get-Command python.exe -ErrorAction SilentlyContinue
if($null -eq $PythonCommand){
    throw 'python.exe not found in PATH.'
}

New-Item -ItemType Directory -Force -Path `
    $ToolDir, `
    $ArtifactDir, `
    $DocsDir, `
    $HistoryDir | Out-Null

$Utf8NoBom = New-Object -TypeName System.Text.UTF8Encoding -ArgumentList @($false)

function Write-TextUtf8NoBom([string]$Path,[string]$Text){
    [System.IO.File]::WriteAllText($Path,$Text,$Utf8NoBom)
}

function Write-JsonUtf8NoBom([string]$Path,[object]$Value,[int]$Depth){
    $JsonText = [string]($Value | ConvertTo-Json -Depth $Depth)
    $JsonBytes = [System.Text.Encoding]::UTF8.GetBytes($JsonText)
    [System.IO.File]::WriteAllBytes($Path,$JsonBytes)
}

# ------------------------------------------------------------
# 1. Verify predecessor checkpoints
# ------------------------------------------------------------

$D42Receipt = (
    [System.IO.File]::ReadAllText($D42ReceiptPath) |
    ConvertFrom-Json
)

$D43Receipt = (
    [System.IO.File]::ReadAllText($D43ReceiptPath) |
    ConvertFrom-Json
)

if([string]$D42Receipt.result -ne 'PASS'){
    throw 'D4.2 result is not PASS.'
}

if([string]$D42Receipt.status -ne 'CLOSED'){
    throw 'D4.2 status is not CLOSED.'
}

if([string]$D43Receipt.result -ne 'PASS'){
    throw 'D4.3 result is not PASS.'
}

if([string]$D43Receipt.status -ne 'CLOSED'){
    throw 'D4.3 status is not CLOSED.'
}

# ------------------------------------------------------------
# 2. Canonical orchestrator
# ------------------------------------------------------------

$OrchestratorScript = @'
import argparse
import hashlib
import json
import sys
from collections import OrderedDict

SCHEMA_ID = "c11d_production_request"
SCHEMA_VERSION = "1.0"
PLAN_ID = "c11d_production_plan"
PLAN_VERSION = "1.0"
FORBIDDEN_FIELDS = {
    "winning_frame",
    "close_calls",
    "simulation_result",
    "simulation_truth",
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, value):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def canonical_json(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=False,
    )


def sha256(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def profile_registry(registry):
    profiles = registry.get("profiles", [])
    result = OrderedDict()
    for profile in profiles:
        profile_id = profile.get("profile_id")
        if profile_id:
            result[str(profile_id)] = profile
    return result


def delivery_profiles(schema):
    result = []
    for field in schema.get("fields", []):
        if field.get("name") == "delivery_profile_id":
            values = field.get("evidence_values", [])
            result.extend(str(value) for value in values)
    return sorted(set(result))


def validate_canonical_request(request, schema):
    if not isinstance(request, dict):
        raise ValueError("Canonical Production Request must be an object")

    for forbidden in FORBIDDEN_FIELDS:
        if forbidden in request:
            raise ValueError(f"Forbidden simulation control: {forbidden}")

    if request.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Production Request schema_version must be 1.0")

    if not request.get("request_id"):
        raise ValueError("request_id is required")

    if request.get("mode") not in {"REVIEW", "PRODUCTION"}:
        raise ValueError("mode must be REVIEW or PRODUCTION")

    challenge_values = []
    for field in schema.get("fields", []):
        if field.get("name") == "challenge_id":
            challenge_values = field.get("allowed_values", [])

    challenge_id = request.get("challenge_id")
    if challenge_values and challenge_id not in challenge_values:
        raise ValueError(f"Unknown challenge_id: {challenge_id}")

    known_delivery = delivery_profiles(schema)
    delivery_id = request.get("delivery_profile_id")
    if known_delivery and delivery_id not in known_delivery:
        raise ValueError(f"Unknown delivery_profile_id: {delivery_id}")

    seed = request.get("seed")
    music_seed = request.get("music_seed")
    if seed is None or music_seed is None:
        raise ValueError("seed and music_seed are both required")

    if not isinstance(seed, int) or isinstance(seed, bool):
        raise ValueError("seed must be integer")

    if not isinstance(music_seed, int) or isinstance(music_seed, bool):
        raise ValueError("music_seed must be integer")

    if "provenance" not in request:
        raise ValueError("provenance is required in canonical request")

    return True


def build_plan(request, schema, personalization_registry):
    validate_canonical_request(request, schema)

    personal_profiles = profile_registry(personalization_registry)
    personalization = request.get("personalization", {})
    personalization_enabled = bool(personalization.get("enabled", False))
    personalization_profile = personalization.get("profile_id", "UNKNOWN")

    if personalization_enabled:
        if personalization_profile == "UNKNOWN":
            raise ValueError(
                "Enabled personalization requires an explicit profile_id"
            )
        if personalization_profile not in personal_profiles:
            raise ValueError(
                f"Unknown personalization profile: {personalization_profile}"
            )

    # One canonical sequence. These are PLAN steps, not renderer calls.
    steps = [
        OrderedDict([
            ("step_id", "request_validation"),
            ("type", "VALIDATION"),
            ("authority", "CANONICAL"),
        ]),
        OrderedDict([
            ("step_id", "challenge_resolution"),
            ("type", "RESOLVE_CHALLENGE"),
            ("authority", "DECLARATIVE"),
            ("challenge_id", request["challenge_id"]),
        ]),
        OrderedDict([
            ("step_id", "delivery_profile_resolution"),
            ("type", "RESOLVE_DELIVERY_PROFILE"),
            ("authority", "REUSABLE_PROFILE"),
            ("delivery_profile_id", request["delivery_profile_id"]),
        ]),
        OrderedDict([
            ("step_id", "personalization_resolution"),
            ("type", "RESOLVE_PERSONALIZATION"),
            ("authority", "D4.3_RESOLVER"),
            ("enabled", personalization_enabled),
            ("profile_id", personalization_profile),
        ]),
        OrderedDict([
            ("step_id", "music_request"),
            ("type", "MUSIC_PLAN"),
            ("authority", "C11D_MUSIC_ENGINE_V5"),
            ("music_seed", request["music_seed"]),
            ("gameplay_rng_consumption", False),
        ]),
        OrderedDict([
            ("step_id", "production_plan"),
            ("type", "DELIVERY_PLAN"),
            ("authority", "CANONICAL_ORCHESTRATOR"),
            ("mode", request["mode"]),
        ]),
        OrderedDict([
            ("step_id", "artifact_provenance"),
            ("type", "PROVENANCE_PLAN"),
            ("authority", "CANONICAL"),
        ]),
    ]

    plan = OrderedDict([
        ("plan_id", PLAN_ID),
        ("plan_version", PLAN_VERSION),
        ("request_id", request["request_id"]),
        ("schema_id", SCHEMA_ID),
        ("schema_version", SCHEMA_VERSION),
        ("mode", request["mode"]),
        ("challenge_id", request["challenge_id"]),
        ("challenge_version", request.get("challenge_version", "UNKNOWN")),
        ("seed", request["seed"]),
        ("music_seed", request["music_seed"]),
        ("delivery_profile_id", request["delivery_profile_id"]),
        ("presentation_profile_id", request.get("presentation_profile_id", "UNKNOWN")),
        ("duration_seconds", request["duration_seconds"]),
        ("variation_index", request.get("variation_index", 0)),
        ("personalization", personalization),
        ("editorial", request.get("editorial", {})),
        ("output", request.get("output", {})),
        ("steps", steps),
        ("runtime_authority", "NONE"),
        ("simulation_truth_mutation", False),
        ("winning_frame_mutation", False),
        ("close_calls_mutation", False),
        ("gameplay_rng_consumption", False),
        ("structural_rng_consumption", False),
        ("renderer_activation", False),
        ("gui_activation", False),
        ("cli_production_activation", False),
        ("orchestrator_execution", False),
    ])

    plan_hash = sha256(plan)

    return plan, plan_hash


def make_fixture(challenge_id, delivery_profile_id, origin):
    return OrderedDict([
        ("request_id", "D4.4-ORCHESTRATOR-001"),
        ("schema_version", "1.0"),
        ("mode", "PRODUCTION"),
        ("challenge_id", challenge_id),
        ("challenge_version", "UNKNOWN"),
        ("seed", 123456),
        ("music_seed", 654321),
        ("delivery_profile_id", delivery_profile_id),
        ("presentation_profile_id", "UNKNOWN"),
        ("duration_seconds", 10.0),
        ("variation_index", 0),
        ("personalization", OrderedDict([
            ("enabled", True),
            ("profile_id", "editorial_text_v1"),
            ("values", OrderedDict([
                ("player_name", "TEST"),
                ("challenge_label", "UNKNOWN"),
            ])),
        ])),
        ("editorial", OrderedDict([
            ("title", "TEST"),
            ("subtitle", "UNKNOWN"),
            ("language", "es"),
            ("call_to_action", "JUEGA"),
        ])),
        ("output", OrderedDict([
            ("container", "mp4"),
            ("width", 720),
            ("height", 1280),
            ("fps", 30),
            ("audio_enabled", True),
        ])),
        ("provenance", OrderedDict([
            ("source_revision", "D4.4-TEST"),
            ("request_origin", origin),
            ("parent_request_id", "PARENT-TEST"),
        ])),
    ])


def run_self_test(schema_path, personalization_registry_path):
    schema = load_json(schema_path)
    personalization_registry = load_json(personalization_registry_path)

    if schema.get("schema_id") != SCHEMA_ID:
        raise AssertionError("schema_id mismatch")

    if schema.get("schema_version") != SCHEMA_VERSION:
        raise AssertionError("schema_version mismatch")

    if schema.get("runtime_authority") != "NONE":
        raise AssertionError("schema runtime authority must be NONE")

    challenge_values = []
    for field in schema.get("fields", []):
        if field.get("name") == "challenge_id":
            challenge_values = list(field.get("allowed_values", []))

    delivery_values = delivery_profiles(schema)

    if len(challenge_values) != 9:
        raise AssertionError(
            f"Expected 9 Challenge IDs, got {len(challenge_values)}"
        )

    if len(delivery_values) != 5:
        raise AssertionError(
            f"Expected 5 delivery profiles, got {len(delivery_values)}"
        )

    personal_profiles = profile_registry(personalization_registry)

    if "none_v1" not in personal_profiles:
        raise AssertionError("none_v1 missing from personalization registry")

    if "editorial_text_v1" not in personal_profiles:
        raise AssertionError("editorial_text_v1 missing from personalization registry")

    challenge_id = challenge_values[0]
    delivery_id = delivery_values[0]

    gui_request = make_fixture(challenge_id, delivery_id, "GUI")
    cli_request = make_fixture(challenge_id, delivery_id, "CLI")

    gui_plan, gui_hash = build_plan(
        gui_request,
        schema,
        personalization_registry,
    )

    cli_plan, cli_hash = build_plan(
        cli_request,
        schema,
        personalization_registry,
    )

    plan_json_equal = canonical_json(gui_plan) == canonical_json(cli_plan)
    plan_hash_equal = gui_hash == cli_hash

    if not plan_json_equal:
        raise AssertionError("GUI/CLI canonical Production Plan differs")

    if not plan_hash_equal:
        raise AssertionError("GUI/CLI Production Plan SHA-256 differs")

    if len(gui_hash) != 64:
        raise AssertionError("Production Plan SHA-256 has invalid length")

    # Personalization change must alter the plan but never alter either seed.
    changed = make_fixture(challenge_id, delivery_id, "GUI")
    changed["personalization"]["values"]["player_name"] = "OTHER"

    changed_plan, changed_hash = build_plan(
        changed,
        schema,
        personalization_registry,
    )

    personalization_plan_changed = changed_hash != gui_hash
    seeds_preserved = (
        changed_plan["seed"] == gui_plan["seed"] and
        changed_plan["music_seed"] == gui_plan["music_seed"]
    )

    if not personalization_plan_changed:
        raise AssertionError("Personalization change did not alter Production Plan identity")

    if not seeds_preserved:
        raise AssertionError("Personalization changed seed values")

    # Runtime boundary tests.
    boundary_pass = (
        gui_plan["runtime_authority"] == "NONE" and
        gui_plan["simulation_truth_mutation"] is False and
        gui_plan["winning_frame_mutation"] is False and
        gui_plan["close_calls_mutation"] is False and
        gui_plan["gameplay_rng_consumption"] is False and
        gui_plan["structural_rng_consumption"] is False and
        gui_plan["renderer_activation"] is False and
        gui_plan["gui_activation"] is False and
        gui_plan["cli_production_activation"] is False and
        gui_plan["orchestrator_execution"] is False
    )

    if not boundary_pass:
        raise AssertionError("Runtime boundary protection failed")

    # Forbidden simulation controls must be rejected.
    rejected = {}
    for field_name in ["winning_frame", "close_calls", "simulation_result"]:
        invalid = make_fixture(challenge_id, delivery_id, "TEST")
        invalid[field_name] = 1
        try:
            build_plan(invalid, schema, personalization_registry)
            rejected[field_name] = False
        except ValueError:
            rejected[field_name] = True

    if not all(rejected.values()):
        raise AssertionError("Forbidden simulation control acceptance detected")

    return OrderedDict([
        ("checkpoint", "C11-D D4.4"),
        ("result", "PASS"),
        ("status", "CLOSED"),
        ("plan_id", PLAN_ID),
        ("plan_version", PLAN_VERSION),
        ("challenge_count", len(challenge_values)),
        ("delivery_profile_count", len(delivery_values)),
        ("personalization_profile_count", len(personal_profiles)),
        ("gui_cli_plan_parity", OrderedDict([
            ("canonical_plan_equal", plan_json_equal),
            ("sha256_equal", plan_hash_equal),
            ("sha256", gui_hash),
        ])),
        ("personalization_isolation", OrderedDict([
            ("plan_hash_changes", personalization_plan_changed),
            ("seed_identical", seeds_preserved),
            ("music_seed_identical", seeds_preserved),
        ])),
        ("forbidden_simulation_controls_rejected", rejected),
        ("runtime_boundary", OrderedDict([
            ("runtime_authority", "NONE"),
            ("simulation_truth_mutation", False),
            ("winning_frame_mutation", False),
            ("close_calls_mutation", False),
            ("gameplay_rng_consumption", False),
            ("structural_rng_consumption", False),
            ("renderer_activation", False),
            ("gui_activation", False),
            ("cli_production_activation", False),
            ("orchestrator_execution", False),
        ])),
        ("example_plan", gui_plan),
        ("next", "D4.5 - CLI Adapter"),
    ])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", required=True)
    parser.add_argument("--personalization-registry", required=True)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--parity", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()

    result = run_self_test(
        args.schema,
        args.personalization_registry,
    )

    save_json(args.evidence, result)
    save_json(args.parity, result["gui_cli_plan_parity"])
    save_json(args.plan, result["example_plan"])
    save_json(args.receipt, result)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"D4.4 ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
'@

Write-TextUtf8NoBom $OrchestratorPath $OrchestratorScript

# ------------------------------------------------------------
# 3. PowerShell runner
# ------------------------------------------------------------

$RunnerScript = @'
#requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 1.0

$RootPath = (Get-Location).Path

$SchemaPath = Join-Path $RootPath 'definitions\c11d\production\C11D_PRODUCTION_REQUEST_SCHEMA_V1.json'
$PersonalizationRegistryPath = Join-Path $RootPath 'definitions\c11d\personalization\C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json'
$OrchestratorPath = Join-Path $RootPath 'tools\c11d\d4\canonical_production_orchestrator.py'

$ArtifactDir = Join-Path $RootPath 'artifacts\tests\c11d_d4\d4_4'
$EvidencePath = Join-Path $ArtifactDir 'd4_4_orchestration_evidence.json'
$ParityPath = Join-Path $ArtifactDir 'd4_4_gui_cli_plan_parity.json'
$PlanPath = Join-Path $ArtifactDir 'd4_4_example_production_plan.json'
$ReceiptPath = Join-Path $ArtifactDir 'd4_4_validation_receipt.json'

if(-not (Test-Path -LiteralPath $SchemaPath)){
    throw 'D4.1 schema missing.'
}

if(-not (Test-Path -LiteralPath $PersonalizationRegistryPath)){
    throw 'D4.3 personalization registry missing.'
}

if(-not (Test-Path -LiteralPath $OrchestratorPath)){
    throw 'D4.4 orchestrator missing.'
}

New-Item -ItemType Directory -Force -Path $ArtifactDir | Out-Null

$RawOutput = & python.exe `
    $OrchestratorPath `
    --schema $SchemaPath `
    --personalization-registry $PersonalizationRegistryPath `
    --self-test `
    --evidence $EvidencePath `
    --parity $ParityPath `
    --plan $PlanPath `
    --receipt $ReceiptPath

if($LASTEXITCODE -ne 0){
    throw 'D4.4 orchestrator self-test failed.'
}

$ReceiptObject = (
    [System.IO.File]::ReadAllText($ReceiptPath) |
    ConvertFrom-Json
)

if([string]$ReceiptObject.result -ne 'PASS'){
    throw 'D4.4 receipt result is not PASS.'
}

if([string]$ReceiptObject.status -ne 'CLOSED'){
    throw 'D4.4 receipt status is not CLOSED.'
}

if([bool]$ReceiptObject.gui_cli_plan_parity.canonical_plan_equal -ne $true){
    throw 'D4.4 GUI/CLI plan JSON parity failed.'
}

if([bool]$ReceiptObject.gui_cli_plan_parity.sha256_equal -ne $true){
    throw 'D4.4 GUI/CLI plan SHA-256 parity failed.'
}

if([string]$ReceiptObject.runtime_boundary.runtime_authority -ne 'NONE'){
    throw 'D4.4 runtime authority boundary failed.'
}

if([bool]$ReceiptObject.runtime_boundary.orchestrator_execution -ne $false){
    throw 'D4.4 must not execute production orchestration.'
}

Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.4 - CANONICAL ORCHESTRATOR'
Write-Host '=================================================='
Write-Host '[OK] D4.2 PASS/CLOSED verified.'
Write-Host '[OK] D4.3 PASS/CLOSED verified.'
Write-Host '[OK] Canonical Production Plan generated.'
Write-Host ('[OK] Challenges supported: {0}.' -f $ReceiptObject.challenge_count)
Write-Host ('[OK] Delivery profiles supported: {0}.' -f $ReceiptObject.delivery_profile_count)
Write-Host ('[OK] Personalization profiles supported: {0}.' -f $ReceiptObject.personalization_profile_count)
Write-Host '[OK] GUI canonical plan == CLI canonical plan.'
Write-Host '[OK] GUI plan SHA-256 == CLI plan SHA-256.'
Write-Host ('[OK] Canonical Production Plan SHA-256: {0}.' -f $ReceiptObject.gui_cli_plan_parity.sha256)
Write-Host '[OK] Personalization changes plan identity without changing seed/music_seed.'
Write-Host '[OK] winning_frame / close_calls / simulation controls rejected.'
Write-Host '[OK] runtime_authority = NONE.'
Write-Host '[OK] Renderer activation = NONE.'
Write-Host '[OK] GUI production activation = NONE.'
Write-Host '[OK] CLI production activation = NONE.'
Write-Host '[OK] Orchestrator execution = NONE.'
Write-Host '[OK] D4.4 receipt verified.'
Write-Host ''
Write-Host '=================================================='
Write-Host ' C11-D D4.4 - PASS / CLOSED'
Write-Host '=================================================='
Write-Host 'NEXT: D4.5 - CLI Adapter'
'@

Write-TextUtf8NoBom $RunnerPath $RunnerScript

# ------------------------------------------------------------
# 4. Execute D4.4
# ------------------------------------------------------------

& powershell.exe `
    -NoProfile `
    -ExecutionPolicy Bypass `
    -File $RunnerPath

if($LASTEXITCODE -ne 0){
    throw 'D4.4 runner failed.'
}

# ------------------------------------------------------------
# 5. Contract
# ------------------------------------------------------------

$ContractLines = @(
    '# C11-D D4.4 - Canonical Production Orchestrator',
    '',
    '## Status',
    '',
    'PASS / CLOSED.',
    '',
    '## Objective',
    '',
    'D4.4 establishes one canonical orchestration layer that consumes a D4.2 canonical Production Request and produces a deterministic Production Plan. It does not execute production.',
    '',
    '## Reuse boundary',
    '',
    '- D4.2 owns request normalization and request identity;',
    '- D4.3 owns personalization profile validation and personalization identity;',
    '- D4.4 owns orchestration order and Production Plan identity;',
    '- reusable delivery profiles remain declarative inputs;',
    '- the future renderer remains outside the orchestrator contract until later D checkpoints.',
    '',
    '## Canonical plan',
    '',
    'The canonical Production Plan contains request identity, Challenge identity, seeds, delivery/presentation profiles, personalization, editorial/output intent and a deterministic ordered list of plan steps.',
    '',
    'The plan has its own SHA-256 identity. GUI and CLI requests that are semantically equivalent must converge to the same plan JSON and same plan hash.',
    '',
    '## Seed isolation',
    '',
    '`seed` and `music_seed` remain distinct. The orchestrator consumes no gameplay or structural RNG. The music step only declares a music plan using the dedicated `music_seed`.',
    '',
    'Personalization can change the plan identity but cannot change either seed.',
    '',
    '## Runtime boundary',
    '',
    'D4.4 generates plans only. GUI production, CLI production, renderer execution and actual orchestrator execution are all explicitly false. Simulation truth, `winning_frame` and `close_calls` remain protected.',
    '',
    '## Evidence',
    '',
    '- `tools/c11d/d4/canonical_production_orchestrator.py`',
    '- `artifacts/tests/c11d_d4/d4_4/d4_4_orchestration_evidence.json`',
    '- `artifacts/tests/c11d_d4/d4_4/d4_4_gui_cli_plan_parity.json`',
    '- `artifacts/tests/c11d_d4/d4_4/d4_4_example_production_plan.json`',
    '- `artifacts/tests/c11d_d4/d4_4/d4_4_validation_receipt.json`',
    '',
    '## Next',
    '',
    'D4.5 - CLI Adapter.'
)

Write-TextUtf8NoBom `
    $ContractPath `
    ($ContractLines -join [Environment]::NewLine)

# ------------------------------------------------------------
# 6. Handover
# ------------------------------------------------------------

$HandoffMarker = '<!-- C11D_D4_4_HANDOFF_V1 -->'

$HandoffLines = @(
    $HandoffMarker,
    '',
    '## C11-D D4.4 CLOSED',
    '',
    '- Canonical Production Orchestrator implemented as a plan-only layer.',
    '- D4.2 normalized Production Request is the orchestrator input contract.',
    '- D4.3 personalization registry is reused for profile resolution.',
    '- Deterministic Production Plan and SHA-256 plan identity implemented.',
    '- GUI and CLI semantically equivalent requests produce identical plans and plan hashes.',
    '- Personalization changes plan identity without changing seed or music_seed.',
    '- `seed` and `music_seed` remain isolated.',
    '- `winning_frame`, `close_calls` and simulation-derived controls are rejected.',
    '- No GUI production activation.',
    '- No CLI production activation.',
    '- No renderer activation.',
    '- No actual orchestrator execution.',
    '- runtime_authority remains NONE.',
    '- Next active checkpoint: **D4.5 - CLI Adapter**.',
    ''
)

function Add-Handoff(
    [string]$Path,
    [string[]]$Lines
){
    if(-not (Test-Path -LiteralPath $Path)){
        return
    }

    $CurrentText = [System.IO.File]::ReadAllText($Path)

    if($CurrentText.Contains($HandoffMarker)){
        return
    }

    $UpdatedText = (
        $CurrentText.TrimEnd() +
        [Environment]::NewLine +
        [Environment]::NewLine +
        ($Lines -join [Environment]::NewLine) +
        [Environment]::NewLine
    )

    Write-TextUtf8NoBom $Path $UpdatedText
}

Add-Handoff $MasterPath $HandoffLines
Add-Handoff $StartPath $HandoffLines

# ------------------------------------------------------------
# 7. Historical snapshots
# ------------------------------------------------------------

$UtcStamp = (Get-Date).ToUniversalTime().ToString('yyyyMMdd_HHmmss')

if(Test-Path -LiteralPath $MasterPath){
    Copy-Item `
        -LiteralPath $MasterPath `
        -Destination (
            Join-Path $HistoryDir (
                'MASTER_HANDOVER_C11D_D4.4_{0}.md' -f $UtcStamp
            )
        ) `
        -Force
}

if(Test-Path -LiteralPath $StartPath){
    Copy-Item `
        -LiteralPath $StartPath `
        -Destination (
            Join-Path $HistoryDir (
                'START_PROMPT_C11D_D4.4_{0}.md' -f $UtcStamp
            )
        ) `
        -Force
}

# ------------------------------------------------------------
# 8. Final artifact checks
# ------------------------------------------------------------

$RequiredPaths = @(
    $OrchestratorPath,
    $RunnerPath,
    $EvidencePath,
    $ParityPath,
    $PlanPath,
    $ReceiptPath,
    $ContractPath,
    $MasterPath,
    $StartPath
)

foreach($RequiredPath in $RequiredPaths){
    if(-not (Test-Path -LiteralPath $RequiredPath)){
        throw "D4.4 required artifact missing: $RequiredPath"
    }
}

$PlanText = [System.IO.File]::ReadAllText($PlanPath)
$PlanObject = $PlanText | ConvertFrom-Json

if([string]$PlanObject.plan_id -ne 'c11d_production_plan'){
    throw 'Production Plan ID validation failed.'
}

if([string]$PlanObject.runtime_authority -ne 'NONE'){
    throw 'Production Plan runtime authority validation failed.'
}

if([bool]$PlanObject.renderer_activation -ne $false){
    throw 'Production Plan renderer activation validation failed.'
}

Write-Host ''
Write-Host 'D4.4 patch applied successfully.'
Write-Host ('ORCHESTRATOR: {0}' -f $OrchestratorPath)
Write-Host ('PLAN:         {0}' -f $PlanPath)
Write-Host ('PARITY:       {0}' -f $ParityPath)
Write-Host ('EVIDENCE:     {0}' -f $EvidencePath)
Write-Host ('RECEIPT:      {0}' -f $ReceiptPath)
Write-Host ('CONTRACT:     {0}' -f $ContractPath)
Write-Host 'NEXT: D4.5 - CLI Adapter'
