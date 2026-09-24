from PySide6.QtWidgets import QFrame,QVBoxLayout,QLabel
class StatusCard(QFrame):
 def __init__(self,title,value,meta="",parent=None):
  super().__init__(parent);self.setStyleSheet("QFrame{background:#10151e;border:1px solid #263247;border-radius:9px;}");v=QVBoxLayout(self);a=QLabel(title.upper());a.setStyleSheet("color:#7f93aa;font-size:9pt;");self.value=QLabel(value);self.value.setStyleSheet("font-size:15pt;font-weight:700;");self.meta=QLabel(meta);self.meta.setStyleSheet("color:#5fcaff;");v.addWidget(a);v.addWidget(self.value);v.addWidget(self.meta)
 def set(self,value,meta=None):self.value.setText(str(value));self.meta.setText(str(meta if meta is not None else self.meta.text()))
