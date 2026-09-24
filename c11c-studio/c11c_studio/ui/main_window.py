from datetime import datetime
from pathlib import Path
from PySide6.QtCore import QTimer,QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMainWindow,QWidget,QHBoxLayout,QVBoxLayout,QLabel,QFrame,QStackedWidget,QStatusBar,QMessageBox
from ..services.tool_discovery import discover_all
from ..services.introspection import BackendIntrospector
from ..services.family_registry import FamilyRegistry
from ..services.seed_manager import SeedManager
from ..services.command_builder import CommandBuilder
from ..services.job_manager import JobManager
from ..services.artifact_registry import ArtifactRegistry
from ..services.product_catalog import ProductCatalog
from ..services.snapshot import SnapshotService
from ..services.environment_validator import EnvironmentValidator
from .widgets.nav_button import NavButton
from .pages.dashboard import DashboardPage
from .pages.review import ReviewPage
from .pages.production import ProductionPage
from .pages.families import FamiliesPage
from .pages.seeds import SeedsPage
from .pages.products import ProductsPage
from .pages.artifacts import ArtifactsPage
from .pages.jobs import JobsPage
from .pages.logs import LogsPage
from .pages.validation import ValidationPage
from .pages.settings import SettingsPage
from .pages.art_direction import ArtDirectionPage
from .pages.games import GamesPage
from .pages.reproduction import ReproductionPage
from .pages.about import AboutPage

class MainWindow(QMainWindow):
 def __init__(self,ctx,cfg,app_version="0.2.1"):
  super().__init__();self.ctx=ctx;self.cfg=cfg;self.app_version=app_version;self.tools=discover_all(ctx.project_root,cfg.get("tool_paths",{}));ctx.powershell_path=self.tools["powershell"].path;ctx.python_path=self.tools["python"].path;ctx.ffmpeg_path=self.tools["ffmpeg"].path;ctx.ffprobe_path=self.tools["ffprobe"].path;ctx.godot_path=self.tools["godot"].path;ctx.godot_version=self.tools["godot"].version
  self.introspector=BackendIntrospector(ctx);catalog=self.introspector.scan();self.families=FamilyRegistry(ctx,self.introspector).load();self.commands=CommandBuilder(ctx,catalog);self.seeds=SeedManager(ctx.paths.gui_workspace/"seeds");self.job_manager=JobManager(ctx.paths.gui_logs);self.registry=ArtifactRegistry(ctx);self.products_catalog=ProductCatalog(ctx);self.snapshots=SnapshotService(ctx.paths.gui_snapshots)
  self._build();self._wire();self._refresh_counts();self.timer=QTimer(self);self.timer.timeout.connect(self._refresh_counts);self.timer.start(15000)
 def _build(self):
  self.setWindowTitle("C11-C Studio — "+self.ctx.project_root.name);self.resize(1480,920);self.setMinimumSize(1120,720);self.setStatusBar(QStatusBar());self.statusBar().showMessage("Ready");central=QWidget();self.setCentralWidget(central);root=QVBoxLayout(central);root.setContentsMargins(0,0,0,0);root.addWidget(self._top());body=QHBoxLayout();body.setContentsMargins(0,0,0,0);body.addWidget(self._nav());self.stack=QStackedWidget();body.addWidget(self.stack,1);w=QWidget();w.setLayout(body);root.addWidget(w,1)
  self.dashboard=DashboardPage(self.ctx,self.tools);self.review=ReviewPage(self.families);self.production=ProductionPage(self.families);self.art=ArtDirectionPage(self.ctx,self.families,self.snapshots);self.families_page=FamiliesPage(self.families);self.seeds_page=SeedsPage(self.seeds);self.products=ProductsPage(self.products_catalog,self.cfg);self.artifacts=ArtifactsPage(self.registry);self.jobs=JobsPage(self.job_manager);self.logs=LogsPage(self.job_manager);self.validation=ValidationPage();self.games=GamesPage(self.ctx);self.repro=ReproductionPage(self.ctx,self.families,self.commands);self.settings=SettingsPage(self.ctx,self.cfg);self.about=AboutPage(self.ctx,self.app_version)
  self.pages=[self.dashboard,self.review,self.production,self.art,self.families_page,self.seeds_page,self.products,self.artifacts,self.jobs,self.logs,self.validation,self.games,self.repro,self.settings,self.about]
  [self.stack.addWidget(p) for p in self.pages]
 def _top(self):
  b=QFrame();b.setObjectName("TopBar");b.setFixedHeight(58);h=QHBoxLayout(b);h.setContentsMargins(16,8,16,8);t=QLabel("C11-C Studio");t.setObjectName("TopBarTitle");h.addWidget(t);meta=QLabel(f"{self.ctx.backend_version} · C11-B {self.ctx.c11b_state} · {self.ctx.delivery_width}×{self.ctx.delivery_height} · {self.ctx.fps} FPS");meta.setObjectName("TopBarMeta");h.addWidget(meta);h.addStretch(1);h.addWidget(QLabel(str(self.ctx.project_root)));return b
 def _nav(self):
  r=QFrame();r.setObjectName("NavRail");r.setFixedWidth(220);v=QVBoxLayout(r);labels=["Dashboard","Review Lab","Production","Art Direction","Families","Seeds","Products","Artifacts","Jobs","Logs","Validation","Games / Drills","Reproduction","Settings","About"];self.nav=[]
  for i,label in enumerate(labels):b=NavButton(label);b.clicked.connect(lambda _=False,j=i:self._goto(j));v.addWidget(b);self.nav.append(b)
  v.addStretch(1);self.nav[0].setChecked(True);return r
 def _wire(self):
  self.dashboard.btn_validate.clicked.connect(lambda:self._goto(10));self.dashboard.btn_review.clicked.connect(lambda:self._goto(1));self.dashboard.btn_produce.clicked.connect(lambda:self._goto(2));self.dashboard.btn_single.clicked.connect(lambda:self._goto(2));self.dashboard.btn_open_prod.clicked.connect(lambda:self._open(self.ctx.paths.production));self.dashboard.btn_open_review.clicked.connect(lambda:self._open(self.ctx.paths.review_assets));self.review.request_run.connect(self._review);self.review.request_cancel.connect(self.job_manager.cancel_current);self.production.request_single.connect(self._single);self.production.request_25.connect(self._prod25);self.artifacts.request_cleanup.connect(self._cleanup);self.artifacts.request_reset.connect(self._reset);self.families_page.request_review.connect(self._family_review);self.families_page.request_open.connect(lambda f:self._open(self.ctx.paths.family_dir(f)));self.validation.request.connect(self._validation)
  self.job_manager.job_output.connect(lambda *_:None);self.job_manager.job_state_changed.connect(lambda *_:self._sync_running());self.job_manager.job_finished.connect(self._finished)
 def _goto(self,i):self.stack.setCurrentIndex(i);[b.setChecked(j==i) for j,b in enumerate(self.nav)]
 def _open(self,path):Path(path).mkdir(parents=True,exist_ok=True);QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
 def _sync_running(self):
  running=self.job_manager.process is not None;self.review.set_running(running);self.statusBar().showMessage("RUNNING" if running else "Ready")
 def _seed_list(self,cfg):
  if cfg.get("seeds"):return [int(x) for x in cfg["seeds"]]
  return self.seeds.random_set(int(cfg.get("count",5))).seeds
 def trigger_review_5x5(self):self._goto(1);self._review({"families":[f.folder for f in self.families],"count":5,"seeds":None,"audio":True,"footer":True,"reset":False})
 def trigger_production_25(self):self._goto(2);self._prod25({"count":5,"seeds":None,"audio":True,"footer":True,"force":False})
 def _start(self,jtype,spec,seeds=None):
  try:j=self.job_manager.start(jtype,spec,seed=(seeds[0] if seeds and len(seeds)==1 else None),batch_id="batch_"+datetime.now().strftime("%Y%m%d_%H%M%S"))
  except Exception as e:QMessageBox.warning(self,"Job",str(e));return
  self.dashboard.add_job(datetime.now().strftime("%H:%M:%S"),jtype,"—",",".join(map(str,seeds or [])),j.stage,j.state.value,j.id);self._goto(8);self._sync_running()
 def _review(self,cfg):
  seeds=self._seed_list(cfg);spec=self.commands.review(seeds,cfg["families"],cfg.get("audio",True),cfg.get("reset",False),cfg.get("footer",True));self._start("REVIEW_5X5",spec,seeds)
 def _single(self,cfg):
  spec=self.commands.production_single(cfg["family"],cfg["seed"],cfg.get("audio",True),cfg.get("footer",True),cfg.get("force",False),cfg.get("grammar"));self._start("PRODUCTION_SINGLE",spec,[cfg["seed"]])
 def _prod25(self,cfg):
  seeds=self._seed_list(cfg);spec=self.commands.production_25(seeds,cfg.get("audio",True),cfg.get("footer",True),cfg.get("force",False));self._start("PRODUCTION_25",spec,seeds)
 def _family_review(self,f):self._goto(1);self.review.checks[f].setChecked(True)
 def _cleanup(self,apply):self._start("CLEANUP",self.commands.cleanup(apply),[])
 def _reset(self):self._start("RESET_C11C",self.commands.reset(True),[])
 def _validation(self,kind):
  if kind=="local":self.validation.show_report(EnvironmentValidator(self.ctx).run_all());return
  spec={"powershell":self.commands.validate_powershell,"delivery":self.commands.validate_delivery}.get(kind)
  if kind=="preflight":spec=self.commands.validate_preflight
  if spec:
   command=spec();self._start("VALIDATE_"+kind.upper(),command,[])
 def _finished(self,jid,code):
  self.products.refresh();self.artifacts.refresh();self._refresh_counts();self._sync_running();self.statusBar().showMessage(f"{self.job_manager.jobs[jid].job_type}: {self.job_manager.jobs[jid].state.value}",8000)
 def _refresh_counts(self):
  prod=sum(1 for _ in self.products_catalog.list_products());review=sum(1 for _ in self.ctx.paths.review_assets.rglob("*.mp4")) if self.ctx.paths.review_assets.exists() else 0;self.dashboard.set_counts(prod,review,len(self.families))
