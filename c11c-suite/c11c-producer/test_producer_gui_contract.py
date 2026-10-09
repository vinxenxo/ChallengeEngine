from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
MAIN = ROOT / "main.py"
DRILL = ROOT / "run_visual_drill_production.ps1"
SCHEMA = ROOT / "producer_schema.json"

main_text = MAIN.read_text(encoding="utf-8")
tree = ast.parse(main_text)
manifest = json.loads((ROOT / "BUILD_MANIFEST.json").read_text(encoding="utf-8"))
assert 'APP_VERSION = "0.11.1"' in main_text
assert "failed_seeds" in main_text
assert "current_seed" in main_text
assert 'QProcess.ProcessError.FailedToStart' in main_text
assert 'REVIEW_CHALLENGES' in main_text
assert 'run_c11c_challenge_bulk_qa.ps1' in main_text
assert 'run_c11a1_challenge_bulk_qa.ps1' not in main_text
assert 'self.proc.errorOccurred.connect(self._process_error)' in main_text
assert 'C11-D · REQUEST + PERSONALIZACIÓN' in main_text
assert 'C11-D · EDITORIAL UNIVERSAL (D9.9)' in main_text
assert 'EDITORIAL → RENDER BRIDGE (PLAN ONLY)' in main_text
assert 'D-ONLY RENDER ADAPTER (PREPARED / OFF)' in main_text
assert 'prepare_d9_d_only_adapter_envelope(result, bridge_record, PROJECT)' in main_text
assert 'd_render_adapter_envelope.json' in main_text
assert 'd_only_adapter_envelope_equal' in main_text
assert 'renderer_dispatch_invoked' in main_text
assert 'build_d9_bridge_planning_record(result, PROJECT)' in main_text
assert 'bridge_planning_record_equal' in main_text
assert 'editorial_render_bridge_plan.json' in main_text
assert 'from d_render_adapter import prepare_d_only_adapter_envelope' in main_text
assert 'def _build_d9_universal_editorial_tab' in main_text
assert 'D9.14 REAL-MEDIA CERTIFICATION PREFLIGHT · NO MEDIA' in main_text
assert 'D9.14 · REAL-MEDIA CERTIFICATION GATE (BLOCKED)' in main_text
assert 'def _run_d914_certification_preflight(' in main_text
assert 'build_d914_certification_gate(PROJECT)' in main_text
assert 'validate_d914_certification_gate(gate, PROJECT)' in main_text
assert 'self.d9_scope.currentIndexChanged.connect(self._d9_universal_scope_changed)' in main_text
assert 'def _d9_universal_scope_changed(' in main_text

# Catch runtime AttributeError regressions: every MainWindow self-method used as
# a Qt signal callback must actually exist on MainWindow (static text checks alone
# previously missed a missing scope-change handler).
main_window = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'MainWindow')
main_window_methods = {node.name for node in main_window.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
missing_callbacks = set()
for node in ast.walk(main_window):
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute) or node.func.attr != 'connect' or not node.args:
        continue
    callback = node.args[0]
    if isinstance(callback, ast.Attribute) and isinstance(callback.value, ast.Name) and callback.value.id == 'self':
        if callback.attr.startswith('_') and callback.attr not in main_window_methods:
            missing_callbacks.add(callback.attr)
assert not missing_callbacks, f'Qt callbacks reference missing MainWindow methods: {sorted(missing_callbacks)}'
assert 'D9_UNIVERSAL.evaluate_universal_request(raw_request, PROJECT)' in main_text
assert 'universal_producer_cli.py' in main_text
assert 'canonical_request_equal' in main_text and 'plan_hash_equal' in main_text
assert 'Longform · DESHABILITADO' in main_text
assert 'release_authority' in main_text and 'renderer OFF' in main_text
assert 'build_production_request' in main_text
assert 'evaluate_gui_request' in main_text
assert '_verify_c11d_planning_predecessors' in main_text
assert 'D4.8 = BLOCKED' in main_text
assert 'production_execution' in main_text
helper_text = (ROOT / 'c11d_gui_request.py').read_text(encoding='utf-8')
assert 'gui_production_adapter.py' in helper_text or 'gui_production_adapter' in helper_text
assert 'production_cli.py' in helper_text or 'production_cli' in helper_text
assert 'renderer_activation_false' in helper_text
assert 'release_authority' in helper_text

# The old blocking behavior is prohibited: a per-seed failure must not clear all pending jobs.
finish = main_text[main_text.index('    def _finish_error'):main_text.index('    def _done', main_text.index('    def _finish_error'))]
seed_branch = finish[finish.index('if recipe.operation == "A_LA_CARTA"'):finish.index('        # Batch/utility failure:')]
assert 'self.jobs = []' not in seed_branch, 'Per-seed failure must preserve pending jobs.'
assert 'self._run_challenge_job()' in seed_branch
assert 'self._run_content_job()' in seed_branch
assert 'QMessageBox.critical' not in finish

schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
ops = {row[0]: row[1] for row in schema["batch_operations"]}
assert "REVIEW_CHALLENGES" in ops
assert "CHALLENGES" in ops["REVIEW_CHALLENGES"]

ps = DRILL.read_text(encoding="utf-8-sig")
assert "[Diagnostics.ProcessStartInfo]::new()" in ps
assert "OS.get_cmdline_user_args" in (ROOT / "C11CVisualDrillProducerEnvelopeGenerator.gd").read_text(encoding="utf-8")
assert "generator_stdout.log" in ps
assert "generator_stderr.log" in ps
assert "Visual Drill envelope generator returned no response" in ps

assert manifest.get('d9_14_real_media_execution') is False and manifest.get('d9_14_renderer_activation') is False and manifest.get('d9_14_release_authority') == 'NONE'
print("C11C_PRODUCER_GUI_CONTRACT_SUITE PASS | Producer 0.11.1 | D9.9 universal editorial + D9.10 D-only adapter prepare-only + D9.14 fail-closed certification gate wired to canonical backend; definitive GUI remains deferred")
