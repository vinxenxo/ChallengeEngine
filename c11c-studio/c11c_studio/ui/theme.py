from PySide6.QtGui import QFont

def apply_dark_theme(app):
    app.setStyleSheet("""
    QWidget { background:#0b0d12; color:#e8eef7; font-family:Segoe UI; font-size:10pt; }
    QMainWindow { background:#0b0d12; }
    #TopBar { background:#10141d; border-bottom:1px solid #263247; }
    #TopBarTitle { font-size:16pt; font-weight:700; color:#f4f8ff; }
    #TopBarMeta { color:#72d7ff; padding-left:16px; }
    #NavRail { background:#0a0d13; border-right:1px solid #1d2838; }
    QPushButton { background:#151b25; border:1px solid #29364c; border-radius:7px; padding:7px 12px; }
    QPushButton:hover { background:#1b2533; border-color:#3c506c; }
    QPushButton[class="Primary"] { background:#123247; border-color:#1f789e; color:#dff7ff; font-weight:700; }
    QLineEdit,QPlainTextEdit,QSpinBox,QComboBox,QTableWidget,QTextBrowser,QTabWidget::pane { background:#0f141d; border:1px solid #28344a; border-radius:6px; }
    QHeaderView::section { background:#141b27; border:0; padding:7px; color:#9fb2ca; }
    QTableWidget { gridline-color:#1d2635; alternate-background-color:#0c1119; }
    QCheckBox { spacing:7px; }
    QGroupBox { border:1px solid #263247; border-radius:8px; margin-top:9px; padding-top:12px; }
    QGroupBox::title { subcontrol-origin:margin; left:10px; padding:0 5px; color:#8fdfff; }
    #PageTitle { font-size:19pt; font-weight:700; }
    #PageSubtitle { color:#8a9ab0; }
    """)
