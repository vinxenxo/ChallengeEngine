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
assert 'APP_VERSION = "0.9.4"' in main_text
assert "failed_seeds" in main_text
assert "current_seed" in main_text
assert 'QProcess.ProcessError.FailedToStart' in main_text
assert 'REVIEW_CHALLENGES' in main_text
assert 'run_c11a1_challenge_bulk_qa.ps1' in main_text
assert 'self.proc.errorOccurred.connect(self._process_error)' in main_text

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

print("C11C_PRODUCER_GUI_CONTRACT_SUITE PASS")
