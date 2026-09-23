from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AboutPage(QWidget):
    def __init__(self, ctx, app_version, parent=None):
        super().__init__(parent)
        v = QVBoxLayout(self)
        v.setContentsMargins(24, 20, 24, 20)
        v.setSpacing(8)

        v.addWidget(QLabel("<h2>C11-C Studio</h2>"))
        v.addWidget(QLabel("GUI version: " + app_version))
        v.addWidget(QLabel("Backend reference: " + ctx.backend_version))
        v.addWidget(QLabel("C11-B: " + ctx.c11b_state))
        v.addWidget(QLabel("Architecture: GUI -> canonical toolchain -> "
                           "Godot/Python/FFmpeg/FFprobe -> artifacts"))
        v.addWidget(QLabel("Rule: the GUI can control the system; "
                           "the GUI must not become the system."))
        v.addStretch(1)
