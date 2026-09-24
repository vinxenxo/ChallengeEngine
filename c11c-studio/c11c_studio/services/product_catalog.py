import json,re
from pathlib import Path
from ..domain.product import Product

class ProductCatalog:
    def __init__(self,ctx):self.ctx=ctx
    def list_products(self):
        out=[]; root=self.ctx.paths.production
        if not root.exists():return out
        for fam in sorted(root.iterdir()):
            if not fam.is_dir() or fam.name.startswith("_"):continue
            for d in sorted(fam.iterdir()):
                if not d.is_dir():continue
                m=re.search(r"seed_(\d+)",d.name,re.I); seed=int(m.group(1)) if m else None
                files={"mp4":next(iter(d.glob("*.mp4")),None),"gif":next(iter(d.glob("*.gif")),None),"wav":next(iter(d.glob("*.wav")),None),"manifest":next(iter(d.glob("*manifest*.json")),None),"ffprobe":next(iter(d.glob("*ffprobe*.json")),None),"social":next(iter(d.glob("*_social.txt")),None),"log":next(iter(d.glob("*.log")),None),"product_txt":d/"PRODUCT.txt"}
                files={k:v for k,v in files.items() if v and v.exists()}
                meta={}
                if files.get("manifest"):
                    try:meta=json.loads(files["manifest"].read_text(encoding="utf-8-sig"))
                    except Exception:pass
                status="PUBLISHED" if files.get("mp4") else "INCOMPLETE"
                out.append(Product(d.name,fam.name,seed,d,status,files,meta))
        return out
