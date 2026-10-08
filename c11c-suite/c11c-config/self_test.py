from __future__ import annotations
import json,sys,tempfile,shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
PROJECT_ROOT=Path(__file__).resolve().parents[2]
from c11d_config import CONFIG_VERSION,D_REGISTRIES,registry_rows,validate_c11d_contracts,blank_profile,validate_operator_profile,profile_path,sha256_text,save_operator_profile,restore_operator_profile_backup,generic_editor_path_protected
rows,errors=validate_c11d_contracts(PROJECT_ROOT)
assert len(rows)==len(D_REGISTRIES) and len(rows)>=18,(len(rows),len(D_REGISTRIES))
assert not errors,'Contract/governance errors:\n'+'\n'.join(errors)
assert all(x['status']=='VALID_JSON' and len(x['sha256'])==64 for x in rows)
valid={'schema_id':'C11D-OPERATOR-CONFIG-PROFILE-V1','schema_version':'1.0','profile_id':'self_test_profile','label':'Self test profile','challenge_id':'CHALLENGE_001','mode':'REVIEW','seed':12345,'music_seed':840001,'delivery_profile_id':'REVIEW_720','presentation_profile_id':'social_default_v1','music_profile_id':'challenge_8bit_v1','audio_enabled':True,'personalization_profile_id':'editorial_text_v1','personalization_values':{'title':'Hola','language':'es'},'runtime_authority':'NONE','renderer_execution':False,'production_execution':False,'release_authority':'NONE'}
assert validate_operator_profile(valid,PROJECT_ROOT)==[]
assert len(sha256_text(json.dumps(valid,ensure_ascii=False,indent=2)))==64
negative=[]
def neg(name,mutator):
 data=json.loads(json.dumps(valid)); mutator(data); assert validate_operator_profile(data,PROJECT_ROOT),name+' unexpectedly passed'; negative.append(name)
neg('missing gameplay seed',lambda x:x.update(seed=None))
neg('boolean music seed',lambda x:x.update(music_seed=True))
neg('unknown editorial field',lambda x:x['personalization_values'].update(stealth='no'))
neg('renderer activation',lambda x:x.update(renderer_execution=True))
neg('release grant',lambda x:x.update(release_authority='GRANTED'))
neg('simulation input injection',lambda x:x.update(winning_frame=99))
try:profile_path(PROJECT_ROOT,'../escape')
except ValueError:negative.append('path traversal')
else:raise AssertionError('path traversal unexpectedly allowed')
empty=blank_profile('empty_profile')
assert empty['seed'] is None and empty['music_seed'] is None and empty['delivery_profile_id']==''
assert validate_operator_profile(empty,PROJECT_ROOT),'empty profile unexpectedly valid'
assert all(x['authority']=='READ_ONLY_CANONICAL' for x in rows)
protected_cases = [
    'challenges/CHALLENGE_001.json', 'definitions/c11d/d4.json',
    'schemas/example.json', 'assets/readme.txt', 'core/simulation.gd',
    'tools/c11d/runner.ps1', 'tests/test.py', 'c11c-suite/c11c-config/main.py',
    'profiles/delivery/social.json', 'profiles/c11d/operator/profile.json',
]
for rel in protected_cases:
    assert generic_editor_path_protected(PROJECT_ROOT, PROJECT_ROOT/rel), 'generic editor failed to protect '+rel
assert not generic_editor_path_protected(PROJECT_ROOT, PROJECT_ROOT/'docs/current/operator_notes.md')
assert generic_editor_path_protected(PROJECT_ROOT, PROJECT_ROOT.parent/'escape.json')
# Protected lexical roots remain protected even if a path might resolve through an alias.
assert generic_editor_path_protected(PROJECT_ROOT, PROJECT_ROOT/'c11c-suite/c11c-config/main.py')
# Schema reflects the strict helper field set.
from c11d_config import PROFILE_KEYS
schema=json.loads((PROJECT_ROOT/'definitions/c11d/config/C11D_OPERATOR_CONFIGURATION_SCHEMA_V1.json').read_text(encoding='utf-8'))
assert set(schema['required'])==PROFILE_KEYS
# Exercise actual explicit save -> backup -> validated restore without writing into the project tree.
with tempfile.TemporaryDirectory(prefix='c11d_config_selftest_') as tmp:
    temp_root=Path(tmp)
    for rel in ['definitions/c11d/production/C11D_PRODUCTION_REQUEST_SCHEMA_V1.json','definitions/c11d/music/C11D_CHALLENGE_8BIT_STYLE_PROFILE_V1.json','definitions/c11d/personalization/C11D_PERSONALIZATION_PROFILE_REGISTRY_V1.json']:
        dest=temp_root/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(PROJECT_ROOT/rel,dest)
    first=dict(valid); target=save_operator_profile(temp_root,first,allow_overwrite=False)
    original=target.read_bytes()
    changed=dict(first); changed['label']='Updated self test profile'
    save_operator_profile(temp_root,changed,allow_overwrite=True,expected_profile_id=target.stem)
    assert Path(str(target)+'.bak').read_bytes()==original
    restore_operator_profile_backup(temp_root,target.stem,authorized=True)
    assert target.read_bytes()==original and Path(str(target)+'.before_restore.bak').exists()
    try: restore_operator_profile_backup(temp_root,target.stem,authorized=False)
    except PermissionError: negative.append('restore requires explicit authorization')
    else: raise AssertionError('unauthorized backup restore unexpectedly passed')
negative.append('backup/save/validated restore lifecycle')
print(f'C11-C Config {CONFIG_VERSION} + C11-D governed configuration self-test PASS | registries={len(rows)}/{len(rows)} | negative={len(negative)-2}/7 | root_protection=PASS | save_backup_restore=PASS | auto_seed=false | renderer=false | release_authority=NONE')
