from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QHBoxLayout)
from PySide6.QtGui import QColor


class ValidationPage(QWidget):
    def __init__(self, ctx, parent=None):
        super().__init__(parent)
        self.ctx = ctx

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(12)

        t = QLabel("Validation Center"); t.setObjectName("PageTitle")
        s = QLabel("Preflight checks. PASS / WARN / FAIL.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t); root.addWidget(s)

        row = QHBoxLayout()
        self.btn_run = QPushButton("RUN ALL")
        row.addWidget(self.btn_run); row.addStretch(1)
        root.addLayout(row)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Check", "Status", "Message"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        root.addWidget(self.table, 1)

        self.btn_run.clicked.connect(self.run)

    def run(self):
        from ...services.environment_validator import EnvironmentValidator
        report = EnvironmentValidator(self.ctx).run_all()
        self.table.setRowCount(0)
        for c in report.checks:
            r = self.table.rowCount(); self.table.insertRow(r)
            for col, txt in enumerate([c.name, c.status, c.message]):
                it = QTableWidgetItem(txt)
                if col == 1:
                    if c.status == "PASS":
                        it.setForeground(QColor("#6ee7a7"))
                    elif c.status == "WARN":
                        it.setForeground(QColor("#f5c451"))
                    else:
                        it.setForeground(QColor("#ff8080"))
                self.table.setItem(r, col, it)
