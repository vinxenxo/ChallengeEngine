from __future__ import annotations
import hashlib, json, os, random, re, sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from PySide6.QtCore import QProcess, QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication,QCheckBox,QComboBox,QDoubleSpinBox,QFrame,QGridLayout,QGroupBox,QHBoxLayout,QLabel,QLineEdit,QMainWindow,QMessageBox,QPlainTextEdit,QPushButton,QScrollArea,QSizePolicy,QSpinBox,QTableWidget,QTableWidgetItem,QVBoxLayout,QWidget

APP_VERSION='0.4.0'
ROOT=Path(__file__).resolve().parent
PROJECT=Path(os.environ.get('C11C_PROJECT_ROOT',ROOT.parent)).resolve()
SCHEMA=json.loads((ROOT/'producer_schema.json').read_text(encoding='utf-8'))
FAMILIES=SCHEMA['families']
VIDEO_TYPES=[('CHALLENGES','challenges'),('VISUAL LOOPS','visual_loops'),('VISUAL DRILLS','visual_drills')]

@dataclass
class Recipe:
    video_type:str; family:str; grammar:str; count:int; manual_seeds:list[int]; no_sound:bool; no_footer:bool; force:bool; targets:dict[str,Any]

class ParamRow(QWidget):
    def __init__(self,spec):
        super().__init__(); self.spec=spec
        lay=QHBoxLayout(self); lay.setContentsMargins(0,1,0,1); lay.setSpacing(8)
        self.label=QLabel(spec['label']); self.label.setMinimumWidth(155)
        self.mode=QComboBox(); self.mode.addItems(['ALEATORIO (seed)','FIJAR']); self.mode.setFixedWidth(155)
        if spec['kind']=='enum':
            self.editor=QComboBox(); self.editor.addItems([str(x) for x in spec['values']])
        else:
            self.editor=QDoubleSpinBox(); self.editor.setRange(float(spec['min']),float(spec['max'])); self.editor.setSingleStep(float(spec['step'])); self.editor.setDecimals(5 if float(spec['step'])<0.001 else 3 if float(spec['step'])<0.01 else 2); self.editor.setValue((float(spec['min'])+float(spec['max']))/2)
        self.editor.setEnabled(False); self.editor.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        lay.addWidget(self.label); lay.addWidget(self.mode); lay.addWidget(self.editor,1)
        self.mode.currentIndexChanged.connect(lambda i:self.editor.setEnabled(i==1))
    def set_random(self): self.mode.setCurrentIndex(0)
    def value(self):
        if self.mode.currentIndex()==0:return None
        if self.spec['kind']=='enum':
            s=self.editor.currentText()
            try:return int(s)
            except ValueError:return s
        return float(self.editor.value())
    def set_interactive(self,enabled:bool):
        self.setEnabled(enabled)
        if not enabled: self.set_random()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle(f'C11-C Producer {APP_VERSION}'); self.resize(1260,900)
        self.queue=[]; self.current_recipe=None; self.jobs=[]; self.proc=None; self.probe_file=None; self.rows=[]
        self._build(); self._check_backend()

    def _build(self):
        root=QWidget(); self.setCentralWidget(root); main=QVBoxLayout(root); main.setContentsMargins(14,14,14,14); main.setSpacing(10)
        banner=QFrame(); banner.setObjectName('Banner'); bl=QHBoxLayout(banner); bl.setContentsMargins(16,9,16,9); t=QLabel('C11-C PRODUCER'); t.setObjectName('Title'); bl.addWidget(t); bl.addStretch(); self.backend_info=QLabel(''); self.backend_info.setObjectName('Muted'); bl.addWidget(self.backend_info); main.addWidget(banner)
        cols=QHBoxLayout(); cols.setSpacing(10); cols.addWidget(self._build_recipe(),1); cols.addWidget(self._build_queue(),1); main.addLayout(cols,1)

    def _build_recipe(self):
        box=QGroupBox('CREAR PRODUCCIÓN'); root=QVBoxLayout(box); root.setSpacing(8)
        grid=QGridLayout(); grid.setHorizontalSpacing(10); grid.setVerticalSpacing(8)
        self.video_type=QComboBox(); self.video_type.addItem('CHALLENGES','challenges'); self.video_type.addItem('VISUAL LOOPS','visual_loops'); self.video_type.addItem('VISUAL DRILLS','visual_drills'); self.video_type.setCurrentIndex(1)
        self.family=QComboBox(); self.family.addItems([v['name'] for v in FAMILIES.values()])
        self.grammar=QComboBox(); self.count=QSpinBox(); self.count.setRange(1,500); self.count.setValue(1)
        self.seed_mode=QComboBox(); self.seed_mode.addItems(['SEEDS ALEATORIAS','SEEDS MANUALES'])
        self.manual=QLineEdit(); self.manual.setPlaceholderText('Una seed por vídeo: 314159, 271828…'); self.manual.setEnabled(False)
        self.video_type_label=QLabel('Tipo de vídeo'); self.family_label=QLabel('Familia'); self.subtype_label=QLabel('Subfamilia'); self.count_label=QLabel('Cantidad'); self.seed_label=QLabel('Seeds')
        for row,label,w in [(0,self.video_type_label,self.video_type),(1,self.family_label,self.family),(2,self.subtype_label,self.grammar),(3,self.count_label,self.count),(4,self.seed_label,self.seed_mode)]: grid.addWidget(label,row,0); grid.addWidget(w,row,1)
        grid.addWidget(self.manual,5,0,1,2); root.addLayout(grid)
        self.type_info=QLabel('Visual Loops disponible. Challenges y Visual Drills se conectarán en fases posteriores.'); self.type_info.setObjectName('Hint'); self.type_info.setWordWrap(True); root.addWidget(self.type_info)
        opts=QHBoxLayout(); self.no_sound=QCheckBox('Sin audio'); self.no_footer=QCheckBox('Sin footer'); self.force=QCheckBox('FORCE'); opts.addWidget(self.no_sound); opts.addWidget(self.no_footer); opts.addWidget(self.force); opts.addStretch(); root.addLayout(opts)
        pbox=QGroupBox('VARIACIÓN · por defecto ALEATORIA por seed'); pl=QVBoxLayout(pbox); pl.setContentsMargins(8,8,8,8)
        self.randomize=QPushButton('PONER TODO EN ALEATORIO'); pl.addWidget(self.randomize)
        self.pscroll=QScrollArea(); self.pscroll.setWidgetResizable(True); self.pscroll.setFrameShape(QFrame.NoFrame); self.pwidget=QWidget(); self.pl=QVBoxLayout(self.pwidget); self.pl.setContentsMargins(4,4,4,4); self.pl.setSpacing(3); self.pl.setAlignment(Qt.AlignTop); self.pscroll.setWidget(self.pwidget); pl.addWidget(self.pscroll,1); root.addWidget(pbox,1)
        hint=QLabel('C11-C genera el perfil desde la seed. Puedes dejar cada parámetro en ALEATORIO o FIJARLO; en este segundo caso se busca una seed compatible.'); hint.setWordWrap(True); hint.setObjectName('Hint'); root.addWidget(hint)
        self.add=QPushButton('AÑADIR A LA COLA'); self.add.setObjectName('Primary'); self.add.setMinimumHeight(46); root.addWidget(self.add)
        self.video_type.currentIndexChanged.connect(self._video_type_changed); self.family.currentIndexChanged.connect(self._refresh_family); self.seed_mode.currentIndexChanged.connect(self._seed_mode_changed); self.randomize.clicked.connect(self._randomize_all); self.add.clicked.connect(self._add); self._refresh_family(0); self._video_type_changed(self.video_type.currentIndex()); return box

    def _build_queue(self):
        box=QGroupBox('COLA DE PRODUCCIÓN'); root=QVBoxLayout(box); self.table=QTableWidget(0,7); self.table.setHorizontalHeaderLabels(['Tipo','Familia','Subfamilia','Cantidad','Audio','Footer','Estado']); self.table.setColumnWidth(0,110); self.table.setColumnWidth(1,145); self.table.setColumnWidth(2,165); self.table.setColumnWidth(3,70); root.addWidget(self.table,3)
        btns=QHBoxLayout(); self.generate=QPushButton('GENERAR'); self.generate.setObjectName('Primary'); self.generate.setMinimumHeight(48); self.remove=QPushButton('QUITAR'); self.clear=QPushButton('VACIAR'); btns.addWidget(self.generate,2); btns.addWidget(self.remove); btns.addWidget(self.clear); root.addLayout(btns)
        lbox=QGroupBox('PROGRESO / LOG'); ll=QVBoxLayout(lbox); self.log=QPlainTextEdit(); self.log.setReadOnly(True); ll.addWidget(self.log); root.addWidget(lbox,2)
        self.generate.clicked.connect(self.start); self.remove.clicked.connect(self.remove_selected); self.clear.clicked.connect(self._clear); return box

    def _video_type_changed(self,idx):
        video_type=str(self.video_type.currentData() or 'visual_loops')
        available=(video_type in ('visual_loops','visual_drills'))
        self.family.setEnabled(available)
        self.count.setEnabled(available)
        self.seed_mode.setEnabled(available)
        self.manual.setEnabled(available and self.seed_mode.currentIndex()==1)
        self.no_sound.setEnabled(available)
        self.no_footer.setEnabled(video_type=='visual_loops')
        self.force.setEnabled(available)
        self.randomize.setEnabled(available)
        self.add.setEnabled(available)
        if video_type=='visual_loops':
            self.subtype_label.setText('Subfamilia')
            self.grammar.setEnabled(self.seed_mode.currentIndex()!=1)
            self.type_info.setText('Visual Loops activo. Familia, subfamilia y variaciones usan el backend C11-C 2.9.1 real.')
        elif video_type=='visual_drills':
            self.subtype_label.setText('Dificultad')
            self.no_footer.setChecked(False)
            self.grammar.setEnabled(True)
            self._refresh_family(self.family.currentIndex() if self.family.count() else 0)
            self.type_info.setText('Visual Drills activo. 3 s de cuenta atrás + gameplay + 3 s de CTA.')
        else:
            self.subtype_label.setText('Subfamilia')
            self.family.clear(); self.grammar.clear()
            while self.pl.count():
                item=self.pl.takeAt(0); w=item.widget()
                if w: w.deleteLater()
            self.rows=[]
            self.grammar.setEnabled(False)
            self.type_info.setText('Challenges: selector preparado, generación aún no conectada en este Producer.')
        self._seed_mode_changed(self.seed_mode.currentIndex())

    def _clear_param_rows(self):
        while self.pl.count():
            item=self.pl.takeAt(0); w=item.widget()
            if w: w.deleteLater()
        self.rows=[]

    def _refresh_family(self,idx):
        video_type=str(self.video_type.currentData() or 'visual_loops')
        self._clear_param_rows()
        if video_type=='visual_loops':
            ids=list(FAMILIES)
            if not ids:return
            idx=max(0,min(idx,len(ids)-1)); self.fid=ids[idx]
            self.family.blockSignals(True); self.family.clear(); self.family.addItems([v['name'] for v in FAMILIES.values()]); self.family.setCurrentIndex(idx); self.family.blockSignals(False)
            self.grammar.clear(); self.grammar.addItem('ALEATORIO — por seed','auto')
            for code,label in FAMILIES[self.fid]['grammars'][1:]: self.grammar.addItem(label,code)
            for spec in FAMILIES[self.fid]['params']:
                r=ParamRow(spec); self.pl.addWidget(r); self.rows.append(r)
            self.type_info.setText('Visual Loops activo. Variación determinista del backend C11-C 2.9.1.')
        elif video_type=='visual_drills':
            ids=list(SCHEMA.get('drills',{}))
            if not ids:return
            idx=max(0,min(idx,len(ids)-1)); self.fid=ids[idx]
            self.family.blockSignals(True); self.family.clear(); self.family.addItems([v['name'] for v in SCHEMA['drills'].values()]); self.family.setCurrentIndex(idx); self.family.blockSignals(False)
            self.grammar.clear(); self.grammar.addItem('ALEATORIO — por vídeo','auto')
            for tier in range(1,6): self.grammar.addItem(f'TIER {tier}',tier)
            for spec in SCHEMA['drills'][self.fid].get('parameters',[]):
                r=ParamRow(spec); self.pl.addWidget(r); self.rows.append(r)
            self.type_info.setText('Visual Drills activo. 3 s de cuenta atrás + gameplay + 3 s de CTA.')
        self._seed_mode_changed(self.seed_mode.currentIndex())

    def _seed_mode_changed(self,idx):
        manual=idx==1; active=self.video_type.currentData() in ('visual_loops','visual_drills')
        self.manual.setEnabled(manual and active)
        self.grammar.setEnabled(active)
        for r in self.rows: r.set_interactive(active)

    def _randomize_all(self):
        self.grammar.setCurrentIndex(0)
        for r in self.rows: r.set_random()

    def _check_backend(self):
        required=[PROJECT/'project.godot',PROJECT/SCHEMA['backend_profile_source'],PROJECT/'tools/prototypes/c11c_bulk/run_c11c_production.ps1']
        missing=[str(p) for p in required if not p.exists()]
        if missing: self.generate.setEnabled(False); QMessageBox.critical(self,'Backend no encontrado','Falta:\n'+'\n'.join(missing)); return
        actual=hashlib.sha256((PROJECT/SCHEMA['backend_profile_source']).read_bytes()).hexdigest()
        expected=SCHEMA.get('backend_profile_sha256','')
        if actual!=expected: self.generate.setEnabled(False); QMessageBox.critical(self,'Backend no esperado','El C11CVariationProfile.gd no coincide con el backend 2.9.1 usado para construir este Producer.'); return
        self.backend_info.setText(f'C11-C 2.9.1 · VariationProfile {SCHEMA["backend_profile_version"]} · 5 familias'); self.log.appendPlainText(f'Backend verificado: {PROJECT}')

    def _add(self):
        manual=[]
        if self.seed_mode.currentIndex()==1:
            try: manual=[int(x.strip()) for x in self.manual.text().split(',') if x.strip()]
            except ValueError: QMessageBox.warning(self,'Seeds','Las seeds deben ser enteros.'); return
            if len(manual)!=self.count.value() or len(set(manual))!=len(manual) or any(x<1 or x>2147483646 for x in manual): QMessageBox.warning(self,'Seeds',f'Necesitas exactamente {self.count.value()} seeds únicas entre 1 y 2147483646.'); return
        video_type=str(self.video_type.currentData() or 'visual_loops')
        if video_type not in ('visual_loops','visual_drills'):
            QMessageBox.information(self,'Tipo no disponible','Challenges todavía no tiene un launcher de producción conectado.'); return
        targets={r.spec['key']:v for r in self.rows if (v:=r.value()) is not None}; grammar=self.grammar.currentData() or 'auto'
        if video_type=='visual_loops':
            if targets.get('palette_name')=='AUTO (seed)': targets.pop('palette_name')
            if manual and (grammar!='auto' or targets): QMessageBox.warning(self,'Configuración incompatible','Con seeds manuales el perfil ya queda determinado por la seed. Usa SEEDS ALEATORIAS para fijar subfamilia o parámetros.'); return
        r=Recipe(video_type,str(self.fid),str(grammar),self.count.value(),manual,self.no_sound.isChecked(),self.no_footer.isChecked(),self.force.isChecked(),targets); self.queue.append(r); self._add_row(r)

    def _add_row(self,r):
        n=self.table.rowCount(); self.table.insertRow(n)
        if r.video_type=='visual_loops':
            g=next((l for c,l in FAMILIES[r.family]['grammars'] if c==r.grammar),'ALEATORIO — por seed')
            vals=['VISUAL LOOPS',FAMILIES[r.family]['name'],g,str(r.count),'NO' if r.no_sound else 'SI','NO' if r.no_footer else 'SI','PENDIENTE']
        else:
            g='ALEATORIO' if r.grammar=='auto' else f'TIER {r.grammar}'
            vals=['VISUAL DRILLS',SCHEMA['drills'][r.family]['name'],g,str(r.count),'NO' if r.no_sound else 'SI','—','PENDIENTE']
        for c,v in enumerate(vals): self.table.setItem(n,c,QTableWidgetItem(v))

    def remove_selected(self):
        n=self.table.currentRow()
        if n>=0 and n<len(self.queue) and not self.proc: self.queue.pop(n); self.table.removeRow(n)
    def _clear(self):
        if self.proc:return
        self.queue.clear(); self.table.setRowCount(0)
    def start(self):
        if self.proc or not self.queue:return
        self.generate.setEnabled(False); self._run_recipe()
    def _run_recipe(self):
        if not self.queue: self.log.appendPlainText('\n=== PRODUCCIÓN FINALIZADA ==='); self.generate.setEnabled(True); return
        self.current_recipe=self.queue[0]; self.jobs=[]; r=self.current_recipe; self.table.selectRow(0)
        if r.manual_seeds: self.jobs=list(r.manual_seeds); self.log.appendPlainText('[SEEDS MANUALES] '+', '.join(map(str,self.jobs))); self._run_job(); return
        if r.video_type=='visual_drills':
            existing=set(); base=PROJECT/'artifacts/production/audiovisual/visual_drills'/r.family
            if base.exists():
                for p in base.glob('*_seed_*'):
                    m=re.search(r'_seed_(\d+)',p.name)
                    if m: existing.add(int(m.group(1)))
            seeds=[]
            while len(seeds)<r.count:
                s=random.randint(1000000,2147483646)
                if s not in existing and s not in seeds: seeds.append(s)
            self.jobs=seeds; self.log.appendPlainText('[SEEDS RANDOM] '+', '.join(map(str,seeds))); self._run_job(); return
        if not r.targets and r.grammar=='auto':
            existing=self._existing(r.family); seeds=[]
            while len(seeds)<r.count:
                s=random.randint(1000000,2147483646)
                if s not in existing and s not in seeds: seeds.append(s)
            self.jobs=seeds; self.log.appendPlainText('[SEEDS RANDOM] '+', '.join(map(str,seeds))); self._run_job(); return
        req={'family':FAMILIES[r.family]['internal'],'count':r.count,'target':dict(r.targets),'excluded_seeds':sorted(self._existing(r.family)),'max_candidates':300000,'start_seed':random.randint(1000000,2147483646)}
        if r.grammar!='auto': req['target']['grammar_name']=r.grammar
        self.probe_file=ROOT/'.runtime'/'request.json'; self.probe_file.parent.mkdir(parents=True,exist_ok=True); self.probe_file.write_text(json.dumps(req,ensure_ascii=False),encoding='utf-8')
        answer=ROOT/'.runtime'/'response.json'; answer.unlink(missing_ok=True); self.log.appendPlainText('[SEED PLANNER] Buscando seeds compatibles…')
        self.proc=QProcess(self); self.proc.setWorkingDirectory(str(PROJECT)); self.proc.setProgram('godot'); self.proc.setArguments(['--headless','--path',str(PROJECT),'--script',str(ROOT/'seed_probe.gd'),'--',str(self.probe_file)]); self.proc.readyReadStandardOutput.connect(self._probe_out); self.proc.readyReadStandardError.connect(self._probe_err); self.proc.finished.connect(self._probe_done); self.proc.start()
    def _probe_out(self):
        if not self.proc:return
        d=bytes(self.proc.readAllStandardOutput()).decode(errors='replace')
        if d:self.log.appendPlainText(d.rstrip())
    def _probe_err(self):
        if not self.proc:return
        d=bytes(self.proc.readAllStandardError()).decode(errors='replace')
        if d:self.log.appendPlainText('[SEED PLANNER STDERR] '+d.rstrip())
    def _probe_done(self,code,status):
        p=self.proc; self.proc=None; self._probe_out(); self._probe_err();
        if p:p.deleteLater()
        if self.probe_file:self.probe_file.unlink(missing_ok=True)
        answer=ROOT/'.runtime'/'response.json'; payload=None
        if answer.exists():
            try: payload=json.loads(answer.read_text(encoding='utf-8'))
            except Exception as e: payload={'ok':False,'error':f'Respuesta inválida del seed planner: {e}'}
            finally: answer.unlink(missing_ok=True)
        if code!=0 or not payload or not payload.get('ok'):
            msg=(payload or {}).get('error',f'seed_probe terminó con código {code}'); self.log.appendPlainText('[SEED PLANNER ERROR] '+msg); QMessageBox.critical(self,'No hay seeds compatibles',msg); self.current_recipe=None; self._finish_error(); return
        self.jobs=[int(x['seed']) for x in payload['results']]; self.log.appendPlainText('[SEEDS PLANNER] '+', '.join(map(str,self.jobs))); self._run_job()
    def _finish_error(self): self.generate.setEnabled(True)
    def _existing(self,family):
        base=PROJECT/'artifacts/production/audiovisual'/family; out=set()
        if base.exists():
            for p in base.glob('*_seed_*'):
                m=re.search(r'_seed_(\d+)$',p.name)
                if m: out.add(int(m.group(1)))
        return out
    def _run_job(self):
        if not self.jobs:
            self.table.setItem(0,6,QTableWidgetItem('COMPLETADA')); self.queue.pop(0); self.table.removeRow(0); self.current_recipe=None; QTimer.singleShot(0,self._run_recipe); return
        seed=self.jobs.pop(0); r=self.current_recipe
        if r.video_type=='visual_drills':
            tier=int(r.grammar) if r.grammar!='auto' else random.randint(1,5)
            speed=float(r.targets['speed_multiplier']) if 'speed_multiplier' in r.targets else random.uniform(*SCHEMA['drills'][r.family]['random_speed_range']) if SCHEMA['drills'][r.family].get('random_speed_range') else 1.0
            if r.family=='tracking':
                pacing=str(r.targets['pacing_mode']) if 'pacing_mode' in r.targets else random.choice(['constant','accelerating','pulsed'])
            else:
                pacing='constant'
            script=str(ROOT/'run_visual_drill_production.ps1')
            args=['-NoProfile','-ExecutionPolicy','Bypass','-File',script,'-Family',r.family,'-Seed',str(seed),'-DifficultyTier',str(tier),'-SpeedMultiplier',f'{speed:.5f}','-PacingMode',pacing]
            if r.no_sound:args.append('-NoSound')
            if r.force:args.append('-Force')
            self.table.setItem(0,6,QTableWidgetItem(f'GENERANDO {seed} · T{tier}')); self.log.appendPlainText('\n[DRILL PRODUCTION] powershell.exe '+' '.join(args))
        else:
            script=str(PROJECT/'tools/prototypes/c11c_bulk/run_c11c_production.ps1'); args=['-NoProfile','-ExecutionPolicy','Bypass','-File',script,'-Family',r.family,'-Seed',str(seed)]
            if r.no_sound:args.append('-NoSound')
            if r.no_footer:args.append('-NoFooter')
            if r.force:args.append('-Force')
            self.table.setItem(0,6,QTableWidgetItem(f'GENERANDO {seed}')); self.log.appendPlainText('\n[PRODUCTION] powershell.exe '+' '.join(args))
        self.proc=QProcess(self); self.proc.setWorkingDirectory(str(PROJECT)); self.proc.setProgram('powershell.exe'); self.proc.setArguments(args); self.proc.readyReadStandardOutput.connect(self._out); self.proc.readyReadStandardError.connect(self._err); self.proc.finished.connect(self._prod_done); self.proc.start()
    def _out(self):
        if not self.proc:return
        d=bytes(self.proc.readAllStandardOutput()).decode(errors='replace');
        if d:self.log.appendPlainText(d.rstrip())
    def _err(self):
        if not self.proc:return
        d=bytes(self.proc.readAllStandardError()).decode(errors='replace');
        if d:self.log.appendPlainText('[STDERR] '+d.rstrip())
    def _prod_done(self,code,status):
        self._out(); self._err(); p=self.proc; self.proc=None
        if p:p.deleteLater()
        if code!=0:
            self.table.setItem(0,6,QTableWidgetItem('ERROR')); self.generate.setEnabled(True); QMessageBox.critical(self,'Producción fallida',f'Launcher terminó con código {code}. Revisa el LOG.'); return
        self.log.appendPlainText('[PRODUCTION] PASS'); QTimer.singleShot(0,self._run_job)

STYLE='''
QWidget{background:#f3f5f7;color:#1b2430;font-family:"Segoe UI";font-size:13px;} QLabel{background:transparent;}
QFrame#Banner{background:#fff;border:1px solid #d3dae2;border-radius:10px;min-height:60px;} QLabel#Title{font-size:22px;font-weight:700;color:#111827;} QLabel#Muted,QLabel#Hint{color:#5b6775;}
QGroupBox{background:#fff;border:1px solid #d3dae2;border-radius:9px;margin-top:10px;padding:10px;font-weight:700;}
QComboBox,QLineEdit,QSpinBox,QDoubleSpinBox{background:#fff;color:#17212b;border:1px solid #9aa7b5;border-radius:6px;min-height:40px;padding:0 10px;font-size:14px;}
QComboBox:focus,QLineEdit:focus,QSpinBox:focus,QDoubleSpinBox:focus{border:2px solid #2563eb;}
QComboBox::drop-down{width:34px;border-left:1px solid #aab5c0;background:#edf2f7;}
QComboBox QAbstractItemView{background:#fff;color:#17212b;border:1px solid #9aa7b5;selection-background-color:#dbeafe;selection-color:#111827;outline:0;padding:5px;}
QComboBox QAbstractItemView::item{min-height:34px;padding:6px 8px;}
QCheckBox{min-height:30px;spacing:7px;} QCheckBox::indicator{width:18px;height:18px;}
QPushButton{background:#fff;color:#17212b;border:1px solid #9aa7b5;border-radius:7px;min-height:40px;padding:0 14px;font-weight:600;} QPushButton:hover{background:#eef4fb;}
QPushButton#Primary{background:#2563eb;color:#fff;border-color:#2563eb;min-height:46px;font-size:15px;} QPushButton#Primary:hover{background:#1d4ed8;}
QTableWidget,QPlainTextEdit{background:#fff;color:#17212b;border:1px solid #9aa7b5;border-radius:6px;} QHeaderView::section{background:#e9eef3;padding:8px;font-weight:700;border:0;min-height:26px;}
QScrollArea{border:0;background:#fff;} QScrollBar:vertical{width:14px;background:#e6ebf0;} QScrollBar::handle:vertical{background:#aeb9c5;min-height:34px;border-radius:7px;}
'''

if __name__=='__main__':
    app=QApplication(sys.argv); app.setFont(QFont('Segoe UI',10)); w=MainWindow(); w.show(); raise SystemExit(app.exec())
