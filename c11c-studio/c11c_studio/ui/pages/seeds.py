from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QSpinBox, QComboBox, QTableWidget,
                               QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt


class SeedsPage(QWidget):
    def __init__(self, seed_manager, parent=None):
        super().__init__(parent)
        self.sm = seed_manager

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        t = QLabel("Seeds"); t.setObjectName("PageTitle")
        s = QLabel("Seed is a reproduction identifier - same 5 seeds "
                   "cross all 5 families for 5x5.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t); root.addWidget(s)

        row = QHBoxLayout()
        self.sp_count = QSpinBox(); self.sp_count.setRange(1, 100)
        self.sp_count.setValue(5)
        self.cb_mode = QComboBox(); self.cb_mode.addItems(["RANDOM", "MANUAL"])
        self.btn_generate = QPushButton("GENERATE")
        self.btn_save = QPushButton("SAVE BATCH")
        row.addWidget(QLabel("Count:")); row.addWidget(self.sp_count)
        row.addWidget(QLabel("Mode:")); row.addWidget(self.cb_mode)
        row.addWidget(self.btn_generate); row.addWidget(self.btn_save)
        row.addStretch(1)
        root.addLayout(row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Seed", "Source", "Batch", "Created"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        root.addWidget(self.table, 1)

        self.btn_generate.clicked.connect(self._generate)
        self.btn_save.clicked.connect(self._save)

    def _generate(self):
        n = self.sp_count.value()
        if self.cb_mode.currentText() == "RANDOM":
            self.sm.random_batch(n)
        else:
            self.sm.manual_batch(list(range(1000, 1000 + n)))
        self._refresh()

    def _save(self):
        if self.sm.records:
            p = self.sm.save_batch(self.sm.records[-5:])
            self.window().statusBar().showMessage("Saved " + p.name, 4000)

    def _refresh(self):
        self.table.setRowCount(0)
        for r in self.sm.records:
            i = self.table.rowCount(); self.table.insertRow(i)
            vals = [str(r.seed), r.source, r.batch_id or "-", r.created_at]
            for c, txt in enumerate(vals):
                it = QTableWidgetItem(txt)
                it.setFlags(it.flags() ^ Qt.ItemIsEditable)
                self.table.setItem(i, c, it)
