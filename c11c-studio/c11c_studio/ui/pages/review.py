from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QCheckBox,QSpinBox,QComboBox,QLineEdit,QSplitter,QTextBrowser,QMessageBox,QGroupBox,QFormLayout,QFrame
from ...domain.seed import MIN_SEED, MAX_SEED

class ReviewPage(QWidget):
    request_run = Signal(dict)
    request_cancel = Signal()

    def __init__(self, families, parent=None):
        super().__init__(parent);self.families=families
        root=QVBoxLayout(self);root.setContentsMargins(28,24,28,24);root.setSpacing(14)
        title=QLabel("Review Lab");title.setObjectName("PageTitle");root.addWidget(title)
        sub=QLabel("Regenerable inspection space. Review can be rebuilt; Production remains protected.");sub.setObjectName("PageSubtitle");root.addWidget(sub)

        strip=QFrame();strip.setObjectName("InfoStrip");sv=QHBoxLayout(strip);sv.setContentsMargins(13,9,13,9);sv.setSpacing(10);badge=QLabel("REVIEW ONLY");badge.setObjectName("Eyebrow");sv.addWidget(badge);msg=QLabel("No production cleanup is performed from this screen.");msg.setObjectName("Hint");sv.addWidget(msg);sv.addStretch(1);root.addWidget(strip)

        splitter=QSplitter(Qt.Horizontal);splitter.setChildrenCollapsible(False);
        left=QFrame();left.setObjectName("Panel");left_layout=QVBoxLayout(left);left_layout.setContentsMargins(14,14,14,14);left_layout.setSpacing(5)
        cap=QLabel("FAMILIES");cap.setObjectName("Eyebrow");left_layout.addWidget(cap);self.checks={}
        for family in families:
            check=QCheckBox(family.artistic+"  ·  "+family.technical);check.setChecked(True);check.clicked.connect(lambda _=False,x=family.folder:self._show(x));self.checks[family.folder]=check;left_layout.addWidget(check)
        left_layout.addStretch(1);splitter.addWidget(left)

        right=QFrame();right.setObjectName("Panel");right_layout=QVBoxLayout(right);right_layout.setContentsMargins(16,14,16,14);cap2=QLabel("FAMILY DETAIL");cap2.setObjectName("Eyebrow");right_layout.addWidget(cap2);self.details=QTextBrowser();self.details.setOpenExternalLinks(False);right_layout.addWidget(self.details,1);splitter.addWidget(right);splitter.setStretchFactor(0,1);splitter.setStretchFactor(1,2);root.addWidget(splitter,1)

        box=QGroupBox("Review configuration");form=QFormLayout(box);form.setLabelAlignment(Qt.AlignLeft);form.setHorizontalSpacing(22);form.setVerticalSpacing(9)
        self.count=QSpinBox();self.count.setRange(1,100);self.count.setValue(5);self.mode=QComboBox();self.mode.addItems(["RANDOM","MANUAL"]);self.seeds=QLineEdit();self.seeds.setPlaceholderText("Unique seeds, comma-separated");self.audio=QCheckBox("Audio");self.audio.setChecked(True);self.footer=QCheckBox("Footer metadata");self.footer.setChecked(True);self.reset=QCheckBox("Reset review assets before run")
        form.addRow("SEED COUNT",self.count);form.addRow("SEED MODE",self.mode);form.addRow("MANUAL SEEDS",self.seeds);form.addRow("",self.audio);form.addRow("",self.footer);form.addRow("",self.reset)
        actions=QHBoxLayout();self.run=QPushButton("RUN REVIEW");self.run.setProperty("class","Primary");self.cancel=QPushButton("CANCEL");self.cancel.setProperty("class","Danger");actions.addWidget(self.run);actions.addWidget(self.cancel);actions.addStretch(1);form.addRow("",actions);root.addWidget(box)
        self.info=QLabel("READY · configure the corpus and run the canonical review tool");self.info.setObjectName("Hint");root.addWidget(self.info)
        self.mode.currentTextChanged.connect(lambda mode:self.seeds.setEnabled(mode=="MANUAL"));self.seeds.setEnabled(False);self.run.clicked.connect(self._emit);self.cancel.clicked.connect(self.request_cancel.emit);self._show(families[0].folder if families else None)

    def _selected(self):return [key for key,check in self.checks.items() if check.isChecked()]
    def _show(self,folder):
        family=next((item for item in self.families if item.folder==folder),None)
        if family:self.details.setPlainText("\n".join([family.artistic,f"Technical ID: {family.technical}",f"Backend ID: {family.id}","",family.short_description,"","GRAMMARS:",*(family.grammars or ["(backend/seed derived)"]),"","PARAMETERS:",*(p.id+"  ["+p.state+"]" for p in family.parameters)]))
    def _parse_manual(self):
        raw=self.seeds.text().replace("\n",",");values=[int(item.strip()) for item in raw.split(",") if item.strip()]
        if len(values)!=self.count.value():raise ValueError(f"Expected exactly {self.count.value()} seeds.")
        if len(values)!=len(set(values)):raise ValueError("Manual seeds must be unique.")
        if any(value<MIN_SEED or value>MAX_SEED for value in values):raise ValueError(f"Seed range is {MIN_SEED}..{MAX_SEED}.")
        return values
    def _emit(self):
        families=self._selected()
        if not families:QMessageBox.warning(self,"Review","Select at least one family.");return
        seeds=None
        if self.mode.currentText()=="MANUAL":
            try:seeds=self._parse_manual()
            except ValueError as exc:QMessageBox.warning(self,"Review",str(exc));return
        self.request_run.emit({"families":families,"count":self.count.value(),"seeds":seeds,"audio":self.audio.isChecked(),"footer":self.footer.isChecked(),"reset":self.reset.isChecked()})
    def set_running(self,running):
        self.run.setEnabled(not running);self.cancel.setEnabled(running);self.info.setText("RUNNING · canonical review job active" if running else "READY · configure the corpus and run the canonical review tool")
