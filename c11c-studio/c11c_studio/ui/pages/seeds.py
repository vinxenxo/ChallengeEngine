from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QHBoxLayout,QSpinBox,QLineEdit,QPushButton,QTableWidget,QTableWidgetItem,QHeaderView,QMessageBox
class SeedsPage(QWidget):
 def __init__(self,manager,parent=None):
  super().__init__(parent);self.manager=manager;root=QVBoxLayout(self);t=QLabel("Seeds");t.setObjectName("PageTitle");root.addWidget(t);row=QHBoxLayout();self.count=QSpinBox();self.count.setRange(1,25);self.count.setValue(5);self.manual=QLineEdit();self.manual.setPlaceholderText("Manual seeds, comma-separated");self.random=QPushButton("GENERATE RANDOM");self.add=QPushButton("SAVE MANUAL SET");row.addWidget(self.count);row.addWidget(self.manual,2);row.addWidget(self.random);row.addWidget(self.add);root.addLayout(row);self.table=QTableWidget(0,4);self.table.setHorizontalHeaderLabels(["Seed","Source","Batch","Created"]);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);root.addWidget(self.table,1);self.random.clicked.connect(self._random);self.add.clicked.connect(self._manual)
 def _show(self,s):
  self.table.setRowCount(0)
  for seed in s.seeds:
   r=self.table.rowCount();self.table.insertRow(r)
   for c,v in enumerate([seed,s.source,s.batch_id,s.created_at]):self.table.setItem(r,c,QTableWidgetItem(str(v)))
 def _random(self):self._show(self.manager.random_set(self.count.value()))
 def _manual(self):
  try:self._show(self.manager.manual_set([int(x.strip()) for x in self.manual.text().split(",") if x.strip()]))
  except Exception as e:QMessageBox.warning(self,"Seeds",str(e))
