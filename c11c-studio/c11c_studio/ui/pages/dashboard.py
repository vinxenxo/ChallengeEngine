from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QLabel,QPushButton,QTableWidget,QTableWidgetItem,QHeaderView,QFrame
from ..widgets.status_card import StatusCard

class DashboardPage(QWidget):
 def __init__(self,ctx,tools,parent=None):
  super().__init__(parent);self.ctx=ctx;root=QVBoxLayout(self);root.setContentsMargins(28,24,28,24);root.setSpacing(16)
  title=QLabel("Dashboard");title.setObjectName("PageTitle");root.addWidget(title)
  sub=QLabel("Your daily control surface for the deterministic visual production pipeline.");sub.setObjectName("PageSubtitle");root.addWidget(sub)

  hero=QFrame();hero.setObjectName("Hero");hv=QVBoxLayout(hero);hv.setContentsMargins(18,16,18,16);hv.setSpacing(10)
  eyebrow=QLabel("QUICK ACTIONS");eyebrow.setObjectName("Eyebrow");hv.addWidget(eyebrow)
  hr=QHBoxLayout();hr.setSpacing(9)
  self.btn_validate=QPushButton("VALIDATE ENVIRONMENT");self.btn_validate.setProperty("class","Primary")
  self.btn_review=QPushButton("NEW REVIEW 5×5");self.btn_review.setProperty("class","Primary")
  self.btn_produce=QPushButton("PRODUCE 5×5");self.btn_produce.setProperty("class","Primary")
  self.btn_single=QPushButton("PRODUCE SINGLE")
  self.btn_open_prod=QPushButton("OPEN PRODUCTION")
  self.btn_open_review=QPushButton("OPEN REVIEW")
  for b in (self.btn_validate,self.btn_review,self.btn_produce,self.btn_single,self.btn_open_prod,self.btn_open_review):hr.addWidget(b)
  hr.addStretch(1);hv.addLayout(hr)
  root.addWidget(hero)

  cards=QGridLayout();cards.setHorizontalSpacing(10);cards.setVerticalSpacing(10)
  self.backend=StatusCard("Backend",ctx.backend_version,ctx.backend_version_source);self.godot=StatusCard("Godot",tools["godot"].version or "missing","READY" if tools["godot"].present else "MISSING");self.delivery=StatusCard("Delivery",f"{ctx.delivery_width}×{ctx.delivery_height}",f"{ctx.fps} FPS · {ctx.default_duration:.2f}s baseline");self.families=StatusCard("Families","5","canonical / discovered");self.review=StatusCard("Review","0","MP4 assets");self.prod=StatusCard("Production","0","published products")
  for pos,c in enumerate((self.backend,self.godot,self.delivery,self.families,self.review,self.prod)):
   cards.addWidget(c,pos//3,pos%3)
  root.addLayout(cards)

  head=QHBoxLayout();lbl=QLabel("Recent jobs");lbl.setObjectName("PanelTitle");head.addWidget(lbl);head.addStretch(1);hint=QLabel("Newest activity appears first");hint.setObjectName("PanelMeta");head.addWidget(hint);root.addLayout(head)
  self.table=QTableWidget(0,7);self.table.setObjectName("RecentJobsTable");self.table.setHorizontalHeaderLabels(["TIME","TYPE","FAMILY","SEED(S)","STAGE","STATE","JOB"]);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch);self.table.setAlternatingRowColors(True);self.table.setMinimumHeight(230);root.addWidget(self.table,1)
 def set_counts(self,prod,review,fam):self.prod.set(prod);self.review.set(review);self.families.set(fam)
 def add_job(self,*vals):
  r=self.table.rowCount();self.table.insertRow(r)
  for c,v in enumerate(vals):self.table.setItem(r,c,QTableWidgetItem(str(v)))
  self.table.scrollToBottom()
