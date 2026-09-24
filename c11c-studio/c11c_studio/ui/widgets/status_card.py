from PySide6.QtWidgets import QFrame,QVBoxLayout,QHBoxLayout,QLabel

class StatusCard(QFrame):
 def __init__(self,title,value,meta="",parent=None):
  super().__init__(parent);self.setObjectName("StatusCard")
  v=QVBoxLayout(self);v.setContentsMargins(15,13,15,13);v.setSpacing(3)
  row=QHBoxLayout();row.setSpacing(6);a=QLabel(title.upper());a.setObjectName("CardLabel");row.addWidget(a);row.addStretch(1);self.dot=QLabel("●");self.dot.setObjectName("CardDot");row.addWidget(self.dot);v.addLayout(row)
  self.value=QLabel(str(value));self.value.setObjectName("CardValue");v.addWidget(self.value)
  self.meta=QLabel(str(meta));self.meta.setObjectName("CardMeta");self.meta.setWordWrap(True);v.addWidget(self.meta)
 def set(self,value,meta=None):self.value.setText(str(value));self.meta.setText(str(meta if meta is not None else self.meta.text()))
