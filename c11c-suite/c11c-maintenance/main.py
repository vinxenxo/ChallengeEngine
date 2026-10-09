from __future__ import annotations
import os, sys, json, subprocess, shutil, zipfile, time
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QPlainTextEdit, QMessageBox, QGroupBox
from PySide6.QtCore import QProcess
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import PROJECT_ROOT, CYBER_STYLE, qprocess_environment, powershell, human_size

SAFE_TRANSIENT_ROOTS=['artifacts/scratch','artifacts/tests/logs/verbose']

class Window(QMainWindow):
  def __init__(self):
    super().__init__(); self.setWindowTitle('C11-C MAINTENANCE'); self.resize(1100,760); self.proc=None
    root=QWidget(); self.setCentralWidget(root); lay=QVBoxLayout(root); t=QLabel('MAINTENANCE'); t.setObjectName('title'); lay.addWidget(t)
    box=QGroupBox('Safe operations'); bl=QVBoxLayout(box); lay.addWidget(box)
    for txt,fn in [('ANALIZAR LIMPIEZA SEGURA',self.preview_cleanup),('ARCHIVAR TRANSITORIOS · REVERSIBLE (D9.11)',self.clean_cleanup),('ANALIZAR MEDIA C11-C',self.c11c_media_preview),('LIMPIAR MEDIA C11-C',self.c11c_media_clean),('ORGANIZAR RAÍZ · DRY RUN',self.root_organize_dry),('ORGANIZAR RAÍZ · APPLY',self.root_organize_apply),('VERIFICAR REPOSITORY LAYOUT',self.layout_check),('VALIDAR DELIVERY CONFIG',self.delivery_check),('CONSOLIDAR DOCS C11-C 2.19 · DRY RUN',self.docs_dry),('FREEZE C11-C · DRY RUN',self.freeze_dry),('GENERAR ZIP FROZEN C11-C 2.19.12',self.make_zip)]:
      b=QPushButton(txt); b.clicked.connect(fn); bl.addWidget(b)
    d9box=QGroupBox('C11-D D9.11 · Maintenance 0.2.0 — canonical backend / dry-run first')
    d9grid=QGridLayout(d9box)
    d9actions=[
      ('D9.11 PLAN · DRY RUN',self.d9_plan),
      ('D9.11 DOCS AUDIT · DRY RUN',self.d9_docs_audit),
      ('D9.11 FREEZE PREFLIGHT',self.d9_freeze_preflight),
      ('D9.11 CLEANUP PREVIEW',self.d9_cleanup_preview),
      ('D9.11 CONTROL QUARANTINE · DRY RUN',self.d9_quarantine_preview),
      ('D9.11 CONTROL QUARANTINE · APPLY',self.d9_quarantine_apply),
      ('D9.11 CONTROL RESTORE · DRY RUN',self.d9_restore_preview),
      ('D9.11 CONTROL RESTORE · APPLY',self.d9_restore_apply),
      ('D9.11 CLEANUP RESTORE · DRY RUN',self.d9_cleanup_restore_preview),
      ('D9.11 CLEANUP RESTORE · APPLY',self.d9_cleanup_restore_apply),
    ]
    for index,(txt,fn) in enumerate(d9actions):
      b=QPushButton(txt); b.clicked.connect(fn); d9grid.addWidget(b,index//3,index%3)
    lay.addWidget(d9box)
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
    self.add('[CLEANUP PREVIEW] '+str(len(lines))+' files | '+human_size(total)); self.add('\n'.join(lines[:500]) if lines else 'Nada para limpiar.')
  def clean_cleanup(self):
    # Compatibility entry point for the original Maintenance button. The old
    # direct-unlink implementation is intentionally retired; all cleanup now
    # goes through the canonical D9.11 reversible archive backend.
    self.d9_cleanup_apply()
  def run_ps(self,args,label):
    if self.proc:return
    self.add('> '+label); self.proc=QProcess(self); self.proc.setProcessEnvironment(qprocess_environment()); self.proc.setWorkingDirectory(str(PROJECT_ROOT)); self.proc.readyReadStandardOutput.connect(self.read); self.proc.readyReadStandardError.connect(self.read); self.proc.finished.connect(lambda c,s:self.finish(c,label)); self.proc.start(powershell(),['-NoProfile','-ExecutionPolicy','Bypass','-File']+args)
  def read(self):
    if not self.proc:return
    for fn in (self.proc.readAllStandardOutput,self.proc.readAllStandardError):
      x=bytes(fn()).decode('utf-8','replace');
      if x:self.add(x)
  def finish(self,c,label): self.read(); self.add(f'[{label}] EXIT={c}'); self.proc=None
  def c11c_media_preview(self): self.run_ps(['tools/prototypes/c11c_bulk/clean_c11c_artifacts.ps1'],'C11-C MEDIA DRY RUN')
  def c11c_media_clean(self):
    if QMessageBox.question(self,'Confirmar limpieza C11-C','Se eliminarán SOLO medios regenerables de los roots C11-C prototype permitidos por clean_c11c_artifacts.ps1. ¿Continuar?')==QMessageBox.Yes:
      self.run_ps(['tools/prototypes/c11c_bulk/clean_c11c_artifacts.ps1','-Apply'],'C11-C MEDIA APPLY')
  def root_organize_dry(self): self.run_ps(['c11c-suite/c11c-maintenance/organize_repository_root.ps1'],'ROOT ORGANIZE DRY RUN')
  def root_organize_apply(self):
    if QMessageBox.question(self,'Confirmar organización','Se aplicarán SOLO los movimientos allowlistados de organización de raíz y se archivará el alias c11c-maintenace sin borrar evidencia. ¿Continuar?')==QMessageBox.Yes:
      self.run_ps(['c11c-suite/c11c-maintenance/organize_repository_root.ps1','-Apply'],'ROOT ORGANIZE APPLY')
  def layout_check(self): self.run_ps(['tools/maintenance/verify_repository_layout.ps1'],'LAYOUT')
  def delivery_check(self): self.run_ps(['tools/prototypes/c11c_bulk/validate_c11c_delivery_configuration.ps1'],'DELIVERY')
  def docs_dry(self): self.run_ps(['tools/maintenance/consolidate_c11c_2_19_documentation.ps1','-DryRun'],'DOCS C11-C 2.19 DRY RUN')
  def freeze_dry(self): self.run_ps(['tools/maintenance/create_c11c_freeze_zip.ps1','-DryRun'],'FREEZE DRY RUN C11-C 2.19.12')
  def make_zip(self): self.run_ps(['tools/maintenance/create_c11c_freeze_zip.ps1'],'FREEZE ZIP C11-C 2.19.12')
  def run_d9_maintenance(self,args,label):
    if self.proc:return
    script=PROJECT_ROOT/'tools'/'c11d'/'d9'/'maintenance.py'
    if not script.is_file():
      self.add('[D9.11 BLOCKED] Canonical maintenance backend missing: '+str(script)); return
    self.add('> '+label+' | canonical tools/c11d/d9/maintenance.py')
    self.proc=QProcess(self); self.proc.setProcessEnvironment(qprocess_environment()); self.proc.setWorkingDirectory(str(PROJECT_ROOT)); self.proc.readyReadStandardOutput.connect(self.read); self.proc.readyReadStandardError.connect(self.read); self.proc.finished.connect(lambda c,s:self.finish(c,label)); self.proc.start(sys.executable,[str(script)]+list(args))
  def d9_plan(self): self.run_d9_maintenance(['plan'],'D9.11 MAINTENANCE PLAN')
  def d9_docs_audit(self): self.run_d9_maintenance(['docs-audit'],'D9.11 DOCUMENTATION AUDIT · DRY RUN')
  def d9_freeze_preflight(self): self.run_d9_maintenance(['freeze-preflight'],'D9.11 FREEZE PREFLIGHT · READ ONLY')
  def d9_cleanup_preview(self): self.run_d9_maintenance(['cleanup-preview'],'D9.11 CLEANUP PREVIEW')
  def d9_cleanup_apply(self):
    if QMessageBox.question(self,'Confirmar limpieza D9.11','Se archivarán de forma reversible SOLO los archivos de artifacts/scratch y artifacts/tests/logs/verbose. No habrá borrado permanente. ¿Continuar?')==QMessageBox.Yes:
      self.run_d9_maintenance(['cleanup-allowlisted','--apply','--confirm','CLEAN_TRANSIENTS_ONLY'],'D9.11 CLEANUP · REVERSIBLE ARCHIVE')
  def d9_quarantine_preview(self): self.run_d9_maintenance(['quarantine-legacy-control'],'D9.11 LEGACY CONTROL QUARANTINE · DRY RUN')
  def d9_quarantine_apply(self):
    if QMessageBox.question(self,'Confirmar cuarentena D9.11','Se moverá intacta SOLO c11c-suite/c11d-control a docs/history/root_conflicts. El manifiesto C11-C quedará byte a byte intacto y sus referencias se registrarán en el ledger. ¿Continuar?')==QMessageBox.Yes:
      self.run_d9_maintenance(['quarantine-legacy-control','--apply','--confirm','QUARANTINE_C11D_CONTROL'],'D9.11 LEGACY CONTROL QUARANTINE · APPLY')
  def d9_restore_preview(self): self.run_d9_maintenance(['restore-legacy-control'],'D9.11 LEGACY CONTROL RESTORE · DRY RUN')
  def d9_restore_apply(self):
    if QMessageBox.question(self,'Confirmar restauración D9.11','Se restaurará el último snapshot verificado solo si el origen no existe y coinciden las identidades de árbol y manifiesto. No se registrará como superficie operativa. ¿Continuar?')==QMessageBox.Yes:
      self.run_d9_maintenance(['restore-legacy-control','--apply','--confirm','RESTORE_C11D_CONTROL'],'D9.11 LEGACY CONTROL RESTORE · APPLY')
  def d9_cleanup_restore_preview(self): self.run_d9_maintenance(['restore-cleanup-archive'],'D9.11 CLEANUP ARCHIVE RESTORE · DRY RUN')
  def d9_cleanup_restore_apply(self):
    if QMessageBox.question(self,'Confirmar restauración de transitorios','Se restaurará el último archivo de transitorios solo si no existe ningún origen en conflicto y coinciden los hashes. No se sobrescribirán archivos. ¿Continuar?')==QMessageBox.Yes:
      self.run_d9_maintenance(['restore-cleanup-archive','--apply','--confirm','RESTORE_CLEANUP_ARCHIVE'],'D9.11 CLEANUP ARCHIVE RESTORE · APPLY')
if __name__=='__main__':
 app=QApplication(sys.argv); app.setStyleSheet(CYBER_STYLE); w=Window(); w.show(); sys.exit(app.exec())
