from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
main=(ROOT/'c11c-catalog'/'main.py').read_text(encoding='utf-8')
assert "C11-C / C11-D CATALOG 0.2.0" in main
assert "C11-D PRODUCTS / PROVENANCE" in main
assert 'build_catalog_data(PROJECT_ROOT)' in main
assert 'COPIAR COMANDO CANÓNICO' in main
assert 'NOT_REGISTERED_FOR_D8_RELEASE' in (ROOT/'c11c-catalog'/'c11d_catalog.py').read_text(encoding='utf-8')
manifest=json.loads((ROOT/'c11c-catalog'/'BUILD_MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['version']=='0.2.0'
assert manifest['d_records'] is True
assert manifest['release_authority']=='NONE'
assert manifest['d9_13_cross_suite_lifecycle_projection'] is True
assert 'CROSS-SUITE LIFECYCLE' in main and 'CROSS_SUITE_LIFECYCLE_INTENT' in main
assert manifest['d9_13_media_created'] is False
print('C11-C Catalog GUI contract PASS | version=0.2.0 | D product provenance/replay + D9.13 lifecycle intent=REGISTERED | media=false | release_authority=NONE')
