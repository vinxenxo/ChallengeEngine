from __future__ import annotations
import ast, json, py_compile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SUITE=ROOT/'c11c-suite'
FILES=[
 'main.py','common.py',
 'c11c-test/main.py','c11c-test/run_all.bat','c11c-test/run_suite.bat','c11c-catalog/main.py','c11c-maintenance/main.py','c11c-config/main.py',
 'c11c-producer/main.py','c11c-producer/self_test.py','c11c-producer/preflight.py','c11c-producer/run_visual_drill_production.ps1',
]
for rel in FILES:
    p=SUITE/rel; assert p.exists(), p
for rel in [p for p in FILES if p.endswith('.py')]: py_compile.compile(str(SUITE/rel),doraise=True)
runall=(ROOT/'tests'/'run_all.py').read_text(encoding='utf-8-sig'); assert 'C11CProductionReviewCopySafetyTest.gd' in runall
assert 'C11CVisualLoopLongformSourceArtifactContractTest.gd' in runall
prod=(ROOT/'tools'/'prototypes'/'c11c_bulk'/'run_c11c_production.ps1').read_text(encoding='utf-8-sig'); assert '$sourceFull=[System.IO.Path]::GetFullPath($sourceMp4)' in prod
assert '$finalFull=[System.IO.Path]::GetFullPath($finalMp4)' in prod
assert 'OrdinalIgnoreCase' in prod
manifest=json.loads((SUITE/'c11c-producer'/'BUILD_MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['version']=='0.9.1'
assert manifest['drill_launcher']=='c11c-suite/c11c-producer/run_visual_drill_production.ps1'
longform=(ROOT/'tools'/'prototypes'/'c11c_bulk'/'run_c11c_visual_loop_longform_production.ps1').read_text(encoding='utf-8-sig')
assert '$productionManifestPath' in longform
assert 'production_manifest.json' in longform
assert '-DeliveryProfile REVIEW_720' in longform
assert '$source.Manifest' not in longform
assert 'artifacts\\prototypes\\$production' in longform
print('C11-C Suite 0.1.2 + Producer relocation + Longform source contract STATIC PASS')
