from __future__ import annotations
import hashlib, json, os, random, re, sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from PySide6.QtCore import QProcess, QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication,QCheckBox,QComboBox,QDoubleSpinBox,QFrame,QGridLayout,QGroupBox,QHBoxLayout,QLabel,QLineEdit,QMainWindow,QMessageBox,QPlainTextEdit,QPushButton,QScrollArea,QSizePolicy,QSpinBox,QTableWidget,QTableWidgetItem,QVBoxLayout,QWidget

APP_VERSION='0.7.0'
ROOT=Path(__file__).resolve().parent
PROJECT=Path(os.environ.get('C11C_PROJECT_ROOT',ROOT.parent)).resolve()
SCHEMA=json.loads((ROOT/'producer_schema.json').read_text(encoding='utf-8'))
FAMILIES=SCHEMA['families']; CHALLENGES={x['id']:x for x in SCHEMA.get('challenges',[])}

@dataclass
class Recipe:
    operation:str; video_type:str; family:str=''; grammar:str='auto'; challenge_id:str=''; count:int=1; manual_seeds:list[int]|None=None
    no_sound:bool=False; no_footer:bool=False; force:bool=False; workers:int=7; resume:bool=False; reset:bool=False
    export_gif:bool=False; keep_avi:bool=False; delivery:str='C11C_REVIEW_720'; targets:dict[str,Any]|None=None

class ParamRow(QWidget):
    def __init__(self,spec):
        super().__init__(); self.spec=spec
        lay=QHBoxLayout(self); lay.setContentsMargins(0,1,0,1); lay.setSpacing(8)
        self.label=QLabel(spec['label']); self.label.setMinimumWidth(155)
        self.mode=QComboBox(); self.mode.addItems(['ALEATORIO (seed)','FIJAR']); self.mode.setFixedWidth(155)
        if spec['kind']=='enum': self.editor=QComboBox(); self.editor.addItems([str(x) for x in spec['values']])
        else:
            self.editor=QDoubleSpinBox(); self.editor.setRange(float(spec['min']),float(spec['max'])); self.editor.setSingleStep(float(spec['step'])); self.editor.setDecimals(5 if float(spec['step'])<0.001 else 3 if float(spec['step'])<0.01 else 2); self.editor.setValue((float(spec['min'])+float(spec['max']))/2)
        self.editor.setEnabled(False); self.editor.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        lay.addWidget(self.label); lay.addWidget(self.mode); lay.addWidget(self.editor,1); self.mode.currentIndexChanged.connect(lambda i:self.editor.setEnabled(i==1))
    def set_random(self): self.mode.setCurrentIndex(0)
    def value(self):
        if self.mode.currentIndex()==0:return None
        if self.spec['kind']=='enum':
            s=self.editor.currentText()
            try:return int(s)
            except ValueError:return s
        return float(self.editor.value())
    def set_interactive(self,enabled): self.setEnabled(enabled); self.mode.setEnabled(enabled); self.editor.setEnabled(enabled and self.mode.currentIndex()==1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle(f'C11-C Producer {APP_VERSION}'); self.resize(1280,920)
        self.queue=[]; self.current_recipe=None; self.jobs=[]; self.proc=None; self.probe_file=None; self.rows=[]; self._build(); self._check_backend()
    def _build(self):
        root=QWidget(); self.setCentralWidget(root); main=QVBoxLayout(root); main.setContentsMargins(14,14,14,14); main.setSpacing(10)
        banner=QFrame(); banner.setObjectName('Banner'); bl=QHBoxLayout(banner); bl.setContentsMargins(16,9,16,9); t=QLabel('C11-C PRODUCER'); t.setObjectName('Title'); bl.addWidget(t); bl.addStretch(); self.backend_info=QLabel(''); self.backend_info.setObjectName('Muted'); bl.addWidget(self.backend_info); main.addWidget(banner)
        cols=QHBoxLayout(); cols.setSpacing(10); cols.addWidget(self._build_recipe(),1); cols.addWidget(self._build_queue(),1); main.addLayout(cols,1)
    def _build_recipe(self):
        box=QGroupBox('CREAR PRODUCCIÓN'); root=QVBoxLayout(box); root.setSpacing(8)
        grid=QGridLayout(); grid.setHorizontalSpacing(10); grid.setVerticalSpacing(8)
        self.operation=QComboBox(); self.operation.addItem('A LA CARTA','A_LA_CARTA')
        for k,label in SCHEMA.get('batch_operations',[])[1:]: self.operation.addItem(label,k)
        self.operation.addItem('REGRESIÓN COMPLETA','RUN_REGRESSION')
        self.video_type=QComboBox(); self.video_type.addItem('CHALLENGES','challenges'); self.video_type.addItem('VISUAL LOOPS','visual_loops'); self.video_type.addItem('VISUAL DRILLS','visual_drills'); self.video_type.setCurrentIndex(1)
        self.family=QComboBox(); self.grammar=QComboBox(); self.count=QSpinBox(); self.count.setRange(1,500); self.count.setValue(1)
        self.seed_mode=QComboBox(); self.seed_mode.addItems(['SEEDS ALEATORIAS','SEEDS MANUALES']); self.manual=QLineEdit(); self.manual.setPlaceholderText('314159, 271828…'); self.manual.setEnabled(False)
        self.video_type_label=QLabel('Tipo de vídeo'); self.family_label=QLabel('Familia'); self.subtype_label=QLabel('Subfamilia'); self.count_label=QLabel('Cantidad'); self.seed_label=QLabel('Seeds')
        for row,label,w in [(0,QLabel('Operación'),self.operation),(1,self.video_type_label,self.video_type),(2,self.family_label,self.family),(3,self.subtype_label,self.grammar),(4,self.count_label,self.count),(5,self.seed_label,self.seed_mode)]:grid.addWidget(label,row,0);grid.addWidget(w,row,1)
        grid.addWidget(self.manual,6,0,1,2);root.addLayout(grid)
        self.type_info=QLabel();self.type_info.setObjectName('Hint');self.type_info.setWordWrap(True);root.addWidget(self.type_info)
        opts=QHBoxLayout();self.no_sound=QCheckBox('Sin audio');self.no_footer=QCheckBox('Sin footer');self.force=QCheckBox('FORCE');opts.addWidget(self.no_sound);opts.addWidget(self.no_footer);opts.addWidget(self.force);opts.addStretch();root.addLayout(opts)
        out=QGridLayout();self.delivery=QComboBox();self.delivery.addItems([x[1] for x in SCHEMA.get('delivery_profiles',[])]);self.workers=QSpinBox();self.workers.setRange(1,7);self.workers.setValue(7);self.resume=QCheckBox('RESUME');self.reset=QCheckBox('RESET');self.export_gif=QCheckBox('Exportar GIF');self.keep_avi=QCheckBox('Conservar AVI')
        out.addWidget(QLabel('Salida'),0,0);out.addWidget(self.delivery,0,1);out.addWidget(QLabel('Workers'),1,0);out.addWidget(self.workers,1,1);out.addWidget(self.resume,2,0);out.addWidget(self.reset,2,1);out.addWidget(self.export_gif,3,0);out.addWidget(self.keep_avi,3,1);root.addLayout(out)
        pbox=QGroupBox('VARIACIÓN · por defecto ALEATORIA por seed');pl=QVBoxLayout(pbox);self.randomize=QPushButton('PONER TODO EN ALEATORIO');pl.addWidget(self.randomize);self.pscroll=QScrollArea();self.pscroll.setWidgetResizable(True);self.pscroll.setFrameShape(QFrame.NoFrame);self.pwidget=QWidget();self.pl=QVBoxLayout(self.pwidget);self.pl.setContentsMargins(4,4,4,4);self.pl.setAlignment(Qt.AlignTop);self.pscroll.setWidget(self.pwidget);pl.addWidget(self.pscroll,1);root.addWidget(pbox,1)
        hint=QLabel('La GUI orquesta launchers canónicos. No reimplementa mecánicas, RNG ni renderers.');hint.setObjectName('Hint');hint.setWordWrap(True);root.addWidget(hint)
        self.add=QPushButton('AÑADIR A LA COLA');self.add.setObjectName('Primary');self.add.setMinimumHeight(46);root.addWidget(self.add)
        self.operation.currentIndexChanged.connect(self._operation_changed);self.video_type.currentIndexChanged.connect(self._video_type_changed);self.family.currentIndexChanged.connect(self._refresh_family);self.seed_mode.currentIndexChanged.connect(self._seed_mode_changed);self.randomize.clicked.connect(self._randomize_all);self.add.clicked.connect(self._add)
        self._video_type_changed(self.video_type.currentIndex());self._operation_changed(0);return box
    def _build_queue(self):
        box=QGroupBox('COLA DE PRODUCCIÓN');root=QVBoxLayout(box);self.table=QTableWidget(0,8);self.table.setHorizontalHeaderLabels(['Operación','Tipo','Familia','Subfamilia','Cantidad','Salida','Workers','Estado']);root.addWidget(self.table,3);btns=QHBoxLayout();self.generate=QPushButton('GENERAR');self.generate.setObjectName('Primary');self.generate.setMinimumHeight(48);self.remove=QPushButton('QUITAR');self.clear=QPushButton('VACIAR');btns.addWidget(self.generate,2);btns.addWidget(self.remove);btns.addWidget(self.clear);root.addLayout(btns);lbox=QGroupBox('PROGRESO / LOG');ll=QVBoxLayout(lbox);self.log=QPlainTextEdit();self.log.setReadOnly(True);ll.addWidget(self.log);root.addWidget(lbox,2);self.generate.clicked.connect(self.start);self.remove.clicked.connect(self.remove_selected);self.clear.clicked.connect(self._clear);return box
    def _clear_rows(self):
        while self.pl.count():
            item=self.pl.takeAt(0);w=item.widget();
            if w:w.deleteLater()
        self.rows=[]
    def _video_type_changed(self,idx):
        if str(self.operation.currentData())!='A_LA_CARTA': return
        vt=str(self.video_type.currentData()); self._clear_rows()
        if vt=='challenges':
            self.family_label.setText('Mecánica');self.subtype_label.setText('Challenge ID');self.family.clear();self.grammar.clear();self.family.addItems(sorted({x['mechanic'] for x in CHALLENGES.values()}));self._refresh_challenges();self.no_footer.setChecked(False);self.type_info.setText('Challenges: usa las definiciones canónicas y el wrapper GeneradorMaestro. El Producer no duplica la mecánica.')
        elif vt=='visual_loops':
            self.family_label.setText('Familia');self.subtype_label.setText('Subfamilia');self.family.clear();self.family.addItems([v['name'] for v in FAMILIES.values()]);self._refresh_family(0);self.type_info.setText('Visual Loops: 5 familias / 27 grammars. Con parámetros FIJAR, el seed planner busca seeds compatibles. La salida de review congelada es 720x1280; Meta final se reserva para la siguiente capa de delivery.')
        else:
            self.family_label.setText('Familia');self.subtype_label.setText('Dificultad');self.family.clear();self.family.addItems([v['name'] for v in SCHEMA['drills'].values()]);self._refresh_family(0);self.no_footer.setChecked(False);self.type_info.setText('Visual Drills: Tracking, Saccade, Pursuit y Peripheral Scan. 3 s de preparación + gameplay + 3 s de CTA.')
        self.delivery.setEnabled(self.operation.currentData()=='A_LA_CARTA' and vt!='visual_loops')
        if vt=='visual_loops': self.delivery.setCurrentIndex(0)
        self._seed_mode_changed(self.seed_mode.currentIndex())
    def _refresh_challenges(self):
        mech=str(self.family.currentText());self.grammar.clear()
        for cid,d in CHALLENGES.items():
            if d['mechanic']==mech:self.grammar.addItem(f"{cid} · {mech}",cid)
    def _refresh_family(self,idx):
        vt=str(self.video_type.currentData());self._clear_rows()
        if vt=='challenges':self._refresh_challenges();return
        if vt=='visual_loops':
            ids=list(FAMILIES);idx=max(0,min(idx,len(ids)-1));self.family.blockSignals(True);self.family.setCurrentIndex(idx);self.family.blockSignals(False);fid=ids[idx];self.grammar.clear()
            for code,label in FAMILIES[fid]['grammars']:self.grammar.addItem(label,code)
            for spec in FAMILIES[fid].get('params',[]):
                r=ParamRow(spec);self.rows.append(r);self.pl.addWidget(r)
            self._seed_mode_changed(self.seed_mode.currentIndex())
        elif vt=='visual_drills':
            ids=list(SCHEMA['drills']);idx=max(0,min(idx,len(ids)-1));self.family.blockSignals(True);self.family.setCurrentIndex(idx);self.family.blockSignals(False);fid=ids[idx];self.grammar.clear();self.grammar.addItem('ALEATORIO', 'auto')
            for tier in range(1,6):self.grammar.addItem(f'TIER {tier}',str(tier))
            for spec in SCHEMA['drills'][fid].get('parameters',[]):
                r=ParamRow(spec);self.rows.append(r);self.pl.addWidget(r)
            self._seed_mode_changed(self.seed_mode.currentIndex())
    def _operation_changed(self,idx):
        op=str(self.operation.currentData());batch=op!='A_LA_CARTA'
        utility=op=='RUN_REGRESSION';
        self.video_type.setEnabled(not batch);self.family.setEnabled(not batch);self.grammar.setEnabled(not batch);self.count.setEnabled(not batch);self.seed_mode.setEnabled(not batch);self.manual.setEnabled(False);self.no_sound.setEnabled(not batch and not utility);self.no_footer.setEnabled(not batch and not utility);self.force.setEnabled(not batch and not utility);self.randomize.setEnabled(not batch);self.delivery.setEnabled(not batch and not utility and self.video_type.currentData()!='visual_loops');self.workers.setEnabled(True);self.resume.setEnabled(batch and not utility);self.reset.setEnabled(batch and not utility);self.export_gif.setEnabled(not utility);self.keep_avi.setEnabled(not utility);self.add.setEnabled(True)
        if batch:self.subtype_label.setText('Contenido');self.type_info.setText('Operación batch: se usa el runner C11-C selectivo y su estado de Resume.')
        if utility:self.type_info.setText('Ejecuta la regresión lógica completa con el runner oficial.')
    def _seed_mode_changed(self,idx):
        active=self.operation.currentData()=='A_LA_CARTA'; manual=idx==1;self.manual.setEnabled(active and manual);
        for r in self.rows:r.set_interactive(active)
    def _randomize_all(self):
        if self.grammar.count():self.grammar.setCurrentIndex(0)
        for r in self.rows:r.set_random()
    def _new_unique_seeds(self,count:int)->list[int]:
        seeds=[];seen=set()
        while len(seeds)<count:
            value=random.randint(1000000,2147483646)
            if value not in seen:
                seen.add(value);seeds.append(value)
        return seeds
    def _manual_seeds(self):
        vals=[int(x.strip()) for x in self.manual.text().split(',') if x.strip()]
        if not vals or any(x<1 or x>2147483646 for x in vals) or len(set(vals))!=len(vals):raise ValueError('Seeds inválidas: deben ser enteros únicos entre 1 y 2147483646.')
        if len(vals)!=self.count.value():raise ValueError(f'Necesitas exactamente {self.count.value()} seeds manuales.')
        return vals
    def _add(self):
        try:
            op=str(self.operation.currentData())
            if op=='RUN_REGRESSION':
                r=Recipe(op,'utility',workers=int(self.workers.value()));self.queue.append(r);self._add_row(r);return
            if op!='A_LA_CARTA':
                r=Recipe(op,'batch',count=1,workers=int(self.workers.value()),resume=self.resume.isChecked(),reset=self.reset.isChecked(),export_gif=self.export_gif.isChecked(),no_sound=self.no_sound.isChecked(),keep_avi=self.keep_avi.isChecked());self.queue.append(r);self._add_row(r);return
            vt=str(self.video_type.currentData());manual=self._manual_seeds() if self.seed_mode.currentIndex()==1 else []
            if vt=='challenges':
                cid=str(self.grammar.currentData() or '');
                if not cid:raise ValueError('Selecciona un Challenge ID.')
                r=Recipe(op,vt,family=str(self.family.currentText()),grammar='auto',challenge_id=cid,count=self.count.value(),manual_seeds=manual,no_sound=self.no_sound.isChecked(),force=self.force.isChecked(),delivery='META_REELS_FINAL_V1' if self.delivery.currentIndex()==1 else 'REVIEW_720')
            else:
                fid=list(FAMILIES if vt=='visual_loops' else SCHEMA['drills'])[self.family.currentIndex()];targets={k:v for row in self.rows if (v:=row.value()) is not None for k in [row.spec['key']]};grammar=str(self.grammar.currentData() or 'auto')
                if vt=='visual_loops' and manual and (grammar!='auto' or targets):raise ValueError('Con seeds manuales, deja subfamilia/parámetros en ALEATORIO; el perfil determinista lo fija la seed.')
                r=Recipe(op,vt,family=fid,grammar=grammar,count=self.count.value(),manual_seeds=manual,no_sound=self.no_sound.isChecked(),no_footer=self.no_footer.isChecked(),force=self.force.isChecked(),workers=1,targets=targets,delivery=self.delivery.currentData() or 'C11C_REVIEW_720')
            self.queue.append(r);self._add_row(r)
        except Exception as e:QMessageBox.warning(self,'Configuración inválida',str(e))
    def _add_row(self,r):
        row=self.table.rowCount();self.table.insertRow(row);vals=[r.operation,r.video_type,r.family or r.challenge_id,r.grammar or '—',str(r.count),r.delivery,str(r.workers),'EN COLA']
        for i,v in enumerate(vals):self.table.setItem(row,i,QTableWidgetItem(v))
    def remove_selected(self):
        rows=sorted({x.row() for x in self.table.selectedIndexes()},reverse=True)
        for i in rows:
            if not self.proc and 0<=i<len(self.queue):self.queue.pop(i);self.table.removeRow(i)
    def _clear(self):
        if self.proc:return
        self.queue.clear();self.table.setRowCount(0)
    def start(self):
        if self.proc or not self.queue:return
        self.generate.setEnabled(False);self._run_recipe()
    def _run_recipe(self):
        if not self.queue:self.log.appendPlainText('\n=== PRODUCCIÓN FINALIZADA ===');self.generate.setEnabled(True);return
        self.current_recipe=self.queue[0];self.jobs=[];self.table.selectRow(0);r=self.current_recipe
        if r.operation=='RUN_REGRESSION':return self._launch_python_regression()
        if r.operation!='A_LA_CARTA':
            script=str(PROJECT/'tools/prototypes/c11c_bulk/run_c11c_art_direction_batch_v4.ps1');args=['-NoProfile','-ExecutionPolicy','Bypass','-File',script,'-Workers',str(r.workers)]
            mapping={'REVIEW_LOOPS':['-Loops'],'REVIEW_DRILLS':['-Drills'],'REVIEW_LONGFORMS':['-Longforms'],'REVIEW_LOOPS_DRILLS':['-Loops','-Drills'],'REVIEW_LOOPS_LONGFORMS':['-Loops','-Longforms'],'REVIEW_DRILLS_LONGFORMS':['-Drills','-Longforms'],'REVIEW_ALL':['-All']}
            args += mapping.get(r.operation,[])
            if r.resume:args.append('-Resume')
            if r.reset:args.append('-Reset')
            if r.export_gif:args.append('-ExportGif')
            if r.no_sound:args.append('-NoSound')
            self.table.setItem(0,7,QTableWidgetItem('REVIEW'));return self._launch(args)
        if r.video_type=='challenges':
            self.jobs=list(r.manual_seeds) if r.manual_seeds else self._new_unique_seeds(r.count);return self._run_challenge_job()
        if r.video_type=='visual_drills':
            self.jobs=list(r.manual_seeds) if r.manual_seeds else self._new_unique_seeds(r.count);return self._run_content_job()
        self._prepare_loop_jobs()
    def _prepare_loop_jobs(self):
        r=self.current_recipe
        if r.manual_seeds:self.jobs=list(r.manual_seeds);return self._run_content_job()
        if r.grammar=='auto' and not r.targets:
            self.jobs=[];existing=self._existing(r.family); 
            while len(self.jobs)<r.count:
                s=random.randint(1000000,2147483646)
                if s not in existing and s not in self.jobs:self.jobs.append(s)
            self.log.appendPlainText('[SEEDS RANDOM] '+', '.join(map(str,self.jobs)));return self._run_content_job()
        req={'family':FAMILIES[r.family]['internal'],'count':r.count,'target':dict(r.targets or {}),'excluded_seeds':sorted(self._existing(r.family)),'max_candidates':300000,'start_seed':random.randint(1000000,2147483646)}
        if r.grammar!='auto':req['target']['grammar_name']=r.grammar
        self.probe_file=ROOT/'.runtime'/'request.json';self.probe_file.parent.mkdir(parents=True,exist_ok=True);self.probe_file.write_text(json.dumps(req,ensure_ascii=False),encoding='utf-8');answer=ROOT/'.runtime'/'response.json';answer.unlink(missing_ok=True);self.log.appendPlainText('[SEED PLANNER] Buscando seeds compatibles…')
        self.proc=QProcess(self);self.proc.setWorkingDirectory(str(PROJECT));self.proc.setProgram('godot');self.proc.setArguments(['--headless','--path',str(PROJECT),'--script',str(ROOT/'seed_probe.gd'),'--',str(self.probe_file)]);self.proc.readyReadStandardOutput.connect(self._out);self.proc.readyReadStandardError.connect(self._err);self.proc.finished.connect(self._probe_done);self.proc.start()
    def _probe_done(self,code,status):
        p=self.proc;self.proc=None;self._out();self._err();
        if p:p.deleteLater()
        answer=ROOT/'.runtime'/'response.json';payload=None
        if answer.exists():
            try:payload=json.loads(answer.read_text(encoding='utf-8'))
            except Exception as e:payload={'ok':False,'error':str(e)}
            answer.unlink(missing_ok=True)
        if self.probe_file:self.probe_file.unlink(missing_ok=True);self.probe_file=None
        if code!=0 or not payload or not payload.get('ok'):self._finish_error((payload or {}).get('error',f'seed_probe exit {code}'));return
        self.jobs=[int(x['seed']) for x in payload['results']];self.log.appendPlainText('[SEEDS PLANNER] '+', '.join(map(str,self.jobs)));self._run_content_job()
    def _finish_error(self,msg):
        self.log.appendPlainText('[ERROR] '+msg);self.generate.setEnabled(True);QMessageBox.critical(self,'Proceso fallido',msg)
    def _existing(self,family):
        base=PROJECT/'artifacts/production/audiovisual'/family;out=set()
        if base.exists():
            for p in base.glob('*_seed_*'):
                m=re.search(r'_seed_(\d+)$',p.name)
                if m:out.add(int(m.group(1)))
        return out
    def _run_challenge_job(self):
        if not self.jobs:return self._job_complete()
        seed=self.jobs.pop(0);r=self.current_recipe;script=str(PROJECT/'tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1');args=['-NoProfile','-ExecutionPolicy','Bypass','-File',script,'-ChallengeId',r.challenge_id,'-Seed',str(seed),'-DeliveryProfile',r.delivery]
        if r.no_sound:args.append('-NoSound')
        if r.force:args.append('-Force')
        if r.export_gif:args.append('-ExportGif')
        if r.keep_avi:args.append('-KeepAvi')
        self.table.setItem(0,7,QTableWidgetItem(f'CHALLENGE {seed}'));self._launch(args)
    def _run_content_job(self):
        if not self.jobs:return self._job_complete()
        seed=self.jobs.pop(0);r=self.current_recipe
        if r.video_type=='visual_drills':
            tier=int(r.grammar) if r.grammar not in ('auto','AUTO') else random.randint(1,5);params=r.targets or {};speed=float(params.get('speed_multiplier',random.uniform(*SCHEMA['drills'][r.family].get('random_speed_range',[1.0,1.0]))));pacing=str(params.get('pacing_mode',random.choice(['constant','accelerating','pulsed'])) if r.family=='tracking' else 'constant');script=str(ROOT/'run_visual_drill_production.ps1');args=['-NoProfile','-ExecutionPolicy','Bypass','-File',script,'-Family',r.family,'-Seed',str(seed),'-DifficultyTier',str(tier),'-SpeedMultiplier',f'{speed:.5f}','-PacingMode',pacing,'-DeliveryProfile',r.delivery]
        else:
            script=str(PROJECT/'tools/prototypes/c11c_bulk/run_c11c_production.ps1');args=['-NoProfile','-ExecutionPolicy','Bypass','-File',script,'-Family',r.family,'-Seed',str(seed)]
            if r.grammar and r.grammar!='auto':args += ['-Grammar',r.grammar]
        if r.no_sound:args.append('-NoSound')
        if r.no_footer:args.append('-NoFooter')
        if r.force:args.append('-Force')
        if r.export_gif:args.append('-ExportGif')
        if r.keep_avi:args.append('-KeepAvi')
        self.table.setItem(0,7,QTableWidgetItem(f'GENERANDO {seed}'));self._launch(args)
    def _job_complete(self):
        self.table.setItem(0,7,QTableWidgetItem('COMPLETADA'));self.queue.pop(0);self.table.removeRow(0);self.current_recipe=None;QTimer.singleShot(0,self._run_recipe)
    def _launch_python_regression(self):
        self.log.appendPlainText('[LAUNCH] python .\\tests\\run_all.py');self.proc=QProcess(self);self.proc.setWorkingDirectory(str(PROJECT));self.proc.setProgram(sys.executable);self.proc.setArguments([str(PROJECT/'tests/run_all.py')]);self.proc.readyReadStandardOutput.connect(self._out);self.proc.readyReadStandardError.connect(self._err);self.proc.finished.connect(self._done);self.proc.start()
    def _launch(self,args):
        self.log.appendPlainText('\n[LAUNCH] powershell.exe '+' '.join(args));self.proc=QProcess(self);self.proc.setWorkingDirectory(str(PROJECT));self.proc.setProgram('powershell.exe');self.proc.setArguments(args);self.proc.readyReadStandardOutput.connect(self._out);self.proc.readyReadStandardError.connect(self._err);self.proc.finished.connect(self._done);self.proc.start()
    def _out(self):
        if self.proc:
            d=bytes(self.proc.readAllStandardOutput()).decode(errors='replace');
            if d:self.log.appendPlainText(d.rstrip())
    def _err(self):
        if self.proc:
            d=bytes(self.proc.readAllStandardError()).decode(errors='replace');
            if d:self.log.appendPlainText('[STDERR] '+d.rstrip())
    def _done(self,code,status):
        self._out();self._err();p=self.proc;self.proc=None
        if p:p.deleteLater()
        if code!=0:self.table.setItem(0,7,QTableWidgetItem('ERROR'));self.generate.setEnabled(True);QMessageBox.critical(self,'Proceso fallido',f'Launcher terminó con código {code}. Revisa el LOG.');return
        r=self.current_recipe
        if not r: return
        if r.operation=='RUN_REGRESSION':return self._job_complete()
        if r.video_type=='challenges':return self._run_challenge_job()
        if r.operation=='A_LA_CARTA':return self._run_content_job()
        self._job_complete()
    def _check_backend(self):
        profile=PROJECT/SCHEMA['backend_profile_source'];
        if not profile.exists():self.backend_info.setText('BACKEND: no encontrado');self.generate.setEnabled(False);return
        actual=hashlib.sha256(profile.read_bytes()).hexdigest();expected=SCHEMA['backend_profile_sha256'];ok=actual==expected;self.backend_info.setText(('BACKEND C11-C 2.16.9 FROZEN · OK' if ok else 'BACKEND HASH MISMATCH'))
        if not ok:self.generate.setEnabled(False);QTimer.singleShot(0,lambda:QMessageBox.critical(self,'Backend incompatible',f'Hash esperado {expected}\nHash actual {actual}'))

STYLE='''
QWidget{background:#f3f5f7;color:#1b2430;font-family:"Segoe UI";font-size:13px;} QLabel{background:transparent;}
QFrame#Banner{background:#fff;border:1px solid #d3dae2;border-radius:10px;min-height:60px;} QLabel#Title{font-size:22px;font-weight:700;color:#111827;} QLabel#Muted,QLabel#Hint{color:#5b6775;}
QGroupBox{background:#fff;border:1px solid #d3dae2;border-radius:9px;margin-top:10px;padding:10px;font-weight:700;}
QComboBox,QLineEdit,QSpinBox,QDoubleSpinBox{background:#fff;color:#17212b;border:1px solid #9aa7b5;border-radius:6px;min-height:40px;padding:0 10px;font-size:14px;}
QComboBox:focus,QLineEdit:focus,QSpinBox:focus,QDoubleSpinBox:focus{border:2px solid #2563eb;}
QComboBox::drop-down{width:34px;border-left:1px solid #aab5c0;background:#edf2f7;}
QComboBox QAbstractItemView{background:#fff;color:#17212b;border:1px solid #9aa7b5;selection-background-color:#dbeafe;selection-color:#111827;outline:0;padding:5px;} QComboBox QAbstractItemView::item{min-height:34px;padding:6px 8px;}
QCheckBox{min-height:30px;spacing:7px;} QCheckBox::indicator{width:18px;height:18px;}
QPushButton{background:#fff;color:#17212b;border:1px solid #9aa7b5;border-radius:7px;min-height:40px;padding:0 14px;font-weight:600;} QPushButton:hover{background:#eef4fb;}
QPushButton#Primary{background:#2563eb;color:#fff;border-color:#2563eb;min-height:46px;font-size:15px;} QPushButton#Primary:hover{background:#1d4ed8;}
QTableWidget,QPlainTextEdit{background:#fff;color:#17212b;border:1px solid #9aa7b5;border-radius:6px;} QHeaderView::section{background:#e9eef3;padding:8px;font-weight:700;border:0;min-height:26px;}
QScrollArea{border:0;background:#fff;} QScrollBar:vertical{width:14px;background:#e6ebf0;} QScrollBar::handle:vertical{background:#aeb9c5;min-height:34px;border-radius:7px;}
'''

if __name__=='__main__':
    app=QApplication(sys.argv);app.setFont(QFont('Segoe UI',10));app.setStyleSheet(STYLE);w=MainWindow();w.show();raise SystemExit(app.exec())
