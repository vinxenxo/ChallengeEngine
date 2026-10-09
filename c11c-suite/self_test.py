from __future__ import annotations
import ast, json, py_compile, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SUITE=ROOT/'c11c-suite'
FILES=[
 'main.py','common.py',
 'c11c-test/main.py','c11c-test/run_all.bat','c11c-test/run_suite.bat','c11c-test/run_c11c_complete_review.bat','c11c-test/run_c11c_acceptance.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','c11c-test/run_c11c_one_video_each_type.bat','c11c-test/run_c11c_focused_validation.bat','test_retro_reference_contract.py','c11c-producer/test_gui_contract.bat','c11c-catalog/main.py','c11c-catalog/c11d_catalog.py','c11c-catalog/self_test.py','c11c-catalog/test_catalog_gui_contract.py','c11c-catalog/BUILD_MANIFEST.json','c11c-catalog/c11d_catalog.py','c11c-catalog/self_test.py','c11c-catalog/test_catalog_gui_contract.py','c11c-catalog/BUILD_MANIFEST.json','c11c-maintenance/main.py','c11c-config/main.py','c11c-config/c11d_config.py','c11c-config/self_test.py','c11c-config/test_config_gui_contract.py','c11c-config/BUILD_MANIFEST.json',
 'run.bat','test_retro_reference_contract.bat','c11c-catalog/run.bat','c11c-config/run.bat','c11c-maintenance/run.bat','c11c-producer/main.py','c11c-producer/self_test.py','c11c-producer/test_producer_gui_contract.py','c11c-producer/c11d_gui_request.py','c11c-producer/test_d9_producer_integration.py','c11c-producer/preflight.py','c11c-producer/run_visual_drill_production.ps1','c11c-producer/run.bat','c11c-maintenance/main.py','c11c-producer/test_gui_contract.bat','c11c-test/run.bat','c11c-test/run_all.bat','c11c-test/run_suite.bat',
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
assert 'LEGACY C11 FREEZE GATE' in test_ui
assert 'C11-A.1 HISTORICAL CHALLENGE QA' in test_ui
assert 'C11-A HISTORICAL VISUAL QA' in test_ui
assert 'tools/maintenance/prepare_c11c_acceptance_workspace.ps1' in test_ui

for command in ('PRODUCER SELF-TEST','PRODUCER GUI CONTRACT','RETRO REFERENCE CONTRACT','C11-C 2.19 CONSOLIDATED ACCEPTANCE','C11-C REVIEW PREP','C11-C PARALLEL WORKER CONTRACT','C11-C VISUAL DRILL ENVELOPE PATH CONTRACT','C11-C SUITE LAUNCHER AUDIT','C11-C COMPLETE VIDEO REVIEW','C11-C FOCUSED VALIDATION','C11-C ONE VIDEO EACH TYPE','C11-C DOCS CONSOLIDATION','C11-C FREEZE DRY RUN','C11-C FREEZE PACKAGE','C11-C CLEANUP CONTRACT','SEED STRESS 32x2'):
    assert command in test_ui, command
assert 'run_c11c_complete_video_review.ps1' in test_ui
assert "'tools/qa/c11/run_c11c_complete_video_review.ps1', '-Workers', '7'" in test_ui
assert "'tools/maintenance/create_c11c_freeze_zip.ps1', '-DryRun'" in test_ui
assert "'c11c-suite/c11c-maintenance/run_freeze_package.bat'" in test_ui
assert 'test_cleanup_contract.py' in test_ui
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
assert "FREEZE C11-C · DRY RUN" in (SUITE/'c11c-maintenance'/'main.py').read_text(encoding='utf-8')
assert "run_visual_drill_production.ps1" in (SUITE/'c11c-producer'/'BUILD_MANIFEST.json').read_text(encoding='utf-8')
prod_schema=json.loads((SUITE/'c11c-producer'/'producer_schema.json').read_text(encoding='utf-8'))
assert any(x[0]=='REVIEW_CHALLENGES' for x in prod_schema.get('batch_operations', []))
prod=(ROOT/'tools'/'prototypes'/'c11c_bulk'/'run_c11c_production.ps1').read_text(encoding='utf-8-sig'); assert '$sourceFull=[System.IO.Path]::GetFullPath($sourceMp4)' in prod
assert '$finalFull=[System.IO.Path]::GetFullPath($finalMp4)' in prod
assert 'OrdinalIgnoreCase' in prod
manifest=json.loads((SUITE/'c11c-producer'/'BUILD_MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['version']=='0.11.1'
assert manifest['d_request_tab'] is True
assert manifest['d_request_runtime_execution'] is False
assert manifest['d_request_release_authority']=='NONE'
assert manifest['drill_launcher']=='c11c-suite/c11c-producer/run_visual_drill_production.ps1'
assert (ROOT/'FULL_ACCEPTANCE_C11C_2.19.12.ps1').exists()
assert (ROOT/'docs'/'master-prompts'/'MASTER_HANDOVER_C11C_2.19_CONSOLIDATED.md').exists()
assert (ROOT/'docs'/'master-prompts'/'START_PROMPT_C11C_2.19_CONSOLIDATED.md').exists()
assert (ROOT/'docs'/'current'/'c11c'/'C11-C_2.19_DOCUMENTATION_INDEX.md').exists()
assert (ROOT/'docs'/'current'/'c11c'/'C11-C_2.19.12_PREFREEZE_HARDENING_REPORT.md').exists()
assert (ROOT/'docs'/'current'/'c11c'/'C11-C_2.19.12_ACCEPTANCE_EVIDENCE.md').exists()
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

# Final operator-surface parity/readiness checks. These are static only: they do not
# execute application logic or alter runtime/mechanics.
assert not (SUITE / 'c11c-maintenace').exists(), 'Obsolete misspelled maintenance alias must be quarantined before freeze.'
maint_text = (SUITE / 'c11c-maintenance' / 'main.py').read_text(encoding='utf-8-sig')
for target in (
    'tools/maintenance/consolidate_c11c_2_19_documentation.ps1',
    'tools/maintenance/organize_repository_root.ps1',
    'tools/maintenance/create_c11c_freeze_zip.ps1',
    'tools/prototypes/c11c_bulk/clean_c11c_artifacts.ps1',
):
    assert target in maint_text or target.replace('tools/', '') in maint_text, target
assert (ROOT / 'tools' / 'maintenance' / 'create_c11c_freeze_zip.ps1').exists()
assert (ROOT / 'c11c-suite' / 'c11c-maintenance' / 'run_freeze_package.bat').exists()
assert (ROOT / 'c11c-suite' / 'c11c-maintenance' / 'organize_repository_root.bat').exists()

# Every path declared by the Suite Test GUI command registry must exist. This guards
# GUI/CLI drift while leaving all canonical target scripts untouched.
test_tree = ast.parse(test_ui)
commands = []
for node in ast.walk(test_tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'C11_COMMANDS':
                try:
                    commands = ast.literal_eval(node.value)
                except Exception:
                    commands = []
                break
if commands:
    for _name, kind, args, _desc in commands:
        if kind in {'ps', 'bat', 'godot'}:
            for arg in args:
                if isinstance(arg, str) and ('/' in arg or '\\' in arg) and not arg.startswith('-'):
                    candidate = ROOT / arg
                    if candidate.suffix.lower() in {'.ps1', '.bat', '.cmd', '.gd'}:
                        assert candidate.exists(), f'Suite GUI command target missing: {arg}'
        elif kind == 'python':
            for arg in args:
                if isinstance(arg, str) and (arg.startswith('./') or arg.endswith('.py')):
                    candidate = ROOT / arg.replace('./', '', 1)
                    if candidate.suffix.lower() == '.py':
                        assert candidate.exists(), f'Suite GUI Python target missing: {arg}'

assert (ROOT/'docs'/'current'/'suite'/'C11C_SUITE_CURRENT_RULES.md').exists()
assert (ROOT/'docs'/'current'/'suite'/'C11C_SUITE_TOOLING_MATRIX.md').exists()
# The shared launcher must expose exactly the five approved operational surfaces.
shell_tree = ast.parse((SUITE/'main.py').read_text(encoding='utf-8-sig'))
app_rows = None
for node in ast.walk(shell_tree):
    if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'APPS' for target in node.targets):
        app_rows = ast.literal_eval(node.value)
        break
assert app_rows is not None, 'Suite launcher APPS registry not found'
expected_apps = {'c11c-test/main.py', 'c11c-catalog/main.py', 'c11c-maintenance/main.py', 'c11c-config/main.py', 'c11c-producer/main.py'}
actual_apps = {row[1] for row in app_rows}
assert actual_apps == expected_apps, f'Non-canonical Suite topology: {actual_apps}'
assert len(app_rows) == 5 and all(row[0] != 'C11-D CONTROL' for row in app_rows)

editorial_test = subprocess.run([sys.executable, str(ROOT/'tools'/'c11d'/'d9'/'test_universal_editorial_model.py')], cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8')
assert editorial_test.returncode == 0, editorial_test.stdout + '\n' + editorial_test.stderr
assert 'challenge=9/9' in editorial_test.stdout and 'loops=5 families/27 grammars' in editorial_test.stdout and 'drills=4 types/20 tiers' in editorial_test.stdout and 'negative=25/25' in editorial_test.stdout

integration = subprocess.run([sys.executable, str(SUITE/'c11c-producer'/'test_d9_producer_integration.py')], cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8')
assert integration.returncode == 0, integration.stdout + '\n' + integration.stderr
assert 'core=90/90' in integration.stdout and 'personalization=12/12' in integration.stdout and 'negative=4/4' in integration.stdout
universal_producer = subprocess.run([sys.executable, str(ROOT/'tools'/'c11d'/'d9'/'test_universal_producer.py')], cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8', timeout=120)
assert universal_producer.returncode == 0, universal_producer.stdout + '\n' + universal_producer.stderr
assert 'challenge=9/9' in universal_producer.stdout and 'loop_selectors=32' in universal_producer.stdout and 'drill_variants=20/20' in universal_producer.stdout and 'GUI/CLI parity=3/3' in universal_producer.stdout and 'negative=20/20' in universal_producer.stdout
producer_gui_contract = subprocess.run([sys.executable, str(SUITE/'c11c-producer'/'test_producer_gui_contract.py')], cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8', timeout=30)
assert producer_gui_contract.returncode == 0, producer_gui_contract.stdout + '\n' + producer_gui_contract.stderr
assert 'Producer 0.11.1' in producer_gui_contract.stdout and 'D9.10 bridge planning' in producer_gui_contract.stdout
bridge_test = subprocess.run([sys.executable, str(ROOT/'tools'/'c11d'/'d9'/'test_editorial_render_bridge.py')], cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8', timeout=120)
assert bridge_test.returncode == 0, bridge_test.stdout + '\n' + bridge_test.stderr
assert 'content_types=3/3' in bridge_test.stdout and 'CLI bridge parity=3/3' in bridge_test.stdout and 'negative=15/15' in bridge_test.stdout
catalog_test = subprocess.run([sys.executable, str(SUITE/'c11c-catalog'/'self_test.py')], cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8')
assert catalog_test.returncode == 0, catalog_test.stdout + '\n' + catalog_test.stderr
assert 'pilot_media=5/5' in catalog_test.stdout and 'negative_controls=5/5' in catalog_test.stdout
catalog_contract = subprocess.run([sys.executable, str(SUITE/'c11c-catalog'/'test_catalog_gui_contract.py')], cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8')
assert catalog_contract.returncode == 0, catalog_contract.stdout + '\n' + catalog_contract.stderr
assert 'version=0.2.0' in catalog_contract.stdout
config_test = subprocess.run([sys.executable, str(SUITE/'c11c-config'/'self_test.py')], cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8')
assert config_test.returncode == 0, config_test.stdout + '\n' + config_test.stderr
assert 'registries=' in config_test.stdout and 'negative=7/7' in config_test.stdout
config_contract = subprocess.run([sys.executable, str(SUITE/'c11c-config'/'test_config_gui_contract.py')], cwd=str(ROOT), capture_output=True, text=True, encoding='utf-8')
assert config_contract.returncode == 0, config_contract.stdout + '\n' + config_contract.stderr
assert 'version=0.2.0' in config_contract.stdout
config_manifest = json.loads((SUITE/'c11c-config'/'BUILD_MANIFEST.json').read_text(encoding='utf-8'))
assert config_manifest['version'] == '0.2.0' and config_manifest['release_authority'] == 'NONE'
print('C11-C Suite 0.1.4 + Producer 0.11.1 + Catalog 0.2.0 + Config 0.2.0 + C11-C 2.19.12 + D9.5.1/D9.6/D9.7/D9.8/D9.9/D9.10 editorial bridge planning PASS')

