from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QFont

class LogView(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        font = QFont("Consolas", 9)
        self.setFont(font)
        self.setPlaceholderText("Job output will appear here…")

    def append_line(self, text, stream="stdout"):
        prefix = "[STDERR] " if stream == "stderr" else ""
        self.appendPlainText(prefix + text.rstrip("\n"))
        self.ensureCursorVisible()
