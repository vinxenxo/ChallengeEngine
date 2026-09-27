from __future__ import annotations
import os, sys, json, shutil, subprocess, tempfile
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QPushButton, QComboBox, QPlainTextEdit, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import PROJECT_ROOT, CYBER_STYLE, human_size, open_path

MEDIA={'.mp4':'VIDEO','.avi':'VIDEO','.gif':'VIDEO','.png':'IMAGE','.jpg':'IMAGE','.jpeg':'IMAGE','.webp':'IMAGE','.wav':'AUDIO','.mp3':'AUDIO'}
class Window(QMainWindow):
  def __init__(self):
    super().__init__(); self.setWindowTitle('C11-C CATALOG'); self.resize(1400,820); self.rows=[]
    root=QWidget(); self.setCentralWidget(root); lay=QVBoxLayout(root)
    top=QHBoxLayout(); lay.addLayout(top); title=QLabel('CATALOG'); title.setObjectName('title'); top.addWidget(title); self.search=QLineEdit(); self.search.setPlaceholderText('Buscar artefacto...'); self.search.textChanged.connect(self.refresh); top.addWidget(self.search); self.kind=QComboBox(); self.kind.addItems(['ALL','VIDEO','IMAGE','AUDIO','JSON','TEXT','OTHER']); self.kind.currentTextChanged.connect(self.refresh); top.addWidget(self.kind); b=QPushButton('REFRESCAR'); b.clicked.connect(self.scan); top.addWidget(b)
    body=QHBoxLayout(); lay.addLayout(body,1)
    self.table=QTableWidget(0,5); self.table.setHorizontalHeaderLabels(['Tipo','Artefacto','Tamaño','Modificado','Ruta']); self.table.setSelectionBehavior(QTableWidget.SelectRows); self.table.itemSelectionChanged.connect(self.show_selected); body.addWidget(self.table,3)
    side=QVBoxLayout(); body.addLayout(side,2); self.thumb=QLabel('SIN PREVIEW'); self.thumb.setAlignment(Qt.AlignCenter); self.thumb.setMinimumSize(360,260); side.addWidget(self.thumb); self.info=QPlainTextEdit(); self.info.setReadOnly(True); side.addWidget(self.info,1); self.open=QPushButton('ABRIR EN EXPLORADOR'); self.open.clicked.connect(self.open_selected); side.addWidget(self.open); self.scan()
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
    r=self.table.currentRow();
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
        raw=p.read_text(encoding='utf-8',errors='replace');
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
    tmp=Path(tempfile.gettempdir())/'c11c_catalog_thumb.png';
    r=subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss','1','-i',str(p),'-frames:v','1','-vf','scale=480:-1',str(tmp)],capture_output=True)
    if r.returncode==0 and tmp.exists():
      pm=QPixmap(str(tmp)); self.thumb.setPixmap(pm.scaled(self.thumb.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
  def open_selected(self):
    p=self.selected();
    if p: open_path(p.parent)
if __name__=='__main__':
 app=QApplication(sys.argv); app.setStyleSheet(CYBER_STYLE); w=Window(); w.show(); sys.exit(app.exec())
