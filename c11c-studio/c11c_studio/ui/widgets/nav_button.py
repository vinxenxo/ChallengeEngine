from PySide6.QtWidgets import QPushButton

class NavButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("NavButton")
        self.setCheckable(True)
        self.setMinimumHeight(40)
