from pathlib import Path
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QHeaderView
class GamesPage(QWidget):
 def __init__(self,ctx,parent=None):
  super().__init__(parent);self.ctx=ctx;root=QVBoxLayout(self);t=QLabel("Challenge Engine / Games & Visual Drills");t.setObjectName("PageTitle");root.addWidget(t);root.addWidget(QLabel("Read-only where mechanics are frozen; runtime discovery only."));self.table=QTableWidget(0,5);self.table.setHorizontalHeaderLabels(["Type","ID","Source","Status","Protection"]);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);root.addWidget(self.table,1);self._scan()
 def _scan(self):
  ch=self.ctx.project_root/"challenges"
  if ch.exists():
   for p in sorted(ch.rglob("*.json")):
    if "challenge" in p.stem.lower():self._add("CHALLENGE",p.stem,str(p),"DISCOVERED","FROZEN CORE")
  profiles=self.ctx.project_root/"profiles"
  for name in ("tracking","pursuit","saccade","peripheral_scan"):
   hits=list(profiles.rglob(f"*{name}*")) if profiles.exists() else []
   if hits:self._add("VISUAL DRILL",name,str(hits[0]),"DISCOVERED","MECHANIC PROTECTED")
 def _add(self,*vals):
  r=self.table.rowCount();self.table.insertRow(r)
  for c,v in enumerate(vals):self.table.setItem(r,c,QTableWidgetItem(str(v)))
