from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QGroupBox,QFormLayout,QLineEdit,QPushButton,QHBoxLayout,QFileDialog,QCheckBox,QComboBox
class SettingsPage(QWidget):
 def __init__(self,ctx,cfg,parent=None):
  super().__init__(parent);self.ctx=ctx;self.cfg=cfg;root=QVBoxLayout(self);t=QLabel("Settings");t.setObjectName("PageTitle");root.addWidget(t);g=QGroupBox("Project / behavior");f=QFormLayout(g);self.project=QLineEdit(str(ctx.project_root));self.project.setReadOnly(True);pick=QPushButton("...");r=QHBoxLayout();r.addWidget(self.project);r.addWidget(pick);f.addRow("Project root",r);self.player=QComboBox();self.player.addItems(["System default","Custom executable"]);self.player.setCurrentText(cfg.get("preferred_player","System default"));self.auto=QCheckBox("Auto-scroll logs");self.auto.setChecked(cfg.get("auto_scroll_logs",True));self.confirm=QCheckBox("Confirm destructive actions");self.confirm.setChecked(cfg.get("confirm_destructive",True));f.addRow("Preferred player",self.player);f.addRow("",self.auto);f.addRow("",self.confirm);root.addWidget(g);g2=QGroupBox("Tool path overrides");f2=QFormLayout(g2);self.edits={};
  for key,label in (("godot","Godot"),("python","Python"),("ffmpeg","FFmpeg"),("ffprobe","FFprobe"),("powershell","PowerShell")):
   e=QLineEdit((cfg.get("tool_paths",{}) or {}).get(key,""));b=QPushButton("...");b.clicked.connect(lambda _=False,k=key,x=e:self._pick_tool(k,x));rr=QHBoxLayout();rr.addWidget(e);rr.addWidget(b);f2.addRow(label,rr);self.edits[key]=e
  root.addWidget(g2);g3=QGroupBox("Effective delivery (read-only)");f3=QFormLayout(g3);f3.addRow("Physical",QLabel(f"{ctx.delivery_width}×{ctx.delivery_height} / {ctx.fps} FPS / {ctx.default_duration:.2f}s"));f3.addRow("Logical",QLabel("540×960 / Header 0..144 / Body 144..816 / Footer 816..960"));f3.addRow("C11-B",QLabel(ctx.c11b_state));root.addWidget(g3);save=QPushButton("SAVE");root.addWidget(save);pick.clicked.connect(self._pick_project);save.clicked.connect(self._save);root.addStretch(1)
 def _pick_project(self):
  p=QFileDialog.getExistingDirectory(self,"Select project",str(self.ctx.project_root));
  if p:self.project.setText(p);self.cfg.set("project_root",p)
 def _pick_tool(self,key,e):
  p,_=QFileDialog.getOpenFileName(self,f"Select {key} executable");
  if p:e.setText(p)
 def _save(self):
  self.cfg.set("project_root",self.project.text());self.cfg.set("tool_paths",{k:e.text().strip() for k,e in self.edits.items() if e.text().strip()});self.cfg.set("preferred_player",self.player.currentText());self.cfg.set("auto_scroll_logs",self.auto.isChecked());self.cfg.set("confirm_destructive",self.confirm.isChecked());self.cfg.save()
