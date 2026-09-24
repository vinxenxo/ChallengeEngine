from PySide6.QtWidgets import QPushButton
class NavButton(QPushButton):
 def __init__(self,text,parent=None):
  super().__init__(text,parent);self.setCheckable(True);self.setMinimumHeight(40);self.setStyleSheet("QPushButton{text-align:left;padding-left:16px;border:0;border-radius:7px;}QPushButton:checked{background:#142638;color:#73dcff;font-weight:700;}QPushButton:hover{background:#111c29;}")
