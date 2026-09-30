from __future__ import annotations
import ast, json, py_compile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SUITE=ROOT/'c11c-suite'
FILES=[
 'main.py','common.py',
 'c11c-test/main.py','c11c-test/run_all.bat','c11c-test/run_suite.bat','c11c-test/run_c11c_complete_review.bat','c11c-test/run_c11c_acceptance.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','test_retro_reference_contract.py','c11c-producer/test_gui_contract.bat','c11c-catalog/main.py','c11c-maintenance/main.py','c11c-config/main.py',
 'run.bat','test_retro_reference_contract.bat','c11c-catalog/run.bat','c11c-config/run.bat','c11c-maintenance/run.bat','c11c-maintenace/run.bat','c11c-producer/main.py','c11c-producer/self_test.py','c11c-producer/test_producer_gui_contract.py','c11c-producer/preflight.py','c11c-producer/run_visual_drill_production.ps1','c11c-producer/run.bat','c11c-maintenance/main.py','c11c-producer/test_gui_contract.bat','c11c-test/run.bat','c11c-test/run_all.bat','c11c-test/run_suite.bat',
]
for rel in FILES:
    p=SUITE/rel; assert p.exists(), p
for rel in [p for p in FILES if p.endswith('.py')]: py_compile.compile(str(SUITE/rel),doraise=True)
runall=(ROOT/'tests'/'run_all.py').read_text(encoding='utf-8-sig'); assert 'C11CProductionReviewCopySafetyTest.gd' in runall
assert 'C11A1FactoryIsolationContractTest.gd' in runall
assert 'C11CVisualLoopLongformSourceArtifactContractTest.gd' in runall
assert 'C11CParallelReviewWorkerIsolationContractTest.gd' in runall
assert 'C11CVisualDrillReviewEnvelopePathContractTest.gd' in runall
test_ui=(SUITE/'c11c-test'/'main.py').read_text(encoding='utf-8')
for command in ('PRODUCER SELF-TEST','PRODUCER GUI CONTRACT','RETRO REFERENCE CONTRACT','C11-C 2.19 CONSOLIDATED ACCEPTANCE','C11-C REVIEW PREP','C11-C PARALLEL WORKER CONTRACT','C11-C VISUAL DRILL ENVELOPE PATH CONTRACT','C11-C SUITE LAUNCHER AUDIT','C11-C COMPLETE VIDEO REVIEW','C11-C FOCUSED VALIDATION','C11-C ONE VIDEO EACH TYPE','C11-C DOCS CONSOLIDATION','SEED STRESS 32x2'):
    assert command in test_ui, command
assert 'run_c11c_complete_video_review.ps1' in test_ui
assert 'verify_c11c_suite_launchers.ps1' in test_ui
assert 'FULL_ACCEPTANCE_C11C_2.19.12.ps1' in test_ui
assert 'C11-C ACCEPTANCE LAUNCHER' in test_ui
assert 'C11-C 2.19.4 ACCEPTANCE' not in test_ui
assert 'C11-C 2.19.10 ACCEPTANCE' not in test_ui
assert "'-Workers', '7', '-All'" in test_ui
assert 'run_c11c_one_video_each_type.ps1' in test_ui
assert 'run_c11c_focused_validation.ps1' in test_ui
assert 'run_c11c_one_video_each_type.ps1' in test_ui
assert 'run_c11c_focused_validation.ps1' in test_ui
assert 'run_c11c_one_video_each_type.ps1' in test_ui
assert 'run_c11c_focused_validation.ps1' in test_ui
assert 'run_c11c_one_video_each_type.ps1' in test_ui
assert 'run_c11c_focused_validation.ps1' in test_ui
assert 'run_c11c_one_video_each_type.ps1' in test_ui
assert 'run_c11c_focused_validation.ps1' in test_ui
assert 'run_c11c_one_video_each_type.ps1' in test_ui
assert 'run_c11c_focused_validation.ps1' in test_ui
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
assert (ROOT/'FULL_ACCEPTANCE_C11C_2.19.12.ps1').exists()
assert (ROOT/'MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md').exists()
assert (ROOT/'START_PROMPT_C11C_2.19_CONSOLIDATED.md').exists()
assert (ROOT/'C11C_2.19.12_CONTEXT_INDEX.md').exists()
assert (ROOT/'docs'/'current'/'c11c'/'C11-C_2.19_DOCUMENTATION_INDEX.md').exists()
assert (ROOT/'docs'/'master-prompts'/'MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md').exists()
assert (ROOT/'docs'/'master-prompts'/'START_PROMPT_C11C_2.19_CONSOLIDATED.md').exists()
assert (ROOT/'tests'/'C11CParallelReviewWorkerIsolationContractTest.gd').exists()
assert (ROOT/'tests'/'C11CVisualDrillReviewEnvelopePathContractTest.gd').exists()
envelope_test=(ROOT/'tests'/'C11CVisualDrillReviewEnvelopePathContractTest.gd').read_text(encoding='utf-8-sig')
assert 'func _initialize() -> void:' in envelope_test
assert 'func _ready()' not in envelope_test
assert 'quit(0)\n        return' in envelope_test or 'quit(0)\n    return' in envelope_test
assert '[C11C_VISUAL_DRILL_ENVELOPE_PATH_CONTRACT_SUITE] PASS' in envelope_test
assert (ROOT/'tests'/'C11CParallelReviewWorkerIsolationContractTest.gd').exists()
envelope_test=(ROOT/'tests'/'C11CVisualDrillReviewEnvelopePathContractTest.gd').read_text(encoding='utf-8-sig')
assert 'func _initialize() -> void:' in envelope_test
assert 'func _ready()' not in envelope_test
assert 'quit(0)\n        return' in envelope_test or 'quit(0)\n    return' in envelope_test
assert '[C11C_VISUAL_DRILL_ENVELOPE_PATH_CONTRACT_SUITE] PASS' in envelope_test
assert (ROOT/'tests'/'C11CParallelReviewWorkerIsolationContractTest.gd').exists()
envelope_test=(ROOT/'tests'/'C11CVisualDrillReviewEnvelopePathContractTest.gd').read_text(encoding='utf-8-sig')
assert 'func _initialize() -> void:' in envelope_test
assert 'func _ready()' not in envelope_test
assert 'quit(0)\n        return' in envelope_test or 'quit(0)\n    return' in envelope_test
assert '[C11C_VISUAL_DRILL_ENVELOPE_PATH_CONTRACT_SUITE] PASS' in envelope_test
assert (ROOT/'tests'/'C11CParallelReviewWorkerIsolationContractTest.gd').exists()
envelope_test=(ROOT/'tests'/'C11CVisualDrillReviewEnvelopePathContractTest.gd').read_text(encoding='utf-8-sig')
assert 'func _initialize() -> void:' in envelope_test
assert 'func _ready()' not in envelope_test
assert 'quit(0)\n        return' in envelope_test or 'quit(0)\n    return' in envelope_test
assert '[C11C_VISUAL_DRILL_ENVELOPE_PATH_CONTRACT_SUITE] PASS' in envelope_test
assert (ROOT/'tests'/'C11CParallelReviewWorkerIsolationContractTest.gd').exists()
envelope_test=(ROOT/'tests'/'C11CVisualDrillReviewEnvelopePathContractTest.gd').read_text(encoding='utf-8-sig')
assert 'func _initialize() -> void:' in envelope_test
assert 'func _ready()' not in envelope_test
assert 'quit(0)\n        return' in envelope_test or 'quit(0)\n    return' in envelope_test
assert '[C11C_VISUAL_DRILL_ENVELOPE_PATH_CONTRACT_SUITE] PASS' in envelope_test
assert (ROOT/'tests'/'C11CParallelReviewWorkerIsolationContractTest.gd').exists()
envelope_test=(ROOT/'tests'/'C11CVisualDrillReviewEnvelopePathContractTest.gd').read_text(encoding='utf-8-sig')
assert 'func _initialize() -> void:' in envelope_test
assert 'func _ready()' not in envelope_test
assert 'quit(0)\n        return' in envelope_test or 'quit(0)\n    return' in envelope_test
assert '[C11C_VISUAL_DRILL_ENVELOPE_PATH_CONTRACT_SUITE] PASS' in envelope_test
assert (ROOT/'tests'/'C11CParallelReviewWorkerIsolationContractTest.gd').exists()
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_complete_video_review.ps1').exists()
assert (ROOT/'tools'/'qa'/'c11'/'verify_c11c_suite_launchers.ps1').exists()
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').exists()
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_focused_validation.ps1').exists()
smoke=(ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').read_text(encoding='utf-8-sig')
for token in ('run_prototype.ps1','run_c11c_visual_drill_review.ps1','run_c11c_visual_loop_longform_production.ps1','720','1280','30'):
    assert token in smoke, token
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').exists()
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_focused_validation.ps1').exists()
smoke=(ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').read_text(encoding='utf-8-sig')
for token in ('run_prototype.ps1','run_c11c_visual_drill_review.ps1','run_c11c_visual_loop_longform_production.ps1','720','1280','30'):
    assert token in smoke, token
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').exists()
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_focused_validation.ps1').exists()
smoke=(ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').read_text(encoding='utf-8-sig')
for token in ('run_prototype.ps1','run_c11c_visual_drill_review.ps1','run_c11c_visual_loop_longform_production.ps1','720','1280','30'):
    assert token in smoke, token
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').exists()
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_focused_validation.ps1').exists()
smoke=(ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').read_text(encoding='utf-8-sig')
for token in ('run_prototype.ps1','run_c11c_visual_drill_review.ps1','run_c11c_visual_loop_longform_production.ps1','720','1280','30'):
    assert token in smoke, token
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').exists()
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_focused_validation.ps1').exists()
smoke=(ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').read_text(encoding='utf-8-sig')
for token in ('run_prototype.ps1','run_c11c_visual_drill_review.ps1','run_c11c_visual_loop_longform_production.ps1','720','1280','30'):
    assert token in smoke, token
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').exists()
assert (ROOT/'tools'/'qa'/'c11'/'run_c11c_focused_validation.ps1').exists()
smoke=(ROOT/'tools'/'qa'/'c11'/'run_c11c_one_video_each_type.ps1').read_text(encoding='utf-8-sig')
for token in ('run_prototype.ps1','run_c11c_visual_drill_review.ps1','run_c11c_visual_loop_longform_production.ps1','720','1280','30'):
    assert token in smoke, token
assert (SUITE/'c11c-test'/'run_c11c_complete_review.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_acceptance.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_one_video_each_type.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_focused_validation.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_one_video_each_type.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_focused_validation.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_one_video_each_type.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_focused_validation.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_one_video_each_type.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_focused_validation.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_one_video_each_type.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_focused_validation.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_one_video_each_type.bat').exists()
assert (SUITE/'c11c-test'/'run_c11c_focused_validation.bat').exists()
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
assert 'WorkerRoot' in worker_helper
assert 'override.cfg' in worker_helper
operational_text=''.join(
    p.read_text(encoding='utf-8-sig', errors='ignore')
    for p in sorted(SUITE.rglob('*'))
    if p.is_file() and p.suffix.lower() in {'.py','.ps1','.bat','.cmd'} and p.name != 'self_test.py'
)
assert 'c11c-studio' not in operational_text
assert 'real 7-worker concurrency' in test_ui.lower() or 'real 7-worker' in test_ui.lower()
assert 'real 7-worker concurrency' in test_ui.lower() or 'real 7-worker' in test_ui.lower()
assert 'real 7-worker concurrency' in test_ui.lower() or 'real 7-worker' in test_ui.lower()
assert 'real 7-worker concurrency' in test_ui.lower() or 'real 7-worker' in test_ui.lower()
assert 'real 7-worker concurrency' in test_ui.lower() or 'real 7-worker' in test_ui.lower()
assert 'real 7-worker concurrency' in test_ui.lower() or 'real 7-worker' in test_ui.lower()
longform=(ROOT/'tools'/'prototypes'/'c11c_bulk'/'run_c11c_visual_loop_longform_production.ps1').read_text(encoding='utf-8-sig')
assert '$productionManifestPath' in longform
assert 'production_manifest.json' in longform
assert '-DeliveryProfile REVIEW_720' in longform
assert '$source.Manifest' not in longform
assert 'artifacts\\prototypes\\$production' in longform
assert (ROOT/'tools'/'maintenance'/'create_c11c_freeze_zip.ps1').exists()
assert 'GENERAR ZIP FROZEN C11-C 2.19.12' in (SUITE/'c11c-maintenance'/'main.py').read_text(encoding='utf-8')
print('C11-C Suite 0.1.4 + Producer 0.9.7 + C11-C 2.19.12 full consolidated contracts STATIC PASS')
