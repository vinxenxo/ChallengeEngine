from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QHeaderView)
from PySide6.QtCore import Qt

from ..widgets.status_card import StatusCard


class DashboardPage(QWidget):
    def __init__(self, ctx, tools, parent=None):
        super().__init__(parent)
        self.ctx = ctx
        self.tools = tools

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(18)

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")
        sub = QLabel("C11-C Visual Loops - operational overview")
        sub.setObjectName("PageSubtitle")
        root.addWidget(title)
        root.addWidget(sub)

        cards = QHBoxLayout()
        cards.setSpacing(14)
        g = self.tools.get("godot")
        self.card_backend = StatusCard("Backend", self.ctx.backend_version, "READY")
        self.card_godot = StatusCard(
            "Godot",
            (g.version or "missing") if g else "missing",
            "READY" if g and g.present else "MISSING")
        self.card_delivery = StatusCard(
            "Delivery",
            "%dx%d / %d FPS / %ds" % (self.ctx.delivery_width,
                self.ctx.delivery_height, self.ctx.fps,
                int(self.ctx.default_duration)),
            "CANONICAL")
        self.card_families = StatusCard("Families", "5", "")
        self.card_prod = StatusCard("Production", "-", "")
        self.card_review = StatusCard("Review corpus", "-", "")

        for c in (self.card_backend, self.card_godot, self.card_delivery,
                  self.card_families, self.card_prod, self.card_review):
            cards.addWidget(c)
        root.addLayout(cards)

        actions = QHBoxLayout()
        self.btn_validate = QPushButton("VALIDATE ENVIRONMENT")
        self.btn_review = QPushButton("NEW 5x5 REVIEW")
        self.btn_produce = QPushButton("PRODUCE 5x5 FINAL")
        self.btn_single = QPushButton("PRODUCE SINGLE")
        self.btn_open_prod = QPushButton("OPEN PRODUCTION")
        self.btn_open_review = QPushButton("OPEN REVIEW")
        for b in (self.btn_validate, self.btn_review, self.btn_produce,
                  self.btn_single, self.btn_open_prod, self.btn_open_review):
            actions.addWidget(b)
        actions.addStretch(1)
        root.addLayout(actions)

        recent = QLabel("Recent activity")
        recent.setStyleSheet("color:#8b96a8; font-weight:600; margin-top:8px;")
        root.addWidget(recent)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Date/Time", "Type", "Family", "Seed", "State", "Duration"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        root.addWidget(self.table, 1)

    def set_counts(self, production, review, families):
        self.card_prod.set(str(production))
        self.card_review.set(str(review))
        self.card_families.set(str(families))

    def add_job_row(self, when, jtype, family, seed, state, duration):
        r = self.table.rowCount()
        self.table.insertRow(r)
        for c, txt in enumerate([when, jtype, family, seed, state, duration]):
            it = QTableWidgetItem(txt)
            it.setFlags(it.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(r, c, it)
