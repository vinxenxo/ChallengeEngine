from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QPushButton, QScrollArea, QGridLayout)
from PySide6.QtCore import Signal


class FamilyCard(QFrame):
    review_requested = Signal(str)
    open_folder_requested = Signal(str)

    def __init__(self, family, parent=None):
        super().__init__(parent)
        self.family = family
        self.setObjectName("Card")

        v = QVBoxLayout(self)
        v.setContentsMargins(14, 12, 14, 12)
        v.setSpacing(6)

        name = QLabel(family.artistic.upper())
        name.setStyleSheet("font-size:13pt; font-weight:600;")
        tech = QLabel(family.technical)
        tech.setStyleSheet("color:#7ad7ff; font-family:Consolas;")
        v.addWidget(name)
        v.addWidget(tech)

        desc = QLabel(family.short_description or family.visual_metaphor or "")
        desc.setWordWrap(True)
        desc.setStyleSheet("color:#b7c1d3;")
        v.addWidget(desc)

        g = ", ".join(family.grammars) if family.grammars else "-"
        p = ", ".join(family.palette_bank) if family.palette_bank else "-"
        meta = QLabel("GRAMMAR: " + g + "\nPALETTE: " + p
                      + "\nPARAMS : " + str(len(family.parameters)))
        meta.setStyleSheet("color:#8b96a8; font-family:Consolas;")
        v.addWidget(meta)

        row = QHBoxLayout()
        btn_r = QPushButton("REVIEW")
        btn_r.setProperty("class", "Primary")
        btn_o = QPushButton("OPEN FOLDER")
        btn_o.setProperty("class", "Ghost")
        row.addWidget(btn_r)
        row.addWidget(btn_o)
        row.addStretch(1)
        v.addLayout(row)

        btn_r.clicked.connect(
            lambda: self.review_requested.emit(self.family.folder))
        btn_o.clicked.connect(
            lambda: self.open_folder_requested.emit(self.family.folder))


class FamiliesPage(QWidget):
    request_review = Signal(str)
    request_open_folder = Signal(str)

    def __init__(self, families, parent=None):
        super().__init__(parent)
        self.families = families

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        t = QLabel("Families")
        t.setObjectName("PageTitle")
        s = QLabel("Discovered from tools/prototypes - dynamic, metadata-driven. "
                   "Click REVIEW to inspect a family, or OPEN FOLDER to browse it.")
        s.setObjectName("PageSubtitle")
        root.addWidget(t)
        root.addWidget(s)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        holder = QWidget()
        grid = QGridLayout(holder)
        grid.setSpacing(14)
        for i, fam in enumerate(families):
            card = FamilyCard(fam)
            card.review_requested.connect(self.request_review)
            card.open_folder_requested.connect(self.request_open_folder)
            grid.addWidget(card, i // 2, i % 2)
        scroll.setWidget(holder)
        root.addWidget(scroll, 1)
