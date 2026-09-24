from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTableWidget,QTableWidgetItem,QHeaderView,QPushButton,QHBoxLayout
class JobsPage(QWidget):
 def __init__(self,jm,parent=None):
  super().__init__(parent);self.jm=jm;root=QVBoxLayout(self);t=QLabel("Jobs");t.setObjectName("PageTitle");root.addWidget(t);self.table=QTableWidget(0,9);self.table.setHorizontalHeaderLabels(["Job","Type","Family","Seed","Stage","State","Progress","Exit","Log"]);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);root.addWidget(self.table,1);row=QHBoxLayout();self.cancel=QPushButton("CANCEL CURRENT");self.open_log=QPushButton("OPEN LOG");row.addWidget(self.cancel);row.addWidget(self.open_log);root.addLayout(row);self.cancel.clicked.connect(jm.cancel_current);self.open_log.clicked.connect(self._open);jm.job_started.connect(lambda *_:self.refresh());jm.job_state_changed.connect(lambda *_:self.refresh());jm.job_finished.connect(lambda *_:self.refresh());self.refresh()
 def refresh(self):
  self.table.setRowCount(0)
  for j in self.jm.jobs.values():
   r=self.table.rowCount();self.table.insertRow(r);vals=[j.id,j.job_type,j.family or "—",j.seed or "—",j.stage,j.state.value,j.progress,j.exit_code if j.exit_code is not None else "—",str(j.log_path)]
   for c,v in enumerate(vals):self.table.setItem(r,c,QTableWidgetItem(str(v)))
 def _open(self):
  r=self.table.currentRow();
  if r<0:return
  p=self.table.item(r,8).text();QDesktopServices.openUrl(QUrl.fromLocalFile(p))
