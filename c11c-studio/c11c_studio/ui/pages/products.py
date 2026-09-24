from PySide6.QtCore import Qt,QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QHeaderView,QHBoxLayout,QPushButton,QTextBrowser
class ProductsPage(QWidget):
 def __init__(self,catalog,cfg,parent=None):
  super().__init__(parent);self.catalog=catalog;self.cfg=cfg;root=QVBoxLayout(self);t=QLabel("Production Catalog");t.setObjectName("PageTitle");root.addWidget(t);split=QHBoxLayout();self.table=QTableWidget(0,8);self.table.setHorizontalHeaderLabels(["Product","Family","Seed","Duration","Resolution","Audio","Status","Path"]);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);split.addWidget(self.table,2);self.details=QTextBrowser();split.addWidget(self.details,1);root.addLayout(split,1);row=QHBoxLayout();self.refresh_btn=QPushButton("REFRESH");self.open_btn=QPushButton("OPEN");self.play_btn=QPushButton("PLAY");self.manifest_btn=QPushButton("SHOW MANIFEST");row.addWidget(self.refresh_btn);row.addWidget(self.open_btn);row.addWidget(self.play_btn);row.addWidget(self.manifest_btn);root.addLayout(row);self.refresh_btn.clicked.connect(self.refresh);self.table.itemSelectionChanged.connect(self._details);self.open_btn.clicked.connect(self._open);self.play_btn.clicked.connect(self._play);self.manifest_btn.clicked.connect(self._manifest);self.refresh()
 def refresh(self):
  self.products=self.catalog.list_products();self.table.setRowCount(0)
  for p in self.products:
   r=self.table.rowCount();self.table.insertRow(r);m=p.metadata or {};vals=[p.product_id,p.family,p.seed or "—",m.get("duration","—"),m.get("resolution","720x1280"),m.get("audio","—"),p.status,str(p.root)]
   for c,v in enumerate(vals):self.table.setItem(r,c,QTableWidgetItem(str(v)))
 def _selected(self):r=self.table.currentRow();return self.products[r] if 0<=r<len(self.products) else None
 def _details(self):
  p=self._selected()
  if not p:return
  self.details.setPlainText("Product: "+p.product_id+"\nFamily: "+p.family+"\nSeed: "+str(p.seed)+"\nStatus: "+p.status+"\n\n"+"\n".join(f"{k}: {v}" for k,v in (p.metadata or {}).items()))
 def _open(self):
  p=self._selected()
  if p:QDesktopServices.openUrl(QUrl.fromLocalFile(str(p.root)))
 def _play(self):
  p=self._selected()
  if p and p.mp4:QDesktopServices.openUrl(QUrl.fromLocalFile(str(p.mp4)))
 def _manifest(self):
  p=self._selected()
  if p and p.manifest:QDesktopServices.openUrl(QUrl.fromLocalFile(str(p.manifest)))
