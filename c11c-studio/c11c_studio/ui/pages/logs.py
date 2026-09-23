from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QComboBox, QLineEdit)
from ..widgets.log_view import LogView


class LogsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(10)

        t = QLabel("Logs"); t.setObjectName("PageTitle")
        s = QLabel("Raw stdout/stderr is preserved verbatim. No line is dropped.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t); root.addWidget(s)

        row = QHBoxLayout()
        self.cb_filter = QComboBox(); self.cb_filter.addItems(
            ["ALL", "INFO", "WARN", "ERROR"])
        self.le_search = QLineEdit()
        self.le_search.setPlaceholderText("Search...")
        self.btn_clear = QPushButton("CLEAR")
        self.btn_open = QPushButton("OPEN RAW LOG")
        row.addWidget(QLabel("Filter:")); row.addWidget(self.cb_filter)
        row.addWidget(self.le_search)
        row.addWidget(self.btn_clear); row.addWidget(self.btn_open)
        row.addStretch(1)
        root.addLayout(row)

        self.view = LogView()
        root.addWidget(self.view, 1)

        self.btn_clear.clicked.connect(self.view.clear_log)
