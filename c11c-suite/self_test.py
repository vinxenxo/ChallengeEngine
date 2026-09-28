from __future__ import annotations
import ast, json, py_compile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SUITE=ROOT/'c11c-suite'
FILES=[
 'main.py','common.py',
 'c11c-test/main.py','c11c-test/run_all.bat','c11c-test/run_suite.bat','test_retro_reference_contract.py','c11c-producer/test_gui_contract.bat','c11c-catalog/main.py','c11c-maintenance/main.py','c11c-config/main.py',
 'c11c-producer/main.py','c11c-producer/self_test.py','c11c-producer/test_producer_gui_contract.py','c11c-producer/preflight.py','c11c-producer/run_visual_drill_production.ps1',
]
for rel in FILES:
    p=SUITE/rel; assert p.exists(), p
for rel in [p for p in FILES if p.endswith('.py')]: py_compile.compile(str(SUITE/rel),doraise=True)
runall=(ROOT/'tests'/'run_all.py').read_text(encoding='utf-8-sig'); assert 'C11CProductionReviewCopySafetyTest.gd' in runall
assert 'C11A1FactoryIsolationContractTest.gd' in runall
assert 'C11CVisualLoopLongformSourceArtifactContractTest.gd' in runall
test_ui=(SUITE/'c11c-test'/'main.py').read_text(encoding='utf-8')
for command in ('PRODUCER SELF-TEST','PRODUCER GUI CONTRACT','RETRO REFERENCE CONTRACT','SEED STRESS 32×2'):
    assert command in test_ui, command
prod_schema=json.loads((SUITE/'c11c-producer'/'producer_schema.json').read_text(encoding='utf-8'))
assert any(x[0]=='REVIEW_CHALLENGES' for x in prod_schema.get('batch_operations', []))
prod=(ROOT/'tools'/'prototypes'/'c11c_bulk'/'run_c11c_production.ps1').read_text(encoding='utf-8-sig'); assert '$sourceFull=[System.IO.Path]::GetFullPath($sourceMp4)' in prod
assert '$finalFull=[System.IO.Path]::GetFullPath($finalMp4)' in prod
assert 'OrdinalIgnoreCase' in prod
manifest=json.loads((SUITE/'c11c-producer'/'BUILD_MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['version']=='0.9.7'
assert manifest['drill_launcher']=='c11c-suite/c11c-producer/run_visual_drill_production.ps1'
longform=(ROOT/'tools'/'prototypes'/'c11c_bulk'/'run_c11c_visual_loop_longform_production.ps1').read_text(encoding='utf-8-sig')
assert '$productionManifestPath' in longform
assert 'production_manifest.json' in longform
assert '-DeliveryProfile REVIEW_720' in longform
assert '$source.Manifest' not in longform
assert 'artifacts\\prototypes\\$production' in longform
print('C11-C Suite 0.1.3 + Producer 0.9.7 + Longform source contract STATIC PASS')
