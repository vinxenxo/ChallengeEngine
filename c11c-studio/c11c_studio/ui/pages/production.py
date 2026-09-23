import random

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QSpinBox, QComboBox, QGroupBox,
                               QFormLayout, QCheckBox, QMessageBox)
from PySide6.QtCore import Signal


def _unique_random_seeds(n):
    seen = set()
    out = []
    while len(out) < n:
        s = random.randint(1, 2147483647)
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


class ProductionPage(QWidget):
    request_single = Signal(dict)
    request_5x5 = Signal(dict)

    def __init__(self, families, parent=None):
        super().__init__(parent)
        self.families = families
        self.family_by_folder = {f.folder: f for f in families}
        self._pending_5x5_seeds = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        t = QLabel("Production")
        t.setObjectName("PageTitle")
        s = QLabel("Protected zone - one canonical MP4 per product. "
                   "Existing products are not overwritten.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t)
        root.addWidget(s)

        gb1 = QGroupBox("Single Product")
        f1 = QFormLayout(gb1)

        self.cb_family = QComboBox()
        for f in families:
            self.cb_family.addItem(
                f.artistic + "  (" + f.technical + ")", f.folder)
        self.cb_family.currentIndexChanged.connect(self._refresh_grammars)

        self.cb_grammar = QComboBox()
        self.cb_grammar.setEnabled(False)
        self.cb_grammar.currentIndexChanged.connect(self._update_run_state)

        self.chk_send_grammar = QCheckBox(
            "Send -Grammar to backend (only if the .ps1 supports it)")
        self.chk_send_grammar.setChecked(False)
        self.chk_send_grammar.toggled.connect(self._on_send_grammar_toggled)

        self.lbl_grammar_hint = QLabel("")
        self.lbl_grammar_hint.setStyleSheet(
            "color:#8b96a8; font-family:Consolas; font-size:8pt;")
        self.lbl_grammar_hint.setWordWrap(True)

        grammar_row = QVBoxLayout()
        grammar_row.setSpacing(2)
        grammar_row.addWidget(self.cb_grammar)
        grammar_row.addWidget(self.chk_send_grammar)
        grammar_row.addWidget(self.lbl_grammar_hint)

        seed_row = QHBoxLayout()
        self.sp_seed = QSpinBox()
        self.sp_seed.setRange(1, 2147483647)
        self.sp_seed.setValue(271828)
        self.btn_random_seed = QPushButton("RANDOM")
        self.btn_random_seed.setProperty("class", "Ghost")
        self.btn_random_seed.setFixedWidth(90)
        self.btn_random_seed.clicked.connect(self._randomize_single_seed)
        seed_row.addWidget(self.sp_seed, 1)
        seed_row.addWidget(self.btn_random_seed)

        self.cb_audio_s = QCheckBox("Audio ON")
        self.cb_audio_s.setChecked(True)
        self.cb_footer_s = QCheckBox("Footer ON")
        self.cb_footer_s.setChecked(True)

        f1.addRow("Family", self.cb_family)
        f1.addRow("Grammar / Subfamily", grammar_row)
        f1.addRow("Seed", seed_row)
        f1.addRow("", self.cb_audio_s)
        f1.addRow("", self.cb_footer_s)
        root.addWidget(gb1)

        b1 = QHBoxLayout()
        self.btn_single = QPushButton("PRODUCE FINAL")
        self.btn_single.setProperty("class", "Primary")
        b1.addWidget(self.btn_single)
        b1.addStretch(1)
        root.addLayout(b1)

        gb2 = QGroupBox("Production 5x5 (25 final products)")
        f2 = QFormLayout(gb2)
        self.sp_seeds5 = QSpinBox()
        self.sp_seeds5.setRange(1, 25)
        self.sp_seeds5.setValue(5)
        self.sp_seeds5.valueChanged.connect(self._reset_5x5_preview)

        self.cb_seedmode5 = QComboBox()
        self.cb_seedmode5.addItems(["RANDOM", "MANUAL"])
        self.cb_audio5 = QCheckBox("Audio ON")
        self.cb_audio5.setChecked(True)
        self.cb_footer5 = QCheckBox("Footer ON")
        self.cb_footer5.setChecked(True)

        self.lbl_preview = QLabel("(seeds will be generated at run time)")
        self.lbl_preview.setStyleSheet(
            "color:#8b96a8; font-family:Consolas; font-size:9pt;")
        self.lbl_preview.setWordWrap(True)

        self.btn_gen_seeds = QPushButton("GENERATE SEEDS NOW")
        self.btn_gen_seeds.setProperty("class", "Ghost")
        self.btn_gen_seeds.clicked.connect(self._pregen_5x5_seeds)

        preview_row = QHBoxLayout()
        preview_row.addWidget(self.lbl_preview, 1)
        preview_row.addWidget(self.btn_gen_seeds)

        f2.addRow("Unique seeds", self.sp_seeds5)
        f2.addRow("Seed mode", self.cb_seedmode5)
        f2.addRow("", self.cb_audio5)
        f2.addRow("", self.cb_footer5)
        f2.addRow("Preview", preview_row)
        root.addWidget(gb2)

        b2 = QHBoxLayout()
        self.btn_5x5 = QPushButton("PRODUCE 25 FINAL PRODUCTS")
        self.btn_5x5.setProperty("class", "Primary")
        b2.addWidget(self.btn_5x5)
        b2.addStretch(1)
        root.addLayout(b2)

        self.info = QLabel("Idle.")
        self.info.setStyleSheet("color:#8b96a8; font-family:Consolas;")
        root.addWidget(self.info)
        root.addStretch(1)

        self.btn_single.clicked.connect(self._emit_single)
        self.btn_5x5.clicked.connect(self._emit_5x5)

        self._refresh_grammars()

    def _on_send_grammar_toggled(self, checked):
        has_grammars = self.cb_grammar.count() > 1
        self.cb_grammar.setEnabled(checked and has_grammars)
        self._update_run_state()

    def _refresh_grammars(self):
        folder = self.cb_family.currentData()
        f = self.family_by_folder.get(folder)
        self.cb_grammar.blockSignals(True)
        self.cb_grammar.clear()
        self.cb_grammar.addItem("AUTO / RANDOM (seed-derived)", None)
        if f and f.grammars:
            for g in f.grammars:
                self.cb_grammar.addItem(g, g)
        self.cb_grammar.blockSignals(False)

        if f and f.grammars:
            self.lbl_grammar_hint.setText(
                str(len(f.grammars)) + " declared grammars for "
                + f.artistic + ". Backend v2.1.4 does NOT accept "
                "-Grammar (seed-derived). Enable the checkbox above only "
                "if your .ps1 supports it.")
        else:
            self.lbl_grammar_hint.setText(
                "No grammars declared for this family. The backend derives "
                "the grammar from the seed.")

        self.cb_grammar.setEnabled(
            self.chk_send_grammar.isChecked() and self.cb_grammar.count() > 1)
        self._update_run_state()

    def _update_run_state(self):
        pass

    def _randomize_single_seed(self):
        self.sp_seed.setValue(random.randint(1, 2147483647))

    def _reset_5x5_preview(self):
        self._pending_5x5_seeds = None
        self.lbl_preview.setText("(seeds will be generated at run time)")

    def _pregen_5x5_seeds(self):
        n = self.sp_seeds5.value()
        seeds = _unique_random_seeds(n)
        self._pending_5x5_seeds = seeds
        self.lbl_preview.setText(", ".join(str(s) for s in seeds))

    def _grammar_payload(self):
        if not self.chk_send_grammar.isChecked():
            return (None, False)
        g = self.cb_grammar.currentData()
        return (g, bool(g))

    def _emit_single(self):
        g, allow = self._grammar_payload()
        self.request_single.emit({
            "family": self.cb_family.currentData(),
            "grammar": g,
            "allow_grammar": allow,
            "seed": self.sp_seed.value(),
            "audio": self.cb_audio_s.isChecked(),
            "footer": self.cb_footer_s.isChecked(),
        })

    def _emit_5x5(self):
        resp = QMessageBox.question(
            self, "Confirm production 5x5",
            "Produce up to 25 canonical final products.\n\n"
            "Existing products will NOT be overwritten (safe default).\n\n"
            "Proceed?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resp != QMessageBox.Yes:
            return

        if self._pending_5x5_seeds:
            seeds_payload = list(self._pending_5x5_seeds)
        else:
            seeds_payload = None

        g, allow = self._grammar_payload()

        self.request_5x5.emit({
            "seed_count": self.sp_seeds5.value(),
            "seed_mode": self.cb_seedmode5.currentText(),
            "families": [f.folder for f in self.families],
            "audio": self.cb_audio5.isChecked(),
            "footer": self.cb_footer5.isChecked(),
            "pre_generated_seeds": seeds_payload,
            "grammar": g,
            "allow_grammar": allow,
        })

    def set_running(self, running):
        self.btn_single.setEnabled(not running)
        self.btn_5x5.setEnabled(not running)
        self.btn_random_seed.setEnabled(not running)
        self.btn_gen_seeds.setEnabled(not running)
        self.info.setText("RUNNING..." if running else "Idle.")
