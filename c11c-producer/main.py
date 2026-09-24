from __future__ import annotations
import hashlib
import json
import os
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PySide6.QtCore import QProcess, QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDoubleSpinBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox,
    QPlainTextEdit, QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget
)

APP_VERSION = '0.3.0'
ROOT = Path(__file__).resolve().parent
PROJECT = Path(os.environ.get('C11C_PROJECT_ROOT', ROOT.parent)).resolve()
SCHEMA = json.loads((ROOT / 'producer_schema.json').read_text(encoding='utf-8'))
FAMILIES = SCHEMA['families']
EXPECTED_PROFILE_SHA = SCHEMA['backend_profile_sha256']


def labelize(key: str) -> str:
    return key.replace('_', ' ').strip().title()


@dataclass
class Recipe:
    family: str
    grammar: str
    count: int
    manual_seeds: list[int]
    no_sound: bool
    no_footer: bool
    force: bool
    targets: dict[str, Any]


class ParamRow(QWidget):
    def __init__(self, spec: dict[str, Any]) -> None:
        super().__init__()
        self.spec = spec
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(7)
        self.label = QLabel(spec.get('label', labelize(spec['key'])))
        self.label.setMinimumWidth(132)
        self.label.setToolTip(f"Valor derivado por seed en C11-C 2.9.1. {spec['key']}")
        self.mode = QComboBox()
        self.mode.addItems(['ALEATORIO', 'FIJAR'])
        self.mode.setFixedWidth(105)
        if spec['kind'] == 'enum':
            self.editor = QComboBox()
            vals = [v for v in spec.get('values', []) if str(v).upper() != 'AUTO (SEED)']
            self.editor.addItems([str(v) for v in vals])
            if vals:
                self.editor.setCurrentIndex(0)
        else:
            self.editor = QDoubleSpinBox()
            self.editor.setRange(float(spec['min']), float(spec['max']))
            self.editor.setSingleStep(float(spec['step']))
            step = float(spec['step'])
            if step < 0.00001:
                decimals = 7
            elif step < 0.001:
                decimals = 5
            elif step < 0.01:
                decimals = 4
            else:
                decimals = 2
            self.editor.setDecimals(decimals)
            self.editor.setValue((float(spec['min']) + float(spec['max'])) / 2.0)
        self.editor.setEnabled(False)
        self.editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        lay.addWidget(self.label)
        lay.addWidget(self.mode)
        lay.addWidget(self.editor, 1)
        self.mode.currentIndexChanged.connect(self._sync)
        self.setMinimumHeight(42)

    def _sync(self, index: int) -> None:
        self.editor.setEnabled(index == 1)

    def value(self) -> Any:
        if self.mode.currentIndex() == 0:
            return None
        if self.spec['kind'] == 'enum':
            raw = self.editor.currentData()
            if raw is None:
                raw = self.editor.currentText()
            try:
                return int(raw)
            except (ValueError, TypeError):
                return raw
        return float(self.editor.value())


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f'C11-C Producer {APP_VERSION}')
        self.resize(1440, 930)
        self.setMinimumSize(1180, 780)
        self.proc: QProcess | None = None
        self.recipe: Recipe | None = None
        self.seeds: list[int] = []
        self.probe_file: Path | None = None
        self.rows: list[ParamRow] = []
        self._build()
        self._check_backend()

    def _build(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        main = QVBoxLayout(root)
        main.setContentsMargins(18, 16, 18, 16)
        main.setSpacing(10)

        banner = QFrame()
        banner.setObjectName('Banner')
        bl = QHBoxLayout(banner)
        bl.setContentsMargins(16, 12, 16, 12)
        title = QLabel('C11-C PRODUCER')
        title.setObjectName('Title')
        bl.addWidget(title)
        bl.addStretch(1)
        self.backend_status = QLabel('Comprobando backend…')
        self.backend_status.setObjectName('Status')
        bl.addWidget(self.backend_status)
        main.addWidget(banner)

        type_box = QGroupBox('TIPO DE VÍDEO')
        type_lay = QHBoxLayout(type_box)
        self.type_buttons: list[QPushButton] = []
        for text, enabled in [('CHALLENGES', False), ('VISUAL LOOPS', True), ('VISUAL DRILLS', False)]:
            b = QPushButton(text)
            b.setCheckable(True)
            b.setEnabled(enabled)
            b.setMinimumHeight(46)
            if enabled:
                b.setChecked(True)
            else:
                b.setToolTip('Esta categoría se habilitará en una fase posterior.')
            self.type_buttons.append(b)
            type_lay.addWidget(b, 1)
        main.addWidget(type_box)

        setup = QGroupBox('PRODUCCIÓN · VISUAL LOOPS')
        grid = QGridLayout(setup)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(9)
        self.family = QComboBox()
        self.family.addItems([f['name'] for f in FAMILIES.values()])
        self.family.currentIndexChanged.connect(self._family_changed)
        self.grammar = QComboBox()
        self.count = QSpinBox(); self.count.setRange(1, 500); self.count.setValue(1)
        self.seed_mode = QComboBox(); self.seed_mode.addItems(['SEEDS ALEATORIAS', 'SEEDS MANUALES'])
        self.seed_mode.currentIndexChanged.connect(lambda i: self.manual.setEnabled(i == 1))
        self.manual = QLineEdit(); self.manual.setEnabled(False)
        self.manual.setPlaceholderText('314159, 271828, 123456…')
        self.sound = QCheckBox('Audio'); self.sound.setChecked(True)
        self.footer = QCheckBox('Footer'); self.footer.setChecked(True)
        self.force = QCheckBox('Force'); self.force.setChecked(False)
        self.force.setToolTip('Reemplaza deliberadamente un producto existente con la misma familia + seed.')
        grid.addWidget(QLabel('Familia'), 0, 0); grid.addWidget(self.family, 0, 1)
        grid.addWidget(QLabel('Subfamilia'), 0, 2); grid.addWidget(self.grammar, 0, 3)
        grid.addWidget(QLabel('Cantidad'), 1, 0); grid.addWidget(self.count, 1, 1)
        grid.addWidget(QLabel('Seeds'), 1, 2); grid.addWidget(self.seed_mode, 1, 3)
        grid.addWidget(QLabel('Seeds manuales'), 2, 0); grid.addWidget(self.manual, 2, 1, 1, 3)
        flags = QHBoxLayout(); flags.addWidget(self.sound); flags.addWidget(self.footer); flags.addWidget(self.force); flags.addStretch(1)
        grid.addLayout(flags, 3, 0, 1, 4)
        main.addWidget(setup)

        target_box = QGroupBox('VARIACIONES · DERIVADAS DE LA SEED')
        target_lay = QVBoxLayout(target_box)
        hint = QLabel('ALEATORIO = la seed decide el valor. FIJAR = se buscarán seeds cuyo perfil real se aproxime al objetivo.')
        hint.setObjectName('Hint')
        target_lay.addWidget(hint)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame)
        body = QWidget(); self.params_grid = QGridLayout(body)
        self.params_grid.setHorizontalSpacing(14); self.params_grid.setVerticalSpacing(6)
        scroll.setWidget(body)
        target_lay.addWidget(scroll, 1)
        main.addWidget(target_box, 1)

        actions = QHBoxLayout()
        self.generate = QPushButton('GENERAR PRODUCCIÓN')
        self.generate.setObjectName('Primary')
        self.generate.setMinimumHeight(52)
        self.reset = QPushButton('RESTABLECER')
        self.reset.setMinimumHeight(46)
        self.reset.clicked.connect(self._reset)
        self.generate.clicked.connect(self.start)
        actions.addWidget(self.generate, 1); actions.addWidget(self.reset)
        main.addLayout(actions)

        self.progress = QProgressBar(); self.progress.setRange(0, 100); self.progress.setValue(0); main.addWidget(self.progress)
        self.log = QPlainTextEdit(); self.log.setReadOnly(True); self.log.setMinimumHeight(180); self.log.setPlaceholderText('La actividad de producción aparecerá aquí…'); main.addWidget(self.log)

        self._family_changed(0)

    def _family_id(self) -> str:
        return next(iter(FAMILIES)) if not self.family.currentData() else str(self.family.currentData())

    def _family_changed(self, index: int) -> None:
        names = list(FAMILIES.keys())
        if index < 0 or index >= len(names):
            return
        fid = names[index]
        self.family.blockSignals(True)
        self.family.setProperty('family_id', fid)
        self.family.blockSignals(False)
        self.grammar.clear()
        self.grammar.addItem('ALEATORIO · POR SEED', userData='auto')
        for code, label in FAMILIES[fid]['grammars']:
            if code != 'auto':
                self.grammar.addItem(label, userData=code)
        while self.params_grid.count():
            item = self.params_grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        self.rows.clear()
        params = FAMILIES[fid]['params']
        half = (len(params) + 1) // 2
        for i, spec in enumerate(params):
            row = ParamRow(spec)
            self.rows.append(row)
            col = 0 if i < half else 1
            rr = i if i < half else i - half
            self.params_grid.addWidget(row, rr, col)
        self.params_grid.setColumnStretch(0, 1); self.params_grid.setColumnStretch(1, 1)

    def _check_backend(self) -> None:
        profile = PROJECT / SCHEMA['backend_profile_source']
        missing = []
        if not (PROJECT / 'project.godot').exists(): missing.append(str(PROJECT / 'project.godot'))
        if not profile.exists(): missing.append(str(profile))
        for fid in FAMILIES:
            launcher = PROJECT / FAMILIES[fid]['prototype']
            if not launcher.exists(): missing.append(str(launcher))
        if missing:
            self.generate.setEnabled(False)
            self.backend_status.setText('BACKEND INCOMPLETO')
            QMessageBox.critical(self, 'Backend no válido', 'Faltan archivos del backend 2.9.1:\n\n' + '\n'.join(missing))
            return
        actual = hashlib.sha256(profile.read_bytes()).hexdigest()
        if actual != EXPECTED_PROFILE_SHA:
            self.generate.setEnabled(False)
            self.backend_status.setText('BACKEND DIFERENTE')
            QMessageBox.critical(self, 'Backend no esperado', 'C11CVariationProfile.gd no coincide con el backend 2.9.1 de referencia.')
            return
        self.backend_status.setText('C11-C 2.9.1 · 5 familias · 720×1280 · 30 FPS')
        self.log.appendPlainText(f'Backend verificado: {PROJECT}')

    def _reset(self) -> None:
        if self.proc:
            return
        self.grammar.setCurrentIndex(0)
        self.count.setValue(1)
        self.seed_mode.setCurrentIndex(0)
        self.manual.clear()
        self.sound.setChecked(True); self.footer.setChecked(True); self.force.setChecked(False)
        for row in self.rows: row.mode.setCurrentIndex(0)
        self.progress.setValue(0)
        self.log.clear()

    def _targets(self) -> dict[str, Any]:
        targets: dict[str, Any] = {}
        grammar = self.grammar.currentData()
        if grammar and grammar != 'auto':
            targets['grammar_name'] = str(grammar)
        for row in self.rows:
            val = row.value()
            if val is not None:
                targets[row.spec['key']] = val
        return targets

    def _manual_seed_list(self) -> list[int] | None:
        if self.seed_mode.currentIndex() == 0:
            return []
        try:
            vals = [int(x.strip()) for x in self.manual.text().split(',') if x.strip()]
        except ValueError:
            QMessageBox.warning(self, 'Seeds', 'Las seeds deben ser enteros separados por comas.')
            return None
        if len(vals) != self.count.value():
            QMessageBox.warning(self, 'Seeds', f'Debes introducir exactamente {self.count.value()} seeds.')
            return None
        if len(set(vals)) != len(vals) or any(v < 1 or v > 2147483646 for v in vals):
            QMessageBox.warning(self, 'Seeds', 'Las seeds deben ser únicas y estar entre 1 y 2147483646.')
            return None
        return vals

    def _existing(self, family: str) -> set[int]:
        root = PROJECT / 'artifacts' / 'production' / 'audiovisual' / family
        out: set[int] = set()
        if root.exists():
            for p in root.iterdir():
                m = re.search(r'_seed_(\d+)$', p.name)
                if m: out.add(int(m.group(1)))
        return out

    def start(self) -> None:
        if self.proc:
            return
        manual = self._manual_seed_list()
        if manual is None:
            return
        fid = self.family.property('family_id') or list(FAMILIES.keys())[self.family.currentIndex()]
        targets = self._targets()
        self.recipe = Recipe(str(fid), str(self.grammar.currentData() or 'auto'), self.count.value(), manual, not self.sound.isChecked(), not self.footer.isChecked(), self.force.isChecked(), targets)
        self.generate.setEnabled(False)
        self.reset.setEnabled(False)
        self.progress.setValue(0)
        self.log.appendPlainText('\n=== NUEVA PRODUCCIÓN ===')
        self.log.appendPlainText(f'Familia: {FAMILIES[self.recipe.family]["name"]}')
        self.log.appendPlainText(f'Subfamilia: {self.grammar.currentText()}')
        self.log.appendPlainText(f'Cantidad: {self.recipe.count}')
        self._plan_seeds()

    def _plan_seeds(self) -> None:
        assert self.recipe is not None
        existing = self._existing(self.recipe.family)
        if self.recipe.manual_seeds:
            candidates = self.recipe.manual_seeds
        elif not self.recipe.targets:
            candidates = []
            while len(candidates) < self.recipe.count:
                s = random.randint(1000000, 2147483646)
                if s not in existing and s not in candidates:
                    candidates.append(s)
        else:
            pool_size = min(200000, max(5000, self.recipe.count * 500))
            candidates = []
            seen = set(existing)
            while len(candidates) < pool_size:
                s = random.randint(1000000, 2147483646)
                if s not in seen:
                    seen.add(s); candidates.append(s)
            req = {
                'family': FAMILIES[self.recipe.family]['internal'],
                'count': self.recipe.count,
                'targets': self.recipe.targets,
                'candidates': candidates,
                'tolerance_multiplier': 1.5,
            }
            self.probe_file = ROOT / '.runtime' / 'request.json'
            self.probe_file.parent.mkdir(parents=True, exist_ok=True)
            self.probe_file.write_text(json.dumps(req, ensure_ascii=False), encoding='utf-8')
            (ROOT / '.runtime' / 'response.json').unlink(missing_ok=True)
            self.log.appendPlainText('[SEED PLANNER] Consultando C11CVariationProfile.gd real…')
            self._launch_probe()
            return
        self._set_seeds(candidates[:self.recipe.count])

    def _launch_probe(self) -> None:
        assert self.probe_file is not None
        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(str(PROJECT))
        self.proc.setProgram('godot')
        self.proc.setArguments(['--headless', '--path', str(PROJECT), '--script', str(ROOT / 'seed_probe.gd'), '--', str(self.probe_file)])
        self.proc.readyReadStandardOutput.connect(self._probe_out)
        self.proc.readyReadStandardError.connect(self._probe_err)
        self.proc.finished.connect(self._probe_done)
        self.proc.start()

    def _probe_out(self) -> None:
        if not self.proc: return
        data = bytes(self.proc.readAllStandardOutput()).decode(errors='replace').strip()
        if data: self.log.appendPlainText(data)

    def _probe_err(self) -> None:
        if not self.proc: return
        data = bytes(self.proc.readAllStandardError()).decode(errors='replace').strip()
        if data: self.log.appendPlainText('[SEED PLANNER STDERR] ' + data)

    def _probe_done(self, code: int, status: QProcess.ExitStatus) -> None:
        p = self.proc
        self.proc = None
        self._probe_out(); self._probe_err()
        if p: p.deleteLater()
        if self.probe_file: self.probe_file.unlink(missing_ok=True)
        response = ROOT / '.runtime' / 'response.json'
        payload = None
        if response.exists():
            try: payload = json.loads(response.read_text(encoding='utf-8'))
            except Exception as exc: payload = {'ok': False, 'error': f'Respuesta inválida: {exc}'}
            response.unlink(missing_ok=True)
        if code != 0 or not payload or not payload.get('ok'):
            msg = (payload or {}).get('error', f'seed_probe terminó con código {code}')
            self.log.appendPlainText('[SEED PLANNER ERROR] ' + msg)
            QMessageBox.critical(self, 'No hay seeds compatibles', msg)
            self._finish(False)
            return
        results = payload.get('results', [])
        seeds = [int(x['seed']) for x in results]
        if len(seeds) != self.recipe.count:
            QMessageBox.critical(self, 'Planner incompleto', f'El planner devolvió {len(seeds)} seeds de {self.recipe.count}.')
            self._finish(False)
            return
        self.log.appendPlainText('[SEEDS PLANNER] ' + ', '.join(map(str, seeds)))
        self._set_seeds(seeds)

    def _set_seeds(self, seeds: list[int]) -> None:
        self.seeds = list(seeds)
        self.progress.setValue(1)
        self._run_next()

    def _run_next(self) -> None:
        assert self.recipe is not None
        if not self.seeds:
            self.log.appendPlainText('\n=== PRODUCCIÓN FINALIZADA ===')
            self._finish(True)
            return
        seed = self.seeds.pop(0)
        family = self.recipe.family
        script = PROJECT / 'tools' / 'prototypes' / 'c11c_bulk' / 'run_c11c_production.ps1'
        args = ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', str(script), '-Family', family, '-Seed', str(seed)]
        if self.recipe.no_sound: args.append('-NoSound')
        if self.recipe.no_footer: args.append('-NoFooter')
        if self.recipe.force: args.append('-Force')
        done = self.recipe.count - len(self.seeds)
        self.progress.setValue(max(1, int(done * 100 / self.recipe.count)))
        self.log.appendPlainText(f'\n[PRODUCTION {done}/{self.recipe.count}] seed={seed}')
        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(str(PROJECT))
        self.proc.setProgram('powershell.exe')
        self.proc.setArguments(args)
        self.proc.readyReadStandardOutput.connect(self._prod_out)
        self.proc.readyReadStandardError.connect(self._prod_err)
        self.proc.finished.connect(self._prod_done)
        self.proc.start()

    def _prod_out(self) -> None:
        if not self.proc: return
        data = bytes(self.proc.readAllStandardOutput()).decode(errors='replace').strip()
        if data: self.log.appendPlainText(data)

    def _prod_err(self) -> None:
        if not self.proc: return
        data = bytes(self.proc.readAllStandardError()).decode(errors='replace').strip()
        if data: self.log.appendPlainText('[STDERR] ' + data)

    def _prod_done(self, code: int, status: QProcess.ExitStatus) -> None:
        p = self.proc
        self.proc = None
        self._prod_out(); self._prod_err()
        if p: p.deleteLater()
        if code != 0:
            self.log.appendPlainText(f'[PRODUCTION ERROR] código {code}')
            self._finish(False)
            QMessageBox.critical(self, 'Producción fallida', f'El launcher terminó con código {code}. Revisa el log.')
            return
        self.log.appendPlainText('[PRODUCTION] PASS')
        QTimer.singleShot(0, self._run_next)

    def _finish(self, ok: bool) -> None:
        self.generate.setEnabled(True)
        self.reset.setEnabled(True)
        self.progress.setValue(100 if ok else 0)
        self.proc = None


STYLE = '''
QWidget{background:#f5f7fa;color:#17212b;font-family:"Segoe UI";font-size:13px;}
QLabel{background:transparent;}
QFrame#Banner{background:#ffffff;border:1px solid #cfd7e2;border-radius:10px;min-height:66px;}
QLabel#Title{font-size:24px;font-weight:700;color:#0f172a;}
QLabel#Status{color:#334155;font-size:12px;font-weight:600;}
QLabel#Hint{color:#475569;font-size:12px;padding:3px 2px;}
QGroupBox{background:#ffffff;border:1px solid #cfd7e2;border-radius:9px;margin-top:10px;padding:12px;font-weight:700;}
QComboBox,QLineEdit,QSpinBox,QDoubleSpinBox{background:#ffffff;color:#111827;border:1px solid #94a3b8;border-radius:6px;min-height:42px;padding:0 10px;font-size:14px;}
QComboBox:focus,QLineEdit:focus,QSpinBox:focus,QDoubleSpinBox:focus{border:2px solid #2563eb;}
QComboBox::drop-down{width:36px;border-left:1px solid #cbd5e1;background:#eef2f7;}
QComboBox QAbstractItemView{background:#ffffff;color:#111827;border:1px solid #94a3b8;selection-background-color:#dbeafe;selection-color:#111827;padding:4px;outline:none;}
QComboBox QAbstractItemView::item{min-height:38px;padding:8px 10px;}
QPushButton{background:#ffffff;color:#17212b;border:1px solid #94a3b8;border-radius:7px;min-height:42px;padding:0 15px;font-weight:650;}
QPushButton:hover{background:#eef4fb;}
QPushButton:disabled{background:#e9edf2;color:#94a3b8;border-color:#d7dde5;}
QPushButton:checked{background:#e8f0ff;border:2px solid #2563eb;color:#1d4ed8;}
QPushButton#Primary{background:#2563eb;color:#ffffff;border-color:#2563eb;min-height:52px;font-size:15px;}
QPushButton#Primary:hover{background:#1d4ed8;}
QCheckBox{min-height:34px;spacing:7px;font-size:13px;}
QCheckBox::indicator{width:18px;height:18px;}
QScrollArea{border:0;background:#ffffff;}
QPlainTextEdit{background:#ffffff;color:#17212b;border:1px solid #94a3b8;border-radius:7px;padding:8px;font-family:"Consolas";font-size:12px;}
QProgressBar{background:#e8edf3;border:1px solid #cbd5e1;border-radius:6px;min-height:14px;text-align:center;}
QProgressBar::chunk{background:#2563eb;border-radius:5px;}
QScrollBar:vertical{width:14px;background:#edf1f5;}
QScrollBar::handle:vertical{background:#a8b4c2;min-height:34px;border-radius:7px;}
'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont('Segoe UI', 10))
    app.setStyleSheet(STYLE)
    win = MainWindow()
    win.show()
    raise SystemExit(app.exec())
