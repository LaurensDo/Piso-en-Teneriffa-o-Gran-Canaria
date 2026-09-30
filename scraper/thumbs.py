"""Fotos für das Dashboard: lädt bis zu 3 Bilder je Eintrag, schneidet auf 480x320 zu (JPEG)
und bereitet sie als Dokumente für die Dashboard-Datenbank vor (Collection "thumbs",
Dokument-ID "<key>-<n>", Feld img = data:-URI). Setzt listing.photos in data/dashboard.json.

Aufruf: python3 scraper/thumbs.py OUT_DIR [key ...]
  ohne keys: alle Einträge mit tier top/ask, die noch kein Feld "photos" haben.
Ausgabe: OUT_DIR/batches.json = Liste von writes-Listen für ArtifactData(action="batch").
"""
import base64, io, json, pathlib, subprocess, sys
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
W, H, N, QUALITY = 480, 320, 3, 62
MAX_BATCH_BYTES, MAX_BATCH_WRITES = 900_000, 50

out = pathlib.Path(sys.argv[1]); (out / "thumbs").mkdir(parents=True, exist_ok=True)
only = set(sys.argv[2:])
imgs = {}
for name, prefix in (("fotocasa", "fc-"), ("milanuncios", "ma-")):
    p = ROOT / "data" / f"{name}_latest.json"
    if p.exists():
        for a in json.load(open(p))["ads"]:
            if a.get("images"):
                imgs[prefix + a["id"]] = a["images"]


def link_keys(l):
    """Primärer Key plus IDs aus weiteren Links (Dubletten auf dem anderen Portal)."""
    keys = [l["key"]]
    for x in l.get("links", []):
        u = x.get("url", "")
        if "fotocasa.es" in u:
            keys.append("fc-" + u.rstrip("/").split("/")[-2])
        elif "milanuncios.com" in u:
            keys.append("ma-" + u.rsplit("-", 1)[-1].replace(".htm", ""))
    return keys


def thumb(url):
    data = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", UA, url], capture_output=True).stdout
    im = Image.open(io.BytesIO(data)).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((max(W, round(im.width * s)), max(H, round(im.height * s))), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    buf = io.BytesIO()
    im.crop((l, t, l + W, t + H)).save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


dash_path = ROOT / "data" / "dashboard.json"
dash = json.load(open(dash_path))
writes = []
for l in dash["listings"]:
    if only:
        if l["key"] not in only:
            continue
    elif l["tier"] == "out" or "photos" in l:
        continue
    urls = next((imgs[k] for k in link_keys(l) if k in imgs), [])
    n = 0
    for u in urls:
        if n >= N:
            break
        try:
            uri = thumb(u)
        except Exception as e:  # kaputtes Bild überspringen
            print("skip", l["key"], u, e, file=sys.stderr)
            continue
        f = out / "thumbs" / f"{l['key']}-{n}.json"
        f.write_text(json.dumps({"img": uri}))
        writes.append({"op": "set", "collection": "thumbs", "doc_id": f"{l['key']}-{n}", "file_path": str(f), "_size": len(uri)})
        n += 1
    l["photos"] = n
    print(l["key"], n, "Fotos")
dash_path.write_text(json.dumps(dash, ensure_ascii=False, indent=1))

batches, cur, size = [], [], 0
for w in writes:
    sz = w.pop("_size")
    if cur and (size + sz > MAX_BATCH_BYTES or len(cur) >= MAX_BATCH_WRITES):
        batches.append(cur); cur, size = [], 0
    cur.append(w); size += sz
if cur:
    batches.append(cur)
(out / "batches.json").write_text(json.dumps(batches))
print(len(writes), "Fotos in", len(batches), "Batches ->", out / "batches.json")
