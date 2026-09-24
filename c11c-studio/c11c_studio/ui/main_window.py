from datetime import datetime
from pathlib import Path
from PySide6.QtCore import QTimer, QUrl, Qt
from PySide6.QtGui import QDesktopServices, QFont
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame,
    QStackedWidget, QStatusBar, QMessageBox, QSizePolicy, QSpacerItem)
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
from .pages.generate import GeneratePage
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
 def __init__(self,ctx,cfg,app_version="0.4.0"):
  super().__init__();self.ctx=ctx;self.cfg=cfg;self.app_version=app_version;self.tools=discover_all(ctx.project_root,cfg.get("tool_paths",{}));ctx.powershell_path=self.tools["powershell"].path;ctx.python_path=self.tools["python"].path;ctx.ffmpeg_path=self.tools["ffmpeg"].path;ctx.ffprobe_path=self.tools["ffprobe"].path;ctx.godot_path=self.tools["godot"].path;ctx.godot_version=self.tools["godot"].version
  self.introspector=BackendIntrospector(ctx);catalog=self.introspector.scan();self.families=FamilyRegistry(ctx,self.introspector).load();self.commands=CommandBuilder(ctx,catalog);self.seeds=SeedManager(ctx.paths.gui_workspace/"seeds");self.job_manager=JobManager(ctx.paths.gui_logs);self.registry=ArtifactRegistry(ctx);self.products_catalog=ProductCatalog(ctx);self.snapshots=SnapshotService(ctx.paths.gui_snapshots);self._batch_queue=[];self._batch_total=0;self._batch_current=0;self._batch_id=None;self._active_batch_id=None
  self._build();self._wire();self._refresh_counts();self.timer=QTimer(self);self.timer.timeout.connect(self._refresh_counts);self.timer.start(15000)
 def _build(self):
  self.setWindowTitle("C11-C Studio — "+self.ctx.project_root.name);self.resize(1480,940);self.setMinimumSize(1180,760)
  status=QStatusBar();status.setSizeGripEnabled(True);self.setStatusBar(status)
  central=QWidget();central.setObjectName("AppShell");self.setCentralWidget(central);root=QVBoxLayout(central);root.setContentsMargins(0,0,0,0);root.setSpacing(0);root.addWidget(self._top())
  body=QHBoxLayout();body.setContentsMargins(0,0,0,0);body.setSpacing(0);body.addWidget(self._nav());self.stack=QStackedWidget();self.stack.setObjectName("PageStack");body.addWidget(self.stack,1);w=QWidget();w.setLayout(body);root.addWidget(w,1)
  self._build_pages()
  self.status_pill=QLabel("●  READY");self.status_pill.setObjectName("StatusPill");self.status_detail=QLabel("Backend connected");self.status_detail.setObjectName("StatusDetail");self.statusBar().addWidget(self.status_pill);self.statusBar().addPermanentWidget(self.status_detail)
 def _build_pages(self):
  self.generate=GeneratePage(self.families);self.art=ArtDirectionPage(self.ctx,self.families,self.snapshots);self.families_page=FamiliesPage(self.families);self.seeds_page=SeedsPage(self.seeds);self.products=ProductsPage(self.products_catalog,self.cfg);self.artifacts=ArtifactsPage(self.registry);self.jobs=JobsPage(self.job_manager);self.logs=LogsPage(self.job_manager);self.validation=ValidationPage();self.games=GamesPage(self.ctx);self.repro=ReproductionPage(self.ctx,self.families,self.commands);self.settings=SettingsPage(self.ctx,self.cfg);self.about=AboutPage(self.ctx,self.app_version)
  self.pages=[self.generate,self.products,self.jobs,self.logs,self.repro,self.art,self.families_page,self.seeds_page,self.artifacts,self.validation,self.settings,self.games,self.about]
  [self.stack.addWidget(p) for p in self.pages]
 def _top(self):
  b=QFrame();b.setObjectName("TopBar");b.setFixedHeight(74);h=QHBoxLayout(b);h.setContentsMargins(22,10,22,10);h.setSpacing(14)
  brand=QVBoxLayout();brand.setSpacing(0);t=QLabel("C11-C Studio");t.setObjectName("TopBarTitle");brand.addWidget(t);s=QLabel("DETERMINISTIC VISUAL PRODUCTION CONTROL") ;s.setObjectName("TopBarKicker");brand.addWidget(s);h.addLayout(brand)
  h.addWidget(self._vertical_divider());
  meta=QVBoxLayout();meta.setSpacing(1);line=QLabel(f"C11-C {self.ctx.backend_version}   ·   C11-B {self.ctx.c11b_state}");line.setObjectName("TopBarMeta");meta.addWidget(line);delivery=QLabel(f"DELIVERY  {self.ctx.delivery_width}×{self.ctx.delivery_height}   ·   {self.ctx.fps} FPS   ·   {self.ctx.default_duration:.2f}s baseline");delivery.setObjectName("TopBarSubMeta");meta.addWidget(delivery);h.addLayout(meta);h.addStretch(1)
  env=QLabel(self._environment_text());env.setObjectName("EnvironmentPill");env.setToolTip(self._environment_tooltip());h.addWidget(env)
  project=QVBoxLayout();project.setSpacing(1);pl=QLabel("PROJECT");pl.setObjectName("TopBarProjectLabel");pv=QLabel(self.ctx.project_root.name);pv.setObjectName("TopBarProject");pv.setToolTip(str(self.ctx.project_root));project.addWidget(pl,alignment=Qt.AlignRight);project.addWidget(pv,alignment=Qt.AlignRight);h.addLayout(project)
  return b
 def _vertical_divider(self):
  d=QFrame();d.setObjectName("TopDivider");d.setFrameShape(QFrame.VLine);d.setFixedWidth(1);return d
 def _environment_text(self):
  required=("godot","python","ffmpeg","ffprobe","powershell")
  missing=[k for k in required if not self.tools.get(k) or not self.tools[k].present]
  return "●  READY" if not missing else f"●  {len(missing)} TOOL{'S' if len(missing)!=1 else ''} MISSING"
 def _environment_tooltip(self):
  parts=[]
  for key in ("godot","python","ffmpeg","ffprobe","powershell"):
   tool=self.tools.get(key);parts.append(f"{key.upper()}: {'READY' if tool and tool.present else 'MISSING'}" + (f" · {tool.version}" if tool and tool.present and tool.version else ""))
  return "Environment health\n"+"\n".join(parts)
 def _nav(self):
  r=QFrame();r.setObjectName("NavRail");r.setFixedWidth(226);v=QVBoxLayout(r);v.setContentsMargins(10,14,10,12);v.setSpacing(3);self.nav=[]
  groups=[("PRODUCCIÓN",[("Generar",0),("Resultados",1),("Jobs",2),("Logs",3),("Reproducir",4)]),("CONFIGURACIÓN",[("Dirección de arte",5),("Familias",6),("Seeds",7),("Artifacts",8),("Validación",9),("Ajustes",10),("Juegos / Drills",11),("Diagnóstico",12)])]
  for heading,items in groups:
   cap=QLabel(heading);cap.setObjectName("NavSection");v.addWidget(cap)
   for label,i in items:
    b=NavButton(label);b.setProperty("navIndex",i);b.clicked.connect(lambda _=False,j=i:self._goto(j));v.addWidget(b);self.nav.append(b)
   if heading=="PRODUCCIÓN":
    v.addSpacing(12)
  v.addSpacing(8);v.addStretch(1)
  hint=QLabel("PRODUCCIÓN = generar y supervisar\nCONFIGURACIÓN = preparar y mantener");hint.setObjectName("NavHint");hint.setWordWrap(True);v.addWidget(hint)
  self.nav[0].setChecked(True);return r
 def _wire(self):
  self.generate.request_prototype.connect(self._prototype);self.generate.request_review.connect(self._review);self.generate.request_single.connect(self._single);self.generate.request_25.connect(self._prod25);self.generate.request_cancel.connect(self.job_manager.cancel_current)
  self.artifacts.request_cleanup.connect(self._cleanup);self.artifacts.request_reset.connect(self._reset);self.families_page.request_review.connect(lambda f:self._goto(0));self.families_page.request_open.connect(lambda f:self._open(self.ctx.paths.family_dir(f)));self.validation.request.connect(self._validation)
  self.job_manager.job_state_changed.connect(lambda *_:self._sync_running());self.job_manager.job_finished.connect(self._finished)
 def _goto(self,i):self.stack.setCurrentIndex(i);[b.setChecked(b.property("navIndex")==i) for b in self.nav];self.statusBar().showMessage(self.pages[i].__class__.__name__.replace("Page","").replace("_"," ").upper(),1500)
 def _open(self,path):Path(path).mkdir(parents=True,exist_ok=True);QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
 def _sync_running(self):
  running=self.job_manager.process is not None;self.generate.set_running(running);self.statusBar().showMessage("RUNNING · canonical job active" if running else "Ready");self.status_pill.setText("●  RUNNING" if running else "●  READY");self.status_pill.setProperty("state","running" if running else "ready");self.status_pill.style().unpolish(self.status_pill);self.status_pill.style().polish(self.status_pill);self.status_detail.setText("Canonical job active" if running else f"Project · {self.ctx.project_root.name}")
 def _seed_list(self,cfg):
  if cfg.get("seeds"):
   seedset=self.seeds.manual_set([int(x) for x in cfg["seeds"]]);self._active_batch_id=seedset.batch_id;return seedset.seeds
  seedset=self.seeds.random_set(int(cfg.get("count",5)));self._active_batch_id=seedset.batch_id;return seedset.seeds
 def trigger_review_5x5(self):self._goto(0);self._review({"count":5,"seeds":None,"reset":True,"families":[]})
 def trigger_production_25(self):self._goto(0);self._prod25({"count":5,"seeds":None,"audio":True,"footer":True,"force":False})
 def _start(self,jtype,spec,seeds=None,batch_id=None):
  try:j=self.job_manager.start(jtype,spec,seed=(seeds[0] if seeds and len(seeds)==1 else None),batch_id=batch_id or self._active_batch_id or "batch_"+datetime.now().strftime("%Y%m%d_%H%M%S"))
  except Exception as e:QMessageBox.warning(self,"Job",str(e));return None
  self.statusBar().showMessage(f"{jtype} · starting",3000);self._sync_running();return j
 def _review(self,cfg):
  seeds=self._seed_list(cfg);spec=self.commands.review(seeds,self.commands.CANONICAL_FAMILIES,audio=True,reset=cfg.get("reset",True),footer=True);self._start("REVIEW_5X5",spec,seeds)
 def _single(self,cfg):
  spec=self.commands.production_single(cfg["family"],cfg["seed"],cfg.get("audio",True),cfg.get("footer",True),cfg.get("force",False),cfg.get("grammar"));self._start("PRODUCTION_SINGLE",spec,[cfg["seed"]])
 def _prod25(self,cfg):
  seeds=self._seed_list(cfg);self._batch_id=self._active_batch_id or "batch_"+datetime.now().strftime("%Y%m%d_%H%M%S");specs=self.commands.production_25(seeds,cfg.get("audio",True),cfg.get("footer",True),cfg.get("force",False));self._batch_queue=[(i+1,spec,seeds) for i,spec in enumerate(specs)];self._batch_total=len(self._batch_queue);self._run_next_batch()
 def _run_next_batch(self):
  if not self._batch_queue:
   self._sync_running();return
  number,spec,seeds=self._batch_queue.pop(0);self._batch_current=number;self.statusBar().showMessage(f"PRODUCTION 5×5 · family {number}/{self._batch_total}");self._start("PRODUCTION_25_FAMILY",spec,seeds,batch_id=getattr(self,"_batch_id",None))

 def _prototype(self,cfg):
  spec=self.commands.prototype(cfg["family"],cfg["seed"],cfg.get("audio",True),cfg.get("footer",True));self._start("PROTOTYPE",spec,[cfg["seed"]])

 def _family_review(self,f):self._goto(0)

 def _cleanup(self,apply):self._start("CLEANUP",self.commands.cleanup(apply),[])
 def _reset(self):self._start("RESET_C11C",self.commands.reset(True),[])
 def _validation(self,kind):
  if kind=="local":self.validation.show_report(EnvironmentValidator(self.ctx).run_all());return
  spec={"powershell":self.commands.validate_powershell,"delivery":self.commands.validate_delivery}.get(kind)
  if kind=="preflight":spec=self.commands.validate_preflight
  if spec:
   command=spec();self._start("VALIDATE_"+kind.upper(),command,[])
 def _finished(self,jid,code):
  self.products.refresh();self.artifacts.refresh();self._refresh_counts();self._sync_running();
  if self._batch_queue:
   if code==0: QTimer.singleShot(0, self._run_next_batch)
   else: self._batch_queue=[];QMessageBox.warning(self,"Production 5×5","La tanda se ha detenido porque una familia falló. Consulta el log del job para el error exacto.")
  if not self._batch_queue:
   self._batch_id=None
  self.statusBar().showMessage(f"{self.job_manager.jobs[jid].job_type}: {self.job_manager.jobs[jid].state.value}",8000)
 def _refresh_counts(self):
  prod=sum(1 for _ in self.products_catalog.list_products());review=sum(1 for _ in self.ctx.paths.review_assets.rglob("*.mp4")) if self.ctx.paths.review_assets.exists() else 0;state="RUNNING" if self.job_manager.process is not None else "READY";self.generate.status.setText(f"{state} · {prod} productos publicados · {review} assets de review")
