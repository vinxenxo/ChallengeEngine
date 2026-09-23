from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget,
                               QTableWidgetItem, QHeaderView, QPushButton,
                               QHBoxLayout, QMessageBox)
from PySide6.QtCore import Qt


def _human(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return "%.1f %s" % (n, unit)
        n /= 1024
    return "%.1f PB" % n


class ArtifactsPage(QWidget):
    def __init__(self, registry, parent=None):
        super().__init__(parent)
        self.registry = registry

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        t = QLabel("Artifacts"); t.setObjectName("PageTitle")
        s = QLabel("Classification & dry-run cleanup. Production, QA, "
                   "Regression, Releases, Legacy, Tests are protected.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t); root.addWidget(s)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Root", "Protection", "Files", "Size", "Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        root.addWidget(self.table, 1)

        row = QHBoxLayout()
        self.btn_refresh = QPushButton("REFRESH")
        self.btn_dry = QPushButton("PREVIEW CLEANUP (scratch only)")
        row.addWidget(self.btn_refresh); row.addWidget(self.btn_dry)
        row.addStretch(1)
        root.addLayout(row)

        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_dry.clicked.connect(self._dry_run)
        self.refresh()

    def refresh(self):
        self.table.setRowCount(0)
        for root in self.registry.roots():
            r = self.table.rowCount(); self.table.insertRow(r)
            lock = "[LOCK] " if self.registry.is_protected(root.key) else ""
            vals = [root.label, lock + root.protection, str(root.file_count),
                    _human(root.size_bytes), str(root.path)]
            for c, txt in enumerate(vals):
                it = QTableWidgetItem(txt)
                it.setFlags(it.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(r, c, it)

    def _dry_run(self):
        scratch = None
        for r in self.registry.roots():
            if r.key == "scratch":
                scratch = r
                break
        if not scratch or not scratch.exists:
            QMessageBox.information(self, "Dry-run",
                                    "Scratch root does not exist.")
            return
        QMessageBox.information(
            self, "Dry-run: SCRATCH only",
            "Target: " + str(scratch.path) + "\n"
            "Files: " + str(scratch.file_count) + "\n"
            "Size: " + _human(scratch.size_bytes) + "\n\n"
            "No deletion will occur automatically. Production and evidence "
            "roots are never touched.")
