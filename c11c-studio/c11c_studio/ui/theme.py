from PySide6.QtGui import QFont

def apply_dark_theme(app):
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet("""
    QWidget { background:#090c11; color:#e7edf5; font-family:Segoe UI; font-size:10pt; }
    QMainWindow { background:#090c11; }
    #AppShell { background:#090c11; }

    #TopBar { background:#0e131b; border-bottom:1px solid #243043; }
    #TopBarTitle { font-size:17pt; font-weight:800; color:#f5f9ff; letter-spacing:0.2px; }
    #TopBarKicker { color:#61738b; font-size:8pt; font-weight:700; letter-spacing:1.2px; }
    #TopBarMeta { color:#9ee9ff; font-size:9pt; font-weight:700; }
    #TopBarSubMeta { color:#73869e; font-size:8.5pt; }
    #TopDivider { background:#253247; border:0; }
    #TopBarProjectLabel { color:#566981; font-size:7.5pt; font-weight:800; letter-spacing:1px; }
    #TopBarProject { color:#d7e3ef; font-size:9pt; font-weight:600; max-width:240px; }
    #EnvironmentPill { background:#102a21; color:#67e4af; border:1px solid #1f6c4d; border-radius:12px; padding:5px 10px; font-weight:800; font-size:8.5pt; }

    #NavRail { background:#080b10; border-right:1px solid #202b3a; }
    #NavSection { color:#53657d; font-size:7.5pt; font-weight:800; letter-spacing:1.3px; padding:4px 8px 3px 8px; }
    #NavHint { color:#405168; font-size:7.5pt; line-height:1.4; padding:12px 8px 4px 8px; border-top:1px solid #172131; }
    #PageStack { background:#0b0f15; }

    QLabel#PageTitle { color:#f2f6fb; font-size:21pt; font-weight:800; }
    QLabel#PageSubtitle { color:#73869c; font-size:10pt; }
    QLabel#Eyebrow { color:#56cce9; font-size:8pt; font-weight:800; letter-spacing:1.2px; }
    QLabel#Muted { color:#6f8299; }
    QLabel#Hint { color:#62758d; font-size:8.5pt; }
    QLabel#StatusPill { background:#102a21; color:#67e4af; border:1px solid #1f6c4d; border-radius:11px; padding:4px 10px; font-weight:800; }
    QLabel#StatusPill[state="running"] { background:#2b2510; color:#ffd36a; border-color:#816627; }
    QLabel#StatusDetail { color:#60738b; padding-left:8px; }

    QFrame#Hero { background:qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #101a24, stop:1 #0e141d); border:1px solid #25374b; border-radius:14px; }
    QFrame#Panel { background:#0f141c; border:1px solid #233044; border-radius:12px; }
    QFrame#InfoStrip { background:#101923; border:1px solid #26384e; border-radius:9px; }
    QLabel#PanelTitle { color:#e9f2fa; font-size:10.5pt; font-weight:800; }
    QLabel#PanelMeta { color:#71869f; font-size:8.5pt; }

    QPushButton { background:#151c26; color:#dce6f0; border:1px solid #2a384c; border-radius:8px; padding:8px 13px; min-height:18px; }
    QPushButton:hover { background:#1a2532; border-color:#3b516b; }
    QPushButton:pressed { background:#111a24; }
    QPushButton:disabled { background:#10151c; color:#46566b; border-color:#1c2736; }
    QPushButton[class="Primary"] { background:#123646; border-color:#1f7695; color:#dcf7ff; font-weight:800; }
    QPushButton[class="Primary"]:hover { background:#174354; border-color:#2b98bd; }
    QPushButton[class="Secondary"] { background:#111820; border-color:#314156; }
    QPushButton[class="Danger"] { background:#281317; border-color:#69333d; color:#ffb8c2; }

    QLineEdit,QPlainTextEdit,QSpinBox,QDoubleSpinBox,QComboBox,QTableWidget,QTextBrowser { background:#0c1219; color:#e7edf5; border:1px solid #28364a; border-radius:8px; selection-background-color:#173e51; selection-color:#f7fbff; padding:6px 8px; }
    QLineEdit:focus,QPlainTextEdit:focus,QSpinBox:focus,QDoubleSpinBox:focus,QComboBox:focus,QTableWidget:focus,QTextBrowser:focus { border-color:#3e7893; }
    QComboBox::drop-down { border:0; width:28px; }
    QComboBox QAbstractItemView { background:#0f151d; border:1px solid #2b3b50; selection-background-color:#173b4e; }

    QTableWidget { gridline-color:#182331; alternate-background-color:#0a1017; padding:0; }
    QTableWidget::item { padding:6px 8px; border-bottom:1px solid #151f2c; }
    QTableWidget::item:selected { background:#143243; color:#f3fbff; }
    QHeaderView::section { background:#111925; color:#8193a9; border:0; border-bottom:1px solid #27364a; padding:8px 9px; font-size:8pt; font-weight:800; }
    QTableCornerButton::section { background:#111925; border:0; }

    QGroupBox { background:#0f141c; border:1px solid #233044; border-radius:11px; margin-top:12px; padding:18px 14px 14px 14px; }
    QGroupBox::title { subcontrol-origin:margin; left:12px; padding:2px 7px; color:#a6dceb; background:#0f141c; font-size:9pt; font-weight:800; }
    QCheckBox { spacing:8px; color:#c8d5e2; padding:4px 0; }
    QCheckBox::indicator { width:15px; height:15px; }

    QTabWidget::pane { background:#0f141c; border:1px solid #233044; border-radius:9px; top:-1px; }
    QTabBar::tab { background:#0c1219; color:#71849b; padding:9px 14px; margin-right:2px; border:1px solid #202c3e; border-bottom:0; border-top-left-radius:7px; border-top-right-radius:7px; }
    QTabBar::tab:selected { background:#121c28; color:#a7e9fa; border-color:#2e5266; }

    QScrollBar:vertical { background:#0b1017; width:10px; margin:2px; }
    QScrollBar::handle:vertical { background:#28374a; min-height:28px; border-radius:5px; }
    QScrollBar::handle:vertical:hover { background:#3a4f67; }
    QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical { height:0; }
    QScrollBar:horizontal { background:#0b1017; height:10px; margin:2px; }
    QScrollBar::handle:horizontal { background:#28374a; min-width:28px; border-radius:5px; }
    QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal { width:0; }

    QSplitter::handle { background:#192536; }
    QStatusBar { background:#0a0f15; color:#62758b; border-top:1px solid #1e2a3a; }
    QToolTip { background:#111923; color:#eaf5ff; border:1px solid #2d4257; padding:6px 8px; }
    """)
