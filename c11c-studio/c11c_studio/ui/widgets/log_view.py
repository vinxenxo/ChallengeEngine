from PySide6.QtWidgets import QPlainTextEdit

class LogView(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        font = self.font()
        font.setFamily("Consolas")
        self.setFont(font)

    def append_line(self, text, stream="stdout"):
        prefix = "[STDERR] " if stream == "stderr" else ""
        self.appendPlainText(prefix + text.rstrip("\n"))
        self.ensureCursorVisible()
