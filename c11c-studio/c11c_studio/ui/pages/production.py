from PySide6.QtCore import Signal,Qt
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QGroupBox,QFormLayout,QComboBox,QSpinBox,QCheckBox,QPlainTextEdit,QPushButton,QHBoxLayout,QMessageBox,QFrame,QSplitter
from ...domain.seed import MIN_SEED, MAX_SEED

class ProductionPage(QWidget):
    request_single=Signal(dict);request_25=Signal(dict)
    def __init__(self,families,parent=None):
        super().__init__(parent);self.families=families;self.family_by_folder={item.folder:item for item in families}
        root=QVBoxLayout(self);root.setContentsMargins(28,24,28,24);root.setSpacing(14)
        title=QLabel("Production");title.setObjectName("PageTitle");root.addWidget(title)
        sub=QLabel("Publish validated final products into the protected production catalog.");sub.setObjectName("PageSubtitle");root.addWidget(sub)
        strip=QFrame();strip.setObjectName("InfoStrip");sv=QHBoxLayout(strip);sv.setContentsMargins(13,9,13,9);b=QLabel("PROTECTED ZONE");b.setObjectName("Eyebrow");sv.addWidget(b);m=QLabel("Existing final products are never replaced silently.");m.setObjectName("Hint");sv.addWidget(m);sv.addStretch(1);root.addWidget(strip)

        splitter=QSplitter(Qt.Horizontal);splitter.setChildrenCollapsible(False)
        single=QGroupBox("Single product");single_form=QFormLayout(single);single_form.setHorizontalSpacing(22);single_form.setVerticalSpacing(10)
        self.family=QComboBox();self.grammars=QComboBox();self.grammars.addItem("AUTO / backend derived","");self.seed=QSpinBox();self.seed.setRange(MIN_SEED,MAX_SEED);self.seed.setValue(271828);self.audio=QCheckBox("Audio");self.audio.setChecked(True);self.footer=QCheckBox("Footer metadata");self.footer.setChecked(True);self.force=QCheckBox("Force replacement — explicit")
        single_form.addRow("FAMILY",self.family);single_form.addRow("GRAMMAR",self.grammars);single_form.addRow("SEED",self.seed);single_form.addRow("",self.audio);single_form.addRow("",self.footer);single_form.addRow("",self.force)
        for item in families:self.family.addItem(item.artistic+"  ·  "+item.technical,item.folder)
        self.family.currentIndexChanged.connect(self._refresh_grammars);self._refresh_grammars();self.bsingle=QPushButton("PRODUCE FINAL PRODUCT");self.bsingle.setProperty("class","Primary");single_form.addRow("",self.bsingle);splitter.addWidget(single)

        bulk=QGroupBox("Production 5×5");bulk_form=QFormLayout(bulk);bulk_form.setHorizontalSpacing(22);bulk_form.setVerticalSpacing(10)
        self.seed_mode=QComboBox();self.seed_mode.addItems(["RANDOM","MANUAL"]);self.seed_count=QSpinBox();self.seed_count.setRange(5,5);self.seed_count.setValue(5);self.manual=QPlainTextEdit();self.manual.setMaximumHeight(90);self.manual.setPlaceholderText("Five unique seeds · comma or newline separated");self.audio25=QCheckBox("Audio");self.audio25.setChecked(True);self.footer25=QCheckBox("Footer metadata");self.footer25.setChecked(True);self.force25=QCheckBox("Force replacement")
        bulk_form.addRow("SEED MODE",self.seed_mode);bulk_form.addRow("SEED COUNT",self.seed_count);bulk_form.addRow("MANUAL SEEDS",self.manual);bulk_form.addRow("",self.audio25);bulk_form.addRow("",self.footer25);bulk_form.addRow("",self.force25);self.b25=QPushButton("PRODUCE 25 FINAL PRODUCTS");self.b25.setProperty("class","Primary");bulk_form.addRow("",self.b25);splitter.addWidget(bulk);splitter.setStretchFactor(0,1);splitter.setStretchFactor(1,1);root.addWidget(splitter,1)
        hint=QLabel("Production 5×5 uses the same five-seed set across all discovered families.");hint.setObjectName("Hint");root.addWidget(hint)
        self.seed_mode.currentTextChanged.connect(lambda mode:self.manual.setEnabled(mode=="MANUAL"));self.manual.setEnabled(False);self.bsingle.clicked.connect(self._single);self.b25.clicked.connect(self._25)
    def _refresh_grammars(self):
        folder=self.family.currentData();family=self.family_by_folder.get(folder);self.grammars.blockSignals(True);self.grammars.clear();self.grammars.addItem("AUTO / backend derived","")
        if family:
            for grammar in family.grammars:self.grammars.addItem(grammar,grammar)
        self.grammars.blockSignals(False)
    def _parse_manual(self):
        values=[]
        for token in self.manual.toPlainText().replace("\n",",").split(","):
            token=token.strip()
            if token:values.append(int(token))
        if len(values)!=5:raise ValueError("Production 5×5 requires exactly 5 seeds.")
        if len(values)!=len(set(values)):raise ValueError("Production seeds must be unique.")
        if any(value<MIN_SEED or value>MAX_SEED for value in values):raise ValueError(f"Seed range is {MIN_SEED}..{MAX_SEED}.")
        return values
    def _single(self):
        if self.force.isChecked() and QMessageBox.warning(self,"Force replacement","This explicitly allows replacement after candidate validation. Continue?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)!=QMessageBox.Yes:return
        self.request_single.emit({"family":self.family.currentData(),"seed":self.seed.value(),"audio":self.audio.isChecked(),"footer":self.footer.isChecked(),"force":self.force.isChecked(),"grammar":self.grammars.currentData()})
    def _25(self):
        seeds=None
        if self.seed_mode.currentText()=="MANUAL":
            try:seeds=self._parse_manual()
            except ValueError as exc:QMessageBox.warning(self,"Production",str(exc));return
        if self.force25.isChecked() and QMessageBox.warning(self,"Force replacement","Existing final products may be replaced after validation. Continue?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)!=QMessageBox.Yes:return
        self.request_25.emit({"count":5,"seeds":seeds,"audio":self.audio25.isChecked(),"footer":self.footer25.isChecked(),"force":self.force25.isChecked()})
