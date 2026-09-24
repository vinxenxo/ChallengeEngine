from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel
class AboutPage(QWidget):
 def __init__(self,ctx,app_version,parent=None):
  super().__init__(parent);v=QVBoxLayout(self);t=QLabel("C11-C Studio");t.setObjectName("PageTitle");v.addWidget(t);info="GUI version: %s\nBackend: %s (%s)\nC11-B: %s\nProject: %s"%(app_version,ctx.backend_version,ctx.backend_version_source,ctx.c11b_state,ctx.project_root);v.addWidget(QLabel(info));v.addStretch(1)
