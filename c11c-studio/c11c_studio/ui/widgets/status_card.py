from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class StatusCard(QFrame):
    def __init__(self, title, value="-", state="", parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.setFrameShape(QFrame.NoFrame)

        v = QVBoxLayout(self)
        v.setContentsMargins(14, 12, 14, 12)
        v.setSpacing(4)

        self.title = QLabel(title.upper())
        self.title.setObjectName("CardTitle")
        self.value = QLabel(value)
        self.value.setObjectName("CardValue")
        self.state = QLabel(state)
        self.state.setObjectName("CardState")

        v.addWidget(self.title)
        v.addWidget(self.value)
        v.addWidget(self.state)

    def set(self, value, state=""):
        self.value.setText(value)
        self.state.setText(state)
