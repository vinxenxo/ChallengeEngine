from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QSpinBox, QComboBox, QLineEdit, QSplitter, QTextBrowser, QMessageBox, QGroupBox, QFormLayout
from ...domain.seed import MIN_SEED, MAX_SEED


class ReviewPage(QWidget):
    request_run = Signal(dict)
    request_cancel = Signal()

    def __init__(self, families, parent=None):
        super().__init__(parent)
        self.families = families
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        title = QLabel("Review Lab")
        title.setObjectName("PageTitle")
        root.addWidget(title)
        root.addWidget(QLabel("Experimental / regenerable. It never cleans Production."))

        splitter = QSplitter(Qt.Horizontal)
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(QLabel("FAMILIES"))
        self.checks = {}
        for family in families:
            check = QCheckBox(family.artistic + "  [" + family.technical + "]")
            check.setChecked(True)
            check.clicked.connect(lambda _=False, x=family.folder: self._show(x))
            self.checks[family.folder] = check
            left_layout.addWidget(check)
        splitter.addWidget(left)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        self.details = QTextBrowser()
        right_layout.addWidget(self.details)
        splitter.addWidget(right)
        splitter.setStretchFactor(1, 2)
        root.addWidget(splitter, 1)

        box = QGroupBox("Review configuration")
        form = QFormLayout(box)
        self.count = QSpinBox()
        self.count.setRange(1, 100)
        self.count.setValue(5)
        self.mode = QComboBox()
        self.mode.addItems(["RANDOM", "MANUAL"])
        self.seeds = QLineEdit()
        self.seeds.setPlaceholderText("Unique seeds, comma-separated")
        self.audio = QCheckBox("Audio ON")
        self.audio.setChecked(True)
        self.footer = QCheckBox("Footer ON")
        self.footer.setChecked(True)
        self.reset = QCheckBox("Reset review assets")
        self.run = QPushButton("RUN REVIEW")
        self.run.setProperty("class", "Primary")
        self.cancel = QPushButton("CANCEL")

        form.addRow("Seed count", self.count)
        form.addRow("Mode", self.mode)
        form.addRow("Manual", self.seeds)
        form.addRow("", self.audio)
        form.addRow("", self.footer)
        form.addRow("", self.reset)
        row = QHBoxLayout()
        row.addWidget(self.run)
        row.addWidget(self.cancel)
        form.addRow(row)
        root.addWidget(box)
        self.info = QLabel("Idle")
        root.addWidget(self.info)

        self.mode.currentTextChanged.connect(lambda mode: self.seeds.setEnabled(mode == "MANUAL"))
        self.seeds.setEnabled(False)
        self.run.clicked.connect(self._emit)
        self.cancel.clicked.connect(self.request_cancel.emit)
        self._show(families[0].folder if families else None)

    def _selected(self):
        return [key for key, check in self.checks.items() if check.isChecked()]

    def _show(self, folder):
        family = next((item for item in self.families if item.folder == folder), None)
        if family:
            self.details.setPlainText(
                "\n".join([
                    family.artistic,
                    family.id,
                    "",
                    family.short_description,
                    "",
                    "GRAMMARS:",
                    *(family.grammars or ["(backend/seed derived)"]),
                    "",
                    "PARAMETERS:",
                    *(p.id + "  [" + p.state + "]" for p in family.parameters),
                ])
            )

    def _parse_manual(self):
        raw = self.seeds.text().replace("\n", ",")
        values = [int(item.strip()) for item in raw.split(",") if item.strip()]
        if len(values) != self.count.value():
            raise ValueError(f"Expected exactly {self.count.value()} seeds.")
        if len(values) != len(set(values)):
            raise ValueError("Manual seeds must be unique.")
        if any(value < MIN_SEED or value > MAX_SEED for value in values):
            raise ValueError(f"Seed range is {MIN_SEED}..{MAX_SEED}.")
        return values

    def _emit(self):
        families = self._selected()
        if not families:
            QMessageBox.warning(self, "Review", "Select at least one family.")
            return
        seeds = None
        if self.mode.currentText() == "MANUAL":
            try:
                seeds = self._parse_manual()
            except ValueError as exc:
                QMessageBox.warning(self, "Review", str(exc))
                return
        self.request_run.emit({
            "families": families,
            "count": self.count.value(),
            "seeds": seeds,
            "audio": self.audio.isChecked(),
            "footer": self.footer.isChecked(),
            "reset": self.reset.isChecked(),
        })

    def set_running(self, running):
        self.run.setEnabled(not running)
        self.cancel.setEnabled(running)
        self.info.setText("RUNNING..." if running else "Idle")
