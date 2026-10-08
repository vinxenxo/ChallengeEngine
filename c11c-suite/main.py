from __future__ import annotations
import os, sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout, QMessageBox
from PySide6.QtCore import QProcess
from PySide6.QtGui import QFont
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import PROJECT_ROOT, CYBER_STYLE, qprocess_environment, powershell

APPS = [
 ('TEST','c11c-test/main.py','Test / QA / regression'),
 ('CATALOG','c11c-catalog/main.py','Artifacts / thumbnails / metadata'),
 ('MAINTENANCE','c11c-maintenance/main.py','Cleanup / layout / ZIP'),
 ('CONFIG','c11c-config/main.py','JSON / definitions / contracts'),
 ('PRODUCER','c11c-producer/main.py','A LA CARTA audiovisual production'),
]
class SuiteWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('C11-C SUITE 0.1.4'); self.resize(980,620); self.procs=[]
        w=QWidget(); lay=QVBoxLayout(w); self.setCentralWidget(w)
        t=QLabel('C11-C SUITE'); t.setObjectName('title'); lay.addWidget(t)
        s=QLabel('Operational interfaces around the deterministic core; c11c-suite is the canonical active operator surface.'); s.setObjectName('muted'); lay.addWidget(s)
        grid=QGridLayout(); lay.addLayout(grid)
        for i,(label,path,desc) in enumerate(APPS):
            b=QPushButton(f'{label}\n{desc}'); b.setMinimumHeight(100); b.clicked.connect(lambda _=False,p=path: self.launch(p)); grid.addWidget(b,i//2,i%2)
        note=QLabel('Boundary: GUIs orchestrate, inspect and configure declared inputs. They do not implement mechanics, RNG, simulation truth or renderers.')
        note.setWordWrap(True); note.setObjectName('muted'); lay.addWidget(note)
    def launch(self, relative):
        p=QProcess(self); p.setProcessEnvironment(qprocess_environment()); p.setWorkingDirectory(str(PROJECT_ROOT)); p.start(sys.executable, [str(PROJECT_ROOT/'c11c-suite'/relative)])
        self.procs.append(p)
        if not p.waitForStarted(1500): QMessageBox.warning(self,'C11-C Suite',f'No se pudo lanzar {relative}.')
if __name__=='__main__':
    app=QApplication(sys.argv); app.setStyleSheet(CYBER_STYLE); win=SuiteWindow(); win.show(); sys.exit(app.exec())
