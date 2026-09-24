import re

_STAGE=[
 ("RENDERING",re.compile(r"Movie Maker mode enabled|Done recording|START family|Start recording",re.I)),
 ("AUDIO",re.compile(r"C11-C-AUDIO|AMBIENT|AUDIO",re.I)),
 ("MUXING",re.compile(r"mux|ffmpeg",re.I)),
 ("VALIDATING",re.compile(r"ffprobe|validation|validat",re.I)),
 ("PUBLISHED",re.compile(r"published|production complete|PRODUCTION-25",re.I)),
]
_PROGRESS=re.compile(r"(?:Overall|Products|product|render)\s*[:=]?\s*(\d+)\s*/\s*(\d+)",re.I)
_FAMILY=re.compile(r"family=([A-Za-z0-9_]+)")
_SEED=re.compile(r"seed=([0-9]+)")
_RES=re.compile(r"recording movie in (\d+x\d+)",re.I)

class ParsedLine:
    def __init__(self,stage=None,progress=None,family=None,seed=None,resolution=None): self.stage=stage; self.progress=progress; self.family=family; self.seed=seed; self.resolution=resolution

def parse(text):
    stage=next((s for s,r in _STAGE if r.search(text)),None)
    m=_PROGRESS.search(text); prog=int(round(100*int(m.group(1))/int(m.group(2)))) if m and int(m.group(2)) else None
    fm=_FAMILY.search(text); sm=_SEED.search(text); rm=_RES.search(text)
    return ParsedLine(stage,prog,fm.group(1) if fm else None,int(sm.group(1)) if sm else None,rm.group(1) if rm else None)
