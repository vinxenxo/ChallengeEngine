from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QTableWidget,QTableWidgetItem,QHeaderView
from ..widgets.status_card import StatusCard
class DashboardPage(QWidget):
 def __init__(self,ctx,tools,parent=None):
  super().__init__(parent); self.ctx=ctx; root=QVBoxLayout(self);root.setContentsMargins(24,20,24,20);title=QLabel("Dashboard");title.setObjectName("PageTitle");root.addWidget(title);sub=QLabel("C11-C Studio — control surface for the deterministic visual production toolchain");sub.setObjectName("PageSubtitle");root.addWidget(sub)
  cards=QHBoxLayout();self.backend=StatusCard("Backend",ctx.backend_version,ctx.backend_version_source);self.godot=StatusCard("Godot",tools["godot"].version or "missing","READY" if tools["godot"].present else "WARN");self.delivery=StatusCard("Delivery",f"{ctx.delivery_width}×{ctx.delivery_height}",f"{ctx.fps} FPS · {ctx.default_duration:.2f}s");self.families=StatusCard("Families","5","canonical/discovered");self.review=StatusCard("Review","0");self.prod=StatusCard("Production","0")
  for c in (self.backend,self.godot,self.delivery,self.families,self.review,self.prod):cards.addWidget(c)
  root.addLayout(cards);row=QHBoxLayout();self.btn_validate=QPushButton("VALIDATE");self.btn_validate.setProperty("class","Primary");self.btn_review=QPushButton("REVIEW 5×5");self.btn_review.setProperty("class","Primary");self.btn_produce=QPushButton("PRODUCE 5×5");self.btn_produce.setProperty("class","Primary");self.btn_single=QPushButton("PRODUCE SINGLE");self.btn_open_prod=QPushButton("OPEN PRODUCTION");self.btn_open_review=QPushButton("OPEN REVIEW")
  for b in (self.btn_validate,self.btn_review,self.btn_produce,self.btn_single,self.btn_open_prod,self.btn_open_review):row.addWidget(b)
  row.addStretch(1);root.addLayout(row);root.addWidget(QLabel("Recent jobs"));self.table=QTableWidget(0,7);self.table.setHorizontalHeaderLabels(["Time","Type","Family","Seed(s)","Stage","State","Job"]);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);root.addWidget(self.table,1)
 def set_counts(self,prod,review,fam):self.prod.set(prod);self.review.set(review);self.families.set(fam)
 def add_job(self,*vals):
  r=self.table.rowCount();self.table.insertRow(r)
  for c,v in enumerate(vals):self.table.setItem(r,c,QTableWidgetItem(str(v)))
