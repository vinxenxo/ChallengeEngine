from __future__ import annotations
import ast, json, py_compile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SUITE=ROOT/'c11c-suite'
FILES=[
 'main.py','common.py',
 'c11c-test/main.py','c11c-test/run_all.bat','c11c-test/run_suite.bat','test_retro_reference_contract.py','c11c-producer/test_gui_contract.bat','c11c-catalog/main.py','c11c-maintenance/main.py','c11c-config/main.py',
 'run.bat','test_retro_reference_contract.bat','c11c-catalog/run.bat','c11c-config/run.bat','c11c-maintenance/run.bat','c11c-maintenace/run.bat','c11c-producer/main.py','c11c-producer/self_test.py','c11c-producer/test_producer_gui_contract.py','c11c-producer/preflight.py','c11c-producer/run_visual_drill_production.ps1','c11c-producer/run.bat','c11c-maintenance/main.py','c11c-producer/test_gui_contract.bat','c11c-test/run.bat','c11c-test/run_all.bat','c11c-test/run_suite.bat',
]
for rel in FILES:
    p=SUITE/rel; assert p.exists(), p
for rel in [p for p in FILES if p.endswith('.py')]: py_compile.compile(str(SUITE/rel),doraise=True)
runall=(ROOT/'tests'/'run_all.py').read_text(encoding='utf-8-sig'); assert 'C11CProductionReviewCopySafetyTest.gd' in runall
assert 'C11A1FactoryIsolationContractTest.gd' in runall
assert 'C11CVisualLoopLongformSourceArtifactContractTest.gd' in runall
assert 'C11CParallelReviewWorkerIsolationContractTest.gd' in runall
launcher_expectations={
    'run.bat':['C11C_PROJECT_ROOT','main.py','cd /d'],
    'c11c-test/run.bat':['C11C_PROJECT_ROOT','main.py','cd /d'],
    'c11c-test/run_all.bat':['C11C_PROJECT_ROOT','tests\\run_all.py'],
    'c11c-test/run_suite.bat':['C11C_PROJECT_ROOT','--headless','--path'],
    'c11c-producer/run.bat':['C11C_PROJECT_ROOT','main.py','cd /d'],
    'c11c-producer/test_gui_contract.bat':['C11C_PROJECT_ROOT','cd /d','test_producer_gui_contract.py'],
    'c11c-maintenance/run.bat':['C11C_PROJECT_ROOT','main.py','cd /d'],
    'c11c-catalog/run.bat':['C11C_PROJECT_ROOT','main.py','cd /d'],
    'c11c-config/run.bat':['C11C_PROJECT_ROOT','main.py','cd /d'],
    'test_retro_reference_contract.bat':['C11C_PROJECT_ROOT','cd /d','test_retro_reference_contract.py'],
    'c11c-maintenace/run.bat':['call','c11c-maintenance\\run.bat'],
}

for rel,markers in launcher_expectations.items():
    launcher=(SUITE/rel).read_text(encoding='utf-8-sig')
    for marker in markers: assert marker in launcher, f'{rel} missing launcher marker: {marker}'
parallel_test=(ROOT/'tests'/'C11CParallelReviewWorkerIsolationContractTest.gd').read_text(encoding='utf-8-sig')
assert 'extends SceneTree' in parallel_test
assert 'func _initialize() -> void:' in parallel_test
assert 'func _ready() -> void:' not in parallel_test
test_ui=(SUITE/'c11c-test'/'main.py').read_text(encoding='utf-8')
for command in ('PRODUCER SELF-TEST','PRODUCER GUI CONTRACT','RETRO REFERENCE CONTRACT','C11-C 2.19.6 ACCEPTANCE','C11-C REVIEW PREP','C11-C DOCS CONSOLIDATION','C11-C FREEZE SEAL 2.19.6','SEED STRESS 32×2'):
    assert command in test_ui, command
assert "'-Workers', '7', '-All'" in test_ui
assert "run_c11c_art_direction_batch_v4.ps1" in (SUITE/'c11c-producer'/'main.py').read_text(encoding='utf-8')
assert "run_c11c_art_direction_batch_v4.ps1" in (SUITE/'c11c-producer'/'producer_schema.json').read_text(encoding='utf-8')
assert "consolidate_c11c_2_19_documentation.ps1" in (SUITE/'c11c-maintenance'/'main.py').read_text(encoding='utf-8')
assert "c11c-maintenance\\run.bat" in (SUITE/'c11c-maintenace'/'run.bat').read_text(encoding='utf-8')
assert "run_visual_drill_production.ps1" in (SUITE/'c11c-producer'/'BUILD_MANIFEST.json').read_text(encoding='utf-8')
prod_schema=json.loads((SUITE/'c11c-producer'/'producer_schema.json').read_text(encoding='utf-8'))
assert any(x[0]=='REVIEW_CHALLENGES' for x in prod_schema.get('batch_operations', []))
prod=(ROOT/'tools'/'prototypes'/'c11c_bulk'/'run_c11c_production.ps1').read_text(encoding='utf-8-sig'); assert '$sourceFull=[System.IO.Path]::GetFullPath($sourceMp4)' in prod
assert '$finalFull=[System.IO.Path]::GetFullPath($finalMp4)' in prod
assert 'OrdinalIgnoreCase' in prod
manifest=json.loads((SUITE/'c11c-producer'/'BUILD_MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['version']=='0.9.7'
assert manifest['drill_launcher']=='c11c-suite/c11c-producer/run_visual_drill_production.ps1'
assert (ROOT/'FULL_ACCEPTANCE_C11C_2.19.6.ps1').exists()
assert (ROOT/'tools'/'c11freeze'/'finalize_c11c_2_19_6_freeze.ps1').exists()
assert (ROOT/'C11C_2.19.6_CONTEXT_INDEX.md').exists()
assert (ROOT/'docs'/'current'/'c11c'/'C11-C_2.19.6_DOCUMENTATION_INDEX.md').exists()
assert (ROOT/'tests'/'C11CParallelReviewWorkerIsolationContractTest.gd').exists()
assert (SUITE/'c11c-producer'/'C11C_PRODUCER_MASTER_HANDOVER_2026-09-28.md').exists()
assert (SUITE/'c11c-producer'/'C11C_PRODUCER_START_PROMPT_2026-09-28.md').exists()
docs_consolidation=ROOT/'tools'/'maintenance'/'consolidate_c11c_2_19_documentation.ps1'
assert docs_consolidation.exists()
maint=(SUITE/'c11c-maintenance'/'main.py').read_text(encoding='utf-8')
assert 'consolidate_c11c_2_19_documentation.ps1' in maint
worker_batch=(ROOT/'tools'/'prototypes'/'c11c_bulk'/'run_c11c_art_direction_batch_v4.ps1').read_text(encoding='utf-8-sig')
worker_helper=(ROOT/'tools'/'prototypes'/'c11c_bulk'/'C11CReviewWorkerIsolation.ps1').read_text(encoding='utf-8-sig')
assert 'New-C11CReviewWorkerPool' in worker_batch
assert 'WorkerRoot' in worker_batch
assert 'C11-C-WORKER' in worker_batch
assert 'powershell.exe @ChildArgs' not in worker_batch
assert 'Mutex' not in worker_batch and 'Mutex' not in worker_helper
assert '$i:' not in worker_helper and '${i}' in worker_helper
assert 'Initialize-C11CReviewWorkerProject' in worker_helper
assert "'--headless','--editor'" in worker_helper
assert "'--quit'" in worker_helper
assert 'global_script_class_cache.cfg' in worker_helper
assert 'PresentationProfile' in worker_helper
assert 'GODOT_BIN' in worker_helper
assert "Join-Path $sourceRoot 'c11c-studio'" in worker_helper
operational_text=''.join(
    p.read_text(encoding='utf-8-sig', errors='ignore')
    for p in sorted(SUITE.rglob('*'))
    if p.is_file() and p.suffix.lower() in {'.py','.ps1','.bat','.cmd'} and p.name != 'self_test.py'
)
assert 'c11c-studio' not in operational_text
for required in launcher_expectations:
    assert (SUITE/required).is_file(), required
longform=(ROOT/'tools'/'prototypes'/'c11c_bulk'/'run_c11c_visual_loop_longform_production.ps1').read_text(encoding='utf-8-sig')
assert '$productionManifestPath' in longform
assert 'production_manifest.json' in longform
assert '-DeliveryProfile REVIEW_720' in longform
assert '$source.Manifest' not in longform
assert 'artifacts\\prototypes\\$production' in longform
print('C11-C Suite 0.1.4 + Producer 0.9.7 + C11-C 2.19.6 final-repair contracts STATIC PASS')
