from __future__ import annotations
import os, sys, json, shutil, subprocess, tempfile
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QPushButton, QComboBox,
    QPlainTextEdit, QTabWidget, QSplitter)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import PROJECT_ROOT, CYBER_STYLE, human_size, open_path
from c11d_catalog import build_catalog_data, CATALOG_INTEGRATION_VERSION

CATALOG_VERSION = "0.2.0"
MEDIA={'.mp4':'VIDEO','.avi':'VIDEO','.gif':'VIDEO','.png':'IMAGE','.jpg':'IMAGE','.jpeg':'IMAGE','.webp':'IMAGE','.wav':'AUDIO','.mp3':'AUDIO'}

class Window(QMainWindow):
  def __init__(self):
    super().__init__(); self.setWindowTitle('C11-C / C11-D CATALOG 0.2.0'); self.resize(1500,880); self.rows=[]; self.d_records=[]; self.d_selected=None
    root=QWidget(); self.setCentralWidget(root); outer=QVBoxLayout(root)
    title=QLabel('CATALOG / ARTIFACTS + C11-D PRODUCT RECORDS'); title.setObjectName('title'); outer.addWidget(title)
    self.tabs=QTabWidget(); outer.addWidget(self.tabs,1)
    self._build_artifact_browser()
    self._build_d_product_view()
    self.scan(); self.refresh_d_products()

  def _build_artifact_browser(self):
    page=QWidget(); lay=QVBoxLayout(page)
    top=QHBoxLayout(); lay.addLayout(top); self.search=QLineEdit(); self.search.setPlaceholderText('Buscar artefacto...'); self.search.textChanged.connect(self.refresh); top.addWidget(self.search); self.kind=QComboBox(); self.kind.addItems(['ALL','VIDEO','IMAGE','AUDIO','JSON','TEXT','OTHER']); self.kind.currentTextChanged.connect(self.refresh); top.addWidget(self.kind); b=QPushButton('REFRESCAR ARTIFACTOS'); b.clicked.connect(self.scan); top.addWidget(b)
    body=QHBoxLayout(); lay.addLayout(body,1)
    self.table=QTableWidget(0,5); self.table.setHorizontalHeaderLabels(['Tipo','Artefacto','Tamaño','Modificado','Ruta']); self.table.setSelectionBehavior(QTableWidget.SelectRows); self.table.itemSelectionChanged.connect(self.show_selected); body.addWidget(self.table,3)
    side=QVBoxLayout(); body.addLayout(side,2); self.thumb=QLabel('SIN PREVIEW'); self.thumb.setAlignment(Qt.AlignCenter); self.thumb.setMinimumSize(320,240); side.addWidget(self.thumb); self.info=QPlainTextEdit(); self.info.setReadOnly(True); side.addWidget(self.info,1); self.open=QPushButton('ABRIR EN EXPLORADOR'); self.open.clicked.connect(self.open_selected); side.addWidget(self.open)
    self.tabs.addTab(page, 'ARTIFACT BROWSER')

  def _build_d_product_view(self):
    page=QWidget(); lay=QVBoxLayout(page)
    top=QHBoxLayout(); lay.addLayout(top)
    self.d_summary=QLabel('C11-D catalog records'); self.d_summary.setObjectName('muted'); top.addWidget(self.d_summary,2)
    self.d_filter=QComboBox(); self.d_filter.addItems(['ALL RECORDS','CANONICAL INTENT','PRODUCER PLAN','PILOT MEDIA']); self.d_filter.currentTextChanged.connect(self.refresh_d_table); top.addWidget(self.d_filter)
    b=QPushButton('REFRESCAR D'); b.clicked.connect(self.refresh_d_products); top.addWidget(b)
    split=QSplitter(Qt.Horizontal); lay.addWidget(split,1)
    self.d_table=QTableWidget(0,8); self.d_table.setHorizontalHeaderLabels(['Tipo','ID / Challenge','Estado','Gameplay seed','Music seed','Delivery','Personalización','Media / Hash']); self.d_table.setSelectionBehavior(QTableWidget.SelectRows); self.d_table.setSelectionMode(QTableWidget.SingleSelection); self.d_table.itemSelectionChanged.connect(self.show_d_selected); split.addWidget(self.d_table)
    detail=QWidget(); side=QVBoxLayout(detail); self.d_detail=QPlainTextEdit(); self.d_detail.setReadOnly(True); side.addWidget(self.d_detail,1)
    controls=QHBoxLayout(); side.addLayout(controls); self.d_open=QPushButton('ABRIR EVIDENCIA / MEDIA'); self.d_open.clicked.connect(self.open_d_evidence); controls.addWidget(self.d_open); self.d_copy=QPushButton('COPIAR COMANDO CANÓNICO'); self.d_copy.clicked.connect(self.copy_d_command); controls.addWidget(self.d_copy)
    split.addWidget(detail); split.setSizes([900,500]); self.tabs.addTab(page, 'C11-D PRODUCTS / PROVENANCE')

  def scan(self):
    base=PROJECT_ROOT/'artifacts'; self.rows=[]
    if base.exists():
      for p in base.rglob('*'):
        if p.is_file():
          ext=p.suffix.lower(); typ=MEDIA.get(ext, 'JSON' if ext=='.json' else 'TEXT' if ext in {'.txt','.log','.md','.csv'} else 'OTHER')
          try: size=p.stat().st_size; mt=p.stat().st_mtime
          except OSError: continue
          self.rows.append((p,typ,size,mt))
    self.refresh()

  def refresh(self):
    q=self.search.text().lower().strip(); k=self.kind.currentText(); visible=[r for r in self.rows if (not q or q in str(r[0]).lower()) and (k=='ALL' or r[1]==k)]
    self.table.setRowCount(len(visible))
    for i,(p,t,s,m) in enumerate(sorted(visible,key=lambda x:str(x[0]).lower())):
      vals=[t,p.name,human_size(s),__import__('datetime').datetime.fromtimestamp(m).strftime('%Y-%m-%d %H:%M'),str(p.relative_to(PROJECT_ROOT))]
      for j,v in enumerate(vals): self.table.setItem(i,j,QTableWidgetItem(v))

  def selected(self):
    r=self.table.currentRow()
    if r<0:return None
    rel=self.table.item(r,4).text(); return PROJECT_ROOT/rel

  def show_selected(self):
    p=self.selected(); self.thumb.clear(); self.thumb.setText('SIN PREVIEW'); self.info.clear()
    if not p:return
    ext=p.suffix.lower(); text=[]
    try: stat=p.stat(); text += [f'PATH: {p.relative_to(PROJECT_ROOT)}',f'SIZE: {human_size(stat.st_size)}',f'MODIFIED: {__import__("datetime").datetime.fromtimestamp(stat.st_mtime).isoformat()}']
    except OSError: pass
    if ext in {'.json','.txt','.md','.log','.csv'}:
      try:
        raw=p.read_text(encoding='utf-8',errors='replace')
        if ext=='.json':
          try: text.append(json.dumps(json.loads(raw),ensure_ascii=False,indent=2))
          except Exception: text.append(raw[:50000])
        else:text.append(raw[:50000])
      except Exception as e:text.append(str(e))
    elif ext in {'.png','.jpg','.jpeg','.webp'}:
      pm=QPixmap(str(p)); self.thumb.setPixmap(pm.scaled(self.thumb.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)); text.append(f'IMAGE: {pm.width()}×{pm.height()}')
    elif ext in {'.mp4','.avi','.gif'}:
      text += self.probe(p); self.make_video_thumb(p)
    elif ext in {'.wav','.mp3'}:
      text += self.probe(p)
    self.info.setPlainText('\n'.join(text))

  def probe(self,p):
    if not shutil.which('ffprobe'): return ['ffprobe: NO DISPONIBLE']
    r=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],capture_output=True,text=True)
    if r.returncode!=0:return [r.stderr]
    try:return [json.dumps(json.loads(r.stdout),ensure_ascii=False,indent=2)]
    except:return [r.stdout[:50000]]

  def make_video_thumb(self,p):
    if not shutil.which('ffmpeg'): return
    tmp=Path(tempfile.gettempdir())/'c11c_catalog_thumb.png'
    r=subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss','1','-i',str(p),'-frames:v','1','-vf','scale=480:-1',str(tmp)],capture_output=True)
    if r.returncode==0 and tmp.exists():
      pm=QPixmap(str(tmp)); self.thumb.setPixmap(pm.scaled(self.thumb.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))

  def open_selected(self):
    p=self.selected()
    if p: open_path(p.parent)

  def refresh_d_products(self):
    result=build_catalog_data(PROJECT_ROOT); self.d_records=result['records']; self.d_issues=result['issues']; self.d_source_status=result['source_status']; self.refresh_d_table()
    s=result['summary']; self.d_summary.setText(f"D Catalog {CATALOG_VERSION} · intents={s['canonical_intents']} · plans={s['producer_plans']} · pilot media={s['pilot_media']} · release products={s['release_products']} · release authority=NONE")
    details={"summary":s,"source_status":self.d_source_status,"issues":self.d_issues,"policy":{"mode":"EXPLICIT RECEIPTS / HASH-VERIFIED MEDIA","D7":"canonical intent only; not executed media","D9.4 media":"validation pilot only; not release eligible","D9.5.1":"plan only; D4.8 remains BLOCKED","release_authority":"NONE"}}
    if not self.d_table.currentRow() >= 0:
      self.d_detail.setPlainText(json.dumps(details,ensure_ascii=False,indent=2))

  def refresh_d_table(self):
    if not hasattr(self,'d_records'): return
    choice=self.d_filter.currentText() if hasattr(self,'d_filter') else 'ALL RECORDS'
    type_map={'CANONICAL INTENT':'CANONICAL_INTENT','PRODUCER PLAN':'PRODUCER_PLAN','PILOT MEDIA':'PILOT_MEDIA'}
    visible=[r for r in self.d_records if choice=='ALL RECORDS' or r['record_type']==type_map.get(choice)]
    self.d_table.setRowCount(len(visible))
    for i,r in enumerate(visible):
      file_hash=r.get('media_sha256') or r.get('plan_hash') or r.get('identity_hash') or r.get('request_hash') or ''
      media=(r.get('media_path') or 'NO MEDIA')
      if file_hash: media += ' · ' + file_hash[:12]
      vals=[r.get('record_type',''),f"{r.get('record_id','')} / {r.get('challenge_id','')}",r.get('status',''),r.get('gameplay_seed',''),r.get('music_seed',''),r.get('delivery_profile_id',''),r.get('personalization_profile',''),media]
      for j,v in enumerate(vals):
        item=QTableWidgetItem(str(v)); item.setData(Qt.UserRole,i); self.d_table.setItem(i,j,item)
    self.d_table.resizeColumnsToContents()
    self.d_selected=None
    self.d_open.setEnabled(False); self.d_copy.setEnabled(False)
    self.d_detail.setPlainText('Selecciona un registro para inspeccionar identidad, hashes, provenance y comando reproducible.')

  def show_d_selected(self):
    row=self.d_table.currentRow()
    if row<0: self.d_selected=None; self.d_open.setEnabled(False); self.d_copy.setEnabled(False); return
    item=self.d_table.item(row,0)
    if item is None: return
    index=item.data(Qt.UserRole)
    # Resolve the row against the filtered view, not the full record list.
    choice=self.d_filter.currentText(); type_map={'CANONICAL INTENT':'CANONICAL_INTENT','PRODUCER PLAN':'PRODUCER_PLAN','PILOT MEDIA':'PILOT_MEDIA'}
    visible=[r for r in self.d_records if choice=='ALL RECORDS' or r['record_type']==type_map.get(choice)]
    if not isinstance(index,int) or index<0 or index>=len(visible): return
    self.d_selected=visible[index]
    data=dict(self.d_selected); data.pop('search_text',None)
    self.d_detail.setPlainText(json.dumps(data,ensure_ascii=False,indent=2))
    self.d_open.setEnabled(bool(self.d_selected.get('evidence_path') or self.d_selected.get('media_path')))
    self.d_copy.setEnabled(bool(self.d_selected.get('reproduction_command')))

  def open_d_evidence(self):
    if not self.d_selected:return
    raw=self.d_selected.get('media_path') or self.d_selected.get('evidence_path')
    if not raw:return
    p=(PROJECT_ROOT/raw).resolve()
    try:p.relative_to(PROJECT_ROOT.resolve())
    except ValueError:return
    target=p.parent if p.is_file() else p
    if target.exists():open_path(target)

  def copy_d_command(self):
    if not self.d_selected:return
    command=self.d_selected.get('reproduction_command')
    if command: QApplication.clipboard().setText(command); self.statusBar().showMessage('Comando canónico copiado; no se ha ejecutado.')

if __name__=='__main__':
  app=QApplication(sys.argv); app.setStyleSheet(CYBER_STYLE); w=Window(); w.show(); sys.exit(app.exec())
