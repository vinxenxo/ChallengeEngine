from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
main=(HERE/'main.py').read_text(encoding='utf-8')
module=(HERE/'c11d_config.py').read_text(encoding='utf-8')
manifest=json.loads((HERE/'BUILD_MANIFEST.json').read_text(encoding='utf-8'))
for token in ('REPOSITORY CONFIG','C11-D CONTRACTS','C11-D OPERATOR PROFILES','VALIDAR TODOS LOS CONTRATOS D','VALIDAR + HASH','MOSTRAR DIFF','GUARDAR + BACKUP','RESTAURAR .BAK'):
 assert token in main,f'missing GUI surface/control: {token}'
for token in ('definitions/c11d/','cross_domain_seed_sharing','D8_MEDIA_SCOPE_V1.json','GENERIC_EDITOR_PROTECTED_PREFIXES','generic_editor_path_protected'):
 assert token in module,f'missing governed source/invariant: {token}'
assert 'profiles/' in main and "profiles/c11d/operator" in main, 'missing profile write-boundary rules'
assert 'def protected_path' in main and "definitions/" in module
assert 'generic_editor_path_protected(PROJECT_ROOT,path)' in main, 'generic Repository Config must delegate its protected-root gate'
assert 'save_operator_profile(PROJECT_ROOT' in main and 'restore_operator_profile_backup(PROJECT_ROOT' in main, 'dedicated operator-profile actions missing'
assert 'os.replace(temporary, target)' in module and 'shutil.copy2(target, Path(str(target) + ".bak"))' in module
assert manifest['version']=='0.2.0' and manifest['renderer_activation'] is False and manifest['production_execution'] is False and manifest['release_authority']=='NONE'
assert "PROFILE_RELATIVE_ROOT = Path('profiles') / 'c11d' / 'operator'" in module and 'path.relative_to(root)' in module
assert 'D9_UNIVERSAL_EDITORIAL_MODEL' in module and 'C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json' in module
assert manifest.get('universal_editorial_model_access') == 'READ_ONLY_CANONICAL'
assert 'D9_EDITORIAL_RENDER_BRIDGE' in module and 'C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json' in module, 'D9.10 bridge contract must be visible in read-only Config registry'
assert manifest.get('editorial_render_bridge_contract') == 'definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json'
assert manifest.get('editorial_render_bridge_contract_access') == 'READ_ONLY_CANONICAL'
assert 'D9_MAINTENANCE_POLICY' in module and 'D9_11_MAINTENANCE_POLICY_V1.json' in module
assert manifest.get('maintenance_policy') == 'definitions/c11d/d9/D9_11_MAINTENANCE_POLICY_V1.json'
assert manifest.get('maintenance_policy_access') == 'READ_ONLY_CANONICAL'
lifecycle_contract = ROOT / 'definitions/c11d/d9/D9_13_CROSS_SUITE_LIFECYCLE_V1.json' if 'ROOT' in globals() else (HERE.parents[1] / 'definitions/c11d/d9/D9_13_CROSS_SUITE_LIFECYCLE_V1.json')
assert lifecycle_contract.is_file()
assert 'D9_CROSS_SUITE_LIFECYCLE' in module
assert manifest.get('cross_suite_lifecycle_contract_access') == 'READ_ONLY_CANONICAL'
d914_contract = HERE.parents[1] / 'definitions/c11d/d9/D9_14_GUI_REAL_MEDIA_CERTIFICATION_GATE_V1.json'
assert d914_contract.is_file() and 'D9_REAL_MEDIA_CERTIFICATION_GATE' in module
assert manifest.get('d9_14_certification_gate_access') == 'READ_ONLY_CANONICAL'
assert manifest.get('d9_14_renderer_activation') is False and manifest.get('d9_14_production_execution') is False and manifest.get('d9_14_release_authority') == 'NONE'
operational_contract = HERE.parents[1] / 'definitions/c11d/d9/D9_15_GUI_OPERATIONAL_ACCEPTANCE_V1.json'
assert operational_contract.is_file() and 'D9_GUI_OPERATIONAL_ACCEPTANCE' in module
assert manifest.get('d9_15_operational_acceptance_contract') == 'definitions/c11d/d9/D9_15_GUI_OPERATIONAL_ACCEPTANCE_V1.json'
assert manifest.get('d9_15_operational_acceptance_contract_access') == 'READ_ONLY_CANONICAL'
assert manifest.get('d9_15_operational_acceptance_closed') is False and manifest.get('d9_15_renderer_activation') is False and manifest.get('d9_15_media_created') is False and manifest.get('d9_15_d4_8') == 'BLOCKED' and manifest.get('d9_15_release_authority') == 'NONE'
assert 'BLOCKED_UNTIL_FUTURE_D_FROZEN_BASELINE_AND_D4_8_AUTHORIZATION' in d914_contract.read_text(encoding='utf-8')
print('C11C_CONFIG_GUI_CONTRACT PASS | version=0.2.0 | canonical_contracts=READ_ONLY | D9.10 bridge + D9.11 maintenance + D9.13 lifecycle + D9.14 blocked gate + D9.15 operational matrix registered | profiles=ALLOWLISTED | diff/hash/backup/restore=EXPOSED | execution=false')
