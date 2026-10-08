from __future__ import annotations
import difflib, json, os, shutil, sys, tempfile
from pathlib import Path
from PySide6.QtWidgets import (QApplication,QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QTreeWidget,QTreeWidgetItem,
 QPlainTextEdit,QPushButton,QLabel,QMessageBox,QSplitter,QTabWidget,QTableWidget,QTableWidgetItem,QHeaderView,QInputDialog,QComboBox)
from PySide6.QtCore import Qt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import PROJECT_ROOT,CYBER_STYLE,open_path
from c11d_config import CONFIG_VERSION,registry_rows,validate_c11d_contracts,validate_operator_profile,blank_profile,profile_path,operator_profiles,sha256_text,save_operator_profile,restore_operator_profile_backup,generic_editor_path_protected
TEXT_EXT={'.json','.jsonc','.cfg','.ini','.toml','.yaml','.yml','.txt','.md','.gdshader','.godot','.tscn'}
EDITABLE={'.json','.jsonc','.cfg','.ini','.toml','.yaml','.yml','.txt'}
ROOTS=['challenges','definitions','profiles','schemas','docs/contracts','docs/checkpoints','tools/prototypes/c11c_common','c11c-suite/c11c-producer']

def protected_path(path:Path)->bool:
 return generic_editor_path_protected(PROJECT_ROOT,path)

class Window(QMainWindow):
 def __init__(self):
  super().__init__(); self.setWindowTitle('C11-C CONFIG '+CONFIG_VERSION); self.resize(1500,900); self.current=None; self.profile_file=None; self.profile_base_text=''; self.registry_entries=[]
  outer=QWidget(); self.setCentralWidget(outer); layout=QVBoxLayout(outer)
  title=QLabel('CONFIG / CONTRACTS + C11-D GOVERNANCE · '+CONFIG_VERSION); title.setObjectName('title'); layout.addWidget(title)
  note=QLabel('Los contratos canónicos D son de solo lectura. Los perfiles operativos se validan, guardan explícitamente y nunca activan producción.'); note.setObjectName('muted'); note.setWordWrap(True); layout.addWidget(note)
  self.tabs=QTabWidget(); layout.addWidget(self.tabs,1)
  self._build_repository_tab(); self._build_d_contracts_tab(); self._build_profiles_tab()
  self.load_tree(); self.refresh_d_contracts(); self.refresh_profiles()

 def _build_repository_tab(self):
  page=QWidget(); layout=QVBoxLayout(page); split=QSplitter(Qt.Horizontal); layout.addWidget(split,1)
  self.tree=QTreeWidget(); self.tree.setHeaderLabels(['Configuración','Estado']); self.tree.itemSelectionChanged.connect(self.load_item); split.addWidget(self.tree)
  right=QWidget(); r=QVBoxLayout(right); split.addWidget(right)
  self.path_label=QLabel('SIN SELECCIÓN'); self.path_label.setObjectName('muted'); r.addWidget(self.path_label)
  self.editor=QPlainTextEdit(); r.addWidget(self.editor,1)
  buttons=QHBoxLayout(); r.addLayout(buttons)
  self.validate_button=QPushButton('VALIDAR JSON'); self.validate_button.clicked.connect(self.validate_json); buttons.addWidget(self.validate_button)
  self.save_button=QPushButton('GUARDAR + BACKUP'); self.save_button.clicked.connect(self.save_file); buttons.addWidget(self.save_button)
  self.open_button=QPushButton('ABRIR CARPETA'); self.open_button.clicked.connect(self.open_folder); buttons.addWidget(self.open_button)
  split.setSizes([520,900]); self.tabs.addTab(page,'REPOSITORY CONFIG')

 def _build_d_contracts_tab(self):
  page=QWidget(); layout=QVBoxLayout(page); top=QHBoxLayout(); layout.addLayout(top)
  self.d_status=QLabel('D2–D9 canonical registries'); self.d_status.setObjectName('muted'); top.addWidget(self.d_status,1)
  self.validate_d_button=QPushButton('VALIDAR TODOS LOS CONTRATOS D'); self.validate_d_button.clicked.connect(self.validate_all_d); top.addWidget(self.validate_d_button)
  refresh=QPushButton('REFRESCAR'); refresh.clicked.connect(self.refresh_d_contracts); top.addWidget(refresh)
  split=QSplitter(Qt.Horizontal); layout.addWidget(split,1)
  self.d_table=QTableWidget(0,6); self.d_table.setHorizontalHeaderLabels(['Dominio','ID','Estado','SHA-256','Acceso','Ruta']); self.d_table.setSelectionBehavior(QTableWidget.SelectRows); self.d_table.setSelectionMode(QTableWidget.SingleSelection); self.d_table.itemSelectionChanged.connect(self.show_d_contract); self.d_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents); split.addWidget(self.d_table)
  details=QWidget(); side=QVBoxLayout(details); self.d_detail_title=QLabel('SELECCIONA UN CONTRATO'); self.d_detail_title.setObjectName('muted'); side.addWidget(self.d_detail_title)
  self.d_json=QPlainTextEdit(); self.d_json.setReadOnly(True); side.addWidget(self.d_json,1)
  self.d_open_button=QPushButton('ABRIR CARPETA DEL CONTRATO'); self.d_open_button.clicked.connect(self.open_d_contract_folder); side.addWidget(self.d_open_button)
  split.addWidget(details); split.setSizes([920,600]); self.tabs.addTab(page,'C11-D CONTRACTS')

 def _build_profiles_tab(self):
  page=QWidget(); layout=QVBoxLayout(page)
  note=QLabel('Los perfiles son presets, no órdenes de ejecución. seed y music_seed deben ser valores enteros explícitos e independientes; no se generan automáticamente.'); note.setObjectName('muted'); note.setWordWrap(True); layout.addWidget(note)
  top=QHBoxLayout(); layout.addLayout(top); self.profile_combo=QComboBox(); self.profile_combo.setMinimumWidth(360); top.addWidget(self.profile_combo,1)
  for label,slot in [('REFRESCAR',self.refresh_profiles),('CARGAR',self.load_profile_from_combo),('NUEVO PERFIL VACÍO',self.new_profile)]:
   b=QPushButton(label); b.clicked.connect(slot); top.addWidget(b)
  self.profile_editor=QPlainTextEdit(); self.profile_editor.setPlaceholderText('Complete todos los campos requeridos. La plantilla inicial no incluye seeds ni perfiles preseleccionados.'); layout.addWidget(self.profile_editor,1)
  self.profile_state=QLabel('SIN PERFIL CARGADO'); self.profile_state.setObjectName('muted'); layout.addWidget(self.profile_state)
  actions=QHBoxLayout(); layout.addLayout(actions)
  for label,slot in [('VALIDAR + HASH',self.validate_profile_ui),('MOSTRAR DIFF',self.show_profile_diff),('GUARDAR + BACKUP',self.save_profile),('RESTAURAR .BAK',self.restore_profile_backup),('ABRIR CARPETA',self.open_profile_folder)]:
   b=QPushButton(label); b.clicked.connect(slot); actions.addWidget(b)
  self.tabs.addTab(page,'C11-D OPERATOR PROFILES')

 def load_tree(self):
  self.tree.clear(); project=QTreeWidgetItem(['project.godot','READ-ONLY']); project.setData(0,Qt.UserRole,str(PROJECT_ROOT/'project.godot')); self.tree.addTopLevelItem(project)
  for rel in ROOTS:
   base=PROJECT_ROOT/rel
   if not base.exists():continue
   top=QTreeWidgetItem([rel,'']); top.setData(0,Qt.UserRole,None); self.tree.addTopLevelItem(top)
   for path in sorted(base.rglob('*')):
    if not path.is_file() or (path.suffix.lower() not in TEXT_EXT and path.name!='project.godot'):continue
    ro=protected_path(path) or path.suffix.lower() not in EDITABLE
    item=QTreeWidgetItem([path.name,'READ-ONLY' if ro else 'EDIT']); item.setData(0,Qt.UserRole,str(path)); top.addChild(item)
  self.tree.expandToDepth(0)

 def load_item(self):
  items=self.tree.selectedItems(); self.current=Path(items[0].data(0,Qt.UserRole)) if items and items[0].data(0,Qt.UserRole) else None
  self.editor.clear(); self.path_label.setText(str(self.current.relative_to(PROJECT_ROOT)) if self.current else 'SIN SELECCIÓN')
  if not self.current:self.save_button.setEnabled(False); self.validate_button.setEnabled(False); return
  try: raw=self.current.read_text(encoding='utf-8',errors='replace')
  except Exception as exc: self.editor.setPlainText(str(exc)); self.editor.setReadOnly(True); self.save_button.setEnabled(False); self.validate_button.setEnabled(False); return
  self.editor.setPlainText(raw); ro=protected_path(self.current) or self.current.suffix.lower() not in EDITABLE
  self.editor.setReadOnly(ro); self.validate_button.setEnabled(self.current.suffix.lower()=='.json'); self.save_button.setEnabled(not ro)

 def validate_json(self):
  if not self.current:return
  try:json.loads(self.editor.toPlainText()); QMessageBox.information(self,'JSON','VÁLIDO')
  except Exception as exc:QMessageBox.critical(self,'JSON',f'INVÁLIDO\n{exc}')

 def save_file(self):
  if not self.current:return
  if protected_path(self.current):QMessageBox.warning(self,'Solo lectura','Ruta protegida. Los contratos canónicos D no se editan desde esta GUI.'); return
  if self.current.suffix.lower()=='.json':
   try:json.loads(self.editor.toPlainText())
   except Exception as exc:QMessageBox.critical(self,'Guardar',f'JSON inválido; no se escribió.\n{exc}'); return
  if QMessageBox.question(self,'Confirmar escritura',f'Se modificará:\n{self.current.relative_to(PROJECT_ROOT)}\n\nCrear backup previo (.bak)?')!=QMessageBox.Yes:return
  shutil.copy2(self.current,self.current.with_suffix(self.current.suffix+'.bak')); self.current.write_text(self.editor.toPlainText(),encoding='utf-8'); QMessageBox.information(self,'Guardar','Guardado con backup.'); self.load_tree()

 def open_folder(self):
  if self.current:open_path(self.current.parent)

 def refresh_d_contracts(self):
  self.registry_entries=registry_rows(PROJECT_ROOT); self.d_table.setRowCount(len(self.registry_entries))
  for i,row in enumerate(self.registry_entries):
   values=[row['domain'],row['id'],row['status'],row.get('sha256','')[:16],row['authority'],row['path']]
   for j,value in enumerate(values):
    item=QTableWidgetItem(str(value)); item.setData(Qt.UserRole,i); self.d_table.setItem(i,j,item)
  valid=sum(1 for row in self.registry_entries if row['status']=='VALID_JSON')
  self.d_status.setText(f'C11-D Config {CONFIG_VERSION} · contratos JSON {valid}/{len(self.registry_entries)} · solo lectura · runtime/release NONE')
  if self.registry_entries and self.d_table.currentRow()<0:self.d_table.selectRow(0)

 def show_d_contract(self):
  row=self.d_table.currentRow()
  if row<0 or row>=len(self.registry_entries):return
  entry=self.registry_entries[row]; path=PROJECT_ROOT/entry['path']; self.d_detail_title.setText(f"{entry['id']} · {entry['status']} · SHA-256 {entry.get('sha256','')}")
  try:self.d_json.setPlainText(json.dumps(json.loads(path.read_text(encoding='utf-8-sig')),ensure_ascii=False,indent=2))
  except Exception as exc:self.d_json.setPlainText(f'NO SE PUEDE LEER/VALIDAR\n{exc}')
  self.d_open_button.setEnabled(path.exists())

 def open_d_contract_folder(self):
  row=self.d_table.currentRow()
  if 0<=row<len(self.registry_entries):open_path((PROJECT_ROOT/self.registry_entries[row]['path']).parent)

 def validate_all_d(self):
  rows,errors=validate_c11d_contracts(PROJECT_ROOT); self.registry_entries=rows; self.refresh_d_contracts()
  if errors:QMessageBox.critical(self,'C11-D Contract Validation','FAIL\n\n'+'\n'.join(errors))
  else:QMessageBox.information(self,'C11-D Contract Validation',f'PASS\n{len(rows)} contracts parsed and governance invariants verified.\nNo files modified.')

 def refresh_profiles(self):
  if not hasattr(self,'profile_combo'):return
  selected=self.profile_combo.currentData(); self.profile_combo.clear()
  for path in operator_profiles(PROJECT_ROOT):self.profile_combo.addItem(path.name,str(path))
  if selected:
   index=self.profile_combo.findData(selected)
   if index>=0:self.profile_combo.setCurrentIndex(index)
  if hasattr(self,'tree'):self.load_tree()

 def load_profile_from_combo(self):
  data=self.profile_combo.currentData()
  if not data:QMessageBox.information(self,'Perfil','No hay perfiles. Usa NUEVO PERFIL VACÍO.'); return
  path=Path(data).resolve()
  try:path.relative_to((PROJECT_ROOT/'profiles/c11d/operator').resolve())
  except ValueError:QMessageBox.critical(self,'Perfil','Ruta fuera del directorio autorizado.'); return
  self.profile_file=path; self.profile_base_text=path.read_text(encoding='utf-8-sig'); self.profile_editor.setPlainText(self.profile_base_text)
  self.profile_state.setText(f"CARGADO: {path.relative_to(PROJECT_ROOT)} · SHA-256 {sha256_text(self.profile_base_text)}")

 def new_profile(self):
  profile_id,ok=QInputDialog.getText(self,'Nuevo perfil','Identificador único (sin rutas):')
  if not ok:return
  try:target=profile_path(PROJECT_ROOT,profile_id.strip())
  except Exception as exc:QMessageBox.critical(self,'Nuevo perfil',str(exc)); return
  if target.exists():QMessageBox.warning(self,'Nuevo perfil','Ese perfil existe. Cárgalo o elige otro ID.'); return
  self.profile_file=None; self.profile_base_text=''; self.profile_editor.setPlainText(json.dumps(blank_profile(profile_id.strip()),ensure_ascii=False,indent=2)); self.profile_state.setText('PERFIL VACÍO · sin seeds/perfiles implícitos · pendiente de validación')

 def current_profile(self):
  try:profile=json.loads(self.profile_editor.toPlainText())
  except Exception as exc:return None,[f'JSON inválido: {exc}']
  expected=self.profile_file.stem if self.profile_file is not None else None
  return profile,validate_operator_profile(profile,PROJECT_ROOT,expected)

 def validate_profile_ui(self):
  profile,errors=self.current_profile()
  if errors:self.profile_state.setText('INVALID · '+'; '.join(errors)); QMessageBox.warning(self,'Perfil inválido','\n'.join(errors)); return
  digest=sha256_text(self.profile_editor.toPlainText()); self.profile_state.setText(f"VALID · {profile['profile_id']} · SHA-256={digest} · execution=false")
  QMessageBox.information(self,'Perfil válido',f"VALID\nprofile_id={profile['profile_id']}\nSHA-256={digest}\nNo se ejecutó producción ni renderer.")

 def show_profile_diff(self):
  now=self.profile_editor.toPlainText().splitlines(True); old=self.profile_base_text.splitlines(True)
  diff=''.join(difflib.unified_diff(old,now,fromfile='SAVED/BASE',tofile='EDITOR',lineterm='')) or 'Sin diferencias.'
  if len(diff)>22000:diff=diff[:22000]+'\n... diff recortado ...'
  QMessageBox.information(self,'Diff del perfil',diff)

 def save_profile(self):
  profile,errors=self.current_profile()
  if errors:QMessageBox.warning(self,'Guardar bloqueado','No se escribió ningún archivo.\n\n'+'\n'.join(errors)); return
  try:target=profile_path(PROJECT_ROOT,profile['profile_id'])
  except Exception as exc:QMessageBox.critical(self,'Ruta de perfil',str(exc)); return
  if self.profile_file is not None and target!=self.profile_file.resolve():QMessageBox.warning(self,'Identidad','No se permite cambiar profile_id del archivo cargado. Crea un perfil nuevo.'); return
  question=f"Guardar perfil operativo?\n{target.relative_to(PROJECT_ROOT)}\n\n"+('Se creará backup .bak.' if target.exists() else 'Se creará un archivo nuevo.')
  if QMessageBox.question(self,'Confirmar escritura',question)!=QMessageBox.Yes:return
  try: target=save_operator_profile(PROJECT_ROOT,profile,allow_overwrite=target.exists(),expected_profile_id=target.stem)
  except Exception as exc:QMessageBox.critical(self,'Guardar perfil',str(exc)); return
  payload=target.read_text(encoding='utf-8-sig')
  self.profile_file=target; self.profile_base_text=payload; self.profile_editor.setPlainText(payload); self.profile_state.setText(f"GUARDADO · {target.relative_to(PROJECT_ROOT)} · SHA-256={sha256_text(payload)}")
  self.refresh_profiles(); index=self.profile_combo.findData(str(target))
  if index>=0:self.profile_combo.setCurrentIndex(index)
  QMessageBox.information(self,'Perfil guardado','Guardado explícitamente. Runtime/renderer/production/release siguen desactivados.')

 def restore_profile_backup(self):
  if self.profile_file is None or not self.profile_file.exists():QMessageBox.information(self,'Backup','Carga primero un perfil guardado.'); return
  backup=Path(str(self.profile_file)+'.bak')
  if not backup.is_file():QMessageBox.warning(self,'Backup','No existe backup .bak.'); return
  try:candidate=json.loads(backup.read_text(encoding='utf-8-sig'))
  except Exception as exc:QMessageBox.critical(self,'Backup',f'Backup JSON inválido.\n{exc}'); return
  errors=validate_operator_profile(candidate,PROJECT_ROOT,self.profile_file.stem)
  if errors:QMessageBox.critical(self,'Backup','Backup inválido; no se restaura.\n'+'\n'.join(errors)); return
  if QMessageBox.question(self,'Restaurar backup',f'Restaurar {backup.relative_to(PROJECT_ROOT)}?\nEl estado actual se respaldará antes de restaurar.')!=QMessageBox.Yes:return
  try:restore_operator_profile_backup(PROJECT_ROOT,self.profile_file.stem,authorized=True)
  except Exception as exc:QMessageBox.critical(self,'Restaurar backup',str(exc)); return
  self.profile_base_text=self.profile_file.read_text(encoding='utf-8-sig'); self.profile_editor.setPlainText(self.profile_base_text); self.profile_state.setText('RESTAURADO · SHA-256='+sha256_text(self.profile_base_text)); self.refresh_profiles()

 def open_profile_folder(self):open_path((PROJECT_ROOT/'profiles/c11d/operator').resolve())

if __name__=='__main__':
 app=QApplication(sys.argv); app.setStyleSheet(CYBER_STYLE); window=Window(); window.show(); sys.exit(app.exec())
