import json
from datetime import datetime
from pathlib import Path
class SnapshotService:
 def __init__(self,folder):self.folder=Path(folder);self.folder.mkdir(parents=True,exist_ok=True)
 def save(self,data,name=None):
  name=name or "snapshot_"+datetime.now().strftime("%Y%m%d_%H%M%S")
  p=self.folder/(name+".json");p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8");return p
 def list(self):return sorted(self.folder.glob("*.json"))
 def load(self,path):return json.loads(Path(path).read_text(encoding="utf-8-sig"))
