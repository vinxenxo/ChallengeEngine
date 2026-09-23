from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QSpinBox, QComboBox, QGroupBox,
                               QFormLayout, QCheckBox, QSplitter, QTextBrowser)
from PySide6.QtCore import Signal, Qt


class ReviewPage(QWidget):
    request_run = Signal(dict)

    def __init__(self, families, parent=None):
        super().__init__(parent)
        self.families = families
        self.family_by_folder = {f.folder: f for f in families}

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(12)

        t = QLabel("Review Lab")
        t.setObjectName("PageTitle")
        s = QLabel("Experimental corpus - regenerable. Never affects Production. "
                   "Select one or more families to review.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t)
        root.addWidget(s)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        left = QWidget()
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 8, 0)
        lv.setSpacing(6)
        lv.addWidget(self._section_label("FAMILIES"))

        self.family_checks = {}
        for f in families:
            cb = QCheckBox(f.artistic + "  (" + f.technical + ")")
            cb.setChecked(True)
            cb.toggled.connect(self._update_run_state)
            cb.clicked.connect(
                lambda _=False, fol=f.folder: self._show_details(fol))
            self.family_checks[f.folder] = cb
            lv.addWidget(cb)

        row = QHBoxLayout()
        btn_all = QPushButton("SELECT ALL")
        btn_all.setProperty("class", "Ghost")
        btn_none = QPushButton("SELECT NONE")
        btn_none.setProperty("class", "Ghost")
        btn_all.clicked.connect(lambda: self._set_all(True))
        btn_none.clicked.connect(lambda: self._set_all(False))
        row.addWidget(btn_all)
        row.addWidget(btn_none)
        row.addStretch(1)
        lv.addLayout(row)
        lv.addStretch(1)

        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(8, 0, 0, 0)
        rv.setSpacing(6)
        rv.addWidget(self._section_label("FAMILY DETAILS"))

        self.details = QTextBrowser()
        self.details.setOpenExternalLinks(False)
        self.details.setStyleSheet(
            "QTextBrowser { background:#0a0d12; color:#c9d3e2; "
            "border:1px solid #232a36; border-radius:6px; padding:10px; "
            "font-family:Consolas; font-size:9pt; }")
        self.details.setText(
            "Click a family to inspect its grammars, palettes, "
            "parameters and audio profile.")
        rv.addWidget(self.details, 1)

        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([320, 720])
        root.addWidget(splitter, 1)

        gb = QGroupBox("Review batch")
        form = QFormLayout(gb)
        self.sp_seeds = QSpinBox()
        self.sp_seeds.setRange(1, 25)
        self.sp_seeds.setValue(5)
        self.sp_seeds.valueChanged.connect(self._update_run_state)
        self.cb_seedmode = QComboBox()
        self.cb_seedmode.addItems(["RANDOM", "MANUAL"])
        self.cb_audio = QCheckBox("Audio ON")
        self.cb_audio.setChecked(True)
        form.addRow("Unique seeds per family", self.sp_seeds)
        form.addRow("Seed mode", self.cb_seedmode)
        form.addRow("", self.cb_audio)
        root.addWidget(gb)

        row2 = QHBoxLayout()
        self.btn_run = QPushButton("RUN REVIEW")
        self.btn_run.setProperty("class", "Primary")
        self.btn_cancel = QPushButton("CANCEL")
        self.btn_cancel.setProperty("class", "Ghost")
        self.btn_cancel.setEnabled(False)
        self.summary = QLabel("")
        self.summary.setStyleSheet("color:#8b96a8; font-family:Consolas;")
        row2.addWidget(self.btn_run)
        row2.addWidget(self.btn_cancel)
        row2.addWidget(self.summary, 1)
        root.addLayout(row2)

        self.info = QLabel("Awaiting run.")
        self.info.setStyleSheet("color:#8b96a8; font-family:Consolas;")
        root.addWidget(self.info)

        self.btn_run.clicked.connect(self._emit_run)
        self.btn_cancel.clicked.connect(
            lambda: self.request_run.emit({"cancel": True}))

        self._update_run_state()
        if families:
            self._show_details(families[0].folder)

    def _section_label(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            "color:#8b96a8; font-weight:600; letter-spacing:1px; padding:2px 0;")
        return lbl

    def _set_all(self, value):
        for cb in self.family_checks.values():
            cb.setChecked(value)

    def preselect_families(self, folders):
        folders = set(folders)
        for fol, cb in self.family_checks.items():
            cb.blockSignals(True)
            cb.setChecked(fol in folders)
            cb.blockSignals(False)
        self._update_run_state()
        if folders:
            first = next(iter(folders))
            self._show_details(first)

    def _selected_folders(self):
        return [fol for fol, cb in self.family_checks.items() if cb.isChecked()]

    def _update_run_state(self):
        n = len(self._selected_folders())
        seeds = self.sp_seeds.value()
        total = n * seeds
        self.summary.setText(
            str(n) + " famil(ies) x " + str(seeds) + " seeds = "
            + str(total) + " renders")
        self.btn_run.setEnabled(n > 0)

    def _show_details(self, folder):
        f = self.family_by_folder.get(folder)
        if not f:
            return
        html = []
        html.append("<div style='font-size:13pt; color:#e6edf3;'><b>"
                    + f.artistic + "</b></div>")
        html.append("<div style='color:#7ad7ff;'>" + f.technical
                    + "  |  " + f.id + "</div>")
        html.append("<br>")
        if f.short_description:
            html.append("<div>" + f.short_description + "</div>")
        if f.visual_metaphor:
            html.append("<div style='color:#8b96a8;'><i>"
                        + f.visual_metaphor + "</i></div>")
        html.append("<br>")
        html.append("<div style='color:#8b96a8;'><b>GRAMMARS ("
                    + str(len(f.grammars)) + ")</b></div>")
        if f.grammars:
            for g in f.grammars:
                html.append("<div>  - " + g + "</div>")
        else:
            html.append("<div>  (none declared)</div>")
        html.append("<br>")
        html.append("<div style='color:#8b96a8;'><b>PALETTE BANK</b></div>")
        html.append("<div>  " + (", ".join(f.palette_bank)
                                 if f.palette_bank else "-") + "</div>")
        html.append("<br>")
        html.append("<div style='color:#8b96a8;'><b>PARAMETERS ("
                    + str(len(f.parameters)) + ")</b></div>")
        if f.parameters:
            html.append("<pre style='font-family:Consolas; font-size:9pt;'>")
            for p in f.parameters:
                html.append(p.id.ljust(24) + "  " + p.type.ljust(8)
                            + "  [" + p.state + "]")
            html.append("</pre>")
        else:
            html.append("<div>  (none declared)</div>")
        html.append("<br>")
        html.append("<div style='color:#8b96a8;'><b>AUDIO PROFILE</b></div>")
        html.append("<div>  " + f.audio_profile + "</div>")
        html.append("<div style='color:#8b96a8;'><b>DEFAULT DURATION</b></div>")
        html.append("<div>  " + str(f.default_duration) + " s</div>")
        self.details.setHtml("".join(html))

    def _emit_run(self):
        folders = self._selected_folders()
        if not folders:
            return
        self.request_run.emit({
            "seed_count": self.sp_seeds.value(),
            "seed_mode": self.cb_seedmode.currentText(),
            "audio": self.cb_audio.isChecked(),
            "families": folders,
        })

    def set_running(self, running):
        enabled = (not running) and len(self._selected_folders()) > 0
        self.btn_run.setEnabled(enabled)
        self.btn_cancel.setEnabled(running)
        self.info.setText("RUNNING..." if running else "Idle.")
