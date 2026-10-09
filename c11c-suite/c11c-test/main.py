from __future__ import annotations

import ast
import os
import shutil
import sys
from pathlib import Path

from PySide6.QtCore import QProcess
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import PROJECT_ROOT, CYBER_STYLE, qprocess_environment, powershell


C11_COMMANDS = [
    ('FULL LOGICAL', 'python', ['./tests/run_all.py'], 'Todas las suites registradas (KNOWN_SUITES).'),
    ('LEGACY C11 FREEZE GATE', 'ps', ['tools/c11freeze/run_all.ps1'], 'Historical low-level freeze regression: core + C11 + logical + retro + physical + stress.'),
    ('CORE', 'ps', ['tools/c11freeze/run_core_suite.ps1'], 'RNG / mechanics / DDI.'),
    ('C11 CONTRACTS', 'ps', ['tools/c11freeze/run_c11_suite.ps1'], 'Contratos C11-B.'),
    ('RETROCOMPATIBILITY', 'ps', ['tools/c11freeze/run_retrocompatibility.ps1'], '54-run comparison.'),
    ('PHYSICAL EXPORT', 'ps', ['tools/c11freeze/run_physical_export_suite.ps1'], 'Physical smoke + export.'),
    ('C11-A.1 HISTORICAL CHALLENGE QA', 'ps', ['tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1'], 'Historical compatibility/regression route: 9×6 challenge matrix.'),
    ('PRODUCER SELF-TEST', 'python', ['./c11c-suite/c11c-producer/self_test.py'], 'Producer package/static contract checks.'),
    ('PRODUCER GUI CONTRACT', 'python', ['./c11c-suite/c11c-producer/test_producer_gui_contract.py'], 'Producer queue, review and drill-launch contracts.'),
    ('RETRO REFERENCE CONTRACT', 'python', ['./c11c-suite/test_retro_reference_contract.py'], 'Immutable C11-A.1 reference bundle.'),
    ('C11-A HISTORICAL VISUAL QA', 'ps', ['tools/qa/c11/run_c11a_visual_bulk_qa.ps1'], 'Historical visual qualification route; not current C11-C review authority.'),
    ('ART DIRECTION ALL', 'ps', ['tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1', '-Workers', '7', '-All'], 'Current review corpus with real 7-worker loop concurrency.'),
    ('ART DIRECTION LONGFORMS', 'ps', ['tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1', '-Longforms'], '5 × 180s longforms.'),
    ('LONGFORM BULK', 'ps', ['tools/prototypes/c11c_bulk/run_c11c_visual_loop_longform_production_bulk.ps1'], 'Canonical 5-family longform bulk production.'),
    ('REPOSITORY LAYOUT', 'ps', ['tools/maintenance/verify_repository_layout.ps1'], 'Repository structure contract.'),
    ('C11-C 2.19 CONSOLIDATED ACCEPTANCE', 'ps', ['FULL_ACCEPTANCE_C11C_2.19.12.ps1'], 'Consolidated C11-C 2.19 acceptance gate.'),
    ('C11-C ACCEPTANCE LAUNCHER', 'bat', ['c11c-suite/c11c-test/run_c11c_acceptance.bat'], 'Canonical full acceptance launcher.'),
    ('C11-C REVIEW PREP', 'ps', ['tools/maintenance/prepare_c11c_acceptance_workspace.ps1', '-RotateAcceptanceRoots'], 'Quarantine prior acceptance outputs without deleting evidence.'),
    ('C11-C PARALLEL WORKER CONTRACT', 'godot', ['--headless', '--path', '.', '--script', './tests/C11CParallelReviewWorkerIsolationContractTest.gd'], 'Static contract for genuine parallel Art Direction worker isolation.'),
    ('C11-C VISUAL DRILL ENVELOPE PATH CONTRACT', 'godot', ['--headless', '--path', '.', '--script', './tests/C11CVisualDrillReviewEnvelopePathContractTest.gd'], 'Static contract for absolute Visual Drill review envelope roots and 17s/21s durations.'),
    ('C11-C FOCUSED VALIDATION', 'ps', ['tools/qa/c11/run_c11c_focused_validation.ps1'], 'Contratos enfocados + smoke de 3 vídeos; no ejecuta la revisión completa.'),
    ('C11-C ONE VIDEO EACH TYPE', 'ps', ['tools/qa/c11/run_c11c_one_video_each_type.ps1'], 'Smoke físico de 3 vídeos: Visual Loop + Visual Drill + Longform.'),
    ('C11-C SUITE LAUNCHER AUDIT', 'ps', ['tools/qa/c11/verify_c11c_suite_launchers.ps1'], 'Verify active suite launchers and retired studio separation.'),
    ('C11-C POWERSHELL PARSE', 'bat', ['c11c-suite/c11c-test/test_powershell_parse.bat'], 'Parse all active PowerShell scripts with Windows PowerShell 5.1.'),
    ('C11-C COMPLETE VIDEO REVIEW', 'ps', ['tools/qa/c11/run_c11c_complete_video_review.ps1', '-Workers', '7'], 'Validate/generate the complete 52-video C11-C review corpus; preserves a COMPLETE corpus instead of forcing a reset.'),
    ('C11-C DOCS CONSOLIDATION', 'ps', ['tools/maintenance/consolidate_c11c_2_19_documentation.ps1'], 'Archive superseded 2.19.x documentation into historical evidence.'),
    ('C11-C FREEZE DRY RUN', 'ps', ['tools/maintenance/create_c11c_freeze_zip.ps1', '-DryRun'], 'Validate acceptance, root cleanliness, build_factory lineage and frozen-package exclusions without creating a ZIP.'),
    ('C11-C FREEZE PACKAGE', 'bat', ['c11c-suite/c11c-maintenance/run_freeze_package.bat'], 'Create the sealed C11-C 2.19.12 frozen archive through the canonical Maintenance packager.'),
    ('C11-C CLEANUP CONTRACT', 'python', ['./c11c-suite/c11c-maintenance/test_cleanup_contract.py'], 'Static safety contract for artifact cleanup and frozen-package exclusions.'),
    ('SEED STRESS 32x2', 'python', ['tools/c11freeze/run_seed_stress.py'], 'Deterministic seed stress regression.'),
    # C11-D D9.12: additive D contract and acceptance routes, backed by existing canonical commands.
    ('D2 ASSET FAMILY / BINDING REGISTRY', 'ps', ['tools/c11d/d2/validate_d2_1_registry.ps1'], 'Read/validate D2 declarative asset-family registry; no production execution.'),
    ('D2 ASSET ROLE / EVIDENCE', 'ps', ['tools/c11d/d2/validate_d2_2_asset_role_evidence_v2.ps1'], 'Validate D2 role/evidence contracts.'),
    ('D3 MUSIC V5 DETERMINISM', 'ps', ['tools/c11d/d3/run_d3_2_deterministic_music.ps1'], 'D3 procedural music determinism contract.'),
    ('D4 REQUEST / PERSONALIZATION ACCEPTANCE', 'python', ['tools/c11d/d4/d4_full_acceptance.py'], 'Canonical D4 request, personalization and plan acceptance; D4.8 remains governed.'),
    ('D4 GUI/CLI PLAN PARITY', 'ps', ['tools/c11d/d4/run_d4_7_gui_cli_parity.ps1'], 'Canonical D4 GUI/CLI normalized request and plan parity.'),
    ('D4.8 ACTIVATION GOVERNANCE (BLOCKED GATE)', 'ps', ['tools/c11d/d4/run_d4_8_activation_governance.ps1'], 'Verify activation remains blocked without an explicit governance checkpoint.'),
    ('D5 PROVENANCE / ARTIFACT LIFECYCLE', 'python', ['tools/c11d/d5/full_d5_acceptance.py'], 'Canonical D5 topology, manifests, provenance and lifecycle acceptance.'),
    ('D6 SEED GOVERNANCE / ISOLATION', 'python', ['tools/c11d/d6/full_d6_acceptance.py'], 'Canonical gameplay/music seed governance and cross-domain isolation checks.'),
    ('D7 CATALOG IDENTITY / PROVENANCE', 'ps', ['tools/c11d/d7/run_d7_4_catalog_identity_provenance.ps1'], 'Canonical D7 identity and provenance builder/validator route.'),
    ('CATALOG 0.2.0 SELF-TEST', 'python', ['./c11c-suite/c11c-catalog/self_test.py'], 'C11-D product identity, provenance, media receipts and reproduction checks.'),
    ('D8 VISUAL MEDIA QA', 'ps', ['tools/c11d/d8/run_d8_2_visual_qa.ps1'], 'Visual QA only against governed D8 scope.'),
    ('D8 AUDIO MEDIA QA', 'ps', ['tools/c11d/d8/run_d8_3_audio_qa.ps1'], 'Audio QA only against governed D8 scope.'),
    ('D8 RELEASE DRY-RUN (NO RELEASE)', 'ps', ['tools/c11d/d8/run_d8_6_release_dry_run.ps1'], 'Non-authoritative release dry-run; must not create release products or grant authority.'),
    ('D9.8 UNIVERSAL EDITORIAL MODEL', 'python', ['tools/c11d/d9/test_universal_editorial_model.py'], 'Universal editorial model inventory, resolver and negative controls.'),
    ('D9.9 UNIVERSAL PRODUCER / GUI-CLI', 'python', ['tools/c11d/d9/test_universal_producer.py'], 'Universal selectors, canonical plan parity and unsupported-field negatives.'),
    ('D9.10 EDITORIAL-RENDER BRIDGE (PLAN ONLY)', 'python', ['tools/c11d/d9/test_editorial_render_bridge.py'], 'Bridge record parity; renderer input and media output remain absent.'),
    ('D9.11 MAINTENANCE 0.2.0', 'python', ['tools/c11d/d9/test_maintenance.py'], 'Dry-run, reversible allowlists, quarantine/restore and immutable manifest guards.'),
    ('D9 NEGATIVE ACCEPTANCE BUNDLE', 'python', ['tools/c11d/d9/test_d9_negative_acceptance.py'], 'Run the canonical D9.8–D9.11 negative matrices without duplicating backend logic.'),
    ('D9 GUI/CLI PARITY BUNDLE', 'python', ['tools/c11d/d9/test_d9_gui_cli_parity.py'], 'Aggregate universal Producer and render-bridge process parity.'),
    ('D9 REAL-MEDIA GUI CERTIFICATION PREFLIGHT (NO MEDIA)', 'python', ['tools/c11d/d9/test_gui_e2e_certification_plan.py'], 'Plan preflight only; NO MEDIA is created, and real-media operator execution is gated and not started.'),
    ('D9.12 TEST 0.2.0 INTEGRATION CONTRACT', 'python', ['./c11c-suite/c11c-test/test_d9_test_integration.py'], 'Validate canonical D2–D9 route registry, protected topology and test GUI contract.'),
    ('D9.13 CROSS-SUITE LIFECYCLE CHAIN', 'python', ['tools/c11d/d9/test_cross_suite_lifecycle.py'], 'Verify one canonical plan-only identity across Config, Producer, Test, Catalog and Maintenance; no media or release.'),
    ('D9.14 REAL GUI PRODUCTION CERTIFICATION GATE (BLOCKED)', 'python', ['tools/c11d/d9/test_gui_real_media_certification.py'], 'Evaluate the real-media GUI certification gate only; it remains BLOCKED and creates no media until future D renderer baseline + explicit D4.8 authorization.'),
    ('D9.15 GUI OPERATIONAL ACCEPTANCE PREFLIGHT (PLAN ONLY)', 'python', ['tools/c11d/d9/test_gui_operational_acceptance.py'], 'Inspect readiness of Config, Producer, Test, Catalog, provenance, logs, Maintenance and reproducibility; requires explicit operator GUI evidence and creates no media.'),
    ('D9.16 FULL D9 ACCEPTANCE PREFLIGHT (NO MEDIA)', 'python', ['tools/c11d/d9/test_full_acceptance.py'], 'Aggregate D9.8–D9.16 evidence wiring; full acceptance remains BLOCKED until authorized real-media evidence and five-surface operator GUI evidence exist; creates no media.'),
    ('D BASELINE CANDIDATE INTEGRITY PREFLIGHT (NO FREEZE)', 'python', ['tools/c11d/baseline_candidate/test_d_baseline_candidate.py'], 'Audit D as a future frozen-baseline candidate while preserving immutable C11-C; no freeze archive, renderer, media or release authority.'),
]


def known_suites() -> list[tuple[str, str]]:
    run_all = PROJECT_ROOT / 'tests' / 'run_all.py'
    text = run_all.read_text(encoding='utf-8-sig')
    tree = ast.parse(text)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'KNOWN_SUITES':
                value = ast.literal_eval(node.value)
                return sorted((str(path), str(marker)) for path, marker in value.items())
    return []


def godot_executable() -> str:
    return shutil.which('godot') or os.environ.get('GODOT_BIN', 'godot')


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('C11-C TEST · Test 0.2.0')
        self.resize(1200, 760)
        self.proc: QProcess | None = None

        root = QWidget()
        self.setCentralWidget(root)
        layout = QHBoxLayout(root)
        left = QVBoxLayout()
        right = QVBoxLayout()
        layout.addLayout(left, 1)
        layout.addLayout(right, 3)

        title = QLabel('TEST / QA')
        title.setObjectName('title')
        left.addWidget(title)

        self.full = QListWidget()
        for name, _kind, _args, description in C11_COMMANDS:
            self.full.addItem(f'{name} — {description}')
        left.addWidget(self.full, 2)

        self.run = QPushButton('EJECUTAR')
        self.run.clicked.connect(self.run_command)
        left.addWidget(self.run)

        box = QGroupBox(f'Suites individuales ({len(known_suites())})')
        box_layout = QVBoxLayout(box)
        self.suites = QListWidget()
        for path, _marker in known_suites():
            self.suites.addItem(path)
        box_layout.addWidget(self.suites)
        selected = QPushButton('EJECUTAR SUITE SELECCIONADA')
        selected.clicked.connect(self.run_selected)
        box_layout.addWidget(selected)
        left.addWidget(box, 3)

        opts = QGroupBox('Seed Stress')
        opts_layout = QHBoxLayout(opts)
        self.limit = QSpinBox()
        self.limit.setRange(0, 999)
        self.limit.setValue(0)
        self.repeat = QSpinBox()
        self.repeat.setRange(1, 9)
        self.repeat.setValue(2)
        opts_layout.addWidget(QLabel('Seed limit'))
        opts_layout.addWidget(self.limit)
        opts_layout.addWidget(QLabel('Repeat'))
        opts_layout.addWidget(self.repeat)
        left.addWidget(opts)

        self.verbose = QCheckBox('VERBOSE')
        self.verbose.setToolTip('Añade --verbose al runner lógico.')
        left.addWidget(self.verbose)

        self.status = QLabel('IDLE')
        self.status.setObjectName('muted')
        right.addWidget(self.status)
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        right.addWidget(self.log, 1)

    def append(self, value: str) -> None:
        self.log.appendPlainText(value.rstrip())

    def start(self, program: str, args: list[str], label: str) -> None:
        if self.proc is not None:
            self.append('[TEST] Ya hay un proceso ejecutándose.')
            return
        self.log.clear()
        self.append('[TEST] ' + label)
        self.append('> ' + program + ' ' + ' '.join(args))
        self.status.setText('RUNNING')
        self.run.setEnabled(False)
        self.proc = QProcess(self)
        self.proc.setProcessEnvironment(qprocess_environment())
        self.proc.setWorkingDirectory(str(PROJECT_ROOT))
        self.proc.setProgram(program)
        self.proc.setArguments(args)
        self.proc.readyReadStandardOutput.connect(self.read_output)
        self.proc.readyReadStandardError.connect(self.read_output)
        self.proc.finished.connect(self.done)
        self.proc.start()

    def read_output(self) -> None:
        if self.proc is None:
            return
        out = bytes(self.proc.readAllStandardOutput()).decode('utf-8', errors='replace')
        err = bytes(self.proc.readAllStandardError()).decode('utf-8', errors='replace')
        if out:
            self.append(out)
        if err:
            self.append('[STDERR] ' + err)

    def done(self, code: int, status: QProcess.ExitStatus) -> None:
        self.read_output()
        self.append(f'\n[TEST] EXIT={code} STATUS={status}')
        self.status.setText('PASS' if code == 0 else f'FAIL ({code})')
        self.run.setEnabled(True)
        process = self.proc
        self.proc = None
        if process:
            process.deleteLater()

    def run_command(self) -> None:
        row = self.full.currentRow()
        if row < 0:
            return
        name, kind, args, _description = C11_COMMANDS[row]
        final_args = list(args)
        if name == 'SEED STRESS 32x2':
            final_args = [
                'tools/c11freeze/run_seed_stress.py',
                '--repeat', str(self.repeat.value()),
                '--retries', '3',
            ]
            if self.limit.value() > 0:
                final_args += ['--limit', str(self.limit.value())]
        if name == 'FULL LOGICAL' and self.verbose.isChecked():
            final_args.append('--verbose')
        if kind == 'bat':
            self.start('cmd.exe', ['/c'] + final_args, name)
        elif kind == 'ps':
            self.start(powershell(), ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File'] + final_args, name)
        elif kind == 'godot':
            self.start(godot_executable(), final_args, name)
        else:
            self.start(sys.executable, ['-u'] + final_args, name)

    def run_selected(self) -> None:
        item = self.suites.currentItem()
        if item is None:
            return
        rel = item.text()
        suite_path = PROJECT_ROOT / 'tests' / rel
        if not suite_path.exists():
            self.append(f'[TEST] No existe la suite: {suite_path}')
            self.status.setText('FAIL')
            return
        self.start(godot_executable(), ['--headless', '--path', str(PROJECT_ROOT), '--script', str(suite_path)], rel)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(CYBER_STYLE)
    window = Window()
    window.show()
    raise SystemExit(app.exec())
