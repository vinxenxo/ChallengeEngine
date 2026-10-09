from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QProcess, QProcessEnvironment, Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

SUITE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(os.environ.get("C11C_PROJECT_ROOT", SUITE_ROOT.parent)).resolve()
sys.path.insert(0, str(SUITE_ROOT))
from common import CYBER_STYLE, human_size, open_path, powershell


@dataclass(frozen=True)
class Command:
    label: str
    path: str
    args: tuple[str, ...] = ()
    description: str = ""
    confirm: bool = False


D_COMMANDS = {
    "D2": (
        Command("D2.1 · HANDOFF REGISTRY", "tools/c11d/d2/run_d2_1_handoff_registry.ps1", confirm=True),
        Command("D2.2 · ROLE EVIDENCE", "tools/c11d/d2/run_d2_2_asset_role_evidence.ps1", confirm=True),
        Command("D2.3 · BINDING / CLOSE", "tools/c11d/d2/run_d2_3_canonical_binding_and_close_d2.ps1", confirm=True),
    ),
    "D3": (
        Command("D3.0 · MUSIC AUDIT", "tools/c11d/d3/run_d3_0_music_source_audit.ps1", confirm=True),
        Command("D3.1 · MUSIC ENGINE V5", "tools/c11d/d3/run_d3_1_shared_music_engine_v5.ps1", confirm=True),
        Command("D3.2 · DETERMINISTIC MUSIC", "tools/c11d/d3/run_d3_2_deterministic_music.ps1", confirm=True),
    ),
    "D4": (
        Command("D4.2 · NORMALIZE", "tools/c11d/d4/run_d4_2_normalization.ps1", description="Canonical production-request normalization.", confirm=True),
        Command("D4.4 · PLAN", "tools/c11d/d4/run_d4_4_canonical_orchestrator.ps1", description="Canonical deterministic production plan, plan-only.", confirm=True),
        Command("D4.6 · GUI ADAPTER", "tools/c11d/d4/run_d4_6_gui_adapter.ps1", description="Toolkit-independent GUI adapter contract.", confirm=True),
        Command("D4.7 · GUI/CLI PARITY", "tools/c11d/d4/run_d4_7_gui_cli_parity.ps1", description="GUI/CLI convergence proof.", confirm=True),
        Command("D4.8 · GOVERNANCE", "tools/c11d/d4/run_d4_8_activation_governance.ps1", description="Production activation governance; policy remains BLOCKED until explicitly changed by governance.", confirm=True),
        Command("D4.9 · ACCEPTANCE", "tools/c11d/d4/run_d4_9_full_acceptance.ps1", description="Full D4 acceptance.", confirm=True),
    ),
    "D5": (
        Command("D5.0 · TOPOLOGY AUDIT", "tools/c11d/d5/run_d5_0_artifact_topology_audit.ps1", confirm=True),
        Command("D5.1 · MANIFEST", "tools/c11d/d5/run_d5_1_canonical_artifact_manifest.ps1", confirm=True),
        Command("D5.2 · PROVENANCE", "tools/c11d/d5/run_d5_2_provenance_lineage_registry.ps1", confirm=True),
        Command("D5.3 · TOPOLOGY VALIDATOR", "tools/c11d/d5/run_d5_3_artifact_topology_validator.ps1", confirm=True),
        Command("D5.4 · LIFECYCLE", "tools/c11d/d5/run_d5_4_artifact_lifecycle_quarantine_rules.ps1", confirm=True),
        Command("D5.5 · ACCEPTANCE", "tools/c11d/d5/run_d5_5_full_d5_acceptance.ps1", confirm=True),
    ),
    "D6": (
        Command("D6.0 · SEED AUDIT", "tools/c11d/d6/run_d6_0_seed_governance_audit.ps1", confirm=True),
        Command("D6.1 · SEED REGISTRY", "tools/c11d/d6/run_d6_1_seed_registry_validator.ps1", confirm=True),
        Command("D6.2 · SEED RESOLVER", "tools/c11d/d6/run_d6_2_seed_resolver.ps1", confirm=True),
        Command("D6.3 · ISOLATION", "tools/c11d/d6/run_d6_3_seed_isolation_collision_validator.ps1", confirm=True),
        Command("D6.4 · REQUEST/PLAN", "tools/c11d/d6/run_d6_4_seed_request_plan_integrator.ps1", confirm=True),
        Command("D6.5 · ACCEPTANCE", "tools/c11d/d6/run_d6_5_full_d6_acceptance.ps1", confirm=True),
    ),
    "D7": (
        Command("D7.0 · MATRIX AUDIT", "tools/c11d/d7/run_d7_0_production_matrix_catalog_audit.ps1", confirm=True),
        Command("D7.1 · MATRIX", "tools/c11d/d7/run_d7_1_canonical_production_matrix.ps1", confirm=True),
        Command("D7.2 · COVERAGE", "tools/c11d/d7/run_d7_2_matrix_coverage_validator.ps1", confirm=True),
        Command("D7.3 · CATALOG", "tools/c11d/d7/run_d7_3_canonical_catalog.ps1", confirm=True),
        Command("D7.4 · IDENTITY", "tools/c11d/d7/run_d7_4_catalog_identity_provenance.ps1", confirm=True),
        Command("D7.5 · ACCEPTANCE", "tools/c11d/d7/run_d7_5_full_acceptance.ps1", confirm=True),
    ),
    "D8": (
        Command("D8.0 · INVENTORY", "tools/c11d/d8/run_d8_0_inventory.ps1", confirm=True),
        Command("D8.1 · FFPROBE", "tools/c11d/d8/run_d8_1_ffprobe_integrity.ps1", confirm=True),
        Command("D8.2 · VISUAL QA", "tools/c11d/d8/run_d8_2_visual_qa.ps1", confirm=True),
        Command("D8.3 · AUDIO QA", "tools/c11d/d8/run_d8_3_audio_qa.ps1", confirm=True),
        Command("D8.4 · ELIGIBILITY", "tools/c11d/d8/run_d8_4_artifact_eligibility.ps1", confirm=True),
        Command("D8.5 · RELEASE STAGING", "tools/c11d/d8/run_d8_5_release_manifest_staging.ps1", confirm=True),
        Command("D8.6 · RELEASE DRY RUN", "tools/c11d/d8/run_d8_6_release_dry_run.ps1", confirm=True),
        Command("D8.7 · ACCEPTANCE", "tools/c11d/d8/run_d8_7_acceptance_freeze.ps1", confirm=True),
    ),
    "D9": (
        Command("D9.0 · PREFLIGHT", "tools/c11d/d9/run_d9_0_media_pilot_preflight.ps1", (), "Controlled pilot preflight."),
        Command("D9.1 · REAL VIDEO PILOT", "tools/c11d/d9/run_d9_1_real_media_pilot.ps1", ("-AuthorizePilot",), "Single real-media pilot; explicit authorization required.", True),
        Command("D9.2 · A/V PILOT", "tools/c11d/d9/run_d9_2_audio_enabled_pilot.ps1", ("-AuthorizePilot",), "Deterministic audio-enabled real-media pilot.", True),
        Command("D9.3 · A/V REPEAT", "tools/c11d/d9/run_d9_3_deterministic_av_repeat.ps1", ("-AuthorizePilot",), "Exact repeatability plus negative controls.", True),
        Command("D9.4 · CHECKPOINT", "tools/c11d/d9/run_d9_4_acceptance_closure.ps1", ("-AuthorizeAcceptance",), "D9.4 acceptance checkpoint; not full D9 closure.", True),
    ),
}

D_RECEIPTS = {
    "D4": "artifacts/tests/c11d_d4/d4_9/d4_9_validation_receipt.json",
    "D5": "artifacts/tests/c11d_d5/d5_5/d5_5_acceptance_receipt.json",
    "D6": "artifacts/tests/c11d_d6/d6_5/d6_5_acceptance_receipt.json",
    "D7": "artifacts/tests/c11d_d7/d7_5/d7_5_acceptance_receipt.json",
    "D8": "artifacts/tests/c11d_d8/d8_7/d8_7_receipt.json",
    "D9": "artifacts/tests/c11d_d9/d9_4/evidence/d9_4_receipt.json",
}


class ConfirmDialog(QDialog):
    def __init__(self, title: str, body: str):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(560, 220)
        layout = QVBoxLayout(self)
        label = QLabel(body)
        label.setWordWrap(True)
        layout.addWidget(label)
        check = QCheckBox("Entiendo que la acción utiliza el runner canónico y respeta sus guardas.")
        layout.addWidget(check)
        box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        box.button(QDialogButtonBox.Yes).setEnabled(False)
        check.toggled.connect(lambda value: box.button(QDialogButtonBox.Yes).setEnabled(value))
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)


class ControlCenter(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("C11-D CONTROL CENTER · SUITE INTEGRATION")
        self.resize(1380, 900)
        self.proc: QProcess | None = None
        self.log_lines: list[str] = []
        self._build()
        self.refresh_status()

    def _build(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        outer = QHBoxLayout(root)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.setSpacing(8)

        nav = QVBoxLayout()
        nav_box = QGroupBox("C11-D / OPERATOR")
        nav_box.setLayout(nav)
        outer.addWidget(nav_box, 0)
        self.stack = QStackedWidget()
        outer.addWidget(self.stack, 1)

        pages = [
            ("OVERVIEW", self._overview_page),
            ("PRODUCTION", self._production_page),
            ("EVIDENCE", self._evidence_page),
            ("MEDIA / QA", self._media_page),
            ("OPERATIONS", self._operations_page),
            ("INTEGRATION MATRIX", self._matrix_page),
        ]
        for label, builder in pages:
            b = QPushButton(label)
            b.setMinimumHeight(42)
            b.clicked.connect(lambda _checked=False, idx=len(self._nav_buttons(nav)): self.stack.setCurrentIndex(idx))
            nav.addWidget(b)
            self._nav_buttons_list = getattr(self, "_nav_buttons_list", [])
            self._nav_buttons_list.append(b)
        nav.addStretch(1)
        note = QLabel("D10 permanece bloqueado hasta el certificado real de integración/GUI de D9.")
        note.setWordWrap(True)
        note.setObjectName("muted")
        nav.addWidget(note)

        for _, builder in pages:
            page = builder()
            self.stack.addWidget(page)

        self.statusBar().showMessage("C11-D control center listo")

    def _nav_buttons(self, _layout) -> list[QPushButton]:
        return getattr(self, "_nav_buttons_list", [])

    def _page(self, title: str, subtitle: str = "") -> tuple[QWidget, QVBoxLayout]:
        page = QWidget()
        layout = QVBoxLayout(page)
        title_label = QLabel(title)
        title_label.setObjectName("title")
        layout.addWidget(title_label)
        if subtitle:
            sub = QLabel(subtitle)
            sub.setObjectName("muted")
            sub.setWordWrap(True)
            layout.addWidget(sub)
        return page, layout

    def _overview_page(self) -> QWidget:
        page, layout = self._page(
            "C11-D / INTEGRATION OVERVIEW",
            "Una única superficie de operador sobre los contratos D. Las acciones ejecutan los runners canónicos; el GUI no reimplementa backend, RNG, render ni FFmpeg.",
        )
        grid = QGridLayout()
        layout.addLayout(grid)
        self.status_labels: dict[str, QLabel] = {}
        stages = [("D0-D3", "CLOSED"), ("D4", "CLOSED"), ("D5", "CLOSED"), ("D6", "CLOSED"), ("D7", "FROZEN"), ("D8", "CLOSED"), ("D9.4", "CHECKPOINT"), ("D10", "BLOCKED")]
        for i, (name, fallback) in enumerate(stages):
            box = QGroupBox(name)
            bl = QVBoxLayout(box)
            value = QLabel(fallback)
            value.setObjectName("title")
            bl.addWidget(value)
            self.status_labels[name] = value
            grid.addWidget(box, i // 4, i % 4)
        gov = QGroupBox("GOVERNANCE / NO SE NEGOCIA")
        gl = QGridLayout(gov)
        rows = [
            ("C11-C", "FROZEN / 2.19.12"),
            ("logical canvas", "540×960 · PROTECTED"),
            ("master_seed", "NOT_ADOPTED"),
            ("cross-domain seed sharing", "FORBIDDEN"),
            ("runtime derivation", "DISABLED"),
            ("D4.8", "BLOCKED BY POLICY"),
            ("release_authority", "NONE"),
            ("D9 status", "ACTIVE · INTEGRATION"),
        ]
        for r, (k, v) in enumerate(rows):
            gl.addWidget(QLabel(k), r, 0)
            gl.addWidget(QLabel(v), r, 1)
        layout.addWidget(gov)
        actions = QHBoxLayout()
        for label, fn in [
            ("REFRESCAR ESTADO", self.refresh_status),
            ("ABRIR TEST", lambda: self.launch_gui("c11c-test/main.py")),
            ("ABRIR PRODUCER", lambda: self.launch_gui("c11c-producer/main.py")),
            ("ABRIR CATALOG", lambda: self.launch_gui("c11c-catalog/main.py")),
            ("ABRIR MAINTENANCE", lambda: self.launch_gui("c11c-maintenance/main.py")),
            ("ABRIR CONFIG", lambda: self.launch_gui("c11c-config/main.py")),
        ]:
            b = QPushButton(label); b.clicked.connect(fn); actions.addWidget(b)
        layout.addLayout(actions)
        self.log = QPlainTextEdit(); self.log.setReadOnly(True); layout.addWidget(self.log, 1)
        return page

    def _production_page(self) -> QWidget:
        page, layout = self._page(
            "PRODUCTION / D4",
            "D4 personaliza y normaliza la producción; D4.8 continúa bloqueado. La producción física general no se habilita desde aquí. El Producer actual permanece como superficie operativa C11-C.",
        )
        info = QGroupBox("CURRENT PRODUCTION TRUTH")
        form = QFormLayout(info)
        for k, v in [("Production Request", "canonical / schema-backed"), ("Personalization", "canonical registry"), ("GUI/CLI", "parity proven in D4.7"), ("Physical general production", "BLOCKED by D4.8 policy"), ("D9 pilot", "explicit single-case authority")]:
            form.addRow(k, QLabel(v))
        layout.addWidget(info)
        layout.addLayout(self._command_group("D4 CANONICAL BACKEND", D_COMMANDS["D4"]))
        return page

    def _evidence_page(self) -> QWidget:
        page, layout = self._page("EVIDENCE / PROVENANCE / SEEDS / CATALOG", "D5, D6 y D7 quedan visibles como operator surfaces; todavía usamos los backends canónicos mientras se completan las vistas nativas.")
        split = QHBoxLayout(); layout.addLayout(split, 1)
        for phase in ("D2", "D3", "D5", "D6", "D7"):
            box = QGroupBox(phase)
            bl = QVBoxLayout(box)
            for cmd in D_COMMANDS[phase]:
                b = QPushButton(cmd.label); b.setToolTip(cmd.description); b.clicked.connect(lambda _=False, c=cmd: self.run_command(c)); bl.addWidget(b)
            split.addWidget(box)
        return page

    def _media_page(self) -> QWidget:
        page, layout = self._page("MEDIA / QA / REAL A/V", "D8 está cerrado como control-plane; D9.1–D9.3 ya probaron media real. D9.4 es un checkpoint, y D9 sigue abierto por integración.")
        layout.addLayout(self._command_group("D8", D_COMMANDS["D8"]))
        layout.addLayout(self._command_group("D9 PILOT / CHECKPOINT", D_COMMANDS["D9"]))
        return page

    def _operations_page(self) -> QWidget:
        page, layout = self._page("OPERATIONS", "Todas las operaciones sensibles mantienen las guardas del backend y requieren confirmación explícita cuando ejecutan un runner.")
        box = QGroupBox("ACTIVE SUITE SURFACES")
        grid = QGridLayout(box)
        ops = [
            ("TEST", "c11c-test/main.py"),
            ("PRODUCER", "c11c-producer/main.py"),
            ("CATALOG", "c11c-catalog/main.py"),
            ("CONFIG", "c11c-config/main.py"),
            ("MAINTENANCE", "c11c-maintenance/main.py"),
        ]
        for i, (label, path) in enumerate(ops):
            b = QPushButton(label); b.clicked.connect(lambda _=False, p=path: self.launch_gui(p)); grid.addWidget(b, i // 3, i % 3)
        layout.addWidget(box)
        suite = QGroupBox("SUITE STATIC / GUI CONTRACT CHECKS")
        sl = QVBoxLayout(suite)
        for label, path in [("SUITE SELF-TEST", "c11c-suite/self_test.py"), ("PRODUCER GUI CONTRACT", "c11c-suite/c11c-producer/test_producer_gui_contract.py")]:
            b = QPushButton(label); b.clicked.connect(lambda _=False, p=path: self.launch_python(p)); sl.addWidget(b)
        layout.addWidget(suite)
        return page

    def _matrix_page(self) -> QWidget:
        page, layout = self._page("D BRANCH → GUI COVERAGE", "La matriz canónica define qué debe aparecer en el operador. D9.5.0 hace visible y operable la primera capa; los checkpoints posteriores completan las vistas nativas.")
        table = QTableWidget(0, 5)
        table.setHorizontalHeaderLabels(["DOMAIN", "CAPABILITY", "GUI STATE", "CANONICAL BACKEND", "AUTHORITY"])
        matrix_path = PROJECT_ROOT / "definitions/c11d/d9/D9_SUITE_INTEGRATION_MATRIX_V1.json"
        rows = []
        try:
            data = json.loads(matrix_path.read_text(encoding="utf-8"))
            rows = [(str(x.get("domain", "")), str(x.get("capability", "")), str(x.get("gui_state", "")), str(x.get("canonical", "")), str(x.get("authority", ""))) for x in data.get("surfaces", [])]
        except Exception as exc:
            rows = [("D9.5.0", "Integration matrix unavailable", "FAIL", str(exc), "NONE")]
        table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row): table.setItem(r, c, QTableWidgetItem(value))
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table, 1)
        return page

    def _command_group(self, title: str, commands: tuple[Command, ...]) -> QVBoxLayout:
        layout = QVBoxLayout()
        box = QGroupBox(title)
        inner = QVBoxLayout(box)
        for cmd in commands:
            b = QPushButton(cmd.label)
            b.setToolTip(cmd.description)
            b.clicked.connect(lambda _=False, c=cmd: self.run_command(c))
            inner.addWidget(b)
        layout.addWidget(box)
        return layout

    def launch_gui(self, relative: str) -> None:
        script = PROJECT_ROOT / "c11c-suite" / relative.split("c11c-suite/")[-1]
        if not script.exists():
            QMessageBox.warning(self, "Suite", f"No existe:\n{script}")
            return
        proc = QProcess(self)
        env = QProcessEnvironment.systemEnvironment(); env.insert("C11C_PROJECT_ROOT", str(PROJECT_ROOT))
        proc.setProcessEnvironment(env); proc.setWorkingDirectory(str(PROJECT_ROOT)); proc.start(sys.executable, [str(script)])
        self._append(f"> GUI {relative}")

    def launch_python(self, relative: str) -> None:
        p = PROJECT_ROOT / relative
        if not p.exists(): QMessageBox.warning(self, "Suite", f"No existe:\n{p}"); return
        self._start_process(sys.executable, [str(p)], f"PYTHON {relative}", False)

    def run_command(self, cmd: Command) -> None:
        target = PROJECT_ROOT / cmd.path
        if not target.exists():
            QMessageBox.critical(self, "C11-D", f"Runner no encontrado:\n{target}")
            return
        if self.proc is not None:
            QMessageBox.information(self, "C11-D", "Ya hay una operación C11-D ejecutándose.")
            return
        if cmd.confirm:
            dialog = ConfirmDialog(cmd.label, f"Se ejecutará el runner canónico:\n\n{cmd.path}\n\n{cmd.description}\n\nNo se concede ninguna autoridad adicional por abrir este comando.")
            if dialog.exec() != QDialog.Accepted: return
        self._start_process(powershell(), ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(target), *cmd.args], cmd.label, True)

    def _start_process(self, executable: str, args: list[str], label: str, ps: bool) -> None:
        self.proc = QProcess(self)
        env = QProcessEnvironment.systemEnvironment(); env.insert("C11C_PROJECT_ROOT", str(PROJECT_ROOT))
        self.proc.setProcessEnvironment(env); self.proc.setWorkingDirectory(str(PROJECT_ROOT))
        self.proc.readyReadStandardOutput.connect(self._read_proc)
        self.proc.readyReadStandardError.connect(self._read_proc)
        self.proc.finished.connect(lambda code, status: self._finish_proc(code, label))
        self.proc.start(executable, args)
        self._append(f"> {label}")
        self.statusBar().showMessage(f"RUNNING · {label}")

    def _read_proc(self) -> None:
        if not self.proc: return
        for reader in (self.proc.readAllStandardOutput, self.proc.readAllStandardError):
            data = bytes(reader()).decode("utf-8", "replace")
            if data: self._append(data.rstrip())

    def _finish_proc(self, code: int, label: str) -> None:
        self._read_proc()
        self._append(f"[{label}] EXIT={code}")
        self.statusBar().showMessage(f"FINISHED · {label} · EXIT={code}")
        self.proc = None
        self.refresh_status()

    def _append(self, text: str) -> None:
        self.log_lines.append(text)
        self.log_lines = self.log_lines[-1000:]
        if hasattr(self, "log"): self.log.setPlainText("\n".join(self.log_lines)); self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

    def _read_json(self, relative: str):
        p = PROJECT_ROOT / relative
        if not p.exists(): return None
        try: return json.loads(p.read_text(encoding="utf-8"))
        except Exception: return None

    def refresh_status(self) -> None:
        for key, rel in D_RECEIPTS.items():
            data = self._read_json(rel)
            label = "NOT FOUND"
            if data:
                result = str(data.get("result", "?")); status = str(data.get("status", "?"))
                label = f"{result} / {status}"
            mapped = {"D4":"D4","D5":"D5","D6":"D6","D7":"D7","D8":"D8","D9":"D9.4"}.get(key)
            if mapped in getattr(self, "status_labels", {}): self.status_labels[mapped].setText(label)
        if "D10" in getattr(self, "status_labels", {}): self.status_labels["D10"].setText("BLOCKED UNTIL D9 GUI ACCEPTANCE")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(CYBER_STYLE)
    win = ControlCenter(); win.show(); sys.exit(app.exec())
