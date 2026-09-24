from PySide6.QtGui import QFont


def apply_light_theme(app):
    """Bright C11-C Studio theme optimized for readability and form controls."""
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(r"""
    QWidget {
        background: #f4f7fb;
        color: #172033;
        font-family: "Segoe UI";
        font-size: 10.5pt;
    }
    QMainWindow { background: #eef2f7; }
    #AppShell { background: #eef2f7; }

    #TopBar { background: #ffffff; border-bottom: 1px solid #d8e0ea; }
    #TopBarTitle { font-size: 17pt; font-weight: 800; color: #10213a; }
    #TopBarKicker { color: #617089; font-size: 8pt; font-weight: 700; letter-spacing: 1.1px; }
    #TopBarMeta { color: #087f9c; font-size: 9pt; font-weight: 800; }
    #TopBarSubMeta { color: #65758d; font-size: 8.5pt; }
    #TopDivider { background: #dbe3ed; border: 0; }
    #TopBarProjectLabel { color: #708198; font-size: 7.5pt; font-weight: 800; letter-spacing: 1px; }
    #TopBarProject { color: #203149; font-size: 9pt; font-weight: 600; max-width: 320px; }
    #EnvironmentPill { background: #e8f8ef; color: #137443; border: 1px solid #9fd9b8; border-radius: 12px; padding: 5px 10px; font-weight: 800; font-size: 8.5pt; }

    #NavRail { background: #ffffff; border-right: 1px solid #d8e0ea; }
    #NavSection { color: #718097; font-size: 7.5pt; font-weight: 800; letter-spacing: 1.3px; padding: 5px 10px 4px 10px; }
    #NavHint { color: #7b889b; font-size: 7.5pt; line-height: 1.4; padding: 12px 10px 4px 10px; border-top: 1px solid #e0e6ee; }
    #PageStack { background: #eef2f7; }

    QLabel#PageTitle { color: #12223a; font-size: 21pt; font-weight: 800; }
    QLabel#PageSubtitle { color: #66758c; font-size: 10pt; }
    QLabel#Eyebrow { color: #087f9c; font-size: 8pt; font-weight: 800; letter-spacing: 1.2px; }
    QLabel#Muted { color: #7c899c; }
    QLabel#Hint { color: #66758c; font-size: 8.5pt; }
    QLabel#StatusPill { background: #e8f8ef; color: #137443; border: 1px solid #9fd9b8; border-radius: 11px; padding: 4px 10px; font-weight: 800; }
    QLabel#StatusPill[state="running"] { background: #fff5da; color: #8a5f00; border-color: #e5c36a; }
    QLabel#StatusDetail { color: #687990; padding-left: 8px; }
    QLabel#CardLabel { color: #76859a; font-size: 7.5pt; font-weight: 800; letter-spacing: 1px; }
    QLabel#CardMeta { color: #8693a5; font-size: 8pt; }

    QFrame#Hero { background: #ffffff; border: 1px solid #d8e0ea; border-radius: 14px; }
    QFrame#Panel { background: #ffffff; border: 1px solid #d8e0ea; border-radius: 12px; }
    QFrame#InfoStrip { background: #f0f8fb; border: 1px solid #c9e5ee; border-radius: 9px; }
    QFrame#GenerateSummary { background: #ffffff; border: 1px solid #d8e0ea; border-radius: 10px; }
    QFrame#ModeBar { background: #e8edf4; border: 1px solid #d4dde8; border-radius: 10px; }
    QFrame#GeneratePanel { background: #ffffff; border: 1px solid #d8e0ea; border-radius: 12px; }
    QFrame#GenerationStatus { background: #ffffff; border: 1px solid #d8e0ea; border-radius: 9px; }
    QLabel#GenerateStatValue { color: #12223a; font-size: 15pt; font-weight: 800; }
    QLabel#GenerateSummaryText { color: #51627a; font-size: 8.5pt; font-weight: 700; }
    QLabel#PanelTitle { color: #192942; font-size: 10.5pt; font-weight: 800; }
    QLabel#PanelMeta { color: #6e7d92; font-size: 8.5pt; }

    QPushButton { background: #ffffff; color: #24334a; border: 1px solid #c7d1de; border-radius: 8px; padding: 8px 13px; min-height: 20px; }
    QPushButton:hover { background: #f5f8fb; border-color: #9eb0c5; }
    QPushButton:pressed { background: #edf2f7; }
    QPushButton:disabled { background: #edf1f5; color: #9aa6b5; border-color: #dce2ea; }
    QPushButton[class="Primary"] { background: #0b8aa8; border-color: #08758f; color: #ffffff; font-weight: 800; }
    QPushButton[class="Primary"]:hover { background: #087b97; border-color: #06677e; }
    QPushButton[class="Secondary"] { background: #f7f9fc; border-color: #bdcad9; }
    QPushButton[class="Danger"] { background: #fff0f1; border-color: #e7a9ae; color: #b4232d; }
    QPushButton[class="Mode"] { background: #f7f9fc; border-color: #c8d3e0; color: #61718a; font-weight: 800; min-height: 36px; padding: 7px 18px; }
    QPushButton[class="Mode"]:checked { background: #ffffff; border-color: #73b8ca; color: #087f9c; }
    QPushButton[class="Mode"]:hover { background: #ffffff; color: #087f9c; }

    QPushButton#NavButton { text-align: left; padding: 8px 12px 8px 15px; border: 1px solid transparent; border-radius: 7px; background: transparent; color: #53637b; }
    QPushButton#NavButton:hover { background: #f1f5f9; color: #203049; }
    QPushButton#NavButton:checked { background: #e8f6fa; color: #087f9c; border-color: #b9dfe8; font-weight: 700; }

    QLineEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTableWidget, QTextBrowser, QTextEdit {
        background: #ffffff; color: #172033; border: 1px solid #aebdcd; border-radius: 8px;
        selection-background-color: #ccecf3; selection-color: #12223a; padding: 8px 10px;
        min-height: 38px;
    }
    QLineEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QTableWidget:focus, QTextBrowser:focus, QTextEdit:focus { border: 2px solid #65b5c8; padding: 6px 8px; background: #ffffff; }
    QLineEdit:disabled, QPlainTextEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled { background: #f0f3f7; color: #98a4b4; }

    QComboBox { min-height: 40px; padding: 7px 38px 7px 11px; }
    QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 38px; border-left: 1px solid #c4cfdb; background: #f3f7fa; border-top-right-radius: 7px; border-bottom-right-radius: 7px; }
    QComboBox::drop-down:hover { background: #eef3f8; }
    QComboBox QAbstractItemView { background: #ffffff; color: #172033; border: 1px solid #9eafc2; selection-background-color: #dff2f6; selection-color: #10213a; padding: 5px; outline: 0; }
    QComboBox QAbstractItemView::item { min-height: 38px; padding: 8px 12px; }

    QSpinBox, QDoubleSpinBox { min-height: 40px; padding: 7px 30px 7px 10px; }
    QSpinBox::up-button, QDoubleSpinBox::up-button, QSpinBox::down-button, QDoubleSpinBox::down-button { width: 22px; background: #f6f8fb; border: 0; border-left: 1px solid #d6dee8; }
    QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover, QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover { background: #eaf0f6; }

    QCheckBox { spacing: 8px; color: #26364e; padding: 5px 0; }
    QCheckBox::indicator { width: 17px; height: 17px; border: 1px solid #aebbc9; border-radius: 4px; background: #ffffff; }
    QCheckBox::indicator:hover { border-color: #65aebe; }
    QCheckBox::indicator:checked { background: #0b8aa8; border-color: #08758f; }

    QTableWidget { gridline-color: #e3e8ef; alternate-background-color: #f8fafc; padding: 0; }
    QTableWidget::item { padding: 7px 9px; border-bottom: 1px solid #e6ebf1; }
    QTableWidget::item:selected { background: #dff2f6; color: #13243b; }
    QHeaderView::section { background: #eef2f6; color: #65758c; border: 0; border-bottom: 1px solid #d5dee8; padding: 8px 9px; font-size: 8pt; font-weight: 800; }
    QTableCornerButton::section { background: #eef2f6; border: 0; }

    QGroupBox { background: #ffffff; border: 1px solid #d8e0ea; border-radius: 11px; margin-top: 12px; padding: 18px 14px 14px 14px; }
    QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 2px 7px; color: #53647c; background: #ffffff; font-size: 9pt; font-weight: 800; }

    QTabWidget::pane { background: #ffffff; border: 1px solid #d8e0ea; border-radius: 9px; top: -1px; }
    QTabBar::tab { background: #f4f7fa; color: #6d7b90; padding: 9px 14px; margin-right: 2px; border: 1px solid #d7e0e9; border-bottom: 0; border-top-left-radius: 7px; border-top-right-radius: 7px; }
    QTabBar::tab:selected { background: #ffffff; color: #087f9c; border-color: #b8dbe5; font-weight: 700; }

    QScrollBar:vertical { background: #edf2f6; width: 13px; margin: 2px; border-radius: 5px; }
    QScrollBar::handle:vertical { background: #bdc9d7; min-height: 28px; border-radius: 5px; }
    QScrollBar::handle:vertical:hover { background: #9faebe; }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
    QScrollBar:horizontal { background: #edf2f6; height: 11px; margin: 2px; }
    QScrollBar::handle:horizontal { background: #bdc9d7; min-width: 28px; border-radius: 5px; }
    QScrollBar::handle:horizontal:hover { background: #9faebe; }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

    QSplitter::handle { background: #dce3eb; }
    QStatusBar { background: #ffffff; color: #6d7c91; border-top: 1px solid #d7e0e9; }
    QToolTip { background: #ffffff; color: #172033; border: 1px solid #b9c7d6; padding: 6px 8px; }
    QMessageBox { background: #ffffff; }
    """)


def apply_dark_theme(app):
    # Backwards-compatible name; v0.4.1 deliberately uses the light theme.
    return apply_light_theme(app)
