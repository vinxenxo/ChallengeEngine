from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QHeaderView,QPushButton,QHBoxLayout,QTextBrowser
from PySide6.QtCore import Signal
class FamiliesPage(QWidget):
 request_review=Signal(str);request_open=Signal(str)
 def __init__(self,families,parent=None):
  super().__init__(parent);self.families=families;root=QVBoxLayout(self);t=QLabel("Families");t.setObjectName("PageTitle");root.addWidget(t);self.table=QTableWidget(0,8);self.table.setHorizontalHeaderLabels(["Art","Technical","ID","Grammars","Parameters","Palettes","Capabilities","Launcher"]);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);root.addWidget(self.table,1);row=QHBoxLayout();self.btn_review=QPushButton("REVIEW SELECTED");self.btn_open=QPushButton("OPEN FOLDER");row.addWidget(self.btn_review);row.addWidget(self.btn_open);root.addLayout(row);self.btn_review.clicked.connect(self._review);self.btn_open.clicked.connect(self._open);self.refresh()
 def refresh(self):
  self.table.setRowCount(0)
  for f in self.families:
   r=self.table.rowCount();self.table.insertRow(r);vals=[f.artistic,f.technical,f.id,", ".join(f.grammars) or "backend/seed derived",len(f.parameters),len(f.palettes),", ".join(sorted(f.capabilities)) or "—",str(f.launcher_path or "—")]
   for c,v in enumerate(vals):self.table.setItem(r,c,QTableWidgetItem(str(v)))
 def _selected(self):
  r=self.table.currentRow();return self.families[r] if 0<=r<len(self.families) else None
 def _review(self):
  f=self._selected()
  if f:self.request_review.emit(f.folder)
 def _open(self):
  f=self._selected()
  if f:self.request_open.emit(f.folder)
