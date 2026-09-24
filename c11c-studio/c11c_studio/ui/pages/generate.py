from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (QWidget,QVBoxLayout,QHBoxLayout,QGridLayout,QLabel,QPushButton,QCheckBox,QSpinBox,QComboBox,QLineEdit,QPlainTextEdit,QFrame,QFormLayout,QStackedWidget,QMessageBox,QScrollArea,QSizePolicy)
from ...domain.seed import MIN_SEED, MAX_SEED

class GeneratePage(QWidget):
    request_prototype = Signal(dict)
    request_review = Signal(dict)
    request_single = Signal(dict)
    request_25 = Signal(dict)
    request_cancel = Signal()

    def __init__(self, families, parent=None):
        super().__init__(parent); self.families=families; self.family_by_folder={f.folder:f for f in families}
        root=QVBoxLayout(self); root.setContentsMargins(18,14,18,14); root.setSpacing(8)
        title=QLabel("Generar"); title.setObjectName("PageTitle"); root.addWidget(title)
        sub=QLabel("Genera, revisa y publica desde un único panel."); sub.setObjectName("PageSubtitle"); root.addWidget(sub)

        stats=QFrame(); stats.setObjectName("GenerateSummary"); stats.setFixedHeight(38); sv=QHBoxLayout(stats); sv.setContentsMargins(12,5,12,5); sv.setSpacing(18)
        summary=QLabel(f"{len(families)} FAMILIAS  ·  720×1280  ·  30 FPS  ·  18.00 s baseline  ·  AUDIO ON")
        summary.setObjectName("GenerateSummaryText"); sv.addWidget(summary); sv.addStretch(1)
        root.addWidget(stats)

        modebar=QFrame(); modebar.setObjectName("ModeBar"); modebar.setFixedHeight(48); mv=QHBoxLayout(modebar); mv.setContentsMargins(7,7,7,7); mv.setSpacing(6)
        self.mode_buttons=[]
        for i,label in enumerate(("VÍDEO","REVIEW 5×5","PRODUCCIÓN")):
            b=QPushButton(label); b.setCheckable(True); b.setProperty("class","Mode"); b.clicked.connect(lambda _=False,j=i:self._mode(j)); mv.addWidget(b); self.mode_buttons.append(b)
        mv.addStretch(1); root.addWidget(modebar)

        self.stack=QStackedWidget(); self.stack.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
        self.stack.addWidget(self._video_panel()); self.stack.addWidget(self._review_panel()); self.stack.addWidget(self._production_panel())
        self.scroll=QScrollArea(); self.scroll.setObjectName("GenerateScroll"); self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.NoFrame); self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff); self.scroll.setWidget(self.stack); root.addWidget(self.scroll,1)
        self.info=QFrame(); self.info.setObjectName("GenerationStatus"); self.info.setFixedHeight(42); ih=QHBoxLayout(self.info); ih.setContentsMargins(12,6,12,6); self.status=QLabel("READY · selecciona una operación"); self.status.setObjectName("Hint"); ih.addWidget(self.status); ih.addStretch(1); self.cancel=QPushButton("CANCELAR"); self.cancel.setProperty("class","Danger"); self.cancel.setEnabled(False); self.cancel.clicked.connect(self.request_cancel.emit); ih.addWidget(self.cancel); root.addWidget(self.info)
        self._mode(0)

    def _family_combo(self):
        c=QComboBox(); c.setMinimumHeight(46); c.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        for f in self.families: c.addItem(f.artistic+"  ·  "+f.technical,f.folder)
        return c

    def _seed_box(self):
        s=QSpinBox(); s.setRange(MIN_SEED,MAX_SEED); s.setValue(271828); s.setMinimumHeight(46); s.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed); return s

    def _text_box(self, placeholder):
        e=QLineEdit(); e.setPlaceholderText(placeholder); e.setMinimumHeight(46); e.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed); return e

    def _video_panel(self):
        panel=QFrame(); panel.setObjectName("GeneratePanel"); root=QVBoxLayout(panel); root.setContentsMargins(20,18,20,20); root.setSpacing(12)
        h=QLabel("GENERAR VÍDEO"); h.setObjectName("PanelTitle"); root.addWidget(h); d=QLabel("Usa el launcher canónico de la familia seleccionada."); d.setObjectName("PanelMeta"); root.addWidget(d)
        form=QFormLayout(); form.setHorizontalSpacing(18); form.setVerticalSpacing(10)
        self.video_family=self._family_combo(); self.video_seed=self._seed_box(); self.video_audio=QCheckBox("Audio"); self.video_audio.setChecked(True); self.video_footer=QCheckBox("Footer editorial"); self.video_footer.setChecked(True)
        form.addRow("FAMILIA",self.video_family); form.addRow("SEED",self.video_seed); form.addRow("",self.video_audio); form.addRow("",self.video_footer); root.addLayout(form)
        self.video_run=QPushButton("GENERAR VÍDEO"); self.video_run.setProperty("class","Primary"); self.video_run.setMinimumHeight(44); self.video_run.clicked.connect(lambda:self.request_prototype.emit({"family":self.video_family.currentData(),"seed":self.video_seed.value(),"audio":self.video_audio.isChecked(),"footer":self.video_footer.isChecked()})); root.addWidget(self.video_run,0,Qt.AlignLeft)
        return panel

    def _review_panel(self):
        panel=QFrame(); panel.setObjectName("GeneratePanel"); root=QVBoxLayout(panel); root.setContentsMargins(20,18,20,20); root.setSpacing(12)
        h=QLabel("REVIEW 5×5"); h.setObjectName("PanelTitle"); root.addWidget(h); d=QLabel("El review canónico genera las 5 familias con exactamente las mismas 5 seeds."); d.setObjectName("PanelMeta"); root.addWidget(d)
        strip=QFrame(); strip.setObjectName("InfoStrip"); sv=QHBoxLayout(strip); sv.setContentsMargins(14,12,14,12); b=QLabel("25 RENDERS"); b.setObjectName("Eyebrow"); sv.addWidget(b); m=QLabel("5 seeds × 5 familias · assets regenerables · Production queda intacta"); m.setObjectName("Hint"); sv.addWidget(m); sv.addStretch(1); root.addWidget(strip)
        form=QFormLayout(); form.setHorizontalSpacing(18); form.setVerticalSpacing(10)
        self.review_seed_mode=QComboBox(); self.review_seed_mode.addItems(["RANDOM","MANUAL"]); self.review_seed_mode.setMinimumHeight(46); self.review_manual=self._text_box("Cinco seeds únicas, separadas por comas"); self.review_reset=QCheckBox("Recrear assets de review antes de ejecutar"); self.review_reset.setChecked(True)
        form.addRow("SEEDS",self.review_seed_mode); form.addRow("MANUAL",self.review_manual); form.addRow("",self.review_reset); root.addLayout(form)
        self.review_manual.setEnabled(False); self.review_seed_mode.currentTextChanged.connect(lambda m:self.review_manual.setEnabled(m=="MANUAL"))
        self.review_run=QPushButton("GENERAR REVIEW 5×5"); self.review_run.setProperty("class","Primary"); self.review_run.setMinimumHeight(44); self.review_run.clicked.connect(self._emit_review); root.addWidget(self.review_run,0,Qt.AlignLeft)
        return panel

    def _production_panel(self):
        panel=QWidget(); grid=QGridLayout(panel); grid.setContentsMargins(0,0,0,0); grid.setHorizontalSpacing(14); grid.setVerticalSpacing(0)
        single=QFrame(); single.setObjectName("GeneratePanel"); sv=QVBoxLayout(single); sv.setContentsMargins(18,18,18,18); sv.setSpacing(10); t=QLabel("PRODUCTO ÚNICO"); t.setObjectName("PanelTitle"); sv.addWidget(t); meta=QLabel("Producto final protegido, validado y trazable."); meta.setObjectName("PanelMeta"); sv.addWidget(meta)
        form=QFormLayout(); form.setHorizontalSpacing(18); form.setVerticalSpacing(10); self.prod_family=self._family_combo(); self.prod_seed=self._seed_box(); self.prod_grammar=QComboBox(); self.prod_grammar.setMinimumHeight(46); self.prod_audio=QCheckBox("Audio"); self.prod_audio.setChecked(True); self.prod_footer=QCheckBox("Footer editorial"); self.prod_footer.setChecked(True); self.prod_force=QCheckBox("Forzar reemplazo")
        form.addRow("FAMILIA",self.prod_family); form.addRow("SEED",self.prod_seed); form.addRow("GRAMMAR",self.prod_grammar); form.addRow("",self.prod_audio); form.addRow("",self.prod_footer); form.addRow("",self.prod_force); sv.addLayout(form); self.prod_family.currentIndexChanged.connect(self._refresh_grammar); self._refresh_grammar(); self.single_run=QPushButton("PRODUCIR FINAL"); self.single_run.setProperty("class","Primary"); self.single_run.setMinimumHeight(42); self.single_run.clicked.connect(self._emit_single); sv.addWidget(self.single_run,0,Qt.AlignLeft)
        bulk=QFrame(); bulk.setObjectName("GeneratePanel"); bv=QVBoxLayout(bulk); bv.setContentsMargins(18,18,18,18); bv.setSpacing(10); t=QLabel("PRODUCCIÓN 5×5"); t.setObjectName("PanelTitle"); bv.addWidget(t); meta=QLabel("Las mismas 5 seeds se cruzan automáticamente con las 5 familias."); meta.setObjectName("PanelMeta"); bv.addWidget(meta)
        bf=QFormLayout(); bf.setHorizontalSpacing(18); bf.setVerticalSpacing(10); self.prod25_mode=QComboBox(); self.prod25_mode.addItems(["RANDOM","MANUAL"]); self.prod25_mode.setMinimumHeight(46); self.prod25_manual=self._text_box("Cinco seeds únicas"); self.prod25_audio=QCheckBox("Audio"); self.prod25_audio.setChecked(True); self.prod25_footer=QCheckBox("Footer editorial"); self.prod25_footer.setChecked(True); self.prod25_force=QCheckBox("Forzar reemplazo")
        bf.addRow("SEEDS",self.prod25_mode); bf.addRow("MANUAL",self.prod25_manual); bf.addRow("",self.prod25_audio); bf.addRow("",self.prod25_footer); bf.addRow("",self.prod25_force); bv.addLayout(bf); self.prod25_manual.setEnabled(False); self.prod25_mode.currentTextChanged.connect(lambda m:self.prod25_manual.setEnabled(m=="MANUAL")); self.prod25_run=QPushButton("PRODUCIR 25 FINALES"); self.prod25_run.setProperty("class","Primary"); self.prod25_run.setMinimumHeight(42); self.prod25_run.clicked.connect(self._emit_25); bv.addWidget(self.prod25_run,0,Qt.AlignLeft)
        grid.addWidget(single,0,0); grid.addWidget(bulk,0,1); grid.setColumnStretch(0,1); grid.setColumnStretch(1,1); return panel

    def _refresh_grammar(self):
        self.prod_grammar.setMinimumHeight(46); self.prod_grammar.clear(); self.prod_grammar.addItem("AUTO / backend derived",""); f=self.family_by_folder.get(self.prod_family.currentData());
        for g in (f.grammars if f else []): self.prod_grammar.addItem(g,g)

    def _parse_five(self,text):
        vals=[]
        for token in text.replace("\n",",").split(","):
            token=token.strip()
            if token: vals.append(int(token))
        if len(vals)!=5: raise ValueError("Se requieren exactamente 5 seeds.")
        if len(set(vals))!=5: raise ValueError("Las 5 seeds deben ser únicas.")
        if any(v<MIN_SEED or v>MAX_SEED for v in vals): raise ValueError(f"Seed range is {MIN_SEED}..{MAX_SEED}.")
        return vals

    def _emit_review(self):
        seeds=None
        if self.review_seed_mode.currentText()=="MANUAL":
            try: seeds=self._parse_five(self.review_manual.text())
            except ValueError as e: QMessageBox.warning(self,"Review 5×5",str(e)); return
        self.request_review.emit({"count":5,"seeds":seeds,"reset":self.review_reset.isChecked(),"families":[]})

    def _emit_single(self):
        if self.prod_force.isChecked() and QMessageBox.warning(self,"Reemplazo explícito","Esta opción puede sustituir un producto existente. ¿Continuar?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)!=QMessageBox.Yes: return
        self.request_single.emit({"family":self.prod_family.currentData(),"seed":self.prod_seed.value(),"audio":self.prod_audio.isChecked(),"footer":self.prod_footer.isChecked(),"force":self.prod_force.isChecked(),"grammar":self.prod_grammar.currentData()})

    def _emit_25(self):
        seeds=None
        if self.prod25_mode.currentText()=="MANUAL":
            try: seeds=self._parse_five(self.prod25_manual.text())
            except ValueError as e: QMessageBox.warning(self,"Producción 5×5",str(e)); return
        if self.prod25_force.isChecked() and QMessageBox.warning(self,"Reemplazo explícito","Los productos existentes podrán sustituirse tras validación. ¿Continuar?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)!=QMessageBox.Yes: return
        self.request_25.emit({"count":5,"seeds":seeds,"audio":self.prod25_audio.isChecked(),"footer":self.prod25_footer.isChecked(),"force":self.prod25_force.isChecked()})

    def _mode(self,index):
        self.stack.setCurrentIndex(index)
        for i,b in enumerate(self.mode_buttons): b.setChecked(i==index)

    def set_running(self,running):
        for b in self.mode_buttons: b.setEnabled(not running)
        for w in (self.video_run,self.review_run,self.single_run,self.prod25_run): w.setEnabled(not running)
        self.cancel.setEnabled(running)
        self.status.setText("RUNNING · comando canónico activo" if running else "READY · selecciona una operación")
