from __future__ import annotations
import os, sys, json, subprocess, shutil, zipfile, time
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QPlainTextEdit, QCheckBox, QMessageBox, QGroupBox
from PySide6.QtCore import QProcess
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import PROJECT_ROOT, CYBER_STYLE, qprocess_environment, powershell, human_size

SAFE_TRANSIENT_ROOTS=['artifacts/scratch','artifacts/tests/logs/verbose']

class Window(QMainWindow):
  def __init__(self):
    super().__init__(); self.setWindowTitle('C11-C MAINTENANCE'); self.resize(1100,760); self.proc=None
    root=QWidget(); self.setCentralWidget(root); lay=QVBoxLayout(root); t=QLabel('MAINTENANCE'); t.setObjectName('title'); lay.addWidget(t)
    box=QGroupBox('Safe operations'); bl=QVBoxLayout(box); lay.addWidget(box)
    for txt,fn in [('ANALIZAR LIMPIEZA',self.preview_cleanup),('LIMPIAR TRANSITORIOS SEGUROS',self.clean_cleanup),('VERIFICAR REPOSITORY LAYOUT',self.layout_check),('VALIDAR DELIVERY CONFIG',self.delivery_check),('DOCS REORG · DRY RUN',self.docs_dry),('GENERAR ZIP DEL PROYECTO',self.make_zip)]:
      b=QPushButton(txt); b.clicked.connect(fn); bl.addWidget(b)
    opt=QHBoxLayout(); self.include_art=QCheckBox('Incluir artifacts/'); self.include_art.setChecked(False); opt.addWidget(self.include_art); bl.addLayout(opt)
    self.log=QPlainTextEdit(); self.log.setReadOnly(True); lay.addWidget(self.log,1)
  def add(self,s): self.log.appendPlainText(s.rstrip())
  def preview_cleanup(self):
    lines=[]; total=0
    for rel in SAFE_TRANSIENT_ROOTS:
      p=PROJECT_ROOT/rel
      if not p.exists(): continue
      for f in p.rglob('*'):
        if f.is_file():
          try: n=f.stat().st_size; total+=n; lines.append(f'{f.relative_to(PROJECT_ROOT)} | {human_size(n)}')
          except OSError: pass
    self.add('[CLEANUP PREVIEW] '+str(len(lines))+' files | '+human_size(total)); self.add('/n'.join(lines[:500]) if lines else 'Nada para limpiar.')
  def clean_cleanup(self):
    self.preview_cleanup()
    if QMessageBox.question(self,'Confirmar limpieza','Se eliminarán SOLO los contenidos de artifacts/scratch y artifacts/tests/logs/verbose. ¿Continuar?')!=QMessageBox.Yes:return
    for rel in SAFE_TRANSIENT_ROOTS:
      p=PROJECT_ROOT/rel
      if not p.exists():continue
      for f in sorted(p.rglob('*'), reverse=True):
        try:
          if f.is_file():f.unlink()
          elif f.is_dir() and not any(f.iterdir()):f.rmdir()
        except OSError:pass
    self.add('[CLEANUP] COMPLETE')
  def run_ps(self,args,label):
    if self.proc:return
    self.add('> '+label); self.proc=QProcess(self); self.proc.setProcessEnvironment(qprocess_environment()); self.proc.setWorkingDirectory(str(PROJECT_ROOT)); self.proc.readyReadStandardOutput.connect(self.read); self.proc.readyReadStandardError.connect(self.read); self.proc.finished.connect(lambda c,s:self.finish(c,label)); self.proc.start(powershell(),['-NoProfile','-ExecutionPolicy','Bypass','-File']+args)
  def read(self):
    if not self.proc:return
    for fn in (self.proc.readAllStandardOutput,self.proc.readAllStandardError):
      x=bytes(fn()).decode('utf-8','replace');
      if x:self.add(x)
  def finish(self,c,label): self.read(); self.add(f'[{label}] EXIT={c}'); self.proc=None
  def layout_check(self): self.run_ps(['tools/maintenance/verify_repository_layout.ps1'],'LAYOUT')
  def delivery_check(self): self.run_ps(['tools/prototypes/c11c_bulk/validate_c11c_delivery_configuration.ps1'],'DELIVERY')
  def docs_dry(self): self.run_ps(['tools/maintenance/reorganize_docs_c11c_2.16.9.ps1'],'DOCS DRY RUN')
  def make_zip(self):
    out=PROJECT_ROOT/'artifacts'/'releases'/f'ChallengeEngineV01_STATELESS_{time.strftime("%Y%m%d_%H%M%S")}.zip'; out.parent.mkdir(parents=True,exist_ok=True)
    exclude_parts=['.git','.godot','__pycache__','.pytest_cache']
    if not self.include_art.isChecked(): exclude_parts.append('artifacts')
    count=0
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
      for p in PROJECT_ROOT.rglob('*'):
        if not p.is_file() or p==out:continue
        rel=p.relative_to(PROJECT_ROOT).as_posix(); parts=set(Path(rel).parts)
        if any(part in parts for part in exclude_parts):continue
        if rel.endswith('.pyc'):continue
        z.write(p,rel); count+=1
    self.add(f'[ZIP] {out.relative_to(PROJECT_ROOT)} | {human_size(out.stat().st_size)} | files={count}')
if __name__=='__main__':
 app=QApplication(sys.argv); app.setStyleSheet(CYBER_STYLE); w=Window(); w.show(); sys.exit(app.exec())
