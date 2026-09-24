from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QSpinBox,QPushButton,QPlainTextEdit,QFormLayout,QGroupBox
class ReproductionPage(QWidget):
 def __init__(self,ctx,families,cb,parent=None):
  super().__init__(parent);self.cb=cb;root=QVBoxLayout(self);t=QLabel("Reproducibility");t.setObjectName("PageTitle");root.addWidget(t);g=QGroupBox("Exact prototype reproduction");f=QFormLayout(g);self.family=QComboBox();self.seed=QSpinBox();self.seed.setRange(1,2147483646);self.seed.setValue(271828);self.build=QPushButton("BUILD COMMAND");self.cmd=QPlainTextEdit();self.cmd.setReadOnly(True);[self.family.addItem(x.artistic+" ("+x.technical+")",x.folder) for x in families];f.addRow("Family",self.family);f.addRow("Seed",self.seed);f.addRow(self.build);root.addWidget(g);root.addWidget(self.cmd,1);self.build.clicked.connect(self._build)
 def _build(self):self.cmd.setPlainText(self.cb.reproduce_prototype(self.family.currentData(),self.seed.value()).display_command)
