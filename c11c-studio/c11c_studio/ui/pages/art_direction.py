from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTabWidget,QTableWidget,QTableWidgetItem,QHeaderView,QPushButton,QHBoxLayout,QInputDialog
class ArtDirectionPage(QWidget):
 def __init__(self,ctx,families,snapshot_service,parent=None):
  super().__init__(parent);self.ctx=ctx;self.families=families;self.snapshots=snapshot_service;root=QVBoxLayout(self);t=QLabel("Art Direction Lab");t.setObjectName("PageTitle");root.addWidget(t);root.addWidget(QLabel("Canonical/effective inspection first. Experimental controls are isolated and snapshot-based."));tabs=QTabWidget();
  self.style=QTableWidget(0,7);self.style.setHorizontalHeaderLabels(["Family","Technical","Grammar","Parameters","Palettes","Delivery","State"]);self.style.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);tabs.addTab(self.style,"STYLE BOARD")
  self.params=QTableWidget(0,6);self.params.setHorizontalHeaderLabels(["Family","Parameter","Type","State","Source","Editable"]);self.params.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);tabs.addTab(self.params,"PARAMETERS")
  self.grammar=QTableWidget(0,3);self.grammar.setHorizontalHeaderLabels(["Family","Grammar","Source"]);self.grammar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);tabs.addTab(self.grammar,"GRAMMARS")
  self.palette=QTableWidget(0,3);self.palette.setHorizontalHeaderLabels(["Family","Palette","Source"]);self.palette.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);tabs.addTab(self.palette,"PALETTES")
  root.addWidget(tabs,1);row=QHBoxLayout();self.save=QPushButton("SAVE CONFIG SNAPSHOT");self.open=QPushButton("OPEN SNAPSHOT FOLDER");row.addWidget(self.save);row.addWidget(self.open);root.addLayout(row);self._fill();self.save.clicked.connect(self._save);self.open.clicked.connect(self._open)
 def _fill(self):
  self.style.setRowCount(0);self.params.setRowCount(0);self.grammar.setRowCount(0);self.palette.setRowCount(0)
  for f in self.families:
   r=self.style.rowCount();self.style.insertRow(r)
   for c,v in enumerate((f.artistic,f.technical,", ".join(f.grammars) or "backend/seed derived",len(f.parameters),", ".join(f.palettes) or "backend/seed derived","720×1280 / 30 FPS / 18s baseline","CANONICAL")):self.style.setItem(r,c,QTableWidgetItem(str(v)))
   for p in f.parameters:
    r=self.params.rowCount();self.params.insertRow(r)
    for c,v in enumerate((f.artistic,p.id,p.type,p.state,p.source,str(p.editable))):self.params.setItem(r,c,QTableWidgetItem(str(v)))
   for g in f.grammars:
    r=self.grammar.rowCount();self.grammar.insertRow(r);self.grammar.setItem(r,0,QTableWidgetItem(f.artistic));self.grammar.setItem(r,1,QTableWidgetItem(g));self.grammar.setItem(r,2,QTableWidgetItem("backend/known"))
   for p in f.palettes:
    r=self.palette.rowCount();self.palette.insertRow(r);self.palette.setItem(r,0,QTableWidgetItem(f.artistic));self.palette.setItem(r,1,QTableWidgetItem(p));self.palette.setItem(r,2,QTableWidgetItem("backend"))
 def _save(self):
  name,ok=QInputDialog.getText(self,"Snapshot","Name:")
  if ok:self.snapshots.save({"backend_version":self.ctx.backend_version,"families":[f.folder for f in self.families],"delivery":{"width":self.ctx.delivery_width,"height":self.ctx.delivery_height,"fps":self.ctx.fps,"duration":self.ctx.default_duration}},name or None)
 def _open(self):
  from PySide6.QtGui import QDesktopServices;from PySide6.QtCore import QUrl;self.snapshots.folder.mkdir(parents=True,exist_ok=True);QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.snapshots.folder)))
