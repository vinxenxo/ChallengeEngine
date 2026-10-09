from __future__ import annotations
import hashlib, json, re, os, shutil, tempfile
from pathlib import Path
from typing import Any

CONFIG_VERSION = '0.2.0'
PROFILE_RELATIVE_ROOT = Path('profiles') / 'c11d' / 'operator'
PROFILE_SCHEMA_REL = Path('definitions') / 'c11d' / 'config' / 'C11D_OPERATOR_CONFIGURATION_SCHEMA_V1.json'
D_REGISTRIES = (
 {'domain':'D2 · ASSETS','id':'D2_ASSET_FAMILIES','path':'definitions/c11d/asset_families/C11D_ASSET_FAMILY_REGISTRY_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D2 · ASSETS','id':'D2_CHALLENGE_BINDINGS','path':'definitions/c11d/asset_families/C11D_CHALLENGE_ASSET_BINDING_REGISTRY_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D3 · AUDIO','id':'D3_MUSIC_STYLE','path':'definitions/c11d/music/C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D3 · AUDIO','id':'D3_MUSIC_ENGINE','path':'definitions/c11d/music/C11D_MUSIC_ENGINE_V5_SPEC_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D4 · REQUEST','id':'D4_REQUEST_SCHEMA','path':'definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D4 · PERSONALIZATION','id':'D4_PERSONALIZATION_REGISTRY','path':'definitions/c11d/personalization/C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D9 · EDITORIAL','id':'D9_UNIVERSAL_EDITORIAL_MODEL','path':'definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D9 · BRIDGE PLANNING','id':'D9_EDITORIAL_RENDER_BRIDGE','path':'definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D9 · MAINTENANCE','id':'D9_MAINTENANCE_POLICY','path':'definitions/c11d/d9/D9_11_MAINTENANCE_POLICY_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D9 · CROSS-SUITE LIFECYCLE','id':'D9_CROSS_SUITE_LIFECYCLE','path':'definitions/c11d/d9/D9_13_CROSS_SUITE_LIFECYCLE_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D9 · REAL-MEDIA GUI CERTIFICATION GATE','id':'D9_REAL_MEDIA_CERTIFICATION_GATE','path':'definitions/c11d/d9/D9_14_GUI_REAL_MEDIA_CERTIFICATION_GATE_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D9 · GUI OPERATIONAL ACCEPTANCE','id':'D9_GUI_OPERATIONAL_ACCEPTANCE','path':'definitions/c11d/d9/D9_15_GUI_OPERATIONAL_ACCEPTANCE_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D9 · FULL ACCEPTANCE','id':'D9_FULL_ACCEPTANCE','path':'definitions/c11d/d9/D9_16_FULL_ACCEPTANCE_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D4 · GOVERNANCE','id':'D4_ACTIVATION_POLICY','path':'definitions/c11d/production/C11D_PRODUCTION_ACTIVATION_POLICY_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D5 · PROVENANCE','id':'D5_LINEAGE_REGISTRY','path':'definitions/c11d/provenance/C11D_PROVENANCE_LINEAGE_REGISTRY_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D6 · SEEDS','id':'D6_SEED_REGISTRY','path':'definitions/c11d/seeds/C11D_SEED_REGISTRY_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D6 · SEEDS','id':'D6_SEED_GOVERNANCE','path':'definitions/c11d/seeds/C11D_SEED_GOVERNANCE_POLICY_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D6 · SEEDS','id':'D6_DERIVATION_SPEC','path':'definitions/c11d/seeds/C11D_SEED_DERIVATION_SPEC_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D7 · CATALOG','id':'D7_MATRIX_SPEC','path':'definitions/c11d/production/C11D_PRODUCTION_MATRIX_SPEC_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D7 · CATALOG','id':'D7_CATALOG_SPEC','path':'definitions/c11d/production/C11D_CANONICAL_CATALOG_SPEC_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D8 · MEDIA QA','id':'D8_MEDIA_SCOPE','path':'definitions/c11d/d8/D8_MEDIA_SCOPE_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D8 · MEDIA QA','id':'D8_VISUAL_QA','path':'definitions/c11d/d8/D8_VISUAL_QA_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D8 · MEDIA QA','id':'D8_AUDIO_QA','path':'definitions/c11d/d8/D8_AUDIO_QA_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D8 · RELEASE','id':'D8_MEDIA_ELIGIBILITY','path':'definitions/c11d/d8/D8_ARTIFACT_MEDIA_ELIGIBILITY_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D8 · RELEASE','id':'D8_RELEASE_MANIFEST','path':'definitions/c11d/d8/D8_RELEASE_MANIFEST_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D8 · RELEASE','id':'D8_ACCEPTANCE_FREEZE','path':'definitions/c11d/d8/D8_ACCEPTANCE_FREEZE_V1.json','authority':'READ_ONLY_CANONICAL'},
 {'domain':'D9 · INTEGRATION','id':'D9_ACCEPTANCE_CLOSURE','path':'definitions/c11d/d9/D9_ACCEPTANCE_CLOSURE_V1.json','authority':'READ_ONLY_CANONICAL'},
)
PROFILE_KEYS = {'schema_id','schema_version','profile_id','label','challenge_id','mode','seed','music_seed','delivery_profile_id','presentation_profile_id','music_profile_id','audio_enabled','personalization_profile_id','personalization_values','runtime_authority','renderer_execution','production_execution','release_authority'}
PROFILE_ID_RE = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$')
GENERIC_EDITOR_PROTECTED_PREFIXES = (
    'challenges/', 'definitions/', 'schemas/', 'assets/', 'core/',
    'tools/', 'tests/', 'c11c-suite/', 'profiles/',
)

def generic_editor_path_protected(project_root: Path, path: Path) -> bool:
    """Protect paths by lexical and resolved identity, including symlink aliases."""
    root = project_root.resolve()
    try:
        lexical = path.absolute().relative_to(root).as_posix().lower()
        resolved = path.resolve().relative_to(root).as_posix().lower()
    except Exception:
        return True
    return any(
        lexical.startswith(prefix) or resolved.startswith(prefix)
        for prefix in GENERIC_EDITOR_PROTECTED_PREFIXES
    )

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def sha256_text(text: str) -> str: return hashlib.sha256(text.encode('utf-8')).hexdigest()

def _summary(data: Any) -> str:
    if not isinstance(data,dict): return type(data).__name__
    identity=data.get('registry_id') or data.get('schema_id') or data.get('policy_id') or data.get('contract') or data.get('profile_id') or data.get('schema') or 'JSON contract'
    version=data.get('schema_version') or data.get('registry_version') or data.get('version') or data.get('profile_version')
    status=data.get('status'); parts=[str(identity)]
    if version is not None: parts.append('v'+str(version))
    if status is not None: parts.append(str(status))
    return ' · '.join(parts)

def registry_rows(project_root: Path) -> list[dict[str,Any]]:
    root=project_root.resolve(); rows=[]
    for decl in D_REGISTRIES:
        row=dict(decl); path=(root/decl['path']).resolve()
        try: path.relative_to(root)
        except ValueError:
            row.update(status='BLOCKED_PATH',sha256='',bytes=0,summary='Path escapes project root'); rows.append(row); continue
        if not path.is_file():
            row.update(status='MISSING',sha256='',bytes=0,summary='Canonical contract missing'); rows.append(row); continue
        try:
            data=read_json(path); row.update(status='VALID_JSON',sha256=sha256_file(path),bytes=path.stat().st_size,summary=_summary(data))
        except Exception as exc: row.update(status='INVALID_JSON',sha256=sha256_file(path),bytes=path.stat().st_size,summary='JSON parse error: '+str(exc))
        rows.append(row)
    return rows

def validate_c11d_contracts(project_root: Path) -> tuple[list[dict[str,Any]],list[str]]:
    root=project_root.resolve(); rows=registry_rows(root); errors=[f"{x['id']}: {x['status']} ({x['path']})" for x in rows if x['status']!='VALID_JSON']; d={}
    for row in rows:
        if row['status']=='VALID_JSON': d[row['id']]=read_json(root/row['path'])
    def need(ok,msg):
        if not ok: errors.append(msg)
    need(d.get('D2_ASSET_FAMILIES',{}).get('runtime_authority')=='NONE','D2 asset family registry must keep runtime_authority=NONE')
    d3=d.get('D3_MUSIC_STYLE',{}); det=d3.get('determinism',{})
    need(d3.get('profile_id')=='challenge_8bit_v1','D3 music style profile identity mismatch')
    need(det.get('dedicated_music_seed') is True,'D3 must require an independent music seed')
    need(det.get('gameplay_rng_consumption') is False and det.get('structural_rng_consumption') is False,'D3 must not consume gameplay/structural RNG')
    d4=d.get('D4_REQUEST_SCHEMA',{}); fields={f.get('name') for f in d4.get('fields',[]) if isinstance(f,dict)}
    need({'seed','music_seed'}.issubset(fields),'D4 request must preserve independent explicit seeds')
    need(not ({'winning_frame','close_calls'} & fields),'D4 request must not control simulation-derived fields')
    need(d4.get('runtime_authority')=='NONE','D4 request schema must remain non-runtime')
    pers=d.get('D4_PERSONALIZATION_REGISTRY',{}); editorial=next((p for p in pers.get('profiles',[]) if p.get('profile_id')=='editorial_text_v1'),{})
    need({'title','subtitle','call_to_action','language','player_name','challenge_label'}.issubset(set(editorial.get('allowed_targets',[]))),'D4 editorial profile must retain six governed text targets')
    act=d.get('D4_ACTIVATION_POLICY',{}); need(act.get('runtime_authority')=='NONE' and act.get('renderer_activation_policy',{}).get('state')=='DISABLED','D4.8 renderer gate must remain disabled')
    need(act.get('execution',{}).get('production_execution') is False and act.get('execution',{}).get('renderer_called') is False,'D4.8 must not activate production/renderer')
    seeds=d.get('D6_SEED_GOVERNANCE',{}).get('defaults',{})
    need(seeds.get('cross_domain_seed_sharing')=='FORBIDDEN','D6 cross-domain seed sharing must remain forbidden')
    need(seeds.get('derivation_allowed') is False and seeds.get('runtime_activation')=='NONE','D6 automatic/runtime seed derivation must remain disabled')
    se=d.get('D6_SEED_REGISTRY',{}).get('entries',[]); by_domain={x.get('domain'):x for x in se if isinstance(x,dict)}
    need(by_domain.get('GAMEPLAY',{}).get('cross_domain_sharing') is False and by_domain.get('MUSIC',{}).get('cross_domain_sharing') is False,'D6 registry must isolate gameplay and music seeds')
    scope=d.get('D8_MEDIA_SCOPE',{})
    need(scope.get('scope_mode')=='EXPLICIT_REGISTRY_ONLY' and scope.get('candidate_count')==0,'D8 scope must stay explicit-registry-only with zero candidates')
    need(scope.get('release_authority')=='NONE' and scope.get('production_execution') is False,'D8 must not imply release/production authority')
    need(d.get('D8_RELEASE_MANIFEST',{}).get('physical_staging_when_release_authority_NONE') is False,'D8 physical staging must stay blocked without authority')
    need(d.get('D8_ACCEPTANCE_FREEZE',{}).get('media_dependent_acceptance_with_zero_media')=='PASS_NO_MEDIA','D8 zero-media acceptance must remain PASS_NO_MEDIA')
    d9=d.get('D9_ACCEPTANCE_CLOSURE',{})
    need(d9.get('release_authority')=='NONE' and d9.get('production_execution') is False and d9.get('renderer_execution') is False,'D9 checkpoint must remain non-execution/non-release')
    editorial=d.get('D9_UNIVERSAL_EDITORIAL_MODEL',{})
    need(editorial.get('schema')=='C11-D-D9-UNIVERSAL-EDITORIAL-MODEL-V1' and editorial.get('checkpoint')=='D9.8','D9.8 universal editorial model schema/checkpoint mismatch')
    need(editorial.get('status')=='CANONICAL_DECLARATIVE_MODEL','D9.8 model must be a declarative canonical contract')
    authority=editorial.get('authority',{})
    need(authority.get('runtime_authority')=='NONE' and authority.get('renderer_activation') is False and authority.get('production_execution') is False and authority.get('release_authority')=='NONE','D9.8 model must not grant runtime/renderer/production/release authority')
    seed_contract=editorial.get('seed_contract',{})
    need(seed_contract.get('master_seed')=='NOT_ADOPTED' and seed_contract.get('gameplay_seed')=='request.seed' and seed_contract.get('music_seed')=='request.music_seed','D9.8 must preserve explicit gameplay/music seed ownership')
    need(seed_contract.get('cross_domain_seed_sharing')=='FORBIDDEN' and seed_contract.get('runtime_seed_derivation') is False and seed_contract.get('automatic_seed_generation') is False,'D9.8 must forbid shared/derived/automatic seeds')
    need(editorial.get('inheritance_order')==['global','content_type','family','subtype','variant','production_override'],'D9.8 editorial inheritance order mismatch')
    content_types=editorial.get('content_types',{})
    longform=content_types.get('longform',{})
    need(longform.get('enabled_for_selection') is False and longform.get('editable_fields')==[] and longform.get('request_plan_compatibility')=='NOT_SUPPORTED_BY_CURRENT_D4_REQUEST_SCHEMA','D9.8 Longform must stay explicitly disabled until the D request contract supports it')
    bridge=d.get('D9_EDITORIAL_RENDER_BRIDGE',{})
    need(bridge.get('schema')=='C11-D-D9.10-EDITORIAL-RENDER-BRIDGE-CONTRACT-V1' and bridge.get('checkpoint')=='D9.10','D9.10 editorial-render bridge schema/checkpoint mismatch')
    need(bridge.get('status')=='PLANNING_ONLY_FUTURE_D_FROZEN_BASELINE_REQUIRED','D9.10 must remain plan-only until a future D frozen baseline')
    bridge_output=bridge.get('output',{})
    need(bridge_output.get('renderer_input_emitted') is False and bridge_output.get('renderer_adapter_invoked') is False and bridge_output.get('media_output_created') is False and bridge_output.get('output_artifact_path') is None,'D9.10 must not emit renderer input or create media')
    bridge_governance=bridge.get('governance',{})
    need(bridge_governance.get('master_seed')=='NOT_ADOPTED' and bridge_governance.get('cross_domain_seed_sharing')=='FORBIDDEN','D9.10 must preserve seed-domain governance')
    need(bridge_governance.get('renderer_activation') is False and bridge_governance.get('production_execution') is False and bridge_governance.get('d4_8')=='BLOCKED' and bridge_governance.get('release_authority')=='NONE','D9.10 must not grant renderer/production/D4.8/release authority')
    need(set(bridge.get('supported_content_types',[]))=={'challenges','visual_loops','visual_drills'},'D9.10 supported content types mismatch')
    need(bridge.get('unsupported_content_types',{}).get('longform')=='DISABLED_UNTIL_CANONICAL_D_REQUEST_SUPPORTS_LONGFORM','D9.10 Longform must remain disabled')
    required_bridge_gates={'FUTURE_D_RENDERER_BASELINE_FROZEN_AND_IDENTIFIED','RENDER_ADAPTER_CONTRACT_VERSIONED_AND_HASHED','D4_8_EXPLICIT_GOVERNANCE_AUTHORIZATION','GAMEPLAY_AND_MUSIC_SEED_ISOLATION_TESTS_PASS','CATALOG_REPRODUCTION_AND_NEGATIVE_ACCEPTANCE_PASS'}
    need(required_bridge_gates.issubset(set(bridge.get('future_d_frozen_baseline_gates',[]))),'D9.10 missing mandatory future baseline gates')
    lifecycle=d.get('D9_CROSS_SUITE_LIFECYCLE',{})
    need(lifecycle.get('schema')=='C11-D-D9.13-CROSS-SUITE-LIFECYCLE-CONTRACT-V1' and lifecycle.get('checkpoint')=='D9.13','D9.13 cross-suite lifecycle schema/checkpoint mismatch')
    need(lifecycle.get('status')=='CANONICAL_PLAN_ONLY_LIFECYCLE_CHAIN','D9.13 lifecycle must remain a plan-only chain')
    expected_pipeline=[('c11c-config','0.2.0'),('c11c-producer','0.11.1'),('c11c-test','0.2.0'),('c11c-catalog','0.2.0'),('c11c-maintenance','0.2.0')]
    need([(x.get('surface'),x.get('version')) for x in lifecycle.get('pipeline',[]) if isinstance(x,dict)]==expected_pipeline,'D9.13 pipeline must preserve exactly five canonical surfaces/versions')
    seed_contract=lifecycle.get('seed_contract',{})
    need(seed_contract.get('master_seed')=='NOT_ADOPTED' and seed_contract.get('gameplay_seed_source')=='canonical_request.seed' and seed_contract.get('music_seed_source')=='canonical_request.music_seed','D9.13 seed sources must remain explicit and independent')
    need(seed_contract.get('cross_domain_seed_sharing')=='FORBIDDEN' and seed_contract.get('automatic_seed_generation') is False and seed_contract.get('runtime_seed_derivation') is False,'D9.13 must forbid seed sharing, generation and runtime derivation')
    governance=lifecycle.get('governance',{})
    need(governance.get('renderer_activation') is False and governance.get('renderer_input_emitted') is False and governance.get('production_execution') is False and governance.get('media_output_created') is False and governance.get('d4_8')=='BLOCKED' and governance.get('release_authority')=='NONE','D9.13 must remain plan-only and non-authoritative')
    need(lifecycle.get('catalog_projection',{}).get('media_created') is False and lifecycle.get('catalog_projection',{}).get('release_authority')=='NONE','D9.13 Catalog projection must be explicitly no-media/non-release')
    d914=d.get('D9_REAL_MEDIA_CERTIFICATION_GATE',{})
    need(d914.get('schema')=='C11-D-D9.14-GUI-REAL-MEDIA-CERTIFICATION-GATE-V1' and d914.get('checkpoint')=='D9.14','D9.14 GUI real-media gate schema/checkpoint mismatch')
    need(d914.get('status')=='BLOCKED_UNTIL_FUTURE_D_FROZEN_BASELINE_AND_D4_8_AUTHORIZATION','D9.14 real-media gate must remain blocked until authorized future D baseline')
    gate_state=d914.get('current_gate_state',{})
    need(gate_state.get('future_d_frozen_baseline')=='ABSENT_NOT_AUTHORIZED' and gate_state.get('d4_8')=='BLOCKED','D9.14 future D baseline and D4.8 authorization must remain blocked')
    need(gate_state.get('renderer_activation') is False and gate_state.get('production_execution') is False and gate_state.get('release_authority')=='NONE','D9.14 must not grant renderer/production/release authority')
    need(gate_state.get('master_seed')=='NOT_ADOPTED' and gate_state.get('gameplay_seed_source')=='request.seed' and gate_state.get('music_seed_source')=='request.music_seed' and gate_state.get('cross_domain_seed_sharing')=='FORBIDDEN','D9.14 must preserve distinct gameplay/music seed governance')
    d914_cases=d914.get('case_matrix',[])
    need(len(d914_cases)==10 and len({x.get('case_id') for x in d914_cases if isinstance(x,dict)})==10,'D9.14 must retain its 10 unique E2E certification cases')
    need(set(d914.get('certification_scope',{}).get('supported_content_types_when_authorized',[]))=={'challenges','visual_loops','visual_drills'},'D9.14 supported content types mismatch')
    need(d914.get('certification_scope',{}).get('unsupported_content_types',{}).get('longform')=='DISABLED_UNTIL_CANONICAL_D_REQUEST_SUPPORTS_LONGFORM','D9.14 Longform must remain disabled until D4 request schema support')
    d914_output=d914.get('output_contract',{})
    need(d914_output.get('preflight_status')=='BLOCKED' and d914_output.get('renderer_activation') is False and d914_output.get('production_execution') is False and d914_output.get('media_output_created') is False and d914_output.get('release_authority')=='NONE','D9.14 gate output must be blocked and no-media/no-authority')
    maintenance=d.get('D9_MAINTENANCE_POLICY',{})
    need(maintenance.get('schema')=='C11-D-D9.11-MAINTENANCE-POLICY-V1' and maintenance.get('checkpoint')=='D9.11','D9.11 maintenance policy schema/checkpoint mismatch')
    need(maintenance.get('surface')=='c11c-maintenance' and maintenance.get('version')=='0.2.0','D9.11 must target existing Maintenance 0.2.0')
    ma=maintenance.get('authority',{})
    need(ma.get('runtime_authority')=='NONE' and ma.get('renderer_activation') is False and ma.get('production_execution') is False and ma.get('release_authority')=='NONE' and ma.get('d4_8')=='BLOCKED','D9.11 must not grant runtime/renderer/production/D4.8/release authority')
    need(ma.get('c11c_frozen_reference_mutation')=='FORBIDDEN','D9.11 must preserve the immutable C11-C reference')
    need(maintenance.get('active_suite_topology')==['c11c-test','c11c-producer','c11c-catalog','c11c-config','c11c-maintenance'],'D9.11 must retain exactly five canonical Suite surfaces')
    need(maintenance.get('safe_transient_roots')==['artifacts/scratch','artifacts/tests/logs/verbose'],'D9.11 cleanup allowlist unexpectedly broadened')
    cleanup_policy=maintenance.get('cleanup_policy',{})
    need(cleanup_policy.get('permanent_deletion') is False and cleanup_policy.get('apply_requires_confirmation') is True,'D9.11 cleanup must be explicit and reversible')
    quarantine_policy=maintenance.get('quarantine_policy',{})
    need(quarantine_policy.get('only_allowed_source')=='c11c-suite/c11d-control' and quarantine_policy.get('allow_overwrite') is False,'D9.11 quarantine must remain exact-path allowlisted/non-overwriting')
    historical=maintenance.get('historical_manifest',{})
    need(historical.get('rewrite_allowed') is False and historical.get('policy')=='READ_ONLY_HISTORICAL_EVIDENCE','D9.11 must preserve the historical C11-C manifest byte-for-byte')
    freeze_policy=maintenance.get('freeze_preparation',{})
    need(freeze_policy.get('mode')=='PREFLIGHT_ONLY' and freeze_policy.get('may_create_release_archive') is False,'D9.11 freeze preflight must not create release archives')
    data_classes=editorial.get('data_classes',{})
    editable=set(data_classes.get('editable_editorial',{}).get('editable_keys',[]))
    protected_fields=set()
    for group_name in ('derived_telemetry','provenance','simulation_truth'):
        group=data_classes.get(group_name,{})
        need(group.get('editable') is False,f'D9.8 protected class must remain non-editable: {group_name}')
        protected_fields.update(group.get('fields',[]))
    need(not editable.intersection(protected_fields),'D9.8 editable editorial keys overlap protected telemetry/provenance/simulation truth')
    return rows,errors

def profile_path(project_root: Path, profile_id: str) -> Path:
    if not isinstance(profile_id,str) or not PROFILE_ID_RE.fullmatch(profile_id) or profile_id in {'.','..'}: raise ValueError('profile_id must be a simple identifier; path traversal is forbidden')
    root=(project_root.resolve()/PROFILE_RELATIVE_ROOT).resolve(); path=(root/(profile_id+'.json')).resolve()
    try: path.relative_to(root)
    except ValueError as exc: raise ValueError('profile path escapes approved operator-profile root') from exc
    return path

def blank_profile(profile_id: str, label: str='') -> dict[str,Any]:
    return {'schema_id':'C11D-OPERATOR-CONFIG-PROFILE-V1','schema_version':'1.0','profile_id':profile_id,'label':label,
      'challenge_id':'','mode':'','seed':None,'music_seed':None,'delivery_profile_id':'','presentation_profile_id':'','music_profile_id':'',
      'audio_enabled':None,'personalization_profile_id':'','personalization_values':{},'runtime_authority':'NONE','renderer_execution':False,
      'production_execution':False,'release_authority':'NONE'}

def validate_operator_profile(profile: Any, project_root: Path, expected_profile_id: str|None=None) -> list[str]:
    errors=[]
    def need(ok,msg):
        if not ok: errors.append(msg)
    if not isinstance(profile,dict): return ['operator profile must be a JSON object']
    unknown=set(profile)-PROFILE_KEYS; missing=PROFILE_KEYS-set(profile)
    if unknown: errors.append('unknown fields forbidden: '+', '.join(sorted(unknown)))
    if missing: errors.append('required fields missing: '+', '.join(sorted(missing)))
    if unknown or missing: return errors
    need(profile.get('schema_id')=='C11D-OPERATOR-CONFIG-PROFILE-V1','schema_id mismatch')
    need(profile.get('schema_version')=='1.0','schema_version must be 1.0')
    try: profile_path(project_root,profile.get('profile_id'))
    except Exception as exc: errors.append(str(exc))
    if expected_profile_id is not None: need(profile.get('profile_id')==expected_profile_id,'profile_id must match file identity')
    need(isinstance(profile.get('label'),str) and 1<=len(profile['label'].strip())<=80,'label must contain 1–80 characters')
    try:
        req=read_json(project_root/'definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json')
        ch=next(x for x in req.get('fields',[]) if x.get('name')=='challenge_id').get('allowed_values',[])
        deliveries=next(x for x in req.get('fields',[]) if x.get('name')=='delivery_profile_id').get('evidence_values',[])
        music=read_json(project_root/'definitions/c11d/music/C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json')
        preg=read_json(project_root/'definitions/c11d/personalization/C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json')
    except Exception as exc: return errors+[f'canonical D3/D4 schemas unavailable: {exc}']
    need(profile.get('challenge_id') in ch,'challenge_id must resolve to canonical Challenge')
    need(profile.get('mode') in {'REVIEW','PRODUCTION'},'mode must be explicit REVIEW or PRODUCTION')
    for key in ('seed','music_seed'): need(isinstance(profile.get(key),int) and not isinstance(profile.get(key),bool),f'{key} must be an explicit integer; auto-seed forbidden')
    need(profile.get('delivery_profile_id') in deliveries,'delivery_profile_id must resolve to a canonical D4 profile')
    need(isinstance(profile.get('presentation_profile_id'),str) and bool(profile['presentation_profile_id'].strip()),'presentation_profile_id must be explicit; no silent default')
    need(profile.get('music_profile_id')==music.get('profile_id'),'music_profile_id must resolve to canonical D3 style')
    ps={x.get('profile_id'):x for x in preg.get('profiles',[]) if isinstance(x,dict)}; pid=profile.get('personalization_profile_id')
    need(pid in ps,'personalization_profile_id must resolve to D4 registry')
    vals=profile.get('personalization_values'); need(isinstance(vals,dict),'personalization_values must be an object')
    if isinstance(vals,dict) and pid in ps:
        p=ps[pid]; allowed=set(p.get('allowed_targets',[])); maximum=int(p.get('constraints',{}).get('max_string_length',160))
        if pid=='none_v1': need(not vals,'none_v1 cannot carry personalization values')
        for key,value in vals.items():
            need(key in allowed,f'field not allowed by {pid}: {key}')
            need(isinstance(value,str),f'personalization {key} must be a string')
            if isinstance(value,str): need(len(value)<=maximum,f'personalization {key} exceeds {maximum} chars')
    need(isinstance(profile.get('audio_enabled'),bool),'audio_enabled must be explicit boolean')
    need(profile.get('runtime_authority')=='NONE','runtime_authority must remain NONE')
    need(profile.get('renderer_execution') is False,'renderer_execution must remain false')
    need(profile.get('production_execution') is False,'production_execution must remain false')
    need(profile.get('release_authority')=='NONE','release_authority must remain NONE')
    return errors

def operator_profiles(project_root: Path) -> list[Path]:
    base=(project_root.resolve()/PROFILE_RELATIVE_ROOT).resolve()
    return sorted((p for p in base.glob('*.json') if p.is_file()),key=lambda p:p.name.lower()) if base.exists() else []


def save_operator_profile(project_root: Path, profile: dict[str, Any], allow_overwrite: bool = False,
                          expected_profile_id: str | None = None) -> Path:
    errors = validate_operator_profile(profile, project_root, expected_profile_id)
    if errors:
        raise ValueError("operator profile validation failed: " + "; ".join(errors))
    target = profile_path(project_root, profile["profile_id"])
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if not allow_overwrite:
            raise FileExistsError(str(target))
        shutil.copy2(target, Path(str(target) + ".bak"))
    payload = json.dumps(profile, ensure_ascii=False, indent=2) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=".c11d_config_", suffix=".tmp", dir=str(target.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return target


def restore_operator_profile_backup(project_root: Path, profile_id: str, authorized: bool = False) -> Path:
    if authorized is not True:
        raise PermissionError("restore requires explicit GUI/operator authorization")
    target = profile_path(project_root, profile_id)
    backup = Path(str(target) + ".bak")
    if not backup.is_file():
        raise FileNotFoundError(str(backup))
    candidate = read_json(backup)
    errors = validate_operator_profile(candidate, project_root, profile_id)
    if errors:
        raise ValueError("backup validation failed: " + "; ".join(errors))
    if target.exists():
        shutil.copy2(target, Path(str(target) + ".before_restore.bak"))
    shutil.copy2(backup, target)
    return target
