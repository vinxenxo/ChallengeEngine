from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QLineEdit,QPushButton,QHBoxLayout
from ..widgets.log_view import LogView
class LogsPage(QWidget):
 def __init__(self,jm,parent=None):
  super().__init__(parent);self.jm=jm;root=QVBoxLayout(self);t=QLabel("Log Center");t.setObjectName("PageTitle");root.addWidget(t);row=QHBoxLayout();self.filter=QComboBox();self.filter.addItems(["ALL","STDOUT","STDERR"]);self.search=QLineEdit();self.search.setPlaceholderText("Search current log");self.clear=QPushButton("CLEAR");row.addWidget(self.filter);row.addWidget(self.search,1);row.addWidget(self.clear);root.addLayout(row);self.view=LogView();root.addWidget(self.view,1);self.clear.clicked.connect(self.view.clear);jm.job_output.connect(self._output)
 def _output(self,jid,stream,text):self.view.append_line(text,stream)
