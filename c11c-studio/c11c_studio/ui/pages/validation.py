from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QHBoxLayout,QTableWidget,QTableWidgetItem,QHeaderView
class ValidationPage(QWidget):
 request=Signal(str)
 def __init__(self,parent=None):
  super().__init__(parent);root=QVBoxLayout(self);t=QLabel("Validation Center");t.setObjectName("PageTitle");root.addWidget(t);row=QHBoxLayout();self.all=QPushButton("RUN ALL LOCAL CHECKS");self.ps=QPushButton("POWERSHELL PARSE");self.delivery=QPushButton("DELIVERY CONFIG");self.preflight=QPushButton("PREFLIGHT");
  for b in (self.all,self.ps,self.delivery,self.preflight):row.addWidget(b)
  root.addLayout(row);self.table=QTableWidget(0,3);self.table.setHorizontalHeaderLabels(["Check","Status","Message"]);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);root.addWidget(self.table,1);self.all.clicked.connect(lambda:self.request.emit("local"));self.ps.clicked.connect(lambda:self.request.emit("powershell"));self.delivery.clicked.connect(lambda:self.request.emit("delivery"));self.preflight.clicked.connect(lambda:self.request.emit("preflight"))
 def show_report(self,rep):
  self.table.setRowCount(0)
  for c in rep.checks:
   r=self.table.rowCount();self.table.insertRow(r)
   for col,v in enumerate((c.name,c.status,c.message)):self.table.setItem(r,col,QTableWidgetItem(str(v)))
