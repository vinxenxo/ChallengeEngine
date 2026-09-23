from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication


QSS = """
QWidget { background-color: #0e1116; color: #e6edf3;
    font-family: 'Segoe UI'; font-size: 10pt; }
QMainWindow { background-color: #0e1116; }
QFrame#TopBar { background-color: #141922;
    border-bottom: 1px solid #232a36; }
QLabel#TopBarTitle { font-size: 14pt; font-weight: 600; color: #e6edf3; }
QLabel#TopBarMeta { color: #8b96a8; font-family: 'Consolas'; }
QFrame#NavRail { background-color: #11151d;
    border-right: 1px solid #232a36; }
QPushButton#NavButton {
    text-align: left; padding: 10px 14px; border: none;
    border-radius: 6px; color: #b7c1d3; background: transparent;
    font-size: 10pt;
}
QPushButton#NavButton:hover { background: #1a2130; color: #ffffff; }
QPushButton#NavButton:checked {
    background: #1e2a3d; color: #7ad7ff; font-weight: 600; }
QLabel#PageTitle { font-size: 18pt; font-weight: 600; color: #e6edf3; }
QLabel#PageSubtitle { color: #8b96a8; }
QFrame#Card { background: #141922;
    border: 1px solid #232a36; border-radius: 8px; }
QLabel#CardTitle { color: #8b96a8; font-size: 9pt; letter-spacing: 1px; }
QLabel#CardValue { font-size: 16pt; font-weight: 600; color: #e6edf3; }
QLabel#CardState { font-family: 'Consolas'; color: #6ee7a7; }
QPushButton.Primary {
    background: #1f6feb; color: #ffffff; border: none;
    padding: 9px 16px; border-radius: 6px; font-weight: 600;
}
QPushButton.Primary:hover { background: #2b7fff; }
QPushButton.Ghost {
    background: transparent; color: #b7c1d3;
    border: 1px solid #2b3444; padding: 8px 14px; border-radius: 6px;
}
QPushButton.Ghost:hover { border-color: #3d4a60; color: #ffffff; }
QPlainTextEdit#LogView {
    background: #0a0d12; color: #c9d3e2;
    font-family: 'Consolas'; font-size: 9pt;
    border: 1px solid #232a36; border-radius: 6px;
}
QTableWidget {
    background: #0f141c; alternate-background-color: #121924;
    gridline-color: #1e2632; border: 1px solid #232a36;
    border-radius: 6px;
}
QHeaderView::section {
    background: #141922; color: #8b96a8; padding: 6px;
    border: none; border-bottom: 1px solid #232a36; font-weight: 600;
}
QLineEdit, QSpinBox, QComboBox, QPlainTextEdit {
    background: #0f141c; border: 1px solid #232a36;
    border-radius: 5px; padding: 5px 8px; color: #e6edf3;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border-color: #1f6feb; }
QStatusBar { background: #0e1116; color: #8b96a8; }
"""


def apply_dark_theme(app):
    app.setStyle("Fusion")
    app.setStyleSheet(QSS)
    app.setFont(QFont("Segoe UI", 10))
