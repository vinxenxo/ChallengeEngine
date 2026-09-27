from __future__ import annotations
import json, sys, shutil, time
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QPlainTextEdit, QPushButton, QLabel, QMessageBox, QSplitter, QCheckBox
from PySide6.QtCore import Qt
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import PROJECT_ROOT, CYBER_STYLE, open_path

TEXT_EXT={'.json','.jsonc','.cfg','.ini','.toml','.yaml','.yml','.txt','.md','.gdshader','.godot','.tscn'}
EDITABLE={'.json','.jsonc','.cfg','.ini','.toml','.yaml','.yml','.txt'}
ROOTS=['challenges','definitions','profiles','schemas','docs/contracts','docs/checkpoints','tools/prototypes/c11c_common','c11c-suite/c11c-producer']
class Window(QMainWindow):
  def __init__(self):
    super().__init__(); self.setWindowTitle('C11-C CONFIG'); self.resize(1400,840); self.current=None
    root=QWidget(); self.setCentralWidget(root); lay=QVBoxLayout(root); t=QLabel('CONFIG / CONTRACTS'); t.setObjectName('title'); lay.addWidget(t)
    sp=QSplitter(Qt.Horizontal); lay.addWidget(sp,1)
    self.tree=QTreeWidget(); self.tree.setHeaderLabels(['Configuración','Estado']); self.tree.itemSelectionChanged.connect(self.load_item); sp.addWidget(self.tree)
    right=QVBoxLayout(); rw=QWidget(); rw.setLayout(right); sp.addWidget(rw)
    self.path=QLabel('SIN SELECCIÓN'); self.path.setObjectName('muted'); right.addWidget(self.path)
    self.editor=QPlainTextEdit(); right.addWidget(self.editor,1)
    btn=QHBoxLayout(); right.addLayout(btn); self.validate=QPushButton('VALIDAR JSON'); self.validate.clicked.connect(self.validate_json); btn.addWidget(self.validate); self.save=QPushButton('GUARDAR + BACKUP'); self.save.clicked.connect(self.save_file); btn.addWidget(self.save); self.open=QPushButton('ABRIR CARPETA'); self.open.clicked.connect(self.open_folder); btn.addWidget(self.open)
    self.load_tree()
  def load_tree(self):
    self.tree.clear()
    project_item=QTreeWidgetItem(['project.godot','READ-ONLY']); project_item.setData(0,Qt.UserRole,str(PROJECT_ROOT/'project.godot')); self.tree.addTopLevelItem(project_item)
    for rel in ROOTS:
      base=PROJECT_ROOT/rel
      if not base.exists():continue
      top=QTreeWidgetItem([rel,'']) ; top.setData(0,Qt.UserRole,None); self.tree.addTopLevelItem(top)
      for p in sorted(base.rglob('*')):
        if not p.is_file():continue
        if p.suffix.lower() not in TEXT_EXT and p.name!='project.godot':continue
        item=QTreeWidgetItem([p.name,'EDIT' if p.suffix.lower() in EDITABLE else 'READ-ONLY']); item.setData(0,Qt.UserRole,str(p)); top.addChild(item)
    self.tree.expandToDepth(0)
  def load_item(self):
    items=self.tree.selectedItems(); self.current=Path(items[0].data(0,Qt.UserRole)) if items and items[0].data(0,Qt.UserRole) else None
    self.editor.clear(); self.path.setText(str(self.current.relative_to(PROJECT_ROOT)) if self.current else 'SIN SELECCIÓN')
    if not self.current:return
    raw=self.current.read_text(encoding='utf-8',errors='replace'); self.editor.setPlainText(raw); self.editor.setReadOnly(self.current.suffix.lower() not in EDITABLE)
    self.validate.setEnabled(self.current.suffix.lower()=='.json'); self.save.setEnabled(self.current.suffix.lower() in EDITABLE)
  def validate_json(self):
    if not self.current:return
    try: json.loads(self.editor.toPlainText()); QMessageBox.information(self,'JSON','VALIDO')
    except Exception as e: QMessageBox.critical(self,'JSON',f'INVALIDO\n{e}')
  def save_file(self):
    if not self.current:return
    if self.current.suffix.lower()=='.json':
      try: json.loads(self.editor.toPlainText())
      except Exception as e: QMessageBox.critical(self,'Guardar',f'JSON inválido; no se escribió.\n{e}'); return
    if QMessageBox.question(self,'Confirmar escritura',f'Se modificará:\n{self.current.relative_to(PROJECT_ROOT)}\n\nCrear backup previo (.bak)?')!=QMessageBox.Yes:return
    backup=self.current.with_suffix(self.current.suffix+'.bak')
    shutil.copy2(self.current,backup)
    self.current.write_text(self.editor.toPlainText(),encoding='utf-8')
    QMessageBox.information(self,'Guardar',f'Guardado. Backup: {backup.name}')
  def open_folder(self):
    if self.current: open_path(self.current.parent)
if __name__=='__main__':
 app=QApplication(sys.argv); app.setStyleSheet(CYBER_STYLE); w=Window(); w.show(); sys.exit(app.exec())
