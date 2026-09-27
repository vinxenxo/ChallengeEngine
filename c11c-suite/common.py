from __future__ import annotations
import json, os, shutil, subprocess, tempfile
from pathlib import Path
from typing import Iterable
from PySide6.QtCore import QProcess, QProcessEnvironment, Qt
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QMessageBox

HERE = Path(__file__).resolve().parent
SUITE_ROOT = HERE.parent if HERE.name.startswith("c11c-") else HERE
PROJECT_ROOT = Path(os.environ.get("C11C_PROJECT_ROOT", SUITE_ROOT.parent)).resolve()

CYBER_STYLE = """
QWidget { background:#070a12; color:#dbeafe; font-family:'Segoe UI'; font-size:13px; }
QMainWindow { background:#070a12; }
QGroupBox { border:1px solid #16324b; margin-top:9px; padding:12px; border-radius:6px; }
QGroupBox::title { color:#6ff9ff; subcontrol-origin:margin; left:12px; padding:0 5px; }
QPushButton { background:#0c1724; border:1px solid #1b7083; border-radius:5px; padding:8px 12px; color:#dffbff; }
QPushButton:hover { border:1px solid #ff3bf7; color:#ffffff; background:#12172a; }
QPushButton:pressed { background:#21102c; }
QLineEdit, QPlainTextEdit, QTreeWidget, QListWidget, QTableWidget, QComboBox, QSpinBox { background:#050810; border:1px solid #17314a; border-radius:4px; color:#e6f7ff; selection-background-color:#8b1d88; selection-color:#ffffff; }
QHeaderView::section { background:#0b1522; color:#6ff9ff; border:0; padding:5px; }
QCheckBox { color:#cfefff; }
QLabel#title { color:#ff46e7; font-size:20px; font-weight:700; }
QLabel#muted { color:#7991a9; }
QProgressBar { border:1px solid #17314a; background:#050810; height:10px; border-radius:4px; }
QProgressBar::chunk { background:#00e5ff; }
QSplitter::handle { background:#122235; }
QSlider::groove:horizontal { background:#142236; height:5px; }
QSlider::handle:horizontal { background:#ff46e7; width:12px; margin:-4px 0; border-radius:6px; }
QTabBar::tab { background:#0b1522; padding:8px 14px; color:#8ca9bf; }
QTabBar::tab:selected { color:#6ff9ff; border-bottom:2px solid #ff46e7; }
"""

def qprocess_environment() -> QProcessEnvironment:
    env = QProcessEnvironment.systemEnvironment()
    env.insert("C11C_PROJECT_ROOT", str(PROJECT_ROOT))
    return env

def powershell() -> str:
    return shutil.which("powershell.exe") or shutil.which("pwsh") or "powershell.exe"

def open_path(path: Path) -> None:
    if os.name == "nt":
        os.startfile(str(path))  # type: ignore[attr-defined]
    elif shutil.which("xdg-open"):
        subprocess.Popen(["xdg-open", str(path)])

def human_size(n: int) -> str:
    units=['B','KB','MB','GB','TB']
    value=float(n)
    for u in units:
        if value < 1024 or u == units[-1]: return f"{value:.1f} {u}"
        value /= 1024
    return f"{n} B"

def json_load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))
