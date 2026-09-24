from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QHeaderView,QPushButton,QHBoxLayout,QMessageBox
class ArtifactsPage(QWidget):
 request_cleanup=Signal(bool);request_reset=Signal()
 def __init__(self,registry,parent=None):
  super().__init__(parent);self.registry=registry;root=QVBoxLayout(self);t=QLabel("Artifacts");t.setObjectName("PageTitle");root.addWidget(t);root.addWidget(QLabel("Production/evidence roots are protected. Cleanup is always explicit."));self.table=QTableWidget(0,5);self.table.setHorizontalHeaderLabels(["Root","Protection","Files","Size","Path"]);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);root.addWidget(self.table,1);row=QHBoxLayout();self.refresh_btn=QPushButton("REFRESH");self.dry=QPushButton("PREVIEW CLEANUP");self.apply=QPushButton("CLEAN REGENERABLE");self.reset=QPushButton("RESET C11-C WORKSPACE");row.addWidget(self.refresh_btn);row.addWidget(self.dry);row.addWidget(self.apply);row.addWidget(self.reset);root.addLayout(row);self.refresh_btn.clicked.connect(self.refresh);self.dry.clicked.connect(lambda:self.request_cleanup.emit(False));self.apply.clicked.connect(self._apply);self.reset.clicked.connect(self._reset);self.refresh()
 def refresh(self):
  self.table.setRowCount(0)
  for x in self.registry.roots():
   r=self.table.rowCount();self.table.insertRow(r);vals=[x.label,x.protection,str(x.file_count),f"{x.size_bytes/1048576:.1f} MB",str(x.path)]
   for c,v in enumerate(vals):self.table.setItem(r,c,QTableWidgetItem(str(v)))
 def _apply(self):
  if QMessageBox.warning(self,"Confirm","Clean only regenerable prototype media? Production/evidence are outside the cleaner scope.",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)==QMessageBox.Yes:self.request_cleanup.emit(True)
 def _reset(self):
  if QMessageBox.warning(self,"Confirm reset","Reset the complete C11-C regenerable workspace? This must not touch production/evidence.",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)==QMessageBox.Yes:self.request_reset.emit()
