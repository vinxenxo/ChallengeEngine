from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QGroupBox,
                               QLabel, QLineEdit, QPushButton, QHBoxLayout,
                               QFileDialog)
from PySide6.QtCore import Signal


class SettingsPage(QWidget):
    project_changed = Signal(str)

    def __init__(self, ctx, cfg, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        self.cfg = cfg

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        t = QLabel("Settings"); t.setObjectName("PageTitle")
        root.addWidget(t)

        gb = QGroupBox("General")
        f = QFormLayout(gb)
        self.le_project = QLineEdit(str(self.ctx.project_root))
        self.le_project.setReadOnly(True)
        btn_pick = QPushButton("..."); btn_pick.setFixedWidth(32)
        row = QHBoxLayout()
        row.addWidget(self.le_project); row.addWidget(btn_pick)
        f.addRow("Project root", row)

        gb_del = QGroupBox("Delivery (read-only in v0.1)")
        fd = QFormLayout(gb_del)
        fd.addRow(QLabel("%dx%d @ %d FPS - %.2fs (%d frames)" % (
            self.ctx.delivery_width, self.ctx.delivery_height, self.ctx.fps,
            self.ctx.default_duration, self.ctx.default_frames)))
        fd.addRow(QLabel("Logical: %dx%d (Header 0-144 / Body 144-816 / "
                         "Footer 816-960)" % (
            self.ctx.logical_width, self.ctx.logical_height)))

        gb_ver = QGroupBox("Versions")
        fv = QFormLayout(gb_ver)
        fv.addRow("Backend", QLabel(self.ctx.backend_version))
        fv.addRow("C11-B", QLabel(self.ctx.c11b_state))

        root.addWidget(gb); root.addWidget(gb_del); root.addWidget(gb_ver)
        root.addStretch(1)
        btn_pick.clicked.connect(self._pick)

    def _pick(self):
        p = QFileDialog.getExistingDirectory(
            self, "Select project root", str(self.ctx.project_root))
        if p:
            self.le_project.setText(p)
            self.cfg.set("project_root", p)
            self.cfg.save()
            self.project_changed.emit(p)
