"""Bereitet Schreibvorgänge für die Dashboard-Datenbank vor.

Aufruf: python3 scraper/dashboard_export.py OUT_DIR [versions.json] [key ...]
  - schreibt pro Eintrag aus data/dashboard.json eine JSON-Datei nach OUT_DIR
  - gibt die `writes`-Liste für ArtifactData(action="batch") aus (max. 50 pro Batch)
  - versions.json: {"<doc_id>": version, "summary": version} aus einem vorherigen
    ArtifactData-list; bestehende Dokumente brauchen if_version, neue nicht.
  - optionale keys: nur diese Einträge (plus meta/summary) exportieren.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
versions = json.load(open(sys.argv[2])) if len(sys.argv) > 2 and sys.argv[2].endswith(".json") else {}
only = set(a for a in sys.argv[2:] if not a.endswith(".json"))
d = json.load(open(ROOT / "data" / "dashboard.json"))
writes = []
for l in d["listings"]:
    if only and l["key"] not in only:
        continue
    p = out / f"{l['key']}.json"
    p.write_text(json.dumps({k: v for k, v in l.items() if k != "key"}, ensure_ascii=False))
    w = {"op": "set", "collection": "listings", "doc_id": l["key"], "file_path": str(p)}
    if l["key"] in versions:
        w["if_version"] = versions[l["key"]]
    writes.append(w)
p = out / "meta-summary.json"
p.write_text(json.dumps(d["meta"], ensure_ascii=False))
w = {"op": "set", "collection": "meta", "doc_id": "summary", "file_path": str(p)}
if "summary" in versions:
    w["if_version"] = versions["summary"]
writes.append(w)
print(json.dumps(writes))
