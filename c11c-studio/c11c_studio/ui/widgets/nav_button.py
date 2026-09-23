from PySide6.QtWidgets import QPushButton


class NavButton(QPushButton):
    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        self.setObjectName("NavButton")
        self.setCheckable(True)
