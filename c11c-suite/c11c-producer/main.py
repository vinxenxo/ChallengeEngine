from __future__ import annotations

import hashlib
import json
import os
import random
import re
import sys
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from c11d_gui_request import (
    build_production_request,
    evaluate_gui_request,
    resolve_delivery_profile_data,
)

from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
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
    QSlider,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

APP_VERSION = "0.10.0"
ROOT = Path(__file__).resolve().parent
PROJECT = Path(os.environ.get("C11C_PROJECT_ROOT", ROOT.parents[1])).resolve()
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


def resolve_delivery_profile(profile_id: str) -> tuple[str, dict[str, Any]]:
    # Shared with the D9.5.1 request adapter so UI labels and D4 requests
    # consume the same central delivery registry/alias semantics.
    return resolve_delivery_profile_data(profile_id, DELIVERY_CONFIG)


def delivery_label(profile_id: str) -> str:
    try:
        resolved_id, profile = resolve_delivery_profile(profile_id)
    except ValueError:
        return profile_id
    width = profile.get("width", "?")
    height = profile.get("height", "?")
    if profile_id == "MASTER_1080":
        return "MASTER · 1080×1920 · ESTÁNDAR"
    if profile_id == "REVIEW_720":
        return "REVIEW · 720×1280 · C11-C"
    if profile_id == "MIN_540":
        return "MÍNIMO · 540×960"
    if profile_id == "META_REELS_FINAL_V1":
        return f"META REELS FINAL · {width}×{height}"
    if profile_id == "LONGFORM_1080":
        return "LONGFORM · 1080×1920"
    return f"{profile_id} · {width}×{height}"


DELIVERY_PROFILES = [
    pid for pid in DELIVERY_ORDER if pid in DELIVERY_CONFIG.get("profiles", {})
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
            phase_seconds = sum(
                float(video.get(key, 0.0))
                for key in ("hook_duration", "game_duration", "reveal_duration", "cta_duration")
            )
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
    delivery: str = DEFAULT_DELIVERY
    targets: dict[str, Any] = field(default_factory=dict)
    ui_row: int = -1
    status: str = "EN COLA"
    completed: bool = False
    current_seed: int | None = None
    failed_seeds: list[int] = field(default_factory=list)


class ParamRow(QWidget):
    """Compact visual control: slider + current value + random checkbox."""

    def __init__(self, spec: dict[str, Any]):
        super().__init__()
        self.spec = spec
        self.is_enum = spec["kind"] == "enum"
        self.values = list(spec.get("values", [])) if self.is_enum else []
        self.random_check = QCheckBox("ALEATORIO")
        self.random_check.setChecked(True)
        self.random_check.setMinimumWidth(105)
        self.random_check.setToolTip("Dejar que la seed determine este parámetro")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setTracking(True)
        self.slider.setMinimum(0)
        if self.is_enum:
            self.slider.setMaximum(max(0, len(self.values) - 1))
        else:
            minimum = float(spec["min"])
            maximum = float(spec["max"])
            step = float(spec["step"])
            steps = max(1, int(round((maximum - minimum) / step)))
            self.slider.setMaximum(steps)
        self.slider.setValue(self.slider.maximum() // 2)
        self.slider.setEnabled(False)
        self.slider.setMinimumWidth(135)

        self.value_label = QLabel(self._display_value())
        self.value_label.setObjectName("SliderValue")
        self.value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.value_label.setMinimumWidth(105)

        self.label = QLabel(str(spec["label"]))
        self.label.setMinimumWidth(132)
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(7)
        layout.addWidget(self.label)
        layout.addWidget(self.slider, 1)
        layout.addWidget(self.value_label)
        layout.addWidget(self.random_check)

        self.slider.valueChanged.connect(self._value_changed)
        self.random_check.toggled.connect(self._random_toggled)

    def _typed_value(self) -> Any:
        if self.is_enum:
            return self.values[self.slider.value()]
        minimum = float(self.spec["min"])
        step = float(self.spec["step"])
        value = minimum + self.slider.value() * step
        maximum = float(self.spec["max"])
        return min(maximum, value)

    def _display_value(self) -> str:
        value = self._typed_value()
        if self.is_enum:
            return str(value)
        step = float(self.spec["step"])
        if step < 0.001:
            return f"{value:.5f}"
        if step < 0.01:
            return f"{value:.3f}"
        if step < 0.1:
            return f"{value:.2f}"
        if step < 1:
            return f"{value:.1f}"
        return f"{value:.0f}"

    def _value_changed(self, _value: int) -> None:
        self.value_label.setText(self._display_value())

    def _random_toggled(self, random_enabled: bool) -> None:
        self.slider.setEnabled(self.isEnabled() and not random_enabled)
        self.value_label.setEnabled(not random_enabled)

    def set_interactive(self, enabled: bool) -> None:
        self.setEnabled(enabled)
        self.random_check.setEnabled(enabled)
        self.slider.setEnabled(enabled and not self.random_check.isChecked())
        self.value_label.setEnabled(enabled and not self.random_check.isChecked())

    def set_random(self) -> None:
        self.random_check.setChecked(True)

    def value(self) -> Any:
        return None if self.random_check.isChecked() else self._typed_value()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"C11-C Producer {APP_VERSION}")
        self.resize(1240, 860)
        self.queue: list[Recipe] = []
        self._table_recipes: list[Recipe] = []
        self.current_recipe: Recipe | None = None
        self.jobs: list[int] = []
        self.job_total = 0
        self.job_completed = 0
        self.proc: QProcess | None = None
        self.probe_file: Path | None = None
        self.rows: list[ParamRow] = []
        self._building_type = False
        self._build()
        self._check_backend()
        self._update_delivery_tooltip()

    def _build(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        main = QVBoxLayout(root)
        main.setContentsMargins(9, 9, 9, 7)
        main.setSpacing(7)

        self.tabs = QTabWidget()
        c11c_tab = QWidget()
        c11c_layout = QVBoxLayout(c11c_tab)
        c11c_layout.setContentsMargins(4, 4, 4, 4)
        cols = QHBoxLayout()
        cols.setSpacing(8)
        cols.addWidget(self._build_recipe(), 1)
        cols.addWidget(self._build_queue(), 1)
        c11c_layout.addLayout(cols, 1)
        self.tabs.addTab(c11c_tab, "C11-C · PRODUCTOR EXISTENTE")
        self.tabs.addTab(self._build_c11d_request_tab(), "C11-D · REQUEST + PERSONALIZACIÓN")
        main.addWidget(self.tabs, 1)

        self.statusBar().showMessage("Preparado")

    def _build_recipe(self) -> QGroupBox:
        box = QGroupBox("CREAR PRODUCCIÓN")
        root = QVBoxLayout(box)
        root.setContentsMargins(10, 9, 10, 10)
        root.setSpacing(7)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)

        self.operation = QComboBox()
        self.operation.addItem("A LA CARTA", "A_LA_CARTA")
        for key, label in SCHEMA.get("batch_operations", [])[1:]:
            self.operation.addItem(label, key)
        self.operation.addItem("REGRESIÓN COMPLETA", "RUN_REGRESSION")

        self.video_type = QComboBox()
        for key in ("challenges", "visual_loops", "visual_drills"):
            self.video_type.addItem(VIDEO_TYPES.get(key, key.upper()), key)

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

        self.family_label = QLabel("Familia")
        self.subtype_label = QLabel("Subfamilia")
        fields = [
            (0, QLabel("Operación"), self.operation),
            (1, QLabel("Tipo de vídeo"), self.video_type),
            (2, self.family_label, self.family),
            (3, self.subtype_label, self.grammar),
            (4, QLabel("Cantidad"), self.count),
            (5, QLabel("Seeds"), self.seed_mode),
        ]
        for row, label, widget in fields:
            grid.addWidget(label, row, 0)
            grid.addWidget(widget, row, 1)
        grid.addWidget(self.manual, 6, 0, 1, 2)
        root.addLayout(grid)

        opts = QGridLayout()
        opts.setHorizontalSpacing(8)
        opts.setVerticalSpacing(4)
        self.no_sound = QCheckBox("SIN AUDIO")
        self.no_footer = QCheckBox("SIN FOOTER")
        self.force = QCheckBox("FORCE")
        opts.addWidget(self.no_sound, 0, 0)
        opts.addWidget(self.no_footer, 0, 1)
        opts.addWidget(self.force, 0, 2)
        root.addLayout(opts)

        out = QGridLayout()
        out.setHorizontalSpacing(8)
        out.setVerticalSpacing(4)
        self.delivery = QComboBox()
        for profile_id in DELIVERY_PROFILES:
            self.delivery.addItem(delivery_label(profile_id), profile_id)
        self.delivery.setCurrentIndex(max(0, self.delivery.findData(DEFAULT_DELIVERY)))
        self.workers = QSpinBox()
        self.workers.setRange(1, 7)
        self.workers.setValue(7)
        self.resume = QCheckBox("RESUME")
        self.reset = QCheckBox("RESET")
        self.export_gif = QCheckBox("GIF")
        out.addWidget(QLabel("SALIDA"), 0, 0)
        out.addWidget(self.delivery, 0, 1, 1, 2)
        out.addWidget(QLabel("WORKERS"), 1, 0)
        out.addWidget(self.workers, 1, 1)
        out.addWidget(self.resume, 1, 2)
        out.addWidget(self.reset, 2, 0)
        out.addWidget(self.export_gif, 2, 1)
        root.addLayout(out)

        self.variation_box = QGroupBox("VARIACIÓN")
        variation = QVBoxLayout(self.variation_box)
        variation.setContentsMargins(8, 7, 8, 8)
        variation.setSpacing(3)
        self.pscroll = QScrollArea()
        self.pscroll.setWidgetResizable(True)
        self.pscroll.setFrameShape(QFrame.NoFrame)
        self.pwidget = QWidget()
        self.pl = QVBoxLayout(self.pwidget)
        self.pl.setContentsMargins(2, 1, 2, 1)
        self.pl.setSpacing(4)
        self.pl.setAlignment(Qt.AlignTop)
        self.pscroll.setWidget(self.pwidget)
        variation.addWidget(self.pscroll, 1)
        root.addWidget(self.variation_box, 1)

        self.add = QPushButton("AÑADIR A LA COLA")
        self.add.setObjectName("Primary")
        self.add.setMinimumHeight(44)
        root.addWidget(self.add)

        self.operation.currentIndexChanged.connect(self._operation_changed)
        self.video_type.currentIndexChanged.connect(self._video_type_changed)
        self.family.currentIndexChanged.connect(self._refresh_family)
        self.seed_mode.currentIndexChanged.connect(self._seed_mode_changed)
        self.delivery.currentIndexChanged.connect(self._update_delivery_tooltip)
        self.add.clicked.connect(self._add)
        self._operation_changed(0)
        return box

    def _build_queue(self) -> QGroupBox:
        box = QGroupBox("COLA DE PRODUCCIÓN")
        root = QVBoxLayout(box)
        root.setContentsMargins(10, 9, 10, 10)
        root.setSpacing(7)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            ["OPERACIÓN", "TIPO", "FAMILIA", "SUBTIPO", "CANTIDAD", "SALIDA", "WORKERS", "ESTADO"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSortingEnabled(False)
        root.addWidget(self.table, 3)

        btns = QHBoxLayout()
        self.generate = QPushButton("GENERAR")
        self.generate.setObjectName("Primary")
        self.generate.setMinimumHeight(46)
        self.remove = QPushButton("QUITAR")
        self.clear = QPushButton("VACIAR")
        btns.addWidget(self.generate, 2)
        btns.addWidget(self.remove)
        btns.addWidget(self.clear)
        root.addLayout(btns)

        lbox = QGroupBox("LOG")
        ll = QVBoxLayout(lbox)
        ll.setContentsMargins(7, 7, 7, 7)
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        ll.addWidget(self.log)
        root.addWidget(lbox, 2)

        self.generate.clicked.connect(self.start)
        self.remove.clicked.connect(self.remove_selected)
        self.clear.clicked.connect(self._clear)
        return box

    def _build_c11d_request_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(10)

        form_box = QGroupBox("D4 · PRODUCTION REQUEST")
        form = QGridLayout(form_box)
        form.setHorizontalSpacing(8)
        form.setVerticalSpacing(6)
        row = 0

        self.d_mode = QComboBox()
        self.d_mode.addItem("REVIEW · PLAN", "REVIEW")
        self.d_mode.addItem("PRODUCTION · PLAN ONLY (D4.8 BLOCKED)", "PRODUCTION")
        form.addWidget(QLabel("Modo"), row, 0)
        form.addWidget(self.d_mode, row, 1, 1, 2)
        row += 1

        self.d_challenge = QComboBox()
        for cid, item in sorted(CHALLENGES.items()):
            self.d_challenge.addItem(
                f"{cid} · {str(item['mechanic']).upper()} · {item['duration_seconds']:.0f}s",
                cid,
            )
        form.addWidget(QLabel("Challenge"), row, 0)
        form.addWidget(self.d_challenge, row, 1, 1, 2)
        row += 1

        self.d_seed = QSpinBox()
        self.d_seed.setRange(1, 2147483646)
        self.d_seed.setValue(12345)
        self.d_music_seed = QSpinBox()
        self.d_music_seed.setRange(1, 2147483646)
        self.d_music_seed.setValue(840001)
        form.addWidget(QLabel("Gameplay seed"), row, 0)
        form.addWidget(self.d_seed, row, 1)
        form.addWidget(QLabel("Music seed"), row, 2)
        form.addWidget(self.d_music_seed, row, 3)
        row += 1

        self.d_delivery = QComboBox()
        for profile_id in DELIVERY_PROFILES:
            self.d_delivery.addItem(delivery_label(profile_id), profile_id)
        review_index = self.d_delivery.findData("REVIEW_720")
        self.d_delivery.setCurrentIndex(review_index if review_index >= 0 else 0)
        form.addWidget(QLabel("Delivery profile"), row, 0)
        form.addWidget(self.d_delivery, row, 1, 1, 3)
        row += 1

        self.d_presentation = QLineEdit("social_default_v1")
        self.d_presentation.setPlaceholderText("presentation_profile_id")
        form.addWidget(QLabel("Presentation profile"), row, 0)
        form.addWidget(self.d_presentation, row, 1, 1, 3)
        row += 1

        self.d_variation = QSpinBox()
        self.d_variation.setRange(0, 1000000)
        self.d_variation.setValue(0)
        self.d_audio = QCheckBox("Audio enabled")
        self.d_audio.setChecked(True)
        form.addWidget(QLabel("Variation index"), row, 0)
        form.addWidget(self.d_variation, row, 1)
        form.addWidget(self.d_audio, row, 2, 1, 2)
        row += 1

        divider = QLabel("PERSONALIZACIÓN EDITORIAL · editorial_text_v1")
        divider.setObjectName("SectionHeader")
        form.addWidget(divider, row, 0, 1, 4)
        row += 1

        self.d_personalization = QCheckBox("Activar personalización editorial")
        self.d_personalization.setChecked(True)
        form.addWidget(self.d_personalization, row, 0, 1, 4)
        row += 1

        self.d_title = QLineEdit()
        self.d_subtitle = QLineEdit()
        self.d_cta = QLineEdit()
        self.d_language = QLineEdit("es")
        self.d_player_name = QLineEdit()
        self.d_challenge_label = QLineEdit()
        for edit, placeholder in (
            (self.d_title, "Título / hook"),
            (self.d_subtitle, "Subtítulo (opcional)"),
            (self.d_cta, "Llamada a la acción"),
            (self.d_language, "Idioma, p. ej. es"),
            (self.d_player_name, "Nombre de jugador (opcional)"),
            (self.d_challenge_label, "Etiqueta del Challenge"),
        ):
            edit.setMaxLength(160)
            edit.setPlaceholderText(placeholder)
        for label, widget in (
            ("Título", self.d_title),
            ("Subtítulo", self.d_subtitle),
            ("CTA", self.d_cta),
            ("Idioma", self.d_language),
            ("Player name", self.d_player_name),
            ("Challenge label", self.d_challenge_label),
        ):
            form.addWidget(QLabel(label), row, 0)
            form.addWidget(widget, row, 1, 1, 3)
            row += 1

        self.d_load_defaults = QPushButton("CARGAR TEXTOS BASE DEL CHALLENGE")
        self.d_load_defaults.clicked.connect(self._load_c11d_editorial_defaults)
        form.addWidget(self.d_load_defaults, row, 0, 1, 4)
        row += 1

        self.d_validate = QPushButton("VALIDAR REQUEST + GENERAR PLAN")
        self.d_validate.setObjectName("Primary")
        self.d_validate.setMinimumHeight(42)
        self.d_validate.clicked.connect(self._validate_c11d_request)
        form.addWidget(self.d_validate, row, 0, 1, 4)
        row += 1

        self.d_notice = QLabel(
            "D4.8 = BLOCKED · Esta vista valida request, personalización y plan. "
            "No activa renderer, no genera MP4 y no publica productos. La conexión "
            "de los textos al render real se certificará en D9.5.2."
        )
        self.d_notice.setWordWrap(True)
        self.d_notice.setObjectName("D4Notice")
        form.addWidget(self.d_notice, row, 0, 1, 4)
        layout.addWidget(form_box, 1)

        output_box = QGroupBox("CANONICAL OUTPUT / PARIDAD / EVIDENCIA")
        output_layout = QVBoxLayout(output_box)
        self.d_output_tabs = QTabWidget()
        self.d_request_view = QPlainTextEdit()
        self.d_canonical_view = QPlainTextEdit()
        self.d_personalization_view = QPlainTextEdit()
        self.d_plan_view = QPlainTextEdit()
        self.d_parity_view = QPlainTextEdit()
        self.d_command_view = QPlainTextEdit()
        for view in (
            self.d_request_view,
            self.d_canonical_view,
            self.d_personalization_view,
            self.d_plan_view,
            self.d_parity_view,
            self.d_command_view,
        ):
            view.setReadOnly(True)
            view.setLineWrapMode(QPlainTextEdit.NoWrap)
        for title, view in (
            ("GUI REQUEST", self.d_request_view),
            ("D4.2 CANONICAL", self.d_canonical_view),
            ("D4.3 PERSONALIZATION", self.d_personalization_view),
            ("D4.4 PLAN", self.d_plan_view),
            ("GUI ↔ CLI PARITY", self.d_parity_view),
            ("REPRODUCIBILITY", self.d_command_view),
        ):
            self.d_output_tabs.addTab(view, title)
        output_layout.addWidget(self.d_output_tabs, 1)
        self.d_evidence_label = QLabel("Todavía no se ha generado una evidencia D9.5.1.")
        self.d_evidence_label.setWordWrap(True)
        output_layout.addWidget(self.d_evidence_label)
        layout.addWidget(output_box, 1)

        self.d_personalization.toggled.connect(self._sync_c11d_personalization_controls)
        self.d_challenge.currentIndexChanged.connect(self._update_c11d_presentation_default)
        self._sync_c11d_personalization_controls(self.d_personalization.isChecked())
        self._load_c11d_editorial_defaults()
        return tab

    def _sync_c11d_personalization_controls(self, enabled: bool) -> None:
        for widget in (
            self.d_title,
            self.d_subtitle,
            self.d_cta,
            self.d_language,
            self.d_player_name,
            self.d_challenge_label,
        ):
            widget.setEnabled(enabled)

    def _selected_c11d_challenge_document(self) -> dict[str, Any]:
        cid = str(self.d_challenge.currentData() or "")
        item = CHALLENGES.get(cid)
        if not item:
            raise ValueError("Selecciona un Challenge válido.")
        path = Path(item["path"])
        document = json.loads(path.read_text(encoding="utf-8-sig"))
        if str(document.get("challenge_id", "")) != cid:
            raise ValueError(f"Challenge ID/file mismatch: {cid}")
        return document

    def _update_c11d_presentation_default(self, _index: int = -1) -> None:
        try:
            document = self._selected_c11d_challenge_document()
            profile_id = str((document.get("presentation") or {}).get("profile", "UNKNOWN"))
            if not self.d_presentation.text().strip() or self.d_presentation.text().strip() == "social_default_v1":
                self.d_presentation.setText(profile_id)
        except Exception:
            return

    def _load_c11d_editorial_defaults(self) -> None:
        try:
            document = self._selected_c11d_challenge_document()
            content = document.get("content") or {}
            self.d_title.setText(str(content.get("hook", ""))[:160])
            self.d_cta.setText(str(content.get("cta", ""))[:160])
            self.d_challenge_label.setText(str(document.get("mechanic", "UNKNOWN")).upper()[:160])
            self.d_presentation.setText(str((document.get("presentation") or {}).get("profile", "UNKNOWN")))
            self.statusBar().showMessage("Textos base cargados desde la definición existente; los cambios aún son plan-only.")
        except Exception as exc:
            QMessageBox.warning(self, "C11-D Request", str(exc))

    def _verify_c11d_planning_predecessors(self) -> None:
        receipt_paths = (
            PROJECT / "artifacts" / "tests" / "c11d_d4" / "d4_2" / "d4_2_validation_receipt.json",
            PROJECT / "artifacts" / "tests" / "c11d_d4" / "d4_3" / "d4_3_validation_receipt.json",
            PROJECT / "artifacts" / "tests" / "c11d_d4" / "d4_4" / "d4_4_validation_receipt.json",
            PROJECT / "artifacts" / "tests" / "c11d_d4" / "d4_6" / "d4_6_validation_receipt.json",
            PROJECT / "artifacts" / "tests" / "c11d_d4" / "d4_7" / "d4_7_validation_receipt.json",
        )
        for receipt_path in receipt_paths:
            if not receipt_path.is_file():
                raise RuntimeError(f"Falta evidencia PASS/CLOSED previa de D4: {receipt_path}")
            receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
            if receipt.get("result") != "PASS" or receipt.get("status") != "CLOSED":
                raise RuntimeError(f"El checkpoint D4 no está PASS/CLOSED: {receipt_path}")

    def _validate_c11d_request(self) -> None:
        try:
            self._verify_c11d_planning_predecessors()
            challenge_document = self._selected_c11d_challenge_document()
            requested_profile = str(self.d_delivery.currentData())
            _resolved_id, resolved_profile = resolve_delivery_profile(requested_profile)
            request_id = "C11D-GUI-{0}-{1}".format(
                datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
                uuid.uuid4().hex[:10].upper(),
            )
            editorial_values = {
                "title": self.d_title.text(),
                "subtitle": self.d_subtitle.text(),
                "call_to_action": self.d_cta.text(),
                "language": self.d_language.text(),
                "player_name": self.d_player_name.text(),
                "challenge_label": self.d_challenge_label.text(),
            }
            request = build_production_request(
                request_id=request_id,
                mode=str(self.d_mode.currentData()),
                challenge_document=challenge_document,
                delivery_profile_id=requested_profile,
                resolved_delivery_profile=resolved_profile,
                presentation_profile_id=self.d_presentation.text().strip() or "UNKNOWN",
                seed=int(self.d_seed.value()),
                music_seed=int(self.d_music_seed.value()),
                audio_enabled=bool(self.d_audio.isChecked()),
                variation_index=int(self.d_variation.value()),
                personalization_enabled=bool(self.d_personalization.isChecked()),
                editorial_values=editorial_values,
            )
            result = evaluate_gui_request(request, PROJECT)

            evidence_root = PROJECT / "artifacts" / "tests" / "c11d_d9" / "producer_gui"
            evidence_root.mkdir(parents=True, exist_ok=True)
            run_root = evidence_root / request_id
            run_root.mkdir(parents=False, exist_ok=False)

            def write_json(path: Path, value: Any) -> None:
                path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            write_json(run_root / "request.json", result["request"])
            write_json(run_root / "canonical_request.json", result["canonical_request"])
            write_json(run_root / "resolved_personalization.json", result["resolved_personalization"])
            write_json(run_root / "production_plan.json", result["plan"])
            write_json(run_root / "gui_cli_parity.json", result["parity"])
            receipt = {
                "schema": "C11-D-D9.5.1-PRODUCER-GUI-RECEIPT-V1",
                "phase": "D9.5.1",
                "result": "PASS_PLAN_ONLY",
                "status": "PLANNED",
                "request_id": request_id,
                "request_hash": result["request_hash"],
                "personalization_hash": result["personalization_hash"],
                "plan_hash": result["plan_hash"],
                "gui_cli_parity": result["parity"]["status"],
                "renderer_execution": False,
                "production_execution": False,
                "release_authority": "NONE",
                "d4_8": "BLOCKED",
                "evidence_root": str(run_root.relative_to(PROJECT)).replace("/", "\\"),
            }
            write_json(run_root / "producer_gui_receipt.json", receipt)

            relative_request = str((run_root / "request.json").relative_to(PROJECT)).replace("/", "\\")
            relative_plan = str((run_root / "production_plan_cli.json").relative_to(PROJECT)).replace("/", "\\")
            command = f'python .\\tools\\c11d\\d4\\production_cli.py --request ".\\{relative_request}" --output ".\\{relative_plan}"'
            self.d_request_view.setPlainText(json.dumps(request, ensure_ascii=False, indent=2))
            self.d_canonical_view.setPlainText(json.dumps(result["canonical_request"], ensure_ascii=False, indent=2))
            self.d_personalization_view.setPlainText(json.dumps(result["resolved_personalization"], ensure_ascii=False, indent=2))
            self.d_plan_view.setPlainText(json.dumps(result["plan"], ensure_ascii=False, indent=2))
            self.d_parity_view.setPlainText(json.dumps(result["parity"], ensure_ascii=False, indent=2))
            self.d_command_view.setPlainText(
                "PLAN ONLY — reproduce with the canonical D4.5 CLI:\n\n" + command
                + "\n\nThe CLI command consumes the saved request; it does not activate the renderer."
            )
            self.d_evidence_label.setText(f"Evidencia: {run_root}")
            self.d_output_tabs.setCurrentWidget(self.d_parity_view)
            self.statusBar().showMessage(
                f"D9.5.1 PLAN PASS · GUI/CLI parity exact · plan={result['plan_hash'][:12]} · D4.8 BLOCKED"
            )
        except Exception as exc:
            self.statusBar().showMessage("D9.5.1 plan failed; no product was created.")
            QMessageBox.warning(self, "C11-D Request / Personalización", str(exc))

    def _clear_rows(self) -> None:
        while self.pl.count():
            item = self.pl.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.rows = []

    def _video_type_changed(self, _idx: int) -> None:
        if self._building_type or self.operation.currentData() != "A_LA_CARTA":
            return
        self._building_type = True
        try:
            video_type = str(self.video_type.currentData())
            self._clear_rows()
            self.family.blockSignals(True)
            self.grammar.blockSignals(True)
            self.family.clear()
            self.grammar.clear()

            if video_type == "challenges":
                self.family_label.setText("Challenge")
                self.subtype_label.setText("Mecánica")
                for cid, item in sorted(CHALLENGES.items()):
                    self.family.addItem(
                        f"{cid} · {item['mechanic'].upper()} · {item['duration_seconds']:.0f}s",
                        cid,
                    )
                self._refresh_challenges()
                self.variation_box.setVisible(False)
                self.no_footer.setChecked(False)
                self.no_footer.setEnabled(False)
            elif video_type == "visual_loops":
                self.family_label.setText("Familia")
                self.subtype_label.setText("Gramática")
                self.family.addItems([value["name"] for value in FAMILIES.values()])
                self._refresh_family(0)
                self.variation_box.setVisible(True)
                self.no_footer.setEnabled(True)
            else:
                self.family_label.setText("Familia")
                self.subtype_label.setText("Dificultad")
                self.family.addItems([value["name"] for value in DRILLS.values()])
                self._refresh_family(0)
                self.variation_box.setVisible(True)
                self.no_footer.setChecked(False)
                self.no_footer.setEnabled(False)
            self.family.blockSignals(False)
            self.grammar.blockSignals(False)
        finally:
            self._building_type = False
        if video_type != "challenges":
            self._refresh_family(self.family.currentIndex() if self.family.count() else 0)
        self._seed_mode_changed(self.seed_mode.currentIndex())
        self._set_status(f"{VIDEO_TYPES.get(video_type, video_type)}")

    def _refresh_challenges(self) -> None:
        cid = str(self.family.currentData() or "")
        item = CHALLENGES.get(cid)
        self.grammar.clear()
        if item:
            self.grammar.addItem(item["mechanic"].upper(), item["mechanic"])

    def _refresh_family(self, idx: int) -> None:
        if self._building_type:
            return
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
            family_id = ids[idx]
            self.family.blockSignals(True)
            self.family.setCurrentIndex(idx)
            self.family.blockSignals(False)
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
            family_id = ids[idx]
            self.family.blockSignals(True)
            self.family.setCurrentIndex(idx)
            self.family.blockSignals(False)
            self.grammar.clear()
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
        self.delivery.setEnabled(not batch and not utility)
        self.workers.setEnabled(True)
        self.resume.setEnabled(batch and not utility)
        self.reset.setEnabled(batch and not utility and op != "REVIEW_CHALLENGES")
        self.export_gif.setEnabled(not utility)
        self.add.setEnabled(True)
        self.variation_box.setVisible(not batch and not utility and str(self.video_type.currentData()) != "challenges")
        if batch:
            self.variation_box.setVisible(False)
        if utility:
            self.variation_box.setVisible(False)
        else:
            self._video_type_changed(self.video_type.currentIndex())

    def _seed_mode_changed(self, idx: int) -> None:
        active = self.operation.currentData() == "A_LA_CARTA"
        manual = idx == 1
        self.manual.setEnabled(active and manual)
        for row in self.rows:
            row.set_interactive(active)

    def _update_delivery_tooltip(self, _idx: int = -1) -> None:
        profile_id = str(self.delivery.currentData() or "")
        try:
            resolved_id, profile = resolve_delivery_profile(profile_id)
            width = profile.get("width", "?")
            height = profile.get("height", "?")
            fps = profile.get("fps", profile.get("fps_max", "?"))
            codec = str(profile.get("codec", "h264")).upper()
            audio = f"{profile.get('audio_codec', 'AAC').upper()} {profile.get('audio_sample_rate_hz', 48000)} Hz estéreo"
            self.delivery.setToolTip(
                f"{profile_id} · {width}×{height} · {fps} FPS · {codec} · {audio}\nBase: {resolved_id}"
            )
        except ValueError as exc:
            self.delivery.setToolTip(str(exc))

    def _set_status(self, text: str) -> None:
        self.statusBar().showMessage(text)

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
                    delivery="REVIEW_720",
                )
                self.queue.append(recipe)
                self._add_row(recipe)
                return

            video_type = str(self.video_type.currentData())
            manual = self._manual_seeds() if self.seed_mode.currentIndex() == 1 else []
            delivery = str(self.delivery.currentData() or DEFAULT_DELIVERY)

            if video_type == "challenges":
                cid = str(self.family.currentData() or "")
                if cid not in CHALLENGES:
                    raise ValueError("Selecciona un Challenge válido.")
                recipe = Recipe(
                    op,
                    video_type,
                    family=str(self.family.currentText()),
                    grammar=str(self.grammar.currentData() or ""),
                    challenge_id=cid,
                    count=self.count.value(),
                    manual_seeds=manual,
                    no_sound=self.no_sound.isChecked(),
                    force=self.force.isChecked(),
                    export_gif=self.export_gif.isChecked(),
                    delivery=delivery,
                )
            else:
                ids = list(FAMILIES if video_type == "visual_loops" else DRILLS)
                if not ids:
                    raise ValueError("No hay familias disponibles.")
                family_id = ids[self.family.currentIndex()]
                targets = {
                    row.spec["key"]: value
                    for row in self.rows
                    if (value := row.value()) is not None
                }
                grammar = str(self.grammar.currentData() or "auto")
                if video_type == "visual_loops" and manual and (grammar != "auto" or targets):
                    raise ValueError(
                        "Con seeds manuales, deja gramática y variación en ALEATORIO."
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
                    export_gif=self.export_gif.isChecked(),
                )
            already_produced = self._recipe_already_produced(recipe) and not recipe.force
            if already_produced:
                recipe.status = "YA PRODUCIDO"
                recipe.completed = True
                self._add_row(recipe)
            else:
                self.queue.append(recipe)
                self._add_row(recipe)
        except Exception as exc:
            QMessageBox.warning(self, "Configuración inválida", str(exc))

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

    def _recipe_already_produced(self, recipe: Recipe) -> bool:
        if not recipe.manual_seeds:
            return False

        def matches_profile(product_dir: Path) -> bool:
            manifest = product_dir / "production_manifest.json"
            if not manifest.exists():
                return False
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return False
            return str(data.get("delivery_profile", "")) == recipe.delivery and any(product_dir.glob("*.mp4"))

        for seed in recipe.manual_seeds:
            if recipe.video_type == "challenges":
                base = PROJECT / "artifacts" / "production" / "audiovisual" / "challenges" / recipe.challenge_id / f"seed_{seed}"
                if not matches_profile(base):
                    return False
            elif recipe.video_type in ("visual_loops", "visual_drills"):
                family_root = recipe.family if recipe.video_type == "visual_loops" else str(Path("visual_drills") / recipe.family)
                base = PROJECT / "artifacts" / "production" / "audiovisual" / family_root
                if not base.exists() or not any(matches_profile(p) for p in base.iterdir() if p.is_dir() and f"seed_{seed}" in p.name):
                    return False
            else:
                return False
        return True

    def _add_row(self, recipe: Recipe) -> None:
        row = self.table.rowCount()
        recipe.ui_row = row
        self._table_recipes.append(recipe)
        self.table.insertRow(row)
        values = [
            recipe.operation,
            recipe.video_type,
            recipe.family or recipe.challenge_id,
            recipe.grammar or "—",
            str(recipe.count),
            recipe.delivery if recipe.video_type != "batch" else "—",
            str(recipe.workers),
            recipe.status,
        ]
        for index, value in enumerate(values):
            item = QTableWidgetItem(value)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, index, item)
        state = "done" if recipe.status == "YA PRODUCIDO" else "pending"
        self._style_row(row, state)
        if state != "done":
            self.table.selectRow(row)

    def _reindex_rows(self) -> None:
        for index, recipe in enumerate(self._table_recipes):
            recipe.ui_row = index

    def _style_row(self, row: int, state: str) -> None:
        if row < 0 or row >= self.table.rowCount():
            return
        if state == "done":
            foreground = Qt.GlobalColor.darkGray
        elif state == "error":
            foreground = Qt.GlobalColor.red
        else:
            foreground = Qt.GlobalColor.white
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            if item:
                item.setForeground(foreground)
                item.setToolTip("Producción completada" if state == "done" else "")

    def _set_recipe_status(self, recipe: Recipe, status: str, state: str = "pending") -> None:
        recipe.status = status
        row = recipe.ui_row
        if 0 <= row < self.table.rowCount():
            self.table.item(row, 7).setText(status)
            self._style_row(row, state)
            self.table.selectRow(row)

    def remove_selected(self) -> None:
        if self.proc:
            return
        row = self.table.currentRow()
        if row < 0 or row >= len(self._table_recipes):
            return
        recipe = self._table_recipes[row]
        if recipe in self.queue:
            self.queue.remove(recipe)
        self._table_recipes.pop(row)
        self.table.removeRow(row)
        self._reindex_rows()
        self._set_status("Elemento eliminado")

    def _clear(self) -> None:
        if self.proc:
            return
        self.queue.clear()
        self._table_recipes.clear()
        self.table.setRowCount(0)
        self._set_status("Cola vacía")

    def start(self) -> None:
        if self.proc or not self.queue:
            return
        self.generate.setEnabled(False)
        self._run_recipe()

    def _run_recipe(self) -> None:
        if not self.queue:
            self.current_recipe = None
            self.generate.setEnabled(True)
            self._set_status("Producción finalizada")
            self.log.appendPlainText("\n=== PRODUCCIÓN FINALIZADA ===")
            return
        self.current_recipe = self.queue[0]
        self.jobs = []
        self.job_total = 0
        self.job_completed = 0
        recipe = self.current_recipe
        if recipe.ui_row >= 0:
            self.table.selectRow(recipe.ui_row)
        if recipe.operation == "RUN_REGRESSION":
            self._set_recipe_status(recipe, "REGRESIÓN")
            self._launch_python_regression()
            return
        if recipe.operation != "A_LA_CARTA":
            if recipe.operation == "REVIEW_CHALLENGES":
                script = PROJECT / "tools" / "qa" / "c11" / "run_c11c_challenge_bulk_qa.ps1"
                args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)]
                if recipe.resume:
                    args.append("-Resume")
                self._set_recipe_status(recipe, "REVIEW CHALLENGES")
                self._launch(args)
                return

            script = PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_art_direction_batch_v4.ps1"
            args = ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), "-Workers", str(recipe.workers)]
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
            self._set_recipe_status(recipe, "REVIEW")
            self._launch(args)
            return

        if recipe.video_type == "challenges":
            self.jobs = list(recipe.manual_seeds) if recipe.manual_seeds else self._new_unique_seeds(recipe.count)
            self.job_total = len(self.jobs)
            self._run_challenge_job()
            return
        if recipe.video_type == "visual_drills":
            self.jobs = list(recipe.manual_seeds) if recipe.manual_seeds else self._new_unique_seeds(recipe.count)
            self.job_total = len(self.jobs)
            self._run_content_job()
            return
        self._prepare_loop_jobs()

    def _prepare_loop_jobs(self) -> None:
        recipe = self.current_recipe
        if recipe is None:
            return
        if recipe.manual_seeds:
            self.jobs = list(recipe.manual_seeds)
            self.job_total = len(self.jobs)
            self._run_content_job()
            return
        if recipe.grammar == "auto" and not recipe.targets:
            existing = self._existing(recipe.family)
            while len(self.jobs) < recipe.count:
                seed = random.randint(1, 2_147_483_646)
                if seed not in existing and seed not in self.jobs:
                    self.jobs.append(seed)
            self.job_total = len(self.jobs)
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
        self._set_status("Buscando seeds compatibles…")
        self.log.appendPlainText("[SEED PLANNER] búsqueda en curso")

        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(str(PROJECT))
        self.proc.setProgram("godot")
        self.proc.setArguments(["--headless", "--path", str(PROJECT), "--script", str(ROOT / "seed_probe.gd"), "--", str(self.probe_file)])
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
        self.job_total = len(self.jobs)
        self.log.appendPlainText("[SEEDS PLANNER] " + ", ".join(map(str, self.jobs)))
        self._run_content_job()

    def _new_unique_seeds(self, count: int) -> list[int]:
        seeds: list[int] = []
        seen: set[int] = set()
        while len(seeds) < count:
            value = random.randint(1, 2_147_483_646)
            if value not in seen:
                seen.add(value)
                seeds.append(value)
        return seeds

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
        recipe.current_seed = seed
        self.job_completed = self.job_total - len(self.jobs) - 1
        script = PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_challenge_production.ps1"
        args = [
            "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
            "-ChallengeId", recipe.challenge_id, "-Seed", str(seed),
            "-DeliveryProfile", recipe.delivery,
            "-OutputRoot", str(PROJECT / "artifacts" / "production" / "audiovisual" / "challenges" / recipe.challenge_id / f"seed_{seed}"),
        ]
        if recipe.no_sound:
            args.append("-NoSound")
        if recipe.force:
            args.append("-Force")
        if recipe.export_gif:
            args.append("-ExportGif")
        self._set_recipe_status(recipe, f"GENERANDO {self.job_completed + 1}/{self.job_total} · {seed}")
        self._launch(args)

    def _run_content_job(self) -> None:
        if not self.jobs:
            self._job_complete()
            return
        recipe = self.current_recipe
        if recipe is None:
            return
        seed = self.jobs.pop(0)
        recipe.current_seed = seed
        job_index = self.job_total - len(self.jobs)
        if recipe.video_type == "visual_drills":
            params = recipe.targets or {}
            tier = int(recipe.grammar) if recipe.grammar not in ("auto", "AUTO", "") else random.randint(1, 5)
            speed = float(params.get("speed_multiplier", random.uniform(*DRILLS[recipe.family].get("random_speed_range", [1.0, 1.0]))))
            pacing = str(params.get("pacing_mode", random.choice(["constant", "accelerating", "pulsed"]))) if recipe.family == "tracking" else "constant"
            script = ROOT / "run_visual_drill_production.ps1"
            args = [
                "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
                "-Family", recipe.family, "-Seed", str(seed), "-DifficultyTier", str(tier),
                "-SpeedMultiplier", f"{speed:.5f}", "-PacingMode", pacing,
                "-DeliveryProfile", recipe.delivery,
            ]
        else:
            script = PROJECT / "tools" / "prototypes" / "c11c_bulk" / "run_c11c_production.ps1"
            args = [
                "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
                "-Family", recipe.family, "-Seed", str(seed), "-DeliveryProfile", recipe.delivery,
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
        self._set_recipe_status(recipe, f"GENERANDO {job_index}/{self.job_total} · {seed}")
        self._launch(args)

    def _job_complete(self) -> None:
        recipe = self.current_recipe
        if recipe is None:
            return
        failed = len(recipe.failed_seeds)
        if failed:
            successful = max(0, self.job_total - failed)
            self._set_recipe_status(recipe, f"FINALIZADA {successful}/{self.job_total} · {failed} ERROR", "error")
            recipe.completed = False
            self._set_status(f"Elemento finalizado con {failed} error(es)")
        else:
            self._set_recipe_status(recipe, "COMPLETADA", "done")
            recipe.completed = True
            self._set_status("Elemento completado")
        recipe.current_seed = None
        if recipe in self.queue:
            self.queue.remove(recipe)
        self.current_recipe = None
        self.jobs = []
        self.job_total = 0
        self.job_completed = 0
        self._run_recipe()
        if not self.queue:
            self.table.clearSelection()

    def _launch_python_regression(self) -> None:
        self.log.appendPlainText("[LAUNCH] python .\\tests\\run_all.py")
        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(str(PROJECT))
        self.proc.setProgram(sys.executable)
        self.proc.setArguments([str(PROJECT / "tests" / "run_all.py")])
        self.proc.readyReadStandardOutput.connect(self._out)
        self.proc.readyReadStandardError.connect(self._err)
        self.proc.finished.connect(self._done)
        self.proc.errorOccurred.connect(self._process_error)
        self.proc.start()

    def _launch(self, args: list[str]) -> None:
        if self.proc:
            return
        self.log.appendPlainText("\n[LAUNCH] powershell.exe " + " ".join(self._display_arg(a) for a in args))
        self.proc = QProcess(self)
        self.proc.setWorkingDirectory(str(PROJECT))
        self.proc.setProgram("powershell.exe")
        self.proc.setArguments(args)
        self.proc.readyReadStandardOutput.connect(self._out)
        self.proc.readyReadStandardError.connect(self._err)
        self.proc.finished.connect(self._done)
        self.proc.errorOccurred.connect(self._process_error)
        self.proc.start()

    @staticmethod
    def _display_arg(value: str) -> str:
        return f'"{value}"' if any(ch.isspace() for ch in value) else value

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

    def _process_error(self, error: QProcess.ProcessError) -> None:
        if self.proc is None:
            return
        if error != QProcess.ProcessError.FailedToStart:
            return
        self._out()
        self._err()
        process = self.proc
        self.proc = None
        if process:
            process.deleteLater()
        self._finish_error("No se pudo iniciar el proceso externo (QProcess FailedToStart).")

    def _finish_error(self, message: str) -> None:
        recipe = self.current_recipe
        self.log.appendPlainText("[ERROR] " + message)
        if recipe is None:
            self.generate.setEnabled(bool(self.queue))
            self._set_status("Proceso fallido")
            self._run_recipe()
            return

        # A single failed seed must not poison the rest of the queue.
        if recipe.operation == "A_LA_CARTA" and recipe.current_seed is not None:
            failed_seed = recipe.current_seed
            if failed_seed not in recipe.failed_seeds:
                recipe.failed_seeds.append(failed_seed)
            remaining = len(self.jobs)
            recipe.current_seed = None
            if remaining:
                self._set_recipe_status(
                    recipe,
                    f"ERROR {failed_seed} · CONTINÚA {self.job_total - remaining}/{self.job_total}",
                    "error",
                )
                self._set_status(f"Seed {failed_seed} falló; continúa la cola")
                self.log.appendPlainText(
                    f"[JOB-ERROR] seed={failed_seed} registrado; continuando con {remaining} job(s) restantes."
                )
                if recipe.video_type == "challenges":
                    self._run_challenge_job()
                else:
                    self._run_content_job()
                return

            # Last seed failed: finalize this recipe and continue with the next one.
            self._job_complete()
            return

        # Batch/utility failure: isolate this recipe and continue with the next queue item.
        self._set_recipe_status(recipe, "ERROR", "error")
        recipe.completed = False
        recipe.current_seed = None
        self.jobs = []
        self.job_total = 0
        self.job_completed = 0
        if recipe in self.queue:
            self.queue.remove(recipe)
        self.current_recipe = None
        self.generate.setEnabled(bool(self.queue))
        self._set_status("Proceso fallido · cola continua")
        self._run_recipe()

    def _done(self, code: int, _status: Any) -> None:
        self._out()
        self._err()
        process = self.proc
        self.proc = None
        if process:
            process.deleteLater()
        if code != 0:
            self._finish_error(f"Launcher terminó con código {code}. Revisa el LOG.")
            return

        recipe = self.current_recipe
        if recipe is None:
            return
        recipe.current_seed = None
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
            self._set_status("BACKEND no encontrado")
            self.generate.setEnabled(False)
            return
        actual = hashlib.sha256(profile_source.read_bytes()).hexdigest()
        expected = SCHEMA["backend_profile_sha256"]
        backend_ok = actual == expected
        delivery_ok = DELIVERY_FILE.exists() and bool(DELIVERY_PROFILES)
        challenge_ok = len(CHALLENGES) == 9
        if backend_ok and delivery_ok and challenge_ok:
            self._set_status("BACKEND 2.16.9 FROZEN · DELIVERY OK · CHALLENGES 9/9")
        else:
            flags = []
            if not backend_ok:
                flags.append("BACKEND HASH MISMATCH")
            if not delivery_ok:
                flags.append("DELIVERY CONFIG MISSING")
            if not challenge_ok:
                flags.append(f"CHALLENGES {len(CHALLENGES)}/9")
            self._set_status(" · ".join(flags))
            self.generate.setEnabled(False)


STYLE = """
QWidget{background:#080d14;color:#e7f7ff;font-family:\"Segoe UI\";font-size:12px;}
QLabel{background:transparent;color:#d9edf5;}
QGroupBox{background:#0d141d;border:1px solid #234353;border-radius:8px;margin-top:8px;padding:8px;font-weight:700;color:#69f5ff;}
QGroupBox::title{subcontrol-origin:margin;left:9px;padding:0 5px;color:#69f5ff;}
QComboBox,QLineEdit,QSpinBox,QDoubleSpinBox{background:#0a1119;color:#e7f7ff;border:1px solid #315365;border-radius:5px;min-height:34px;padding:0 8px;font-size:13px;selection-background-color:#ff2bd6;}
QComboBox:focus,QLineEdit:focus,QSpinBox:focus,QDoubleSpinBox:focus{border:1px solid #00f0ff;}
QComboBox::drop-down{width:28px;border-left:1px solid #244655;background:#111c27;}
QComboBox QAbstractItemView{background:#0d141d;color:#e7f7ff;border:1px solid #00aeca;selection-background-color:#ff2bd6;selection-color:#ffffff;padding:4px;}
QCheckBox{min-height:26px;spacing:5px;color:#cbeaf2;}
QCheckBox::indicator{width:16px;height:16px;border:1px solid #356274;border-radius:3px;background:#091019;}
QCheckBox::indicator:checked{background:#00d9ff;border:1px solid #00f0ff;}
QPushButton{background:#101a24;color:#dffaff;border:1px solid #325668;border-radius:6px;min-height:36px;padding:0 12px;font-weight:700;}
QPushButton:hover{background:#162532;border-color:#00d9ff;color:#ffffff;}
QPushButton#Primary{background:#00c8e6;color:#031018;border-color:#00f0ff;min-height:44px;font-size:14px;}
QPushButton#Primary:hover{background:#45eaff;border-color:#ff2bd6;}
QPushButton#Primary:pressed{background:#ff2bd6;color:#ffffff;border-color:#ff71df;}
QTableWidget,QPlainTextEdit{background:#09111a;color:#dffaff;border:1px solid #274655;border-radius:6px;}
QTableWidget::item{padding:7px 6px;border-bottom:1px solid #142632;}
QTableWidget::item:selected{background:#ff2bd6;color:#ffffff;border:1px solid #ff71df;}
QHeaderView::section{background:#101c27;color:#69f5ff;padding:7px;font-weight:800;border:0;border-right:1px solid #203643;min-height:25px;}
QScrollArea{border:0;background:#0d141d;}
QScrollBar:vertical{width:11px;background:#09111a;}
QScrollBar::handle:vertical{background:#284a5a;min-height:28px;border-radius:5px;}
QScrollBar::handle:vertical:hover{background:#00b9d5;}
QSlider::groove:horizontal{height:5px;border-radius:2px;background:#213441;}
QSlider::sub-page:horizontal{background:#00cfe8;border-radius:2px;}
QSlider::handle:horizontal{width:15px;margin:-5px 0;border-radius:8px;background:#ff2bd6;border:1px solid #ff8be8;}
QSlider::handle:horizontal:hover{background:#ff71df;}
QLabel#SliderValue{color:#a9f7ff;font-family:"Consolas";font-size:11px;}
QStatusBar{background:#070c12;color:#6ff5ff;border-top:1px solid #1e3743;}
"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE)
    window = MainWindow()
    window.show()
    raise SystemExit(app.exec())
