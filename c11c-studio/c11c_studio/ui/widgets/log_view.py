from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QTextCursor


class LogView(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LogView")
        self.setReadOnly(True)
        self.setMaximumBlockCount(20000)

    def append_text(self, text):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(text)
        self.moveCursor(QTextCursor.End)

    def clear_log(self):
        self.clear()
