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
