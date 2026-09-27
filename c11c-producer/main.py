from __future__ import annotations

import hashlib
import json
import os
import random
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from PySide6.QtCore import QProcess, QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

APP_VERSION = "0.8.0"
ROOT = Path(__file__).resolve().parent
PROJECT = Path(os.environ.get("C11C_PROJECT_ROOT", ROOT.parent)).resolve()
SCHEMA = json.loads((ROOT / "producer_schema.json").read_text(encoding="utf-8"))

FAMILIES: dict[str, dict[str, Any]] = SCHEMA["families"]
DRILLS: dict[str, dict[str, Any]] = SCHEMA["drills"]
VIDEO_TYPES = {key: label for key, label in SCHEMA.get("video_types", [])}

DELIVERY_FILE = PROJECT / "profiles" / "delivery" / "c11c_video_delivery_profiles.json"
if DELIVERY_FILE.exists():
    DELIVERY_CONFIG = json.loads(DELIVERY_FILE.read_text(encoding="utf-8"))
else:
    DELIVERY_CONFIG = {"standard_default": "MASTER_1080", "profiles": {}}

DELIVERY_ORDER = [
    "MASTER_1080",
    "REVIEW_720",
    "MIN_540",
    "META_REELS_FINAL_V1",
    "LONGFORM_1080",
]


def delivery_label(profile_id: str) -> str:
    profile = DELIVERY_CONFIG.get("profiles", {}).get(profile_id, {})
    if profile_id == "MASTER_1080":
        return "MASTER — 1080x1920 (ESTÁNDAR)"
    if profile_id == "REVIEW_720":
        return "REVIEW — 720x1280 (C11-C)"
    if profile_id == "MIN_540":
        return "MÍNIMO — 540x960"
    if profile_id == "META_REELS_FINAL_V1":
        return "META REELS FINAL — 1080x1920"
    if profile_id == "LONGFORM_1080":
        return "LONGFORM — 1080x1920"
    return f"{profile_id} — {profile.get('width', '?')}x{profile.get('height', '?')}"


DELIVERY_PROFILES = [
    pid
    for pid in DELIVERY_ORDER
    if pid in DELIVERY_CONFIG.get("profiles", {})
]
DEFAULT_DELIVERY = (
    DELIVERY_CONFIG.get("standard_default")
    if DELIVERY_CONFIG.get("standard_default") in DELIVERY_PROFILES
    else (DELIVERY_PROFILES[0] if DELIVERY_PROFILES else "MASTER_1080")
)


def load_challenge_catalog() -> dict[str, dict[str, Any]]:
    catalog: dict[str, dict[str, Any]] = {}
    challenges_root = PROJECT / "challenges"
    for path in sorted(challenges_root.glob("CHALLENGE_*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            cid = str(payload.get("challenge_id") or path.stem)
            video = payload.get("video") or {}
            fps = int(video.get("fps", 60))
            phase_seconds = sum(float(video.get(key, 0.0)) for key in (
                "hook_duration",
                "game_duration",
                "reveal_duration",
                "cta_duration",
            ))
            total_frames = int(round(phase_seconds * fps))
            catalog[cid] = {
                "id": cid,
                "mechanic": str(payload.get("mechanic", "unknown")),
                "fps": fps,
                "duration_seconds": phase_seconds,
                "frames": total_frames,
                "assets": payload.get("assets", {}),
                "seed": int((payload.get("generation") or {}).get("seed", 1)),
                "path": str(path),
            }
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            continue
    return catalog


CHALLENGES = load_challenge_catalog()


@dataclass
class Recipe:
    operation: str
    video_type: str
    family: str = ""
    grammar: str = "auto"
    challenge_id: str = ""
    count: int = 1
    manual_seeds: list[int] | None = None
    no_sound: bool = False
    no_footer: bool = False
    force: bool = False
    workers: int = 7
    resume: bool = False
    reset: bool = False
    export_gif: bool = False
    keep_avi: bool = False
    delivery: str = DEFAULT_DELIVERY
    targets: dict[str, Any] = field(default_factory=dict)


class ParamRow(QWidget):
    def __init__(self, spec: dict[str, Any]):
        super().__init__()
        self.spec = spec
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 1, 0, 1)
        lay.setSpacing(8)
        self.label = QLabel(spec["label"])
        self.label.setMinimumWidth(155)
        self.mode = QComboBox()
        self.mode.addItems(["ALEATORIO (seed)", "FIJAR"])
        self.mode.setFixedWidth(155)
        if spec["kind"] == "enum":
            self.editor = QComboBox()
            self.editor.addItems([str(value) for value in spec["values"]])
        else:
            self.editor = QDoubleSpinBox()
            self.editor.setRange(float(spec["min"]), float(spec["max"]))
            self.editor.setSingleStep(float(spec["step"]))
            step = float(spec["step"])
            self.editor.setDecimals(5 if step < 0.001 else 3 if step < 0.01 else 2)
            self.editor.setValue((float(spec["min"]) + float(spec["max"])) / 2)
        self.editor.setEnabled(False)
        self.editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        lay.addWidget(self.label)
        lay.addWidget(self.mode)
        lay.addWidget(self.editor, 1)
        self.mode.currentIndexChanged.connect(
            lambda index: self.editor.setEnabled(index == 1 and self.isEnabled())
        )

    def set_random(self) -> None:
        self.mode.setCurrentIndex(0)

    def value(self) -> Any:
        if self.mode.currentIndex() == 0:
            return None
        if self.spec["kind"] == "enum":
            value = self.editor.currentText()
            try:
                return int(value)
            except ValueError:
                return value
        return float(self.editor.value())

    def set_interactive(self, enabled: bool) -> None:
        self.setEnabled(enabled)
        self.mode.setEnabled(enabled)
        self.editor.setEnabled(enabled and self.mode.currentIndex() == 1)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"C11-C Producer {APP_VERSION}")
        self.resize(1280, 920)
        self.queue: list[Recipe] = []
        self.current_recipe: Recipe | None = None
        self.jobs: list[int] = []
        self.proc: QProcess | None = None
        self.probe_file: Path | None = None
        self.rows: list[ParamRow] = []
        self._build()
        self._check_backend()
        self._refresh_profile_hint()

    def _build(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        main = QVBoxLayout(root)
        main.setContentsMargins(14, 14, 14, 14)
        main.setSpacing(10)

        banner = QFrame()
        banner.setObjectName("Banner")
        bl = QHBoxLayout(banner)
        bl.setContentsMargins(16, 9, 16, 9)
        title = QLabel("C11-C PRODUCER")
        title.setObjectName("Title")
        bl.addWidget(title)
        bl.addStretch()
        self.backend_info = QLabel("")
        self.backend_info.setObjectName("Muted")
        bl.addWidget(self.backend_info)
        main.addWidget(banner)

        cols = QHBoxLayout()
        cols.setSpacing(10)
        cols.addWidget(self._build_recipe(), 1)
        cols.addWidget(self._build_queue(), 1)
        main.addLayout(cols, 1)

    def _build_recipe(self) -> QGroupBox:
        box = QGroupBox("CREAR PRODUCCIÓN")
        root = QVBoxLayout(box)
        root.setSpacing(8)
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(8)

        self.operation = QComboBox()
        self.operation.addItem("A LA CARTA", "A_LA_CARTA")
        for key, label in SCHEMA.get("batch_operations", [])[1:]:
            self.operation.addItem(label, key)
        self.operation.addItem("REGRESIÓN COMPLETA", "RUN_REGRESSION")

        self.video_type = QComboBox()
        for key in ("challenges", "visual_loops", "visual_drills"):
            self.video_type.addItem(VIDEO_TYPES.get(key, key.upper()), key)
        self.video_type.setCurrentIndex(0)

        self.family = QComboBox()
        self.grammar = QComboBox()
        self.count = QSpinBox()
        self.count.setRange(1, 500)
        self.count.setValue(1)
        self.seed_mode = QComboBox()
        self.seed_mode.addItems(["SEEDS ALEATORIAS", "SEEDS MANUALES"])
        self.manual = QLineEdit()
        self.manual.setPlaceholderText("314159, 271828…")
        self.manual.setEnabled(False)

        self.video_type_label = QLabel("Tipo de vídeo")
        self.family_label = QLabel("Familia")
        self.subtype_label = QLabel("Subfamilia")
        self.count_label = QLabel("Cantidad")
        self.seed_label = QLabel("Seeds")

        fields = [
            (0, QLabel("Operación"), self.operation),
            (1, self.video_type_label, self.video_type),
            (2, self.family_label, self.family),
            (3, self.subtype_label, self.grammar),
            (4, self.count_label, self.count),
            (5, self.seed_label, self.seed_mode),
        ]
        for row, label, widget in fields:
            grid.addWidget(label, row, 0)
            grid.addWidget(widget, row, 1)
        grid.addWidget(self.manual, 6, 0, 1, 2)
        root.addLayout(grid)

        self.type_info = QLabel()
        self.type_info.setObjectName("Hint")
        self.type_info.setWordWrap(True)
        root.addWidget(self.type_info)

        opts = QHBoxLayout()
        self.no_sound = QCheckBox("Sin audio")
        self.no_footer = QCheckBox("Sin footer")
        self.force = QCheckBox("FORCE")
        opts.addWidget(self.no_sound)
        opts.addWidget(self.no_footer)
        opts.addWidget(self.force)
        opts.addStretch()
        root.addLayout(opts)

        out = QGridLayout()
        self.delivery = QComboBox()
        for profile_id in DELIVERY_PROFILES:
            self.delivery.addItem(delivery_label(profile_id), profile_id)
        default_index = max(0, self.delivery.findData(DEFAULT_DELIVERY))
        self.delivery.setCurrentIndex(default_index)
        self.workers = QSpinBox()
        self.workers.setRange(1, 7)
        self.workers.setValue(7)
        self.resume = QCheckBox("RESUME")
        self.reset = QCheckBox("RESET")
        self.export_gif = QCheckBox("Exportar GIF")
        self.keep_avi = QCheckBox("Conservar AVI")
        out.addWidget(QLabel("Salida"), 0, 0)
        out.addWidget(self.delivery, 0, 1)
        out.addWidget(QLabel("Workers"), 1, 0)
        out.addWidget(self.workers, 1, 1)
        out.addWidget(self.resume, 2, 0)
        out.addWidget(self.reset, 2, 1)
        out.addWidget(self.export_gif, 3, 0)
        out.addWidget(self.keep_avi, 3, 1)
        root.addLayout(out)

        pbox = QGroupBox("VARIACIÓN · por defecto ALEATORIA por seed")
        pl = QVBoxLayout(pbox)
        self.randomize = QPushButton("PONER TODO EN ALEATORIO")
        pl.addWidget(self.randomize)
        self.pscroll = QScrollArea()
        self.pscroll.setWidgetResizable(True)
        self.pscroll.setFrameShape(QFrame.NoFrame)
        self.pwidget = QWidget()
        self.pl = QVBoxLayout(self.pwidget)
        self.pl.setContentsMargins(4, 4, 4, 4)
        self.pl.setAlignment(Qt.AlignTop)
        self.pscroll.setWidget(self.pwidget)
        pl.addWidget(self.pscroll, 1)
        root.addWidget(pbox, 1)

        hint = QLabel(
            "La GUI solo orquesta launchers canónicos. No reimplementa mecánicas, RNG ni renderers."
        )
        hint.setObjectName("Hint")
        hint.setWordWrap(True)
        root.addWidget(hint)

        self.add = QPushButton("AÑADIR A LA COLA")
        self.add.setObjectName("Primary")
        self.add.setMinimumHeight(46)
        root.addWidget(self.add)

        self.operation.currentIndexChanged.connect(self._operation_changed)
        self.video_type.currentIndexChanged.connect(self._video_type_changed)
        self.family.currentIndexChanged.connect(self._refresh_family)
        self.seed_mode.currentIndexChanged.connect(self._seed_mode_changed)
        self.delivery.currentIndexChanged.connect(self._refresh_profile_hint)
        self.randomize.clicked.connect(self._randomize_all)
        self.add.clicked.connect(self._add)

        self._video_type_changed(self.video_type.currentIndex())
        self._operation_changed(0)
        return box

    def _build_queue(self) -> QGroupBox:
        box = QGroupBox("COLA DE PRODUCCIÓN")
        root = QVBoxLayout(box)
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            ["Operación", "Tipo", "Familia", "Subfamilia", "Cantidad", "Salida", "Workers", "Estado"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        root.addWidget(self.table, 3)

        btns = QHBoxLayout()
        self.generate = QPushButton("GENERAR")
        self.generate.setObjectName("Primary")
        self.generate.setMinimumHeight(48)
        self.remove = QPushButton("QUITAR")
        self.clear = QPushButton("VACIAR")
        btns.addWidget(self.generate, 2)
        btns.addWidget(self.remove)
        btns.addWidget(self.clear)
        root.addLayout(btns)

        lbox = QGroupBox("PROGRESO / LOG")
        ll = QVBoxLayout(lbox)
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        ll.addWidget(self.log)
        root.addWidget(lbox, 2)

        self.generate.clicked.connect(self.start)
        self.remove.clicked.connect(self.remove_selected)
        self.clear.clicked.connect(self._clear)
        return box

    def _clear_rows(self) -> None:
        while self.pl.count():
            item = self.pl.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.rows = []

    def _video_type_changed(self, _idx: int) -> None:
        if self.operation.currentData() != "A_LA_CARTA":
            return
        video_type = str(self.video_type.currentData())
        self._clear_rows()
        self.family.clear()
        self.grammar.clear()

        if video_type == "challenges":
            self.family_label.setText("Mecánica")
            self.subtype_label.setText("Challenge ID")
            mechanics = sorted({item["mechanic"] for item in CHALLENGES.values()})
            self.family.addItems(mechanics)
            self._refresh_challenges()
            self.no_footer.setChecked(False)
            self.type_info.setText(
                "Challenges: catálogo leído directamente de challenges/*.json. El timeline se deriva de las cuatro fases; el Producer no duplica mecánica."
            )
        elif video_type == "visual_loops":
            self.family_label.setText("Familia")
            self.subtype_label.setText("Gramática")
            self.family.addItems([value["name"] for value in FAMILIES.values()])
            self._refresh_family(0)
            self.no_footer.setEnabled(True)
            self.type_info.setText(
                "Visual Loops: 5 familias / 27 grammars. Review histórico 720x1280; MASTER_1080 se obtiene después mediante el perfil de entrega."
            )
        else:
            self.family_label.setText("Familia")
            self.subtype_label.setText("Dificultad")
            self.family.addItems([value["name"] for value in DRILLS.values()])
            self._refresh_family(0)
            self.no_footer.setChecked(False)
            self.no_footer.setEnabled(False)
            self.type_info.setText(
                "Visual Drills: Tracking, Saccade, Pursuit y Peripheral Scan. PRE_ROLL + gameplay + END_CTA; la entrega se selecciona en el perfil central."
            )

        self.delivery.setEnabled(True)
        self._seed_mode_changed(self.seed_mode.currentIndex())
        self._refresh_profile_hint()

    def _refresh_challenges(self) -> None:
        mechanic = str(self.family.currentText())
        self.grammar.clear()
        for cid, item in CHALLENGES.items():
            if item["mechanic"] == mechanic:
                self.grammar.addItem(
                    f"{cid} · {item['duration_seconds']:.0f}s · {item['frames']} frames",
                    cid,
                )

    def _refresh_family(self, idx: int) -> None:
        video_type = str(self.video_type.currentData())
        if video_type == "challenges":
            self._refresh_challenges()
            return

        self._clear_rows()
        if video_type == "visual_loops":
            ids = list(FAMILIES)
            if not ids:
                return
            idx = max(0, min(idx, len(ids) - 1))
            self.family.blockSignals(True)
            self.family.setCurrentIndex(idx)
            self.family.blockSignals(False)
            family_id = ids[idx]
            self.grammar.clear()
            for code, label in FAMILIES[family_id].get("grammars", []):
                self.grammar.addItem(label, code)
            for spec in FAMILIES[family_id].get("params", []):
                row = ParamRow(spec)
                self.rows.append(row)
                self.pl.addWidget(row)
        elif video_type == "visual_drills":
            ids = list(DRILLS)
            if not ids:
                return
            idx = max(0, min(idx, len(ids) - 1))
            self.family.blockSignals(True)
            self.family.setCurrentIndex(idx)
            self.family.blockSignals(False)
            family_id = ids[idx]
            self.grammar.clear()
            self.grammar.addItem("ALEATORIO", "auto")
            for tier in range(1, 6):
                self.grammar.addItem(f"TIER {tier}", str(tier))
            for spec in DRILLS[family_id].get("parameters", []):
                row = ParamRow(spec)
                self.rows.append(row)
                self.pl.addWidget(row)
        self._seed_mode_changed(self.seed_mode.currentIndex())

    def _operation_changed(self, _idx: int) -> None:
        op = str(self.operation.currentData())
        batch = op != "A_LA_CARTA"
        utility = op == "RUN_REGRESSION"
        self.video_type.setEnabled(not batch)
        self.family.setEnabled(not batch)
        self.grammar.setEnabled(not batch)
        self.count.setEnabled(not batch)
        self.seed_mode.setEnabled(not batch)
        self.manual.setEnabled(False)
        self.no_sound.setEnabled(not batch and not utility)
        self.no_footer.setEnabled(not batch and not utility)
        self.force.setEnabled(not batch and not utility)
        self.randomize.setEnabled(not batch)
        self.delivery.setEnabled(not batch and not utility)
        self.workers.setEnabled(True)
        self.resume.setEnabled(batch and not utility)
        self.reset.setEnabled(batch and not utility)
        self.export_gif.setEnabled(not utility)
        self.keep_avi.setEnabled(not utility)
        self.add.setEnabled(True)
        if batch:
            self.subtype_label.setText("Contenido")
            self.type_info.setText(
                "Operación batch: utiliza el runner C11-C selectivo. Estas operaciones son revisiones históricas; el perfil de entrega de A LA CARTA no se reutiliza automáticamente."
            )
        if utility:
            self.type_info.setText("Ejecuta la regresión lógica completa con el runner oficial.")
        else:
            self._video_type_changed(self.video_type.currentIndex())

    def _seed_mode_changed(self, idx: int) -> None:
        active = self.operation.currentData() == "A_LA_CARTA"
        manual = idx == 1
        self.manual.setEnabled(active and manual)
        for row in self.rows:
            row.set_interactive(active)

    def _refresh_profile_hint(self, _idx: int = -1) -> None:
        profile_id = str(self.delivery.currentData() or "")
        profile = DELIVERY_CONFIG.get("profiles", {}).get(profile_id, {})
        if profile.get("alias_of"):
            text = f"Salida: {profile_id} → {profile['alias_of']}"
        else:
            width = profile.get("width", "?")
            height = profile.get("height", "?")
            hz = profile.get("audio_sample_rate_hz", "?")
            text = f"Salida: {profile_id} · {width}x{height} · audio {hz} Hz"
        current = self.type_info.text().split("\n\n")[0]
        self.type_info.setText(f"{current}\n\n{text}")

    def _randomize_all(self) -> None:
        if self.grammar.count():
            self.grammar.setCurrentIndex(0)
        for row in self.rows:
            row.set_random()

    def _new_unique_seeds(self, count: int) -> list[int]:
        seeds: list[int] = []
        seen: set[int] = set()
        while len(seeds) < count:
            value = random.randint(1, 2_147_483_646)
            if value not in seen:
                seen.add(value)
                seeds.append(value)
        return seeds

    def _manual_seeds(self) -> list[int]:
        try:
            values = [int(x.strip()) for x in self.manual.text().split(",") if x.strip()]
        except ValueError as exc:
            raise ValueError("Seeds inválidas: deben ser enteros.") from exc
        if not values or any(x < 1 or x > 2_147_483_646 for x in values):
            raise ValueError("Seeds inválidas: rango permitido 1..2147483646.")
        if len(set(values)) != len(values):
            raise ValueError("Las seeds manuales deben ser únicas.")
        if len(values) != self.count.value():
            raise ValueError(f"Necesitas exactamente {self.count.value()} seeds manuales.")
        return values

    def _add(self) -> None:
        try:
            op = str(self.operation.currentData())
            if op == "RUN_REGRESSION":
                recipe = Recipe(op, "utility", workers=int(self.workers.value()))
                self.queue.append(recipe)
                self._add_row(recipe)
                return
            if op != "A_LA_CARTA":
                if self.resume.isChecked() and self.reset.isChecked():
                    raise ValueError("RESUME y RESET son excluyentes.")
                recipe = Recipe(
                    op,
                    "batch",
                    count=1,
                    workers=int(self.workers.value()),
                    resume=self.resume.isChecked(),
                    reset=self.reset.isChecked(),
                    export_gif=self.export_gif.isChecked(),
                    no_sound=self.no_sound.isChecked(),
                    keep_avi=self.keep_avi.isChecked(),
                )
                self.queue.append(recipe)
                self._add_row(recipe)
                return

            video_type = str(self.video_type.currentData())
            manual = self._manual_seeds() if self.seed_mode.currentIndex() == 1 else []
            delivery = str(self.delivery.currentData() or DEFAULT_DELIVERY)

            if video_type == "challenges":
                cid = str(self.grammar.currentData() or "")
                if cid not in CHALLENGES:
                    raise ValueError("Selecciona un Challenge ID válido.")
                recipe = Recipe(
                    op,
                    video_type,
                    family=str(self.family.currentText()),
                    grammar=cid,
                    challenge_id=cid,
                    count=self.count.value(),
                    manual_seeds=manual,
                    no_sound=self.no_sound.isChecked(),
                    force=self.force.isChecked(),
                    delivery=delivery,
                )
            else:
                ids = list(FAMILIES if video_type == "visual_loops" else DRILLS)
                family_id = ids[self.family.currentIndex()]
                targets = {
                    row.spec["key"]: value
                    for row in self.rows
                    if (value := row.value()) is not None
                }
                grammar = str(self.grammar.currentData() or "auto")
                if video_type == "visual_loops" and manual and (grammar != "auto" or targets):
                    raise ValueError(
                        "Con seeds manuales, deja gramática/parámetros en ALEATORIO; la variación determinista la fija la seed."
                    )
                recipe = Recipe(
                    op,
                    video_type,
                    family=family_id,
                    grammar=grammar,
                    count=self.count.value(),
                    manual_seeds=manual,
                    no_sound=self.no_sound.isChecked(),
                    no_footer=self.no_footer.isChecked(),
                    force=self.force.isChecked(),
                    workers=1,
                    targets=targets,
                    delivery=delivery,
                )
            self.queue.append(recipe)
            self._add_row(recipe)
        except Exception as exc:
            QMessageBox.warning(self, "Configuración inválida", str(exc))

    def _add_row(self, recipe: Recipe) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        values = [
            recipe.operation,
            recipe.video_type,
            recipe.family or recipe.challenge_id,
            recipe.grammar or "—",
            str(recipe.count),
            recipe.delivery,
            str(recipe.workers),
            "EN COLA",
        ]
        for index, value in enumerate(values):
            self.table.setItem(row, index, QTableWidgetItem(value))

    def remove_selected(self) -> None:
        if self.proc:
            return
        rows = sorted({item.row() for item in self.table.selectedIndexes()}, reverse=True)
        for index in rows:
            if 0 <= index < len(self.queue):
                self.queue.pop(index)
                self.table.removeRow(index)

    def _clear(self) -> None:
        if self.proc:
            return
        self.queue.clear()
        self.table.setRowCount(0)

    def start(self) -> None:
        if self.proc or not self.queue:
            return
        self.generate.setEnabled(False)
        self._run_recipe()

    def _run_recipe(self) -> None:
        if not self.queue:
            self.current_recipe = None
            self.generate.setEnabled(True)
            self.log.appendPlainText("\n=== PRODUCCIÓN FINALIZADA ===")
            return
        self.current_recipe = self.queue[0]
        self.jobs = []
        self.table.selectRow(0)
        recipe = self.current_recipe
        if recipe.operation == "RUN_REGRESSION":
            self._launch_python_regression()
            return
        if recipe.operation != "A_LA_CARTA":
            script = PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_art_direction_batch_v4.ps1"
            args = [
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script),
                "-Workers",
                str(recipe.workers),
            ]
            mapping = {
                "REVIEW_LOOPS": ["-Loops"],
                "REVIEW_DRILLS": ["-Drills"],
                "REVIEW_LONGFORMS": ["-Longforms"],
                "REVIEW_LOOPS_DRILLS": ["-Loops", "-Drills"],
                "REVIEW_LOOPS_LONGFORMS": ["-Loops", "-Longforms"],
                "REVIEW_DRILLS_LONGFORMS": ["-Drills", "-Longforms"],
                "REVIEW_ALL": ["-All"],
            }
            args += mapping.get(recipe.operation, [])
            if recipe.resume:
                args.append("-Resume")
            if recipe.reset:
                args.append("-Reset")
            if recipe.export_gif:
                args.append("-ExportGif")
            if recipe.no_sound:
                args.append("-NoSound")
            self.table.setItem(0, 7, QTableWidgetItem("REVIEW"))
            self._launch(args)
            return

        if recipe.video_type == "challenges":
            self.jobs = list(recipe.manual_seeds) if recipe.manual_seeds else self._new_unique_seeds(recipe.count)
            self._run_challenge_job()
            return
        if recipe.video_type == "visual_drills":
            self.jobs = list(recipe.manual_seeds) if recipe.manual_seeds else self._new_unique_seeds(recipe.count)
            self._run_content_job()
            return
        self._prepare_loop_jobs()

    def _prepare_loop_jobs(self) -> None:
        recipe = self.current_recipe
        if recipe is None:
            return
        if recipe.manual_seeds:
            self.jobs = list(recipe.manual_seeds)
            self._run_content_job()
            return
        if recipe.grammar == "auto" and not recipe.targets:
            existing = self._existing(recipe.family)
            while len(self.jobs) < recipe.count:
                seed = random.randint(1, 2_147_483_646)
                if seed not in existing and seed not in self.jobs:
                    self.jobs.append(seed)
            self.log.appendPlainText("[SEEDS RANDOM] " + ", ".join(map(str, self.jobs)))
            self._run_content_job()
            return

        request = {
            "family": FAMILIES[recipe.family]["internal"],
            "count": recipe.count,
            "target": dict(recipe.targets),
            "excluded_seeds": sorted(self._existing(recipe.family)),
            "max_candidates": 300_000,
            "start_seed": random.randint(1, 2_147_483_646),
        }
        if recipe.grammar != "auto":
            request["target"]["grammar_name"] = recipe.grammar

        self.probe_file = ROOT / ".runtime" / "request.json"
        self.probe_file.parent.mkdir(parents=True, exist_ok=True)
        self.probe_file.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
        answer = ROOT / ".runtime" / "response.json"
        answer.unlink(missing_ok=True)
        self.log.appendPlainText("[SEED PLANNER] Buscando seeds compatibles…")

        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(str(PROJECT))
        self.proc.setProgram("godot")
        self.proc.setArguments(
            [
                "--headless",
                "--path",
                str(PROJECT),
                "--script",
                str(ROOT / "seed_probe.gd"),
                "--",
                str(self.probe_file),
            ]
        )
        self.proc.readyReadStandardOutput.connect(self._out)
        self.proc.readyReadStandardError.connect(self._err)
        self.proc.finished.connect(self._probe_done)
        self.proc.start()

    def _probe_done(self, code: int, _status: Any) -> None:
        process = self.proc
        self.proc = None
        self._out()
        self._err()
        if process:
            process.deleteLater()

        answer = ROOT / ".runtime" / "response.json"
        payload: dict[str, Any] | None = None
        if answer.exists():
            try:
                payload = json.loads(answer.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                payload = {"ok": False, "error": str(exc)}
            answer.unlink(missing_ok=True)
        if self.probe_file:
            self.probe_file.unlink(missing_ok=True)
            self.probe_file = None
        if code != 0 or not payload or not payload.get("ok"):
            self._finish_error((payload or {}).get("error", f"seed_probe exit {code}"))
            return
        self.jobs = [int(item["seed"]) for item in payload["results"]]
        self.log.appendPlainText("[SEEDS PLANNER] " + ", ".join(map(str, self.jobs)))
        self._run_content_job()

    def _finish_error(self, message: str) -> None:
        self.log.appendPlainText("[ERROR] " + message)
        self.jobs = []
        self.current_recipe = None
        self.generate.setEnabled(True)
        QMessageBox.critical(self, "Proceso fallido", message)

    def _existing(self, family: str) -> set[int]:
        base = PROJECT / "artifacts" / "production" / "audiovisual" / family
        existing: set[int] = set()
        if base.exists():
            for path in base.glob("*_seed_*"):
                match = re.search(r"_seed_(\d+)", path.name)
                if match:
                    existing.add(int(match.group(1)))
        return existing

    def _run_challenge_job(self) -> None:
        if not self.jobs:
            self._job_complete()
            return
        recipe = self.current_recipe
        if recipe is None:
            return
        seed = self.jobs.pop(0)
        script = PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_challenge_production.ps1"
        args = [
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script),
            "-ChallengeId",
            recipe.challenge_id,
            "-Seed",
            str(seed),
            "-DeliveryProfile",
            recipe.delivery,
            "-OutputRoot",
            str(PROJECT / "artifacts" / "production" / "audiovisual" / "challenges" / recipe.challenge_id / f"seed_{seed}"),
        ]
        if recipe.no_sound:
            args.append("-NoSound")
        if recipe.force:
            args.append("-Force")
        if recipe.export_gif:
            args.append("-ExportGif")
        if recipe.keep_avi:
            args.append("-KeepAvi")
        self.table.setItem(0, 7, QTableWidgetItem(f"CHALLENGE {seed}"))
        self._launch(args)

    def _run_content_job(self) -> None:
        if not self.jobs:
            self._job_complete()
            return
        recipe = self.current_recipe
        if recipe is None:
            return
        seed = self.jobs.pop(0)

        if recipe.video_type == "visual_drills":
            params = recipe.targets or {}
            tier = int(recipe.grammar) if recipe.grammar not in ("auto", "AUTO") else random.randint(1, 5)
            speed = float(
                params.get(
                    "speed_multiplier",
                    random.uniform(*DRILLS[recipe.family].get("random_speed_range", [1.0, 1.0])),
                )
            )
            pacing = (
                str(params.get("pacing_mode", random.choice(["constant", "accelerating", "pulsed"])))
                if recipe.family == "tracking"
                else "constant"
            )
            script = ROOT / "run_visual_drill_production.ps1"
            args = [
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script),
                "-Family",
                recipe.family,
                "-Seed",
                str(seed),
                "-DifficultyTier",
                str(tier),
                "-SpeedMultiplier",
                f"{speed:.5f}",
                "-PacingMode",
                pacing,
                "-DeliveryProfile",
                recipe.delivery,
            ]
        else:
            script = PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_production.ps1"
            args = [
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script),
                "-Family",
                recipe.family,
                "-Seed",
                str(seed),
                "-DeliveryProfile",
                recipe.delivery,
            ]
            if recipe.grammar and recipe.grammar != "auto":
                args += ["-Grammar", recipe.grammar]

        if recipe.no_sound:
            args.append("-NoSound")
        if recipe.no_footer:
            args.append("-NoFooter")
        if recipe.force:
            args.append("-Force")
        if recipe.export_gif:
            args.append("-ExportGif")
        if recipe.keep_avi:
            args.append("-KeepAvi")
        self.table.setItem(0, 7, QTableWidgetItem(f"GENERANDO {seed}"))
        self._launch(args)

    def _job_complete(self) -> None:
        self.table.setItem(0, 7, QTableWidgetItem("COMPLETADA"))
        if self.queue:
            self.queue.pop(0)
        self.table.removeRow(0)
        self.current_recipe = None
        QTimer.singleShot(0, self._run_recipe)

    def _launch_python_regression(self) -> None:
        self.log.appendPlainText("[LAUNCH] python .\\tests\\run_all.py")
        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(str(PROJECT))
        self.proc.setProgram(sys.executable)
        self.proc.setArguments([str(PROJECT / "tests" / "run_all.py")])
        self.proc.readyReadStandardOutput.connect(self._out)
        self.proc.readyReadStandardError.connect(self._err)
        self.proc.finished.connect(self._done)
        self.proc.start()

    def _launch(self, args: list[str]) -> None:
        self.log.appendPlainText("\n[LAUNCH] powershell.exe " + " ".join(args))
        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(str(PROJECT))
        self.proc.setProgram("powershell.exe")
        self.proc.setArguments(args)
        self.proc.readyReadStandardOutput.connect(self._out)
        self.proc.readyReadStandardError.connect(self._err)
        self.proc.finished.connect(self._done)
        self.proc.start()

    def _out(self) -> None:
        if self.proc:
            data = bytes(self.proc.readAllStandardOutput()).decode("utf-8", errors="replace")
            if data:
                self.log.appendPlainText(data.rstrip())

    def _err(self) -> None:
        if self.proc:
            data = bytes(self.proc.readAllStandardError()).decode("utf-8", errors="replace")
            if data:
                self.log.appendPlainText("[STDERR] " + data.rstrip())

    def _done(self, code: int, _status: Any) -> None:
        self._out()
        self._err()
        process = self.proc
        self.proc = None
        if process:
            process.deleteLater()
        if code != 0:
            self.table.setItem(0, 7, QTableWidgetItem("ERROR"))
            self.jobs = []
            self.current_recipe = None
            self.generate.setEnabled(True)
            QMessageBox.critical(self, "Proceso fallido", f"Launcher terminó con código {code}. Revisa el LOG.")
            return

        recipe = self.current_recipe
        if recipe is None:
            return
        if recipe.operation == "RUN_REGRESSION":
            self._job_complete()
            return
        if recipe.video_type == "challenges":
            self._run_challenge_job()
            return
        if recipe.operation == "A_LA_CARTA":
            self._run_content_job()
            return
        self._job_complete()

    def _check_backend(self) -> None:
        profile_source = PROJECT / SCHEMA["backend_profile_source"]
        if not profile_source.exists():
            self.backend_info.setText("BACKEND: no encontrado")
            self.generate.setEnabled(False)
            return
        actual = hashlib.sha256(profile_source.read_bytes()).hexdigest()
        expected = SCHEMA["backend_profile_sha256"]
        backend_ok = actual == expected
        delivery_ok = DELIVERY_FILE.exists() and bool(DELIVERY_PROFILES)
        challenge_ok = len(CHALLENGES) == 9
        if backend_ok and delivery_ok and challenge_ok:
            self.backend_info.setText("BACKEND C11-C 2.16.9 FROZEN · DELIVERY OK · CHALLENGES 9/9")
        else:
            flags = []
            if not backend_ok:
                flags.append("BACKEND HASH MISMATCH")
            if not delivery_ok:
                flags.append("DELIVERY CONFIG MISSING")
            if not challenge_ok:
                flags.append(f"CHALLENGES {len(CHALLENGES)}/9")
            self.backend_info.setText(" · ".join(flags))
            self.generate.setEnabled(False)
            QTimer.singleShot(
                0,
                lambda: QMessageBox.critical(
                    self,
                    "Entorno incompatible",
                    "El Producer requiere el backend congelado, los perfiles de delivery actuales y el corpus CHALLENGE_001..009.",
                ),
            )


STYLE = """
QWidget{background:#f3f5f7;color:#1b2430;font-family:\"Segoe UI\";font-size:13px;} QLabel{background:transparent;}
QFrame#Banner{background:#fff;border:1px solid #d3dae2;border-radius:10px;min-height:60px;} QLabel#Title{font-size:22px;font-weight:700;color:#111827;} QLabel#Muted,QLabel#Hint{color:#5b6775;}
QGroupBox{background:#fff;border:1px solid #d3dae2;border-radius:9px;margin-top:10px;padding:10px;font-weight:700;}
QComboBox,QLineEdit,QSpinBox,QDoubleSpinBox{background:#fff;color:#17212b;border:1px solid #9aa7b5;border-radius:6px;min-height:40px;padding:0 10px;font-size:14px;}
QComboBox:focus,QLineEdit:focus,QSpinBox:focus,QDoubleSpinBox:focus{border:2px solid #2563eb;}
QComboBox::drop-down{width:34px;border-left:1px solid #aab5c0;background:#edf2f7;}
QComboBox QAbstractItemView{background:#fff;color:#17212b;border:1px solid #9aa7b5;selection-background-color:#dbeafe;selection-color:#111827;outline:0;padding:5px;} QComboBox QAbstractItemView::item{min-height:34px;padding:6px 8px;}
QCheckBox{min-height:30px;spacing:7px;} QCheckBox::indicator{width:18px;height:18px;}
QPushButton{background:#fff;color:#17212b;border:1px solid #9aa7b5;border-radius:7px;min-height:40px;padding:0 14px;font-weight:600;} QPushButton:hover{background:#eef4fb;}
QPushButton#Primary{background:#2563eb;color:#fff;border-color:#2563eb;min-height:46px;font-size:15px;} QPushButton#Primary:hover{background:#1d4ed8;}
QTableWidget,QPlainTextEdit{background:#fff;color:#17212b;border:1px solid #9aa7b5;border-radius:6px;} QHeaderView::section{background:#e9eef3;padding:8px;font-weight:700;border:0;min-height:26px;}
QScrollArea{border:0;background:#fff;} QScrollBar:vertical{width:14px;background:#e6ebf0;} QScrollBar::handle:vertical{background:#aeb9c5;min-height:34px;border-radius:7px;}
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE)
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
